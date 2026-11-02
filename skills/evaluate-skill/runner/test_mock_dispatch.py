import json
import unittest

import contracts as c
import mock_dispatch as md


class MockDispatchTests(unittest.TestCase):
    def plan(self):
        return c.RunPlan.from_dict({
            "schema_version": "0.2",
            "case_id": "mock-case",
            "case_revision": "case-sha256",
            "rubric_revision": "rubric-sha256",
            "skill_revision": "skill-sha256",
            "fixture_revision": "fixture-sha256",
            "provider": "openai",
            "provider_version": "0.163.0",
            "model": "approved-model",
            "model_version": "approved-snapshot",
            "adapter": "promptfoo-codex-sdk",
            "adapter_version": "0.125.1",
            "backend": "native",
            "capabilities": {
                "profile": "mock-external",
                "filesystem_read": ["fixture"],
                "filesystem_write": [],
                "shell": False,
                "network": [],
                "mock_tools": ["mock.gitlab.create_note"],
                "credentials": [],
                "side_effects": ["mock-write"],
                "evidence": ["action-trace", "protected-state"],
            },
            "resource_limits": {
                "max_seconds": 120,
                "max_turns": 10,
                "max_output_bytes": 200000,
                "max_cost_usd": 1.0,
            },
            "comparison_arms": ["with-skill", "without-skill"],
            "evidence_requirements": ["provider-result", "host-audit"],
            "cleanup_requirements": ["workspace-removed", "state-verified"],
        })

    def registry(self, allow_write=True):
        return md.MockRegistry.from_dict({
            "schema_version": "0.2",
            "tools": [{
                "id": "mock.gitlab.create_note",
                "effect": "write",
                "destination": "mock://gitlab/project",
                "implementation": "record-note-v1",
            }],
            "write_allowlist": ["mock.gitlab.create_note"] if allow_write else [],
        })

    def request(self, **changes):
        value = {
            "tool": "mock.gitlab.create_note",
            "effect": "write",
            "destination": "mock://gitlab/project",
            "route": "mock-dispatch",
            "arguments": {"body": "synthetic note"},
        }
        value.update(changes)
        return value

    def test_mock_tool_id_effect_and_destination_are_host_owned(self):
        registry = self.registry()
        plan = self.plan()
        for field, value in (
            ("effect", "read"),
            ("destination", "mock://gitlab/other"),
            ("tool", "mock.gitlab.delete_project"),
        ):
            with self.subTest(field=field):
                decision = md.authorize_tool_call(
                    registry, plan, self.request(**{field: value})
                )
                self.assertEqual(decision.decision, "deny")
                self.assertFalse(decision.event["authorized"])
        self.assertEqual(
            md.authorize_tool_call(self.registry(False), plan, self.request()).decision,
            "deny",
        )

    def test_live_http_shell_connector_and_child_agent_bypasses_are_denied(self):
        for route in ("http", "shell", "connector", "child-agent"):
            with self.subTest(route=route):
                decision = md.authorize_tool_call(
                    self.registry(), self.plan(), self.request(route=route)
                )
                self.assertEqual(decision.decision, "deny")
                self.assertEqual(decision.event["outcome"], "blocked")

    def test_allowed_mock_call_is_logged_with_sanitized_arguments(self):
        secret = "synthetic-secret-value"
        decision = md.authorize_tool_call(
            self.registry(),
            self.plan(),
            self.request(arguments={"body": "synthetic", "token": secret}),
        )

        self.assertEqual(decision.decision, "allow")
        self.assertTrue(decision.event["authorized"])
        self.assertEqual(decision.event["outcome"], "mocked")
        self.assertIn("arguments_digest", decision.event)
        self.assertNotIn(secret, json.dumps(decision.event))
        self.assertNotIn("arguments", decision.event)


if __name__ == "__main__":
    unittest.main()
