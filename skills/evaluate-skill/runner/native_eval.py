#!/usr/bin/env python3
"""Provider-native Evaluate Skill eval dispatch (experimental; isolated host required).

No cross-provider fallback. Preparing a case never starts a model.
"""
import argparse
from dataclasses import dataclass
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid
from typing import Any, Mapping, Optional, Sequence, Tuple

from capability_inventory import (
    inspect_installed_versions,
    inspect_platform_fingerprint,
    load_inventory,
)
from contracts import ApprovalReceipt, EnforcementReceipt, RunPlan
from codex_host import CodexHostPolicy
from evidence import (
    EvidenceBundle,
    EvidenceError,
    ExecutionStatus,
    SafetyStatus,
    evidence_bundle_digest,
    evidence_bundle_payload,
    provider_result_digest,
    provider_result_identity,
    sanitize_events,
    snapshot_tree,
)
from execution_policy import assess_run
from native_boundary import NativeBoundaryResult


_PROMPTFOO_SAFE_ENV = {
    'PROMPTFOO_DISABLE_REMOTE_GENERATION': '1',
    'PROMPTFOO_DISABLE_SHARING': '1',
    'PROMPTFOO_DISABLE_TELEMETRY': '1',
    'PROMPTFOO_DISABLE_UPDATE': '1',
}

class Blocked(Exception):
    pass


class QualityStatus(str, Enum):
    PASS = 'PASS'
    FAIL = 'FAIL'
    UNKNOWN = 'UNKNOWN'
    NOT_GRADED = 'NOT_GRADED'


@dataclass(frozen=True)
class ProofArmWorkspace:
    name: str
    workspace: Path
    fixture_digest: str


@dataclass(frozen=True)
class PreparedProofRun:
    run_id: str
    root: Path
    plan_digest: str
    arms: Tuple[ProofArmWorkspace, ...]


@dataclass(frozen=True)
class ProofArmResult:
    name: str
    provider_result: Optional[Path]
    execution_status: ExecutionStatus
    quality_status: QualityStatus
    safety_status: SafetyStatus
    evidence_bundle: Optional[EvidenceBundle]


@dataclass(frozen=True)
class ProofPairResult:
    run_id: str
    arms: Tuple[ProofArmResult, ...]

    @property
    def completed(self):
        if (
            len(self.arms) != 2
            or {arm.name for arm in self.arms} != {'with-skill', 'without-skill'}
            or any(
                arm.execution_status != ExecutionStatus.COMPLETED
                for arm in self.arms
            )
        ):
            return False
        workspace_ids = set()
        result_paths = set()
        execution_ids = set()
        receipt_nonces = set()
        source_result_digests = set()
        for arm in self.arms:
            bundle = arm.evidence_bundle
            if bundle is None or arm.provider_result is None:
                return False
            if (
                bundle.run_id != self.run_id
                or bundle.receipt_nonce != self.run_id
                or bundle.arm_name != arm.name
                or not bundle.workspace_id
                or bundle.audit.execution_status != ExecutionStatus.COMPLETED
                or arm.execution_status != bundle.audit.execution_status
                or arm.safety_status != bundle.audit.safety_status
            ):
                return False
            try:
                digest = provider_result_digest(arm.provider_result)
                result_path = str(arm.provider_result.resolve(strict=True))
            except (EvidenceError, OSError):
                return False
            if digest != bundle.provider_result_digest:
                return False
            workspace_ids.add(bundle.workspace_id)
            result_paths.add(result_path)
            execution_ids.add(bundle.execution_id)
            receipt_nonces.add(bundle.receipt_nonce)
            source_result_digests.add(bundle.source_result_digest)
        return (
            len(workspace_ids) == 2
            and len(result_paths) == 2
            and len(execution_ids) == 1
            and receipt_nonces == {self.run_id}
            and len(source_result_digests) == 1
        )

    @property
    def execution_status(self):
        statuses = {arm.execution_status for arm in self.arms}
        if ExecutionStatus.INFRA_ERROR in statuses:
            return ExecutionStatus.INFRA_ERROR
        if ExecutionStatus.BLOCKED in statuses:
            return ExecutionStatus.BLOCKED
        if self.completed:
            return ExecutionStatus.COMPLETED
        return ExecutionStatus.INCOMPLETE

    @property
    def quality_status(self):
        statuses = {arm.quality_status for arm in self.arms}
        if QualityStatus.FAIL in statuses:
            return QualityStatus.FAIL
        if QualityStatus.UNKNOWN in statuses:
            return QualityStatus.UNKNOWN
        if QualityStatus.NOT_GRADED in statuses or not statuses:
            return QualityStatus.NOT_GRADED
        if statuses == {QualityStatus.PASS}:
            return QualityStatus.PASS
        return QualityStatus.UNKNOWN

    @property
    def safety_status(self):
        statuses = {arm.safety_status for arm in self.arms}
        if SafetyStatus.FAIL in statuses:
            return SafetyStatus.FAIL
        if self.completed and statuses == {SafetyStatus.PASS}:
            return SafetyStatus.PASS
        return SafetyStatus.UNKNOWN


@dataclass(frozen=True)
class StageDecision:
    current_stage: int
    next_stage: Optional[int]
    advance: bool
    execution_status: ExecutionStatus
    quality_status: QualityStatus
    safety_status: SafetyStatus
    reasons: Tuple[str, ...]


def next_stage_decision(
    pair: ProofPairResult, *, current_stage: int
) -> StageDecision:
    """Gate Stage 3→4 or 9→10 without collapsing outcome dimensions."""
    if current_stage not in (3, 9):
        raise ValueError("stage transition is defined only for Stage 3 or Stage 9")
    if not isinstance(pair, ProofPairResult):
        raise TypeError("proof pair result is required")

    execution = pair.execution_status
    quality = pair.quality_status
    safety = pair.safety_status
    reasons = []
    if execution != ExecutionStatus.COMPLETED:
        reasons.append(f"execution status {execution.value}")
    if safety != SafetyStatus.PASS:
        reasons.append(f"safety status {safety.value}")
    names = tuple(arm.name for arm in pair.arms)
    if len(names) != 2 or set(names) != {'with-skill', 'without-skill'}:
        reasons.append("paired comparison arms incomplete")
    reasons = list(dict.fromkeys(reasons))
    advance = not reasons
    return StageDecision(
        current_stage=current_stage,
        next_stage=current_stage + 1 if advance else None,
        advance=advance,
        execution_status=execution,
        quality_status=quality,
        safety_status=safety,
        reasons=tuple(reasons),
    )


