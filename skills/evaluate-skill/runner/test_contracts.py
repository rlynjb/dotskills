import copy
import unittest

import contracts as c


class ContractTests(unittest.TestCase):
    def run_plan_value(self):
        return {
            "schema_version": "0.2",
            "case_id": "learn-repo-read-only",
            "case_revision": "case-sha256",
            "rubric_revision": "rubric-sha256",
            "skill_revision": "skill-sha256",
            "fixture_revision": "fixture-sha256",
            "provider": "openai",
            "provider_version": "codex-cli-0.163.0",
            "model": "approved-model",
            "model_version": "approved-model-snapshot",
            "adapter": "promptfoo-codex-sdk",
            "adapter_version": "0.125.1",
            "backend": "native",
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

    def approval_value(self, plan):
        return {
            "schema_version": "0.2",
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

    def enforcement_value(self, plan):
        return {
            "schema_version": "0.2",
            "plan_digest": plan.digest(),
            "verified_by": "trusted-host-verifier",
            "verifier_version": "1.0",
            "provider": plan.provider,
            "model": plan.model,
            "adapter": plan.adapter,
            "adapter_version": plan.adapter_version,
            "backend": plan.backend,
            "backend_version": "macos-seatbelt-verified",
            "capability_profile": plan.capabilities.profile,
            "effective_policy_digest": "policy-sha256",
            "workspace_id": "disposable-workspace-id",
            "probe_results": {
                "read-outside-workspace": "PASS",
                "write-outside-workspace": "PASS",
            },
            "enabled_tools": ["read"],
            "disabled_tools": ["write", "network"],
            "state_verification_method": "tree-digest-v1",
            "cleanup_method": "remove-and-verify-v1",
        }

    def test_run_plan_digest_is_stable_for_key_order(self):
        original = self.run_plan_value()
        reordered = dict(reversed(list(original.items())))
        reordered["capabilities"] = dict(
            reversed(list(original["capabilities"].items()))
        )
        reordered["resource_limits"] = dict(
            reversed(list(original["resource_limits"].items()))
        )

        self.assertEqual(
            c.RunPlan.from_dict(original).digest(),
            c.RunPlan.from_dict(reordered).digest(),
        )

    def test_run_plan_digest_changes_for_any_material_field(self):
        original = self.run_plan_value()
        original_digest = c.RunPlan.from_dict(original).digest()
        mutations = {
            "schema version": ("schema_version", "0.3"),
            "case revision": ("case_revision", "changed"),
            "rubric revision": ("rubric_revision", "changed"),
            "skill revision": ("skill_revision", "changed"),
            "fixture revision": ("fixture_revision", "changed"),
            "provider": ("provider", "changed"),
            "provider version": ("provider_version", "changed"),
            "model": ("model", "changed"),
            "model version": ("model_version", "changed"),
            "adapter": ("adapter", "changed"),
            "adapter version": ("adapter_version", "changed"),
            "backend": ("backend", "docker"),
            "comparison arms": ("comparison_arms", ["with-skill"]),
            "evidence requirements": ("evidence_requirements", ["host-audit"]),
            "cleanup requirements": ("cleanup_requirements", ["state-verified"]),
        }
        for name, (field, value) in mutations.items():
            with self.subTest(field=name):
                changed = copy.deepcopy(original)
                changed[field] = value
                self.assertNotEqual(c.RunPlan.from_dict(changed).digest(), original_digest)

        nested_mutations = {
            "capability surfaces": ("capabilities", "filesystem_read", ["other"]),
            "resource limits": ("resource_limits", "max_turns", 11),
        }
        for name, (parent, field, value) in nested_mutations.items():
            with self.subTest(field=name):
                changed = copy.deepcopy(original)
                changed[parent][field] = value
                self.assertNotEqual(c.RunPlan.from_dict(changed).digest(), original_digest)

    def test_run_plan_rejects_unknown_profile_or_backend(self):
        for field, value in (("backend", "automatic"),):
            with self.subTest(field=field):
                data = self.run_plan_value()
                data[field] = value
                with self.assertRaises(c.ContractError):
                    c.RunPlan.from_dict(data)
        for profile in ("full-access", "read-write", ""):
            with self.subTest(profile=profile):
                data = self.run_plan_value()
                data["capabilities"]["profile"] = profile
                with self.assertRaises(c.ContractError):
                    c.RunPlan.from_dict(data)

    def test_run_plan_requires_version_and_resource_pins(self):
        required_pins = (
            "schema_version",
            "case_revision",
            "rubric_revision",
            "skill_revision",
            "fixture_revision",
            "provider_version",
            "model_version",
            "adapter_version",
            "resource_limits",
        )
        for field in required_pins:
            with self.subTest(field=field):
                data = self.run_plan_value()
                del data[field]
                with self.assertRaises(c.ContractError):
                    c.RunPlan.from_dict(data)
        for field in ("max_seconds", "max_turns", "max_output_bytes", "max_cost_usd"):
            with self.subTest(resource=field):
                data = self.run_plan_value()
                del data["resource_limits"][field]
                with self.assertRaises(c.ContractError):
                    c.RunPlan.from_dict(data)

    def test_approval_receipt_must_match_plan_digest_and_scope(self):
        plan = c.RunPlan.from_dict(self.run_plan_value())
        receipt = c.ApprovalReceipt.from_dict(self.approval_value(plan))
        receipt.validate_for(plan)

        for field, value in (
            ("plan_digest", "wrong-digest"),
            ("provider", "wrong-provider"),
            ("model", "wrong-model"),
            ("adapter", "wrong-adapter"),
            ("backend", "docker"),
            ("capability_profile", "no-tool"),
            ("capability_digest", "wrong-capabilities"),
            ("side_effects", ["live-write"]),
        ):
            with self.subTest(field=field):
                value_dict = self.approval_value(plan)
                value_dict[field] = value
                mismatched = c.ApprovalReceipt.from_dict(value_dict)
                with self.assertRaises(c.ContractError):
                    mismatched.validate_for(plan)

    def test_enforcement_receipt_requires_independent_verifier_and_probe_results(self):
        plan = c.RunPlan.from_dict(self.run_plan_value())
        c.EnforcementReceipt.from_dict(self.enforcement_value(plan))

        for field, value in (
            ("verified_by", ""),
            ("verified_by", plan.provider),
            ("verified_by", plan.adapter),
            ("probe_results", {}),
        ):
            with self.subTest(field=field, value=value):
                data = self.enforcement_value(plan)
                data[field] = value
                with self.assertRaises(c.ContractError):
                    c.EnforcementReceipt.from_dict(data)

    def test_contract_rejects_unknown_fields(self):
        plan_data = self.run_plan_value()
        plan = c.RunPlan.from_dict(plan_data)
        examples = (
            (c.RunPlan.from_dict, plan_data),
            (c.CapabilityRequirements.from_dict, plan_data["capabilities"]),
            (c.ApprovalReceipt.from_dict, self.approval_value(plan)),
            (c.EnforcementReceipt.from_dict, self.enforcement_value(plan)),
        )
        for loader, value in examples:
            with self.subTest(loader=loader.__qualname__):
                changed = copy.deepcopy(value)
                changed["unexpected"] = True
                with self.assertRaises(c.ContractError):
                    loader(changed)


if __name__ == "__main__":
    unittest.main()
