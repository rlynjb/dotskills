#!/usr/bin/env python3
"""Narrow trusted-host CLI for native Codex preflight and supervised execution."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import stat
import subprocess
from typing import Any, Callable, Mapping, Optional, Sequence, Tuple

from capability_inventory import load_inventory
from codex_host import (
    CodexHostError,
    CodexHostPolicy,
    ExecutableIdentity,
    HostAttestation,
    PreflightRequest,
    PreflightResult,
    SupervisedProcessResult,
    SupervisedRunIncomplete,
    SupervisedRunRequest,
    attest_host,
    compile_read_only_policy,
    run_supervised_provider,
    run_trusted_preflight,
)
from contracts import ApprovalReceipt, EnforcementReceipt, RunPlan
from evidence import StateEntry, StateSnapshot
from native_boundary import NativeBoundaryResult, ProbeResult
import native_eval
from provider_trace import OBSERVER_ID, OBSERVER_VERSION


_VERSION = re.compile(r"(?<!\d)(\d+\.\d+\.\d+)(?!\d)")
_LIVE_AUTH_FIELDS = frozenset((
    "schema_version", "decision", "authorized_by", "issued_at", "expires_at",
    "plan_digest", "run_nonce", "provider", "model_version", "backend",
    "capability_profile", "preflight_receipt_digest",
    "preflight_artifact_digest", "codex_executable_digest",
    "promptfoo_executable_digest", "node_executable_digest",
    "promptfoo_runtime_digest",
    "codex_sdk_digest", "observer_id", "observer_version",
))
_READ_ONLY_PROBE_IDS = tuple(sorted((
    "environment-secret", "network-egress", "read-outside-workspace",
    "secondary-tool-route", "write-inside-workspace", "write-outside-workspace",
)))


def _run_observation(command: Sequence[str], *, home: Optional[Path] = None) -> str:
    binary_directory = str(Path(command[0]).resolve().parent)
    completed = subprocess.run(
        list(command),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=15,
        env={
            "HOME": str(home) if home is not None else os.environ.get("HOME", ""),
            "PATH": binary_directory + os.pathsep + os.defpath,
            "LANG": "C",
            "LC_ALL": "C",
        },
        text=True,
    )
    if completed.returncode != 0:
        raise CodexHostError(f"host observation command exited {completed.returncode}")
    if len(completed.stdout.encode("utf-8")) > 1024 * 1024:
        raise CodexHostError("host observation output exceeded its limit")
    return completed.stdout.strip()


def _default_versions(
    codex_path: Path, promptfoo_path: Path, node_path: Path
) -> Mapping[str, str]:
    result = {}
    commands = (
        ("codex", (str(codex_path), "--version")),
        ("promptfoo", (str(node_path), str(promptfoo_path), "--version")),
        ("node", (str(node_path), "--version")),
    )
    for name, command in commands:
        observed = _run_observation(command)
        match = _VERSION.search(observed)
        if match is None:
            raise CodexHostError(f"cannot parse installed {name} version")
        result[name] = match.group(1)
    return result


def _default_platform() -> Tuple[str, str, str]:
    return (platform.system().lower(), platform.release(), platform.machine().lower())


def _default_login(codex_path: Path, home: Path) -> str:
    return _run_observation((str(codex_path), "login", "status"), home=home)


def _default_mcp_servers(codex_path: Path, home: Path) -> Sequence[str]:
    observed = _run_observation(
        (str(codex_path), "mcp", "list", "--json"), home=home
    )
    try:
        value = json.loads(observed)
    except json.JSONDecodeError:
        raise CodexHostError("Codex MCP inventory is not JSON") from None
    if isinstance(value, dict):
        values = value.get("mcp_servers", value.get("servers"))
    else:
        values = value
    if not isinstance(values, list):
        raise CodexHostError("Codex MCP inventory has an unknown shape")
    names = []
    for item in values:
        name = item.get("name") if isinstance(item, dict) else item
        if not isinstance(name, str) or not name:
            raise CodexHostError("Codex MCP inventory contains an invalid name")
        names.append(name)
    return tuple(names)


@dataclass(frozen=True)
class HostDependencies:
    inspect_versions: Callable[[Path, Path, Path], Mapping[str, str]] = _default_versions
    inspect_platform: Callable[[], Sequence[str]] = _default_platform
    inspect_login: Callable[[Path, Path], str] = _default_login
    inspect_mcp_servers: Callable[[Path, Path], Sequence[str]] = _default_mcp_servers
    inspect_environment: Callable[[], Mapping[str, str]] = lambda: dict(os.environ)
    boundary_runner: Optional[Callable[..., NativeBoundaryResult]] = None
    trusted_process_runner: Optional[Callable[..., SupervisedProcessResult]] = None


def file_digest(path: Path, *, max_bytes: int = 64 * 1024 * 1024) -> str:
    path = Path(path)
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = None
    digest = hashlib.sha256()
    try:
        descriptor = os.open(path, flags)
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > max_bytes:
            raise CodexHostError("trusted host input must be a bounded regular file")
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    except OSError as exc:
        raise CodexHostError(f"cannot hash trusted host input: {type(exc).__name__}") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)
    return digest.hexdigest()


def preflight_artifact_digest(directory: Path) -> str:
    directory = Path(directory)
    records = []
    for name in (
        "host-policy.json", "preflight-snapshots.json", "preflight-probes.json",
        "enforcement-receipt.json",
    ):
        records.append({"name": name, "digest": file_digest(directory / name)})
    return hashlib.sha256(json.dumps(
        records, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")).hexdigest()


def _json_object(path: Path, label: str, *, max_bytes: int = 16 * 1024 * 1024) -> dict[str, Any]:
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
        remaining = max_bytes + 1
        while remaining:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        if len(payload) > max_bytes:
            raise CodexHostError(f"{label} exceeds the size limit")
        value = json.loads(payload.decode("utf-8"))
    except CodexHostError:
        raise
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CodexHostError(f"cannot load {label}: {type(exc).__name__}") from None
    finally:
        if descriptor is not None:
            os.close(descriptor)
    if not isinstance(value, dict):
        raise CodexHostError(f"{label} must contain a JSON object")
    return value


def _approval_payload(path: Path) -> ApprovalReceipt:
    return ApprovalReceipt.from_dict(_json_object(path, "approval receipt"))


def _snapshot(value: Any, label: str) -> StateSnapshot:
    if not isinstance(value, dict) or set(value) != {"root_id", "entries", "digest"}:
        raise CodexHostError(f"{label} snapshot shape is invalid")
    entries_value = value["entries"]
    if not isinstance(entries_value, list):
        raise CodexHostError(f"{label} snapshot entries are invalid")
    entries = []
    for item in entries_value:
        if not isinstance(item, dict) or set(item) != {
            "path", "entry_type", "mode", "content_digest"
        }:
            raise CodexHostError(f"{label} snapshot entry is invalid")
        entries.append(StateEntry(**item))
    return StateSnapshot(value["root_id"], tuple(entries), value["digest"])


def _load_policy(path: Path) -> CodexHostPolicy:
    value = _json_object(path, "host policy")
    expected = {
        "schema_version", "profile_name", "workspace", "workspace_id",
        "codex_path", "codex_executable", "promptfoo_path",
        "promptfoo_executable", "node_path", "node_executable",
        "promptfoo_runtime_root",
        "promptfoo_runtime_digest", "codex_sdk_root", "codex_sdk_digest",
        "command_line_tools_root", "home",
        "home_shape_digest", "protected_roots",
        "disabled_mcp_servers", "cli_config", "boundary_launcher",
        "process_environment",
    }
    if set(value) != expected:
        raise CodexHostError("host policy artifact shape is invalid")
    def executable(field: str) -> ExecutableIdentity:
        item = value[field]
        expected_identity = {"path", "device", "inode", "size", "digest"}
        if not isinstance(item, dict) or set(item) != expected_identity:
            raise CodexHostError(f"host policy {field} shape is invalid")
        return ExecutableIdentity(
            path=Path(item["path"]),
            device=item["device"],
            inode=item["inode"],
            size=item["size"],
            digest=item["digest"],
        )

    return CodexHostPolicy(
        schema_version=value["schema_version"],
        profile_name=value["profile_name"],
        workspace=Path(value["workspace"]),
        workspace_id=value["workspace_id"],
        codex_path=Path(value["codex_path"]),
        codex_executable=executable("codex_executable"),
        promptfoo_path=Path(value["promptfoo_path"]),
        promptfoo_executable=executable("promptfoo_executable"),
        node_path=Path(value["node_path"]),
        node_executable=executable("node_executable"),
        promptfoo_runtime_root=Path(value["promptfoo_runtime_root"]),
        promptfoo_runtime_digest=value["promptfoo_runtime_digest"],
        codex_sdk_root=Path(value["codex_sdk_root"]),
        codex_sdk_digest=value["codex_sdk_digest"],
        command_line_tools_root=Path(value["command_line_tools_root"]),
        home=Path(value["home"]),
        home_shape_digest=value["home_shape_digest"],
        protected_roots=tuple(Path(item) for item in value["protected_roots"]),
        disabled_mcp_servers=tuple(value["disabled_mcp_servers"]),
        cli_config=value["cli_config"],
        boundary_launcher=tuple(value["boundary_launcher"]),
        process_environment=value["process_environment"],
    )


def _load_preflight(directory: Path, plan: RunPlan) -> PreflightResult:
    directory = Path(directory)
    if not directory.is_absolute() or directory.is_symlink() or not directory.is_dir():
        raise CodexHostError("preflight directory must be a real absolute directory")
    directory = directory.resolve()
    policy_path = directory / "host-policy.json"
    snapshot_path = directory / "preflight-snapshots.json"
    probe_path = directory / "preflight-probes.json"
    receipt_path = directory / "enforcement-receipt.json"
    policy = _load_policy(policy_path)
    snapshots = _json_object(snapshot_path, "preflight snapshots")
    probes = _json_object(probe_path, "preflight probes")
    receipt = EnforcementReceipt.from_dict(
        _json_object(receipt_path, "enforcement receipt")
    )
    if (
        snapshots.get("plan_digest") != plan.digest()
        or probes.get("plan_digest") != plan.digest()
        or receipt.plan_digest != plan.digest()
        or snapshots.get("run_nonce") != receipt.run_nonce
        or probes.get("run_nonce") != receipt.run_nonce
        or probes.get("host_policy_digest") != policy.digest()
    ):
        raise CodexHostError("preflight artifacts do not share one plan and nonce binding")
    protected_values = snapshots.get("protected")
    if not isinstance(protected_values, list) or not protected_values:
        raise CodexHostError("preflight protected snapshots are missing")
    protected = tuple(
        _snapshot(value, f"protected[{index}]")
        for index, value in enumerate(protected_values)
    )
    workspace = _snapshot(snapshots.get("workspace"), "workspace")
    attestation_value = snapshots.get("attestation")
    expected_attestation = {
        "schema_version", "platform", "versions", "auth_method",
        "policy_digest", "workspace_id", "disabled_mcp_servers",
        "codex_executable_digest", "promptfoo_executable_digest",
        "node_executable_digest", "promptfoo_runtime_digest",
        "codex_sdk_digest", "home_shape_digest",
    }
    if not isinstance(attestation_value, dict) or set(attestation_value) != expected_attestation:
        raise CodexHostError("stored host attestation shape is invalid")
    try:
        attestation = HostAttestation(
            schema_version=attestation_value["schema_version"],
            platform=tuple(attestation_value["platform"]),
            versions=attestation_value["versions"],
            auth_method=attestation_value["auth_method"],
            policy_digest=attestation_value["policy_digest"],
            workspace_id=attestation_value["workspace_id"],
            disabled_mcp_servers=tuple(attestation_value["disabled_mcp_servers"]),
            codex_executable_digest=attestation_value["codex_executable_digest"],
            promptfoo_executable_digest=attestation_value["promptfoo_executable_digest"],
            node_executable_digest=attestation_value["node_executable_digest"],
            promptfoo_runtime_digest=attestation_value["promptfoo_runtime_digest"],
            codex_sdk_digest=attestation_value["codex_sdk_digest"],
            home_shape_digest=attestation_value["home_shape_digest"],
        )
    except (TypeError, ValueError):
        raise CodexHostError("stored host attestation is invalid") from None
    if attestation.policy_digest != policy.digest():
        raise CodexHostError("stored host attestation policy binding changed")
    result_values = probes.get("results")
    if not isinstance(result_values, list):
        raise CodexHostError("preflight probe results are missing")
    try:
        results = tuple(ProbeResult(**value) for value in result_values)
    except (TypeError, ValueError):
        raise CodexHostError("preflight probe result shape is invalid") from None
    if tuple(sorted(item.probe_id for item in results)) != _READ_ONLY_PROBE_IDS:
        raise CodexHostError("stored preflight does not contain the exact six probes")
    boundary = NativeBoundaryResult(
        plan_digest=plan.digest(),
        provider_config_digest=probes.get("boundary_config_digest"),
        required_probe_ids=_READ_ONLY_PROBE_IDS,
        results=results,
        unsupported_surfaces=(),
    )
    if not boundary.complete:
        raise CodexHostError("stored preflight boundary evidence is incomplete")
    return PreflightResult(
        receipt=receipt,
        boundary=boundary,
        attestation=attestation,
        policy_digest=policy.digest(),
        bundle_digest=receipt.prepared_bundle_digest,
        provider_config_digest=receipt.provider_config_digest,
        protected_snapshots=protected,
        workspace_snapshot=workspace,
        policy_artifact=policy_path,
        snapshot_artifact=snapshot_path,
        probe_artifact=probe_path,
        receipt_artifact=receipt_path,
    )


def _timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise CodexHostError(f"{label} timestamp is required")
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise CodexHostError(f"{label} timestamp is invalid") from None
    if result.tzinfo is None or result.utcoffset() is None:
        raise CodexHostError(f"{label} timestamp must include a timezone")
    return result.astimezone(timezone.utc)


def _validate_live_authorization(
    path: Path, plan: RunPlan, preflight: PreflightResult
) -> Mapping[str, Any]:
    value = _json_object(path, "live authorization")
    if set(value) != _LIVE_AUTH_FIELDS:
        raise CodexHostError("live authorization shape is not exact")
    now = datetime.now(timezone.utc)
    issued = _timestamp(value["issued_at"], "live authorization issued_at")
    expires = _timestamp(value["expires_at"], "live authorization expires_at")
    if issued > now or now >= expires or expires - issued > timedelta(hours=2):
        raise CodexHostError("live authorization is not currently valid")
    expected = {
        "schema_version": "0.3",
        "decision": "APPROVED_LIVE_RUN",
        "plan_digest": plan.digest(),
        "run_nonce": preflight.receipt.run_nonce,
        "provider": plan.provider,
        "model_version": plan.model_version,
        "backend": "native",
        "capability_profile": "read-only",
        "preflight_receipt_digest": file_digest(preflight.receipt_artifact),
        "preflight_artifact_digest": preflight_artifact_digest(
            preflight.receipt_artifact.parent
        ),
        "codex_executable_digest": preflight.attestation.codex_executable_digest,
        "promptfoo_executable_digest": (
            preflight.attestation.promptfoo_executable_digest
        ),
        "node_executable_digest": preflight.attestation.node_executable_digest,
        "promptfoo_runtime_digest": preflight.attestation.promptfoo_runtime_digest,
        "codex_sdk_digest": preflight.attestation.codex_sdk_digest,
        "observer_id": OBSERVER_ID,
        "observer_version": OBSERVER_VERSION,
    }
    for field, expected_value in expected.items():
        if value.get(field) != expected_value:
            raise CodexHostError(f"live authorization {field} does not match")
    if not isinstance(value.get("authorized_by"), str) or not value["authorized_by"].strip():
        raise CodexHostError("live authorization signer is missing")
    return value


def _real_explicit_path(path: Path, label: str, *, directory: bool) -> Path:
    path = Path(path)
    if not path.is_absolute() or path.is_symlink():
        raise CodexHostError(f"{label} must be an explicit real absolute path")
    if directory and not path.is_dir():
        raise CodexHostError(f"{label} must be an existing directory")
    if not directory and not path.is_file():
        raise CodexHostError(f"{label} must be an existing file")
    return path.resolve()


def _preflight(args: argparse.Namespace, dependencies: HostDependencies) -> dict[str, Any]:
    plan = RunPlan.from_dict(_json_object(args.run_plan, "run plan"))
    if plan.backend != "native" or plan.capabilities.profile != "read-only":
        raise CodexHostError("trusted host supports only native read-only Codex runs")
    approval = _approval_payload(args.approval_receipt)
    inventory = load_inventory(args.capability_inventory)
    codex_path = _real_explicit_path(args.codex_path, "codex path", directory=False)
    promptfoo_path = _real_explicit_path(
        args.promptfoo_path, "Promptfoo path", directory=False
    )
    node_path = _real_explicit_path(args.node_path, "Node path", directory=False)
    promptfoo_runtime_root = _real_explicit_path(
        args.promptfoo_runtime_root, "Promptfoo runtime root", directory=True
    )
    codex_sdk_root = _real_explicit_path(
        args.codex_sdk_root, "Codex SDK root", directory=True
    )
    protected = tuple(
        _real_explicit_path(path, "protected root", directory=True)
        for path in args.protected_root
    )
    home = _real_explicit_path(args.home, "home", directory=True)
    observed_mcp = tuple(dependencies.inspect_mcp_servers(codex_path, home))
    policy = compile_read_only_policy(
        workspace=args.bundle,
        codex_path=codex_path,
        promptfoo_path=promptfoo_path,
        node_path=node_path,
        promptfoo_runtime_root=promptfoo_runtime_root,
        codex_sdk_root=codex_sdk_root,
        command_line_tools_root=args.command_line_tools_root,
        home=home,
        mcp_servers=observed_mcp,
        protected_roots=protected,
    )
    observed_versions = dependencies.inspect_versions(
        codex_path, promptfoo_path, node_path
    )
    attestation = attest_host(
        policy,
        expected_platform=(
            inventory.platform.system,
            inventory.platform.release,
            inventory.platform.machine,
        ),
        observed_platform=dependencies.inspect_platform(),
        expected_versions={
            "codex": inventory.required_versions["codex"],
            "promptfoo": inventory.required_versions["promptfoo"],
            "node": inventory.required_versions["node"],
        },
        observed_versions=observed_versions,
        login_status=dependencies.inspect_login(codex_path, home),
        observed_mcp_servers=observed_mcp,
        environment=dependencies.inspect_environment(),
    )
    request = PreflightRequest(
        plan=plan,
        approval=approval,
        inventory=inventory,
        policy=policy,
        attestation=attestation,
        bundle=args.bundle,
        provider_config=_json_object(args.provider_config, "boundary provider config"),
        artifact_directory=args.artifact_directory,
        issued_at=args.issued_at,
        expires_at=args.expires_at,
        verifier_version=args.verifier_version,
    )
    result = run_trusted_preflight(
        request,
        boundary_runner=dependencies.boundary_runner,
    )
    return {
        "status": "READY_NOT_RUN",
        "model_executed": False,
        "plan_digest": plan.digest(),
        "run_nonce": result.receipt.run_nonce,
        "policy_digest": result.policy_digest,
        "receipt": str(result.receipt_artifact),
        "preflight_artifact_digest": preflight_artifact_digest(
            result.receipt_artifact.parent
        ),
    }


def _run(args: argparse.Namespace, dependencies: HostDependencies) -> dict[str, Any]:
    if dependencies.trusted_process_runner is None:
        raise CodexHostError(
            "trusted provider process and independent session observer are unavailable"
        )
    plan = RunPlan.from_dict(_json_object(args.run_plan, "run plan"))
    preflight = _load_preflight(args.preflight_directory, plan)
    policy = _load_policy(preflight.policy_artifact)
    artifacts = _real_explicit_path(
        args.artifact_directory, "artifact directory", directory=True
    )
    if artifacts != Path(args.preflight_directory).resolve():
        raise CodexHostError("run artifact directory must equal its preflight directory")
    protected = tuple(
        _real_explicit_path(path, "protected root", directory=True)
        for path in args.protected_root
    )
    if protected != policy.protected_roots:
        raise CodexHostError("explicit protected roots differ from the preflight policy")
    live_authorization = _validate_live_authorization(
        args.live_authorization, plan, preflight
    )
    bundle = _real_explicit_path(args.bundle, "bound bundle", directory=True)
    manifest = _json_object(bundle / "manifest.json", "bound bundle manifest")
    command = tuple(native_eval.native_command(bundle, manifest))
    promptfoo_path = _real_explicit_path(
        args.promptfoo_path, "Promptfoo path", directory=False
    )
    if promptfoo_path != policy.promptfoo_path:
        raise CodexHostError("run Promptfoo path differs from the preflight policy")
    node_path = _real_explicit_path(args.node_path, "Node path", directory=False)
    if node_path != policy.node_path:
        raise CodexHostError("run Node path differs from the preflight policy")
    command = (
        str(policy.node_path), str(policy.promptfoo_path), *command[1:]
    )
    current_attestation = attest_host(
        policy,
        expected_platform=preflight.attestation.platform,
        observed_platform=dependencies.inspect_platform(),
        expected_versions=preflight.attestation.versions,
        observed_versions=dependencies.inspect_versions(
            policy.codex_path, policy.promptfoo_path, policy.node_path
        ),
        login_status=dependencies.inspect_login(policy.codex_path, policy.home),
        observed_mcp_servers=dependencies.inspect_mcp_servers(
            policy.codex_path, policy.home
        ),
        environment=dependencies.inspect_environment(),
    )
    if current_attestation.canonical_payload() != preflight.attestation.canonical_payload():
        raise CodexHostError("host attestation changed after preflight")
    request = SupervisedRunRequest(
        plan=plan,
        policy=policy,
        preflight=preflight,
        bundle=bundle,
        command=command,
        nonce_ledger=args.nonce_ledger,
        artifact_directory=artifacts,
        live_authorization_expires_at=live_authorization["expires_at"],
        observer_id=live_authorization["observer_id"],
        observer_version=live_authorization["observer_version"],
    )
    result = run_supervised_provider(
        request, process_runner=dependencies.trusted_process_runner
    )
    return {
        "status": result.execution_status,
        "model_executed": True,
        "run_id": result.run_id,
        "execution_id": result.execution_id,
        "execution_status": result.execution_status,
        "quality_status": result.quality_status,
        "safety_status": result.safety_status,
        "trace": str(result.trace_artifact),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)
    preflight = subparsers.add_parser("preflight")
    for name in ("run_plan", "approval_receipt", "capability_inventory", "bundle",
                 "artifact_directory", "codex_path", "promptfoo_path",
                 "node_path", "promptfoo_runtime_root", "codex_sdk_root",
                 "command_line_tools_root", "home", "provider_config"):
        preflight.add_argument(f"--{name.replace('_', '-')}", type=Path, required=True)
    preflight.add_argument("--protected-root", type=Path, action="append", required=True)
    preflight.add_argument("--issued-at", required=True)
    preflight.add_argument("--expires-at", required=True)
    preflight.add_argument("--verifier-version", required=True)

    run = subparsers.add_parser("run")
    for name in ("run_plan", "bundle", "preflight_directory", "artifact_directory",
                 "promptfoo_path", "node_path", "nonce_ledger",
                 "live_authorization"):
        run.add_argument(f"--{name.replace('_', '-')}", type=Path, required=True)
    run.add_argument("--protected-root", type=Path, action="append", required=True)
    return parser


def _redacted_message(exc: BaseException, dependencies: HostDependencies) -> str:
    message = str(exc) or type(exc).__name__
    try:
        environment = dependencies.inspect_environment()
    except Exception:
        environment = {}
    secrets = sorted(
        {
            value for value in environment.values()
            if isinstance(value, str) and value
        },
        key=len,
        reverse=True,
    )
    for secret in secrets:
        message = message.replace(secret, "[REDACTED]")
    return message


def main(argv: Optional[Sequence[str]] = None, *, dependencies: HostDependencies = HostDependencies()) -> int:
    try:
        args = _parser().parse_args(argv)
    except SystemExit:
        print(json.dumps({
            "status": "BLOCKED_NOT_RUN",
            "model_executed": False,
            "reason": "explicit required CLI input is missing or invalid",
        }, sort_keys=True))
        return 2
    try:
        payload = _preflight(args, dependencies) if args.action == "preflight" else _run(
            args, dependencies
        )
        print(json.dumps(payload, sort_keys=True))
        return 0
    except SupervisedRunIncomplete as exc:
        print(json.dumps({
            "status": "INCOMPLETE",
            "execution_status": exc.execution_status,
            "safety_status": exc.safety_status,
            "model_executed": exc.model_executed,
            "reason": _redacted_message(exc, dependencies),
        }, sort_keys=True))
        return 2
    except Exception as exc:
        print(json.dumps({
            "status": "BLOCKED_NOT_RUN",
            "model_executed": False,
            "reason": _redacted_message(exc, dependencies),
        }, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
