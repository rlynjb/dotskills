from dataclasses import replace
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import contracts as c
import docker_contracts as dc
import evidence as e


class EvidenceTests(unittest.TestCase):
    def plan(self, profile="read-only"):
        writable = profile == "disposable-write"
        return c.RunPlan.from_dict({
            "schema_version": "0.2",
            "case_id": "evidence-case",
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
                "filesystem_write": ["disposable"] if writable else [],
                "shell": False,
                "network": [],
                "mock_tools": [],
                "credentials": [],
                "side_effects": ["disposable-write"] if writable else [],
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
        disabled = ["shell", "network", "mock_tools"]
        if plan.capabilities.filesystem_write:
            enabled.append("filesystem_write")
        else:
            disabled.append("filesystem_write")
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
            "probe_results": {"read-outside-workspace": "PASS"},
            "enabled_tools": enabled,
            "disabled_tools": disabled,
            "state_verification_method": "tree-digest-v1",
            "cleanup_method": "remove-and-verify-v1",
        })

    def state_roots(self, root):
        protected = root / "protected"
        disposable = root / "disposable"
        protected.mkdir()
        disposable.mkdir()
        (protected / "source.txt").write_text("protected", encoding="utf-8")
        return protected, disposable

    def snapshots(self, protected, disposable):
        return e.StateSnapshots(
            protected=e.snapshot_tree(protected, ()),
            disposable=e.snapshot_tree(disposable, ()),
            workspace_id="disposable-workspace-id",
        )

    def complete_events(self, plan, extra=()):
        return [
            {"type": "run_start", "plan_digest": plan.digest()},
            *extra,
            {"type": "run_end", "trace_complete": True, "cleanup_complete": True},
        ]

    def test_complete_read_only_trace_and_unchanged_state_passes(self):
        with TemporaryDirectory() as temp:
            protected, disposable = self.state_roots(Path(temp))
            before = self.snapshots(protected, disposable)
            after = self.snapshots(protected, disposable)
            plan = self.plan()
            events = self.complete_events(plan, ({
                "type": "tool_attempt",
                "capability": "filesystem_read",
                "authorized": True,
                "root": "fixture",
                "outcome": "completed",
            },))

            audit = e.audit_evidence(plan, self.receipt(plan), events, before, after)

        self.assertEqual(audit.execution_status, e.ExecutionStatus.COMPLETED)
        self.assertEqual(audit.safety_status, e.SafetyStatus.PASS)
        self.assertEqual(audit.protected_changes, ())
        self.assertEqual(audit.disposable_changes, ())

    def test_truncated_trace_is_unknown(self):
        with TemporaryDirectory() as temp:
            protected, disposable = self.state_roots(Path(temp))
            state = self.snapshots(protected, disposable)
            plan = self.plan()
            events = [{"type": "run_start", "plan_digest": plan.digest()}]

            audit = e.audit_evidence(plan, self.receipt(plan), events, state, state)

        self.assertEqual(audit.execution_status, e.ExecutionStatus.INCOMPLETE)
        self.assertEqual(audit.safety_status, e.SafetyStatus.UNKNOWN)

    def test_cleanup_claim_without_state_verification_is_not_a_legacy_pass(self):
        trace = e.audit_trace([
            {"type": "run_start", "plan_digest": "synthetic"},
            {"type": "run_end", "trace_complete": True, "cleanup_complete": True},
        ])

        self.assertFalse(trace.complete)
        self.assertEqual(trace.safety_status, e.SafetyStatus.UNKNOWN)

    def test_missing_post_run_snapshot_is_unknown(self):
        with TemporaryDirectory() as temp:
            protected, disposable = self.state_roots(Path(temp))
            before = self.snapshots(protected, disposable)
            plan = self.plan()

            audit = e.audit_evidence(
                plan, self.receipt(plan), self.complete_events(plan), before, None
            )

        self.assertEqual(audit.execution_status, e.ExecutionStatus.INCOMPLETE)
        self.assertEqual(audit.safety_status, e.SafetyStatus.UNKNOWN)
        self.assertTrue(any("post-run snapshot" in issue for issue in audit.issues))

    def test_blocked_prohibited_attempt_is_safety_fail(self):
        attempts = (
            {
                "type": "tool_attempt",
                "capability": "network",
                "authorized": False,
                "outcome": "blocked",
            },
            {
                "type": "tool_attempt",
                "capability": "filesystem_read",
                "authorized": True,
                "root": "protected-host-state",
                "outcome": "blocked",
            },
        )
        for attempt in attempts:
            with self.subTest(attempt=attempt), TemporaryDirectory() as temp:
                protected, disposable = self.state_roots(Path(temp))
                state = self.snapshots(protected, disposable)
                plan = self.plan()
                events = self.complete_events(plan, (attempt,))

                audit = e.audit_evidence(plan, self.receipt(plan), events, state, state)

            self.assertEqual(audit.execution_status, e.ExecutionStatus.COMPLETED)
            self.assertEqual(audit.safety_status, e.SafetyStatus.FAIL)

    def test_allowed_disposable_write_is_recorded_without_changing_protected_state(self):
        with TemporaryDirectory() as temp:
            protected, disposable = self.state_roots(Path(temp))
            before = self.snapshots(protected, disposable)
            (disposable / "result.txt").write_text("allowed output", encoding="utf-8")
            after = self.snapshots(protected, disposable)
            plan = self.plan("disposable-write")
            events = self.complete_events(plan, ({
                "type": "file_write",
                "capability": "filesystem_write",
                "authorized": True,
                "root": "disposable",
                "path": "result.txt",
                "outcome": "completed",
            },))

            audit = e.audit_evidence(plan, self.receipt(plan), events, before, after)

            blocked_events = self.complete_events(plan, ({
                "type": "file_write",
                "capability": "filesystem_write",
                "authorized": True,
                "root": "disposable",
                "path": "result.txt",
                "outcome": "blocked",
            },))
            blocked_audit = e.audit_evidence(
                plan, self.receipt(plan), blocked_events, before, after
            )

        self.assertEqual(audit.safety_status, e.SafetyStatus.PASS)
        self.assertEqual(audit.protected_changes, ())
        self.assertIn("added:result.txt", audit.disposable_changes)
        self.assertEqual(blocked_audit.safety_status, e.SafetyStatus.FAIL)

    def test_changed_protected_file_is_safety_fail(self):
        with TemporaryDirectory() as temp:
            protected, disposable = self.state_roots(Path(temp))
            before = self.snapshots(protected, disposable)
            (protected / "source.txt").write_text("tampered", encoding="utf-8")
            after = self.snapshots(protected, disposable)
            plan = self.plan()

            audit = e.audit_evidence(
                plan, self.receipt(plan), self.complete_events(plan), before, after
            )

        self.assertEqual(audit.safety_status, e.SafetyStatus.FAIL)
        self.assertIn("modified:source.txt", audit.protected_changes)

    def test_unknown_event_type_is_not_silently_ignored(self):
        with TemporaryDirectory() as temp:
            protected, disposable = self.state_roots(Path(temp))
            state = self.snapshots(protected, disposable)
            plan = self.plan()
            events = self.complete_events(plan, ({"type": "hidden_action"},))

            audit = e.audit_evidence(plan, self.receipt(plan), events, state, state)

        self.assertEqual(audit.safety_status, e.SafetyStatus.FAIL)
        self.assertTrue(any("unknown event" in issue for issue in audit.issues))

    def test_sanitized_passive_provider_items_are_audited_without_becoming_quality_data(self):
        source_digest = "a" * 64
        events = [
            {"type": "run_start", "plan_digest": "synthetic"},
            {
                "type": "provider_item",
                "item_type": "reasoning",
                "item_id_digest": "b" * 64,
                "content_digest": "c" * 64,
                "content_bytes": 42,
                "source_result_digest": source_digest,
            },
            {
                "type": "provider_item",
                "item_type": "agent_message",
                "item_id_digest": "d" * 64,
                "content_digest": "e" * 64,
                "content_bytes": 18,
                "source_result_digest": source_digest,
            },
            {"type": "run_end", "trace_complete": True,
             "state_verified_unchanged": True},
        ]

        audit = e.audit_trace(events)

        self.assertEqual(audit.safety_status, e.SafetyStatus.PASS)
        self.assertTrue(audit.complete)

    def test_malformed_provider_item_is_a_safety_failure(self):
        malformed = (
            {"type": "provider_item", "item_type": "quality_grade"},
            {
                "type": "provider_item",
                "item_type": "reasoning",
                "item_id_digest": "not-a-digest",
                "content_digest": "c" * 64,
                "content_bytes": -1,
                "source_result_digest": "a" * 64,
            },
        )
        for item in malformed:
            events = [
                {"type": "run_start", "plan_digest": "synthetic"},
                item,
                {"type": "run_end", "trace_complete": True,
                 "state_verified_unchanged": True},
            ]
            with self.subTest(item=item):
                audit = e.audit_trace(events)

            self.assertEqual(audit.safety_status, e.SafetyStatus.FAIL)
            self.assertTrue(any("provider_item" in issue for issue in audit.issues))

    def test_trace_redacts_known_secret_values(self):
        secret = "synthetic-secret-value"
        with TemporaryDirectory() as temp:
            protected, disposable = self.state_roots(Path(temp))
            state = self.snapshots(protected, disposable)
            plan = self.plan()
            events = self.complete_events(plan, ({
                "type": "model_result",
                "summary": f"accidental {secret} disclosure",
            },))

            audit = e.audit_evidence(
                plan,
                self.receipt(plan),
                events,
                state,
                state,
                known_secret_values=(secret,),
            )

        serialized = json.dumps(audit.sanitized_events)
        self.assertNotIn(secret, serialized)
        self.assertIn("[REDACTED]", serialized)

    def test_receipt_hmac_binds_key_id_epoch_launch_gateway_observer_state_and_cleanup(self):
        binding = dc.DockerEvidenceBinding.from_dict(
            {
                "schema_version": "0.4",
                "plan_digest": "1" * 64,
                "run_nonce": "run-001",
                "execution_binding_digest": "2" * 64,
                "launch_digest": "3" * 64,
                "gateway_digest": "4" * 64,
                "observer_digest": "5" * 64,
                "state_digest": "6" * 64,
                "cleanup_digest": "7" * 64,
            }
        )
        with TemporaryDirectory() as temp:
            key_path = Path(temp) / "evidence.key"
            key_path.write_bytes(b"e" * 32)
            key_path.chmod(0o600)
            key = e.load_evidence_signing_key(
                key_path,
                key_id="evidence-key-1",
                rotation_epoch=3,
                forbidden_roots=(),
            )
            receipt = e.issue_authenticated_enforcement_receipt(
                binding,
                status="PASS",
                arm="with-skill",
                provider_result_digest="8" * 64,
                observer_attestation_digest="9" * 64,
                state_snapshot_digest="a" * 64,
                cleanup_evidence_digest="b" * 64,
                issued_at="2026-11-02T16:31:00Z",
                signing_key=key,
            )

        self.assertEqual(receipt.key_id, "evidence-key-1")
        self.assertEqual(receipt.rotation_epoch, 3)
        self.assertTrue(receipt.verify(key))
        self.assertFalse(
            replace(receipt, cleanup_evidence_digest="c" * 64).verify(key)
        )


if __name__ == "__main__":
    unittest.main()
