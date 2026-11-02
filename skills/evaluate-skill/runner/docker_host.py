"""Trusted lifecycle owner for one Docker evaluation arm."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple

from docker_contracts import DockerEvidenceBinding
from docker_observer import (
    DockerExecutableIdentity,
    DockerObserverAttestation,
    DockerObserverError,
    observe_docker_run,
)
from docker_policy import (
    DockerCommand,
    DockerPolicyError,
    DockerRunTopology,
    verify_effective_container,
    verify_effective_network,
)
from docker_probes import DockerPreflightResult
from evidence import (
    AuthenticatedEnforcementReceipt,
    EvidenceError,
    EvidenceSigningKey,
    issue_authenticated_enforcement_receipt,
    provider_result_digest,
)


class DockerHostError(ValueError):
    """The Docker live run is unauthorized, drifted, or incompletely observed."""


_SCHEMA_VERSION = "0.4"
_DIGEST = re.compile(r"^[0-9a-f]{64}$")
_AUTH_FIELDS = frozenset(
    (
        "schema_version",
        "plan_digest",
        "topology_digest",
        "preflight_digest",
        "run_id",
        "arm",
        "issued_at",
        "expires_at",
        "nonce",
        "execution_binding_digest",
    )
)
_SNAPSHOT_FIELDS = frozenset(
    (
        "plan_digest",
        "topology_digest",
        "preflight_digest",
        "runtime_digest",
        "image_digest",
        "gateway_policy_digest",
        "fixture_digest",
        "observer_policy_digest",
    )
)


def _digest(value: Any, name: str) -> str:
    if not isinstance(value, str) or _DIGEST.fullmatch(value) is None:
        raise DockerHostError(f"{name} must be a lowercase SHA-256 digest")
    return value


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise DockerHostError(f"{name} must be a canonical non-empty string")
    return value


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise DockerHostError(f"{name} must be an object")
    return value


def _timestamp(value: Any, name: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        raise DockerHostError(f"{name} must be an ISO-8601 timestamp") from None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise DockerHostError(f"{name} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _clock_value(clock: Callable[[], datetime]) -> datetime:
    value = clock()
    if not isinstance(value, datetime) or value.tzinfo is None or value.utcoffset() is None:
        raise DockerHostError("trusted host clock must include a timezone")
    return value.astimezone(timezone.utc)


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _canonical_digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _file_digest_no_follow(path: Path, name: str) -> str:
    descriptor = None
    hasher = hashlib.sha256()
    try:
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > 64 * 1024 * 1024:
            raise DockerHostError(f"{name} is not a bounded regular file")
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                return hasher.hexdigest()
            hasher.update(chunk)
    except DockerHostError:
        raise
    except OSError as exc:
        raise DockerHostError(f"cannot read {name}: {type(exc).__name__}") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)


@dataclass(frozen=True)
class DockerLiveAuthorization:
    schema_version: str
    plan_digest: str
    topology_digest: str
    preflight_digest: str
    run_id: str
    arm: str
    issued_at: str
    expires_at: str
    nonce: str
    execution_binding_digest: str

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "DockerLiveAuthorization":
        value = _mapping(value, "Docker live authorization")
        if frozenset(value) != _AUTH_FIELDS:
            raise DockerHostError("Docker live authorization shape is not exact")
        if value["schema_version"] != _SCHEMA_VERSION:
            raise DockerHostError("Docker live authorization schema is unsupported")
        arm = value["arm"]
        if arm not in ("with-skill", "without-skill"):
            raise DockerHostError("Docker live authorization arm is invalid")
        issued = _timestamp(value["issued_at"], "live authorization issued_at")
        expires = _timestamp(value["expires_at"], "live authorization expires_at")
        if issued >= expires or (expires - issued).total_seconds() > 7200:
            raise DockerHostError("Docker live authorization window is invalid")
        return cls(
            schema_version=_SCHEMA_VERSION,
            plan_digest=_digest(value["plan_digest"], "live authorization plan digest"),
            topology_digest=_digest(
                value["topology_digest"], "live authorization topology digest"
            ),
            preflight_digest=_digest(
                value["preflight_digest"], "live authorization preflight digest"
            ),
            run_id=_text(value["run_id"], "live authorization run id"),
            arm=arm,
            issued_at=value["issued_at"],
            expires_at=value["expires_at"],
            nonce=_text(value["nonce"], "live authorization nonce"),
            execution_binding_digest=_digest(
                value["execution_binding_digest"],
                "live authorization execution binding digest",
            ),
        )

    def valid_at(self, at: datetime) -> bool:
        current = at.astimezone(timezone.utc)
        return _timestamp(self.issued_at, "issued_at") <= current < _timestamp(
            self.expires_at, "expires_at"
        )


@dataclass(frozen=True)
class DockerSupervisedRun:
    execution_status: str
    quality_status: str
    safety_status: str
    model_may_have_executed: bool
    cleanup_complete: bool
    provider_result_digest: Optional[str]
    observer_attestation: Optional[DockerObserverAttestation]
    receipt: Optional[AuthenticatedEnforcementReceipt]
    evidence_artifact: Optional[Path]
    recovery_journal: Path
    issues: Tuple[str, ...]


def _command(topology: DockerRunTopology, action: str, role: str) -> DockerCommand:
    matches = tuple(
        item
        for item in topology.commands
        if item.action == action and item.role == role
    )
    if len(matches) != 1:
        raise DockerHostError(f"topology lacks one exact {action}/{role} command")
    return matches[0]


def _write_exclusive(path: Path, payload: Mapping[str, Any]) -> None:
    encoded = (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    descriptor = None
    try:
        descriptor = os.open(path, flags, 0o600)
        offset = 0
        while offset < len(encoded):
            offset += os.write(descriptor, encoded[offset:])
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = None
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except FileExistsError:
        raise DockerHostError(f"trusted Docker artifact already exists: {path.name}") from None
    except OSError as exc:
        raise DockerHostError(
            f"cannot durably write Docker artifact: {type(exc).__name__}"
        ) from None
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _publish_no_replace(path: Path, payload: Mapping[str, Any]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    _write_exclusive(temporary, payload)
    try:
        os.link(temporary, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        temporary.unlink()
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    except FileExistsError:
        raise DockerHostError("trusted Docker evidence already exists") from None
    except OSError as exc:
        raise DockerHostError(
            f"cannot atomically publish Docker evidence: {type(exc).__name__}"
        ) from None


def load_docker_recovery_journal(path: Path) -> Mapping[str, Any]:
    path = Path(path)
    if path.is_symlink() or not path.is_file() or path.stat().st_size > 1024 * 1024:
        raise DockerHostError("Docker recovery journal is missing or unsafe")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        raise DockerHostError("Docker recovery journal is malformed") from None
    value = _mapping(value, "Docker recovery journal")
    if value.get("status") != "INCOMPLETE" or "signature" in value:
        raise DockerHostError("Docker recovery journal cannot claim signed completion")
    return value


def _run_command(
    runner: Callable[..., Any], topology: DockerRunTopology, command: DockerCommand
) -> Any:
    try:
        result = runner(
            list(command.argv),
            timeout_seconds=topology.timeout_seconds,
            max_output_bytes=topology.max_output_bytes,
        )
    except (TimeoutError, ConnectionError, OSError) as exc:
        raise DockerHostError(f"Docker lifecycle failed: {type(exc).__name__}") from None
    if getattr(result, "returncode", None) != 0:
        raise DockerHostError("Docker lifecycle command returned nonzero status")
    stdout = getattr(result, "stdout", None)
    stderr = getattr(result, "stderr", None)
    if not isinstance(stdout, bytes) or not isinstance(stderr, bytes):
        raise DockerHostError("Docker lifecycle output must be captured as bytes")
    if len(stdout) + len(stderr) > topology.max_output_bytes:
        raise DockerHostError("Docker lifecycle exceeded the approved output limit")
    return result


def _json_result(result: Any, name: str) -> Any:
    try:
        return json.loads(result.stdout.decode("utf-8"))
    except (AttributeError, UnicodeDecodeError, json.JSONDecodeError):
        raise DockerHostError(f"{name} is not valid Docker JSON") from None


def _single_inspect(result: Any, name: str) -> Mapping[str, Any]:
    value = _json_result(result, name)
    if not isinstance(value, list) or len(value) != 1 or not isinstance(value[0], Mapping):
        raise DockerHostError(f"{name} must contain exactly one object")
    return value[0]


def _expected_snapshot(
    topology: DockerRunTopology, preflight: DockerPreflightResult
) -> dict[str, str]:
    return {
        "plan_digest": topology.plan_digest,
        "topology_digest": topology.digest(),
        "preflight_digest": preflight.artifact_digest,
        "runtime_digest": preflight.runtime_digest,
        "image_digest": preflight.image_digest,
        "gateway_policy_digest": preflight.gateway_policy_digest,
        "fixture_digest": preflight.fixture_digest,
        "observer_policy_digest": preflight.observer_policy_digest,
    }


def _revalidate(
    revalidate: Callable[[str], Mapping[str, str]],
    phase: str,
    expected: Mapping[str, str],
) -> None:
    observed = _mapping(revalidate(phase), f"{phase} digest snapshot")
    if frozenset(observed) != _SNAPSHOT_FIELDS or dict(observed) != dict(expected):
        raise DockerHostError(f"trusted Docker digests drifted {phase}")


def _directory(path: Path) -> Path:
    path = Path(path)
    if not path.is_absolute() or path.is_symlink() or not path.is_dir():
        raise DockerHostError("artifact directory must be a real absolute directory")
    for parent in (path, *path.parents):
        if (parent / ".git").exists():
            raise DockerHostError("artifact directory must be outside source repositories")
    return path


def _prevalidate(
    topology: DockerRunTopology,
    preflight: DockerPreflightResult,
    authorization: DockerLiveAuthorization,
    binding: DockerEvidenceBinding,
    signing_key: EvidenceSigningKey,
    gateway_key_digest: str,
    at: datetime,
) -> None:
    if not isinstance(topology, DockerRunTopology):
        raise DockerHostError("DockerRunTopology is required")
    if not isinstance(preflight, DockerPreflightResult) or not preflight.complete:
        raise DockerHostError("complete READY_NOT_RUN Docker preflight is required")
    if not isinstance(authorization, DockerLiveAuthorization) or not authorization.valid_at(at):
        raise DockerHostError("fresh Docker live authorization is required")
    if not isinstance(binding, DockerEvidenceBinding):
        raise DockerHostError("DockerEvidenceBinding is required")
    actual_preflight = _file_digest_no_follow(
        preflight.artifact_path, "Docker preflight artifact"
    )
    if actual_preflight != preflight.artifact_digest:
        raise DockerHostError("Docker preflight artifact changed")
    expected_auth = (
        authorization.plan_digest == topology.plan_digest
        and authorization.topology_digest == topology.digest()
        and authorization.preflight_digest == preflight.artifact_digest
        and authorization.run_id == topology.run_id
        and authorization.arm == topology.arm
        and authorization.execution_binding_digest == binding.execution_binding_digest
    )
    if not expected_auth:
        raise DockerHostError("Docker live authorization scope changed")
    if (
        binding.plan_digest != topology.plan_digest
        or binding.run_nonce != topology.run_id
        or binding.launch_digest != topology.digest()
        or binding.gateway_digest != preflight.gateway_policy_digest
        or binding.observer_digest != preflight.observer_policy_digest
    ):
        raise DockerHostError("Docker evidence binding differs from run scope")
    if not isinstance(signing_key, EvidenceSigningKey):
        raise DockerHostError("external evidence signing key is required")
    gateway_key_digest = _digest(gateway_key_digest, "gateway key digest")
    if gateway_key_digest == signing_key.material_digest:
        raise DockerHostError("gateway and evidence keys must be distinct")
    for container in (topology.workload, topology.gateway):
        if any(Path(mount.source).resolve() == signing_key.path.resolve() for mount in container.mounts):
            raise DockerHostError("evidence signing key must never be mounted")


def _blocked_result(directory: Path, reason: str) -> DockerSupervisedRun:
    return DockerSupervisedRun(
        execution_status="BLOCKED",
        quality_status="UNKNOWN",
        safety_status="UNKNOWN",
        model_may_have_executed=False,
        cleanup_complete=False,
        provider_result_digest=None,
        observer_attestation=None,
        receipt=None,
        evidence_artifact=None,
        recovery_journal=directory / "docker-recovery.json",
        issues=(reason,),
    )


def run_supervised_docker(
    topology: DockerRunTopology,
    *,
    preflight: DockerPreflightResult,
    live_authorization: DockerLiveAuthorization,
    evidence_binding: DockerEvidenceBinding,
    signing_key: EvidenceSigningKey,
    gateway_key_digest: str,
    runner: Callable[..., Any],
    revalidate: Callable[[str], Mapping[str, str]],
    observer_events: Sequence[Mapping[str, Any]],
    daemon_digest: str,
    approved_executables: Sequence[Mapping[str, Any]],
    provider: str,
    model_version: str,
    session_id: str,
    provider_result: Path,
    state_before_digest: str,
    state_after_digest: str,
    artifact_directory: Path,
    revoke_grant: Callable[[], bool],
    consume_authorization: Callable[[DockerLiveAuthorization], bool],
    clock: Callable[[], datetime],
    quality_status: str,
    publish_hook: Optional[Callable[[Mapping[str, Any]], None]] = None,
) -> DockerSupervisedRun:
    """Own one authorized arm from create through cleanup and signed evidence."""

    directory = _directory(artifact_directory)
    if quality_status not in ("PASS", "FAIL", "UNKNOWN"):
        raise DockerHostError("quality status is invalid")
    at = _clock_value(clock)
    try:
        _prevalidate(
            topology,
            preflight,
            live_authorization,
            evidence_binding,
            signing_key,
            gateway_key_digest,
            at,
        )
        if _digest(daemon_digest, "daemon digest") != preflight.runtime_digest:
            raise DockerHostError("daemon identity differs from accepted preflight")
    except (DockerHostError, OSError) as exc:
        return _blocked_result(directory, str(exc))

    journal_path = directory / "docker-recovery.json"
    evidence_path = directory / "docker-enforcement-evidence.json"
    journal = {
        "schema_version": _SCHEMA_VERSION,
        "status": "INCOMPLETE",
        "plan_digest": topology.plan_digest,
        "topology_digest": topology.digest(),
        "run_id": topology.run_id,
        "arm": topology.arm,
        "authorization_nonce": live_authorization.nonce,
        "created_at": at.isoformat(),
    }
    try:
        _write_exclusive(journal_path, journal)
    except DockerHostError as exc:
        return _blocked_result(directory, str(exc))

    expected = _expected_snapshot(topology, preflight)
    execution_status = "INCOMPLETE"
    safety_status = "UNKNOWN"
    model_may_have_executed = False
    cleanup_complete = True
    provider_digest_value = None
    attestation = None
    receipt = None
    issues = []
    output_bytes = 0
    observation_started = at

    setup = (
        ("create-internal-network", "network"),
        ("create-egress-network", "network"),
        ("create", "gateway"),
        ("connect-egress-network", "gateway"),
        ("inspect-networks", "network"),
        ("inspect", "gateway"),
        ("create", "workload"),
        ("inspect", "workload"),
    )
    cleanup = (
        ("stop", "workload"),
        ("stop", "gateway"),
        ("rm", "workload"),
        ("rm", "gateway"),
        ("remove-networks", "network"),
    )
    try:
        _revalidate(revalidate, "before-create", expected)
        if consume_authorization(live_authorization) is not True:
            raise DockerHostError("Docker live authorization was already consumed")
        for action, role in setup:
            process = _run_command(
                runner, topology, _command(topology, action, role)
            )
            try:
                if action == "inspect-networks":
                    verify_effective_network(
                        _json_result(process, "network inspect"), topology
                    )
                elif action == "inspect":
                    verify_effective_container(
                        _single_inspect(process, role + " inspect"),
                        topology,
                        role,
                    )
            except DockerPolicyError as exc:
                raise DockerHostError(
                    f"effective Docker state drifted: {exc}"
                ) from None
        _revalidate(revalidate, "before-start", expected)
        _run_command(runner, topology, _command(topology, "start", "gateway"))
        model_may_have_executed = True
        process = _run_command(
            runner, topology, _command(topology, "start", "workload")
        )
        output_bytes = len(process.stdout) + len(process.stderr)
        if output_bytes > topology.max_output_bytes:
            raise DockerHostError("provider output exceeded approved limit")
        provider_digest_value = provider_result_digest(
            provider_result, max_bytes=topology.max_output_bytes
        )
        execution_status = "COMPLETED"
    except KeyboardInterrupt:
        issues.append("Docker lifecycle interrupted")
    except Exception as exc:
        issues.append(
            str(exc) if isinstance(exc, (DockerHostError, EvidenceError)) else type(exc).__name__
        )
    finally:
        for action, role in cleanup:
            try:
                _run_command(runner, topology, _command(topology, action, role))
            except (DockerHostError, KeyboardInterrupt):
                cleanup_complete = False
        try:
            if revoke_grant() is not True:
                cleanup_complete = False
        except Exception:
            cleanup_complete = False

    completed_at = _clock_value(clock)
    if execution_status == "COMPLETED" and cleanup_complete and provider_digest_value:
        try:
            attestation = observe_docker_run(
                topology,
                observer_events,
                daemon_digest=daemon_digest,
                provider=provider,
                model_version=model_version,
                session_id=session_id,
                provider_result_digest=provider_digest_value,
                approved_executables=approved_executables,
                observation_started_at=observation_started,
                observation_completed_at=completed_at,
                expected_exit_code=0,
                expected_timed_out=False,
                expected_output_bytes=output_bytes,
            )
            state_before_digest = _digest(state_before_digest, "state before digest")
            state_after_digest = _digest(state_after_digest, "state after digest")
            if evidence_binding.state_digest != state_before_digest:
                raise DockerHostError("state evidence differs from binding")
            safety_status = (
                "PASS"
                if attestation.safety_status == "PASS"
                and state_before_digest == state_after_digest
                else "FAIL"
            )
            state_snapshot_digest = _canonical_digest(
                {"before": state_before_digest, "after": state_after_digest}
            )
            cleanup_evidence_digest = _canonical_digest(
                {
                    "grant_revoked": True,
                    "containers_removed": True,
                    "volumes_removed": True,
                    "networks_removed": True,
                }
            )
            receipt = issue_authenticated_enforcement_receipt(
                evidence_binding,
                status=safety_status,
                arm=topology.arm,
                provider_result_digest=provider_digest_value,
                observer_attestation_digest=attestation.digest(),
                state_snapshot_digest=state_snapshot_digest,
                cleanup_evidence_digest=cleanup_evidence_digest,
                issued_at=completed_at.isoformat(),
                signing_key=signing_key,
            )
            payload = {
                "schema_version": _SCHEMA_VERSION,
                "execution_status": execution_status,
                "quality_status": quality_status,
                "safety_status": safety_status,
                "model_may_have_executed": model_may_have_executed,
                "cleanup_complete": cleanup_complete,
                "observer_attestation": attestation.canonical_payload(),
                "receipt": receipt.canonical_payload(),
            }
            if publish_hook is not None:
                publish_hook(payload)
            _publish_no_replace(evidence_path, payload)
            journal_path.unlink()
            directory_fd = os.open(directory, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        except (Exception, KeyboardInterrupt) as exc:
            execution_status = "INCOMPLETE"
            safety_status = "UNKNOWN"
            attestation = None
            receipt = None
            issues.append(f"evidence publication incomplete: {type(exc).__name__}")
    else:
        if not cleanup_complete:
            issues.append("Docker cleanup is incomplete")
        execution_status = "INCOMPLETE"
        safety_status = "UNKNOWN"

    return DockerSupervisedRun(
        execution_status=execution_status,
        quality_status=quality_status,
        safety_status=safety_status,
        model_may_have_executed=model_may_have_executed,
        cleanup_complete=cleanup_complete,
        provider_result_digest=provider_digest_value,
        observer_attestation=attestation,
        receipt=receipt,
        evidence_artifact=evidence_path if evidence_path.is_file() else None,
        recovery_journal=journal_path,
        issues=tuple(issues),
    )
