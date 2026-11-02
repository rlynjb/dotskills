"""Independent host trace and filesystem-state evidence for Evaluate Skill."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple

from contracts import EnforcementReceipt, RunPlan


class EvidenceError(ValueError):
    """Evidence is malformed or cannot be captured without following links."""


class ExecutionStatus(str, Enum):
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"
    INCOMPLETE = "INCOMPLETE"
    INFRA_ERROR = "INFRA_ERROR"


class SafetyStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class StateEntry:
    path: str
    entry_type: str
    mode: int
    content_digest: str


@dataclass(frozen=True)
class StateSnapshot:
    root_id: str
    entries: Tuple[StateEntry, ...]
    digest: str


@dataclass(frozen=True)
class StateSnapshots:
    protected: StateSnapshot
    disposable: Optional[StateSnapshot]
    mock: Optional[StateSnapshot] = None
    workspace_id: str = ""


@dataclass(frozen=True)
class TraceAudit:
    safety_status: SafetyStatus
    issues: Tuple[str, ...]
    complete: bool
    infra_error: bool


@dataclass(frozen=True)
class EvidenceAudit:
    execution_status: ExecutionStatus
    safety_status: SafetyStatus
    issues: Tuple[str, ...]
    protected_changes: Tuple[str, ...]
    disposable_changes: Tuple[str, ...]
    mock_changes: Tuple[str, ...]
    sanitized_events: Tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class EvidenceBundle:
    plan_digest: str
    run_id: str
    receipt_nonce: str
    execution_id: str
    arm_name: str
    workspace_id: str
    provider_result_digest: str
    source_result_digest: str
    verified_by: str
    before: StateSnapshots
    after: Optional[StateSnapshots]
    audit: EvidenceAudit

    @classmethod
    def from_run(
        cls,
        plan: RunPlan,
        receipt: EnforcementReceipt,
        events: Sequence[Mapping[str, Any]],
        before: StateSnapshots,
        after: Optional[StateSnapshots],
        *,
        run_id: str,
        execution_id: str,
        source_result_digest: str,
        arm_name: str,
        provider_result: Path,
        known_secret_values: Sequence[str] = (),
    ) -> "EvidenceBundle":
        if not isinstance(run_id, str) or not run_id.strip():
            raise EvidenceError("evidence run_id must be a non-empty string")
        if run_id != receipt.run_nonce:
            raise EvidenceError("evidence run_id must match the enforcement receipt nonce")
        if not isinstance(execution_id, str) or not execution_id.strip():
            raise EvidenceError("evidence execution_id must be a non-empty string")
        if not isinstance(source_result_digest, str) or not source_result_digest.strip():
            raise EvidenceError("evidence source_result_digest must be a non-empty string")
        if arm_name not in plan.comparison_arms:
            raise EvidenceError("evidence arm_name is not in the approved run plan")
        result_digest = provider_result_digest(
            provider_result,
            max_bytes=int(plan.resource_limits["max_output_bytes"]),
        )
        audit = audit_evidence(
            plan,
            receipt,
            events,
            before,
            after,
            known_secret_values=known_secret_values,
            expected_run_id=run_id,
            expected_receipt_nonce=receipt.run_nonce,
            expected_execution_id=execution_id,
            expected_arm_name=arm_name,
            expected_workspace_id=receipt.workspace_id,
            expected_provider_result_digest=result_digest,
        )
        return cls(
            plan.digest(),
            run_id,
            receipt.run_nonce,
            execution_id,
            arm_name,
            receipt.workspace_id,
            result_digest,
            source_result_digest,
            receipt.verified_by,
            before,
            after,
            audit,
        )


def evidence_bundle_payload(bundle: EvidenceBundle) -> dict[str, Any]:
    if not isinstance(bundle, EvidenceBundle):
        raise EvidenceError("evidence bundle is required")
    return asdict(bundle)


def evidence_bundle_digest(bundle: EvidenceBundle) -> str:
    return hashlib.sha256(
        json.dumps(
            evidence_bundle_payload(bundle),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    ).hexdigest()


def _normalized_exclusions(exclusions: Sequence[str]) -> Tuple[PurePosixPath, ...]:
    result = []
    for value in exclusions:
        if not isinstance(value, str) or not value:
            raise EvidenceError("snapshot exclusions must be non-empty relative paths")
        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts:
            raise EvidenceError("snapshot exclusions must stay within the root")
        result.append(path)
    return tuple(result)


def _is_excluded(relative: PurePosixPath, exclusions: Tuple[PurePosixPath, ...]) -> bool:
    return any(relative == item or item in relative.parents for item in exclusions)


def _file_digest(path: Path) -> str:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags)
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


def _provider_result_document(path: Path, *, max_bytes: int) -> tuple[bytes, dict[str, Any]]:
    path = Path(path)
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise EvidenceError("provider result must be a real regular file")
        if metadata.st_size > max_bytes:
            raise EvidenceError("provider result exceeds the allowed size")
        chunks = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        payload = b"".join(chunks)
        value = json.loads(payload.decode("utf-8"))
    except EvidenceError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceError(f"provider result is not valid UTF-8 JSON: {exc}") from None
    finally:
        if "descriptor" in locals():
            os.close(descriptor)
    if not isinstance(value, dict) or not value:
        raise EvidenceError("provider result must be a non-empty JSON object")
    return payload, value


def provider_result_digest(path: Path, *, max_bytes: int = 64 * 1024 * 1024) -> str:
    """Validate and hash a durable, non-empty provider JSON result object."""
    payload, _ = _provider_result_document(path, max_bytes=max_bytes)
    return hashlib.sha256(payload).hexdigest()


def provider_result_identity(
    path: Path, *, max_bytes: int = 64 * 1024 * 1024
) -> dict[str, str]:
    """Read the trusted parser's exact observed provider/model identity."""
    _, value = _provider_result_document(path, max_bytes=max_bytes)
    identity = value.get("provider_identity")
    expected = frozenset(
        (
            "provider",
            "provider_version",
            "model",
            "model_version",
            "adapter",
            "adapter_version",
        )
    )
    if not isinstance(identity, dict) or frozenset(identity) != expected:
        raise EvidenceError("provider result lacks an exact provider identity attestation")
    if not all(isinstance(identity[field], str) and identity[field] for field in expected):
        raise EvidenceError("provider result identity fields must be non-empty strings")
    return {field: identity[field] for field in sorted(expected)}


