"""Trusted-host policy compilation and host attestation for Codex evaluations."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any, Mapping, Sequence, Tuple


class CodexHostError(ValueError):
    """The requested trusted-host policy or observation is unsafe or incomplete."""


POLICY_SCHEMA_VERSION = "0.3"
READ_ONLY_PROFILE_NAME = "evaluate-skill-read-only"
FORBIDDEN_API_KEY_ENVIRONMENT = (
    "AZURE_OPENAI_API_KEY",
    "CODEX_API_KEY",
    "OPENAI_API_KEY",
)
_MCP_NAME = re.compile(r"^[A-Za-z0-9_-]+$")
_DISABLED_FEATURES = (
    "apps",
    "browser_use",
    "browser_use_external",
    "browser_use_full_cdp_access",
    "code_mode_host",
    "computer_use",
    "goals",
    "hooks",
    "image_generation",
    "in_app_browser",
    "in_app_local_automation",
    "multi_agent",
    "multi_agent_v2",
    "plugin_sharing",
    "plugins",
    "remote_plugin",
    "skill_search",
    "sleep_tool",
    "standalone_web_search",
    "view_image",
    "workspace_dependencies",
)


def _freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        return MappingProxyType({str(key): _freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


def _canonical_digest(value: Mapping[str, Any]) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _real_path(path: Path, name: str, *, directory: bool) -> Path:
    raw = Path(path)
    if not raw.is_absolute():
        raise CodexHostError(f"{name} must be absolute")
    if raw.is_symlink():
        raise CodexHostError(f"{name} must be a real {'directory' if directory else 'file'}")
    if directory and not raw.is_dir():
        raise CodexHostError(f"{name} must be a real directory")
    if not directory and not raw.is_file():
        raise CodexHostError(f"{name} must be a real file")
    return raw.resolve()


def _real_workspace(path: Path) -> Path:
    try:
        return _real_path(path, "workspace", directory=True)
    except CodexHostError as exc:
        raise CodexHostError("a real workspace directory is required") from exc


def _path_identity(path: Path) -> str:
    stat_result = os.stat(path, follow_symlinks=False)
    material = f"{path}\x00{stat_result.st_dev}\x00{stat_result.st_ino}".encode("utf-8")
    return hashlib.sha256(material).hexdigest()


def _paths_overlap(first: Path, second: Path) -> bool:
    return first == second or first.is_relative_to(second) or second.is_relative_to(first)


def _toml_inline(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, Mapping):
        fields = ",".join(
            f"{json.dumps(str(key), ensure_ascii=False)}={_toml_inline(value[key])}"
            for key in sorted(value)
        )
        return "{" + fields + "}"
    raise CodexHostError("permission policy contains an unsupported TOML value")


def _mcp_names(values: Sequence[str]) -> Tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise CodexHostError("mcp_servers must be an array")
    names = tuple(values)
    if any(not isinstance(name, str) or not _MCP_NAME.fullmatch(name) for name in names):
        raise CodexHostError("mcp server names must contain only letters, digits, _ or -")
    if len(names) != len(set(names)):
        raise CodexHostError("mcp server names must not contain duplicates")
    return tuple(sorted(names))


@dataclass(frozen=True)
class CodexHostPolicy:
    schema_version: str
    profile_name: str
    workspace: Path
    workspace_id: str
    codex_path: Path
    command_line_tools_root: Path
    home: Path
    protected_roots: Tuple[Path, ...]
    disabled_mcp_servers: Tuple[str, ...]
    cli_config: Mapping[str, Any]
    boundary_launcher: Tuple[str, ...]
    process_environment: Mapping[str, str]

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "profile_name": self.profile_name,
            "workspace": str(self.workspace),
            "workspace_id": self.workspace_id,
            "codex_path": str(self.codex_path),
            "command_line_tools_root": str(self.command_line_tools_root),
            "home": str(self.home),
            "protected_roots": [str(path) for path in self.protected_roots],
            "disabled_mcp_servers": list(self.disabled_mcp_servers),
            "cli_config": _thaw(self.cli_config),
            "boundary_launcher": list(self.boundary_launcher),
            "process_environment": dict(self.process_environment),
        }

    def digest(self) -> str:
        return _canonical_digest(self.canonical_payload())


@dataclass(frozen=True)
class HostAttestation:
    schema_version: str
    platform: Tuple[str, str, str]
    versions: Mapping[str, str]
    auth_method: str
    policy_digest: str
    workspace_id: str
    disabled_mcp_servers: Tuple[str, ...]

    def canonical_payload(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "platform": list(self.platform),
            "versions": dict(self.versions),
            "auth_method": self.auth_method,
            "policy_digest": self.policy_digest,
            "workspace_id": self.workspace_id,
            "disabled_mcp_servers": list(self.disabled_mcp_servers),
        }


def compile_read_only_policy(
    *,
    workspace: Path,
    codex_path: Path,
    command_line_tools_root: Path,
    home: Path,
    mcp_servers: Sequence[str],
    protected_roots: Sequence[Path] = (),
) -> CodexHostPolicy:
    """Compile the one supported native read-only Codex permission profile."""
    resolved_workspace = _real_workspace(workspace)
    resolved_codex = _real_path(codex_path, "codex_path", directory=False)
    if not os.access(resolved_codex, os.X_OK):
        raise CodexHostError("codex_path must be executable")
    resolved_tools = _real_path(
        command_line_tools_root, "command_line_tools_root", directory=True
    )
    resolved_home = _real_path(home, "home", directory=True)

    resolved_protected = []
    for index, protected in enumerate(protected_roots):
        raw = Path(protected)
        if not raw.is_absolute() or raw.is_symlink() or not raw.exists():
            raise CodexHostError(f"protected_roots[{index}] must be a real absolute path")
        resolved = raw.resolve()
        if _paths_overlap(resolved_workspace, resolved):
            raise CodexHostError("protected roots must not overlap the workspace")
        resolved_protected.append(resolved)
    if len(resolved_protected) != len(set(resolved_protected)):
        raise CodexHostError("protected roots must not contain duplicates")

    disabled_mcp_servers = _mcp_names(mcp_servers)
    filesystem = {
        ":root": "deny",
        ":minimal": "read",
        str(resolved_tools): "read",
        ":workspace_roots": {".": "read"},
    }
    permission_profile = {
        "filesystem": filesystem,
        "network": {"enabled": False},
    }
    features = {name: False for name in _DISABLED_FEATURES}
    features["skip_host_skill_discovery"] = True
    cli_config = {
        "default_permissions": READ_ONLY_PROFILE_NAME,
        "permissions": {READ_ONLY_PROFILE_NAME: permission_profile},
        "web_search": "disabled",
        "features": features,
        "mcp_servers": {
            name: {"enabled": False} for name in disabled_mcp_servers
        },
    }
    permission_assignment = (
        f"permissions.{READ_ONLY_PROFILE_NAME}={_toml_inline(permission_profile)}"
    )
    boundary_launcher = (
        str(resolved_codex),
        "sandbox",
        "-P",
        READ_ONLY_PROFILE_NAME,
        "-C",
        str(resolved_workspace),
        "-c",
        permission_assignment,
        "--",
    )
    process_environment = {
        "HOME": str(resolved_home),
        "PATH": os.defpath,
        "LANG": "C",
        "LC_ALL": "C",
        "PYTHONIOENCODING": "utf-8",
    }
    return CodexHostPolicy(
        schema_version=POLICY_SCHEMA_VERSION,
        profile_name=READ_ONLY_PROFILE_NAME,
        workspace=resolved_workspace,
        workspace_id=_path_identity(resolved_workspace),
        codex_path=resolved_codex,
        command_line_tools_root=resolved_tools,
        home=resolved_home,
        protected_roots=tuple(sorted(resolved_protected, key=str)),
        disabled_mcp_servers=disabled_mcp_servers,
        cli_config=_freeze(cli_config),
        boundary_launcher=boundary_launcher,
        process_environment=_freeze(process_environment),
    )


def _platform(value: Sequence[str], name: str) -> Tuple[str, str, str]:
    if isinstance(value, (str, bytes)) or len(value) != 3:
        raise CodexHostError(f"{name} platform fingerprint is invalid")
    result = tuple(value)
    if any(not isinstance(item, str) or not item.strip() for item in result):
        raise CodexHostError(f"{name} platform fingerprint is invalid")
    return (result[0].lower(), result[1], result[2].lower())


def _versions(value: Mapping[str, str], name: str) -> dict[str, str]:
    if not isinstance(value, Mapping) or not value:
        raise CodexHostError(f"{name} versions are required")
    result = {}
    for tool, version in value.items():
        if not isinstance(tool, str) or not tool or not isinstance(version, str) or not version:
            raise CodexHostError(f"{name} versions are invalid")
        result[tool] = version
    return result


def attest_host(
    policy: CodexHostPolicy,
    *,
    expected_platform: Sequence[str],
    observed_platform: Sequence[str],
    expected_versions: Mapping[str, str],
    observed_versions: Mapping[str, str],
    login_status: str,
    observed_mcp_servers: Sequence[str],
    environment: Mapping[str, str],
) -> HostAttestation:
    """Bind sanitized host observations to an unchanged compiled policy."""
    if not isinstance(policy, CodexHostPolicy):
        raise CodexHostError("a compiled CodexHostPolicy is required")
    expected_host = _platform(expected_platform, "expected")
    observed_host = _platform(observed_platform, "observed")
    if observed_host != expected_host:
        raise CodexHostError("observed platform does not match the pinned platform")

    required_versions = _versions(expected_versions, "expected")
    actual_versions = _versions(observed_versions, "observed")
    mismatches = [
        tool
        for tool, required in sorted(required_versions.items())
        if actual_versions.get(tool) != required
    ]
    if mismatches:
        raise CodexHostError(
            "observed tool version does not match the pin: " + ", ".join(mismatches)
        )

    if not isinstance(environment, Mapping):
        raise CodexHostError("host environment must be an object")
    present_api_keys = [name for name in FORBIDDEN_API_KEY_ENVIRONMENT if name in environment]
    if present_api_keys:
        raise CodexHostError(
            "API-key environment authentication is forbidden: "
            + ", ".join(present_api_keys)
        )
    if not isinstance(login_status, str) or login_status.strip().lower() != (
        "logged in using chatgpt"
    ):
        raise CodexHostError("ChatGPT file login is required")

    observed_mcp = _mcp_names(observed_mcp_servers)
    if observed_mcp != policy.disabled_mcp_servers:
        raise CodexHostError("observed MCP server inventory does not match the compiled policy")

    workspace = _real_workspace(policy.workspace)
    if _path_identity(workspace) != policy.workspace_id:
        raise CodexHostError("workspace identity changed after policy compilation")
    for protected in policy.protected_roots:
        if protected.is_symlink() or not protected.exists():
            raise CodexHostError("protected root identity is no longer valid")
        if _paths_overlap(workspace, protected.resolve()):
            raise CodexHostError("protected roots overlap the workspace")

    return HostAttestation(
        schema_version=POLICY_SCHEMA_VERSION,
        platform=observed_host,
        versions=_freeze({tool: actual_versions[tool] for tool in sorted(required_versions)}),
        auth_method="chatgpt-file",
        policy_digest=policy.digest(),
        workspace_id=policy.workspace_id,
        disabled_mcp_servers=policy.disabled_mcp_servers,
    )
