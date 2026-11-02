from dataclasses import replace
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import contracts as c
import native_boundary as nb


class NativeBoundaryTests(unittest.TestCase):
    def plan(self):
        return c.RunPlan.from_dict({
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

    def completed(self, status="PASS", observation="denied"):
        return SimpleNamespace(
            returncode=0,
            stdout=json.dumps({"status": status, "observation": observation}),
            stderr="",
        )

    def successful_result(self, workspace, config=None):
        config = config or self.provider_config(workspace)
        with patch("native_boundary.subprocess.run", return_value=self.completed()):
            return nb.run_native_preflight(self.plan(), workspace, config)

    def receipt(self, result, workspace, config):
        return result.to_enforcement_receipt(
            self.plan(),
            config,
            verified_by="trusted-host-verifier",
            verifier_version="1.0",
            issued_at="2026-01-01T00:00:00Z",
            expires_at="2026-01-01T01:00:00Z",
            run_nonce="synthetic-run-nonce",
            prepared_bundle_digest="prepared-bundle-sha256",
            backend_version="native-boundary-v1",
            workspace_id="disposable-workspace-id",
            enabled_tools=("filesystem_read",),
            disabled_tools=("filesystem_write", "shell", "network", "mock_tools"),
            state_verification_method="tree-digest-v1",
            cleanup_method="remove-and-verify-v1",
        )

    def test_read_only_profile_runs_every_relevant_negative_probe(self):
        with TemporaryDirectory() as temp:
            workspace = Path(temp) / "workspace"
            workspace.mkdir()
            config = self.provider_config(workspace)
            with patch("native_boundary.subprocess.run", return_value=self.completed()) as run:
                result = nb.run_native_preflight(self.plan(), workspace, config)

        self.assertEqual(
            result.required_probe_ids,
            (
                "environment-secret",
                "network-egress",
                "read-outside-workspace",
                "secondary-tool-route",
                "write-inside-workspace",
                "write-outside-workspace",
            ),
        )
        self.assertEqual(run.call_count, 6)
        self.assertTrue(result.complete)
        self.assertTrue(all(item.status == "PASS" for item in result.results))

    def test_environment_probe_receives_host_canary_for_launcher_to_strip(self):
        with TemporaryDirectory() as temp:
            workspace = Path(temp) / "workspace"
            workspace.mkdir()
            config = self.provider_config(workspace)
            with patch("native_boundary.subprocess.run", return_value=self.completed()) as run:
                nb.run_native_preflight(self.plan(), workspace, config)

        environment_call = next(
            call
            for call in run.call_args_list
            if any(str(item).endswith("environment_secret.py") for item in call.args[0])
        )
        probe_environment = environment_call.kwargs["env"]
        self.assertIn("SYNTHETIC_PROBE_SECRET", probe_environment)
        self.assertTrue(
            probe_environment["SYNTHETIC_PROBE_SECRET"].startswith(
                "evaluate-skill-host-canary-"
            )
        )

    def test_probe_failure_or_missing_result_blocks_receipt(self):
        with TemporaryDirectory() as temp:
            workspace = Path(temp) / "workspace"
            workspace.mkdir()
            config = self.provider_config(workspace)
            responses = [self.completed()] * 5 + [self.completed("FAIL", "allowed")]
            with patch("native_boundary.subprocess.run", side_effect=responses):
                failed = nb.run_native_preflight(self.plan(), workspace, config)
            with self.assertRaises(nb.BoundaryError):
                self.receipt(failed, workspace, config)

            successful = self.successful_result(workspace, config)
            missing = replace(successful, results=successful.results[:-1])
            with self.assertRaises(nb.BoundaryError):
                self.receipt(missing, workspace, config)

    def test_probe_cannot_be_redefined_by_fixture_or_skill(self):
        with TemporaryDirectory() as temp:
            workspace = Path(temp) / "workspace"
            malicious = workspace / "probes" / "read_outside_workspace.py"
            malicious.parent.mkdir(parents=True)
            malicious.write_text("raise SystemExit('fixture controlled')\n", encoding="utf-8")
            config = self.provider_config(workspace)
            with patch("native_boundary.subprocess.run", return_value=self.completed()) as run:
                nb.run_native_preflight(self.plan(), workspace, config)

        immutable_root = Path(nb.__file__).with_name("probes").resolve()
        for call in run.call_args_list:
            command = call.args[0]
            script = next(Path(item) for item in command if str(item).endswith(".py"))
            self.assertTrue(script.resolve().is_relative_to(immutable_root))
            self.assertNotEqual(script.resolve(), malicious.resolve())

        with TemporaryDirectory() as temp:
            workspace = Path(temp) / "workspace"
            workspace.mkdir()
            config = self.provider_config(workspace)
            spoof_root = workspace / "host-probes"
            spoof_root.mkdir()
            alternate = spoof_root / "fixture_controlled.py"
            alternate.write_text("print('fixture controlled')\n", encoding="utf-8")
            for filename in (
                "environment_secret.py",
                "network_egress.py",
                "read_outside_workspace.py",
                "secondary_tool_route.py",
                "write_inside_workspace.py",
                "write_outside_workspace.py",
            ):
                (spoof_root / filename).symlink_to(alternate)
            with patch.object(nb, "_PROBE_ROOT", spoof_root), patch(
                "native_boundary.subprocess.run", return_value=self.completed()
            ):
                with self.assertRaises(nb.BoundaryError):
                    nb.run_native_preflight(self.plan(), workspace, config)

    def test_probe_output_redacts_environment_values(self):
        with TemporaryDirectory() as temp:
            workspace = Path(temp) / "workspace"
            workspace.mkdir()
            config = self.provider_config(workspace)
            leaked = "synthetic-secret-value"
            with patch(
                "native_boundary.subprocess.run",
                return_value=self.completed("FAIL", leaked),
            ):
                result = nb.run_native_preflight(self.plan(), workspace, config)

        serialized = json.dumps([item.observation for item in result.results])
        self.assertNotIn(leaked, serialized)
        self.assertIn("redacted", serialized)

    def test_provider_config_drift_invalidates_probe_result(self):
        with TemporaryDirectory() as temp:
            workspace = Path(temp) / "workspace"
            workspace.mkdir()
            config = self.provider_config(workspace)
            result = self.successful_result(workspace, config)
            changed = dict(config, sandbox_mode="workspace-write")

            self.assertFalse(result.is_valid_for(self.plan(), changed))
            with self.assertRaises(nb.BoundaryError):
                self.receipt(result, workspace, changed)

    def test_native_boundary_never_claims_connector_or_mcp_isolation_without_probe(self):
        for field, value, gap in (
            ("connectors_enabled", ["github"], "connector-isolation-unprobed"),
            ("mcp_servers", ["external-mcp"], "mcp-isolation-unprobed"),
        ):
            with self.subTest(field=field), TemporaryDirectory() as temp:
                workspace = Path(temp) / "workspace"
                workspace.mkdir()
                config = self.provider_config(workspace)
                config[field] = value
                with patch(
                    "native_boundary.subprocess.run", return_value=self.completed()
                ):
                    result = nb.run_native_preflight(self.plan(), workspace, config)
                self.assertIn(gap, result.unsupported_surfaces)
                self.assertFalse(result.complete)
                with self.assertRaises(nb.BoundaryError):
                    self.receipt(result, workspace, config)


if __name__ == "__main__":
    unittest.main()
