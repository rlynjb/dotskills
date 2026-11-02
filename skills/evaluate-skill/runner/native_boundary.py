"""Host-owned negative probes for a provider-native execution boundary."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Mapping, Tuple

from contracts import EnforcementReceipt, RunPlan


class BoundaryError(ValueError):
    """A native boundary or its probe evidence is incomplete or inconsistent."""


_CONFIG_FIELDS = frozenset(
    (
        "provider",
        "provider_version",
        "adapter",
        "adapter_version",
        "backend",
        "profile",
        "sandbox_mode",
        "boundary_launcher",
        "outside_read_path",
        "outside_write_path",
        "network_host",
        "network_port",
        "secret_names",
        "forbidden_commands",
        "connectors_enabled",
        "mcp_servers",
    )
)
_OBSERVATIONS = frozenset(
    ("denied", "absent", "unavailable", "blocked", "allowed", "present", "error")
)
_STATUSES = frozenset(("PASS", "FAIL", "UNKNOWN"))
_PROBE_ROOT = Path(__file__).with_name("probes")
_PROBES = {
    "environment-secret": ("credentials", "environment_secret.py"),
    "network-egress": ("network", "network_egress.py"),
    "read-outside-workspace": ("filesystem_read", "read_outside_workspace.py"),
    "secondary-tool-route": ("shell", "secondary_tool_route.py"),
    "write-outside-workspace": ("filesystem_write", "write_outside_workspace.py"),
}
_PROFILE_PROBES = {
    "no-tool": tuple(sorted(_PROBES)),
    "read-only": tuple(sorted(_PROBES)),
    "disposable-write": tuple(sorted(_PROBES)),
    "mock-external": tuple(sorted(_PROBES)),
}


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise BoundaryError(f"{name} must be an object")
    if not all(isinstance(key, str) for key in value):
        raise BoundaryError(f"{name} field names must be strings")
    return value


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BoundaryError(f"{name} must be a non-empty string")
    return value


def _strings(value: Any, name: str, *, nonempty: bool = False) -> Tuple[str, ...]:
    if not isinstance(value, (list, tuple)):
        raise BoundaryError(f"{name} must be an array")
    result = tuple(_text(item, f"{name} item") for item in value)
    if nonempty and not result:
        raise BoundaryError(f"{name} must not be empty")
    if len(result) != len(set(result)):
        raise BoundaryError(f"{name} must not contain duplicates")
    return result


def _normalized_config(value: Mapping[str, Any]) -> dict[str, Any]:
    value = _mapping(value, "provider config")
    actual = frozenset(value)
    missing = sorted(_CONFIG_FIELDS - actual)
    unknown = sorted(actual - _CONFIG_FIELDS)
    if missing:
        raise BoundaryError(f"provider config missing fields: {', '.join(missing)}")
    if unknown:
        raise BoundaryError(f"provider config unknown fields: {', '.join(unknown)}")
    port = value["network_port"]
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise BoundaryError("provider config network_port must be an integer from 1 to 65535")
    read_path = Path(_text(value["outside_read_path"], "outside_read_path"))
    write_path = Path(_text(value["outside_write_path"], "outside_write_path"))
    if not read_path.is_absolute() or not write_path.is_absolute():
        raise BoundaryError("outside probe paths must be absolute")
    return {
        "provider": _text(value["provider"], "provider"),
        "provider_version": _text(value["provider_version"], "provider_version"),
        "adapter": _text(value["adapter"], "adapter"),
        "adapter_version": _text(value["adapter_version"], "adapter_version"),
        "backend": _text(value["backend"], "backend"),
        "profile": _text(value["profile"], "profile"),
        "sandbox_mode": _text(value["sandbox_mode"], "sandbox_mode"),
        "boundary_launcher": list(
            _strings(value["boundary_launcher"], "boundary_launcher", nonempty=True)
        ),
        "outside_read_path": str(read_path),
        "outside_write_path": str(write_path),
        "network_host": _text(value["network_host"], "network_host"),
        "network_port": port,
        "secret_names": list(_strings(value["secret_names"], "secret_names", nonempty=True)),
        "forbidden_commands": list(
            _strings(value["forbidden_commands"], "forbidden_commands", nonempty=True)
        ),
        "connectors_enabled": list(_strings(value["connectors_enabled"], "connectors_enabled")),
        "mcp_servers": list(_strings(value["mcp_servers"], "mcp_servers")),
    }


def provider_config_digest(value: Mapping[str, Any]) -> str:
    payload = json.dumps(
        _normalized_config(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class ProbeResult:
    probe_id: str
    capability: str
    status: str
    observation: str
    provider_config_digest: str


@dataclass(frozen=True)
class NativeBoundaryResult:
    plan_digest: str
    provider_config_digest: str
    required_probe_ids: Tuple[str, ...]
    results: Tuple[ProbeResult, ...]
    unsupported_surfaces: Tuple[str, ...]

    @property
    def complete(self) -> bool:
        result_ids = tuple(item.probe_id for item in self.results)
        return (
            not self.unsupported_surfaces
            and len(result_ids) == len(set(result_ids))
            and set(result_ids) == set(self.required_probe_ids)
            and all(item.status == "PASS" for item in self.results)
            and all(
                item.provider_config_digest == self.provider_config_digest
                for item in self.results
            )
        )

    def is_valid_for(self, plan: RunPlan, provider_config: Mapping[str, Any]) -> bool:
        try:
            config_digest = provider_config_digest(provider_config)
        except BoundaryError:
            return False
        return self.plan_digest == plan.digest() and self.provider_config_digest == config_digest

    def to_enforcement_receipt(
        self,
        plan: RunPlan,
        provider_config: Mapping[str, Any],
        *,
        verified_by: str,
        verifier_version: str,
        backend_version: str,
        workspace_id: str,
        enabled_tools: Tuple[str, ...],
        disabled_tools: Tuple[str, ...],
        state_verification_method: str,
        cleanup_method: str,
    ) -> EnforcementReceipt:
        if not self.is_valid_for(plan, provider_config):
            raise BoundaryError("probe result does not match the plan and provider config")
        if not self.complete:
            raise BoundaryError("complete successful probe evidence is required")
        return EnforcementReceipt.from_dict(
            {
                "schema_version": plan.schema_version,
                "plan_digest": plan.digest(),
                "verified_by": verified_by,
                "verifier_version": verifier_version,
                "provider": plan.provider,
                "provider_version": plan.provider_version,
                "model": plan.model,
                "model_version": plan.model_version,
                "adapter": plan.adapter,
                "adapter_version": plan.adapter_version,
                "backend": plan.backend,
                "backend_version": backend_version,
                "capability_profile": plan.capabilities.profile,
                "effective_policy_digest": plan.capabilities.digest(),
                "workspace_id": workspace_id,
                "probe_results": {item.probe_id: item.status for item in self.results},
                "enabled_tools": list(enabled_tools),
                "disabled_tools": list(disabled_tools),
                "state_verification_method": state_verification_method,
                "cleanup_method": cleanup_method,
            }
        )


def _probe_args(probe_id: str, config: Mapping[str, Any]) -> list[str]:
    if probe_id == "read-outside-workspace":
        return ["--path", config["outside_read_path"]]
    if probe_id == "write-outside-workspace":
        return ["--path", config["outside_write_path"]]
    if probe_id == "network-egress":
        return ["--host", config["network_host"], "--port", str(config["network_port"])]
    if probe_id == "environment-secret":
        result = []
        for name in config["secret_names"]:
            result.extend(("--name", name))
        return result
    if probe_id == "secondary-tool-route":
        result = []
        for command in config["forbidden_commands"]:
            result.extend(("--command", command))
        return result
    raise BoundaryError(f"unknown probe id: {probe_id}")


def _sanitize_observation(value: Any) -> str:
    if isinstance(value, str) and value in _OBSERVATIONS:
        return value
    return "redacted"


def _run_probe(
    probe_id: str,
    workspace: Path,
    config: Mapping[str, Any],
    config_digest: str,
) -> ProbeResult:
    capability, filename = _PROBES[probe_id]
    raw_script = _PROBE_ROOT / filename
    if _PROBE_ROOT.is_symlink() or raw_script.is_symlink():
        raise BoundaryError(f"immutable probe unavailable: {probe_id}")
    script = raw_script.resolve()
    if not script.is_file() or not script.is_relative_to(_PROBE_ROOT.resolve()):
        raise BoundaryError(f"immutable probe unavailable: {probe_id}")
    command = [
        *config["boundary_launcher"],
        sys.executable,
        str(script),
        *_probe_args(probe_id, config),
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=workspace,
            env={"PATH": os.defpath, "PYTHONIOENCODING": "utf-8"},
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
            shell=False,
        )
        payload = json.loads(completed.stdout) if completed.returncode == 0 else {}
        status = payload.get("status") if isinstance(payload, dict) else None
        if status not in _STATUSES:
            status = "UNKNOWN"
        observation = _sanitize_observation(
            payload.get("observation") if isinstance(payload, dict) else None
        )
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        status = "UNKNOWN"
        observation = "error"
    return ProbeResult(
        probe_id=probe_id,
        capability=capability,
        status=status,
        observation=observation,
        provider_config_digest=config_digest,
    )


def run_native_preflight(
    plan: RunPlan, workspace: Path, provider_config: Mapping[str, Any]
) -> NativeBoundaryResult:
    """Run immutable probes through a trusted native-boundary launcher."""
    if not isinstance(plan, RunPlan) or plan.backend != "native":
        raise BoundaryError("a native RunPlan is required")
    workspace = Path(workspace)
    if not workspace.is_dir() or workspace.is_symlink():
        raise BoundaryError("a real disposable workspace directory is required")
    config = _normalized_config(provider_config)
    expected = {
        "provider": plan.provider,
        "provider_version": plan.provider_version,
        "adapter": plan.adapter,
        "adapter_version": plan.adapter_version,
        "backend": plan.backend,
        "profile": plan.capabilities.profile,
    }
    for field, value in expected.items():
        if config[field] != value:
            raise BoundaryError(f"provider config {field} does not match run plan")
    resolved_workspace = workspace.resolve()
    for field in ("outside_read_path", "outside_write_path"):
        if Path(config[field]).resolve().is_relative_to(resolved_workspace):
            raise BoundaryError(f"{field} must be outside the disposable workspace")
    config_digest = provider_config_digest(config)
    required = _PROFILE_PROBES[plan.capabilities.profile]
    gaps = []
    if config["connectors_enabled"]:
        gaps.append("connector-isolation-unprobed")
    if config["mcp_servers"]:
        gaps.append("mcp-isolation-unprobed")
    results = tuple(
        _run_probe(probe_id, workspace, config, config_digest)
        for probe_id in required
    )
    return NativeBoundaryResult(
        plan_digest=plan.digest(),
        provider_config_digest=config_digest,
        required_probe_ids=required,
        results=results,
        unsupported_surfaces=tuple(gaps),
    )
