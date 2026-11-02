"""Compile and verify one exact, fail-closed Docker v0.4 run topology."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, Mapping, Optional, Sequence, Tuple

from contracts import RunPlan
from docker_contracts import DockerExecutionBinding
from docker_runtime import DockerRuntimeIdentity, ImageLock
from provider_gateway import RunGrant


class DockerPolicyError(ValueError):
    """The requested or effective Docker topology differs from approval."""


_SCHEMA_VERSION = "0.4"
_ARMS = frozenset(("with-skill", "without-skill"))
_NONROOT_USER = "65532:65532"
_GATEWAY_ALIAS = "provider-gateway"
_GATEWAY_URL = "http://provider-gateway:8080/v1"
_WORKLOAD_BINDING_TARGET = "/run/evaluate/binding.json"
_GATEWAY_BINDING_TARGET = "/run/evaluate/gateway-binding.json"
_GATEWAY_REPLAY_TARGET = "/var/lib/evaluate-gateway/replay"
_WORKLOAD_ENTRYPOINT = (
    "/opt/evaluate/bin/python3",
    "/opt/evaluate/codex-entrypoint.py",
)
_GATEWAY_ENTRYPOINT = (
    "/opt/evaluate/bin/python3",
    "/opt/evaluate/gateway-entrypoint.py",
)
_DIGEST_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_RUN_ID_PATTERN = re.compile(r"[^a-z0-9]+")
_MAX_RUN_ID_LENGTH = 24


def _canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_digest(path: Path) -> str:
    hasher = hashlib.sha256()
    try:
        with path.open("rb") as source:
            while True:
                chunk = source.read(1024 * 1024)
                if not chunk:
                    return hasher.hexdigest()
                hasher.update(chunk)
    except OSError as exc:
        raise DockerPolicyError(f"cannot hash policy file {path}: {exc}") from None


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise DockerPolicyError(f"{name} must be an object")
    return value


def _root(value: Path, name: str) -> Path:
    path = Path(value)
    if not path.is_absolute() or path.is_symlink() or not path.is_dir():
        raise DockerPolicyError(f"{name} must be a real absolute directory")
    resolved = path.resolve()
    home = Path.home().resolve()
    if resolved in (Path("/").resolve(), home) or len(resolved.parts) < 4:
        raise DockerPolicyError(f"{name} is too broad")
    if (path / ".git").exists():
        raise DockerPolicyError(f"{name} must not be a repository root")
    for parent in (path, *path.parents):
        if (parent / ".git").exists():
            raise DockerPolicyError(f"{name} must be outside every source repository")
    return path


def _safe_path(
    value: Path,
    root: Path,
    name: str,
    *,
    directory: bool,
) -> Path:
    path = Path(value)
    if not path.is_absolute():
        raise DockerPolicyError(f"{name} must be absolute")
    try:
        relative = path.relative_to(root)
    except ValueError:
        raise DockerPolicyError(f"{name} is outside its approved root") from None
    if relative == Path("."):
        raise DockerPolicyError(f"{name} cannot expose an entire approved root")
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise DockerPolicyError(f"{name} contains a symlink")
    if directory:
        if not path.is_dir():
            raise DockerPolicyError(f"{name} must be a directory")
    elif not path.is_file():
        raise DockerPolicyError(f"{name} must be a regular file")
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        raise DockerPolicyError(f"{name} resolves outside its approved root") from None
    return path


def _run_token(value: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise DockerPolicyError("run_id must be a non-empty canonical string")
    token = _RUN_ID_PATTERN.sub("-", value.lower()).strip("-")
    token = token[:_MAX_RUN_ID_LENGTH].rstrip("-")
    if not token:
        raise DockerPolicyError("run_id contains no safe name characters")
    return token


def _labels(plan_digest: str, run_id: str, role: str) -> Mapping[str, str]:
    return MappingProxyType(
        {
            "evaluate.plan": plan_digest,
            "evaluate.run": run_id,
            "evaluate.role": role,
            "evaluate.schema": _SCHEMA_VERSION,
        }
    )


@dataclass(frozen=True)
class DockerMount:
    kind: str
    source: str
    target: str
    read_only: bool
    propagation: str = "rprivate"

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "source": self.source,
            "target": self.target,
            "read_only": self.read_only,
            "propagation": self.propagation,
        }


@dataclass(frozen=True)
class DockerNetworkPolicy:
    name: str
    internal: bool
    ipv6: bool
    driver: str
    attachable: bool
    labels: Mapping[str, str]

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "internal": self.internal,
            "ipv6": self.ipv6,
            "driver": self.driver,
            "attachable": self.attachable,
            "labels": dict(self.labels),
        }


@dataclass(frozen=True)
class DockerContainerPolicy:
    role: str
    name: str
    image: str
    user: str
    read_only_root: bool
    cap_drop: Tuple[str, ...]
    security_options: Tuple[str, ...]
    networks: Tuple[str, ...]
    mounts: Tuple[DockerMount, ...]
    tmpfs: Mapping[str, str]
    environment: Tuple[str, ...]
    entrypoint: Tuple[str, ...]
    command: Tuple[str, ...]
    cpus: float
    memory_bytes: int
    pids_limit: int
    labels: Mapping[str, str]

    def security_payload(self) -> dict[str, Any]:
        """Return arm-invariant hardening controls for equivalence checks."""

        return {
            "user": self.user,
            "read_only_root": self.read_only_root,
            "cap_drop": list(self.cap_drop),
            "security_options": list(self.security_options),
            "tmpfs": dict(self.tmpfs),
            "entrypoint": list(self.entrypoint),
            "command": list(self.command),
            "cpus": self.cpus,
            "memory_bytes": self.memory_bytes,
            "pids_limit": self.pids_limit,
        }

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "name": self.name,
            "image": self.image,
            **self.security_payload(),
            "networks": list(self.networks),
            "mounts": [mount.canonical_payload() for mount in self.mounts],
            "environment": list(self.environment),
            "labels": dict(self.labels),
        }


@dataclass(frozen=True)
class DockerCommand:
    action: str
    role: str
    argv: Tuple[str, ...]

    def canonical_payload(self) -> dict[str, Any]:
        return {"action": self.action, "role": self.role, "argv": list(self.argv)}


@dataclass(frozen=True)
class DockerRunTopology:
    schema_version: str
    plan_digest: str
    run_id: str
    arm: str
    internal_network: DockerNetworkPolicy
    egress_network: DockerNetworkPolicy
    workload: DockerContainerPolicy
    gateway: DockerContainerPolicy
    resource_limits: Mapping[str, float]
    timeout_seconds: int
    max_output_bytes: int
    commands: Tuple[DockerCommand, ...]

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "plan_digest": self.plan_digest,
            "run_id": self.run_id,
            "arm": self.arm,
            "internal_network": self.internal_network.canonical_payload(),
            "egress_network": self.egress_network.canonical_payload(),
            "workload": self.workload.canonical_payload(),
            "gateway": self.gateway.canonical_payload(),
            "resource_limits": dict(self.resource_limits),
            "timeout_seconds": self.timeout_seconds,
            "max_output_bytes": self.max_output_bytes,
            "commands": [command.canonical_payload() for command in self.commands],
        }

    def digest(self) -> str:
        return _canonical_digest(self.canonical_payload())


def _mount(source: Path, target: str, *, read_only: bool) -> DockerMount:
    return DockerMount(
        kind="bind",
        source=str(source),
        target=target,
        read_only=read_only,
    )


def _mount_arg(mount: DockerMount) -> str:
    values = (
        f"type={mount.kind}",
        f"src={mount.source}",
        f"dst={mount.target}",
        "readonly" if mount.read_only else "rw",
        f"bind-propagation={mount.propagation}",
    )
    return ",".join(values)


def _network_command(
    docker: str, network: DockerNetworkPolicy, action: str
) -> DockerCommand:
    argv = [docker, "network", "create", "--driver", "bridge"]
    if network.internal:
        argv.append("--internal")
    argv.append("--ipv6=false")
    for key, value in sorted(network.labels.items()):
        argv.extend(("--label", f"{key}={value}"))
    argv.append(network.name)
    return DockerCommand(action=action, role="network", argv=tuple(argv))


def _create_command(docker: str, container: DockerContainerPolicy) -> DockerCommand:
    argv = [
        docker,
        "create",
        "--name",
        container.name,
        "--read-only",
        "--user",
        container.user,
        "--cap-drop",
        "ALL",
    ]
    for option in container.security_options:
        argv.extend(("--security-opt", option))
    argv.extend(("--network", container.networks[0]))
    if container.role == "gateway":
        argv.extend(("--network-alias", _GATEWAY_ALIAS))
    argv.extend(("--cpus", str(container.cpus)))
    argv.extend(("--memory", str(container.memory_bytes)))
    argv.extend(("--pids-limit", str(container.pids_limit)))
    for mount in container.mounts:
        argv.extend(("--mount", _mount_arg(mount)))
    for target, options in sorted(container.tmpfs.items()):
        argv.extend(("--tmpfs", f"{target}:{options}"))
    for environment in container.environment:
        argv.extend(("--env", environment))
    for key, value in sorted(container.labels.items()):
        argv.extend(("--label", f"{key}={value}"))
    argv.append(container.image)
    argv.extend(container.command)
    return DockerCommand(action="create", role=container.role, argv=tuple(argv))


def _lifecycle_command(
    docker: str, action: str, role: str, *arguments: str
) -> DockerCommand:
    return DockerCommand(action=action, role=role, argv=(docker, action, *arguments))


def _validate_contracts(
    plan: RunPlan,
    binding: DockerExecutionBinding,
    runtime: DockerRuntimeIdentity,
    image_lock: ImageLock,
    arm: str,
    run_grant: RunGrant,
    seccomp_profile: Path,
) -> None:
    if not isinstance(plan, RunPlan) or plan.schema_version != _SCHEMA_VERSION:
        raise DockerPolicyError("an approved v0.4 RunPlan is required")
    if plan.backend != "docker" or plan.capabilities.profile != "read-only":
        raise DockerPolicyError("only the Docker read-only profile is supported")
    if plan.capabilities.shell:
        raise DockerPolicyError("the initial Docker profile is shell-free")
    if arm not in _ARMS or arm not in plan.comparison_arms:
        raise DockerPolicyError("arm is outside the approved comparison")
    if not isinstance(binding, DockerExecutionBinding):
        raise DockerPolicyError("DockerExecutionBinding is required")
    if (
        binding.plan_digest != plan.digest()
        or binding.provider != plan.provider
        or binding.profile != plan.capabilities.profile
    ):
        raise DockerPolicyError("execution binding differs from the approved plan")
    if not isinstance(runtime, DockerRuntimeIdentity):
        raise DockerPolicyError("DockerRuntimeIdentity is required")
    if not Path(runtime.executable_path).is_absolute() or not _DIGEST_PATTERN.fullmatch(
        runtime.executable_digest
    ):
        raise DockerPolicyError("Docker executable identity is malformed")
    if not isinstance(image_lock, ImageLock):
        raise DockerPolicyError("verified ImageLock is required")
    if (
        image_lock.final_image != binding.workload_image
        or image_lock.target_platform != runtime.platform
        or image_lock.profile != binding.profile
    ):
        raise DockerPolicyError("runtime, image lock, and execution binding differ")
    if (
        image_lock.build_inputs["seccomp_profile"]
        != binding.seccomp_policy_digest
        or image_lock.build_inputs["executable_inventory"]
        != binding.runtime_inventory_digest
    ):
        raise DockerPolicyError("reviewed image policies differ from execution binding")
    if _file_digest(seccomp_profile) != binding.seccomp_policy_digest:
        raise DockerPolicyError("seccomp policy content differs from its binding")
    if not isinstance(run_grant, RunGrant):
        raise DockerPolicyError("signed RunGrant is required")
    if (
        run_grant.plan_digest != plan.digest()
        or run_grant.provider != plan.provider
        or run_grant.model != plan.model
        or run_grant.model_version != plan.model_version
        or run_grant.role != arm
    ):
        raise DockerPolicyError("run grant scope differs from the approved arm")


def compile_docker_topology(
    plan: RunPlan,
    binding: DockerExecutionBinding,
    runtime: DockerRuntimeIdentity,
    image_lock: ImageLock,
    *,
    arm: str,
    prepared_bundle_root: Path,
    host_artifact_root: Path,
    fixture: Path,
    skill_snapshot: Optional[Path],
    workload_binding: Path,
    gateway_binding: Path,
    gateway_replay: Path,
    seccomp_profile: Path,
    run_grant: RunGrant,
    run_id: str,
) -> DockerRunTopology:
    """Compile immutable argv and expected post-create state without running Docker."""

    bundle_root = _root(prepared_bundle_root, "prepared bundle root")
    artifact_root = _root(host_artifact_root, "host artifact root")
    bundle_resolved = bundle_root.resolve()
    artifact_resolved = artifact_root.resolve()
    if (
        bundle_resolved == artifact_resolved
        or bundle_resolved in artifact_resolved.parents
        or artifact_resolved in bundle_resolved.parents
    ):
        raise DockerPolicyError("prepared bundle and host artifact roots overlap")

    fixture_path = _safe_path(fixture, bundle_root, "fixture", directory=True)
    workload_binding_path = _safe_path(
        workload_binding, artifact_root, "workload binding", directory=False
    )
    gateway_binding_path = _safe_path(
        gateway_binding, artifact_root, "gateway binding", directory=False
    )
    gateway_replay_path = _safe_path(
        gateway_replay, artifact_root, "gateway replay ledger", directory=True
    )
    seccomp_path = _safe_path(
        seccomp_profile, artifact_root, "seccomp profile", directory=False
    )
    if arm == "with-skill":
        if skill_snapshot is None:
            raise DockerPolicyError("with-skill arm requires the approved skill snapshot")
        skill_path = _safe_path(
            skill_snapshot, bundle_root, "skill snapshot", directory=True
        )
    else:
        if skill_snapshot is not None:
            raise DockerPolicyError("without-skill arm forbids a skill snapshot")
        skill_path = None

    _validate_contracts(
        plan,
        binding,
        runtime,
        image_lock,
        arm,
        run_grant,
        seccomp_path,
    )

    limits = plan.resource_limits
    required_limits = frozenset(
        (
            "max_seconds",
            "max_turns",
            "max_output_bytes",
            "max_cost_usd",
            "max_cpus",
            "max_memory_bytes",
            "max_pids",
            "max_tmpfs_bytes",
        )
    )
    if frozenset(limits) != required_limits:
        raise DockerPolicyError("Docker resource limits are incomplete")
    token = _run_token(run_id)
    prefix = f"eval-{plan.digest()[:12]}-{token}"
    internal = DockerNetworkPolicy(
        name=f"{prefix}-internal",
        internal=True,
        ipv6=False,
        driver="bridge",
        attachable=False,
        labels=_labels(plan.digest(), token, "internal-network"),
    )
    egress = DockerNetworkPolicy(
        name=f"{prefix}-gateway-egress",
        internal=False,
        ipv6=False,
        driver="bridge",
        attachable=False,
        labels=_labels(plan.digest(), token, "gateway-egress-network"),
    )
    tmpfs = MappingProxyType(
        {
            "/tmp": (
                "rw,noexec,nosuid,nodev,size="
                + str(int(limits["max_tmpfs_bytes"]))
            )
        }
    )
    security_options = (
        "no-new-privileges:true",
        "seccomp=" + str(seccomp_path),
    )
    workload_mounts = [
        _mount(fixture_path, "/fixture", read_only=True),
        _mount(
            workload_binding_path,
            _WORKLOAD_BINDING_TARGET,
            read_only=True,
        ),
    ]
    if skill_path is not None:
        workload_mounts.insert(1, _mount(skill_path, "/skill", read_only=True))
    workload = DockerContainerPolicy(
        role="workload",
        name=f"{prefix}-work-{arm}",
        image=binding.workload_image,
        user=_NONROOT_USER,
        read_only_root=True,
        cap_drop=("ALL",),
        security_options=security_options,
        networks=(internal.name,),
        mounts=tuple(workload_mounts),
        tmpfs=tmpfs,
        environment=(
            "EVALUATE_GATEWAY_BASE_URL=" + _GATEWAY_URL,
            "EVALUATE_RUN_GRANT=" + run_grant.to_token(),
        ),
        entrypoint=_WORKLOAD_ENTRYPOINT,
        command=("evaluate", "--binding", _WORKLOAD_BINDING_TARGET),
        cpus=float(limits["max_cpus"]),
        memory_bytes=int(limits["max_memory_bytes"]),
        pids_limit=int(limits["max_pids"]),
        labels=_labels(plan.digest(), token, "workload-" + arm),
    )
    gateway = DockerContainerPolicy(
        role="gateway",
        name=f"{prefix}-gateway",
        image=binding.gateway_image,
        user=_NONROOT_USER,
        read_only_root=True,
        cap_drop=("ALL",),
        security_options=security_options,
        networks=(internal.name, egress.name),
        mounts=(
            _mount(
                gateway_binding_path,
                _GATEWAY_BINDING_TARGET,
                read_only=True,
            ),
            _mount(
                gateway_replay_path,
                _GATEWAY_REPLAY_TARGET,
                read_only=False,
            ),
        ),
        tmpfs=tmpfs,
        environment=(),
        entrypoint=_GATEWAY_ENTRYPOINT,
        command=(
            "serve",
            "--binding",
            _GATEWAY_BINDING_TARGET,
            "--replay-ledger",
            _GATEWAY_REPLAY_TARGET,
        ),
        cpus=float(limits["max_cpus"]),
        memory_bytes=int(limits["max_memory_bytes"]),
        pids_limit=int(limits["max_pids"]),
        labels=_labels(plan.digest(), token, "gateway"),
    )

    docker = runtime.executable_path
    commands = [
        _network_command(docker, internal, "create-internal-network"),
        _network_command(docker, egress, "create-egress-network"),
        _create_command(docker, gateway),
        DockerCommand(
            action="connect-egress-network",
            role="gateway",
            argv=(docker, "network", "connect", egress.name, gateway.name),
        ),
        DockerCommand(
            action="inspect-networks",
            role="network",
            argv=(docker, "network", "inspect", internal.name, egress.name),
        ),
        _lifecycle_command(docker, "inspect", "gateway", gateway.name),
        _create_command(docker, workload),
        _lifecycle_command(docker, "inspect", "workload", workload.name),
        _lifecycle_command(docker, "start", "gateway", gateway.name),
        _lifecycle_command(docker, "start", "workload", workload.name),
        _lifecycle_command(docker, "inspect", "workload", workload.name),
        _lifecycle_command(docker, "stop", "workload", "--time", "10", workload.name),
        _lifecycle_command(docker, "stop", "gateway", "--time", "10", gateway.name),
        _lifecycle_command(docker, "rm", "workload", "--force", workload.name),
        _lifecycle_command(docker, "rm", "gateway", "--force", gateway.name),
        DockerCommand(
            action="remove-networks",
            role="network",
            argv=(docker, "network", "rm", internal.name, egress.name),
        ),
    ]
    return DockerRunTopology(
        schema_version=_SCHEMA_VERSION,
        plan_digest=plan.digest(),
        run_id=token,
        arm=arm,
        internal_network=internal,
        egress_network=egress,
        workload=workload,
        gateway=gateway,
        resource_limits=MappingProxyType(dict(limits)),
        timeout_seconds=int(limits["max_seconds"]),
        max_output_bytes=int(limits["max_output_bytes"]),
        commands=tuple(commands),
    )


def _sequence(value: Any, name: str) -> Sequence[Any]:
    if not isinstance(value, (list, tuple)):
        raise DockerPolicyError(f"{name} must be an array")
    return value


def verify_effective_container(
    inspect_payload: Mapping[str, Any],
    topology: DockerRunTopology,
    role: str,
) -> None:
    """Reject any post-create container state that differs from the compiler."""

    if not isinstance(topology, DockerRunTopology):
        raise DockerPolicyError("DockerRunTopology is required")
    if role == "workload":
        expected = topology.workload
    elif role == "gateway":
        expected = topology.gateway
    else:
        raise DockerPolicyError("container role is unsupported")
    payload = _mapping(inspect_payload, "container inspect")
    config = _mapping(payload.get("Config"), "container inspect.Config")
    host = _mapping(payload.get("HostConfig"), "container inspect.HostConfig")
    network_settings = _mapping(
        payload.get("NetworkSettings"), "container inspect.NetworkSettings"
    )
    networks = _mapping(
        network_settings.get("Networks"), "container inspect networks"
    )
    expected_config = {
        "Image": expected.image,
        "User": expected.user,
        "Env": list(expected.environment),
        "Entrypoint": list(expected.entrypoint),
        "Cmd": list(expected.command),
        "Labels": dict(expected.labels),
    }
    for field, value in expected_config.items():
        if config.get(field) != value:
            raise DockerPolicyError(f"effective container {field} drifted")
    if payload.get("Name") != "/" + expected.name:
        raise DockerPolicyError("effective container name drifted")
    expected_host = {
        "ReadonlyRootfs": expected.read_only_root,
        "Privileged": False,
        "CapDrop": list(expected.cap_drop),
        "SecurityOpt": list(expected.security_options),
        "NetworkMode": expected.networks[0],
        "PidMode": "",
        "IpcMode": "",
        "UTSMode": "",
        "UsernsMode": "",
        "NanoCpus": int(expected.cpus * 1_000_000_000),
        "Memory": expected.memory_bytes,
        "PidsLimit": expected.pids_limit,
        "Tmpfs": dict(expected.tmpfs),
    }
    for field, value in expected_host.items():
        if host.get(field) != value:
            raise DockerPolicyError(f"effective container HostConfig.{field} drifted")
    effective_mounts = _sequence(payload.get("Mounts"), "container inspect.Mounts")
    expected_mounts = [
        {
            "Type": mount.kind,
            "Source": mount.source,
            "Destination": mount.target,
            "RW": not mount.read_only,
            "Propagation": mount.propagation,
        }
        for mount in expected.mounts
    ]
    if list(effective_mounts) != expected_mounts:
        raise DockerPolicyError("effective container mounts drifted")
    if len(networks) != len(expected.networks) or frozenset(networks) != frozenset(
        expected.networks
    ):
        raise DockerPolicyError("effective container networks drifted")


def verify_effective_network(
    inspect_payload: Sequence[Mapping[str, Any]], topology: DockerRunTopology
) -> None:
    """Reject reused, relabeled, externally routed, or IPv6-enabled networks."""

    if not isinstance(topology, DockerRunTopology):
        raise DockerPolicyError("DockerRunTopology is required")
    payloads = _sequence(inspect_payload, "network inspect")
    if len(payloads) != 2:
        raise DockerPolicyError("network inspect must return exactly two networks")
    by_name: dict[str, Mapping[str, Any]] = {}
    for item in payloads:
        network = _mapping(item, "network inspect item")
        name = network.get("Name")
        if not isinstance(name, str) or name in by_name:
            raise DockerPolicyError("network inspect names are invalid or duplicate")
        by_name[name] = network
    for expected in (topology.internal_network, topology.egress_network):
        actual = by_name.get(expected.name)
        if actual is None:
            raise DockerPolicyError("expected network is absent")
        if (
            actual.get("Internal") is not expected.internal
            or actual.get("EnableIPv6") is not expected.ipv6
            or actual.get("Driver") != expected.driver
            or actual.get("Attachable") is not expected.attachable
            or actual.get("Labels") != dict(expected.labels)
        ):
            raise DockerPolicyError("effective network policy drifted")
    if frozenset(by_name) != frozenset(
        (topology.internal_network.name, topology.egress_network.name)
    ):
        raise DockerPolicyError("unapproved network is present")