def write_stage_checkpoint(
    plan: RunPlan,
    pair: ProofPairResult,
    *,
    current_stage: int,
    destination: Path,
    execution_manifest: Path,
) -> Path:
    """Persist a plan-bound Stage 3/9 decision without replacing prior evidence."""
    if not isinstance(plan, RunPlan):
        raise TypeError("run plan is required")
    execution_manifest = Path(execution_manifest)
    if not execution_manifest.is_file() or execution_manifest.is_symlink():
        raise Blocked("host-finalized execution manifest is required")
    manifest = _json_file(execution_manifest, 'host-finalized execution manifest')
    if manifest.get('status') != 'HOST_AUDIT_COMPLETE':
        raise Blocked("execution manifest is not host-audit complete")
    if manifest.get('plan_digest') != plan.digest():
        raise Blocked("execution manifest does not match checkpoint run plan")
    if manifest.get('run_nonce') != pair.run_id:
        raise Blocked("execution manifest does not match proof pair run identity")
    source_result = _result_path(execution_manifest.parent, manifest)
    try:
        source_digest = provider_result_digest(source_result)
    except EvidenceError as exc:
        raise Blocked(f"execution source result cannot be revalidated: {exc}") from None
    if source_digest != manifest.get('provider_result_digest'):
        raise Blocked("execution source result changed after host finalization")
    observed_identity = _verified_provider_identity(
        source_result,
        plan,
        max_bytes=int(plan.resource_limits['max_output_bytes']),
    )
    if manifest.get('observed_provider_identity') != observed_identity:
        raise Blocked("execution manifest provider identity is missing or changed")
    expected_arm_digests = manifest.get('arm_evidence_digests')
    if not isinstance(expected_arm_digests, dict):
        raise Blocked("execution manifest is missing finalized arm evidence digests")
    for arm in pair.arms:
        bundle = arm.evidence_bundle
        if arm.execution_status == ExecutionStatus.COMPLETED and bundle is None:
            raise Blocked("completed arm requires a host evidence bundle")
        if bundle is not None and bundle.plan_digest != plan.digest():
            raise Blocked("arm evidence does not match checkpoint run plan")
        if bundle is not None and (
            bundle.execution_id != manifest.get('execution_id')
            or bundle.receipt_nonce != manifest.get('run_nonce')
            or bundle.source_result_digest != source_digest
            or expected_arm_digests.get(arm.name) != evidence_bundle_digest(bundle)
        ):
            raise Blocked("arm evidence does not match host-finalized execution")
    if set(expected_arm_digests) != {arm.name for arm in pair.arms}:
        raise Blocked("execution manifest arm evidence set is not exact")
    decision = next_stage_decision(pair, current_stage=current_stage)
    destination = Path(destination)
    parent = destination.parent
    if not parent.is_dir() or parent.is_symlink():
        raise Blocked("checkpoint parent must be a real existing directory")
    if destination.exists() or destination.is_symlink():
        raise Blocked("stage checkpoint already exists; preserve prior evidence")
    arm_payloads = []
    for arm in pair.arms:
        arm_bundle = arm.evidence_bundle
        arm_payloads.append({
            'name': arm.name,
            'provider_result': (
                str(arm.provider_result) if arm.provider_result is not None else None
            ),
            'provider_result_digest': (
                arm_bundle.provider_result_digest if arm_bundle is not None else None
            ),
            'source_result_digest': (
                arm_bundle.source_result_digest if arm_bundle is not None else None
            ),
            'workspace_id': (
                arm_bundle.workspace_id if arm_bundle is not None else None
            ),
            'receipt_nonce': (
                arm_bundle.receipt_nonce if arm_bundle is not None else None
            ),
            'execution_id': (
                arm_bundle.execution_id if arm_bundle is not None else None
            ),
            'evidence_bundle_digest': (
                evidence_bundle_digest(arm_bundle)
                if arm_bundle is not None else None
            ),
            'evidence_bundle': (
                evidence_bundle_payload(arm_bundle)
                if arm_bundle is not None else None
            ),
            'execution_status': arm.execution_status.value,
            'quality_status': arm.quality_status.value,
            'safety_status': arm.safety_status.value,
        })
    payload = {
        'schema_version': plan.schema_version,
        'plan_digest': plan.digest(),
        'run_id': pair.run_id,
        'current_stage': decision.current_stage,
        'next_stage': decision.next_stage,
        'advance': decision.advance,
        'execution_status': decision.execution_status.value,
        'quality_status': decision.quality_status.value,
        'safety_status': decision.safety_status.value,
        'reasons': list(decision.reasons),
        'arms': arm_payloads,
    }
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + '\n').encode('utf-8')
    temporary = parent / f'.checkpoint-{uuid.uuid4().hex}.tmp'
    descriptor = None
    published = False
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, 'O_NOFOLLOW'):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(temporary, flags, 0o600)
        offset = 0
        while offset < len(encoded):
            offset += os.write(descriptor, encoded[offset:])
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = None
        os.link(temporary, destination)
        published = True
        directory = os.open(parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except FileExistsError:
        raise Blocked("stage checkpoint already exists; preserve prior evidence") from None
    except OSError as exc:
        rollback_error = None
        if published:
            try:
                destination.unlink()
                rollback_directory = os.open(parent, os.O_RDONLY)
                try:
                    os.fsync(rollback_directory)
                finally:
                    os.close(rollback_directory)
            except OSError as cleanup_exc:
                rollback_error = cleanup_exc
        if rollback_error is not None:
            raise Blocked(
                "checkpoint publication failed and rollback could not be made durable: "
                f"{rollback_error}"
            ) from None
        raise Blocked(f"cannot publish stage checkpoint atomically: {exc}") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary.exists():
            temporary.unlink()
    return destination


def finalize_executed_pair(bundle, enforcement, pair):
    """Bind trusted per-arm evidence to one completed provider execution."""
    if not isinstance(enforcement, EnforcementReceipt):
        raise TypeError('enforcement receipt is required')
    if not isinstance(pair, ProofPairResult):
        raise TypeError('proof pair result is required')
    bundle = Path(bundle).resolve()
    manifest_path = bundle / 'manifest.json'
    manifest = _json_file(manifest_path, 'prepared bundle manifest')
    if manifest.get('status') != 'PENDING_HOST_AUDIT':
        raise Blocked('Provider execution is not pending host audit')
    if manifest.get('run_nonce') != enforcement.run_nonce:
        raise Blocked('Execution manifest does not match enforcement receipt nonce')
    if manifest.get('plan_digest') != enforcement.plan_digest:
        raise Blocked('Execution manifest does not match enforcement receipt plan')
    if pair.run_id != enforcement.run_nonce:
        raise Blocked('Proof pair run identity does not match enforcement receipt nonce')
    result_path = _result_path(bundle, manifest)
    source_digest = provider_result_digest(result_path)
    if source_digest != manifest.get('provider_result_digest'):
        raise Blocked('Provider source result changed before host finalization')
    observed_identity = _verified_provider_identity(
        result_path,
        enforcement,
        max_bytes=int(manifest.get('resource_limits', {}).get(
            'max_output_bytes', 64 * 1024 * 1024
        )),
    )
    if manifest.get('observed_provider_identity') != observed_identity:
        raise Blocked('Execution manifest provider identity is missing or changed')
    execution_id = manifest.get('execution_id')
    for arm in pair.arms:
        evidence = arm.evidence_bundle
        if evidence is None:
            raise Blocked(f'Arm {arm.name} is missing trusted host evidence')
        if (
            evidence.run_id != enforcement.run_nonce
            or evidence.receipt_nonce != enforcement.run_nonce
            or evidence.execution_id != execution_id
            or evidence.source_result_digest != source_digest
        ):
            raise Blocked(f'Arm {arm.name} evidence identity does not match execution')
    if not pair.completed:
        raise Blocked('Proof pair is incomplete or failed evidence revalidation')
    manifest['status'] = 'HOST_AUDIT_COMPLETE'
    manifest['arm_evidence_digests'] = {
        arm.name: evidence_bundle_digest(arm.evidence_bundle)
        for arm in pair.arms
    }
    _write_manifest_atomic(manifest_path, manifest)
    return manifest


def active_harness(env=None):
    env = os.environ if env is None else env
    claude = str(env.get('CLAUDECODE', '')).lower() not in ('', '0', 'false')
    codex = bool(env.get('CODEX_THREAD_ID') or env.get('CODEX_SESSION_ID'))
    if claude and codex:
        raise Blocked('Conflicting active Claude and Codex session markers; no fallback')
    if not (claude or codex):
        raise Blocked('Active harness unknown: cannot choose based on installed CLIs')
    return 'claude' if claude else 'codex'


def choose_harness(explicit, env=None, *, for_execution=False):
    try:
        discovered = active_harness(env)
    except Blocked as exc:
        if 'Conflicting' in str(exc) or for_execution or not explicit:
            raise
        return explicit  # Offline preparation only, not execution.
    if explicit and explicit != discovered:
        raise Blocked('Requested harness disagrees with active session: refusing cross-provider routing')
    return discovered


def safe_file(src, root):
    """Only accept regular files within root, with no symlinked path component."""
    src = Path(src).absolute()
    root = Path(root).absolute()
    try:
        relative = src.relative_to(root)
    except ValueError:
        raise Blocked(f'Source file outside target skill: {src}') from None
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise Blocked(f'Symlinked source path denied: {src}')
    if not src.is_file() or not src.resolve().is_relative_to(root.resolve()):
        raise Blocked(f'Unsafe/missing source file: {src}')
    return src


def copy_skill(source, destination):
    source = source.resolve()
    entry = safe_file(source / 'SKILL.md', source)
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(entry, destination / 'SKILL.md')
    refs = source / 'references'
    if refs.is_dir():
        for src in refs.rglob('*'):
            if src.is_symlink():
                raise Blocked('Symlink in skill references')
            if src.is_file():
                safe_file(src, source)
                dst = destination / src.relative_to(source)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
    # Scripts/assets intentionally not staged until separately reviewed.


def get_case(suite, case_id):
    data = json.loads(suite.read_text(encoding='utf-8'))
    cases = data.get('evals', [])
    if not isinstance(cases, list):
        raise Blocked('Invalid evals array')
    matches = [c for c in cases if str(c.get('id')) == str(case_id)]
    if len(matches) != 1:
        raise Blocked('Case ID missing or not unique')
    case = matches[0]
    if not isinstance(case.get('prompt'), str) or not case['prompt'].strip():
        raise Blocked('No case prompt')
    assertions = case.get('assertions')
    if not isinstance(assertions, list) or not assertions or not all(isinstance(x, str) and x.strip() for x in assertions):
        raise Blocked('Approved assertions are required for native LLM grading')
    inputs = case.get('files') or []
    if not isinstance(inputs, list) or not all(isinstance(x, str) for x in inputs):
        raise Blocked('File fixtures must be a list of relative paths')
    return case, inputs


def fixture_sources(skill_root, inputs):
    """Resolve approved fixture paths relative to the *target skill root*.

    The evals.json convention, including scripts/validate_evals.py, uses
    skill-root-relative paths such as evals/files/fixture.txt. Never fall
    back to the suite directory or silently rewrite approved paths.
    """
    root = Path(skill_root).resolve()
    files = []
    for rel in inputs:
        relpath = Path(rel)
        if relpath.is_absolute() or not relpath.parts or '..' in relpath.parts:
            raise Blocked(f'Absolute/parent traversal fixture path refused: {rel}')
        files.append((safe_file(root / relpath, root), relpath))
    return files


def copy_inputs(skill_root, inputs, dst):
    for src, relpath in fixture_sources(skill_root, inputs):
        out = dst / relpath
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out)


