"""Independent Docker, gateway, runtime, and provider event attestation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import PurePosixPath
import re
from typing import Any, Mapping, Sequence, Tuple

from docker_policy import DockerRunTopology


class DockerObserverError(ValueError):
    """Observed events are incomplete, ambiguous, or outside the run scope."""


_SCHEMA_VERSION = "0.4"
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_EVENT_TYPES = (
    "daemon",
    "containers",
    "networks",
    "gateway",
    "runtime_processes",
    "provider_session",
    "provider_result",
    "tool_decisions",
    "lifecycle",
    "cleanup",
)
_EVENT_FIELDS = frozenset(("event_id", "type", "run_id", "arm", "observed_at", "payload"))


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _canonical_digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _digest(value: Any, name: str) -> str:
    if not isinstance(value, str) or _DIGEST.fullmatch(value) is None:
        raise DockerObserverError(f"{name} must be a lowercase SHA-256 digest")
    return value


def _optional_digest(value: Any, name: str) -> Any:
    return None if value is None else _digest(value, name)


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise DockerObserverError(f"{name} must be an object")
    return value


def _exact(value: Mapping[str, Any], fields: Sequence[str], name: str) -> None:
    if frozenset(value) != frozenset(fields):
        raise DockerObserverError(f"{name} shape is not exact")


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise DockerObserverError(f"{name} must be a canonical non-empty string")
    return value


def _timestamp(value: Any, name: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        raise DockerObserverError(f"{name} must be an ISO-8601 timestamp") from None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise DockerObserverError(f"{name} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _aware(value: datetime, name: str) -> datetime:
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise DockerObserverError(f"{name} must include a timezone")
    return value.astimezone(timezone.utc)


@dataclass(frozen=True)
class DockerExecutableIdentity:
    image_digest: str
    path: str
    file_digest: str
    argv_digest: str
    role: str
    interpreter_digest: Any
    script_digest: Any

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "DockerExecutableIdentity":
        value = _mapping(value, "executable identity")
        _exact(
            value,
            (
                "image_digest",
                "path",
                "file_digest",
                "argv_digest",
                "role",
                "interpreter_digest",
                "script_digest",
            ),
            "executable identity",
        )
        path = _text(value["path"], "executable path")
        parsed = PurePosixPath(path)
        if not parsed.is_absolute() or ".." in parsed.parts or not path.startswith(
            "/opt/evaluate/"
        ):
            raise DockerObserverError("executable path is outside the reviewed image")
        return cls(
            image_digest=_digest(value["image_digest"], "executable image digest"),
            path=path,
            file_digest=_digest(value["file_digest"], "executable file digest"),
            argv_digest=_digest(value["argv_digest"], "executable argv digest"),
            role=_text(value["role"], "executable role"),
            interpreter_digest=_optional_digest(
                value["interpreter_digest"], "executable interpreter digest"
            ),
            script_digest=_optional_digest(
                value["script_digest"], "executable script digest"
            ),
        )

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "image_digest": self.image_digest,
            "path": self.path,
            "file_digest": self.file_digest,
            "argv_digest": self.argv_digest,
            "role": self.role,
            "interpreter_digest": self.interpreter_digest,
            "script_digest": self.script_digest,
        }


@dataclass(frozen=True)
class DockerCommandDecision:
    session_id: str
    item_id_digest: str
    command_digest: str
    decision: str

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "DockerCommandDecision":
        value = _mapping(value, "Docker command decision")
        _exact(
            value,
            ("session_id", "item_id_digest", "command_digest", "decision"),
            "Docker command decision",
        )
        decision = value["decision"]
        if decision not in ("ALLOW", "DENY"):
            raise DockerObserverError("Docker command decision is invalid")
        return cls(
            session_id=_text(value["session_id"], "command session id"),
            item_id_digest=_digest(value["item_id_digest"], "command item digest"),
            command_digest=_digest(value["command_digest"], "command digest"),
            decision=decision,
        )

    def canonical_payload(self) -> dict[str, str]:
        return {
            "session_id": self.session_id,
            "item_id_digest": self.item_id_digest,
            "command_digest": self.command_digest,
            "decision": self.decision,
        }


@dataclass(frozen=True)
class DockerObserverAttestation:
    schema_version: str
    run_id: str
    arm: str
    plan_digest: str
    topology_digest: str
    daemon_digest: str
    provider: str
    model_version: str
    provider_session_id: str
    provider_result_digest: str
    executable_identities: Tuple[DockerExecutableIdentity, ...]
    command_decisions: Tuple[DockerCommandDecision, ...]
    event_digest: str
    observation_started_at: str
    observation_completed_at: str
    lifecycle_complete: bool
    cleanup_complete: bool
    safety_status: str

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "run_id": self.run_id,
            "arm": self.arm,
            "plan_digest": self.plan_digest,
            "topology_digest": self.topology_digest,
            "daemon_digest": self.daemon_digest,
            "provider": self.provider,
            "model_version": self.model_version,
            "provider_session_id": self.provider_session_id,
            "provider_result_digest": self.provider_result_digest,
            "executable_identities": [
                item.canonical_payload() for item in self.executable_identities
            ],
            "command_decisions": [
                item.canonical_payload() for item in self.command_decisions
            ],
            "event_digest": self.event_digest,
            "observation_started_at": self.observation_started_at,
            "observation_completed_at": self.observation_completed_at,
            "lifecycle_complete": self.lifecycle_complete,
            "cleanup_complete": self.cleanup_complete,
            "safety_status": self.safety_status,
        }

    def digest(self) -> str:
        return _canonical_digest(self.canonical_payload())

    @classmethod
    def synthetic_for_test(
        cls,
        *,
        run_id: str,
        arm: str,
        provider_session_id: str,
        provider_result_digest: str,
        command_decisions: Tuple[DockerCommandDecision, ...],
    ) -> "DockerObserverAttestation":
        """Construct a minimal immutable attestation for parser unit tests only."""

        return cls(
            schema_version=_SCHEMA_VERSION,
            run_id=run_id,
            arm=arm,
            plan_digest="1" * 64,
            topology_digest="2" * 64,
            daemon_digest="3" * 64,
            provider="synthetic",
            model_version="synthetic",
            provider_session_id=provider_session_id,
            provider_result_digest=provider_result_digest,
            executable_identities=(),
            command_decisions=command_decisions,
            event_digest="4" * 64,
            observation_started_at="2026-01-01T00:00:00Z",
            observation_completed_at="2026-01-01T00:00:01Z",
            lifecycle_complete=True,
            cleanup_complete=True,
            safety_status="PASS",
        )


def observe_docker_run(
    topology: DockerRunTopology,
    events: Sequence[Mapping[str, Any]],
    *,
    daemon_digest: str,
    provider: str,
    model_version: str,
    session_id: str,
    provider_result_digest: str,
    approved_executables: Sequence[Mapping[str, Any]],
    observation_started_at: datetime,
    observation_completed_at: datetime,
    expected_exit_code: int = 0,
    expected_timed_out: bool = False,
    expected_output_bytes: int = 1024,
) -> DockerObserverAttestation:
    """Build an attestation only from a complete exact trusted event set."""

    if not isinstance(topology, DockerRunTopology):
        raise DockerObserverError("DockerRunTopology is required")
    daemon_digest = _digest(daemon_digest, "daemon digest")
    provider = _text(provider, "provider")
    model_version = _text(model_version, "model version")
    session_id = _text(session_id, "provider session id")
    provider_result_digest = _digest(
        provider_result_digest, "provider result digest"
    )
    started = _aware(observation_started_at, "observation start")
    completed = _aware(observation_completed_at, "observation completion")
    if completed < started:
        raise DockerObserverError("observation window is reversed")
    if not isinstance(events, (list, tuple)) or len(events) != len(_EVENT_TYPES):
        raise DockerObserverError("observer requires one exact event per event type")

    by_type = {}
    event_ids = set()
    canonical_events = []
    for index, raw in enumerate(events):
        event = _mapping(raw, f"observer event {index}")
        _exact(event, _EVENT_FIELDS, f"observer event {index}")
        event_id = _text(event["event_id"], "observer event id")
        event_type = _text(event["type"], "observer event type")
        if event_id in event_ids or event_type in by_type:
            raise DockerObserverError("observer events must be unique")
        if event_type not in _EVENT_TYPES:
            raise DockerObserverError("observer event type is not approved")
        if event["run_id"] != topology.run_id or event["arm"] != topology.arm:
            raise DockerObserverError("observer event belongs to another run or arm")
        observed = _timestamp(event["observed_at"], "observer event timestamp")
        if observed < started or observed > completed:
            raise DockerObserverError("observer event is outside the run window")
        payload = _mapping(event["payload"], f"{event_type} payload")
        event_ids.add(event_id)
        by_type[event_type] = payload
        canonical_events.append(dict(event))
    if tuple(sorted(by_type)) != tuple(sorted(_EVENT_TYPES)):
        raise DockerObserverError("observer event set is incomplete")

    daemon = by_type["daemon"]
    _exact(daemon, ("identity_digest",), "daemon payload")
    if daemon["identity_digest"] != daemon_digest:
        raise DockerObserverError("observed daemon identity changed")

    containers = by_type["containers"]
    expected_containers = {
        "workload_name": topology.workload.name,
        "workload_image": topology.workload.image,
        "gateway_name": topology.gateway.name,
        "gateway_image": topology.gateway.image,
    }
    if dict(containers) != expected_containers:
        raise DockerObserverError("observed containers differ from topology")
    networks = by_type["networks"]
    if dict(networks) != {
        "internal": topology.internal_network.name,
        "egress": topology.egress_network.name,
    }:
        raise DockerObserverError("observed networks differ from topology")

    gateway = by_type["gateway"]
    expected_gateway = {
        "session_id": session_id,
        "provider": provider,
        "model_version": model_version,
        "role": topology.arm,
        "decision": "ALLOW",
        "provider_result_digest": provider_result_digest,
    }
    if dict(gateway) != expected_gateway:
        raise DockerObserverError("gateway event differs from approved provider scope")
    provider_session = by_type["provider_session"]
    if dict(provider_session) != {
        "session_id": session_id,
        "provider_result_digest": provider_result_digest,
    }:
        raise DockerObserverError("provider session event does not match gateway")
    if dict(by_type["provider_result"]) != {"digest": provider_result_digest}:
        raise DockerObserverError("provider result event digest changed")

    approved = tuple(
        DockerExecutableIdentity.from_dict(value) for value in approved_executables
    )
    runtime = by_type["runtime_processes"]
    _exact(runtime, ("executables",), "runtime process payload")
    values = runtime["executables"]
    if not isinstance(values, list):
        raise DockerObserverError("runtime executable identities must be an array")
    observed_executables = tuple(
        DockerExecutableIdentity.from_dict(value) for value in values
    )
    if observed_executables != approved or len({item.path for item in approved}) != len(
        approved
    ):
        raise DockerObserverError("runtime executable inventory changed")
    image_digest = topology.workload.image.rsplit("@sha256:", 1)[-1]
    if any(item.image_digest != image_digest for item in observed_executables):
        raise DockerObserverError("runtime executable image identity changed")

    decisions_payload = by_type["tool_decisions"]
    _exact(decisions_payload, ("commands",), "tool decisions payload")
    decision_values = decisions_payload["commands"]
    if not isinstance(decision_values, list):
        raise DockerObserverError("tool decisions must be an array")
    decisions = tuple(DockerCommandDecision.from_dict(value) for value in decision_values)
    decision_keys = {
        (item.session_id, item.item_id_digest, item.command_digest) for item in decisions
    }
    if len(decision_keys) != len(decisions) or any(
        item.session_id != session_id for item in decisions
    ):
        raise DockerObserverError("tool decisions are duplicate or cross-session")

    lifecycle = by_type["lifecycle"]
    _exact(lifecycle, ("exit_code", "timed_out", "output_bytes"), "lifecycle payload")
    output_bytes = lifecycle["output_bytes"]
    if isinstance(output_bytes, bool) or not isinstance(output_bytes, int) or output_bytes < 0:
        raise DockerObserverError("lifecycle output size is invalid")
    lifecycle_complete = (
        lifecycle["exit_code"] == expected_exit_code == 0
        and lifecycle["timed_out"] is expected_timed_out is False
        and output_bytes == expected_output_bytes
        and output_bytes <= topology.max_output_bytes
    )
    cleanup = by_type["cleanup"]
    expected_cleanup = {
        "grant_revoked": True,
        "containers_removed": True,
        "volumes_removed": True,
        "networks_removed": True,
    }
    cleanup_complete = dict(cleanup) == expected_cleanup
    safety_status = "PASS" if lifecycle_complete and cleanup_complete else "UNKNOWN"
    return DockerObserverAttestation(
        schema_version=_SCHEMA_VERSION,
        run_id=topology.run_id,
        arm=topology.arm,
        plan_digest=topology.plan_digest,
        topology_digest=topology.digest(),
        daemon_digest=daemon_digest,
        provider=provider,
        model_version=model_version,
        provider_session_id=session_id,
        provider_result_digest=provider_result_digest,
        executable_identities=observed_executables,
        command_decisions=decisions,
        event_digest=_canonical_digest(canonical_events),
        observation_started_at=started.isoformat(),
        observation_completed_at=completed.isoformat(),
        lifecycle_complete=lifecycle_complete,
        cleanup_complete=cleanup_complete,
        safety_status=safety_status,
    )
