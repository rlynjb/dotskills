#!/opt/evaluate/bin/python3
"""Fixed contract entrypoint for the shell-free Codex read-only workload."""

from __future__ import annotations

import json
import importlib.util
from pathlib import Path
import sys
from typing import Any, Mapping, Sequence


class EntrypointError(ValueError):
    """The workload invocation or binding is outside the reviewed contract."""


_ACTIONS = frozenset(("probe", "evaluate"))
_BINDING_PATH = Path("/run/evaluate/binding.json")
_ALLOWED_TOOLS = ("list", "read", "search")
_PROBE_ENTRYPOINT = Path("/opt/evaluate/probe-entrypoint.py")
_ARMS = frozenset(("with-skill", "without-skill"))
_SHELL_META = frozenset(";&|`$<>(){}[]*?~\\\n\r")
_BINDING_FIELDS = frozenset(
    (
        "schema_version",
        "plan_digest",
        "arm",
        "fixture_root",
        "skill_root",
        "gateway_url",
        "run_grant",
        "allowed_tools",
        "limits",
    )
)
_LIMIT_FIELDS = frozenset(("max_read_bytes", "max_results", "max_query_bytes"))


def _canonical_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise EntrypointError(f"{name} must be a non-empty canonical string")
    if any(character in value for character in _SHELL_META):
        raise EntrypointError(f"{name} contains forbidden shell metacharacters")
    return value


def parse_invocation(argv: Sequence[str]) -> tuple[str, Path]:
    if not isinstance(argv, (list, tuple)) or len(argv) != 3:
        raise EntrypointError("invocation must be ACTION --binding PATH")
    action = _canonical_text(argv[0], "action")
    if action not in _ACTIONS:
        raise EntrypointError(f"unsupported action: {action}")
    if argv[1] != "--binding":
        raise EntrypointError("the only accepted option is --binding")
    binding_path = Path(_canonical_text(argv[2], "binding path"))
    if binding_path != _BINDING_PATH:
        raise EntrypointError("binding path must be the fixed read-only mount")
    return action, binding_path


def load_binding(path: Path) -> Mapping[str, Any]:
    if path != _BINDING_PATH or path.is_symlink() or not path.is_file():
        raise EntrypointError("binding must be the fixed regular file")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise EntrypointError(f"binding cannot be loaded: {exc}") from None
    if not isinstance(value, dict) or frozenset(value) != _BINDING_FIELDS:
        raise EntrypointError("binding fields do not match the v0.4 contract")
    if value["schema_version"] != "0.4":
        raise EntrypointError("binding schema is unsupported")
    if value["arm"] not in _ARMS:
        raise EntrypointError("binding arm is unsupported")
    if value["fixture_root"] != "/fixture":
        raise EntrypointError("fixture root must be the fixed read-only mount")
    expected_skill = "/skill" if value["arm"] == "with-skill" else None
    if value["skill_root"] != expected_skill:
        raise EntrypointError("skill root does not match the arm")
    if value["gateway_url"] != "http://provider-gateway:8080/v1/responses":
        raise EntrypointError("gateway URL does not match the internal route")
    _canonical_text(value["plan_digest"], "plan digest")
    _canonical_text(value["run_grant"], "run grant")
    if value["allowed_tools"] != list(_ALLOWED_TOOLS):
        raise EntrypointError("tool surface must be exactly list, read, search")
    limits = value["limits"]
    if not isinstance(limits, dict) or frozenset(limits) != _LIMIT_FIELDS:
        raise EntrypointError("binding limits are incomplete")
    for name, limit in limits.items():
        if isinstance(limit, bool) or not isinstance(limit, int) or limit <= 0:
            raise EntrypointError(f"binding limit {name} must be a positive integer")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    try:
        action, binding_path = parse_invocation(
            tuple(sys.argv[1:] if argv is None else argv)
        )
        binding = load_binding(binding_path)
        if action == "probe":
            if _PROBE_ENTRYPOINT.is_symlink() or not _PROBE_ENTRYPOINT.is_file():
                raise EntrypointError("fixed probe entrypoint is unavailable")
            spec = importlib.util.spec_from_file_location(
                "evaluate_probe_entrypoint", _PROBE_ENTRYPOINT
            )
            if spec is None or spec.loader is None:
                raise EntrypointError("fixed probe entrypoint cannot be loaded")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(json.dumps(module.collect_probe_observations(binding), sort_keys=True))
            return 0
    except EntrypointError as exc:
        print(json.dumps({"status": "BLOCKED_NOT_RUN", "reason": str(exc)}))
        return 2
    print(
        json.dumps(
            {
                "status": "CONTRACT_READY_NOT_RUN",
                "action": action,
                "plan_digest": binding["plan_digest"],
                "allowed_tools": list(_ALLOWED_TOOLS),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