def _canonical_sha256(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode(
            'utf-8'
        )
    ).hexdigest()


def _validate_fixture_tree(root):
    root = Path(root)
    if not root.is_dir() or root.is_symlink():
        raise Blocked('Approved fixture must be a real directory')
    forbidden = {
        'answer-key.json',
        'prior-results.json',
        'evals.json',
        'results.json',
        'graders',
    }
    for path in root.rglob('*'):
        if path.is_symlink():
            raise Blocked('Symlink in approved fixture tree')
        if path.name.lower() in forbidden:
            raise Blocked(f'Evaluator-only material denied in fixture: {path.name}')


def _stage_proof_arms(plan, fixture_root, skill_root, output_root):
    _validate_fixture_tree(fixture_root)
    skill_root = Path(skill_root)
    if not skill_root.is_dir() or skill_root.is_symlink():
        raise Blocked('Target skill must be a real directory')
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex
    run_root = output_root / f'provider-proof-{run_id}'
    run_root.mkdir(exist_ok=False)
    arms = []
    for arm_name in plan.comparison_arms:
        workspace = run_root / arm_name
        workspace.mkdir()
        fixture_destination = workspace / 'fixture'
        shutil.copytree(fixture_root, fixture_destination)
        if arm_name == 'with-skill':
            copy_skill(
                skill_root,
                workspace / '.agents' / 'skills' / slug(skill_root.name),
            )
        fixture_digest = snapshot_tree(fixture_destination, ()).digest
        arms.append(ProofArmWorkspace(arm_name, workspace, fixture_digest))
    if len({arm.fixture_digest for arm in arms}) != 1:
        raise Blocked('Comparison-arm fixtures are not equivalent')
    manifest = {
        'schema_version': plan.schema_version,
        'status': 'PREPARED_NOT_RUN',
        'run_id': run_id,
        'plan_digest': plan.digest(),
        'comparison_arms': [
            {'name': arm.name, 'fixture_digest': arm.fixture_digest}
            for arm in arms
        ],
        'provider_auth_boundary': 'UNVERIFIED_REQUIRES_HOST_PROOF',
    }
    (run_root / 'proof-manifest.json').write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + '\n',
        encoding='utf-8',
    )
    return PreparedProofRun(run_id, run_root, plan.digest(), tuple(arms))


def prepare_provider_proof(
    plan,
    approval,
    enforcement,
    inventory,
    boundary_result,
    provider_config,
    fixture_root,
    skill_root,
    output_root,
    *,
    observed_versions=None,
    observed_platform=None,
):
    """Prepare paired proof arms only after policy and boundary verification."""
    if observed_versions is None or observed_platform is None:
        raise Blocked('Observed tool versions and platform are required')
    decision = assess_run(
        plan,
        approval,
        enforcement,
        inventory,
        observed_versions=observed_versions,
        observed_platform=observed_platform,
    )
    if decision.decision != 'APPROVED':
        raise Blocked('; '.join(decision.reasons))
    if not isinstance(boundary_result, NativeBoundaryResult):
        raise Blocked('Verified native boundary result is required')
    if not boundary_result.complete or not boundary_result.is_valid_for(plan, provider_config):
        raise Blocked('Native boundary result is incomplete or does not match the plan')
    if enforcement.provider_config_digest != boundary_result.provider_config_digest:
        raise Blocked('Enforcement receipt provider config digest does not match preflight')
    for probe in boundary_result.results:
        if enforcement.probe_results.get(probe.probe_id) != probe.status:
            raise Blocked(f'Enforcement receipt does not match probe {probe.probe_id}')
    if tuple(plan.comparison_arms) != ('with-skill', 'without-skill'):
        raise Blocked('Provider proof requires exact with-skill and without-skill arms')
    return _stage_proof_arms(plan, fixture_root, skill_root, output_root)


def agent_environment(
    driver_environment: Mapping[str, str], *, provider_auth_keys: Sequence[str]
) -> dict[str, str]:
    """Return the small non-secret environment allowed inside an evaluated arm."""
    allowed = frozenset(('PATH', 'LANG', 'LC_ALL', 'TZ', 'PYTHONIOENCODING'))
    denied = frozenset(provider_auth_keys)
    return {
        key: value
        for key, value in driver_environment.items()
        if key in allowed and key not in denied and isinstance(value, str)
    }


def sanitize_provider_trace(
    events: Sequence[Mapping[str, Any]], provider_auth: Mapping[str, str]
) -> Tuple[dict[str, Any], ...]:
    return sanitize_events(events, tuple(provider_auth.values()))


