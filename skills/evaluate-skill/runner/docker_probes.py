"""Trusted no-model Docker probes and durable READY_NOT_RUN publication."""

from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
import os
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple

from docker_policy import (
    DockerCommand,
    DockerPolicyError,
    DockerRunTopology,
    verify_effective_container,
    verify_effective_network,
)


class DockerProbeError(ValueError):
    """Probe inputs, execution, or durable publication are unsafe/incomplete."""


REQUIRED_DOCKER_PROBES = (
    "docker-mount-boundary",
    "docker-readonly-filesystem",
    "docker-network-boundary",
    "docker-gateway-credential-isolation",
    "docker-executable-inventory",
    "docker-tool-broker",
    "docker-protected-state",
    "docker-observer-completeness",
    "docker-cleanup",
)
_SCHEMA_VERSION = "0.4"
_STATUSES = frozenset(("PASS", "FAIL", "UNKNOWN", "INCOMPLETE"))
_DIGEST_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_FORBIDDEN_PATH_KEYS = (
    "host_home",
    "original_repo",
    "provider_auth",
    "rubric",
    "docker_socket",
    "outside_mount",
)
_NETWORK_KEYS = (
    "direct_egress",
    "host_service",
    "metadata",
    "unapproved_sidecar",
)
_EXPECTED_GATEWAY = {
    "valid_synthetic_request": "ALLOWED",
    "wrong_nonce": "DENIED",
    "wrong_provider": "DENIED",
    "wrong_model": "DENIED",
    "wrong_role": "DENIED",
    "over_budget": "DENIED",
    "expired": "DENIED",
    "credential_retrieval": "DENIED",
    "direct_destination": "DENIED",
    "real_credential_exposed": False,
    "provider_called": False,
}
_EXPECTED_TOOL_DECISIONS = (
    ("list", "/fixture", "ALLOWED"),
    ("read", "/fixture/sample.txt", "ALLOWED"),
    ("search", "/fixture", "ALLOWED"),
    ("read", "/etc/passwd", "DENIED"),
    ("read", "/fixture-link", "DENIED"),
)
_MAX_OBSERVATION_BYTES = 1024 * 1024


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _bound_digest(value: Any, name: str) -> str:
    if not isinstance(value, str) or not _DIGEST_PATTERN.fullmatch(value):
        raise DockerProbeError(f"{name} must be one lowercase SHA-256 digest")
    return value


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise DockerProbeError(f"{name} must be an object")
    return value


def _exact_fields(value: Mapping[str, Any], fields: Sequence[str], name: str) -> None:
    expected = frozenset(fields)
    actual = frozenset(value)
    if actual != expected:
        raise DockerProbeError(f"{name} fields are incomplete or unknown")


def _command(
    topology: DockerRunTopology, action: str, role: str
) -> DockerCommand:
    matches = tuple(
        command
        for command in topology.commands
        if command.action == action and command.role == role
    )
    if len(matches) != 1:
        raise DockerProbeError(
            f"topology must contain exactly one {action}/{role} command"
        )
    return matches[0]


def _call_runner(
    runner: Callable[[list[str]], Any], argv: Sequence[str], *, allow_empty: bool
) -> str:
    if not isinstance(argv, (list, tuple)) or not argv or not all(
        isinstance(item, str) and item for item in argv
    ):
        raise DockerProbeError("Docker probe command must be explicit argv")
    try:
        result = runner(list(argv))
    except TimeoutError:
        raise DockerProbeError("Docker probe command timed out") from None
    except Exception as exc:
        raise DockerProbeError(
            f"Docker probe command failed: {type(exc).__name__}"
        ) from None
    if getattr(result, "returncode", None) != 0:
        raise DockerProbeError("Docker probe command returned nonzero status")
    stdout = getattr(result, "stdout", None)
    if not isinstance(stdout, str) or len(stdout.encode("utf-8")) > _MAX_OBSERVATION_BYTES:
        raise DockerProbeError("Docker probe output is missing or oversized")
    if not allow_empty and not stdout:
        raise DockerProbeError("Docker probe output is empty")
    return stdout