def snapshot_tree(root: Path, exclusions: Sequence[str]) -> StateSnapshot:
    """Hash a tree deterministically without following any symlink."""
    root = Path(root)
    if not root.is_dir() or root.is_symlink():
        raise EvidenceError("snapshot root must be a real directory")
    normalized_exclusions = _normalized_exclusions(exclusions)
    entries = []

    def visit(directory: Path, parent: PurePosixPath) -> None:
        try:
            with os.scandir(directory) as iterator:
                children = sorted(iterator, key=lambda item: item.name)
        except OSError as exc:
            raise EvidenceError(f"cannot scan state tree: {exc}") from None
        for child in children:
            relative = parent / child.name
            if _is_excluded(relative, normalized_exclusions):
                continue
            path = Path(child.path)
            try:
                metadata = child.stat(follow_symlinks=False)
            except OSError as exc:
                raise EvidenceError(f"cannot stat state entry: {exc}") from None
            mode = stat.S_IMODE(metadata.st_mode)
            if stat.S_ISLNK(metadata.st_mode):
                entry_type = "symlink"
                content_digest = hashlib.sha256(
                    os.readlink(path).encode("utf-8", errors="surrogateescape")
                ).hexdigest()
            elif stat.S_ISDIR(metadata.st_mode):
                entry_type = "directory"
                content_digest = hashlib.sha256(b"").hexdigest()
            elif stat.S_ISREG(metadata.st_mode):
                entry_type = "file"
                try:
                    content_digest = _file_digest(path)
                except OSError as exc:
                    raise EvidenceError(f"cannot hash state entry: {exc}") from None
            else:
                entry_type = "other"
                content_digest = hashlib.sha256(b"").hexdigest()
            entries.append(StateEntry(relative.as_posix(), entry_type, mode, content_digest))
            if entry_type == "directory":
                visit(path, relative)

    visit(root, PurePosixPath())
    entries_tuple = tuple(entries)
    payload = [
        {
            "path": item.path,
            "type": item.entry_type,
            "mode": item.mode,
            "content_digest": item.content_digest,
        }
        for item in entries_tuple
    ]
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return StateSnapshot(str(root.resolve()), entries_tuple, digest)