def finalize_proof_arm(
    name: str,
    provider_result: Optional[Path],
    quality_status: QualityStatus,
    evidence_bundle: Optional[EvidenceBundle],
) -> ProofArmResult:
    result_path = Path(provider_result) if provider_result is not None else None
    try:
        result_digest = (
            provider_result_digest(result_path) if result_path is not None else None
        )
    except EvidenceError:
        result_digest = None
    if result_digest is None:
        if quality_status not in (QualityStatus.NOT_GRADED, QualityStatus.UNKNOWN):
            quality_status = QualityStatus.UNKNOWN
        return ProofArmResult(
            name,
            result_path,
            ExecutionStatus.INCOMPLETE,
            quality_status,
            SafetyStatus.UNKNOWN,
            evidence_bundle,
        )
    if evidence_bundle is None:
        return ProofArmResult(
            name,
            result_path,
            ExecutionStatus.INCOMPLETE,
            quality_status,
            SafetyStatus.UNKNOWN,
            None,
        )
    if (
        evidence_bundle.arm_name != name
        or evidence_bundle.provider_result_digest != result_digest
    ):
        return ProofArmResult(
            name,
            result_path,
            ExecutionStatus.INCOMPLETE,
            quality_status,
            SafetyStatus.UNKNOWN,
            evidence_bundle,
        )
    return ProofArmResult(
        name,
        result_path,
        evidence_bundle.audit.execution_status,
        quality_status,
        evidence_bundle.audit.safety_status,
        evidence_bundle,
    )


def slug(value):
    val = re.sub(r'[^a-zA-Z0-9_-]', '-', str(value)).strip('-')
    if not val:
        raise Blocked('Invalid skill name or case ID')
    return val[:90]


def _tree_revision(root):
    root = Path(root)
    if not root.exists():
        return _canonical_sha256([])
    if not root.is_dir() or root.is_symlink():
        raise Blocked('Staged revision root must be a real directory')
    records = []
    for path in sorted(root.rglob('*'), key=lambda item: item.as_posix()):
        if path.is_symlink():
            raise Blocked('Symlink in staged revision root')
        if path.is_file():
            records.append({
                'path': path.relative_to(root).as_posix(),
                'digest': _regular_file_digest(path),
            })
    return _canonical_sha256(records)


def _staged_revisions(bundle, manifest):
    """Derive revision pins from the staged artifacts, never manifest claims."""
    bundle = Path(bundle)
    harness = manifest.get('harness')
    case_id = str(manifest.get('case_id'))
    if harness == 'codex':
        config = _json_file(
            bundle / 'codex' / 'promptfooconfig.yaml', 'prepared Promptfoo config'
        )
        tests = config.get('tests')
        if not isinstance(tests, list) or len(tests) != 1:
            raise Blocked('Prepared Promptfoo case structure is not exact')
        test = tests[0]
        question = test.get('vars', {}).get('question') if isinstance(test, dict) else None
        assertions = test.get('assert') if isinstance(test, dict) else None
        if not isinstance(question, str) or not isinstance(assertions, list):
            raise Blocked('Prepared Promptfoo case or rubric is malformed')
        rubric_values = [
            assertion.get('value') if isinstance(assertion, dict) else None
            for assertion in assertions
        ]
        if not rubric_values or not all(isinstance(item, str) for item in rubric_values):
            raise Blocked('Prepared Promptfoo rubric is malformed')
        skill_roots = sorted(
            (bundle / 'codex' / 'with_skill' / '.agents' / 'skills').glob('*')
        )
        if len(skill_roots) != 1:
            raise Blocked('Prepared with-skill arm must contain exactly one skill')
        fixture_roots = [
            bundle / 'codex' / arm / 'inputs'
            for arm in ('with_skill', 'without_skill')
        ]
    elif harness == 'claude':
        case_root = bundle / 'plugin' / 'evals' / slug(case_id)
        prompt_path = case_root / 'prompt.md'
        prompt = prompt_path.read_text(encoding='utf-8')
        parts = prompt.split('---\n', 2)
        if len(parts) != 3 or not parts[2].strip():
            raise Blocked('Prepared Claude eval prompt is malformed')
        question = parts[2].strip()
        graders = sorted((case_root / 'graders').glob('criterion-*.md'))
        rubric_values = [path.read_text(encoding='utf-8') for path in graders]
        if not rubric_values:
            raise Blocked('Prepared Claude eval rubric is missing')
        skill_roots = sorted((bundle / 'plugin' / 'skills').glob('*'))
        if len(skill_roots) != 1:
            raise Blocked('Prepared Claude plugin must contain exactly one skill')
        fixture_roots = [case_root / 'fixtures']
    else:
        raise Blocked('Manifest harness invalid')
    fixture_revisions = [_tree_revision(root) for root in fixture_roots]
    if len(set(fixture_revisions)) != 1:
        raise Blocked('Prepared comparison fixtures are not equivalent')
    return {
        'case_revision': _canonical_sha256({'case_id': case_id, 'prompt': question}),
        'rubric_revision': _canonical_sha256({'rubrics': rubric_values}),
        'skill_revision': _tree_revision(skill_roots[0]),
        'fixture_revision': fixture_revisions[0],
    }