def _json_output(
    runner: Callable[[list[str]], Any], argv: Sequence[str], name: str
) -> Any:
    output = _call_runner(runner, argv, allow_empty=False)
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        raise DockerProbeError(f"{name} output is malformed") from None


def _json_lines_output(
    runner: Callable[[list[str]], Any], argv: Sequence[str], name: str
) -> list[Any]:
    output = _call_runner(runner, argv, allow_empty=True)
    if not output.strip():
        return []
    try:
        decoded = json.loads(output)
        if isinstance(decoded, list):
            return decoded
    except json.JSONDecodeError:
        pass
    values = []
    try:
        for line in output.splitlines():
            if line.strip():
                values.append(json.loads(line))
    except json.JSONDecodeError:
        raise DockerProbeError(f"{name} output is malformed") from None
    return values


def _probe_create_command(topology: DockerRunTopology) -> Tuple[str, ...]:
    command = list(_command(topology, "create", "workload").argv)
    try:
        image_index = command.index(topology.workload.image)
    except ValueError:
        raise DockerProbeError("workload create command does not bind its immutable image") from None
    expected_tail = list(topology.workload.command)
    if command[image_index + 1 :] != expected_tail:
        raise DockerProbeError("workload create command differs from topology command")
    return tuple(
        command[: image_index + 1]
        + ["probe", "--binding", "/run/evaluate/binding.json"]
    )


def _parse_inspect(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, list) or len(value) != 1:
        raise DockerProbeError(f"{name} inspect must contain exactly one item")
    return _mapping(value[0], f"{name} inspect item")


def _validated_canaries(value: Mapping[str, Any]) -> Mapping[str, Any]:
    value = _mapping(value, "host canaries")
    _exact_fields(
        value,
        (
            "forbidden_paths",
            "credential_canary",
            "protected_state_before",
            "protected_state_after",
            "fixture_state_before",
            "fixture_state_after",
            "grant_present_before",
            "grant_present_after",
        ),
        "host canaries",
    )
    paths = _mapping(value["forbidden_paths"], "host canary paths")
    _exact_fields(paths, _FORBIDDEN_PATH_KEYS, "host canary paths")
    for name, path in paths.items():
        if not isinstance(path, str) or not Path(path).is_absolute():
            raise DockerProbeError(f"host canary path {name} must be absolute")
    credential = value["credential_canary"]
    if not isinstance(credential, str) or len(credential) < 16:
        raise DockerProbeError("credential canary must be a non-empty secret marker")
    for name in (
        "protected_state_before",
        "protected_state_after",
        "fixture_state_before",
        "fixture_state_after",
    ):
        _bound_digest(value[name], f"host canaries.{name}")
    if value["grant_present_before"] is not True or not isinstance(
        value["grant_present_after"], bool
    ):
        raise DockerProbeError("host canary grant lifecycle is malformed")
    return value


def _validated_inventory(value: Mapping[str, Any]) -> tuple[bool, tuple[str, ...]]:
    try:
        value = _mapping(value, "executable inventory")
        _exact_fields(
            value,
            (
                "schema_version",
                "status",
                "target_platform",
                "allowed_tools",
                "executables",
                "scripts",
            ),
            "executable inventory",
        )
        if (
            value["schema_version"] != _SCHEMA_VERSION
            or value["status"] != "verified"
            or value["target_platform"] != "linux/arm64"
            or value["allowed_tools"] != ["list", "read", "search"]
        ):
            return False, ()
        executables = value["executables"]
        scripts = value["scripts"]
        if not isinstance(executables, list) or not isinstance(scripts, list):
            return False, ()
        paths = []
        for item in executables:
            item = _mapping(item, "executable inventory item")
            _exact_fields(item, ("path", "role", "digest"), "executable inventory item")
            if not isinstance(item["path"], str) or not isinstance(item["role"], str):
                return False, ()
            _bound_digest(item["digest"], "executable inventory digest")
            paths.append(item["path"])
        expected_paths = (
            "/opt/evaluate/bin/python3",
            "/opt/evaluate/bin/node",
            "/opt/evaluate/bin/codex",
            "/opt/evaluate/bin/promptfoo",
        )
        if tuple(paths) != expected_paths:
            return False, ()
        expected_scripts = (
            "/opt/evaluate/codex-entrypoint.py",
            "/opt/evaluate/probe-entrypoint.py",
        )
        actual_scripts = []
        for item in scripts:
            item = _mapping(item, "script inventory item")
            _exact_fields(item, ("path", "interpreter", "digest"), "script inventory item")
            if item["interpreter"] != "/opt/evaluate/bin/python3":
                return False, ()
            _bound_digest(item["digest"], "script inventory digest")
            actual_scripts.append(item["path"])
        if tuple(actual_scripts) != expected_scripts:
            return False, ()
        return True, expected_paths
    except DockerProbeError:
        return False, ()


