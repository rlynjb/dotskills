"""Trusted-host policy compilation and host attestation for Codex evaluations."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
from types import MappingProxyType
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple

from capability_inventory import CapabilityInventory, PlatformFingerprint
from contracts import ApprovalReceipt, ContractError, EnforcementReceipt, RunPlan
from evidence import EvidenceError, StateSnapshot, snapshot_tree
from native_boundary import (
    BoundaryError,
    NativeBoundaryResult,
    provider_config_digest as boundary_config_digest,
    run_native_preflight,
)


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
        "/usr/bin/env",
        "-i",
        f"HOME={resolved_home}",
        f"PATH={os.defpath}",
        "LANG=C",
        "LC_ALL=C",
        "PYTHONIOENCODING=utf-8",
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


@dataclass(frozen=True)
class PreflightRequest:
    plan: RunPlan
    approval: ApprovalReceipt
    inventory: CapabilityInventory
    policy: CodexHostPolicy
    attestation: HostAttestation
    bundle: Path
    provider_config: Mapping[str, Any]
    artifact_directory: Path
    issued_at: str
    expires_at: str
    verifier_version: str
    known_secret_values: Tuple[str, ...] = ()


@dataclass(frozen=True)
class PreflightResult:
    receipt: EnforcementReceipt
    boundary: NativeBoundaryResult
    policy_digest: str
    bundle_digest: str
    provider_config_digest: str
    protected_snapshots: Tuple[StateSnapshot, ...]
    workspace_snapshot: StateSnapshot
    policy_artifact: Path
    snapshot_artifact: Path
    probe_artifact: Path
    receipt_artifact: Path


def _timestamp(value: str, name: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise CodexHostError(f"{name} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise CodexHostError(f"{name} must be an ISO-8601 timestamp") from None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise CodexHostError(f"{name} must include a timezone")
    return parsed.astimezone(timezone.utc)


def _read_json_object(path: Path, label: str, *, max_bytes: int = 4 * 1024 * 1024) -> dict[str, Any]:
    path = Path(path)
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = None
    try:
        descriptor = os.open(path, flags)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > max_bytes:
            raise CodexHostError(f"{label} must be a bounded regular file")
        chunks = []
        while True:
            chunk = os.read(descriptor, min(1024 * 1024, max_bytes + 1))
            if not chunk:
                break
            chunks.append(chunk)
            if sum(len(item) for item in chunks) > max_bytes:
                raise CodexHostError(f"{label} exceeds the size limit")
        value = json.loads(b"".join(chunks).decode("utf-8"))
    except CodexHostError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CodexHostError(f"cannot read {label}: {type(exc).__name__}") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if not isinstance(value, dict):
        raise CodexHostError(f"{label} must contain a JSON object")
    return value


def _preflight_paths(directory: Path) -> tuple[Path, Path, Path, Path]:
    return (
        directory / "host-policy.json",
        directory / "preflight-snapshots.json",
        directory / "preflight-probes.json",
        directory / "enforcement-receipt.json",
    )


def _write_json_exclusive(path: Path, payload: Mapping[str, Any]) -> Path:
    encoded = (
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
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
        raise CodexHostError(f"trusted host artifact already exists: {path.name}") from None
    except OSError as exc:
        raise CodexHostError(
            f"cannot durably publish trusted host artifact {path.name}: {type(exc).__name__}"
        ) from None
    finally:
        if descriptor is not None:
            os.close(descriptor)
    return path


def _redact(value: Any, secrets: Tuple[str, ...]) -> Any:
    if isinstance(value, str):
        result = value
        for secret in secrets:
            result = result.replace(secret, "[REDACTED]")
        return result
    if isinstance(value, Mapping):
        return {str(key): _redact(item, secrets) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_redact(item, secrets) for item in value]
    return value


def _receipt_payload(receipt: EnforcementReceipt) -> dict[str, Any]:
    return {
        "schema_version": receipt.schema_version,
        "plan_digest": receipt.plan_digest,
        "verified_by": receipt.verified_by,
        "verifier_version": receipt.verifier_version,
        "issued_at": receipt.issued_at,
        "expires_at": receipt.expires_at,
        "run_nonce": receipt.run_nonce,
        "provider": receipt.provider,
        "provider_version": receipt.provider_version,
        "model": receipt.model,
        "model_version": receipt.model_version,
        "adapter": receipt.adapter,
        "adapter_version": receipt.adapter_version,
        "backend": receipt.backend,
        "backend_version": receipt.backend_version,
        "capability_profile": receipt.capability_profile,
        "effective_policy_digest": receipt.effective_policy_digest,
        "provider_config_digest": receipt.provider_config_digest,
        "prepared_bundle_digest": receipt.prepared_bundle_digest,
        "workspace_id": receipt.workspace_id,
        "probe_results": dict(receipt.probe_results),
        "enabled_tools": list(receipt.enabled_tools),
        "disabled_tools": list(receipt.disabled_tools),
        "state_verification_method": receipt.state_verification_method,
        "cleanup_method": receipt.cleanup_method,
    }


def _snapshot_payload(snapshot: StateSnapshot) -> dict[str, Any]:
    return asdict(snapshot)


def _validate_preflight_request(request: PreflightRequest) -> tuple[Path, Path, dict[str, Any]]:
    if not isinstance(request, PreflightRequest):
        raise CodexHostError("a PreflightRequest is required")
    plan = request.plan
    if not isinstance(plan, RunPlan):
        raise CodexHostError("preflight requires a RunPlan")
    if (
        plan.provider != "openai"
        or plan.adapter != "promptfoo-codex-sdk"
        or plan.backend != "native"
        or plan.capabilities.profile != "read-only"
    ):
        raise CodexHostError("preflight supports only the pinned native Codex read-only route")
    if not isinstance(request.approval, ApprovalReceipt):
        raise CodexHostError("preflight requires an ApprovalReceipt")
    issued = _timestamp(request.issued_at, "preflight issued_at")
    expires = _timestamp(request.expires_at, "preflight expires_at")
    if issued >= expires:
        raise CodexHostError("preflight expiry must follow issuance")
    try:
        request.approval.validate_for(plan, at=issued)
    except ContractError as exc:
        raise CodexHostError(f"approval receipt is invalid: {exc}") from None
    if expires > _timestamp(request.approval.expires_at, "approval expires_at"):
        raise CodexHostError("preflight receipt cannot outlive approval")

    if not isinstance(request.policy, CodexHostPolicy):
        raise CodexHostError("preflight requires a CodexHostPolicy")
    if not isinstance(request.attestation, HostAttestation):
        raise CodexHostError("preflight requires a HostAttestation")
    if (
        request.attestation.policy_digest != request.policy.digest()
        or request.attestation.workspace_id != request.policy.workspace_id
    ):
        raise CodexHostError("host attestation does not match the compiled policy")

    if not isinstance(request.inventory, CapabilityInventory):
        raise CodexHostError("preflight requires a CapabilityInventory")
    inventory_platform = PlatformFingerprint(*request.attestation.platform)
    if request.inventory.platform != inventory_platform:
        raise CodexHostError("capability inventory platform changed after host attestation")
    for tool in ("codex", "promptfoo"):
        if request.inventory.required_versions.get(tool) != request.attestation.versions.get(tool):
            raise CodexHostError(f"capability inventory version changed for {tool}")
    provider_key = request.inventory.provider_for_plan(plan.provider, plan.adapter)
    if provider_key != "codex":
        raise CodexHostError("capability inventory does not identify the pinned Codex route")
    descriptor = request.inventory.providers[provider_key]
    if (
        descriptor.provider_version != plan.provider_version
        or descriptor.adapter_version != plan.adapter_version
    ):
        raise CodexHostError("capability inventory provider identity changed")

    bundle = _real_workspace(request.bundle)
    if bundle != request.policy.workspace or _path_identity(bundle) != request.policy.workspace_id:
        raise CodexHostError("configured bundle does not match the policy workspace")
    artifacts = Path(request.artifact_directory)
    if not artifacts.is_absolute() or artifacts.is_symlink() or not artifacts.is_dir():
        raise CodexHostError("artifact directory must be a real existing directory")
    artifacts = artifacts.resolve()
    if _paths_overlap(bundle, artifacts):
        raise CodexHostError("artifact directory must be outside the evaluated workspace")

    if not isinstance(request.provider_config, Mapping):
        raise CodexHostError("native boundary provider config is required")
    if tuple(request.provider_config.get("boundary_launcher", ())) != request.policy.boundary_launcher:
        raise CodexHostError("native boundary launcher does not match the compiled policy")
    if request.provider_config.get("sandbox_mode") != request.policy.profile_name:
        raise CodexHostError("native boundary permission profile does not match the policy")
    if request.provider_config.get("connectors_enabled") or request.provider_config.get("mcp_servers"):
        raise CodexHostError("connectors and MCP servers must be disabled for preflight")

    manifest = _read_json_object(bundle / "manifest.json", "configured bundle manifest")
    if manifest.get("status") != "CONFIGURED_NOT_BOUND":
        raise CodexHostError("configured bundle must be fresh and unbound")
    if manifest.get("plan_digest") != plan.digest():
        raise CodexHostError("configured bundle plan digest changed")
    for field in (
        "provider",
        "provider_version",
        "model",
        "model_version",
        "adapter",
        "adapter_version",
    ):
        if manifest.get(field) != getattr(plan, field):
            raise CodexHostError(f"configured bundle {field} changed")

    # Local import avoids a module cycle when native_eval later consumes the host policy.
    import native_eval

    try:
        bundle_digest = native_eval._bundle_digest(bundle)
        provider_digest = native_eval._provider_config_digest(bundle, manifest)
    except native_eval.Blocked as exc:
        raise CodexHostError(f"configured bundle cannot be revalidated: {exc}") from None
    if manifest.get("bundle_digest") != bundle_digest:
        raise CodexHostError("configured bundle digest changed")
    if manifest.get("provider_config_digest") != provider_digest:
        raise CodexHostError("configured provider config digest changed")
    return bundle, artifacts, manifest


def run_trusted_preflight(
    request: PreflightRequest,
    *,
    boundary_runner: Optional[
        Callable[[RunPlan, Path, Mapping[str, Any]], NativeBoundaryResult]
    ] = None,
) -> PreflightResult:
    """Run local negative probes and issue a short-lived, durable receipt."""
    bundle, artifact_directory, manifest = _validate_preflight_request(request)
    policy_path, snapshot_path, probe_path, receipt_path = _preflight_paths(
        artifact_directory
    )
    for path in (policy_path, snapshot_path, probe_path, receipt_path):
        if os.path.lexists(path):
            raise CodexHostError(f"trusted host artifact already exists: {path.name}")

    runner = run_native_preflight if boundary_runner is None else boundary_runner
    try:
        boundary = runner(request.plan, bundle, request.provider_config)
    except (BoundaryError, OSError) as exc:
        raise CodexHostError(f"native boundary probe execution failed: {exc}") from None
    if not isinstance(boundary, NativeBoundaryResult):
        raise CodexHostError("native boundary probe result is invalid")
    if not boundary.is_valid_for(request.plan, request.provider_config):
        raise CodexHostError("native boundary probe result binding is invalid")
    if not boundary.complete:
        raise CodexHostError("complete successful native boundary probe evidence is required")

    try:
        protected_snapshots = tuple(snapshot_tree(path, ()) for path in request.policy.protected_roots)
        workspace_snapshot = snapshot_tree(bundle, ())
    except EvidenceError as exc:
        raise CodexHostError(f"preflight state snapshot failed: {exc}") from None

    probe_results = {item.probe_id: item.status for item in boundary.results}
    probe_results.update(
        {
            "action-trace-completeness": "UNKNOWN",
            "cleanup-verification": "UNKNOWN",
            "provider-auth-gateway": "PASS",
            "resource-limits": "PASS",
            "state-snapshot": "PASS",
        }
    )
    enabled_tools = ("filesystem_read",)
    disabled_tools = ("filesystem_write", "shell", "network", "mock_tools")
    try:
        receipt = EnforcementReceipt.from_dict(
            {
                "schema_version": request.plan.schema_version,
                "plan_digest": request.plan.digest(),
                "verified_by": "evaluate-skill-trusted-host",
                "verifier_version": request.verifier_version,
                "issued_at": request.issued_at,
                "expires_at": request.expires_at,
                "run_nonce": request.approval.run_nonce,
                "provider": request.plan.provider,
                "provider_version": request.plan.provider_version,
                "model": request.plan.model,
                "model_version": request.plan.model_version,
                "adapter": request.plan.adapter,
                "adapter_version": request.plan.adapter_version,
                "backend": request.plan.backend,
                "backend_version": f"codex-seatbelt-host-{POLICY_SCHEMA_VERSION}",
                "capability_profile": request.plan.capabilities.profile,
                "effective_policy_digest": request.plan.capabilities.digest(),
                "provider_config_digest": manifest["provider_config_digest"],
                "prepared_bundle_digest": manifest["bundle_digest"],
                "workspace_id": request.policy.workspace_id,
                "probe_results": probe_results,
                "enabled_tools": list(enabled_tools),
                "disabled_tools": list(disabled_tools),
                "state_verification_method": "tree-digest-v1",
                "cleanup_method": "remove-and-verify-v1",
            }
        )
    except ContractError as exc:
        raise CodexHostError(f"cannot issue enforcement receipt: {exc}") from None

    secrets = tuple(
        sorted(
            {
                value
                for value in request.known_secret_values
                if isinstance(value, str) and value
            },
            key=len,
            reverse=True,
        )
    )
    policy_payload = _redact(request.policy.canonical_payload(), secrets)
    snapshot_payload = _redact(
        {
            "schema_version": POLICY_SCHEMA_VERSION,
            "plan_digest": request.plan.digest(),
            "run_nonce": request.approval.run_nonce,
            "workspace": _snapshot_payload(workspace_snapshot),
            "protected": [
                _snapshot_payload(snapshot) for snapshot in protected_snapshots
            ],
        },
        secrets,
    )
    probe_payload = _redact(
        {
            "schema_version": POLICY_SCHEMA_VERSION,
            "plan_digest": request.plan.digest(),
            "run_nonce": request.approval.run_nonce,
            "host_policy_digest": request.policy.digest(),
            "boundary_config_digest": boundary_config_digest(request.provider_config),
            "provider_config_digest": manifest["provider_config_digest"],
            "prepared_bundle_digest": manifest["bundle_digest"],
            "results": [asdict(item) for item in boundary.results],
        },
        secrets,
    )
    receipt_payload = _redact(_receipt_payload(receipt), secrets)

    _write_json_exclusive(policy_path, policy_payload)
    _write_json_exclusive(snapshot_path, snapshot_payload)
    _write_json_exclusive(probe_path, probe_payload)
    _write_json_exclusive(receipt_path, receipt_payload)
    return PreflightResult(
        receipt=receipt,
        boundary=boundary,
        policy_digest=request.policy.digest(),
        bundle_digest=manifest["bundle_digest"],
        provider_config_digest=manifest["provider_config_digest"],
        protected_snapshots=protected_snapshots,
        workspace_snapshot=workspace_snapshot,
        policy_artifact=policy_path,
        snapshot_artifact=snapshot_path,
        probe_artifact=probe_path,
        receipt_artifact=receipt_path,
    )