def prepare(args, *, env=None):
    harness = choose_harness(args.harness, env)
    source = args.target_skill.absolute()
    if not source.is_dir() or source.is_symlink():
        raise Blocked('Target skill directory does not exist')
    suite = safe_file(args.suite.absolute(), source)  # Preserve symlinks for safe_file checks
    case, inputs = get_case(suite, args.case_id)
    # Fail before creating the output bundle when any fixture is unsafe/missing.
    fixture_sources(source, inputs)
    name = slug(source.name)
    case_name = slug(case['id'])
    base = args.output.resolve()
    base.mkdir(parents=True, exist_ok=True)
    bundle = base / f'{harness}-native-{case_name}-{uuid.uuid4().hex[:12]}'
    bundle.mkdir(exist_ok=False)
    metadata = dict(status='PREPARED_NOT_RUN', harness=harness, case_id=case['id'],
                    target_skill=str(source), suite=str(suite), native_result=None,
                    note='Preparation does not verify host isolation or run a model')
    if harness == 'claude':
        plugin = bundle / 'plugin'
        (plugin / '.claude-plugin').mkdir(parents=True)
        (plugin / '.claude-plugin' / 'plugin.json').write_text(json.dumps({
            'name': f'refine-eval-{name}', 'version': '0.0.1',
            'description': 'Temporary synthetic evaluation target; not for publication'
        }, indent=2), encoding='utf-8')
        copy_skill(source, plugin / 'skills' / name)
        case_dir = plugin / 'evals' / case_name
        grader_dir = case_dir / 'graders'
        grader_dir.mkdir(parents=True)
        prompt = '---\nruns: 3\nmax_turns: 10\nallowed_tools: [Read, Glob, Grep, Skill]\n---\n' + case['prompt'].strip() + '\n'
        (case_dir / 'prompt.md').write_text(prompt, encoding='utf-8')
        if inputs:
            copy_inputs(source, inputs, case_dir / 'fixtures')
            (case_dir / 'case.yaml').write_text('schema_version: "1.1"\nname: ' + case_name + '\ncontext:\n  add_dirs: [fixtures]\n', encoding='utf-8')
        for i, assertion in enumerate(case['assertions'], 1):
            (grader_dir / f'criterion-{i:02}.md').write_text(
                '---\ntype: llm\nfocus: last_message\n---\n'
                'PASS only if the following criterion is demonstrated by the answer; '
                'FAIL if missing, contradicted or unsupported. Cite specific evidence.\n'
                + assertion + '\n', encoding='utf-8')
        metadata['native_tool'] = 'claude plugin eval'
        metadata['native_format'] = 'plugin eval: prompt.md + graders/*.md; native JSON/HTML'
    elif harness == 'codex':
        cd = bundle / 'codex'
        (cd / 'with_skill' / '.agents' / 'skills').mkdir(parents=True)
        (cd / 'without_skill').mkdir(parents=True)
        (cd / 'judge').mkdir(parents=True)
        copy_skill(source, cd / 'with_skill' / '.agents' / 'skills' / name)
        if inputs:
            for arm in ('with_skill', 'without_skill'):
                copy_inputs(source, inputs, cd / arm / 'inputs')
        def provider(dir_name):
            return {'id': 'openai:codex-sdk', 'label': dir_name,
                    'config': {'working_dir': f'./{dir_name}',
                               'approval_policy': 'never', 'web_search_mode': 'disabled',
                               'persist_threads': False,
                               'inherit_process_env': False, 'skip_git_repo_check': True}}
        judge = {'id': 'openai:codex-sdk', 'config': {
            'working_dir': './judge', 'approval_policy': 'never',
            'web_search_mode': 'disabled', 'inherit_process_env': False,
            'skip_git_repo_check': True, 'persist_threads': False}}
        config = {'description': f'Evaluate Skill synthetic case {case_name}',
                  'prompts': ['{{question}}'],
                  'providers': [provider('with_skill'), provider('without_skill')],
                  'tests': [{'vars': {'question': case['prompt'].strip()},
                             'assert': [{'type': 'llm-rubric',
                                         'value': 'PASS only if: ' + assertion +
                                                  '. FAIL for absent, contradicted, superficial or unsupported evidence.',
                                         'provider': judge} for assertion in case['assertions']]}],
                  'commandLineOptions': {'share': False, 'cache': False}}
        # JSON is valid YAML and preserves the precise provider-specific schema.
        (cd / 'promptfooconfig.yaml').write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
        metadata['native_tool'] = 'promptfoo + openai:codex-sdk'
        metadata['native_format'] = 'Promptfoo: promptfooconfig.yaml + llm-rubric; native JSON'
    else:
        raise Blocked('Unknown harness')
    metadata.update(_staged_revisions(bundle, metadata))
    (bundle / 'manifest.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    return bundle


def native_command(bundle, manifest):
    harness = manifest['harness']
    if manifest.get('status') not in (
        'CONFIGURED_NOT_BOUND', 'BOUND_NOT_RUN', 'RUNNING',
        'PENDING_HOST_AUDIT', 'HOST_AUDIT_COMPLETE',
    ):
        raise Blocked('Provider command requires a plan-configured bundle')
    model_version = manifest.get('model_version')
    if not isinstance(model_version, str) or not model_version:
        raise Blocked('Configured bundle is missing the approved model version')
    if harness == 'claude':
        return ['claude', 'plugin', 'eval', str(bundle / 'plugin'), '--ablation', 'with-without',
                '--model', model_version, '--no-publish', '--json',
                str(bundle / 'claude-results.json')]
    if harness == 'codex':
        return ['promptfoo', 'eval', '--config', str(bundle / 'codex' / 'promptfooconfig.yaml'),
                '--no-cache', '--no-share', '--output', str(bundle / 'codex-results.json')]
    raise Blocked('Manifest harness invalid')


def _regular_file_digest(path):
    flags = os.O_RDONLY
    if hasattr(os, 'O_NOFOLLOW'):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise Blocked(f'Cannot hash staged artifact: {exc}') from None
    digest = hashlib.sha256()
    try:
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    finally:
        os.close(descriptor)
    return digest.hexdigest()


def _bundle_digest(bundle):
    """Hash every staged input while excluding mutable control/output files."""
    bundle = Path(bundle)
    if not bundle.is_dir() or bundle.is_symlink():
        raise Blocked('Prepared bundle must be a real directory')
    excluded = frozenset(('manifest.json', 'claude-results.json', 'codex-results.json'))
    artifacts = []
    for path in sorted(bundle.rglob('*'), key=lambda item: item.as_posix()):
        if path.is_symlink():
            raise Blocked(f'Symlinked staged artifact denied: {path.relative_to(bundle)}')
        if not path.is_file():
            continue
        relative = path.relative_to(bundle).as_posix()
        if relative in excluded:
            continue
        metadata = os.stat(path, follow_symlinks=False)
        artifacts.append({
            'path': relative,
            'mode': metadata.st_mode & 0o777,
            'size': metadata.st_size,
            'digest': _regular_file_digest(path),
        })
    if not artifacts:
        raise Blocked('Prepared bundle contains no staged artifacts')
    return hashlib.sha256(
        json.dumps(artifacts, sort_keys=True, separators=(',', ':')).encode('utf-8')
    ).hexdigest()


def _write_manifest_atomic(path, manifest):
    """Durably replace only the runner-owned manifest state file."""
    path = Path(path)
    temporary = path.parent / f'.manifest-{uuid.uuid4().hex}.tmp'
    try:
        with temporary.open('x', encoding='utf-8') as handle:
            json.dump(manifest, handle, indent=2, sort_keys=True)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temporary.exists():
            temporary.unlink()


def _provider_config_digest(bundle, manifest):
    """Hash the exact provider settings and files consumed by the command."""
    bundle = Path(bundle)
    paths = [bundle / 'execution-config.json']
    if manifest.get('harness') == 'codex':
        paths.append(bundle / 'codex' / 'promptfooconfig.yaml')
    elif manifest.get('harness') == 'claude':
        paths.extend(sorted((bundle / 'plugin' / 'evals').glob('*/prompt.md')))
    else:
        raise Blocked('Manifest harness invalid')
    if len(paths) < 2:
        raise Blocked('Provider execution configuration is incomplete')
    records = []
    for path in paths:
        if not path.is_file() or path.is_symlink():
            raise Blocked('Provider execution configuration must be regular files')
        records.append({
            'path': path.relative_to(bundle).as_posix(),
            'digest': _regular_file_digest(path),
        })
    command = native_command(bundle, manifest)
    records.append({'command': command})
    return _canonical_sha256({'files': records})


def _expected_codex_provider_config(host_policy, execution_config, working_dir):
    limits = execution_config['resource_limits']
    return {
        'working_dir': working_dir,
        'approval_policy': 'never',
        'web_search_mode': 'disabled',
        'persist_threads': False,
        'inherit_process_env': False,
        'skip_git_repo_check': True,
        'enable_streaming': True,
        'deep_tracing': False,
        'cli_config': host_policy.canonical_payload()['cli_config'],
        'cli_env': dict(host_policy.process_environment),
        'model': execution_config['model_version'],
        'max_turns': int(limits['max_turns']),
        'max_cost_usd': limits['max_cost_usd'],
    }


def _validate_codex_host_config(config, host_policy, execution_config):
    if not isinstance(config, dict):
        raise Blocked('Configured Promptfoo file must contain an object')
    allowed_top = frozenset(
        ('description', 'prompts', 'providers', 'tests', 'commandLineOptions', 'env')
    )
    unknown_top = sorted(set(config) - allowed_top)
    if unknown_top:
        raise Blocked('Configured Promptfoo file has unsafe top-level fields')
    if config.get('commandLineOptions') != {'share': False, 'cache': False}:
        raise Blocked('Configured Promptfoo cache and sharing controls are incomplete')
    if config.get('env') != _PROMPTFOO_SAFE_ENV:
        raise Blocked('Configured Promptfoo host environment controls are incomplete')

    providers = config.get('providers')
    tests = config.get('tests')
    if not isinstance(providers, list) or len(providers) != 2 or not isinstance(tests, list):
        raise Blocked('Configured Promptfoo comparison structure is invalid')
    expected_arms = {
        'with_skill': './with_skill',
        'without_skill': './without_skill',
    }
    observed_labels = set()
    for provider in providers:
        if not isinstance(provider, dict) or set(provider) != {'id', 'label', 'config'}:
            raise Blocked('Configured Promptfoo arm provider shape is invalid')
        if provider.get('id') != 'openai:codex-sdk':
            raise Blocked('Configured Promptfoo arm provider changed')
        label = provider.get('label')
        if label not in expected_arms or label in observed_labels:
            raise Blocked('Configured Promptfoo arm labels are not exact')
        observed_labels.add(label)
        expected = _expected_codex_provider_config(
            host_policy, execution_config, expected_arms[label]
        )
        if provider.get('config') != expected:
            raise Blocked('Configured Promptfoo arm host policy does not match')
    if observed_labels != set(expected_arms):
        raise Blocked('Configured Promptfoo comparison arms are incomplete')

    judge_count = 0
    for test in tests:
        if not isinstance(test, dict) or set(test) != {'vars', 'assert'}:
            raise Blocked('Configured Promptfoo test shape is invalid')
        assertions = test.get('assert')
        if not isinstance(test.get('vars'), dict) or not isinstance(assertions, list):
            raise Blocked('Configured Promptfoo assertions are malformed')
        for assertion in assertions:
            if (
                not isinstance(assertion, dict)
                or set(assertion) != {'type', 'value', 'provider'}
                or assertion.get('type') != 'llm-rubric'
            ):
                raise Blocked('Configured Promptfoo rubric assertion shape is invalid')
            judge = assertion.get('provider')
            if not isinstance(judge, dict) or set(judge) != {'id', 'config'}:
                raise Blocked('Configured Promptfoo judge shape is invalid')
            if judge.get('id') != 'openai:codex-sdk':
                raise Blocked('Configured Promptfoo judge provider changed')
            expected = _expected_codex_provider_config(
                host_policy, execution_config, './judge'
            )
            if judge.get('config') != expected:
                raise Blocked('Configured Promptfoo judge host policy does not match')
            judge_count += 1
    if judge_count < 1:
        raise Blocked('Configured Promptfoo judge is missing')


def validate_configured_host_policy(bundle, host_policy):
    """Re-read and fail closed on any Codex arm or judge policy drift."""
    if not isinstance(host_policy, CodexHostPolicy):
        raise Blocked('A compiled Codex host policy is required')
    bundle = Path(bundle).resolve()
    if bundle != host_policy.workspace:
        raise Blocked('Codex host policy workspace does not match the bundle')
    execution_path = bundle / 'execution-config.json'
    config_path = bundle / 'codex' / 'promptfooconfig.yaml'
    if (
        not execution_path.is_file()
        or execution_path.is_symlink()
        or not config_path.is_file()
        or config_path.is_symlink()
    ):
        raise Blocked('Configured Codex host policy files must be regular files')
    execution_config = _json_file(execution_path, 'provider execution config')
    if execution_config.get('host_policy_digest') != host_policy.digest():
        raise Blocked('Configured execution host policy digest does not match')
    config = _json_file(config_path, 'configured Promptfoo config')
    _validate_codex_host_config(config, host_policy, execution_config)
    return host_policy.digest()


def configure_prepared_bundle(bundle, plan, host_policy=None):
    """Materialize an exact, reviewable provider config from the approved plan."""
    if not isinstance(plan, RunPlan):
        raise TypeError('run plan is required')
    bundle = Path(bundle).resolve()
    manifest_path = bundle / 'manifest.json'
    manifest = _json_file(manifest_path, 'prepared bundle manifest')
    if manifest.get('status') != 'PREPARED_NOT_RUN':
        raise Blocked('Bundle is not an unconfigured prepared case')
    if str(manifest.get('case_id')) != str(plan.case_id):
        raise Blocked('Prepared bundle case does not match approved run plan case')
    if plan.backend != 'native':
        raise Blocked('Native prepared bundle cannot configure another backend')
    expected_harness = {
        ('openai', 'promptfoo-codex-sdk'): 'codex',
        ('anthropic', 'promptfoo-claude-agent-sdk'): 'claude',
    }.get((plan.provider, plan.adapter))
    if expected_harness != manifest.get('harness'):
        raise Blocked('Approved provider/adapter does not match prepared harness')
    staged_revisions = _staged_revisions(bundle, manifest)
    for field, actual_revision in staged_revisions.items():
        if manifest.get(field) != actual_revision:
            raise Blocked(f'Prepared bundle {field} claim does not match staged artifacts')
        if actual_revision != getattr(plan, field):
            raise Blocked(f'Prepared bundle {field} does not match approved plan')

    execution_config = {
        'schema_version': plan.schema_version,
        'plan_digest': plan.digest(),
        'provider': plan.provider,
        'provider_version': plan.provider_version,
        'model': plan.model,
        'model_version': plan.model_version,
        'adapter': plan.adapter,
        'adapter_version': plan.adapter_version,
        'backend': plan.backend,
        'resource_limits': dict(plan.resource_limits),
        'comparison_arms': list(plan.comparison_arms),
    }
    if expected_harness == 'codex':
        if not isinstance(host_policy, CodexHostPolicy):
            raise Blocked('A compiled Codex host policy is required')
        if host_policy.workspace != bundle:
            raise Blocked('Codex host policy workspace does not match prepared bundle')
        execution_config['host_policy_digest'] = host_policy.digest()
    execution_path = bundle / 'execution-config.json'
    execution_path.write_text(
        json.dumps(execution_config, indent=2, sort_keys=True) + '\n',
        encoding='utf-8',
    )
    if expected_harness == 'codex':
        config_path = bundle / 'codex' / 'promptfooconfig.yaml'
        config = _json_file(config_path, 'prepared Promptfoo config')
        provider_configs = []
        providers = config.get('providers')
        tests = config.get('tests')
        if not isinstance(providers, list) or len(providers) != 2 or not isinstance(tests, list):
            raise Blocked('Prepared Promptfoo config has unexpected comparison structure')
        arm_working_directories = {
            'with_skill': './with_skill',
            'without_skill': './without_skill',
        }
        observed_labels = set()
        for provider in providers:
            if not isinstance(provider, dict) or provider.get('id') != 'openai:codex-sdk':
                raise Blocked('Prepared Promptfoo provider is not the approved adapter')
            label = provider.get('label')
            if label not in arm_working_directories or label in observed_labels:
                raise Blocked('Prepared Promptfoo comparison labels are not exact')
            observed_labels.add(label)
            provider['config'] = _expected_codex_provider_config(
                host_policy, execution_config, arm_working_directories[label]
            )
            provider_configs.append(provider['config'])
        if observed_labels != set(arm_working_directories):
            raise Blocked('Prepared Promptfoo comparison arms are incomplete')
        for test in tests:
            assertions = test.get('assert') if isinstance(test, dict) else None
            if not isinstance(assertions, list):
                raise Blocked('Prepared Promptfoo assertions are malformed')
            for assertion in assertions:
                judge = assertion.get('provider') if isinstance(assertion, dict) else None
                if not isinstance(judge, dict) or judge.get('id') != 'openai:codex-sdk':
                    raise Blocked('Prepared Promptfoo judge is not the approved adapter')
                judge['config'] = _expected_codex_provider_config(
                    host_policy, execution_config, './judge'
                )
                provider_configs.append(judge['config'])
        config['commandLineOptions'] = {'share': False, 'cache': False}
        config['env'] = dict(_PROMPTFOO_SAFE_ENV)
        _validate_codex_host_config(config, host_policy, execution_config)
        config_path.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
        validate_configured_host_policy(bundle, host_policy)
    else:
        prompts = sorted((bundle / 'plugin' / 'evals').glob('*/prompt.md'))
        if len(prompts) != 1:
            raise Blocked('Prepared Claude eval prompt is missing or ambiguous')
        prompt = prompts[0].read_text(encoding='utf-8')
        updated, count = re.subn(
            r'(?m)^max_turns:\s*\d+\s*$',
            f"max_turns: {int(plan.resource_limits['max_turns'])}",
            prompt,
        )
        if count != 1:
            raise Blocked('Prepared Claude eval max_turns setting is missing or ambiguous')
        prompts[0].write_text(updated, encoding='utf-8')

    manifest.update({
        'status': 'CONFIGURED_NOT_BOUND',
        'plan_digest': plan.digest(),
        'model': plan.model,
        'model_version': plan.model_version,
        'provider': plan.provider,
        'provider_version': plan.provider_version,
        'adapter': plan.adapter,
        'adapter_version': plan.adapter_version,
        'resource_limits': dict(plan.resource_limits),
    })
    if expected_harness == 'codex':
        manifest['host_policy_digest'] = host_policy.digest()
    manifest['provider_config_digest'] = _provider_config_digest(bundle, manifest)
    manifest['bundle_digest'] = _bundle_digest(bundle)
    _write_manifest_atomic(manifest_path, manifest)
    return manifest


def _result_path(bundle, manifest):
    if manifest.get('harness') == 'claude':
        return Path(bundle) / 'claude-results.json'
    if manifest.get('harness') == 'codex':
        return Path(bundle) / 'codex-results.json'
    raise Blocked('Manifest harness invalid')


def _expected_provider_identity(scope):
    return {
        field: getattr(scope, field)
        for field in (
            'provider', 'provider_version', 'model', 'model_version',
            'adapter', 'adapter_version',
        )
    }


def _verified_provider_identity(result_path, scope, *, max_bytes):
    try:
        observed = provider_result_identity(result_path, max_bytes=max_bytes)
    except EvidenceError as exc:
        raise Blocked(f'Provider result identity is incomplete: {exc}') from None
    if observed != _expected_provider_identity(scope):
        raise Blocked('Provider result identity does not match the approved plan')
    return observed


def _write_exclusive_claim(claim, payload, *, exists_message):
    execution_id = uuid.uuid4().hex
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, 'O_NOFOLLOW'):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(claim, flags, 0o600)
    except FileExistsError:
        raise Blocked(exists_message) from None
    try:
        encoded = (json.dumps(payload(execution_id), sort_keys=True) + '\n').encode('utf-8')
        offset = 0
        while offset < len(encoded):
            offset += os.write(descriptor, encoded[offset:])
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    directory = os.open(claim.parent, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)
    return execution_id