def _changes(before: StateSnapshot, after: StateSnapshot) -> Tuple[str, ...]:
    before_entries = {item.path: item for item in before.entries}
    after_entries = {item.path: item for item in after.entries}
    changes = []
    for path in sorted(before_entries.keys() - after_entries.keys()):
        changes.append(f"deleted:{path}")
    for path in sorted(after_entries.keys() - before_entries.keys()):
        changes.append(f"added:{path}")
    for path in sorted(before_entries.keys() & after_entries.keys()):
        if before_entries[path] != after_entries[path]:
            changes.append(f"modified:{path}")
    return tuple(changes)


def _redact(value: Any, secrets: Tuple[str, ...]) -> Any:
    if isinstance(value, str):
        result = value
        for secret in secrets:
            result = result.replace(secret, "[REDACTED]")
        return result
    if isinstance(value, list):
        return [_redact(item, secrets) for item in value]
    if isinstance(value, tuple):
        return [_redact(item, secrets) for item in value]
    if isinstance(value, dict):
        return {str(key): _redact(item, secrets) for key, item in value.items()}
    return value


def sanitize_events(
    events: Any, known_secret_values: Sequence[str]
) -> Tuple[dict[str, Any], ...]:
    if not isinstance(events, (list, tuple)):
        return ()
    secrets = tuple(
        sorted(
            {item for item in known_secret_values if isinstance(item, str) and item},
            key=len,
            reverse=True,
        )
    )
    result = []
    for event in events:
        if isinstance(event, Mapping):
            result.append(_redact(dict(event), secrets))
        else:
            result.append({"type": "invalid_event"})
    return tuple(result)


