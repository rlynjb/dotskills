from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import MappingProxyType
import unittest

import capability_inventory as ci
import contracts as c
import execution_policy as ep

try:
    import docker_contracts as dc
except ModuleNotFoundError:
    dc = None


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
        now = datetime.now(timezone.utc)
        value = {
            "schema_version": plan.schema_version,
            "plan_digest": plan.digest(),
            "approved_by": "human-reviewer",
            "issued_at": (now - timedelta(minutes=5)).isoformat(),
            "expires_at": (now + timedelta(minutes=55)).isoformat(),
            "run_nonce": "synthetic-run-nonce",
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
        now = datetime.now(timezone.utc)
        probe_results = {
            "read-outside-workspace": "PASS",
            "write-outside-workspace": "PASS",
            "secondary-tool-route": "PASS",
            "network-egress": "PASS",
            "environment-secret": "PASS",
            "action-trace-completeness": "PASS",
            "state-snapshot": "PASS",
            "cleanup-verification": "PASS",
            "write-inside-workspace": "PASS",
        }
        value = {
            "schema_version": plan.schema_version,
            "plan_digest": plan.digest(),
            "verified_by": "trusted-host-verifier",
            "verifier_version": "1.0",
            "issued_at": (now - timedelta(minutes=5)).isoformat(),
            "expires_at": (now + timedelta(minutes=55)).isoformat(),
            "run_nonce": "synthetic-run-nonce",
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
            "provider_config_digest": "provider-config-sha256",
            "prepared_bundle_digest": "prepared-bundle-sha256",
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

    def docker_binding(self, plan, **changes):
        self.assertIsNotNone(dc, "docker_contracts module must exist")
        value = {
            "schema_version": "0.4",
            "plan_digest": plan.digest(),
            "provider": plan.provider,
            "profile": plan.capabilities.profile,
            "workload_image": "registry.invalid/evaluate-codex@sha256:" + "1" * 64,
            "workload_image_digest": "1" * 64,
            "gateway_image": "registry.invalid/evaluate-gateway@sha256:" + "2" * 64,
            "gateway_image_digest": "2" * 64,
            "build_input_digest": "3" * 64,
            "runtime_inventory_digest": "4" * 64,
            "launch_policy_digest": "5" * 64,
            "network_policy_digest": "6" * 64,
            "seccomp_policy_digest": "7" * 64,
            "gateway_policy_digest": "8" * 64,
            "observer_policy_digest": "9" * 64,
            "fixture_digest": "a" * 64,
            "cleanup_policy_digest": "b" * 64,
        }
        value.update(changes)
        return dc.DockerExecutionBinding.from_dict(value)

    def docker_enforcement(self, plan, binding, **changes):
        probe_results = dict(self.enforcement(plan).probe_results)
        for claim in self.inventory(False).claims_for(
            "codex", "docker", plan.capabilities.profile
        ).values():
            probe_results.update(
                {probe_id: "PASS" for probe_id in claim.required_probes}
            )
        value = {
            "schema_version": "0.4",
            "execution_binding_digest": binding.digest(),
            "effective_policy_digest": binding.digest(),
            "backend_version": "docker-v0.4",
            "probe_results": probe_results,
        }
        value.update(changes)
        return self.enforcement(plan, **value)

    def test_verified_native_read_only_plan_is_approved(self):
        plan = c.RunPlan.from_dict(self.plan_value())
        inventory = self.inventory()

        decision = ep.assess_run(
            plan,
            self.approval(plan),
            self.enforcement(plan),
            inventory,
            observed_versions=inventory.required_versions,
            observed_platform=inventory.platform,
        )

        self.assertEqual(decision, ep.PolicyDecision("APPROVED", "native", ()))

    def test_missing_runtime_observations_block(self):
        plan = c.RunPlan.from_dict(self.plan_value())
        decision = ep.assess_run(
            plan, self.approval(plan), self.enforcement(plan), self.inventory()
        )
        self.assert_blocked_for(decision, "installed_versions")
        self.assert_blocked_for(decision, "installed_platform")

    def test_platform_fingerprint_must_match_exactly(self):
        plan = c.RunPlan.from_dict(self.plan_value())
        inventory = self.inventory()
        changed = replace(inventory.platform, release="different-release")
        decision = ep.assess_run(
            plan,
            self.approval(plan),
            self.enforcement(plan),
            inventory,
            observed_versions=inventory.required_versions,
            observed_platform=changed,
        )
        self.assert_blocked_for(decision, "installed_platform")

    def test_read_only_requires_inside_workspace_write_denial_probe(self):
        plan = c.RunPlan.from_dict(self.plan_value())
        inventory = self.inventory()
        probes = dict(self.enforcement(plan).probe_results)
        probes.pop("write-inside-workspace", None)
        decision = ep.assess_run(
            plan,
            self.approval(plan),
            self.enforcement(plan, probe_results=probes),
            inventory,
            observed_versions=inventory.required_versions,
            observed_platform=inventory.platform,
        )
        self.assert_blocked_for(
            decision, "enforcement.probe_results.write-inside-workspace"
        )

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

    def test_stale_or_cross_run_receipts_block(self):
        plan = c.RunPlan.from_dict(self.plan_value())
        mismatched_nonce = ep.assess_run(
            plan,
            self.approval(plan),
            self.enforcement(plan, run_nonce="different-run"),
            self.inventory(),
        )
        self.assert_blocked_for(mismatched_nonce, "receipt.run_nonce")

        expired = ep.assess_run(
            plan,
            self.approval(
                plan,
                issued_at="2026-05-31T23:00:00Z",
                expires_at="2026-06-01T00:00:00Z",
            ),
            self.enforcement(
                plan,
                issued_at="2026-05-31T23:00:00Z",
                expires_at="2026-06-01T00:00:00Z",
            ),
            self.inventory(),
            at=datetime(2026, 7, 1, tzinfo=timezone.utc),
        )
        self.assert_blocked_for(expired, "approval.validity")
        self.assert_blocked_for(expired, "enforcement.validity")

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
        with self.assertRaises(c.ContractError):
            c.RunPlan.from_dict(value)

    def test_self_declared_manifest_without_receipt_blocks(self):
        plan = c.RunPlan.from_dict(self.plan_value())
        manifest = {"host_enforced": True, "all_checks": True}

        decision = ep.assess_run(plan, self.approval(plan), manifest, self.inventory())

        self.assert_blocked_for(decision, "enforcement_receipt")

    def test_docker_policy_rejects_native_backend_without_fallback(self):
        self.assertTrue(hasattr(ep, "assess_docker_run"))
        plan = c.RunPlan.from_dict(self.plan_value("native"))

        decision = ep.assess_docker_run(
            plan,
            self.approval(plan),
            self.enforcement(plan),
            object(),
            self.inventory(),
        )

        self.assertEqual(decision.decision, "BLOCKED")
        self.assertIsNone(decision.backend)
        self.assertTrue(any("plan.backend" in reason for reason in decision.reasons))

    def test_docker_policy_blocks_unverified_inventory_or_mismatched_binding(self):
        self.assertTrue(hasattr(ep, "assess_docker_run"))
        plan = c.RunPlan.from_dict(self.plan_value("docker"))
        binding = self.docker_binding(plan)
        enforcement = self.docker_enforcement(plan, binding)

        blocked_inventory = ep.assess_docker_run(
            plan,
            self.approval(plan),
            enforcement,
            binding,
            self.inventory(False),
            observed_versions=self.inventory().required_versions,
            observed_platform=self.inventory().platform,
        )
        self.assert_blocked_for(blocked_inventory, "capabilities.filesystem_read")

        mismatched = self.docker_binding(plan, fixture_digest="c" * 64)
        blocked_binding = ep.assess_docker_run(
            plan,
            self.approval(plan),
            enforcement,
            mismatched,
            self.inventory(),
            observed_versions=self.inventory().required_versions,
            observed_platform=self.inventory().platform,
        )
        self.assert_blocked_for(
            blocked_binding, "enforcement.execution_binding_digest"
        )

        approved = ep.assess_docker_run(
            plan,
            self.approval(plan),
            enforcement,
            binding,
            self.inventory(),
            observed_versions=self.inventory().required_versions,
            observed_platform=self.inventory().platform,
        )
        self.assertEqual(approved, ep.PolicyDecision("APPROVED", "docker", ()))

    def test_historical_native_receipts_remain_parseable_but_not_live_dispatchable(self):
        self.assertTrue(hasattr(ep, "assess_docker_run"))
        plan = c.RunPlan.from_dict(self.plan_value("native"))
        historical = self.enforcement(plan)
        self.assertEqual(historical.schema_version, "0.2")

        decision = ep.assess_docker_run(
            plan,
            self.approval(plan),
            historical,
            object(),
            self.inventory(),
        )

        self.assertEqual(decision.decision, "BLOCKED")
        self.assertIsNone(decision.backend)


if __name__ == "__main__":
    unittest.main()