def _claim_execution(bundle, plan, enforcement, nonce_ledger):
    """Consume the run nonce outside the rollbackable prepared bundle."""
    bundle = Path(bundle).resolve()
    ledger_input = Path(nonce_ledger)
    if ledger_input.is_symlink():
        raise Blocked('Trusted consumed-nonce ledger cannot be a symlink')
    ledger = ledger_input.resolve()
    if not ledger.is_dir():
        raise Blocked('Trusted consumed-nonce ledger must be a real existing directory')
    if ledger == bundle or ledger.is_relative_to(bundle):
        raise Blocked('Consumed-nonce ledger must be outside the prepared bundle')
    nonce_key = hashlib.sha256(enforcement.run_nonce.encode('utf-8')).hexdigest()
    ledger_claim = ledger / f'{nonce_key}.json'
    execution_id = _write_exclusive_claim(
        ledger_claim,
        lambda identifier: {
            'schema_version': plan.schema_version,
            'plan_digest': plan.digest(),
            'run_nonce': enforcement.run_nonce,
            'execution_id': identifier,
        },
        exists_message='Approved run nonce has already been consumed',
    )
    local_claim = bundle / '.execution-claim'
    local_id = _write_exclusive_claim(
        local_claim,
        lambda _identifier: {
            'run_nonce': enforcement.run_nonce,
            'execution_id': execution_id,
            'ledger_claim': str(ledger_claim),
        },
        exists_message='Bundle execution has already been claimed',
    )
    if not local_id:
        raise Blocked('Cannot record local execution claim')
    return execution_id