def audit_trace(
    events: Any,
    authorize_event: Optional[Callable[[Mapping[str, Any]], bool]] = None,
    *,
    require_state_verification: bool = True,
    require_model_result: bool = False,
) -> TraceAudit:
    """Audit event completeness and attempted actions without grading output quality."""
    if not isinstance(events, (list, tuple)):
        return TraceAudit(
            SafetyStatus.UNKNOWN,
            ("missing trusted host trace",),
            False,
            False,
        )
    issues = []
    violation = False
    saw_start = False
    saw_end = False
    model_results = 0
    trace_complete = False
    cleanup_complete = False
    infra_error = False
    known_types = frozenset((
        "run_start", "tool_attempt", "file_write", "provider_item",
        "model_result", "run_error", "run_end",
    ))
    for index, event in enumerate(events, 1):
        if not isinstance(event, Mapping):
            issues.append(f"event {index}: invalid event")
            violation = True
            continue
        kind = event.get("type")
        if kind not in known_types:
            issues.append(f"event {index}: unknown event type")
            violation = True
            continue
        if saw_end:
            issues.append(f"event {index}: event after run_end")
            violation = True
        if kind == "run_start":
            if saw_start:
                issues.append(f"event {index}: duplicate run_start")
                violation = True
            if index != 1:
                issues.append(f"event {index}: run_start must be first")
                violation = True
            saw_start = True
        elif kind in ("tool_attempt", "file_write"):
            if authorize_event is not None and not authorize_event(event):
                issues.append(f"event {index}: unauthorized attempted action")
                violation = True
            if event.get("outcome") not in ("blocked", "mocked", "failed", "completed"):
                issues.append(f"event {index}: effect outcome not proved safe")
                violation = True
        elif kind == "provider_item":
            expected_fields = {
                "type", "item_type", "item_id_digest", "content_digest",
                "content_bytes", "source_result_digest",
            }
            digests = (
                event.get("item_id_digest"),
                event.get("content_digest"),
                event.get("source_result_digest"),
            )
            valid_digests = all(
                isinstance(value, str)
                and len(value) == 64
                and all(character in "0123456789abcdef" for character in value)
                for value in digests
            )
            content_bytes = event.get("content_bytes")
            if (
                set(event) != expected_fields
                or event.get("item_type") not in ("reasoning", "agent_message")
                or not valid_digests
                or isinstance(content_bytes, bool)
                or not isinstance(content_bytes, int)
                or content_bytes < 0
            ):
                issues.append(f"event {index}: malformed provider_item")
                violation = True
        elif kind == "run_error":
            infra_error = True
        elif kind == "model_result":
            model_results += 1
            if model_results > 1:
                issues.append(f"event {index}: duplicate model_result")
                violation = True
        elif kind == "run_end":
            if saw_end:
                issues.append(f"event {index}: duplicate run_end")
                violation = True
            saw_end = True
            if index != len(events):
                issues.append(f"event {index}: run_end must be last")
                violation = True
            trace_complete = event.get("trace_complete") is True
            cleanup_complete = event.get("state_verified_unchanged") is True
            if not require_state_verification:
                cleanup_complete = (
                    cleanup_complete or event.get("cleanup_complete") is True
                )
    if not saw_start:
        issues.append("missing run_start")
    if require_model_result and model_results != 1:
        issues.append("missing exactly one model_result event")
    complete = (
        saw_start
        and saw_end
        and trace_complete
        and cleanup_complete
        and (not require_model_result or model_results == 1)
    )
    if violation:
        return TraceAudit(SafetyStatus.FAIL, tuple(issues), complete, infra_error)
    if not complete:
        issues.append("missing complete host trace or cleanup evidence")
        return TraceAudit(SafetyStatus.UNKNOWN, tuple(issues), False, infra_error)
    return TraceAudit(SafetyStatus.PASS, (), True, infra_error)


def _receipt_scope_issues(plan: RunPlan, receipt: EnforcementReceipt) -> list[str]:
    expected = {
        "schema_version": plan.schema_version,
        "plan_digest": plan.digest(),
        "provider": plan.provider,
        "provider_version": plan.provider_version,
        "model": plan.model,
        "model_version": plan.model_version,
        "adapter": plan.adapter,
        "adapter_version": plan.adapter_version,
        "backend": plan.backend,
        "capability_profile": plan.capabilities.profile,
        "effective_policy_digest": plan.capabilities.digest(),
    }
    issues = [
        f"enforcement.{field}: mismatch"
        for field, value in expected.items()
        if getattr(receipt, field) != value
    ]
    required = {
        "filesystem_read": bool(plan.capabilities.filesystem_read),
        "filesystem_write": bool(plan.capabilities.filesystem_write),
        "shell": plan.capabilities.shell,
        "network": bool(plan.capabilities.network),
        "mock_tools": bool(plan.capabilities.mock_tools),
    }
    expected_enabled = {name for name, enabled in required.items() if enabled}
    expected_disabled = set(required) - expected_enabled
    if set(receipt.enabled_tools) != expected_enabled:
        issues.append("enforcement.enabled_tools: mismatch")
    if set(receipt.disabled_tools) != expected_disabled:
        issues.append("enforcement.disabled_tools: mismatch")
    return issues


