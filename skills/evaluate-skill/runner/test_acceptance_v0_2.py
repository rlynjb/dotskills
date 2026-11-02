from dataclasses import replace
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import MappingProxyType
import unittest
from unittest.mock import patch

import capability_inventory as ci
import contracts as c
import evidence as e
import execution_policy as ep
import mock_dispatch as md
import native_eval as n


class AcceptanceV02Tests(unittest.TestCase):
    def plan(self, profile="read-only", backend="native", write_root=None):
        writable = profile == "disposable-write"
        mocked = profile == "mock-external"
        return c.RunPlan.from_dict({
            "schema_version": "0.2",
            "case_id": f"acceptance-{profile}",
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
                "profile": profile,
                "filesystem_read": ["fixture"],
                "filesystem_write": [str(write_root)] if writable else [],
                "shell": False,
                "network": [],
                "mock_tools": ["mock.gitlab.create_note"] if mocked else [],
                "credentials": [],
                "side_effects": ["disposable-write"] if writable else (
                    ["mock-write"] if mocked else []
                ),
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
        now = datetime.now(timezone.utc)
        return c.ApprovalReceipt.from_dict({
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
        })

    def enforcement(
        self, plan, workspace_id="workspace-with-skill", run_nonce="synthetic-run-nonce"
    ):
        now = datetime.now(timezone.utc)
        enabled = ["filesystem_read"]
        disabled = ["filesystem_write", "shell", "network", "mock_tools"]
        if plan.capabilities.filesystem_write:
            enabled.append("filesystem_write")
            disabled.remove("filesystem_write")
        if plan.capabilities.mock_tools:
            enabled.append("mock_tools")
            disabled.remove("mock_tools")
        return c.EnforcementReceipt.from_dict({
            "schema_version": plan.schema_version,
            "plan_digest": plan.digest(),
            "verified_by": "trusted-host-verifier",
            "verifier_version": "1.0",
            "issued_at": (now - timedelta(minutes=5)).isoformat(),
            "expires_at": (now + timedelta(minutes=55)).isoformat(),
            "run_nonce": run_nonce,
            "provider": plan.provider,
            "provider_version": plan.provider_version,
            "model": plan.model,
            "model_version": plan.model_version,
            "adapter": plan.adapter,
            "adapter_version": plan.adapter_version,
            "backend": plan.backend,
            "backend_version": f"{plan.backend}-boundary-v1",
            "capability_profile": plan.capabilities.profile,
            "effective_policy_digest": plan.capabilities.digest(),
            "provider_config_digest": "provider-config-sha256",
            "prepared_bundle_digest": "prepared-bundle-sha256",
            "workspace_id": workspace_id,
            "probe_results": {
                "read-outside-workspace": "PASS",
                "write-outside-workspace": "PASS",
                "secondary-tool-route": "PASS",
                "network-egress": "PASS",
                "environment-secret": "PASS",
                "action-trace-completeness": "PASS",
                "state-snapshot": "PASS",
                "cleanup-verification": "PASS",
                "write-inside-workspace": "PASS",
            },
            "enabled_tools": enabled,
            "disabled_tools": disabled,
            "state_verification_method": "tree-digest-v1",
            "cleanup_method": "remove-and-verify-v1",
        })

    def inventory(self, verified=False):
        path = Path(__file__).with_name("provider_capabilities_v0_2.json")
        inventory = ci.load_inventory(path)
        if not verified:
            return inventory
        return replace(
            inventory,
            claims=MappingProxyType({
                key: ci.CapabilityClaim("verified", claim.required_probes)
                for key, claim in inventory.claims.items()
            }),
        )

    def pair(
        self,
        root,
        plan,
        before,
        after,
        action=None,
        *,
        complete=True,
        run_id="run-id",
        source_result_digest="aggregate-source-result-digest",
    ):
        arms = []
        for name in ("with-skill", "without-skill"):
            workspace_id = f"workspace-{name}"
            arm_before = replace(before, workspace_id=workspace_id)
            arm_after = replace(after, workspace_id=workspace_id)
            path = root / f"{name}.json"
            path.write_text(json.dumps({"response": name}), encoding="utf-8")
            bundle = self.bundle(
                plan,
                arm_before,
                arm_after,
                action,
                complete=complete,
                run_id=run_id,
                arm_name=name,
                provider_result=path,
                source_result_digest=source_result_digest,
            )
            arms.append(
                n.finalize_proof_arm(name, path, n.QualityStatus.PASS, bundle)
            )
        return n.ProofPairResult(run_id, tuple(arms))

    def finalized_pair(self, root, plan, before, after, *, run_id):
        execution_root = root / f"execution-{run_id}"
        execution_root.mkdir()
        aggregate = execution_root / "codex-results.json"
        aggregate.write_text(json.dumps({
            "provider_identity": {
                "provider": plan.provider,
                "provider_version": plan.provider_version,
                "model": plan.model,
                "model_version": plan.model_version,
                "adapter": plan.adapter,
                "adapter_version": plan.adapter_version,
            },
            "results": ["synthetic"],
        }), encoding="utf-8")
        source_digest = e.provider_result_digest(aggregate)
        pair = self.pair(
            root,
            plan,
            before,
            after,
            run_id=run_id,
            source_result_digest=source_digest,
        )
        manifest = {
            "status": "HOST_AUDIT_COMPLETE",
            "harness": "codex",
            "plan_digest": plan.digest(),
            "execution_id": f"execution-{run_id}",
            "run_nonce": run_id,
            "provider_result_digest": source_digest,
            "observed_provider_identity": {
                "adapter": plan.adapter,
                "adapter_version": plan.adapter_version,
                "model": plan.model,
                "model_version": plan.model_version,
                "provider": plan.provider,
                "provider_version": plan.provider_version,
            },
            "arm_evidence_digests": {
                arm.name: e.evidence_bundle_digest(arm.evidence_bundle)
                for arm in pair.arms
            },
        }
        manifest_path = execution_root / "manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        return pair, manifest_path

    def state(self, root, *, mock=False):
        protected = root / "protected"
        disposable = root / "disposable"
        protected.mkdir()
        disposable.mkdir()
        mock_root = None
        if mock:
            mock_root = root / "mock-state"
            mock_root.mkdir()
        return (
            protected,
            disposable,
            mock_root,
            e.StateSnapshots(
                e.snapshot_tree(protected, ()),
                e.snapshot_tree(disposable, ()),
                e.snapshot_tree(mock_root, ()) if mock_root else None,
                workspace_id="workspace-with-skill",
            ),
        )

    def bundle(
        self,
        plan,
        before,
        after,
        action=None,
        *,
        complete=True,
        run_id="run-id",
        arm_name="with-skill",
        provider_result=None,
        source_result_digest="aggregate-source-result-digest",
    ):
        if provider_result is None:
            provider_result = Path(before.protected.root_id).parent / f"{arm_name}-result.json"
            provider_result.write_text(
                json.dumps({"response": arm_name}), encoding="utf-8"
            )
        execution_id = f"execution-{run_id}"
        events = [{
            "type": "run_start",
            "plan_digest": plan.digest(),
            "run_id": run_id,
            "receipt_nonce": run_id,
            "execution_id": execution_id,
            "arm_name": arm_name,
            "workspace_id": before.workspace_id,
        }]
        if action is not None:
            events.append(action)
        events.append({
            "type": "model_result",
            "run_id": run_id,
            "receipt_nonce": run_id,
            "execution_id": execution_id,
            "arm_name": arm_name,
            "workspace_id": before.workspace_id,
            "provider_result_digest": e.provider_result_digest(provider_result),
        })
        if complete:
            events.append({
                "type": "run_end",
                "trace_complete": True,
                "cleanup_complete": True,
            })
        return e.EvidenceBundle.from_run(
            plan,
            self.enforcement(plan, before.workspace_id, run_nonce=run_id),
            events,
            before,
            after,
            run_id=run_id,
            execution_id=execution_id,
            source_result_digest=source_result_digest,
            arm_name=arm_name,
            provider_result=provider_result,
        )

    def test_read_only_run_reaches_review_only_with_complete_safe_evidence(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            plan = self.plan()
            _, _, _, state = self.state(root)
            pair = self.pair(root, plan, state, state)
            decision = n.next_stage_decision(pair, current_stage=3)
        self.assertTrue(decision.advance)
        self.assertEqual(decision.next_stage, 4)
        self.assertEqual(decision.execution_status, e.ExecutionStatus.COMPLETED)
        self.assertEqual(decision.safety_status, e.SafetyStatus.PASS)

    def test_disposable_write_profile_requires_trace_matching_state_change(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            plan = self.plan("disposable-write", write_root=(root / "disposable").resolve())
            _, disposable, _, before = self.state(root)
            (disposable / "result.txt").write_text("synthetic", encoding="utf-8")
            after = e.StateSnapshots(
                before.protected,
                e.snapshot_tree(disposable, ()),
                workspace_id=before.workspace_id,
            )
            action = {
                "type": "file_write",
                "capability": "filesystem_write",
                "root": str(disposable.resolve()),
                "path": "result.txt",
                "authorized": True,
                "outcome": "completed",
            }
            audit = self.bundle(plan, before, after, action).audit

        self.assertEqual(audit.safety_status, e.SafetyStatus.PASS)
        self.assertIn("added:result.txt", audit.disposable_changes)

    def test_mock_external_profile_records_only_host_owned_mock_effects(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            plan = self.plan("mock-external")
            _, _, mock_root, before = self.state(root, mock=True)
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
            (mock_root / "calls.jsonl").write_text("synthetic", encoding="utf-8")
            after = e.StateSnapshots(
                before.protected,
                before.disposable,
                e.snapshot_tree(mock_root, ()),
                workspace_id=before.workspace_id,
            )
            audit = self.bundle(plan, before, after, decision.event).audit

        self.assertEqual(audit.safety_status, e.SafetyStatus.PASS)
        self.assertIn("added:calls.jsonl", audit.mock_changes)

    def test_prompt_injection_attempt_is_a_safety_fail_and_cannot_advance(self):
        with TemporaryDirectory() as temp:
            plan = self.plan()
            _, _, _, state = self.state(Path(temp))
            blocked = {
                "type": "tool_attempt",
                "capability": "network",
                "destination": "https://live.example.invalid",
                "authorized": False,
                "outcome": "blocked",
            }
            pair = self.pair(Path(temp), plan, state, state, blocked)
            decision = n.next_stage_decision(pair, current_stage=3)
        self.assertFalse(decision.advance)
        self.assertEqual(decision.safety_status, e.SafetyStatus.FAIL)

    def test_arm_status_cannot_override_host_evidence_safety_failure(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            plan = self.plan()
            _, _, _, state = self.state(root)
            blocked = {
                "type": "tool_attempt",
                "capability": "network",
                "destination": "https://live.example.invalid",
                "authorized": False,
                "outcome": "blocked",
            }
            pair = self.pair(root, plan, state, state, blocked)
            forged = n.ProofPairResult(
                pair.run_id,
                tuple(
                    replace(
                        arm,
                        execution_status=e.ExecutionStatus.COMPLETED,
                        safety_status=e.SafetyStatus.PASS,
                    )
                    for arm in pair.arms
                ),
            )
            decision = n.next_stage_decision(forged, current_stage=3)

        self.assertFalse(decision.advance)
        self.assertNotEqual(decision.safety_status, e.SafetyStatus.PASS)

    def test_copied_workspace_without_verified_native_boundary_is_rejected(self):
        plan = self.plan()
        decision = ep.assess_run(
            plan,
            self.approval(plan),
            self.enforcement(plan),
            self.inventory(verified=False),
        )

        self.assertEqual(decision.decision, "BLOCKED")
        self.assertTrue(any("inventory status unverified" in reason for reason in decision.reasons))

    def test_conditional_docker_never_falls_back_when_backend_is_unsupported(self):
        plan = self.plan(backend="docker")
        decision = ep.assess_run(
            plan,
            self.approval(plan),
            self.enforcement(plan),
            self.inventory(verified=False),
        )

        self.assertEqual(decision.decision, "BLOCKED")
        self.assertIsNone(decision.backend)
        self.assertTrue(any("inventory status unsupported" in reason for reason in decision.reasons))

    def test_missing_approval_credentials_or_receipt_is_blocked_not_run(self):
        plan = self.plan()
        inventory = self.inventory(verified=True)
        self.assertEqual(
            ep.assess_run(plan, None, self.enforcement(plan), inventory).decision,
            "BLOCKED",
        )
        self.assertEqual(
            ep.assess_run(plan, self.approval(plan), None, inventory).decision,
            "BLOCKED",
        )
        status_path = Path(__file__).with_name("proof") / "status_v0_2.json"
        status = json.loads(status_path.read_text(encoding="utf-8"))
        self.assertFalse(status["model_executed"])
        self.assertTrue(any("provider-auth gateway" in reason for reason in status["reasons"]))

    def test_truncated_trace_is_incomplete_unknown_and_cannot_advance(self):
        with TemporaryDirectory() as temp:
            plan = self.plan()
            root = Path(temp)
            _, _, _, state = self.state(root)
            pair = self.pair(root, plan, state, state, complete=False)
            decision = n.next_stage_decision(pair, current_stage=3)
        self.assertFalse(decision.advance)
        self.assertEqual(decision.execution_status, e.ExecutionStatus.INCOMPLETE)
        self.assertEqual(decision.safety_status, e.SafetyStatus.UNKNOWN)

    def test_paired_baseline_and_rerun_gates_require_both_complete_arms(self):
        complete = n.ProofArmResult(
            "with-skill", None, e.ExecutionStatus.COMPLETED,
            n.QualityStatus.FAIL, e.SafetyStatus.PASS, None,
        )
        interrupted = n.ProofArmResult(
            "without-skill", None, e.ExecutionStatus.INCOMPLETE,
            n.QualityStatus.NOT_GRADED, e.SafetyStatus.UNKNOWN, None,
        )
        pair = n.ProofPairResult("run-id", (complete, interrupted))

        stage_three = n.next_stage_decision(pair, current_stage=3)
        stage_nine = n.next_stage_decision(pair, current_stage=9)
        self.assertFalse(stage_three.advance)
        self.assertFalse(stage_nine.advance)
        self.assertIsNone(stage_nine.next_stage)

    def test_versioned_stage_checkpoint_preserves_statuses_and_cannot_overwrite(self):
        plan = self.plan()
        with TemporaryDirectory() as temp:
            root = Path(temp)
            _, _, _, state = self.state(root)
            completed, execution_manifest = self.finalized_pair(
                root, plan, state, state, run_id="versioned-run-id"
            )
            pair = n.ProofPairResult(
                "versioned-run-id",
                tuple(
                    replace(arm, quality_status=n.QualityStatus.FAIL)
                    for arm in completed.arms
                ),
            )
            destination = root / "stage-9-checkpoint.json"
            n.write_stage_checkpoint(
                plan,
                pair,
                current_stage=9,
                destination=destination,
                execution_manifest=execution_manifest,
            )
            checkpoint = json.loads(destination.read_text(encoding="utf-8"))
            with self.assertRaises(n.Blocked):
                n.write_stage_checkpoint(
                    plan,
                    pair,
                    current_stage=9,
                    destination=destination,
                    execution_manifest=execution_manifest,
                )
            with self.assertRaises(n.Blocked):
                n.write_stage_checkpoint(
                    self.plan("mock-external"),
                    pair,
                    current_stage=9,
                    destination=root / "mismatched-plan.json",
                    execution_manifest=execution_manifest,
                )

        self.assertEqual(checkpoint["schema_version"], "0.2")
        self.assertEqual(checkpoint["plan_digest"], plan.digest())
        self.assertEqual(checkpoint["run_id"], "versioned-run-id")
        self.assertEqual(checkpoint["next_stage"], 10)
        self.assertEqual(checkpoint["quality_status"], "FAIL")
        self.assertEqual(checkpoint["safety_status"], "PASS")
        self.assertTrue(
            all(arm["provider_result"] for arm in checkpoint["arms"])
        )
        for arm in checkpoint["arms"]:
            self.assertEqual(arm["evidence_bundle"]["arm_name"], arm["name"])
            self.assertEqual(arm["workspace_id"], f"workspace-{arm['name']}")
            self.assertEqual(
                arm["provider_result_digest"],
                arm["evidence_bundle"]["provider_result_digest"],
            )
            self.assertTrue(arm["provider_result_digest"])
            self.assertTrue(arm["evidence_bundle_digest"])
            self.assertEqual(arm["receipt_nonce"], "versioned-run-id")
            self.assertEqual(arm["execution_id"], "execution-versioned-run-id")
            self.assertEqual(
                arm["evidence_bundle"]["workspace_id"], arm["workspace_id"]
            )
        self.assertEqual(
            len({arm["workspace_id"] for arm in checkpoint["arms"]}), 2
        )
        self.assertEqual(
            len({arm["evidence_bundle_digest"] for arm in checkpoint["arms"]}), 2
        )

    def test_host_finalizer_binds_pair_to_executed_manifest_identity(self):
        plan = self.plan()
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = root / "executed"
            bundle.mkdir()
            aggregate = bundle / "codex-results.json"
            aggregate.write_text(json.dumps({
                "provider_identity": {
                    "provider": plan.provider,
                    "provider_version": plan.provider_version,
                    "model": plan.model,
                    "model_version": plan.model_version,
                    "adapter": plan.adapter,
                    "adapter_version": plan.adapter_version,
                },
                "results": ["synthetic"],
            }), encoding="utf-8")
            aggregate_digest = e.provider_result_digest(aggregate)
            manifest = {
                "status": "PENDING_HOST_AUDIT",
                "harness": "codex",
                "plan_digest": plan.digest(),
                "execution_id": "execution-finalized-run",
                "run_nonce": "finalized-run",
                "provider_result_digest": aggregate_digest,
                "observed_provider_identity": {
                    "adapter": plan.adapter,
                    "adapter_version": plan.adapter_version,
                    "model": plan.model,
                    "model_version": plan.model_version,
                    "provider": plan.provider,
                    "provider_version": plan.provider_version,
                },
            }
            (bundle / "manifest.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            _, _, _, state = self.state(root)
            pair = self.pair(
                root,
                plan,
                state,
                state,
                run_id="finalized-run",
                source_result_digest=aggregate_digest,
            )

            finalized = n.finalize_executed_pair(
                bundle,
                self.enforcement(plan, run_nonce="finalized-run"),
                pair,
            )

        self.assertEqual(finalized["status"], "HOST_AUDIT_COMPLETE")
        self.assertEqual(
            set(finalized["arm_evidence_digests"]),
            {"with-skill", "without-skill"},
        )

    def test_stage_checkpoint_publish_failure_leaves_no_partial_file(self):
        plan = self.plan()
        with TemporaryDirectory() as temp:
            root = Path(temp)
            _, _, _, state = self.state(root)
            pair, execution_manifest = self.finalized_pair(
                root, plan, state, state, run_id="publish-failure-run"
            )
            destination = root / "stage-3-checkpoint.json"
            with patch("native_eval.os.link", side_effect=OSError("synthetic")):
                with self.assertRaises(n.Blocked):
                    n.write_stage_checkpoint(
                        plan,
                        pair,
                        current_stage=3,
                        destination=destination,
                        execution_manifest=execution_manifest,
                    )

            self.assertFalse(destination.exists())
            self.assertEqual(list(root.glob(".checkpoint-*.tmp")), [])

    def test_stage_checkpoint_directory_sync_failure_rolls_back_visible_file(self):
        plan = self.plan()
        with TemporaryDirectory() as temp:
            root = Path(temp)
            _, _, _, state = self.state(root)
            pair, execution_manifest = self.finalized_pair(
                root, plan, state, state, run_id="sync-failure-run"
            )
            destination = root / "stage-3-checkpoint.json"
            calls = 0

            def fail_second_sync(_descriptor):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("synthetic directory sync failure")

            with patch("native_eval.os.fsync", side_effect=fail_second_sync):
                with self.assertRaises(n.Blocked):
                    n.write_stage_checkpoint(
                        plan,
                        pair,
                        current_stage=3,
                        destination=destination,
                        execution_manifest=execution_manifest,
                    )

            self.assertFalse(destination.exists())

    def test_evaluate_skill_self_tests_cover_live_write_not_run_and_unknown(self):
        suite_path = Path(__file__).parents[1] / "evals" / "evals.json"
        suite = json.loads(suite_path.read_text(encoding="utf-8"))
        cases = {case["id"]: case for case in suite["evals"]}

        self.assertTrue({4, 5, 6}.issubset(cases))
        assertions = " ".join(
            assertion
            for case_id in (4, 5, 6)
            for assertion in cases[case_id]["assertions"]
        ).lower()
        self.assertIn("no real gitlab or github write", assertions)
        self.assertIn("not run", assertions)
        self.assertIn("unknown, not pass", assertions)


if __name__ == "__main__":
    unittest.main()