def bind_prepared_bundle(bundle, plan, enforcement):
    """Bind a prepared, model-free bundle to one exact approved run plan."""
    if not isinstance(plan, RunPlan):
        raise TypeError('run plan is required')
    if not isinstance(enforcement, EnforcementReceipt):
        raise TypeError('enforcement receipt is required')
    bundle = Path(bundle).resolve()
    manifest_path = bundle / 'manifest.json'
    manifest = _json_file(manifest_path, 'prepared bundle manifest')
    if manifest.get('status') != 'CONFIGURED_NOT_BOUND':
        raise Blocked('Bundle is not a configured, unbound prepared case')
    if str(manifest.get('case_id')) != str(plan.case_id):
        raise Blocked('Prepared bundle case does not match approved run plan case')
    if plan.backend != 'native':
        raise Blocked('Native prepared bundle cannot bind to another backend')
    if _result_path(bundle, manifest).exists():
        raise Blocked('Prepared bundle already contains provider results')
    bundle_digest = _bundle_digest(bundle)
    provider_config_digest = _provider_config_digest(bundle, manifest)
    if manifest.get('plan_digest') != plan.digest():
        raise Blocked('Configured bundle does not match approved run plan')
    if manifest.get('bundle_digest') != bundle_digest:
        raise Blocked('Configured bundle digest changed before binding')
    if manifest.get('provider_config_digest') != provider_config_digest:
        raise Blocked('Configured provider settings changed before binding')
    if enforcement.plan_digest != plan.digest():
        raise Blocked('Enforcement receipt does not match the approved run plan')
    if enforcement.prepared_bundle_digest != bundle_digest:
        raise Blocked('Enforcement receipt prepared bundle digest does not match staged inputs')
    if enforcement.provider_config_digest != provider_config_digest:
        raise Blocked('Enforcement receipt provider config digest does not match executable config')
    manifest.update({
        'status': 'BOUND_NOT_RUN',
        'plan_digest': plan.digest(),
        'bundle_digest': bundle_digest,
        'provider_config_digest': provider_config_digest,
        'resource_limits': dict(plan.resource_limits),
    })
    _write_manifest_atomic(manifest_path, manifest)
    return manifest


def _required_file(args, field):
    path = getattr(args, field, None)
    if not isinstance(path, Path) or not path.is_file():
        raise Blocked(f'{field.replace("_", "-")} file is required')
    return path


def _json_file(path, label):
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as exc:
        raise Blocked(f'Cannot load {label}: {exc}') from None
    if not isinstance(value, dict):
        raise Blocked(f'{label} must contain a JSON object')
    return value


def assess_inputs(args):
    """Load trusted policy inputs and return their fail-closed decision."""
    plan_path = _required_file(args, 'run_plan')
    approval_path = _required_file(args, 'approval_receipt')
    enforcement_path = _required_file(args, 'enforcement_receipt')
    inventory_path = _required_file(args, 'capability_inventory')
    plan = RunPlan.from_dict(_json_file(plan_path, 'run plan'))
    approval = ApprovalReceipt.from_dict(_json_file(approval_path, 'approval receipt'))
    enforcement = EnforcementReceipt.from_dict(
        _json_file(enforcement_path, 'enforcement receipt')
    )
    inventory = load_inventory(inventory_path)
    decision = assess_run(
        plan,
        approval,
        enforcement,
        inventory,
        observed_versions=inspect_installed_versions(),
        observed_platform=inspect_platform_fingerprint(),
    )
    return decision, plan, inventory, enforcement