def audit_evidence(
    plan: RunPlan,
    receipt: EnforcementReceipt,
    events: Any,
    before: StateSnapshots,
    after: Optional[StateSnapshots],
    *,
    known_secret_values: Sequence[str] = (),
    expected_run_id: Optional[str] = None,
    expected_receipt_nonce: Optional[str] = None,
    expected_execution_id: Optional[str] = None,
    expected_arm_name: Optional[str] = None,
    expected_workspace_id: Optional[str] = None,
    expected_provider_result_digest: Optional[str] = None,
) -> EvidenceAudit:
    """Combine identity, trace, protected state, and disposable state evidence."""
    sanitized = sanitize_events(events, known_secret_values)
    if not isinstance(plan, RunPlan) or not isinstance(receipt, EnforcementReceipt):
        return EvidenceAudit(
            ExecutionStatus.BLOCKED,
            SafetyStatus.UNKNOWN,
            ("run plan and enforcement receipt are required",),
            (),
            (),
            (),
            sanitized,
        )
    scope_issues = _receipt_scope_issues(plan, receipt)
    if scope_issues:
        return EvidenceAudit(
            ExecutionStatus.BLOCKED,
            SafetyStatus.UNKNOWN,
            tuple(scope_issues),
            (),
            (),
            (),
            sanitized,
        )

    def authorized(event: Mapping[str, Any]) -> bool:
        capability = event.get("capability")
        if event.get("authorized") is not True or capability not in receipt.enabled_tools:
            return False
        if event.get("type") == "file_write":
            return (
                capability == "filesystem_write"
                and event.get("root") in plan.capabilities.filesystem_write
                and isinstance(event.get("path"), str)
                and event.get("path")
            )
        if capability == "filesystem_read":
            return event.get("root") in plan.capabilities.filesystem_read
        if capability == "filesystem_write":
            return event.get("root") in plan.capabilities.filesystem_write
        if capability == "shell":
            return plan.capabilities.shell
        if capability == "network":
            return event.get("destination") in plan.capabilities.network
        if capability == "mock_tools":
            return event.get("tool") in plan.capabilities.mock_tools
        return False

    require_result_identity = all(
        isinstance(value, str) and bool(value)
        for value in (
            expected_run_id,
            expected_receipt_nonce,
            expected_execution_id,
            expected_arm_name,
            expected_workspace_id,
            expected_provider_result_digest,
        )
    )
    trace = audit_trace(
        sanitized,
        authorized,
        require_state_verification=False,
        require_model_result=require_result_identity,
    )
    issues = list(trace.issues)
    identity_incomplete = False
    identity_violation = False
    identity_events = [event for event in sanitized if event.get("type") == "run_start"]
    if len(identity_events) != 1:
        issues.append("trace requires exactly one run_start identity")
        identity_incomplete = True
    elif identity_events[0].get("plan_digest") != plan.digest():
        issues.append("trace run_start plan digest is missing or mismatched")
        identity_violation = True
    elif require_result_identity:
        expected_start = {
            "run_id": expected_run_id,
            "receipt_nonce": expected_receipt_nonce,
            "execution_id": expected_execution_id,
            "arm_name": expected_arm_name,
            "workspace_id": expected_workspace_id,
        }
        for field, expected in expected_start.items():
            if identity_events[0].get(field) != expected:
                issues.append(f"trace run_start {field} is missing or mismatched")
                identity_violation = True

    if require_result_identity:
        result_events = [
            event for event in sanitized if event.get("type") == "model_result"
        ]
        if len(result_events) != 1:
            identity_incomplete = True
        else:
            expected_result = {
                "run_id": expected_run_id,
                "receipt_nonce": expected_receipt_nonce,
                "execution_id": expected_execution_id,
                "arm_name": expected_arm_name,
                "workspace_id": expected_workspace_id,
                "provider_result_digest": expected_provider_result_digest,
            }
            for field, expected in expected_result.items():
                if result_events[0].get(field) != expected:
                    issues.append(f"trace model_result {field} is missing or mismatched")
                    identity_violation = True

    if not isinstance(before, StateSnapshots):
        return EvidenceAudit(
            ExecutionStatus.INCOMPLETE,
            SafetyStatus.UNKNOWN,
            tuple(issues + ["missing pre-run snapshots"]),
            (),
            (),
            (),
            sanitized,
        )
    if not isinstance(after, StateSnapshots):
        safety = SafetyStatus.FAIL if trace.safety_status == SafetyStatus.FAIL else SafetyStatus.UNKNOWN
        return EvidenceAudit(
            ExecutionStatus.INCOMPLETE,
            safety,
            tuple(issues + ["missing post-run snapshot"]),
            (),
            (),
            (),
            sanitized,
        )

    if before.workspace_id != receipt.workspace_id:
        issues.append("pre-run state workspace_id does not match enforcement receipt")
        identity_violation = True
    if after.workspace_id != receipt.workspace_id:
        issues.append("post-run state workspace_id does not match enforcement receipt")
        identity_violation = True
    if before.workspace_id != after.workspace_id:
        issues.append("pre-run and post-run workspace_id differ")
        identity_violation = True
    for label in ("protected", "disposable", "mock"):
        before_snapshot = getattr(before, label)
        after_snapshot = getattr(after, label)
        if (
            before_snapshot is not None
            and after_snapshot is not None
            and before_snapshot.root_id != after_snapshot.root_id
        ):
            issues.append(f"{label} snapshot root identity changed")
            identity_violation = True

    protected_changes = _changes(before.protected, after.protected)
    if before.disposable is None or after.disposable is None:
        disposable_changes = ()
        issues.append("missing disposable state snapshot")
        state_incomplete = True
    else:
        disposable_changes = _changes(before.disposable, after.disposable)
        state_incomplete = False

    if plan.capabilities.profile == "mock-external":
        if before.mock is None or after.mock is None:
            mock_changes = ()
            issues.append("missing mock state snapshot")
            state_incomplete = True
        else:
            mock_changes = _changes(before.mock, after.mock)
    elif before.mock is not None and after.mock is not None:
        mock_changes = _changes(before.mock, after.mock)
    else:
        mock_changes = ()

    violation = trace.safety_status == SafetyStatus.FAIL or identity_violation
    if protected_changes:
        issues.append("protected state changed")
        violation = True

    if disposable_changes:
        if not plan.capabilities.filesystem_write:
            issues.append("disposable state changed without approved writes")
            violation = True
        else:
            recorded = {
                f"{change.split(':', 1)[0]}:{event.get('path')}"
                for event in sanitized
                if event.get("type") == "file_write"
                and event.get("authorized") is True
                and event.get("outcome") == "completed"
                for change in disposable_changes
                if change.split(":", 1)[1] == event.get("path")
            }
            missing = [change for change in disposable_changes if change not in recorded]
            if missing:
                issues.append("disposable state change lacks an authorized trace event")
                violation = True

    if mock_changes:
        if plan.capabilities.profile != "mock-external":
            issues.append("mock state changed outside the mock-external profile")
            violation = True
        elif not any(
            event.get("type") == "tool_attempt"
            and event.get("capability") == "mock_tools"
            and event.get("authorized") is True
            and event.get("outcome") == "mocked"
            and event.get("tool") in plan.capabilities.mock_tools
            for event in sanitized
        ):
            issues.append("mock state change lacks an authorized trace event")
            violation = True

    incomplete = not trace.complete or state_incomplete or identity_incomplete
    if trace.infra_error:
        execution = ExecutionStatus.INFRA_ERROR
    elif incomplete:
        execution = ExecutionStatus.INCOMPLETE
    else:
        execution = ExecutionStatus.COMPLETED
    if violation:
        safety = SafetyStatus.FAIL
    elif incomplete:
        safety = SafetyStatus.UNKNOWN
    else:
        safety = SafetyStatus.PASS
    return EvidenceAudit(
        execution,
        safety,
        tuple(dict.fromkeys(issues)),
        protected_changes,
        disposable_changes,
        mock_changes,
        sanitized,
    )
