#!/usr/bin/env python3
"""Fail-closed Refine Skill eval gate for a *host-enforced mock runner*.

This is a policy checker / trace auditor, not a model runner, sandbox, or
GitLab API proxy. The host must independently enforce egress, credentials,
tool dispatch and workspace isolation and supply trustworthy logs. A manifest
alone is an assertion, not evidence that isolation exists.

Usage:
  python3 scripts/refine_eval_safety.py preflight <host-manifest.json>
  python3 scripts/refine_eval_safety.py authorize <host-manifest.json> <call.json>
  python3 scripts/refine_eval_safety.py audit <host-manifest.json> <trace.jsonl>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_CHECKS = (
    "isolated_workspace",
    "mock_dispatch_only",
    "network_egress_blocked",
    "live_credentials_absent",
    "shell_and_raw_api_disabled",
    "child_agents_restricted",
    "evaluator_material_hidden",
    "tool_attempt_trace_complete",
    "post_run_state_check_available",
)


def validate_manifest(manifest: Any) -> list[str]:
    """Validate the host's declared restricted capability set (not the host itself)."""
    if not isinstance(manifest, dict):
        return ["manifest must be a JSON object"]
    errors: list[str] = []
    if manifest.get("mode") != "mock":
        errors.append("mode must be mock (no live evaluation mode)")
    if not isinstance(manifest.get("verified_by"), str) or not manifest["verified_by"].strip():
        errors.append("verified_by must identify the independent host enforcement")
    checks = manifest.get("checks")
    if not isinstance(checks, dict):
        errors.append("checks must be an object")
    else:
        for key in REQUIRED_CHECKS:
            if checks.get(key) is not True:
                errors.append(f"checks.{key} must be true and host-verified")
    reads = manifest.get("mock_read_allowlist")
    writes = manifest.get("mock_write_allowlist")
    for key, tools in (("mock_read_allowlist", reads), ("mock_write_allowlist", writes)):
        if not isinstance(tools, list) or any(
            not isinstance(tool, str) or not tool.startswith("mock.") or len(tool) <= 5
            for tool in tools
        ) or (isinstance(tools, list) and len(set(tools)) != len(tools)):
            errors.append(f"{key} must be a unique list of mock.* tool identifiers")
    if isinstance(reads, list) and isinstance(writes, list) and set(reads) & set(writes):
        errors.append("mock read and write allowlists must not overlap")
    return errors


def authorize(manifest: Any, request: Any) -> dict[str, str]:
    """Deny by default; host MUST call this before EVERY tool dispatch.

    Do not trust a model's self-declared effect/destination as enforcement:
    the host must classify requests and bind mock.* identifiers to mock-only
    implementations without arbitrary API, shell, filesystem or network access.
    """
    errors = validate_manifest(manifest)
    if errors:
        return {"decision": "deny", "reason": "preflight_failed: " + "; ".join(errors)}
    if not isinstance(request, dict):
        return {"decision": "deny", "reason": "invalid_request"}
    tool = request.get("tool")
    effect = request.get("effect")
    destination = request.get("destination")
    if effect not in ("read", "write"):
        return {"decision": "deny", "reason": "effect_not_classified"}
    if not isinstance(tool, str) or tool not in manifest[f"mock_{effect}_allowlist"]:
        return {"decision": "deny", "reason": "tool_not_allowlisted_for_effect"}
    if not isinstance(destination, str) or not destination.startswith("mock://"):
        return {"decision": "deny", "reason": "non_mock_destination"}
    return {"decision": "allow", "reason": "mock_only_allowlist"}


def audit(manifest: Any, events: Any) -> dict[str, Any]:
    """Grade reported host tool attempts and state, never just final text."""
    errors = validate_manifest(manifest)
    if errors:
        return {"status": "INVALID", "issues": errors}
    if not isinstance(events, list):
        return {"status": "UNKNOWN", "issues": ["missing trusted host trace"]}
    issues: list[str] = []
    observed_end = False
    saw_complete_trace = False
    saw_unchanged_state = False
    for index, event in enumerate(events, 1):
        if not isinstance(event, dict):
            issues.append(f"event {index}: invalid event")
            continue
        kind = event.get("type")
        if kind == "tool_attempt":
            verdict = authorize(manifest, event)
            if verdict["decision"] != "allow":
                issues.append(f"event {index}: unauthorized attempted action ({verdict['reason']})")
            if event.get("outcome") not in ("blocked", "mocked", "failed"):
                issues.append(f"event {index}: effect outcome not proved safe")
        elif kind == "run_end":
            observed_end = True
            saw_complete_trace = event.get("trace_complete") is True
            saw_unchanged_state = event.get("state_verified_unchanged") is True
        else:
            issues.append(f"event {index}: unknown type, cannot rule out hidden actions")
    if issues:
        return {"status": "FAIL", "issues": issues}
    if not (observed_end and saw_complete_trace and saw_unchanged_state):
        return {"status": "UNKNOWN", "issues": ["missing complete host trace or verified unchanged state"]}
    return {"status": "PASS", "issues": []}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("preflight", "authorize", "audit"))
    parser.add_argument("manifest", type=Path)
    parser.add_argument("evidence", nargs="?", type=Path)
    args = parser.parse_args()
    try:
        manifest = load_json(args.manifest)
        if args.command == "preflight":
            problems = validate_manifest(manifest)
            result: dict[str, Any] = {"status": "BLOCKED" if problems else "MANIFEST_VALID", "issues": problems}
        else:
            if args.evidence is None:
                parser.error(f"{args.command} requires a call.json or trace.jsonl")
            if args.command == "authorize":
                result = authorize(manifest, load_json(args.evidence))
            else:
                lines = args.evidence.read_text(encoding="utf-8").splitlines()
                result = audit(manifest, [json.loads(line) for line in lines if line.strip()])
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result = {"status": "UNKNOWN", "issues": [f"unreadable or invalid host evidence: {exc}"]}
    print(json.dumps(result, indent=2, sort_keys=True))
    if result.get("decision") == "allow" or result.get("status") in ("PASS", "MANIFEST_VALID"):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
