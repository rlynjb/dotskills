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
import subprocess
import tempfile
import time
from types import MappingProxyType
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple

from capability_inventory import CapabilityInventory, PlatformFingerprint
from contracts import ApprovalReceipt, ContractError, EnforcementReceipt, RunPlan
from evidence import (
    EvidenceBundle,
    EvidenceError,
    StateEntry,
    StateSnapshot,
    StateSnapshots,
    evidence_bundle_digest,
    evidence_bundle_payload,
    snapshot_tree,
)
from native_boundary import (
    BoundaryError,
    NativeBoundaryResult,
    provider_config_digest as boundary_config_digest,
    run_native_preflight,
)
from provider_trace import (
    ObservedSessionIdentity,
    ParsedArm,
    ProviderTraceBinding,
    parse_promptfoo_result,
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


@dataclass(frozen=True)
class SupervisedRunRequest:
    plan: RunPlan
    policy: CodexHostPolicy
    preflight: PreflightResult
    bundle: Path
    command: Tuple[str, ...]
    nonce_ledger: Path
    artifact_directory: Path
    known_secret_values: Tuple[str, ...] = ()


@dataclass(frozen=True)
class SupervisedProcessResult:
    returncode: int
    stdout: bytes
    stderr: bytes
    observed_sessions: Tuple[ObservedSessionIdentity, ...]


@dataclass(frozen=True)
class SupervisedArmResult:
    arm_name: str
    provider_result_path: Path
    quality_path: Path
    evidence_path: Path
    execution_status: str
    quality_status: str
    safety_status: str
    evidence: EvidenceBundle


@dataclass(frozen=True)
class SupervisedRunResult:
    run_id: str
    execution_id: str
    execution_status: str
    quality_status: str
    safety_status: str
    source_result_digest: str
    trace_artifact: Path
    arms: Tuple[SupervisedArmResult, ...]


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
        native_eval.validate_configured_host_policy(bundle, request.policy)
    except native_eval.Blocked as exc:
        raise CodexHostError(f"configured bundle cannot be revalidated: {exc}") from None
    if manifest.get("host_policy_digest") != request.policy.digest():
        raise CodexHostError("configured bundle host policy digest changed")
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


def _write_bytes_exclusive(path: Path, payload: bytes) -> Path:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = None
    try:
        descriptor = os.open(path, flags, 0o600)
        offset = 0
        while offset < len(payload):
            offset += os.write(descriptor, payload[offset:])
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


class _TransitionRecorder:
    def __init__(
        self,
        directory: Path,
        base_payload: Mapping[str, Any],
        hook: Optional[Callable[[str], None]],
    ) -> None:
        self.directory = directory
        self.base_payload = dict(base_payload)
        self.hook = hook
        self.sequence = 0

    def record(self, state: str, payload: Mapping[str, Any] = MappingProxyType({})) -> Path:
        self.sequence += 1
        path = self.directory / f"run-state-{self.sequence:02d}-{state}.json"
        value = dict(self.base_payload)
        value.update({"sequence": self.sequence, "state": state})
        value.update(dict(payload))
        _write_json_exclusive(path, value)
        if self.hook is not None:
            self.hook(state)
        return path


def _combined_snapshot(snapshots: Sequence[StateSnapshot]) -> StateSnapshot:
    snapshots = tuple(snapshots)
    if not snapshots:
        raise CodexHostError("at least one protected snapshot is required")
    if len(snapshots) == 1:
        return snapshots[0]
    entries = []
    for index, snapshot in enumerate(snapshots):
        prefix = f"root-{index:02d}"
        entries.append(StateEntry(prefix, "directory", 0, snapshot.digest))
        entries.extend(
            StateEntry(
                f"{prefix}/{entry.path}",
                entry.entry_type,
                entry.mode,
                entry.content_digest,
            )
            for entry in snapshot.entries
        )
    entries_tuple = tuple(entries)
    payload = [asdict(entry) for entry in entries_tuple]
    return StateSnapshot(
        root_id=_canonical_digest({
            "roots": [snapshot.root_id for snapshot in snapshots]
        }),
        entries=entries_tuple,
        digest=hashlib.sha256(_canonical_json_bytes(payload)).hexdigest(),
    )


def _canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def _remove_tree_no_follow(path: Path) -> bool:
    """Remove a host-owned tree without following links; return whether links existed."""
    path = Path(path)
    metadata = os.lstat(path)
    if stat.S_ISLNK(metadata.st_mode):
        path.unlink()
        return True
    if not stat.S_ISDIR(metadata.st_mode):
        raise OSError("cleanup target is not a directory")
    found_link = False
    with os.scandir(path) as iterator:
        entries = list(iterator)
    for entry in entries:
        child = Path(entry.path)
        child_metadata = entry.stat(follow_symlinks=False)
        if stat.S_ISLNK(child_metadata.st_mode):
            child.unlink()
            found_link = True
        elif stat.S_ISDIR(child_metadata.st_mode):
            found_link = _remove_tree_no_follow(child) or found_link
        else:
            child.unlink()
    path.rmdir()
    return found_link


def _cleanup_disposable_workspaces(
    bundle: Path, arm_paths: Mapping[str, Path]
) -> bool:
    found_link = False
    for path in (*arm_paths.values(), bundle / "codex" / "judge"):
        if not os.path.lexists(path):
            continue
        found_link = _remove_tree_no_follow(path) or found_link
    if any(os.path.lexists(path) for path in (
        *arm_paths.values(), bundle / "codex" / "judge"
    )):
        raise OSError("workspace removal could not be verified")
    return found_link


def _bounded_process_runner(
    argv: Sequence[str],
    *,
    cwd: Path,
    environment: Mapping[str, str],
    timeout: int,
    max_output_bytes: int,
) -> SupervisedProcessResult:
    """Run a process with disk-backed output, killing it on time or output overflow."""
    with tempfile.TemporaryFile() as stdout_file, tempfile.TemporaryFile() as stderr_file:
        process = subprocess.Popen(
            list(argv),
            cwd=cwd,
            env=dict(environment),
            stdin=subprocess.DEVNULL,
            stdout=stdout_file,
            stderr=stderr_file,
            close_fds=True,
        )
        deadline = time.monotonic() + timeout
        failure = None
        while process.poll() is None:
            total_size = (
                os.fstat(stdout_file.fileno()).st_size
                + os.fstat(stderr_file.fileno()).st_size
            )
            if total_size > max_output_bytes:
                failure = "output-limit"
                process.kill()
                break
            if time.monotonic() >= deadline:
                failure = "timeout"
                process.kill()
                break
            time.sleep(0.01)
        process.wait()
        total_size = (
            os.fstat(stdout_file.fileno()).st_size
            + os.fstat(stderr_file.fileno()).st_size
        )
        if total_size > max_output_bytes:
            failure = "output-limit"
        if failure == "timeout":
            raise TimeoutError("provider process exceeded the approved timeout")
        if failure == "output-limit":
            raise CodexHostError("provider process exceeded the approved output limit")
        stdout_file.seek(0)
        stderr_file.seek(0)
        return SupervisedProcessResult(
            returncode=process.returncode,
            stdout=stdout_file.read(max_output_bytes + 1),
            stderr=stderr_file.read(max_output_bytes + 1),
            observed_sessions=(),
        )


def _supervised_artifact_paths(directory: Path) -> tuple[Path, ...]:
    paths = []
    for arm in ("with-skill", "without-skill"):
        paths.extend((
            directory / f"{arm}-provider-result.json",
            directory / f"{arm}-quality.json",
            directory / f"{arm}-evidence.json",
        ))
    paths.append(directory / "host-trace.json")
    return tuple(paths)


def _validate_supervised_request(
    request: SupervisedRunRequest,
) -> tuple[Path, Path, dict[str, Any], Mapping[str, Any]]:
    if not isinstance(request, SupervisedRunRequest):
        raise CodexHostError("a SupervisedRunRequest is required")
    if not isinstance(request.plan, RunPlan):
        raise CodexHostError("supervision requires a RunPlan")
    if not isinstance(request.policy, CodexHostPolicy):
        raise CodexHostError("supervision requires a CodexHostPolicy")
    if not isinstance(request.preflight, PreflightResult):
        raise CodexHostError("supervision requires a trusted preflight result")
    plan = request.plan
    receipt = request.preflight.receipt
    if (
        receipt.plan_digest != plan.digest()
        or receipt.provider != plan.provider
        or receipt.provider_version != plan.provider_version
        or receipt.model != plan.model
        or receipt.model_version != plan.model_version
        or receipt.adapter != plan.adapter
        or receipt.adapter_version != plan.adapter_version
        or receipt.backend != plan.backend
    ):
        raise CodexHostError("preflight receipt identity does not match the run plan")
    now = datetime.now(timezone.utc)
    if now < _timestamp(receipt.issued_at, "receipt issued_at"):
        raise CodexHostError("preflight receipt is not yet valid")
    if now >= _timestamp(receipt.expires_at, "receipt expires_at"):
        raise CodexHostError("preflight receipt expired before dispatch")
    if (
        request.preflight.policy_digest != request.policy.digest()
        or request.preflight.bundle_digest != receipt.prepared_bundle_digest
        or request.preflight.provider_config_digest != receipt.provider_config_digest
        or receipt.workspace_id != request.policy.workspace_id
        or not request.preflight.boundary.complete
    ):
        raise CodexHostError("preflight policy, boundary, bundle, or receipt binding changed")

    bundle = _real_workspace(request.bundle)
    if bundle != request.policy.workspace or _path_identity(bundle) != receipt.workspace_id:
        raise CodexHostError("supervised bundle identity changed")
    artifacts = Path(request.artifact_directory)
    if not artifacts.is_absolute() or artifacts.is_symlink() or not artifacts.is_dir():
        raise CodexHostError("supervised artifact directory must be real and absolute")
    artifacts = artifacts.resolve()
    if artifacts != request.preflight.receipt_artifact.parent.resolve():
        raise CodexHostError("supervision artifact directory differs from preflight")
    if _paths_overlap(bundle, artifacts):
        raise CodexHostError("supervision artifacts must remain outside the evaluated workspace")
    ledger = Path(request.nonce_ledger)
    if not ledger.is_absolute() or ledger.is_symlink() or not ledger.is_dir():
        raise CodexHostError("nonce ledger must be a real absolute directory")
    ledger = ledger.resolve()
    if _paths_overlap(bundle, ledger):
        raise CodexHostError("nonce ledger must remain outside the evaluated workspace")

    import native_eval

    manifest = _read_json_object(bundle / "manifest.json", "bound bundle manifest")
    if manifest.get("status") != "BOUND_NOT_RUN":
        raise CodexHostError("supervised bundle is not a fresh bound execution")
    if manifest.get("plan_digest") != plan.digest():
        raise CodexHostError("bound bundle plan digest changed")
    if manifest.get("host_policy_digest") != request.policy.digest():
        raise CodexHostError("bound bundle host policy changed")
    try:
        bundle_digest = native_eval._bundle_digest(bundle)
        provider_digest = native_eval._provider_config_digest(bundle, manifest)
        native_eval.validate_configured_host_policy(bundle, request.policy)
        expected_command = tuple(native_eval.native_command(bundle, manifest))
    except native_eval.Blocked as exc:
        raise CodexHostError(f"bound bundle cannot be revalidated: {exc}") from None
    if (
        bundle_digest != manifest.get("bundle_digest")
        or bundle_digest != request.preflight.bundle_digest
        or provider_digest != manifest.get("provider_config_digest")
        or provider_digest != request.preflight.provider_config_digest
    ):
        raise CodexHostError("bound bundle or provider config digest changed")

    if not isinstance(request.command, tuple) or len(request.command) < 2:
        raise CodexHostError("exact supervised provider command is required")
    binary = _real_path(Path(request.command[0]), "Promptfoo command", directory=False)
    if not os.access(binary, os.X_OK):
        raise CodexHostError("Promptfoo command must be executable")
    exact_command = (str(binary), *expected_command[1:])
    if request.command != exact_command:
        raise CodexHostError("supervised command differs from the bound Promptfoo command")
    result_path = bundle / "codex-results.json"
    if os.path.lexists(result_path):
        raise CodexHostError("fresh supervised bundle already contains provider output")
    for path in _supervised_artifact_paths(artifacts):
        if os.path.lexists(path):
            raise CodexHostError(f"trusted host artifact already exists: {path.name}")
    promptfoo_config = _read_json_object(
        bundle / "codex" / "promptfooconfig.yaml", "bound Promptfoo config"
    )
    return bundle, ledger, manifest, promptfoo_config


def _quality_status(arm: ParsedArm) -> str:
    quality = arm.quality
    grading = quality.get("grading_result")
    if grading is None:
        return "NOT_GRADED"
    if quality.get("success") is True and grading.get("pass") is True:
        return "PASS"
    if quality.get("success") is False or grading.get("pass") is False:
        return "FAIL"
    return "UNKNOWN"


def run_supervised_provider(
    request: SupervisedRunRequest,
    *,
    process_runner: Optional[Callable[..., SupervisedProcessResult]] = None,
    transition_hook: Optional[Callable[[str], None]] = None,
) -> SupervisedRunResult:
    """Consume one receipt and supervise exactly one paired Promptfoo execution."""
    bundle, ledger, manifest, promptfoo_config = _validate_supervised_request(request)
    import native_eval

    try:
        execution_id, manifest = native_eval.claim_supervised_execution(
            bundle, request.plan, request.preflight.receipt, ledger
        )
    except native_eval.Blocked as exc:
        raise CodexHostError(f"cannot consume supervised execution nonce: {exc}") from None
    recorder = _TransitionRecorder(
        request.artifact_directory,
        {
            "schema_version": POLICY_SCHEMA_VERSION,
            "plan_digest": request.plan.digest(),
            "run_nonce": request.preflight.receipt.run_nonce,
            "execution_id": execution_id,
        },
        transition_hook,
    )
    secrets = tuple(sorted(
        {
            value for value in request.known_secret_values
            if isinstance(value, str) and value
        },
        key=len,
        reverse=True,
    ))
    arm_paths = {
        "with-skill": bundle / "codex" / "with_skill",
        "without-skill": bundle / "codex" / "without_skill",
    }
    try:
        before_arms = {
            arm: snapshot_tree(path, ()) for arm, path in arm_paths.items()
        }
        before_protected = _combined_snapshot(request.preflight.protected_snapshots)
        recorder.record("run-started", {"command_digest": hashlib.sha256(
            "\0".join(request.command).encode("utf-8")
        ).hexdigest()})

        runner = _bounded_process_runner if process_runner is None else process_runner
        environment = {
            **dict(request.policy.process_environment),
            **dict(native_eval._PROMPTFOO_SAFE_ENV),
        }
        process = runner(
            request.command,
            cwd=bundle,
            environment=environment,
            timeout=int(request.plan.resource_limits["max_seconds"]),
            max_output_bytes=int(request.plan.resource_limits["max_output_bytes"]),
        )
        if not isinstance(process, SupervisedProcessResult):
            raise CodexHostError("trusted process runner returned an invalid result")
        if isinstance(process.returncode, bool) or not isinstance(process.returncode, int):
            raise CodexHostError("provider process return code is invalid")
        if not isinstance(process.stdout, bytes) or not isinstance(process.stderr, bytes):
            raise CodexHostError("provider process output must be captured as bytes")
        if len(process.stdout) + len(process.stderr) > int(
            request.plan.resource_limits["max_output_bytes"]
        ):
            raise CodexHostError("provider process exceeded the approved output limit")
        recorder.record("provider-exited", {
            "returncode": process.returncode,
            "stdout_digest": hashlib.sha256(process.stdout).hexdigest(),
            "stdout_bytes": len(process.stdout),
            "stderr_digest": hashlib.sha256(process.stderr).hexdigest(),
            "stderr_bytes": len(process.stderr),
        })
        if process.returncode != 0:
            raise CodexHostError(f"provider process exited nonzero: {process.returncode}")

        binding = ProviderTraceBinding(
            provider_config_digest=request.preflight.provider_config_digest,
            promptfoo_config=promptfoo_config,
            observed_sessions=process.observed_sessions,
        )
        parsed = parse_promptfoo_result(
            bundle / "codex-results.json",
            request.plan,
            binding,
            known_secret_values=secrets,
        )
        recorder.record("result-parsed", {
            "source_result_digest": parsed.source_file_digest,
            "arm_source_result_digests": {
                arm.arm_name: arm.source_result_digest for arm in parsed.arms
            },
        })

        after_arms = {
            arm: snapshot_tree(path, ()) for arm, path in arm_paths.items()
        }
        after_protected_snapshots = tuple(
            snapshot_tree(path, ()) for path in request.policy.protected_roots
        )
        after_protected = _combined_snapshot(after_protected_snapshots)
        if after_protected != before_protected:
            raise CodexHostError("protected state changed during provider execution")
        if any(after_arms[arm] != before_arms[arm] for arm in arm_paths):
            raise CodexHostError("read-only arm workspace changed during provider execution")
        recorder.record("state-verified", {
            "protected_digest": after_protected.digest,
            "arm_digests": {arm: value.digest for arm, value in after_arms.items()},
        })

        try:
            found_link = _cleanup_disposable_workspaces(bundle, arm_paths)
        except OSError as exc:
            raise CodexHostError(
                f"workspace cleanup failed: {type(exc).__name__}"
            ) from None
        if found_link:
            raise CodexHostError("workspace cleanup found an unexpected symlink")
        recorder.record("cleanup-verified")

        supervised_arms = []
        trace_payload = {
            "schema_version": POLICY_SCHEMA_VERSION,
            "plan_digest": request.plan.digest(),
            "run_nonce": request.preflight.receipt.run_nonce,
            "execution_id": execution_id,
            "source_result_digest": parsed.source_file_digest,
            "arm_events": {},
        }
        for parsed_arm in parsed.arms:
            arm_name = parsed_arm.arm_name
            provider_path = (
                request.artifact_directory / f"{arm_name}-provider-result.json"
            )
            quality_path = request.artifact_directory / f"{arm_name}-quality.json"
            evidence_path = request.artifact_directory / f"{arm_name}-evidence.json"
            provider_payload = _canonical_json_bytes(parsed_arm.provider_result)
            _write_bytes_exclusive(provider_path, provider_payload)
            _write_json_exclusive(quality_path, _redact(parsed_arm.quality, secrets))
            events = [
                {
                    "type": "run_start",
                    "plan_digest": request.plan.digest(),
                    "run_id": request.preflight.receipt.run_nonce,
                    "receipt_nonce": request.preflight.receipt.run_nonce,
                    "execution_id": execution_id,
                    "arm_name": arm_name,
                    "workspace_id": request.preflight.receipt.workspace_id,
                },
                *parsed_arm.events,
                {
                    "type": "model_result",
                    "run_id": request.preflight.receipt.run_nonce,
                    "receipt_nonce": request.preflight.receipt.run_nonce,
                    "execution_id": execution_id,
                    "arm_name": arm_name,
                    "workspace_id": request.preflight.receipt.workspace_id,
                    "provider_result_digest": parsed_arm.provider_result_digest,
                    "source_result_digest": parsed_arm.source_result_digest,
                },
                {
                    "type": "run_end",
                    "trace_complete": True,
                    "cleanup_complete": True,
                    "state_verified_unchanged": True,
                },
            ]
            states_before = StateSnapshots(
                protected=before_protected,
                disposable=before_arms[arm_name],
                workspace_id=request.preflight.receipt.workspace_id,
            )
            states_after = StateSnapshots(
                protected=after_protected,
                disposable=after_arms[arm_name],
                workspace_id=request.preflight.receipt.workspace_id,
            )
            evidence = EvidenceBundle.from_run(
                request.plan,
                request.preflight.receipt,
                events,
                states_before,
                states_after,
                run_id=request.preflight.receipt.run_nonce,
                execution_id=execution_id,
                source_result_digest=parsed_arm.source_result_digest,
                arm_name=arm_name,
                provider_result=provider_path,
                known_secret_values=secrets,
            )
            _write_json_exclusive(
                evidence_path, _redact(evidence_bundle_payload(evidence), secrets)
            )
            quality_status = _quality_status(parsed_arm)
            supervised_arms.append(SupervisedArmResult(
                arm_name=arm_name,
                provider_result_path=provider_path,
                quality_path=quality_path,
                evidence_path=evidence_path,
                execution_status=evidence.audit.execution_status.value,
                quality_status=quality_status,
                safety_status=evidence.audit.safety_status.value,
                evidence=evidence,
            ))
            trace_payload["arm_events"][arm_name] = events

        trace_path = request.artifact_directory / "host-trace.json"
        _write_json_exclusive(trace_path, _redact(trace_payload, secrets))
        recorder.record("evidence-published", {
            "trace_digest": hashlib.sha256(trace_path.read_bytes()).hexdigest(),
            "arm_evidence_digests": {
                arm.arm_name: evidence_bundle_digest(arm.evidence)
                for arm in supervised_arms
            },
        })
        manifest.update({
            "status": "HOST_AUDIT_COMPLETE",
            "execution_id": execution_id,
            "run_nonce": request.preflight.receipt.run_nonce,
            "provider_result_digest": parsed.source_file_digest,
            "arm_source_result_digests": {
                arm.arm_name: arm.source_result_digest for arm in parsed.arms
            },
            "arm_provider_identities": {
                arm.arm_name: dict(arm.provider_result["provider_identity"])
                for arm in parsed.arms
            },
            "arm_evidence_digests": {
                arm.arm_name: evidence_bundle_digest(arm.evidence)
                for arm in supervised_arms
            },
        })
        native_eval._write_manifest_atomic(bundle / "manifest.json", manifest)
        recorder.record("complete")
    except Exception as exc:
        cleanup_error = None
        try:
            found_link = _cleanup_disposable_workspaces(bundle, arm_paths)
            if found_link:
                cleanup_error = "unexpected-symlink"
        except (OSError, CodexHostError) as cleanup_exc:
            cleanup_error = type(cleanup_exc).__name__
        try:
            recorder.record("incomplete", {
                "error": type(exc).__name__,
                "failure_cleanup": (
                    "PASS" if cleanup_error is None else f"FAIL:{cleanup_error}"
                ),
            })
        except (CodexHostError, OSError, InterruptedError):
            pass
        if isinstance(exc, CodexHostError):
            raise
        raise CodexHostError(
            f"supervised provider execution remained incomplete: {type(exc).__name__}"
        ) from None

    arms_tuple = tuple(supervised_arms)
    execution_status = (
        "COMPLETED" if all(arm.execution_status == "COMPLETED" for arm in arms_tuple)
        else "INCOMPLETE"
    )
    safety_status = (
        "FAIL" if any(arm.safety_status == "FAIL" for arm in arms_tuple)
        else "PASS" if all(arm.safety_status == "PASS" for arm in arms_tuple)
        else "UNKNOWN"
    )
    quality_values = {arm.quality_status for arm in arms_tuple}
    if "FAIL" in quality_values:
        quality_status = "FAIL"
    elif "UNKNOWN" in quality_values:
        quality_status = "UNKNOWN"
    elif "NOT_GRADED" in quality_values:
        quality_status = "NOT_GRADED"
    elif quality_values == {"PASS"}:
        quality_status = "PASS"
    else:
        quality_status = "UNKNOWN"
    return SupervisedRunResult(
        run_id=request.preflight.receipt.run_nonce,
        execution_id=execution_id,
        execution_status=execution_status,
        quality_status=quality_status,
        safety_status=safety_status,
        source_result_digest=parsed.source_file_digest,
        trace_artifact=trace_path,
        arms=arms_tuple,
    )
