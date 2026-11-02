#!/usr/bin/env python3
"""Provider-native Evaluate Skill eval dispatch (experimental; isolated host required).

No cross-provider fallback. Preparing a case never starts a model.
"""
import argparse
from dataclasses import dataclass
from enum import Enum
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid
from typing import Any, Mapping, Optional, Sequence, Tuple

from capability_inventory import load_inventory
from contracts import ApprovalReceipt, EnforcementReceipt, RunPlan
from evidence import EvidenceBundle, ExecutionStatus, SafetyStatus, sanitize_events, snapshot_tree
from execution_policy import assess_run
from native_boundary import NativeBoundaryResult

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
        return (
            {arm.name for arm in self.arms} == {'with-skill', 'without-skill'}
            and all(arm.execution_status == ExecutionStatus.COMPLETED for arm in self.arms)
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
):
    """Prepare paired proof arms only after policy and boundary verification."""
    decision = assess_run(plan, approval, enforcement, inventory)
    if decision.decision != 'APPROVED':
        raise Blocked('; '.join(decision.reasons))
    if not isinstance(boundary_result, NativeBoundaryResult):
        raise Blocked('Verified native boundary result is required')
    if not boundary_result.complete or not boundary_result.is_valid_for(plan, provider_config):
        raise Blocked('Native boundary result is incomplete or does not match the plan')
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
    if result_path is None or not result_path.is_file():
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
                    'config': {'working_dir': f'./{dir_name}', 'sandbox_mode': 'read-only',
                               'approval_policy': 'never', 'network_access_enabled': False,
                               'web_search_enabled': False, 'persist_threads': False,
                               'inherit_process_env': False, 'skip_git_repo_check': True}}
        judge = {'id': 'openai:codex-sdk', 'config': {
            'working_dir': './judge', 'sandbox_mode': 'read-only',
            'approval_policy': 'never', 'network_access_enabled': False,
            'web_search_enabled': False, 'inherit_process_env': False,
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
    (bundle / 'manifest.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    return bundle


def native_command(bundle, manifest):
    harness = manifest['harness']
    if harness == 'claude':
        return ['claude', 'plugin', 'eval', str(bundle / 'plugin'), '--ablation', 'with-without',
                '--no-publish', '--json', str(bundle / 'claude-results.json')]
    if harness == 'codex':
        return ['promptfoo', 'eval', '--config', str(bundle / 'codex' / 'promptfooconfig.yaml'),
                '--no-cache', '--no-share', '--output', str(bundle / 'codex-results.json')]
    raise Blocked('Manifest harness invalid')


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
    decision = assess_run(plan, approval, enforcement, inventory)
    return decision, plan, inventory


def execute(args, env=None):
    decision, plan, inventory = assess_inputs(args)
    if decision.decision != 'APPROVED':
        raise Blocked('; '.join(decision.reasons))
    bundle = args.bundle.resolve()
    manifest = json.loads((bundle / 'manifest.json').read_text(encoding='utf-8'))
    harness = choose_harness(None, env, for_execution=True)
    if harness != manifest.get('harness'):
        raise Blocked('Prepared bundle belongs to another provider; no cross-provider execution')
    if manifest.get('status') != 'PREPARED_NOT_RUN':
        raise Blocked('Bundle is not a fresh prepared case')
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
    result = subprocess.run(command, cwd=bundle, env=env_override, check=False)
    if result.returncode:
        raise Blocked(f'Native {harness} eval exited {result.returncode}; inspect provider output')
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
    def add_policy_inputs(parser):
        parser.add_argument('--run-plan', type=Path, required=True)
        parser.add_argument('--approval-receipt', type=Path, required=True)
        parser.add_argument('--enforcement-receipt', type=Path, required=True)
        parser.add_argument('--capability-inventory', type=Path, required=True)
    assess_parser = sub.add_parser('assess', help='assess pinned policy inputs; never runs model')
    add_policy_inputs(assess_parser)
    run = sub.add_parser('run', help='run provider-native command inside verified isolated host ONLY')
    run.add_argument('--bundle', type=Path, required=True)
    add_policy_inputs(run)
    opts = ap.parse_args(argv)
    try:
        if opts.action == 'inspect':
            print(json.dumps({'active_harness': active_harness(), 'model_executed': False}))
        elif opts.action == 'prepare':
            print('PREPARED_NOT_RUN:', prepare(opts))
        elif opts.action == 'assess':
            decision, _, _ = assess_inputs(opts)
            if decision.decision != 'APPROVED':
                raise Blocked('; '.join(decision.reasons))
            print('APPROVED_NOT_RUN:', json.dumps({
                'decision': decision.decision,
                'backend': decision.backend,
                'model_executed': False,
            }, sort_keys=True))
        else:
            return execute(opts)
        return 0
    except (Blocked, OSError, ValueError, TypeError, json.JSONDecodeError) as e:
        print('BLOCKED_NOT_RUN:', e, file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
