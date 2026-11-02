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
        return cls(
            schema_version=schema_version,
            status=status,
            provider=_text(value["provider"], "image lock.provider"),
            profile=profile,
            base_image=base_image,
            final_image=final_image,
            target_platform=target_platform,
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
