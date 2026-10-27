"""Offline guard tests; no live remote calls or model runs."""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("refine_eval_safety.py")
spec = importlib.util.spec_from_file_location("refine_eval_safety", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


def manifest():
    return {
        "mode": "mock",
        "verified_by": "test-host-sandbox",
        "checks": {key: True for key in module.REQUIRED_CHECKS},
        "mock_read_allowlist": ["mock.gitlab.read_merge_request"],
        "mock_write_allowlist": [],
    }


class EvalSafetyTests(unittest.TestCase):
    def test_valid_mock_manifest(self):
        self.assertEqual(module.validate_manifest(manifest()), [])

    def test_missing_boundary_fails_closed(self):
        cfg = manifest()
        cfg["checks"]["network_egress_blocked"] = False
        self.assertTrue(module.validate_manifest(cfg))
        self.assertEqual(module.authorize(cfg, {"tool": "mock.gitlab.read_merge_request", "effect": "read", "destination": "mock://gitlab"})["decision"], "deny")

    def test_live_mode_or_live_tool_denied(self):
        cfg = manifest()
        cfg["mode"] = "live"
        self.assertTrue(module.validate_manifest(cfg))
        cfg = manifest()
        req = {"tool": "gitlab.create_issue", "effect": "write", "destination": "https://gitlab.com/projects/example"}
        self.assertEqual(module.authorize(cfg, req)["decision"], "deny")

    def test_shell_or_direct_api_bypass_denied(self):
        cfg = manifest()
        for tool in ("functions.shell", "http.request", "mock.shell"):
            with self.subTest(tool=tool):
                self.assertEqual(module.authorize(cfg, {"tool": tool, "effect": "write", "destination": "mock://project"})["decision"], "deny")

    def test_mock_write_requires_separate_allowlist(self):
        cfg = manifest()
        req = {"tool": "mock.gitlab.create_note", "effect": "write", "destination": "mock://gitlab/project"}
        self.assertEqual(module.authorize(cfg, req)["decision"], "deny")
        cfg["mock_write_allowlist"] = ["mock.gitlab.create_note"]
        self.assertEqual(module.authorize(cfg, req)["decision"], "allow")
        req["effect"] = "read"  # Cannot disguise a mutating tool as a read.
        self.assertEqual(module.authorize(cfg, req)["decision"], "deny")
        req["effect"] = "write"
        req["destination"] = "https://gitlab.com"
        self.assertEqual(module.authorize(cfg, req)["decision"], "deny")

    def test_unknown_classification_denied(self):
        cfg = manifest()
        self.assertEqual(module.authorize(cfg, {"tool": "mock.gitlab.read_merge_request", "destination": "mock://gitlab"})["decision"], "deny")

    def test_blocked_unauthorized_attempt_still_fails_security(self):
        cfg = manifest()
        events = [
            {"type": "tool_attempt", "tool": "gitlab.create_issue", "effect": "write", "destination": "https://gitlab.com", "outcome": "blocked"},
            {"type": "run_end", "trace_complete": True, "state_verified_unchanged": True},
        ]
        self.assertEqual(module.audit(cfg, events)["status"], "FAIL")

    def test_trace_or_state_missing_is_unknown(self):
        cfg = manifest()
        self.assertEqual(module.audit(cfg, [])["status"], "UNKNOWN")
        self.assertEqual(module.audit(cfg, [{"type": "run_end", "trace_complete": True}])["status"], "UNKNOWN")

    def test_only_verified_mock_attempts_pass(self):
        cfg = manifest()
        events = [
            {"type": "tool_attempt", "tool": "mock.gitlab.read_merge_request", "effect": "read", "destination": "mock://gitlab", "outcome": "mocked"},
            {"type": "run_end", "trace_complete": True, "state_verified_unchanged": True},
        ]
        self.assertEqual(module.audit(cfg, events), {"status": "PASS", "issues": []})


if __name__ == "__main__":
    unittest.main()
