"""Offline regression tests; these exercise the analyzer, not any live model."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from profile_trace import ProfileInputError, profile  # noqa: E402


class ProfileTraceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.trace = json.loads((ROOT / "examples/trace.json").read_text())
        self.policy = json.loads((ROOT / "examples/routing-policy.json").read_text())

    def test_example_dispatch_cache_and_grader_cost(self) -> None:
        report = profile(self.trace, self.policy)
        status = {d["rule_id"]: d["status"] for d in report["dispatch_checks"]}
        self.assertEqual(status, {
            "R-01": "PASS", "R-02": "PASS", "R-03": "PASS",
            "R-04": "PASS", "R-05": "NOT_APPLICABLE",
        })
        self.assertEqual(report["usage"]["execution"]["observed_input_tokens"], 3000)
        self.assertEqual(report["usage"]["execution"]["observed_cached_input_tokens"], 700)
        self.assertAlmostEqual(report["usage"]["execution"]["observed_cost_usd"], 0.084)
        self.assertAlmostEqual(report["usage"]["grader"]["observed_cost_usd"], 0.011)
        self.assertAlmostEqual(report["usage"]["observed_total_cost_usd"], 0.095)
        self.assertEqual(len(report["repeat_tool_call_candidates"]), 1)
        self.assertEqual(report["repeat_tool_call_candidates"][0]["status"], "REVIEW_ONLY")
        self.assertTrue(all(b["status"] == "PASS" for b in report["budget_checks"]))

    def test_forbidden_actual_start_fails_even_if_dispatch_incomplete(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["coverage"]["dispatch_complete"] = False
        trace["events"].append({
            "id": "new", "type": "agent_start", "unit_id": "T-014",
            "skill": "refine-requirements",
        })
        result = profile(trace, self.policy)["dispatch_checks"][0]
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["observed_starts"], 1)

    def test_missing_required_start_on_incomplete_trace_is_unknown(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["coverage"]["dispatch_complete"] = False
        trace["events"] = [
            e for e in trace["events"]
            if e["id"] not in {"E-05", "E-06"}
        ]
        by_id = {d["rule_id"]: d for d in profile(trace, self.policy)["dispatch_checks"]}
        self.assertEqual(by_id["R-03"]["status"], "UNKNOWN")

    def test_explicit_wrong_skip_fails_even_with_incomplete_trace(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["coverage"]["dispatch_complete"] = False
        trace["events"] = [e for e in trace["events"] if e["id"] not in {"E-05", "E-06"}]
        trace["events"].append({
            "id": "wrong-skip", "type": "dispatch_decision", "unit_id": "T-015",
            "skill": "refine-requirements", "decision": "SKIP",
        })
        statuses = {r["rule_id"]: r["status"] for r in profile(trace, self.policy)["dispatch_checks"]}
        self.assertEqual(statuses["R-03"], "FAIL")

    def test_incomplete_usage_cannot_pass_under_budget(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["coverage"]["model_usage_complete"] = False
        statuses = {b["budget"]: b["status"] for b in profile(trace, self.policy)["budget_checks"]}
        self.assertEqual(statuses["max_execution_cost_usd"], "UNKNOWN")
        self.assertEqual(statuses["max_total_cost_usd"], "UNKNOWN")

    def test_partial_observed_overrun_is_still_fail(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["coverage"]["model_usage_complete"] = False
        policy = copy.deepcopy(self.policy)
        policy["budgets"]["max_execution_input_tokens"] = 100
        budget = {b["budget"]: b for b in profile(trace, policy)["budget_checks"]}
        self.assertEqual(budget["max_execution_input_tokens"]["status"], "FAIL")

    def test_no_contract_does_not_label_unnecessary(self) -> None:
        policy = copy.deepcopy(self.policy)
        policy["rules"] = []
        report = profile(self.trace, policy)
        self.assertEqual(report["dispatch_checks"], [])
        self.assertEqual(len(report["uncontracted_invocations"]), 3)
        self.assertTrue(all(x["status"] == "UNKNOWN" for x in report["uncontracted_invocations"]))

    def test_missing_token_field_remains_partial(self) -> None:
        trace = copy.deepcopy(self.trace)
        next(e for e in trace["events"] if e["id"] == "E-09")["usage"].pop("input_tokens")
        report = profile(trace, self.policy)
        self.assertFalse(report["usage"]["execution"]["input_tokens_complete"])
        budget = next(b for b in report["budget_checks"]
                      if b["budget"] == "max_execution_input_tokens")
        self.assertEqual(budget["status"], "UNKNOWN")

    def test_invalid_cached_subset_rejected(self) -> None:
        trace = copy.deepcopy(self.trace)
        next(e for e in trace["events"] if e["id"] == "E-04")["usage"]["cached_input_tokens"] = 9999
        with self.assertRaises(ProfileInputError):
            profile(trace, self.policy)

    def test_duplicate_event_rejected(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["events"].append(copy.deepcopy(trace["events"][0]))
        with self.assertRaises(ProfileInputError):
            profile(trace, self.policy)

    def test_mismatched_workflow_revision_rejected(self) -> None:
        policy = copy.deepcopy(self.policy)
        policy["workflow_revision"] = "unrelated-revision"
        with self.assertRaises(ProfileInputError):
            profile(self.trace, policy)


if __name__ == "__main__":
    unittest.main()
