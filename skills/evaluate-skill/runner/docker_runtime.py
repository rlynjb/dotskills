"""Fail-closed Docker runtime identity and immutable image-lock validation."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, Callable, Mapping, Sequence


class DockerRuntimeError(ValueError):
    """Docker identity or reviewed image provenance is incomplete or drifted."""


_SCHEMA_VERSION = "0.4"
_IMAGE_PATTERN = re.compile(
    r"^[a-z0-9][a-z0-9._/-]*@sha256:([0-9a-f]{64})$"
)
_DIGEST_PATTERN = re.compile(r"^[0-9a-f]{64}$")
_BUILD_INPUTS = frozenset(
    (
        "dockerfile",
        "provider_lockfiles",
        "entrypoint",
        "seccomp_profile",
        "executable_inventory",
    )
)
_PROVIDER_ARTIFACTS = frozenset(
    ("codex", "promptfoo", "codex_sdk", "node", "python")
)
_PROFILES = frozenset(("read-only",))
_TARGET_PLATFORMS = frozenset(("linux/arm64",))
_MAX_COMMAND_OUTPUT = 1024 * 1024


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise DockerRuntimeError(f"{name} must be an object")
    if not all(isinstance(key, str) for key in value):
        raise DockerRuntimeError(f"{name} field names must be strings")
    return value


def _exact_fields(value: Mapping[str, Any], expected: frozenset[str], name: str) -> None:
    actual = frozenset(value)
    missing = sorted(expected - actual)
    unknown = sorted(actual - expected)
    if missing:
        raise DockerRuntimeError(f"{name} missing fields: {', '.join(missing)}")
    if unknown:
        raise DockerRuntimeError(f"{name} unknown fields: {', '.join(unknown)}")


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise DockerRuntimeError(f"{name} must be a non-empty canonical string")
    return value


def _digest(value: Any, name: str) -> str:
    digest = _text(value, name)
    if not _DIGEST_PATTERN.fullmatch(digest) or digest == "0" * 64:
        raise DockerRuntimeError(f"{name} must be a non-placeholder SHA-256 digest")
    return digest


def _image(value: Any, name: str) -> tuple[str, str]:
    reference = _text(value, name)
    match = _IMAGE_PATTERN.fullmatch(reference)
    if match is None:
        raise DockerRuntimeError(
            f"{name} must be an immutable name@sha256:<digest> reference"
        )
    digest = _digest(match.group(1), f"{name} digest")
    return reference, digest


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
        raise DockerRuntimeError(f"cannot hash Docker executable: {exc}") from None


def _run_json(
    runner: Callable[[list[str]], Any], argv: list[str], name: str
) -> Mapping[str, Any]:
    try:
        result = runner(argv)
    except Exception as exc:
        raise DockerRuntimeError(f"{name} inspection failed: {exc}") from None
    if getattr(result, "returncode", None) != 0:
        raise DockerRuntimeError(f"{name} inspection returned nonzero status")
    stdout = getattr(result, "stdout", None)
    if not isinstance(stdout, str) or not stdout or len(stdout) > _MAX_COMMAND_OUTPUT:
        raise DockerRuntimeError(f"{name} inspection output is missing or oversized")
    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        raise DockerRuntimeError(f"{name} inspection output is not valid JSON") from None
    return _mapping(payload, f"{name} inspection output")


@dataclass(frozen=True)
class DockerRuntimeIdentity:
    client_version: str
    server_version: str
    context: str
    endpoint: str
    platform: str
    daemon_name: str
    executable_path: str
    executable_digest: str


def inspect_docker_runtime(
    docker_path: Path,
    *,
    expected_context: str,
    expected_endpoint: str,
    expected_platform: str,
    runner: Callable[[list[str]], Any],
) -> DockerRuntimeIdentity:
    """Inspect an already-running local daemon without starting or changing it."""

    path = Path(docker_path)
    if not path.is_absolute():
        raise DockerRuntimeError("Docker executable path must be absolute")
    if path.is_symlink() or not path.is_file() or not os.access(path, os.X_OK):
        raise DockerRuntimeError(
            "Docker executable must be an executable regular file, not a symlink"
        )
    expected_context = _text(expected_context, "expected Docker context")
    expected_endpoint = _text(expected_endpoint, "expected Docker endpoint")
    expected_platform = _text(expected_platform, "expected Docker platform")
    if not expected_endpoint.startswith("unix:///"):
        raise DockerRuntimeError("Docker endpoint must be one explicit local Unix socket")
    if expected_platform not in _TARGET_PLATFORMS:
        raise DockerRuntimeError(f"Docker platform is unsupported: {expected_platform}")

    executable_path = str(path)
    executable_digest = _file_digest(path)
    version = _run_json(
        runner,
        [executable_path, "version", "--format", "{{json .}}"],
        "Docker version",
    )
    context = _run_json(
        runner,
        [
            executable_path,
            "context",
            "inspect",
            expected_context,
            "--format",
            "{{json .}}",
        ],
        "Docker context",
    )
    info = _run_json(
        runner,
        [executable_path, "info", "--format", "{{json .}}"],
        "Docker info",
    )
    if _file_digest(path) != executable_digest:
        raise DockerRuntimeError("Docker executable identity changed during inspection")

    client = _mapping(version.get("Client"), "Docker version.Client")
    server = _mapping(version.get("Server"), "Docker version.Server")
    client_version = _text(client.get("Version"), "Docker client version")
    server_version = _text(server.get("Version"), "Docker server version")

    context_name = _text(context.get("Name"), "Docker context name")
    endpoints = _mapping(context.get("Endpoints"), "Docker context.Endpoints")
    docker_endpoint = _mapping(endpoints.get("docker"), "Docker context docker endpoint")
    endpoint = _text(docker_endpoint.get("Host"), "Docker context endpoint host")
    if context_name != expected_context:
        raise DockerRuntimeError("Docker context differs from the approved context")
    if endpoint != expected_endpoint or not endpoint.startswith("unix:///"):
        raise DockerRuntimeError("Docker endpoint differs or is not local")

    os_type = _text(info.get("OSType"), "Docker server OS type")
    architecture = _text(info.get("Architecture"), "Docker server architecture")
    platform = f"{os_type}/{architecture}"
    if platform != expected_platform:
        raise DockerRuntimeError("Docker server platform differs from the approved platform")
    daemon_name = _text(info.get("Name"), "Docker daemon name")

    return DockerRuntimeIdentity(
        client_version=client_version,
        server_version=server_version,
        context=context_name,
        endpoint=endpoint,
        platform=platform,
        daemon_name=daemon_name,
        executable_path=executable_path,
        executable_digest=executable_digest,
    )


@dataclass(frozen=True)
class ImageLock:
    schema_version: str
    status: str
    provider: str
    profile: str
    base_image: str
    final_image: str
    target_platform: str
    provider_artifacts: Mapping[str, str]
    build_inputs: Mapping[str, str]

    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ImageLock":
        value = _mapping(value, "image lock")
        _exact_fields(
            value,
            frozenset(
                (
                    "schema_version",
                    "status",
                    "provider",
                    "profile",
                    "base_image",
                    "final_image",
                    "target_platform",
                    "provider_artifacts",
                    "build_inputs",
                )
            ),
            "image lock",
        )
        schema_version = _text(value["schema_version"], "image lock.schema_version")
        if schema_version != _SCHEMA_VERSION:
            raise DockerRuntimeError(f"unsupported image lock schema: {schema_version}")
        status = _text(value["status"], "image lock.status")
        if status != "verified":
            raise DockerRuntimeError("image lock is not verified from an observed build")
        profile = _text(value["profile"], "image lock.profile")
        if profile not in _PROFILES:
            raise DockerRuntimeError(f"unsupported image lock profile: {profile}")
        target_platform = _text(
            value["target_platform"], "image lock.target_platform"
        )
        if target_platform not in _TARGET_PLATFORMS:
            raise DockerRuntimeError(
                f"unsupported image lock target platform: {target_platform}"
            )
        base_image, _ = _image(value["base_image"], "image lock.base_image")
        final_image, _ = _image(value["final_image"], "image lock.final_image")
        build_inputs = _mapping(value["build_inputs"], "image lock.build_inputs")
        _exact_fields(build_inputs, _BUILD_INPUTS, "image lock.build_inputs")
        normalized_inputs = {
            name: _digest(build_inputs[name], f"image lock.build_inputs.{name}")
            for name in sorted(_BUILD_INPUTS)
        }
        artifacts = _mapping(
            value["provider_artifacts"], "image lock.provider_artifacts"
        )
        _exact_fields(artifacts, _PROVIDER_ARTIFACTS, "image lock.provider_artifacts")
        normalized_artifacts = {
            name: _text(
                artifacts[name], f"image lock.provider_artifacts.{name}"
            )
            for name in sorted(_PROVIDER_ARTIFACTS)
        }
        return cls(
            schema_version=schema_version,
            status=status,
            provider=_text(value["provider"], "image lock.provider"),
            profile=profile,
            base_image=base_image,
            final_image=final_image,
            target_platform=target_platform,
            provider_artifacts=MappingProxyType(normalized_artifacts),
            build_inputs=MappingProxyType(normalized_inputs),
        )


def load_image_lock(path: Path) -> ImageLock:
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DockerRuntimeError(f"cannot load image lock: {exc}") from None
    return ImageLock.from_dict(_mapping(document, "image lock"))


def verify_image_inspect(lock: ImageLock, payload: Sequence[Any]) -> None:
    if not isinstance(lock, ImageLock):
        raise DockerRuntimeError("reviewed ImageLock is required")
    if not isinstance(payload, list) or len(payload) != 1:
        raise DockerRuntimeError("Docker image inspect must contain exactly one image")
    image = _mapping(payload[0], "Docker image inspect item")
    repo_digests = image.get("RepoDigests")
    if not isinstance(repo_digests, list) or tuple(repo_digests) != (lock.final_image,):
        raise DockerRuntimeError("inspected image digest differs from reviewed lock")
    platform = f"{_text(image.get('Os'), 'image OS')}/{_text(image.get('Architecture'), 'image architecture')}"
    if platform != lock.target_platform:
        raise DockerRuntimeError("inspected image platform differs from reviewed lock")


_IMAGE_CONTRACT_FILES = {
    "dockerfile": "codex-read-only.Dockerfile",
    "entrypoint": "codex-entrypoint.py",
    "seccomp_profile": "seccomp-codex-read-only.json",
    "executable_inventory": "executable-inventory-codex.json",
}
_IMAGE_LOCK_FIELDS = frozenset(
    (
        "schema_version",
        "status",
        "provider",
        "profile",
        "base_image",
        "final_image",
        "target_platform",
        "provider_artifacts",
        "build_inputs",
    )
)
_APPROVED_EXECUTABLES = frozenset(
    (
        "/opt/evaluate/bin/python3",
        "/opt/evaluate/bin/node",
        "/opt/evaluate/bin/codex",
        "/opt/evaluate/bin/promptfoo",
    )
)
_FORBIDDEN_SYSCALLS = frozenset(
    (
        "mount",
        "umount2",
        "unshare",
        "setns",
        "clone3",
        "ptrace",
        "bpf",
        "perf_event_open",
        "kexec_load",
        "init_module",
        "finit_module",
    )
)


def _contract_file(root: Path, filename: str) -> Path:
    root = Path(root)
    path = root / filename
    if root.is_symlink() or path.is_symlink() or not path.is_file():
        raise DockerRuntimeError(f"image contract file is missing or unsafe: {filename}")
    if path.parent.resolve() != root.resolve():
        raise DockerRuntimeError(f"image contract file escapes its root: {filename}")
    return path


def _canonical_json_digest(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def image_contract_build_inputs(
    root: Path, lock: Mapping[str, Any]
) -> Mapping[str, str]:
    lock = _mapping(lock, "image contract lock")
    artifacts = _mapping(
        lock.get("provider_artifacts"), "image contract provider_artifacts"
    )
    _exact_fields(
        artifacts, _PROVIDER_ARTIFACTS, "image contract provider_artifacts"
    )
    inputs = {
        name: _file_digest(_contract_file(Path(root), filename))
        for name, filename in _IMAGE_CONTRACT_FILES.items()
    }
    inputs["provider_lockfiles"] = _canonical_json_digest(
        {name: _text(artifacts[name], f"provider artifact {name}") for name in sorted(artifacts)}
    )
    return MappingProxyType(dict(sorted(inputs.items())))


def image_contract_digest(root: Path, lock: Mapping[str, Any]) -> str:
    lock = _mapping(lock, "image contract lock")
    payload = {
        key: lock.get(key)
        for key in (
            "schema_version",
            "status",
            "provider",
            "profile",
            "base_image",
            "final_image",
            "target_platform",
            "provider_artifacts",
        )
    }
    payload["build_inputs"] = dict(image_contract_build_inputs(root, lock))
    return _canonical_json_digest(payload)


def validate_image_contract(root: Path, lock: Mapping[str, Any]) -> None:
    """Validate the offline image definition without building or running it."""

    root = Path(root)
    if not root.is_absolute():
        root = root.resolve()
    if root.is_symlink() or not root.is_dir():
        raise DockerRuntimeError("image contract root must be a regular directory")
    lock = _mapping(lock, "image contract lock")
    _exact_fields(lock, _IMAGE_LOCK_FIELDS, "image contract lock")
    if lock["schema_version"] != _SCHEMA_VERSION:
        raise DockerRuntimeError("image contract schema is unsupported")
    if lock["provider"] != "codex" or lock["profile"] != "read-only":
        raise DockerRuntimeError("image contract provider/profile is unsupported")
    if lock["target_platform"] != "linux/arm64":
        raise DockerRuntimeError("image contract platform is unsupported")
    status = lock["status"]
    if status == "unverified":
        if lock["base_image"] is not None or lock["final_image"] is not None:
            raise DockerRuntimeError("unverified image contract cannot claim image digests")
    elif status == "verified":
        ImageLock.from_dict(lock)
    else:
        raise DockerRuntimeError("image contract status is unsupported")

    declared_inputs = _mapping(lock["build_inputs"], "image contract build_inputs")
    _exact_fields(declared_inputs, _BUILD_INPUTS, "image contract build_inputs")
    computed_inputs = image_contract_build_inputs(root, lock)
    for name in sorted(_BUILD_INPUTS):
        declared = _digest(declared_inputs[name], f"image contract build_inputs.{name}")
        if declared != computed_inputs[name]:
            raise DockerRuntimeError(f"image contract build input drift: {name}")

    dockerfile = _contract_file(root, "codex-read-only.Dockerfile").read_text(
        encoding="utf-8"
    )
    required_lines = (
        "ARG RUNTIME_IMAGE",
        "FROM ${RUNTIME_IMAGE} AS reviewed-runtime",
        "FROM scratch AS workload",
        "USER 65532:65532",
        "WORKDIR /workspace",
        'ENTRYPOINT ["/opt/evaluate/bin/python3", "/opt/evaluate/codex-entrypoint.py"]',
    )
    if any(line not in dockerfile for line in required_lines):
        raise DockerRuntimeError("Dockerfile is missing a fixed hardened directive")
    forbidden_fragments = (
        "curl ",
        "wget ",
        "npm install",
        "pip install",
        "apt-get",
        " apk ",
        " yum ",
        " dnf ",
        " brew ",
        "| sh",
    )
    lowered = dockerfile.lower()
    if any(fragment in lowered for fragment in forbidden_fragments):
        raise DockerRuntimeError("Dockerfile contains a remote fetch or package install")
    if any(line.lstrip().upper().startswith("RUN ") for line in dockerfile.splitlines()):
        raise DockerRuntimeError("Dockerfile runtime commands are forbidden")

    inventory = json.loads(
        _contract_file(root, "executable-inventory-codex.json").read_text(
            encoding="utf-8"
        )
    )
    inventory = _mapping(inventory, "executable inventory")
    _exact_fields(
        inventory,
        frozenset(
            (
                "schema_version",
                "status",
                "target_platform",
                "allowed_tools",
                "executables",
                "scripts",
            )
        ),
        "executable inventory",
    )
    if inventory["status"] != status or inventory["target_platform"] != "linux/arm64":
        raise DockerRuntimeError("executable inventory status/platform mismatch")
    if inventory["allowed_tools"] != ["list", "read", "search"]:
        raise DockerRuntimeError("executable inventory tool surface is not bounded")
    executables = inventory["executables"]
    if not isinstance(executables, list) or not executables:
        raise DockerRuntimeError("executable inventory must not be empty")
    paths = []
    for index, item in enumerate(executables):
        item = _mapping(item, f"executable inventory item {index}")
        _exact_fields(item, frozenset(("path", "role", "digest")), "executable item")
        path = _text(item["path"], "executable path")
        paths.append(path)
        if status == "unverified" and item["digest"] is not None:
            raise DockerRuntimeError("unverified executable cannot claim a digest")
        if status == "verified":
            _digest(item["digest"], f"executable digest {path}")
    if frozenset(paths) != _APPROVED_EXECUTABLES or len(paths) != len(set(paths)):
        raise DockerRuntimeError("executable inventory differs from the approved runtime")
    if any(path.startswith(("/bin/", "/sbin/", "/usr/bin/")) for path in paths):
        raise DockerRuntimeError("shell or ambient executable path is forbidden")

    seccomp = json.loads(
        _contract_file(root, "seccomp-codex-read-only.json").read_text(
            encoding="utf-8"
        )
    )
    seccomp = _mapping(seccomp, "seccomp profile")
    if seccomp.get("defaultAction") != "SCMP_ACT_ERRNO":
        raise DockerRuntimeError("seccomp profile must deny by default")
    syscalls = seccomp.get("syscalls")
    if not isinstance(syscalls, list) or not syscalls:
        raise DockerRuntimeError("seccomp profile requires an explicit allowlist")
    allowed = {
        name
        for rule in syscalls
        if isinstance(rule, dict) and rule.get("action") == "SCMP_ACT_ALLOW"
        for name in rule.get("names", [])
    }
    if allowed & _FORBIDDEN_SYSCALLS:
        raise DockerRuntimeError("seccomp profile allows a privileged kernel route")