def _mounts_exclude_canaries(
    topology: DockerRunTopology, paths: Mapping[str, str]
) -> bool:
    canaries = tuple(Path(path) for path in paths.values())
    for container in (topology.workload, topology.gateway):
        for mount in container.mounts:
            source = Path(mount.source)
            lowered = mount.source.lower()
            if "docker.sock" in lowered or "rubric" in lowered or "provider-auth" in lowered:
                return False
            for canary in canaries:
                if (
                    source == canary
                    or source in canary.parents
                    or canary in source.parents
                ):
                    return False
    return True


def _report_checks(
    report: Optional[Mapping[str, Any]],
    topology: DockerRunTopology,
    credential_canary: str,
) -> tuple[bool, Mapping[str, Any]]:
    if report is None:
        return False, MappingProxyType({})
    try:
        if credential_canary in json.dumps(report, sort_keys=True):
            return False, MappingProxyType({})
        _exact_fields(
            report,
            ("schema_version", "status", "plan_digest", "observations"),
            "probe report",
        )
        if (
            report["schema_version"] != _SCHEMA_VERSION
            or report["status"] != "OBSERVED"
            or report["plan_digest"] != topology.plan_digest
        ):
            return False, MappingProxyType({})
        observations = _mapping(report["observations"], "probe observations")
        _exact_fields(
            observations,
            ("forbidden_paths", "writes", "network", "runtime", "inventory", "tools"),
            "probe observations",
        )
        return True, observations
    except (DockerProbeError, TypeError, ValueError):
        return False, MappingProxyType({})


def _enum_map(value: Any, keys: Sequence[str], expected: str) -> bool:
    if not isinstance(value, Mapping) or frozenset(value) != frozenset(keys):
        return False
    return all(value[key] == expected for key in keys)


def _runtime_ok(value: Any) -> bool:
    return value == {
        "uid": 65532,
        "gid": 65532,
        "no_new_privileges": True,
        "seccomp": "FILTERED",
        "effective_capabilities": "0",
        "host_namespaces": False,
    }


def _tools_ok(value: Any) -> bool:
    if not isinstance(value, Mapping):
        return False
    return (
        value.get("allowed_tools") == ["list", "read", "search"]
        and value.get("bounded") is True
        and tuple(tuple(item) for item in value.get("decisions", ()))
        == _EXPECTED_TOOL_DECISIONS
    )


def _inventory_report_ok(
    value: Any, inventory_ok: bool, executable_paths: tuple[str, ...]
) -> bool:
    if not inventory_ok or not isinstance(value, Mapping):
        return False
    return (
        value.get("executables") == list(executable_paths)
        and value.get("processes") == ["/opt/evaluate/bin/python3"]
        and value.get("forbidden_executables") == []
    )


def _result(probe_id: str, status: str, observation: str, evidence: Any) -> "DockerProbeResult":
    if status not in _STATUSES:
        raise DockerProbeError("internal probe status is invalid")
    return DockerProbeResult(
        probe_id=probe_id,
        source="trusted-host",
        status=status,
        observation=observation,
        evidence_digest=_digest(evidence),
    )


@dataclass(frozen=True)
class DockerProbeResult:
    probe_id: str
    source: str
    status: str
    observation: str
    evidence_digest: str

    def canonical_payload(self) -> dict[str, str]:
        return {
            "probe_id": self.probe_id,
            "source": self.source,
            "status": self.status,
            "observation": self.observation,
            "evidence_digest": self.evidence_digest,
        }


