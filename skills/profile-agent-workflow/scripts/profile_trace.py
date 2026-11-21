#!/usr/bin/env python3
"""Deterministic, read-only profiler for a normalized agent workflow trace.

No network, model calls, subprocesses, or filesystem writes. This analyzes
supplied trace/policy JSON; it cannot verify their provenance or completeness.

python3 scripts/profile_trace.py --trace examples/trace.json --policy examples/policy.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

EVENT_TYPES = {"dispatch_decision", "agent_start", "tool_call", "model_call", "retry", "error"}
EXPECTED = {"REQUIRED", "FORBIDDEN", "OPTIONAL"}
BUDGETS = {
    "max_execution_cost_usd": ("execution_cost", "model_usage_complete"),
    "max_total_cost_usd": ("total_cost", "model_usage_complete"),
    "max_execution_input_tokens": ("execution_input", "model_usage_complete"),
    "max_agent_starts": ("agent_starts", "dispatch_complete"),
    "max_model_calls": ("model_calls", "model_usage_complete"),
    "max_tool_calls": ("tool_calls", "tool_complete"),
}
USAGE_FIELDS = {"input_tokens", "cached_input_tokens", "output_tokens", "cost_usd"}


class ProfileInputError(ValueError):
    """Invalid or incompatible normalized evidence."""


def _object(value: Any, label: str) -> dict:
    if not isinstance(value, dict):
        raise ProfileInputError(f"{label} must be an object")
    return value


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProfileInputError(f"{label} must be a nonempty string")
    return value


def _number(value: Any, label: str, *, integer: bool = False) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ProfileInputError(f"{label} must be a nonnegative number")
    if not math.isfinite(value) or value < 0 or (integer and not isinstance(value, int)):
        raise ProfileInputError(f"{label} must be a nonnegative {'integer' if integer else 'number'}")
    return value


def load_json(path: Path) -> dict:
    try:
        return _object(json.loads(path.read_text(encoding="utf-8")), str(path))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProfileInputError(f"cannot load {path}: {exc}") from exc


def validate(trace: dict, policy: dict) -> tuple[list[dict], list[dict], dict, dict]:
    if trace.get("schema_version") != 1 or policy.get("schema_version") != 1:
        raise ProfileInputError("trace and policy must have schema_version 1")
    _string(trace.get("run_id"), "trace.run_id")
    _string(policy.get("policy_id"), "policy.policy_id")
    t_rev, p_rev = trace.get("workflow_revision"), policy.get("workflow_revision")
    if t_rev is not None:
        _string(t_rev, "trace.workflow_revision")
    if p_rev is not None:
        _string(p_rev, "policy.workflow_revision")
    if t_rev and p_rev and t_rev != p_rev:
        raise ProfileInputError("workflow revisions differ; do not compare mismatched evidence")

    coverage = _object(trace.get("coverage"), "trace.coverage")
    for key in ("dispatch_complete", "tool_complete", "model_usage_complete"):
        if type(coverage.get(key)) is not bool:
            raise ProfileInputError(f"coverage.{key} must be explicitly true or false")

    events = trace.get("events")
    if not isinstance(events, list):
        raise ProfileInputError("trace.events must be an array")
    seen_event_ids: set[str] = set()
    for index, event in enumerate(events):
        event = _object(event, f"events[{index}]")
        event_id = _string(event.get("id"), f"events[{index}].id")
        if event_id in seen_event_ids:
            raise ProfileInputError(f"duplicate event id: {event_id}")
        seen_event_ids.add(event_id)
        kind = event.get("type")
        if not isinstance(kind, str) or kind not in EVENT_TYPES:
            raise ProfileInputError(f"unknown event type at {event_id}: {kind!r}")
        _string(event.get("unit_id"), f"{event_id}.unit_id")
        if kind in ("dispatch_decision", "agent_start"):
            _string(event.get("skill"), f"{event_id}.skill")
        if kind == "dispatch_decision" and event.get("decision") not in {"SKIP", "DISPATCH"}:
            raise ProfileInputError(f"{event_id}.decision must be SKIP or DISPATCH")
        if kind == "tool_call":
            _string(event.get("tool"), f"{event_id}.tool")
            if "fingerprint" in event:
                _string(event["fingerprint"], f"{event_id}.fingerprint")
        if kind == "model_call":
            if event.get("purpose") not in {"execution", "grader"}:
                raise ProfileInputError(f"{event_id}.purpose must be execution or grader")
            if "usage" in event:
                usage = _object(event["usage"], f"{event_id}.usage")
                if not set(usage).issubset(USAGE_FIELDS):
                    raise ProfileInputError(f"{event_id}.usage contains an unknown field")
                for field, value in usage.items():
                    _number(value, f"{event_id}.{field}", integer=field != "cost_usd")
                if (usage.get("cached_input_tokens") is not None
                        and usage.get("input_tokens") is not None
                        and usage["cached_input_tokens"] > usage["input_tokens"]):
                    raise ProfileInputError(f"{event_id}: cached tokens exceed input tokens")

    rules = policy.get("rules")
    if not isinstance(rules, list):
        raise ProfileInputError("policy.rules must be an array")
    seen_rules: set[tuple[str, str]] = set()
    rule_ids: set[str] = set()
    for index, rule in enumerate(rules):
        rule = _object(rule, f"rules[{index}]")
        rule_id = _string(rule.get("id"), f"rules[{index}].id")
        unit = _string(rule.get("unit_id"), f"{rule_id}.unit_id")
        skill = _string(rule.get("skill"), f"{rule_id}.skill")
        if rule.get("expected") not in EXPECTED:
            raise ProfileInputError(f"{rule_id}.expected must be REQUIRED, FORBIDDEN or OPTIONAL")
        if (unit, skill) in seen_rules or rule_id in rule_ids:
            raise ProfileInputError(f"duplicate routing rule: {rule_id} / {unit} / {skill}")
        seen_rules.add((unit, skill))
        rule_ids.add(rule_id)

    budgets = policy.get("budgets", {})
    budgets = _object(budgets, "policy.budgets")
    if not set(budgets).issubset(BUDGETS):
        raise ProfileInputError("unknown budget key(s): " + ", ".join(sorted(set(budgets) - set(BUDGETS))))
    for key, value in budgets.items():
        _number(value, f"budgets.{key}", integer=key.endswith("_tokens")
                or key in {"max_agent_starts", "max_tool_calls", "max_model_calls"})
    return events, rules, budgets, coverage


def usage_bucket(events: list[dict], purpose: str, declared_complete: bool) -> dict:
    calls = [e for e in events if e["type"] == "model_call" and e["purpose"] == purpose]
    result: dict[str, Any] = {"observed_model_calls": len(calls)}
    for field in sorted(USAGE_FIELDS):
        present = [e["usage"][field] for e in calls if isinstance(e.get("usage"), dict)
                   and field in e["usage"]]
        result[f"observed_{field}"] = round(sum(present), 10) if field == "cost_usd" else sum(present)
        result[f"{field}_complete"] = bool(declared_complete and len(present) == len(calls))
    return result


def budget_status(observed: float, complete: bool, cap: float) -> str:
    # Already observed spending above the cap proves a violation even on a partial trace.
    if observed > cap + (1e-10 if isinstance(cap, float) else 0):
        return "FAIL"
    return "PASS" if complete else "UNKNOWN"


def profile(trace: dict, policy: dict) -> dict:
    events, rules, budgets, coverage = validate(trace, policy)
    starts: dict[tuple[str, str], list[str]] = defaultdict(list)
    decisions: dict[tuple[str, str], list[dict]] = defaultdict(list)
    tool_groups: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    counts = Counter(e["type"] for e in events)
    for event in events:
        key = (event["unit_id"], event.get("skill", ""))
        if event["type"] == "agent_start":
            starts[key].append(event["id"])
        elif event["type"] == "dispatch_decision":
            decisions[key].append(event)
        elif event["type"] == "tool_call" and event.get("fingerprint"):
            tool_groups[(event["unit_id"], event["tool"], event["fingerprint"])].append(event["id"])

    dispatch = []
    allowed_keys = {(r["unit_id"], r["skill"]) for r in rules}
    for rule in rules:
        key = (rule["unit_id"], rule["skill"])
        observed = starts.get(key, [])
        d = decisions.get(key, [])
        choices = {x["decision"] for x in d}
        expected = rule["expected"]
        if expected == "OPTIONAL":
            status = "NOT_APPLICABLE"
        elif expected == "FORBIDDEN":
            status = "FAIL" if observed or "DISPATCH" in choices else (
                "PASS" if coverage["dispatch_complete"] else "UNKNOWN")
        elif observed:
            status = "UNKNOWN" if "SKIP" in choices else "PASS"
        elif "SKIP" in choices:
            status = "FAIL"
        else:
            status = "FAIL" if coverage["dispatch_complete"] else "UNKNOWN"
        dispatch.append({
            "rule_id": rule["id"], "unit_id": key[0], "skill": key[1],
            "expected": expected, "status": status,
            "observed_starts": len(observed),
            "start_event_ids": observed,
            "decision_event_ids": [x["id"] for x in d],
            "recorded_decisions": sorted(choices),
            "rule_reason": rule.get("reason"),
        })

    uncontracted = [
        {"unit_id": k[0], "skill": k[1], "start_event_ids": ids, "status": "UNKNOWN"}
        for k, ids in sorted(starts.items()) if k not in allowed_keys
    ]
    repeat_agents = [
        {"unit_id": k[0], "skill": k[1], "start_event_ids": ids, "status": "REVIEW_ONLY"}
        for k, ids in sorted(starts.items()) if len(ids) > 1
    ]
    repeats = [
        {"unit_id": k[0], "tool": k[1], "fingerprint": k[2],
         "event_ids": ids, "status": "REVIEW_ONLY"}
        for k, ids in sorted(tool_groups.items()) if len(ids) > 1
    ]

    execution = usage_bucket(events, "execution", coverage["model_usage_complete"])
    grader = usage_bucket(events, "grader", coverage["model_usage_complete"])
    observed_total_cost = execution["observed_cost_usd"] + grader["observed_cost_usd"]
    total_cost_complete = execution["cost_usd_complete"] and grader["cost_usd_complete"]
    values = {
        "execution_cost": (execution["observed_cost_usd"], execution["cost_usd_complete"]),
        "total_cost": (observed_total_cost, total_cost_complete),
        "execution_input": (execution["observed_input_tokens"], execution["input_tokens_complete"]),
        "agent_starts": (counts["agent_start"], coverage["dispatch_complete"]),
        "tool_calls": (counts["tool_call"], coverage["tool_complete"]),
        "model_calls": (counts["model_call"], coverage["model_usage_complete"]),
    }
    budget_checks = []
    for name, cap in sorted(budgets.items()):
        observed, complete = values[BUDGETS[name][0]]
        budget_checks.append({
            "budget": name, "limit": cap, "observed": observed,
            "complete_as_claimed": complete,
            "status": budget_status(observed, complete, cap),
        })

    unknowns = []
    for channel, flag in coverage.items():
        if channel in {"dispatch_complete", "tool_complete", "model_usage_complete"} and not flag:
            unknowns.append(f"trace claims incomplete {channel}; absence and under-budget conclusions are uncertain")
    if not all(execution[f"{field}_complete"] and grader[f"{field}_complete"] for field in USAGE_FIELDS):
        unknowns.append("at least one model-usage metric lacks complete provider-reported evidence")
    if uncontracted:
        unknowns.append("some observed skill starts have no matching approved routing rule")
    if any(d["status"] == "UNKNOWN" for d in dispatch):
        unknowns.append("at least one routing check lacks enough evidence for PASS or FAIL")

    return {
        "schema_version": 1,
        "run_id": trace["run_id"],
        "policy_id": policy["policy_id"],
        "workflow_revision": trace.get("workflow_revision"),
        "coverage_claims": {k: coverage[k] for k in
                            ("dispatch_complete", "tool_complete", "model_usage_complete")},
        "coverage_warning": "Input coverage flags are claims, not independently verified host evidence.",
        "observed_event_counts": dict(sorted(counts.items())),
        "dispatch_summary": dict(sorted(Counter(d["status"] for d in dispatch).items())),
        "dispatch_checks": dispatch,
        "uncontracted_invocations": uncontracted,
        "repeat_tool_call_candidates": repeats,
        "repeat_agent_start_candidates": repeat_agents,
        "usage": {
            "execution": execution, "grader": grader,
            "observed_total_cost_usd": round(observed_total_cost, 10),
            "total_cost_complete_as_claimed": total_cost_complete,
            "cached_tokens_note": "cached input tokens are a subset of input tokens; do not add twice",
        },
        "budget_checks": budget_checks,
        "unknowns": unknowns,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trace", type=Path, required=True)
    parser.add_argument("--policy", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = profile(load_json(args.trace), load_json(args.policy))
    except ProfileInputError as exc:
        print(f"PROFILE_INPUT_ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0  # A FAIL finding is a valid report, not a CLI execution failure.


if __name__ == "__main__":
    raise SystemExit(main())
