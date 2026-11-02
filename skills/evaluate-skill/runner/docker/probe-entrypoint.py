#!/opt/evaluate/bin/python3
"""Fixed no-model observations for the Docker read-only boundary probe."""

from __future__ import annotations

import json
import hashlib
import os
from pathlib import Path
import socket
import sys
from typing import Any, Mapping, Sequence


class ProbeEntrypointError(ValueError):
    pass


_BINDING_PATH = Path("/run/evaluate/binding.json")
_TOOLS = ("list", "read", "search")
_FORBIDDEN_PATHS = {
    "host_home": Path("/host/home"),
    "original_repo": Path("/host/repository"),
    "provider_auth": Path("/run/secrets/provider-auth"),
    "rubric": Path("/rubric"),
    "docker_socket": Path("/var/run/docker.sock"),
    "outside_mount": Path("/outside"),
}
_NETWORK_TARGETS = {
    "direct_egress": ("1.1.1.1", 443),
    "host_service": ("host.docker.internal", 80),
    "metadata": ("169.254.169.254", 80),
    "unapproved_sidecar": ("unapproved-sidecar", 8080),
}
_APPROVED_EXECUTABLES = (
    "/opt/evaluate/bin/python3",
    "/opt/evaluate/bin/node",
    "/opt/evaluate/bin/codex",
    "/opt/evaluate/bin/promptfoo",
)
_FORBIDDEN_EXECUTABLES = (
    "/bin/sh",
    "/bin/bash",
    "/usr/bin/env",
    "/usr/bin/curl",
    "/usr/bin/wget",
)


def parse_invocation(argv: Sequence[str]) -> Path:
    if tuple(argv) != ("--binding", str(_BINDING_PATH)):
        raise ProbeEntrypointError("probe invocation must use the fixed binding")
    return _BINDING_PATH


def authorize_tool(tool: str, requested_path: str) -> str:
    if tool not in _TOOLS or not isinstance(requested_path, str):
        return "DENIED"
    path = Path(requested_path)
    if not path.is_absolute() or ".." in path.parts:
        return "DENIED"
    try:
        path.relative_to(Path("/fixture"))
    except ValueError:
        return "DENIED"
    current = Path("/")
    for part in path.parts[1:]:
        current /= part
        if current.is_symlink():
            return "DENIED"
    return "ALLOWED"


def _denied_path(path: Path) -> str:
    try:
        path.lstat()
    except OSError:
        return "DENIED"
    return "ALLOWED"


def _denied_write(path: Path) -> str:
    descriptor = None
    try:
        descriptor = os.open(
            path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
            0o600,
        )
    except OSError:
        return "DENIED"
    finally:
        if descriptor is not None:
            os.close(descriptor)
    try:
        path.unlink()
    except OSError:
        pass
    return "ALLOWED"


def _denied_network(target: tuple[str, int]) -> str:
    try:
        connection = socket.create_connection(target, timeout=0.25)
    except OSError:
        return "DENIED"
    try:
        connection.close()
    finally:
        return "ALLOWED"


def _process_status() -> dict[str, Any]:
    values = {
        "no_new_privileges": False,
        "seccomp": "UNKNOWN",
        "effective_capabilities": "UNKNOWN",
    }
    try:
        for line in Path("/proc/self/status").read_text(encoding="utf-8").splitlines():
            if line.startswith("NoNewPrivs:"):
                values["no_new_privileges"] = line.split(":", 1)[1].strip() == "1"
            elif line.startswith("Seccomp:"):
                values["seccomp"] = (
                    "FILTERED" if line.split(":", 1)[1].strip() == "2" else "UNFILTERED"
                )
            elif line.startswith("CapEff:"):
                raw = line.split(":", 1)[1].strip()
                values["effective_capabilities"] = str(int(raw, 16))
    except (OSError, ValueError):
        pass
    return values


def collect_probe_observations(binding: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(binding, Mapping) or binding.get("schema_version") != "0.4":
        raise ProbeEntrypointError("a v0.4 workload binding is required")
    plan_digest = binding.get("plan_digest")
    if not isinstance(plan_digest, str) or len(plan_digest) != 64:
        raise ProbeEntrypointError("binding plan digest is malformed")
    run_grant = binding.get("run_grant")
    if not isinstance(run_grant, str) or not run_grant:
        raise ProbeEntrypointError("binding run grant is malformed")
    write_nonce = hashlib.sha256(run_grant.encode("utf-8")).hexdigest()[:16]
    runtime = {
        "uid": os.getuid(),
        "gid": os.getgid(),
        "host_namespaces": False,
        **_process_status(),
    }
    return {
        "schema_version": "0.4",
        "status": "OBSERVED",
        "plan_digest": plan_digest,
        "observations": {
            "forbidden_paths": {
                name: _denied_path(path) for name, path in _FORBIDDEN_PATHS.items()
            },
            "writes": {
                "root": _denied_write(
                    Path("/.evaluate-root-write-canary-" + write_nonce)
                ),
                "fixture": _denied_write(
                    Path("/fixture/.evaluate-write-canary-" + write_nonce)
                ),
            },
            "network": {
                name: _denied_network(target)
                for name, target in _NETWORK_TARGETS.items()
            },
            "runtime": runtime,
            "inventory": {
                "executables": [
                    path for path in _APPROVED_EXECUTABLES if Path(path).is_file()
                ],
                "processes": ["/opt/evaluate/bin/python3"],
                "forbidden_executables": [
                    path for path in _FORBIDDEN_EXECUTABLES if Path(path).exists()
                ],
            },
            "tools": {
                "allowed_tools": list(_TOOLS),
                "bounded": True,
                "decisions": [
                    ["list", "/fixture", authorize_tool("list", "/fixture")],
                    [
                        "read",
                        "/fixture/sample.txt",
                        authorize_tool("read", "/fixture/sample.txt"),
                    ],
                    ["search", "/fixture", authorize_tool("search", "/fixture")],
                    ["read", "/etc/passwd", authorize_tool("read", "/etc/passwd")],
                    [
                        "read",
                        "/fixture-link",
                        authorize_tool("read", "/fixture-link"),
                    ],
                ],
            },
        },
    }


def _load_binding(path: Path) -> Mapping[str, Any]:
    if path != _BINDING_PATH or path.is_symlink() or not path.is_file():
        raise ProbeEntrypointError("probe binding must be the fixed regular file")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProbeEntrypointError(f"probe binding cannot be loaded: {type(exc).__name__}") from None
    if not isinstance(value, dict):
        raise ProbeEntrypointError("probe binding must be an object")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    try:
        binding_path = parse_invocation(tuple(sys.argv[1:] if argv is None else argv))
        payload = collect_probe_observations(_load_binding(binding_path))
    except ProbeEntrypointError as exc:
        print(json.dumps({"schema_version": "0.4", "status": "UNKNOWN", "reason": str(exc)}))
        return 2
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
