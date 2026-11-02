"""Fail-closed Promptfoo/Codex result parsing for the trusted native host."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from typing import Any, Mapping, Sequence, Tuple

from contracts import RunPlan


class ProviderTraceError(ValueError):
    """Provider output is incomplete, ambiguous, unsafe, or outside the pinned schema."""


@dataclass(frozen=True)
class ObservedSessionIdentity:
    """Provider identity observed independently by the supervising host."""

    role: str
    arm_name: str
    result_index: int
    assertion_index: int
    session_id: str
    execution_id: str
    process_id: int
    parent_process_id: int
    executable_digest: str
    observed_at: str
    provider: str
    provider_version: str
    model: str
    model_version: str
    adapter: str
    adapter_version: str
    provider_config_digest: str


@dataclass(frozen=True)
class ObservedCommandDecision:
    """Canonical command authorization emitted by the trusted boundary."""

    session_id: str
    process_id: int
    item_id_digest: str
    command_digest: str
    capability: str
    canonical_resource: str
    decision: str


@dataclass(frozen=True)
class ObserverAttestation:
    """One host-observer document from which every session identity is derived."""

    schema_version: str
    observer_id: str
    observer_version: str
    execution_id: str
    promptfoo_process_id: int
    executable_digest: str
    provider_config_digest: str
    sessions: Tuple[ObservedSessionIdentity, ...]
    command_decisions: Tuple[ObservedCommandDecision, ...]

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "observer_id": self.observer_id,
            "observer_version": self.observer_version,
            "execution_id": self.execution_id,
            "promptfoo_process_id": self.promptfoo_process_id,
            "executable_digest": self.executable_digest,
            "provider_config_digest": self.provider_config_digest,
            "sessions": [session.__dict__ for session in self.sessions],
            "command_decisions": [
                decision.__dict__ for decision in self.command_decisions
            ],
        }


@dataclass(frozen=True)
class ProviderTraceBinding:
    """Exact configured provider document and independently observed sessions."""

    provider_config_digest: str
    promptfoo_config: Mapping[str, Any]
    execution_id: str
    executable_digest: str
    observer_attestation_digest: str
    observed_sessions: Tuple[ObservedSessionIdentity, ...]
    observed_command_decisions: Tuple[ObservedCommandDecision, ...]


@dataclass(frozen=True)
class ParsedArm:
    arm_name: str
    promptfoo_label: str
    session_id: str
    source_result_digest: str
    provider_result_digest: str
    provider_result: Mapping[str, Any]
    events: Tuple[dict[str, Any], ...]
    quality: Mapping[str, Any]

    def to_payload(self) -> dict[str, Any]:
        return {
            "arm_name": self.arm_name,
            "promptfoo_label": self.promptfoo_label,
            "session_id": self.session_id,
            "source_result_digest": self.source_result_digest,
            "provider_result_digest": self.provider_result_digest,
            "provider_result": dict(self.provider_result),
            "events": [dict(event) for event in self.events],
            "quality": dict(self.quality),
        }


@dataclass(frozen=True)
class ParsedProviderRun:
    eval_id: str
    source_file_digest: str
    provider_config_digest: str
    arms: Tuple[ParsedArm, ...]

    def to_payload(self) -> dict[str, Any]:
        return {
            "eval_id": self.eval_id,
            "source_file_digest": self.source_file_digest,
            "provider_config_digest": self.provider_config_digest,
            "arms": [arm.to_payload() for arm in self.arms],
        }


_ARM_LABELS = {
    "with-skill": "with_skill",
    "without-skill": "without_skill",
}
_OUTPUT_KEYS = frozenset((
    "evalId", "results", "config", "shareableUrl", "metadata", "vars",
    "runtimeOptions",
))
_METADATA_KEYS = frozenset((
    "promptfooVersion", "nodeVersion", "platform", "arch", "exportedAt",
    "evaluationCreatedAt", "author",
))
_SUMMARY_KEYS = frozenset((
    "version", "timestamp", "results", "prompts", "stats", "repeatStability",
))
_STATS_KEYS = frozenset((
    "successes", "failures", "errors", "tokenUsage", "durationMs",
    "generationDurationMs", "evaluationDurationMs", "cacheHits",
))
_RESULT_KEYS = frozenset((
    "id", "description", "promptIdx", "testIdx", "testCase", "promptId",
    "provider", "prompt", "vars", "response", "error", "failureReason",
    "success", "score", "latencyMs", "gradingResult", "namedScores", "cost",
    "incurredCost", "metadata", "tokenUsage", "evaluationId", "traceId",
    "repeatIndex", "repeatGroupId",
))
_RESPONSE_KEYS = frozenset((
    "cached", "cost", "incurredCost", "error", "latencyMs", "metadata",
    "prompt", "raw", "output", "tokenUsage", "isRefusal", "sessionId",
    "guardrails",
))
_GRADING_KEYS = frozenset((
    "pass", "score", "reason", "namedScores", "namedScoreWeights",
    "tokensUsed", "componentResults", "assertion", "comment", "suggestions",
    "metadata",
))
_RUNTIME_KEYS = frozenset((
    "cache", "delay", "generateSuggestions", "suggestionsCount",
    "interactiveProviders", "maxConcurrency", "repeat", "showProgressBar",
    "timeoutMs", "maxEvalTimeMs", "isRedteam", "silent", "filterRange",
    "providerFilter",
))
_PASSIVE_ITEMS = frozenset(("agent_message", "reasoning"))
_PROHIBITED_ITEMS = frozenset((
    "file_change", "mcp_tool_call", "web_search", "collaboration_tool_call",
    "dynamic_tool_call", "spawn_agent", "send_input", "agent_wait", "todo_list",
    "error", "user_message",
))
OBSERVER_SCHEMA_VERSION = "0.4"
OBSERVER_ID = "evaluate-skill-session-observer"
OBSERVER_VERSION = "0.4.0"
_OBSERVER_FIELDS = frozenset((
    "schema_version", "observer_id", "observer_version", "execution_id",
    "promptfoo_process_id", "executable_digest", "provider_config_digest",
    "sessions", "command_decisions",
))
_COMMAND_DECISION_FIELDS = frozenset((
    "session_id", "process_id", "item_id_digest", "command_digest",
    "capability", "canonical_resource", "decision",
))
_COMMAND_CAPABILITIES = frozenset((
    "credentials", "filesystem_read", "filesystem_write", "network", "shell",
))
_CANONICAL_RESOURCE = re.compile(r"[a-z][a-z0-9._:/-]{0,127}")
_SESSION_FIELDS = frozenset((
    "role", "arm_name", "result_index", "assertion_index", "session_id",
    "execution_id", "process_id", "parent_process_id", "executable_digest",
    "observed_at", "provider", "provider_version", "model", "model_version",
    "adapter", "adapter_version", "provider_config_digest",
))


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _text_digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _object(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ProviderTraceError(f"{label} must be an object")
    return value


def _exact_known_keys(
    value: Mapping[str, Any], allowed: frozenset[str], label: str
) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ProviderTraceError(f"{label} has unknown schema fields: {unknown}")


def _nonempty_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProviderTraceError(f"{label} must be a non-empty string")
    return value


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ProviderTraceError(f"{label} must be numeric")
    return float(value)


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


def _read_document(path: Path, max_bytes: int) -> tuple[bytes, Mapping[str, Any]]:
    path = Path(path)
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = None
    try:
        descriptor = os.open(path, flags)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise ProviderTraceError("Promptfoo result must be a real regular file")
        if metadata.st_size <= 0 or metadata.st_size > max_bytes:
            raise ProviderTraceError("Promptfoo result size is outside the approved limit")
        chunks = []
        remaining = max_bytes + 1
        while remaining > 0:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        if len(payload) > max_bytes:
            raise ProviderTraceError("Promptfoo result exceeds the approved limit")
        value = json.loads(payload.decode("utf-8"))
    except ProviderTraceError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProviderTraceError(f"Promptfoo result is not valid UTF-8 JSON: {exc}") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)
    return payload, _object(value, "Promptfoo result")


def _observer_timestamp(value: Any, label: str) -> datetime:
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        raise ProviderTraceError(f"{label} is invalid") from None
    if result.tzinfo is None or result.utcoffset() is None:
        raise ProviderTraceError(f"{label} lacks a timezone")
    return result.astimezone(timezone.utc)


def parse_observer_attestation(
    payload: bytes,
    *,
    expected_execution_id: str,
    expected_executable_digest: str,
    expected_provider_config_digest: str,
    expected_observer_id: str,
    expected_observer_version: str,
    observation_started_at: datetime,
    observation_completed_at: datetime,
) -> ObserverAttestation:
    """Parse the single durable source of independently observed sessions."""
    if not isinstance(payload, bytes) or not payload or len(payload) > 1024 * 1024:
        raise ProviderTraceError("observer attestation bytes are missing or oversized")
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ProviderTraceError("observer attestation is not valid UTF-8 JSON") from None
    document = _object(value, "observer attestation")
    if set(document) != _OBSERVER_FIELDS:
        raise ProviderTraceError("observer attestation shape is not exact")
    expected_top = {
        "schema_version": OBSERVER_SCHEMA_VERSION,
        "observer_id": expected_observer_id,
        "observer_version": expected_observer_version,
        "execution_id": expected_execution_id,
        "executable_digest": expected_executable_digest,
        "provider_config_digest": expected_provider_config_digest,
    }
    for field, expected in expected_top.items():
        if document.get(field) != expected:
            raise ProviderTraceError(f"observer attestation {field} changed")
    promptfoo_pid = document.get("promptfoo_process_id")
    if isinstance(promptfoo_pid, bool) or not isinstance(promptfoo_pid, int) or promptfoo_pid <= 0:
        raise ProviderTraceError("observer Promptfoo process identity is invalid")
    started = observation_started_at.astimezone(timezone.utc)
    completed = observation_completed_at.astimezone(timezone.utc)
    if completed < started:
        raise ProviderTraceError("observer time window is invalid")
    session_values = document.get("sessions")
    if not isinstance(session_values, list) or not session_values:
        raise ProviderTraceError("observer sessions must be a non-empty array")
    sessions = []
    process_ids = set()
    session_ids = set()
    for index, item in enumerate(session_values):
        session = _object(item, f"observer session {index}")
        if set(session) != _SESSION_FIELDS:
            raise ProviderTraceError("observer session shape is not exact")
        try:
            observed = ObservedSessionIdentity(**session)
        except TypeError:
            raise ProviderTraceError("observer session is invalid") from None
        if observed.execution_id != expected_execution_id:
            raise ProviderTraceError("observer session belongs to another execution")
        if observed.session_id in session_ids:
            raise ProviderTraceError("observer session identities must be unique")
        session_ids.add(observed.session_id)
        if observed.executable_digest != expected_executable_digest:
            raise ProviderTraceError("observer session executable identity changed")
        if observed.provider_config_digest != expected_provider_config_digest:
            raise ProviderTraceError("observer session provider config changed")
        if observed.parent_process_id != promptfoo_pid:
            raise ProviderTraceError("observer session is not bound to the Promptfoo process")
        if (
            isinstance(observed.process_id, bool)
            or not isinstance(observed.process_id, int)
            or observed.process_id <= 0
            or observed.process_id == promptfoo_pid
            or observed.process_id in process_ids
        ):
            raise ProviderTraceError("observer child process identity is invalid")
        process_ids.add(observed.process_id)
        observed_at = _observer_timestamp(
            observed.observed_at, "observer session timestamp"
        )
        if observed_at < started or observed_at > completed:
            raise ProviderTraceError("observer session timestamp is outside this run")
        sessions.append(observed)
    sessions_by_id = {session.session_id: session for session in sessions}
    decision_values = document.get("command_decisions")
    if not isinstance(decision_values, list):
        raise ProviderTraceError("observer command decisions must be an array")
    command_decisions = []
    decision_keys = set()
    for index, item in enumerate(decision_values):
        value = _object(item, f"observer command decision {index}")
        if set(value) != _COMMAND_DECISION_FIELDS:
            raise ProviderTraceError("observer command decision shape is not exact")
        try:
            decision = ObservedCommandDecision(**value)
        except TypeError:
            raise ProviderTraceError("observer command decision is invalid") from None
        session = sessions_by_id.get(decision.session_id)
        if session is None or decision.process_id != session.process_id:
            raise ProviderTraceError(
                "observer command decision is not bound to an observed session"
            )
        for digest, label in (
            (decision.item_id_digest, "item id digest"),
            (decision.command_digest, "command digest"),
        ):
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise ProviderTraceError(
                    f"observer command decision {label} is invalid"
                )
        if decision.capability not in _COMMAND_CAPABILITIES:
            raise ProviderTraceError("observer command decision capability is invalid")
        if (
            not isinstance(decision.canonical_resource, str)
            or _CANONICAL_RESOURCE.fullmatch(decision.canonical_resource) is None
        ):
            raise ProviderTraceError(
                "observer command decision canonical resource is invalid"
            )
        if decision.decision not in ("ALLOW", "DENY"):
            raise ProviderTraceError("observer command decision value is invalid")
        key = (
            decision.session_id,
            decision.item_id_digest,
            decision.command_digest,
        )
        if key in decision_keys:
            raise ProviderTraceError("observer command decisions must be unique")
        decision_keys.add(key)
        command_decisions.append(decision)
    return ObserverAttestation(
        schema_version=document["schema_version"],
        observer_id=document["observer_id"],
        observer_version=document["observer_version"],
        execution_id=document["execution_id"],
        promptfoo_process_id=promptfoo_pid,
        executable_digest=document["executable_digest"],
        provider_config_digest=document["provider_config_digest"],
        sessions=tuple(sessions),
        command_decisions=tuple(command_decisions),
    )


def _validate_binding(
    plan: RunPlan, binding: ProviderTraceBinding
) -> tuple[
    dict[str, ObservedSessionIdentity],
    Tuple[ObservedSessionIdentity, ...],
    dict[tuple[str, str, str], ObservedCommandDecision],
]:
    if not isinstance(binding, ProviderTraceBinding):
        raise ProviderTraceError("trusted provider trace binding is required")
    digest = _nonempty_text(binding.provider_config_digest, "provider config digest")
    _object(binding.promptfoo_config, "bound Promptfoo config")
    if not isinstance(binding.observed_sessions, tuple):
        raise ProviderTraceError("observed sessions must be an immutable tuple")
    if not isinstance(binding.observed_command_decisions, tuple):
        raise ProviderTraceError(
            "observed command decisions must be an immutable tuple"
        )
    expected_arms = tuple(plan.comparison_arms)
    if expected_arms != ("with-skill", "without-skill"):
        raise ProviderTraceError("run plan comparison arms are not the approved pair")
    execution_id = _nonempty_text(binding.execution_id, "observer execution id")
    if not re.fullmatch(r"[0-9a-f]{32,64}", execution_id):
        raise ProviderTraceError("observer execution id is invalid")
    for value, label in (
        (binding.executable_digest, "observer executable digest"),
        (binding.observer_attestation_digest, "observer attestation digest"),
    ):
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ProviderTraceError(f"{label} is invalid")
    tests = binding.promptfoo_config.get("tests")
    if not isinstance(tests, list) or len(tests) != 1:
        raise ProviderTraceError("bound Promptfoo config must contain exactly one test")
    assertions = tests[0].get("assert") if isinstance(tests[0], dict) else None
    if not isinstance(assertions, list):
        raise ProviderTraceError("bound Promptfoo judge assertions are invalid")
    judge_count = len(assertions)
    expected_keys = {
        *(("arm", arm, -1) for arm in expected_arms),
        *(("judge", arm, assertion) for arm in expected_arms for assertion in range(judge_count)),
    }
    if len(binding.observed_sessions) != len(expected_keys):
        raise ProviderTraceError("independent arm and judge session observations are incomplete")
    expected_identity = {
        "provider": plan.provider,
        "provider_version": plan.provider_version,
        "model": plan.model,
        "model_version": plan.model_version,
        "adapter": plan.adapter,
        "adapter_version": plan.adapter_version,
    }
    sessions = {}
    observed_keys = set()
    session_ids = set()
    for observed in binding.observed_sessions:
        if not isinstance(observed, ObservedSessionIdentity):
            raise ProviderTraceError("observed session identity has an invalid type")
        arm = observed.arm_name
        key = (observed.role, arm, observed.assertion_index)
        if key not in expected_keys or key in observed_keys:
            raise ProviderTraceError("observed arm/judge sessions are missing, extra, or duplicate")
        observed_keys.add(key)
        if (
            isinstance(observed.result_index, bool)
            or not isinstance(observed.result_index, int)
            or observed.result_index not in (0, 1)
        ):
            raise ProviderTraceError("observed session result index is invalid")
        _nonempty_text(observed.session_id, f"{arm} observed session id")
        if observed.session_id in session_ids:
            raise ProviderTraceError("observed provider session ids must be unique")
        session_ids.add(observed.session_id)
        if observed.execution_id != execution_id:
            raise ProviderTraceError("observed session belongs to another execution")
        if (
            isinstance(observed.process_id, bool)
            or not isinstance(observed.process_id, int)
            or observed.process_id <= 0
        ):
            raise ProviderTraceError("observed session process identity is invalid")
        if observed.executable_digest != binding.executable_digest:
            raise ProviderTraceError("observed session executable identity changed")
        try:
            timestamp = datetime.fromisoformat(observed.observed_at.replace("Z", "+00:00"))
        except (AttributeError, ValueError):
            raise ProviderTraceError("observed session timestamp is invalid") from None
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ProviderTraceError("observed session timestamp lacks a timezone")
        for field, expected in expected_identity.items():
            actual = getattr(observed, field)
            if actual != expected:
                raise ProviderTraceError(f"observed {arm} {field} does not match the run plan")
        if observed.provider_config_digest != digest:
            raise ProviderTraceError(
                f"observed {arm} provider config digest does not match the binding"
            )
        if observed.role == "arm":
            sessions[arm] = observed
    if set(sessions) != set(expected_arms) or observed_keys != expected_keys:
        raise ProviderTraceError("observed session arms are incomplete")
    sessions_by_id = {
        observed.session_id: observed for observed in binding.observed_sessions
    }
    command_decisions = {}
    for decision in binding.observed_command_decisions:
        if not isinstance(decision, ObservedCommandDecision):
            raise ProviderTraceError("observed command decision has an invalid type")
        session = sessions_by_id.get(decision.session_id)
        if (
            session is None
            or session.role != "arm"
            or decision.process_id != session.process_id
        ):
            raise ProviderTraceError(
                "observed command decision is not bound to an arm session"
            )
        for value, label in (
            (decision.item_id_digest, "item id digest"),
            (decision.command_digest, "command digest"),
        ):
            if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
                raise ProviderTraceError(f"observed command {label} is invalid")
        if decision.capability not in _COMMAND_CAPABILITIES:
            raise ProviderTraceError("observed command capability is invalid")
        if (
            not isinstance(decision.canonical_resource, str)
            or _CANONICAL_RESOURCE.fullmatch(decision.canonical_resource) is None
        ):
            raise ProviderTraceError("observed command canonical resource is invalid")
        if decision.decision not in ("ALLOW", "DENY"):
            raise ProviderTraceError("observed command decision value is invalid")
        if decision.decision == "ALLOW":
            approved = {
                "credentials": set(plan.capabilities.credentials),
                "filesystem_read": set(plan.capabilities.filesystem_read),
                "filesystem_write": set(plan.capabilities.filesystem_write),
                "network": set(plan.capabilities.network),
                "shell": {"restricted-shell"} if plan.capabilities.shell else set(),
            }
            if decision.canonical_resource not in approved[decision.capability]:
                raise ProviderTraceError(
                    "observer allowed a command resource outside the run plan"
                )
        key = (
            decision.session_id,
            decision.item_id_digest,
            decision.command_digest,
        )
        if key in command_decisions:
            raise ProviderTraceError("observed command decisions are duplicated")
        command_decisions[key] = decision
    return sessions, binding.observed_sessions, command_decisions


def _validate_metadata(metadata_value: Any, adapter_version: str) -> None:
    metadata = _object(metadata_value, "Promptfoo output metadata")
    _exact_known_keys(metadata, _METADATA_KEYS, "Promptfoo output metadata")
    required = ("promptfooVersion", "nodeVersion", "platform", "arch", "exportedAt")
    for field in required:
        _nonempty_text(metadata.get(field), f"Promptfoo metadata {field}")
    if metadata["promptfooVersion"] != adapter_version:
        raise ProviderTraceError("Promptfoo output version does not match the pinned adapter")


def _validate_runtime_options(value: Any) -> None:
    if value is None:
        return
    options = _object(value, "Promptfoo runtime options")
    _exact_known_keys(options, _RUNTIME_KEYS, "Promptfoo runtime options")
    if options.get("cache") is not False:
        raise ProviderTraceError("Promptfoo runtime cache must be explicitly disabled")
    if "repeat" in options and options["repeat"] != 1:
        raise ProviderTraceError("repeated Promptfoo execution is not approved")
    if options.get("isRedteam") is True:
        raise ProviderTraceError("red-team runtime mode is not approved")


def _contains_cached_grade(value: Any) -> bool:
    if isinstance(value, dict):
        if value.get("cachedResponse") is True:
            return True
        return any(_contains_cached_grade(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_cached_grade(item) for item in value)
    return False


def _quality(result: Mapping[str, Any], secrets: Tuple[str, ...]) -> dict[str, Any]:
    success = result.get("success")
    if not isinstance(success, bool):
        raise ProviderTraceError("Promptfoo result success must be boolean")
    score = _number(result.get("score"), "Promptfoo result score")
    named_scores = _object(result.get("namedScores"), "Promptfoo named scores")
    for name, named_score in named_scores.items():
        _nonempty_text(name, "Promptfoo named score name")
        _number(named_score, f"Promptfoo named score {name}")
    grading = result.get("gradingResult")
    if grading is not None:
        grading = _object(grading, "Promptfoo grading result")
        _exact_known_keys(grading, _GRADING_KEYS, "Promptfoo grading result")
        if _contains_cached_grade(grading):
            raise ProviderTraceError("cache-derived grading result is not accepted")
        if not isinstance(grading.get("pass"), bool):
            raise ProviderTraceError("Promptfoo grading pass must be boolean")
        _number(grading.get("score"), "Promptfoo grading score")
        _nonempty_text(grading.get("reason"), "Promptfoo grading reason")
    return _redact({
        "success": success,
        "score": score,
        "named_scores": dict(named_scores),
        "grading_result": deepcopy_json(grading),
    }, secrets)


def deepcopy_json(value: Any) -> Any:
    """Copy already parsed JSON without retaining caller-owned mutable containers."""
    if isinstance(value, dict):
        return {str(key): deepcopy_json(item) for key, item in value.items()}
    if isinstance(value, list):
        return [deepcopy_json(item) for item in value]
    return value


def _passive_event(
    item: Mapping[str, Any], source_digest: str, secrets: Tuple[str, ...]
) -> dict[str, Any]:
    if set(item) != {"id", "type", "text"}:
        raise ProviderTraceError(
            f"{item.get('type')} item has an incomplete or unknown schema"
        )
    item_id = _nonempty_text(item.get("id"), f"{item.get('type')} item id")
    text = item.get("text")
    if not isinstance(text, str):
        raise ProviderTraceError(f"{item.get('type')} item text must be a string")
    sanitized = _redact(text, secrets)
    return {
        "type": "provider_item",
        "item_type": item["type"],
        "item_id_digest": _text_digest(item_id),
        "content_digest": _text_digest(sanitized),
        "content_bytes": len(sanitized.encode("utf-8")),
        "source_result_digest": source_digest,
    }


def _command_event(
    item: Mapping[str, Any],
    source_digest: str,
    observed: ObservedSessionIdentity,
    command_decisions: Mapping[tuple[str, str, str], ObservedCommandDecision],
    secrets: Tuple[str, ...],
) -> dict[str, Any]:
    required = {
        "id", "type", "command", "aggregated_output", "exit_code", "status"
    }
    if set(item) != required:
        raise ProviderTraceError("command_execution item has an incomplete or unknown schema")
    item_id = _nonempty_text(item.get("id"), "command item id")
    command = _nonempty_text(item.get("command"), "command item command")
    output = item.get("aggregated_output")
    if not isinstance(output, str):
        raise ProviderTraceError("command item aggregated output must be a string")
    exit_code = item.get("exit_code")
    if isinstance(exit_code, bool) or not isinstance(exit_code, int):
        raise ProviderTraceError("command item exit code must be an integer")
    status_value = item.get("status")
    if status_value not in ("completed", "failed"):
        raise ProviderTraceError("command item status is incomplete")
    if (status_value == "completed") != (exit_code == 0):
        raise ProviderTraceError("command item status and exit code disagree")
    sanitized_command = _redact(command, secrets)
    sanitized_output = _redact(output, secrets)
    item_id_digest = _text_digest(item_id)
    command_digest = _text_digest(sanitized_command)
    decision = command_decisions.get((
        observed.session_id,
        item_id_digest,
        command_digest,
    ))
    capability = decision.capability if decision is not None else "shell"
    canonical_resource = (
        decision.canonical_resource if decision is not None else "unattested-command"
    )
    return {
        "type": "tool_attempt",
        "tool": "sandboxed_command",
        "capability": capability,
        "authorized": decision is not None and decision.decision == "ALLOW",
        "authorization_decision": (
            decision.decision if decision is not None else "MISSING"
        ),
        "canonical_resource": canonical_resource,
        "item_id_digest": item_id_digest,
        "command_digest": command_digest,
        "command_bytes": len(sanitized_command.encode("utf-8")),
        "output_digest": _text_digest(sanitized_output),
        "output_bytes": len(sanitized_output.encode("utf-8")),
        "status": status_value,
        "exit_code": exit_code,
        "outcome": "completed" if exit_code == 0 else "failed",
        "source_result_digest": source_digest,
    }


def _turn_events(
    raw: Any,
    response_output: str,
    source_digest: str,
    observed: ObservedSessionIdentity,
    command_decisions: Mapping[tuple[str, str, str], ObservedCommandDecision],
    secrets: Tuple[str, ...],
) -> Tuple[dict[str, Any], ...]:
    if not isinstance(raw, str) or not raw:
        raise ProviderTraceError("Codex response raw turn is missing")
    try:
        turn_value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ProviderTraceError(f"Codex raw turn is not valid JSON: {exc}") from None
    turn = _object(turn_value, "Codex raw turn")
    if set(turn) - {"items", "finalResponse", "usage"}:
        raise ProviderTraceError("Codex raw turn has unknown schema fields")
    if set(turn) < {"items", "finalResponse"}:
        raise ProviderTraceError("Codex raw turn is incomplete")
    final_response = turn.get("finalResponse")
    if not isinstance(final_response, str) or final_response != response_output:
        raise ProviderTraceError("Codex final response does not match Promptfoo output")
    items = turn.get("items")
    if not isinstance(items, list) or not items:
        raise ProviderTraceError("Codex raw turn items are missing")
    events = []
    item_ids = set()
    messages = []
    for item_value in items:
        item = _object(item_value, "Codex turn item")
        item_type = item.get("type")
        if item_type in _PROHIBITED_ITEMS:
            raise ProviderTraceError(f"prohibited Codex item type: {item_type}")
        if item_type not in _PASSIVE_ITEMS and item_type != "command_execution":
            raise ProviderTraceError(f"unknown Codex item type: {item_type}")
        item_id = _nonempty_text(item.get("id"), f"{item_type} item id")
        if item_id in item_ids:
            raise ProviderTraceError("Codex turn contains duplicate item ids")
        item_ids.add(item_id)
        if item_type in _PASSIVE_ITEMS:
            event = _passive_event(item, source_digest, secrets)
            if item_type == "agent_message":
                messages.append(item["text"])
        else:
            event = _command_event(
                item, source_digest, observed, command_decisions, secrets
            )
        events.append(event)
    if not messages or messages[-1] != final_response:
        raise ProviderTraceError("Codex final response lacks a matching agent message")
    return tuple(events)


def _parse_arm(
    result_value: Any,
    plan: RunPlan,
    observed: ObservedSessionIdentity,
    command_decisions: Mapping[tuple[str, str, str], ObservedCommandDecision],
    arm_name: str,
    secrets: Tuple[str, ...],
) -> ParsedArm:
    result = _object(result_value, f"{arm_name} Promptfoo result")
    _exact_known_keys(result, _RESULT_KEYS, f"{arm_name} Promptfoo result")
    required = {
        "promptIdx", "testIdx", "testCase", "promptId", "provider", "prompt",
        "vars", "response", "failureReason", "success", "score", "latencyMs",
        "gradingResult", "namedScores",
    }
    if set(result) < required:
        raise ProviderTraceError(f"{arm_name} Promptfoo result is incomplete")
    if any(field in result for field in (
        "evaluationId", "traceId", "repeatIndex", "repeatGroupId"
    )):
        raise ProviderTraceError("Promptfoo tracing or repeated result fields are not approved")
    if result.get("error") not in (None, ""):
        raise ProviderTraceError(f"{arm_name} Promptfoo result contains an error")
    provider = _object(result.get("provider"), f"{arm_name} provider")
    if set(provider) != {"id", "label"}:
        raise ProviderTraceError(f"{arm_name} provider shape is not exact")
    if provider.get("id") != "openai:codex-sdk":
        raise ProviderTraceError(f"{arm_name} provider is not openai:codex-sdk")
    label = _ARM_LABELS[arm_name]
    if provider.get("label") != label:
        raise ProviderTraceError(f"{arm_name} Promptfoo label does not match")
    response = _object(result.get("response"), f"{arm_name} provider response")
    _exact_known_keys(response, _RESPONSE_KEYS, f"{arm_name} provider response")
    if response.get("cached") not in (None, False):
        raise ProviderTraceError(f"{arm_name} provider response is cache-derived")
    if response.get("error") not in (None, ""):
        raise ProviderTraceError(f"{arm_name} provider response contains an error")
    session_id = _nonempty_text(response.get("sessionId"), f"{arm_name} session id")
    if session_id == "unknown" or session_id != observed.session_id:
        raise ProviderTraceError(f"{arm_name} session identity was not independently observed")
    response_output = response.get("output")
    if not isinstance(response_output, str):
        raise ProviderTraceError(f"{arm_name} provider output must be text")
    source_digest = _digest(result)
    events = _turn_events(
        response.get("raw"),
        response_output,
        source_digest,
        observed,
        command_decisions,
        secrets,
    )
    quality = _quality(result, secrets)
    identity = {
        "provider": observed.provider,
        "provider_version": observed.provider_version,
        "model": observed.model,
        "model_version": observed.model_version,
        "adapter": observed.adapter,
        "adapter_version": observed.adapter_version,
    }
    sanitized_output = _redact(response_output, secrets)
    provider_result = {
        "schema_version": "0.3",
        "arm_name": arm_name,
        "promptfoo_label": label,
        "session_id": session_id,
        "provider_config_digest": observed.provider_config_digest,
        "provider_identity": identity,
        "source_result_digest": source_digest,
        "output_digest": _text_digest(sanitized_output),
        "output_bytes": len(sanitized_output.encode("utf-8")),
    }
    normalized_digest = _digest(provider_result)
    return ParsedArm(
        arm_name=arm_name,
        promptfoo_label=label,
        session_id=session_id,
        source_result_digest=source_digest,
        provider_result_digest=normalized_digest,
        provider_result=provider_result,
        events=events,
        quality=quality,
    )


def parse_promptfoo_result(
    path: Path,
    plan: RunPlan,
    binding: ProviderTraceBinding,
    *,
    known_secret_values: Sequence[str] = (),
) -> ParsedProviderRun:
    """Parse one paired Promptfoo export only when every trusted binding agrees."""
    if not isinstance(plan, RunPlan):
        raise ProviderTraceError("approved run plan is required")
    if plan.provider != "openai" or plan.adapter != "promptfoo-codex-sdk":
        raise ProviderTraceError("only the pinned Codex provider route is supported")
    sessions, observed_sessions, command_decisions = _validate_binding(plan, binding)
    secrets = tuple(sorted(
        {value for value in known_secret_values if isinstance(value, str) and value},
        key=len,
        reverse=True,
    ))
    max_bytes = int(plan.resource_limits["max_output_bytes"])
    payload, document = _read_document(path, max_bytes)
    _exact_known_keys(document, _OUTPUT_KEYS, "Promptfoo result")
    required_top = {"evalId", "results", "config", "shareableUrl", "metadata"}
    if set(document) < required_top:
        raise ProviderTraceError("Promptfoo result is missing required output fields")
    eval_id = _nonempty_text(document.get("evalId"), "Promptfoo eval id")
    if document.get("shareableUrl") is not None:
        raise ProviderTraceError("Promptfoo result unexpectedly contains a shared URL")
    if document.get("config") != binding.promptfoo_config:
        raise ProviderTraceError("Promptfoo output config differs from the bound configuration")
    _validate_metadata(document.get("metadata"), plan.adapter_version)
    _validate_runtime_options(document.get("runtimeOptions"))

    summary = _object(document.get("results"), "Promptfoo result summary")
    _exact_known_keys(summary, _SUMMARY_KEYS, "Promptfoo result summary")
    if summary.get("version") != 3:
        raise ProviderTraceError("Promptfoo result summary version must be exactly 3")
    if "repeatStability" in summary:
        raise ProviderTraceError("Promptfoo repeat-stability output is not approved")
    _nonempty_text(summary.get("timestamp"), "Promptfoo result timestamp")
    if not isinstance(summary.get("prompts"), list):
        raise ProviderTraceError("Promptfoo summary prompts must be a list")
    stats = _object(summary.get("stats"), "Promptfoo result stats")
    _exact_known_keys(stats, _STATS_KEYS, "Promptfoo result stats")
    for field in ("successes", "failures", "errors"):
        value = stats.get(field)
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ProviderTraceError(f"Promptfoo stats {field} must be a non-negative integer")
    cache_hits = stats.get("cacheHits", 0)
    if isinstance(cache_hits, bool) or not isinstance(cache_hits, int) or cache_hits != 0:
        raise ProviderTraceError("Promptfoo result contains response-cache hits")

    results = summary.get("results")
    if not isinstance(results, list) or len(results) != 2:
        raise ProviderTraceError("Promptfoo result must contain exactly two comparison results")
    by_label = {}
    for result_index, result_value in enumerate(results):
        result = _object(result_value, "Promptfoo comparison result")
        provider = _object(result.get("provider"), "Promptfoo comparison provider")
        label = provider.get("label")
        if label not in set(_ARM_LABELS.values()):
            raise ProviderTraceError("Promptfoo result contains an unexpected arm label")
        if label in by_label:
            raise ProviderTraceError("Promptfoo result contains a duplicate comparison arm")
        by_label[label] = (result, result_index)
    if set(by_label) != set(_ARM_LABELS.values()):
        raise ProviderTraceError("Promptfoo comparison arms are incomplete")
    result_indexes = {
        arm: by_label[label][1] for arm, label in _ARM_LABELS.items()
    }
    for observed in observed_sessions:
        if observed.result_index != result_indexes[observed.arm_name]:
            raise ProviderTraceError("observed session result index does not match output")

    arms = tuple(
        _parse_arm(
            by_label[_ARM_LABELS[arm]][0],
            plan,
            sessions[arm],
            command_decisions,
            arm,
            secrets,
        )
        for arm in plan.comparison_arms
    )
    observed_command_keys = {
        (
            arm.session_id,
            event["item_id_digest"],
            event["command_digest"],
        )
        for arm in arms
        for event in arm.events
        if event.get("type") == "tool_attempt"
    }
    if set(command_decisions) - observed_command_keys:
        raise ProviderTraceError(
            "observer command decisions contain extra or mismatched evidence"
        )
    return ParsedProviderRun(
        eval_id=eval_id,
        source_file_digest=hashlib.sha256(payload).hexdigest(),
        provider_config_digest=binding.provider_config_digest,
        arms=arms,
    )
