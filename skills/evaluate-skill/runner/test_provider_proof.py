from dataclasses import replace
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import MappingProxyType
import unittest

import capability_inventory as ci
import contracts as c
import evidence as e
import native_boundary as nb
import native_eval as n


class ProviderProofTests(unittest.TestCase):
    def plan(self):
        return c.RunPlan.from_dict({
            "schema_version": "0.2",
            "case_id": "synthetic-read-only",
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
        })

    def approval(self, plan):
        return c.ApprovalReceipt.from_dict({
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
        })

    def enforcement(self, plan):
        return c.EnforcementReceipt.from_dict({
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
            "backend_version": "native-boundary-v1",
            "capability_profile": plan.capabilities.profile,
            "effective_policy_digest": plan.capabilities.digest(),
            "workspace_id": "disposable-workspace-id",
            "probe_results": {
                "read-outside-workspace": "PASS",
                "write-outside-workspace": "PASS",
                "secondary-tool-route": "PASS",
                "network-egress": "PASS",
                "environment-secret": "PASS",
                "action-trace-completeness": "PASS",
                "state-snapshot": "PASS",
                "cleanup-verification": "PASS",
            },
            "enabled_tools": ["filesystem_read"],
            "disabled_tools": ["filesystem_write", "shell", "network", "mock_tools"],
            "state_verification_method": "tree-digest-v1",
            "cleanup_method": "remove-and-verify-v1",
        })

    def inventory(self):
        path = Path(__file__).with_name("provider_capabilities_v0_2.json")
        inventory = ci.load_inventory(path)
        claims = {
            key: ci.CapabilityClaim("verified", claim.required_probes)
            for key, claim in inventory.claims.items()
        }
        return replace(inventory, claims=MappingProxyType(claims))

    def provider_config(self, workspace):
        outside = workspace.parent / "host-owned-probe-target"
        return {
            "provider": "openai",
            "provider_version": "0.163.0",
            "adapter": "promptfoo-codex-sdk",
            "adapter_version": "0.125.1",
            "backend": "native",
            "profile": "read-only",
            "sandbox_mode": "read-only",
            "boundary_launcher": ["/trusted/native-boundary-launcher"],
            "outside_read_path": str(outside / "read-canary"),
            "outside_write_path": str(outside / "write-canary"),
            "network_host": "192.0.2.1",
            "network_port": 9,
            "secret_names": ["SYNTHETIC_PROBE_SECRET"],
            "forbidden_commands": ["curl", "sh"],
            "connectors_enabled": [],
            "mcp_servers": [],
        }

    def boundary_result(self, plan, config):
        digest = nb.provider_config_digest(config)
        probe_ids = (
            "environment-secret",
            "network-egress",
            "read-outside-workspace",
            "secondary-tool-route",
            "write-outside-workspace",
        )
        results = tuple(
            nb.ProbeResult(probe_id, "boundary", "PASS", "denied", digest)
            for probe_id in probe_ids
        )
        return nb.NativeBoundaryResult(plan.digest(), digest, probe_ids, results, ())

    def source_tree(self, root):
        fixture = root / "approved-fixture"
        fixture.mkdir()
        (fixture / "input.txt").write_text("synthetic fixture", encoding="utf-8")
        skill = root / "test-skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text(
            "---\nname: test-skill\ndescription: synthetic\n---\nUse the fixture.\n",
            encoding="utf-8",
        )
        return fixture, skill

    def prepare(self, root):
        plan = self.plan()
        fixture, skill = self.source_tree(root)
        provider_config = self.provider_config(root)
        result = n.prepare_provider_proof(
            plan,
            self.approval(plan),
            self.enforcement(plan),
            self.inventory(),
            self.boundary_result(plan, provider_config),
            provider_config,
            fixture,
            skill,
            root / "proof-runs",
        )
        return result, fixture, skill

    def state_bundle(self, root, plan):
        protected = root / "protected"
        disposable = root / "disposable"
        protected.mkdir()
        disposable.mkdir()
        (protected / "source.txt").write_text("unchanged", encoding="utf-8")
        state = e.StateSnapshots(
            e.snapshot_tree(protected, ()),
            e.snapshot_tree(disposable, ()),
        )
        events = [
            {"type": "run_start", "plan_digest": plan.digest()},
            {"type": "run_end", "trace_complete": True, "cleanup_complete": True},
        ]
        return e.EvidenceBundle.from_run(
            plan, self.enforcement(plan), events, state, state
        )

    def test_each_arm_gets_independent_equivalent_fixture(self):
        with TemporaryDirectory() as temp:
            proof, _, _ = self.prepare(Path(temp))
            with_skill, without_skill = proof.arms
            with_input = with_skill.workspace / "fixture" / "input.txt"
            without_input = without_skill.workspace / "fixture" / "input.txt"

            self.assertEqual(with_skill.fixture_digest, without_skill.fixture_digest)
            self.assertEqual(with_input.read_text(), without_input.read_text())
            self.assertNotEqual(with_input, without_input)
            self.assertNotEqual(with_input.stat().st_ino, without_input.stat().st_ino)
            self.assertTrue((with_skill.workspace / ".agents" / "skills" / "test-skill" / "SKILL.md").is_file())
            self.assertFalse((without_skill.workspace / ".agents").exists())

    def test_answer_key_and_prior_results_are_absent_from_both_arms(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "answer-key.json").write_text("secret rubric", encoding="utf-8")
            (root / "prior-results.json").write_text("old output", encoding="utf-8")
            proof, _, _ = self.prepare(root)

            for arm in proof.arms:
                names = {path.name for path in arm.workspace.rglob("*")}
                self.assertNotIn("answer-key.json", names)
                self.assertNotIn("prior-results.json", names)
                self.assertNotIn("evals.json", names)

    def test_provider_auth_is_not_in_agent_environment_or_trace(self):
        secret = "synthetic-provider-secret"
        driver_environment = {"PATH": "/approved/bin", "OPENAI_API_KEY": secret}
        agent_environment = n.agent_environment(
            driver_environment, provider_auth_keys=("OPENAI_API_KEY",)
        )
        events = ({"type": "model_result", "detail": f"redact {secret}"},)
        sanitized = n.sanitize_provider_trace(
            events, {"OPENAI_API_KEY": secret}
        )

        self.assertNotIn("OPENAI_API_KEY", agent_environment)
        self.assertNotIn(secret, json.dumps(agent_environment))
        self.assertNotIn(secret, json.dumps(sanitized))

    def test_native_result_without_host_audit_is_incomplete(self):
        with TemporaryDirectory() as temp:
            result = Path(temp) / "provider-result.json"
            result.write_text("{}", encoding="utf-8")
            arm = n.finalize_proof_arm(
                "with-skill", result, n.QualityStatus.PASS, None
            )

        self.assertEqual(arm.execution_status, e.ExecutionStatus.INCOMPLETE)
        self.assertEqual(arm.quality_status, n.QualityStatus.PASS)
        self.assertEqual(arm.safety_status, e.SafetyStatus.UNKNOWN)

    def test_complete_provider_result_and_host_audit_preserve_three_status_dimensions(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            result = root / "provider-result.json"
            result.write_text("{}", encoding="utf-8")
            plan = self.plan()
            bundle = self.state_bundle(root, plan)
            arm = n.finalize_proof_arm(
                "with-skill", result, n.QualityStatus.PASS, bundle
            )

        self.assertEqual(arm.execution_status, e.ExecutionStatus.COMPLETED)
        self.assertEqual(arm.quality_status, n.QualityStatus.PASS)
        self.assertEqual(arm.safety_status, e.SafetyStatus.PASS)

    def test_interrupted_arm_does_not_mark_pair_completed(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            result = root / "provider-result.json"
            result.write_text("{}", encoding="utf-8")
            plan = self.plan()
            completed = n.finalize_proof_arm(
                "with-skill", result, n.QualityStatus.PASS, self.state_bundle(root, plan)
            )
            interrupted = n.finalize_proof_arm(
                "without-skill", None, n.QualityStatus.NOT_GRADED, None
            )
            pair = n.ProofPairResult("run-id", (completed, interrupted))

        self.assertEqual(pair.execution_status, e.ExecutionStatus.INCOMPLETE)
        self.assertFalse(pair.completed)
        self.assertEqual(interrupted.quality_status, n.QualityStatus.NOT_GRADED)


if __name__ == "__main__":
    unittest.main()