@dataclass(frozen=True)
class DockerPreflightResult:
    schema_version: str
    status: str
    model_executed: bool
    plan_digest: str
    runtime_digest: str
    image_digest: str
    topology_digest: str
    probe_topology_digest: str
    gateway_policy_digest: str
    fixture_digest: str
    observer_policy_digest: str
    results: Tuple[DockerProbeResult, ...]
    artifact_digest: str
    artifact_path: Path

    @property
    def complete(self) -> bool:
        ids = tuple(item.probe_id for item in self.results)
        return (
            self.status == "READY_NOT_RUN"
            and self.model_executed is False
            and ids == REQUIRED_DOCKER_PROBES
            and all(item.status == "PASS" for item in self.results)
        )

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "status": self.status,
            "model_executed": self.model_executed,
            "plan_digest": self.plan_digest,
            "runtime_digest": self.runtime_digest,
            "image_digest": self.image_digest,
            "topology_digest": self.topology_digest,
            "probe_topology_digest": self.probe_topology_digest,
            "gateway_policy_digest": self.gateway_policy_digest,
            "fixture_digest": self.fixture_digest,
            "observer_policy_digest": self.observer_policy_digest,
            "results": [item.canonical_payload() for item in self.results],
        }


def _publish_exclusive(path: Path, payload: Mapping[str, Any]) -> str:
    encoded = (
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")
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
        raise DockerProbeError("Docker preflight artifact already exists") from None
    except OSError as exc:
        raise DockerProbeError(
            f"cannot durably publish Docker preflight: {type(exc).__name__}"
        ) from None
    finally:
        if descriptor is not None:
            os.close(descriptor)
    return hashlib.sha256(encoded).hexdigest()


def run_docker_preflight(
    topology: DockerRunTopology,
    *,
    runner: Callable[[list[str]], Any],
    gateway_probe: Callable[[], Mapping[str, Any]],
    host_canaries: Mapping[str, Any],
    executable_inventory: Mapping[str, Any],
    runtime_digest: str,
    image_digest: str,
    gateway_policy_digest: str,
    fixture_digest: str,
    observer_policy_digest: str,
    artifact_directory: Path,
) -> DockerPreflightResult:
    """Run fixed no-model probes; never issue live auth or call a provider."""

    if not isinstance(topology, DockerRunTopology) or topology.schema_version != _SCHEMA_VERSION:
        raise DockerProbeError("a v0.4 DockerRunTopology is required")
    for value, name in (
        (runtime_digest, "runtime_digest"),
        (image_digest, "image_digest"),
        (gateway_policy_digest, "gateway_policy_digest"),
        (fixture_digest, "fixture_digest"),
        (observer_policy_digest, "observer_policy_digest"),
    ):
        _bound_digest(value, name)
    if not topology.workload.image.endswith("@sha256:" + image_digest):
        raise DockerProbeError("image digest differs from the topology workload image")
    directory = Path(artifact_directory)
    if not directory.is_absolute() or directory.is_symlink() or not directory.is_dir():
        raise DockerProbeError("artifact directory must be a real absolute directory")
    for parent in (directory, *directory.parents):
        if (parent / ".git").exists():
            raise DockerProbeError("artifact directory must be outside source repositories")
    artifact_path = directory / "docker-preflight.json"
    if artifact_path.exists() or artifact_path.is_symlink():
        raise DockerProbeError("Docker preflight artifact already exists")
    canaries = _validated_canaries(host_canaries)
    inventory_ok, executable_paths = _validated_inventory(executable_inventory)
    probe_workload = replace(
        topology.workload,
        command=("probe", "--binding", "/run/evaluate/binding.json"),
    )
    probe_topology = replace(topology, workload=probe_workload, commands=())
    if not topology.commands:
        raise DockerProbeError("topology command set is empty")
    docker = topology.commands[0].argv[0]
    if not Path(docker).is_absolute() or any(
        not command.argv or command.argv[0] != docker for command in topology.commands
    ):
        raise DockerProbeError("topology commands do not share one absolute Docker client")
    probe_create = _probe_create_command(topology)
    report: Optional[Mapping[str, Any]] = None
    host_verified = True
    execution_complete = True
    cleanup_commands_complete = True
    cleanup_state = {"containers": None, "networks": None, "volumes": None}

    setup_commands = (
        _command(topology, "create-internal-network", "network").argv,
        _command(topology, "create-egress-network", "network").argv,
        _command(topology, "create", "gateway").argv,
        _command(topology, "connect-egress-network", "gateway").argv,
        probe_create,
    )
    try:
        for argv in setup_commands:
            _call_runner(runner, argv, allow_empty=True)
        network_payload = _json_output(
            runner,
            _command(topology, "inspect-networks", "network").argv,
            "network inspect",
        )
        try:
            verify_effective_network(network_payload, probe_topology)
        except DockerPolicyError:
            host_verified = False
        gateway_payload = _parse_inspect(
            _json_output(
                runner,
                _command(topology, "inspect", "gateway").argv,
                "gateway inspect",
            ),
            "gateway",
        )
        workload_payload = _parse_inspect(
            _json_output(
                runner,
                _command(topology, "inspect", "workload").argv,
                "workload inspect",
            ),
            "workload",
        )
        try:
            verify_effective_container(gateway_payload, probe_topology, "gateway")
            verify_effective_container(workload_payload, probe_topology, "workload")
        except DockerPolicyError:
            host_verified = False
        _call_runner(
            runner, _command(topology, "start", "gateway").argv, allow_empty=True
        )
        attached = (
            topology.commands[0].argv[0],
            "start",
            "--attach",
            topology.workload.name,
        )
        raw_report = _json_output(runner, attached, "workload probe")
        report = _mapping(raw_report, "workload probe report")
    except DockerProbeError:
        execution_complete = False
    finally:
        for action, role in (
            ("stop", "workload"),
            ("stop", "gateway"),
            ("rm", "workload"),
            ("rm", "gateway"),
            ("remove-networks", "network"),
        ):
            try:
                _call_runner(
                    runner, _command(topology, action, role).argv, allow_empty=True
                )
            except DockerProbeError:
                cleanup_commands_complete = False
        cleanup_queries = {
            "containers": (
                docker,
                "ps",
                "-a",
                "--filter",
                "label=evaluate.plan=" + topology.plan_digest,
                "--format",
                "{{json .}}",
            ),
            "networks": (
                docker,
                "network",
                "ls",
                "--filter",
                "label=evaluate.plan=" + topology.plan_digest,
                "--format",
                "{{json .}}",
            ),
            "volumes": (
                docker,
                "volume",
                "ls",
                "--filter",
                "label=evaluate.plan=" + topology.plan_digest,
                "--format",
                "{{json .}}",
            ),
        }
        for name, argv in cleanup_queries.items():
            try:
                value = _json_lines_output(runner, argv, f"cleanup {name}")
                cleanup_state[name] = value
            except DockerProbeError:
                cleanup_commands_complete = False

    report_valid, observations = _report_checks(
        report, topology, canaries["credential_canary"]
    )
    try:
        gateway_observation = _mapping(gateway_probe(), "synthetic gateway probe")
        gateway_ok = dict(gateway_observation) == _EXPECTED_GATEWAY
    except Exception:
        gateway_observation = MappingProxyType({})
        gateway_ok = False

    paths_ok = _mounts_exclude_canaries(topology, canaries["forbidden_paths"])
    forbidden_ok = report_valid and _enum_map(
        observations.get("forbidden_paths"), _FORBIDDEN_PATH_KEYS, "DENIED"
    )
    writes_ok = report_valid and _enum_map(
        observations.get("writes"), ("root", "fixture"), "DENIED"
    )
    network_ok = report_valid and _enum_map(
        observations.get("network"), _NETWORK_KEYS, "DENIED"
    )
    runtime_ok = report_valid and _runtime_ok(observations.get("runtime"))
    inventory_report_ok = report_valid and _inventory_report_ok(
        observations.get("inventory"), inventory_ok, executable_paths
    )
    tools_ok = report_valid and _tools_ok(observations.get("tools"))
    protected_ok = (
        canaries["protected_state_before"] == canaries["protected_state_after"]
        and canaries["fixture_state_before"] == canaries["fixture_state_after"]
    )
    cleanup_ok = (
        cleanup_commands_complete
        and cleanup_state == {"containers": [], "networks": [], "volumes": []}
        and canaries["grant_present_before"] is True
        and canaries["grant_present_after"] is False
    )

    unavailable_status = "UNKNOWN" if not execution_complete else "FAIL"

    def assessed(ok: bool, available: bool = True) -> str:
        if not available:
            return unavailable_status
        return "PASS" if ok else "FAIL"

    results = (
        _result(
            "docker-mount-boundary",
            assessed(paths_ok and forbidden_ok, report_valid),
            "mounts_and_forbidden_paths_checked",
            {"host_mounts": paths_ok, "container_denials": forbidden_ok},
        ),
        _result(
            "docker-readonly-filesystem",
            assessed(host_verified and writes_ok, report_valid),
            "root_and_fixture_writes_checked",
            {"host_policy": host_verified, "container_denials": writes_ok},
        ),
        _result(
            "docker-network-boundary",
            assessed(host_verified and network_ok, report_valid),
            "internal_route_and_direct_targets_checked",
            {"host_policy": host_verified, "container_denials": network_ok},
        ),
        _result(
            "docker-gateway-credential-isolation",
            assessed(gateway_ok),
            "synthetic_gateway_scope_checked",
            {"gateway_contract": gateway_ok},
        ),
        _result(
            "docker-executable-inventory",
            assessed(host_verified and runtime_ok and inventory_report_ok, report_valid),
            "runtime_and_process_inventory_checked",
            {
                "host_policy": host_verified,
                "runtime": runtime_ok,
                "inventory": inventory_report_ok,
            },
        ),
        _result(
            "docker-tool-broker",
            assessed(tools_ok, report_valid),
            "bounded_file_tools_checked",
            {"tool_contract": tools_ok},
        ),
        _result(
            "docker-protected-state",
            assessed(protected_ok),
            "fixture_and_protected_state_checked",
            {"state_unchanged": protected_ok},
        ),
        _result(
            "docker-observer-completeness",
            assessed(host_verified and report_valid and execution_complete, execution_complete),
            "host_and_container_observations_checked",
            {
                "host_policy": host_verified,
                "report_complete": report_valid,
                "execution_complete": execution_complete,
            },
        ),
        _result(
            "docker-cleanup",
            assessed(cleanup_ok),
            "containers_networks_volumes_and_grant_checked",
            {"cleanup_complete": cleanup_ok},
        ),
    )
    if tuple(item.probe_id for item in results) != REQUIRED_DOCKER_PROBES:
        raise DockerProbeError("internal Docker probe set is incomplete")
    status = (
        "READY_NOT_RUN"
        if all(item.status == "PASS" for item in results)
        else "BLOCKED_NOT_RUN"
    )
    base_payload = {
        "schema_version": _SCHEMA_VERSION,
        "status": status,
        "model_executed": False,
        "plan_digest": topology.plan_digest,
        "runtime_digest": runtime_digest,
        "image_digest": image_digest,
        "topology_digest": topology.digest(),
        "probe_topology_digest": probe_topology.digest(),
        "gateway_policy_digest": gateway_policy_digest,
        "fixture_digest": fixture_digest,
        "observer_policy_digest": observer_policy_digest,
        "results": [item.canonical_payload() for item in results],
    }
    artifact_digest = _publish_exclusive(artifact_path, base_payload)
    return DockerPreflightResult(
        schema_version=_SCHEMA_VERSION,
        status=status,
        model_executed=False,
        plan_digest=topology.plan_digest,
        runtime_digest=runtime_digest,
        image_digest=image_digest,
        topology_digest=topology.digest(),
        probe_topology_digest=probe_topology.digest(),
        gateway_policy_digest=gateway_policy_digest,
        fixture_digest=fixture_digest,
        observer_policy_digest=observer_policy_digest,
        results=results,
        artifact_digest=artifact_digest,
        artifact_path=artifact_path,
    )
