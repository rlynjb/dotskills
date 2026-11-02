from dataclasses import replace
from pathlib import Path
from types import MappingProxyType
import unittest

import capability_inventory as ci
import contracts as c
import execution_policy as ep


class ExecutionPolicyTests(unittest.TestCase):
    def plan_value(self, backend="native"):
        return {
            "schema_version": "0.2",
            "case_id": "read-only-case",
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
            "backend": backend,
            "capabilities": {
                "profile": "read-only",
                "filesystem_read": ["fixture"],
                "filesystem_write": [],
                "shell": False,
                "network": [],
                "mock_tools": [],
                "credentials": [],
                "side_effects": [],
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
        }

    def approval(self, plan, **changes):
        value = {
            "schema_version": plan.schema_version,
            "plan_digest": plan.digest(),
            "approved_by": "human-reviewer",
            "provider": plan.provider,
            "model": plan.model,
            "adapter": plan.adapter,
            "backend": plan.backend,
            "capability_profile": plan.capabilities.profile,
            "capability_digest": plan.capabilities.digest(),
            "side_effects": list(plan.capabilities.side_effects),
        }
        value.update(changes)
        return c.ApprovalReceipt.from_dict(value)

    def enforcement(self, plan, **changes):
        probe_results = {
            "read-outside-workspace": "PASS",
            "write-outside-workspace": "PASS",
            "secondary-tool-route": "PASS",
            "network-egress": "PASS",
            "environment-secret": "PASS",
            "action-trace-completeness": "PASS",
            "state-snapshot": "PASS",
            "cleanup-verification": "PASS",
        }
        value = {
            "schema_version": plan.schema_version,
            "plan_digest": plan.digest(),
            "verified_by": "trusted-host-verifier",
            "verifier_version": "1.0",
            "provider": plan.provider,
            "provider_version": plan.provider_version,
            "model": plan.model,
            "model_version": plan.model_version,
            "adapter": plan.adapter,
            "adapter_version": plan.adapter_version,
            "backend": plan.backend,
            "backend_version": "verified-boundary-v1",
            "capability_profile": plan.capabilities.profile,
            "effective_policy_digest": plan.capabilities.digest(),
            "workspace_id": "disposable-workspace-id",
            "probe_results": probe_results,
            "enabled_tools": ["filesystem_read"],
            "disabled_tools": ["filesystem_write", "shell", "network", "mock_tools"],
            "state_verification_method": "tree-digest-v1",
            "cleanup_method": "remove-and-verify-v1",
        }
        value.update(changes)
        return c.EnforcementReceipt.from_dict(value)

    def inventory(self, verified=True):
        path = Path(__file__).with_name("provider_capabilities_v0_2.json")
        inventory = ci.load_inventory(path)
        if not verified:
            return inventory
        claims = {
            key: ci.CapabilityClaim("verified", claim.required_probes)
            for key, claim in inventory.claims.items()
        }
        return replace(inventory, claims=MappingProxyType(claims))

    def assert_blocked_for(self, decision, field):
        self.assertEqual(decision.decision, "BLOCKED")
        self.assertIsNone(decision.backend)
        self.assertTrue(
            any(field in reason for reason in decision.reasons),
            (field, decision.reasons),
        )

    def test_verified_native_read_only_plan_is_approved(self):
        plan = c.RunPlan.from_dict(self.plan_value())

        decision = ep.assess_run(
            plan, self.approval(plan), self.enforcement(plan), self.inventory()
        )

        self.assertEqual(decision, ep.PolicyDecision("APPROVED", "native", ()))

    def test_missing_or_mismatched_approval_blocks(self):
        plan = c.RunPlan.from_dict(self.plan_value())
        enforcement = self.enforcement(plan)

        missing = ep.assess_run(plan, None, enforcement, self.inventory())
        self.assert_blocked_for(missing, "approval_receipt")

        mismatched = ep.assess_run(
            plan,
            self.approval(plan, plan_digest="wrong-digest"),
            enforcement,
            self.inventory(),
        )
        self.assert_blocked_for(mismatched, "approval.plan_digest")

    def test_unverified_required_native_capability_blocks(self):
        plan = c.RunPlan.from_dict(self.plan_value())

        decision = ep.assess_run(
            plan, self.approval(plan), self.enforcement(plan), self.inventory(False)
        )

        self.assert_blocked_for(decision, "capabilities.filesystem_read")

    def test_failed_or_missing_negative_probe_blocks(self):
        plan = c.RunPlan.from_dict(self.plan_value())
        for status in ("FAIL", None):
            with self.subTest(status=status):
                probe_results = dict(self.enforcement(plan).probe_results)
                if status is None:
                    del probe_results["read-outside-workspace"]
                else:
                    probe_results["read-outside-workspace"] = status
                decision = ep.assess_run(
                    plan,
                    self.approval(plan),
                    self.enforcement(plan, probe_results=probe_results),
                    self.inventory(),
                )
                self.assert_blocked_for(
                    decision, "enforcement.probe_results.read-outside-workspace"
                )

    def test_docker_is_never_selected_when_plan_approves_native(self):
        plan = c.RunPlan.from_dict(self.plan_value("native"))

        decision = ep.assess_run(
            plan,
            self.approval(plan),
            self.enforcement(plan, backend="docker"),
            self.inventory(),
        )

        self.assert_blocked_for(decision, "enforcement.backend")

    def test_native_is_never_selected_when_plan_approves_docker(self):
        plan = c.RunPlan.from_dict(self.plan_value("docker"))

        decision = ep.assess_run(
            plan,
            self.approval(plan),
            self.enforcement(plan, backend="native"),
            self.inventory(),
        )

        self.assert_blocked_for(decision, "enforcement.backend")

    def test_provider_model_adapter_or_backend_drift_blocks(self):
        plan = c.RunPlan.from_dict(self.plan_value())
        changes = {
            "provider": "anthropic",
            "provider_version": "changed-provider-version",
            "model": "changed-model",
            "model_version": "changed-model-version",
            "adapter": "promptfoo-claude-agent-sdk",
            "adapter_version": "changed-adapter-version",
            "backend": "docker",
        }
        for field, value in changes.items():
            with self.subTest(field=field):
                decision = ep.assess_run(
                    plan,
                    self.approval(plan),
                    self.enforcement(plan, **{field: value}),
                    self.inventory(),
                )
                self.assert_blocked_for(decision, f"enforcement.{field}")

    def test_unknown_required_evidence_blocks(self):
        value = self.plan_value()
        value["evidence_requirements"] = ["provider-result", "magic-proof"]
        plan = c.RunPlan.from_dict(value)

        decision = ep.assess_run(
            plan, self.approval(plan), self.enforcement(plan), self.inventory()
        )

        self.assert_blocked_for(decision, "evidence_requirements.magic-proof")

    def test_self_declared_manifest_without_receipt_blocks(self):
        plan = c.RunPlan.from_dict(self.plan_value())
        manifest = {"host_enforced": True, "all_checks": True}

        decision = ep.assess_run(plan, self.approval(plan), manifest, self.inventory())

        self.assert_blocked_for(decision, "enforcement_receipt")


if __name__ == "__main__":
    unittest.main()