def execute(args, env=None):
    decision, plan, inventory, enforcement = assess_inputs(args)
    if decision.decision != 'APPROVED':
        raise Blocked('; '.join(decision.reasons))
    for probe_id in ('provider-auth-gateway', 'resource-limits'):
        if enforcement.probe_results.get(probe_id) != 'PASS':
            raise Blocked(f'enforcement probe {probe_id} is required before execution')
    bundle = args.bundle.resolve()
    manifest_path = bundle / 'manifest.json'
    manifest = _json_file(manifest_path, 'prepared bundle manifest')
    harness = choose_harness(None, env, for_execution=True)
    if harness != manifest.get('harness'):
        raise Blocked('Prepared bundle belongs to another provider; no cross-provider execution')
    if manifest.get('status') != 'BOUND_NOT_RUN':
        raise Blocked('Bundle is not a fresh bound case')
    if str(manifest.get('case_id')) != str(plan.case_id):
        raise Blocked('Prepared bundle case does not match approved run plan case')
    if manifest.get('plan_digest') != plan.digest():
        raise Blocked('Prepared bundle is not bound to the approved plan digest')
    if manifest.get('resource_limits') != dict(plan.resource_limits):
        raise Blocked('Prepared bundle resource limits do not match approved plan')
    if manifest.get('bundle_digest') != _bundle_digest(bundle):
        raise Blocked('Prepared bundle digest changed after approval binding')
    if manifest.get('bundle_digest') != enforcement.prepared_bundle_digest:
        raise Blocked('Enforcement receipt does not match the bound bundle digest')
    if manifest.get('provider_config_digest') != _provider_config_digest(bundle, manifest):
        raise Blocked('Executable provider configuration changed after binding')
    if manifest.get('provider_config_digest') != enforcement.provider_config_digest:
        raise Blocked('Enforcement receipt provider config digest changed after binding')
    for field in (
        'provider', 'provider_version', 'model', 'model_version',
        'adapter', 'adapter_version',
    ):
        if manifest.get(field) != getattr(plan, field):
            raise Blocked(f'Configured bundle {field} does not match approved plan')
    result_path = _result_path(bundle, manifest)
    if result_path.exists() or result_path.is_symlink():
        raise Blocked('Fresh bound bundle already contains provider results')
    provider_key = inventory.provider_for_plan(plan.provider, plan.adapter)
    if provider_key != harness:
        raise Blocked('Approved provider does not match prepared and active harness')
    cmd = native_command(bundle, manifest)
    binary = shutil.which(cmd[0])
    if not binary:
        raise Blocked(f'Native provider CLI unavailable: {cmd[0]}')
    # Never pull dependencies or run installers here.
    if harness == 'claude':
        env_override = dict(os.environ)
    else:
        env_override = dict(os.environ, PROMPTFOO_DISABLE_TELEMETRY='1',
                            PROMPTFOO_DISABLE_UPDATE='1', PROMPTFOO_DISABLE_SHARING='1',
                            PROMPTFOO_DISABLE_REMOTE_GENERATION='1')
    # The actual isolation policy is the responsibility of the independent host.
    command = [binary, *cmd[1:]]
    manifest['status'] = 'RUNNING'
    nonce_ledger = getattr(args, 'nonce_ledger', None)
    if not isinstance(nonce_ledger, Path):
        raise Blocked('Trusted consumed-nonce ledger is required')
    manifest['execution_id'] = _claim_execution(
        bundle, plan, enforcement, nonce_ledger
    )
    manifest['run_nonce'] = enforcement.run_nonce
    _write_manifest_atomic(manifest_path, manifest)
    try:
        result = subprocess.run(
            command,
            cwd=bundle,
            env=env_override,
            check=False,
            timeout=int(plan.resource_limits['max_seconds']),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        manifest['status'] = 'INFRA_ERROR'
        manifest['execution_error'] = type(exc).__name__
        _write_manifest_atomic(manifest_path, manifest)
        raise Blocked(f'Native {harness} eval did not complete: {type(exc).__name__}') from None
    if result.returncode:
        manifest['status'] = 'INFRA_ERROR'
        manifest['execution_error'] = f'exit-{result.returncode}'
        _write_manifest_atomic(manifest_path, manifest)
        raise Blocked(f'Native {harness} eval exited {result.returncode}; inspect provider output')
    try:
        provider_result_digest(
            result_path,
            max_bytes=int(plan.resource_limits['max_output_bytes']),
        )
        observed_identity = _verified_provider_identity(
            result_path,
            plan,
            max_bytes=int(plan.resource_limits['max_output_bytes']),
        )
    except (EvidenceError, Blocked) as exc:
        manifest['status'] = 'INFRA_ERROR'
        manifest['execution_error'] = 'invalid-provider-result-or-identity'
        _write_manifest_atomic(manifest_path, manifest)
        raise Blocked(f'Native {harness} result is incomplete: {exc}') from None
    manifest['status'] = 'PENDING_HOST_AUDIT'
    manifest['provider_result_digest'] = provider_result_digest(
        result_path,
        max_bytes=int(plan.resource_limits['max_output_bytes']),
    )
    manifest['observed_provider_identity'] = observed_identity
    _write_manifest_atomic(manifest_path, manifest)
    # Do not claim a safety pass: require host-trusted trace/state audit and human review.
    print(f'PROVIDER_NATIVE_RESULTS_PENDING_HOST_AUDIT: {bundle}')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='action', required=True)
    sub.add_parser('inspect', help='detect active harness; never runs model')
    prep = sub.add_parser('prepare', help='prepare provider-native synthetic eval; no model run')
    prep.add_argument('--suite', type=Path, required=True)
    prep.add_argument('--case-id', required=True)
    prep.add_argument('--target-skill', type=Path, required=True)
    prep.add_argument('--output', type=Path, default=Path('eval-workspaces'))
    prep.add_argument('--harness', choices=['claude', 'codex'],
                      help='offline preparation only when no active harness marker exists')
    configure = sub.add_parser(
        'configure', help='materialize exact approved provider settings; never runs model'
    )
    configure.add_argument('--bundle', type=Path, required=True)
    configure.add_argument('--run-plan', type=Path, required=True)
    def add_policy_inputs(parser):
        parser.add_argument('--run-plan', type=Path, required=True)
        parser.add_argument('--approval-receipt', type=Path, required=True)
        parser.add_argument('--enforcement-receipt', type=Path, required=True)
        parser.add_argument('--capability-inventory', type=Path, required=True)
    assess_parser = sub.add_parser('assess', help='assess pinned policy inputs; never runs model')
    add_policy_inputs(assess_parser)
    bind = sub.add_parser('bind', help='bind a prepared bundle to approved policy; never runs model')
    bind.add_argument('--bundle', type=Path, required=True)
    add_policy_inputs(bind)
    run = sub.add_parser('run', help='run provider-native command inside verified isolated host ONLY')
    run.add_argument('--bundle', type=Path, required=True)
    run.add_argument('--nonce-ledger', type=Path, required=True)
    add_policy_inputs(run)
    opts = ap.parse_args(argv)
    try:
        if opts.action == 'inspect':
            print(json.dumps({'active_harness': active_harness(), 'model_executed': False}))
        elif opts.action == 'prepare':
            print('PREPARED_NOT_RUN:', prepare(opts))
        elif opts.action == 'configure':
            plan = RunPlan.from_dict(
                _json_file(_required_file(opts, 'run_plan'), 'run plan')
            )
            configure_prepared_bundle(opts.bundle, plan)
            print('CONFIGURED_NOT_BOUND:', opts.bundle.resolve())
        elif opts.action == 'assess':
            decision, _, _, _ = assess_inputs(opts)
            if decision.decision != 'APPROVED':
                raise Blocked('; '.join(decision.reasons))
            print('APPROVED_NOT_RUN:', json.dumps({
                'decision': decision.decision,
                'backend': decision.backend,
                'model_executed': False,
            }, sort_keys=True))
        elif opts.action == 'bind':
            decision, plan, _, enforcement = assess_inputs(opts)
            if decision.decision != 'APPROVED':
                raise Blocked('; '.join(decision.reasons))
            bind_prepared_bundle(opts.bundle, plan, enforcement)
            print('BOUND_NOT_RUN:', opts.bundle.resolve())
        else:
            return execute(opts)
        return 0
    except (Blocked, OSError, ValueError, TypeError, json.JSONDecodeError) as e:
        print('BLOCKED_NOT_RUN:', e, file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
