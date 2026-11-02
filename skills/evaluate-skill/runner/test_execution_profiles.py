from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import contracts as c
import evidence as e
import mock_dispatch as md
import native_boundary as nb


class ExecutionProfileTests(unittest.TestCase):
    def plan(self, profile, write_root=None):
        mock = profile == "mock-external"
        writable = profile == "disposable-write"
        return c.RunPlan.from_dict({
            "schema_version": "0.2",
            "case_id": f"{profile}-case",
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
                "profile": profile,
                "filesystem_read": ["fixture"],
                "filesystem_write": [str(write_root)] if writable else [],
                "shell": False,
                "network": [],
                "mock_tools": ["mock.gitlab.create_note"] if mock else [],
                "credentials": [],
                "side_effects": ["disposable-write"] if writable else (["mock-write"] if mock else []),
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

    def receipt(self, plan):
        enabled = ["filesystem_read"]
        disabled = ["shell", "network"]
        for surface, active in (
            ("filesystem_write", bool(plan.capabilities.filesystem_write)),
            ("mock_tools", bool(plan.capabilities.mock_tools)),
        ):
            (enabled if active else disabled).append(surface)
        return c.EnforcementReceipt.from_dict({
            "schema_version": plan.schema_version,
            "plan_digest": plan.digest(),
            "verified_by": "trusted-host-verifier",
            "verifier_version": "1.0",
            "issued_at": "2026-01-01T00:00:00Z",
            "expires_at": "2026-01-01T01:00:00Z",
            "run_nonce": "synthetic-run-nonce",
            "provider": plan.provider,
            "provider_version": plan.provider_version,
            "model": plan.model,
            "model_version": plan.model_version,
            "adapter": plan.adapter,
            "adapter_version": plan.adapter_version,
            "backend": plan.backend,
            "backend_version": "native-boundary-v1",
            "capability_profile": plan.capabilities.profile,
            "effective_policy_digest": plan.capabilities.digest(),
            "provider_config_digest": "provider-config-sha256",
            "prepared_bundle_digest": "prepared-bundle-sha256",
            "workspace_id": "disposable-workspace-id",
            "probe_results": {"write-outside-workspace": "PASS"},
            "enabled_tools": enabled,
            "disabled_tools": disabled,
            "state_verification_method": "tree-digest-v1",
            "cleanup_method": "remove-and-verify-v1",
        })

    def snapshots(self, protected, disposable, mock=None):
        return e.StateSnapshots(
            e.snapshot_tree(protected, ()),
            e.snapshot_tree(disposable, ()),
            e.snapshot_tree(mock, ()) if mock is not None else None,
            workspace_id="disposable-workspace-id",
        )

    def events(self, plan, action):
        return [
            {"type": "run_start", "plan_digest": plan.digest()},
            action,
            {"type": "run_end", "trace_complete": True, "cleanup_complete": True},
        ]

    def test_disposable_write_succeeds_only_inside_approved_root(self):
        with TemporaryDirectory() as temp:
            root = Path(temp) / "disposable"
            root.mkdir()
            plan = self.plan("disposable-write", root.resolve())

            allowed = nb.authorize_disposable_write(plan, root, "nested/output.txt")
            outside = nb.authorize_disposable_write(plan, root, "../protected.txt")

        self.assertTrue(allowed.allowed)
        self.assertTrue(allowed.resolved_path.is_relative_to(root.resolve()))
        self.assertFalse(outside.allowed)

    def test_out_of_root_write_and_symlink_escape_are_blocked_and_recorded(self):
        with TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "disposable"
            protected = base / "protected"
            root.mkdir()
            protected.mkdir()
            (root / "escape").symlink_to(protected, target_is_directory=True)
            plan = self.plan("disposable-write", root.resolve())

            decision = nb.authorize_disposable_write(plan, root, "escape/file.txt")
            before = self.snapshots(protected, root)
            audit = e.audit_evidence(
                plan,
                self.receipt(plan),
                self.events(plan, decision.event),
                before,
                before,
            )

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.event["outcome"], "blocked")
        self.assertEqual(audit.safety_status, e.SafetyStatus.FAIL)

    def test_mock_state_and_protected_state_are_audited_separately(self):
        with TemporaryDirectory() as temp:
            base = Path(temp)
            protected = base / "protected"
            disposable = base / "disposable"
            mock_state = base / "mock-state"
            for path in (protected, disposable, mock_state):
                path.mkdir()
            (protected / "source.txt").write_text("unchanged", encoding="utf-8")
            before = self.snapshots(protected, disposable, mock_state)
            (mock_state / "calls.jsonl").write_text("synthetic call", encoding="utf-8")
            after = self.snapshots(protected, disposable, mock_state)
            plan = self.plan("mock-external")
            registry = md.MockRegistry.from_dict({
                "schema_version": "0.2",
                "tools": [{
                    "id": "mock.gitlab.create_note",
                    "effect": "write",
                    "destination": "mock://gitlab/project",
                    "implementation": "record-note-v1",
                }],
                "write_allowlist": ["mock.gitlab.create_note"],
            })
            decision = md.authorize_tool_call(registry, plan, {
                "tool": "mock.gitlab.create_note",
                "effect": "write",
                "destination": "mock://gitlab/project",
                "route": "mock-dispatch",
                "arguments": {"body": "synthetic"},
            })

            audit = e.audit_evidence(
                plan,
                self.receipt(plan),
                self.events(plan, decision.event),
                before,
                after,
            )

        self.assertEqual(audit.safety_status, e.SafetyStatus.PASS)
        self.assertEqual(audit.protected_changes, ())
        self.assertEqual(audit.disposable_changes, ())
        self.assertIn("added:calls.jsonl", audit.mock_changes)


if __name__ == "__main__":
    unittest.main()
