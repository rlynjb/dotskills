import json
import os
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import capability_inventory as ci
import codex_host as ch
import contracts as c
import native_boundary as nb
import native_eval as ne


class CodexHostPolicyTests(unittest.TestCase):
    def paths(self, root):
        root = Path(root)
        workspace = root / "workspace"
        workspace.mkdir()
        command_line_tools = root / "CommandLineTools"
        command_line_tools.mkdir()
        home = root / "home"
        home.mkdir()
        protected = root / "protected"
        protected.mkdir()
        codex = root / "codex"
        codex.write_text("binary placeholder\n", encoding="utf-8")
        codex.chmod(0o700)
        return workspace, command_line_tools, home, protected, codex

    def policy(self, root, **overrides):
        workspace, command_line_tools, home, protected, codex = self.paths(root)
        arguments = {
            "workspace": workspace,
            "codex_path": codex,
            "command_line_tools_root": command_line_tools,
            "home": home,
            "mcp_servers": ("cua_repl", "node_repl"),
            "protected_roots": (protected,),
        }
        arguments.update(overrides)
        return ch.compile_read_only_policy(**arguments)

    def test_compiled_policy_is_canonical_root_deny_read_only_and_network_off(self):
        with TemporaryDirectory() as temp:
            policy = self.policy(temp)
            profile = policy.cli_config["permissions"][policy.profile_name]

            self.assertEqual(profile["filesystem"][":root"], "deny")
            self.assertEqual(profile["filesystem"][":minimal"], "read")
            self.assertEqual(
                profile["filesystem"][":workspace_roots"],
                {".": "read"},
            )
            self.assertEqual(
                profile["filesystem"][str(policy.command_line_tools_root)], "read"
            )
            self.assertEqual(profile["network"], {"enabled": False})
            canonical_profile = policy.canonical_payload()["cli_config"]["permissions"][
                policy.profile_name
            ]
            self.assertNotIn("write", json.dumps(canonical_profile, sort_keys=True))
            self.assertEqual(policy.cli_config["default_permissions"], policy.profile_name)
            self.assertEqual(policy.digest(), policy.digest())

    def test_compiled_policy_disables_every_mcp_web_apps_collaboration_and_skills(self):
        with TemporaryDirectory() as temp:
            policy = self.policy(temp)

            self.assertEqual(
                policy.cli_config["mcp_servers"],
                {
                    "cua_repl": {"enabled": False},
                    "node_repl": {"enabled": False},
                },
            )
            self.assertEqual(policy.cli_config["web_search"], "disabled")
            features = policy.cli_config["features"]
            self.assertFalse(features["apps"])
            self.assertFalse(features["multi_agent"])
            self.assertFalse(features["multi_agent_v2"])
            self.assertFalse(features["computer_use"])
            self.assertFalse(features["skill_search"])
            self.assertTrue(features["skip_host_skill_discovery"])

    def test_compiled_policy_uses_cli_config_without_legacy_sandbox_mode(self):
        with TemporaryDirectory() as temp:
            policy = self.policy(temp)
            serialized = json.dumps(policy.canonical_payload(), sort_keys=True)

            self.assertNotIn("sandbox_mode", serialized)
            self.assertNotIn("sandboxMode", serialized)
            self.assertEqual(policy.boundary_launcher.count("-c"), 1)
            self.assertEqual(policy.boundary_launcher[:2], ("/usr/bin/env", "-i"))
            self.assertIn(f"HOME={policy.home}", policy.boundary_launcher)
            self.assertIn("-P", policy.boundary_launcher)
            self.assertIn(policy.profile_name, policy.boundary_launcher)
            self.assertEqual(policy.boundary_launcher[-1], "--")
            self.assertEqual(
                set(policy.process_environment),
                {"HOME", "PATH", "LANG", "LC_ALL", "PYTHONIOENCODING"},
            )

    def test_attestation_refuses_api_key_environment_authentication(self):
        with TemporaryDirectory() as temp:
            policy = self.policy(temp)
            arguments = self.attestation_arguments(policy)
            for name in ch.FORBIDDEN_API_KEY_ENVIRONMENT:
                with self.subTest(name=name):
                    arguments["environment"] = {name: "must-not-be-observed"}
                    with self.assertRaisesRegex(ch.CodexHostError, "API-key"):
                        ch.attest_host(policy, **arguments)

    def test_attestation_refuses_missing_file_login_platform_or_version_drift(self):
        with TemporaryDirectory() as temp:
            policy = self.policy(temp)
            arguments = self.attestation_arguments(policy)

            for field, value, message in (
                ("login_status", "Not logged in", "ChatGPT file login"),
                ("observed_platform", ("linux", "25.4.0", "arm64"), "platform"),
                (
                    "observed_versions",
                    {"codex": "0.162.0", "promptfoo": "0.125.1"},
                    "version",
                ),
            ):
                with self.subTest(field=field):
                    changed = dict(arguments)
                    changed[field] = value
                    with self.assertRaisesRegex(ch.CodexHostError, message):
                        ch.attest_host(policy, **changed)

    def test_attestation_rejects_symlink_or_overlapping_workspace(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            workspace, command_line_tools, home, protected, codex = self.paths(root)
            symlink = root / "workspace-link"
            symlink.symlink_to(workspace, target_is_directory=True)
            with self.assertRaisesRegex(ch.CodexHostError, "real workspace"):
                ch.compile_read_only_policy(
                    workspace=symlink,
                    codex_path=codex,
                    command_line_tools_root=command_line_tools,
                    home=home,
                    mcp_servers=(),
                    protected_roots=(protected,),
                )

            nested_protected = workspace / "protected"
            nested_protected.mkdir()
            with self.assertRaisesRegex(ch.CodexHostError, "overlap"):
                ch.compile_read_only_policy(
                    workspace=workspace,
                    codex_path=codex,
                    command_line_tools_root=command_line_tools,
                    home=home,
                    mcp_servers=(),
                    protected_roots=(nested_protected,),
                )

    def attestation_arguments(self, policy):
        return {
            "expected_platform": ("darwin", "25.4.0", "arm64"),
            "observed_platform": ("darwin", "25.4.0", "arm64"),
            "expected_versions": {"codex": "0.163.0", "promptfoo": "0.125.1"},
            "observed_versions": {"codex": "0.163.0", "promptfoo": "0.125.1"},
            "login_status": "Logged in using ChatGPT",
            "observed_mcp_servers": ("node_repl", "cua_repl"),
            "environment": {},
        }

    def test_attestation_returns_sanitized_bound_observations(self):
        with TemporaryDirectory() as temp:
            policy = self.policy(temp)
            attestation = ch.attest_host(policy, **self.attestation_arguments(policy))

            self.assertEqual(attestation.auth_method, "chatgpt-file")
            self.assertEqual(attestation.policy_digest, policy.digest())
            self.assertEqual(attestation.workspace_id, policy.workspace_id)
            self.assertEqual(attestation.disabled_mcp_servers, ("cua_repl", "node_repl"))
            self.assertNotIn("Logged in", json.dumps(attestation.canonical_payload()))


class TrustedPreflightTests(unittest.TestCase):
    def plan(self):
        return c.RunPlan.from_dict(
            {
                "schema_version": "0.2",
                "case_id": "trusted-host-case",
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
            }
        )

    def approval(self, plan, *, plan_digest=None):
        now = datetime.now(timezone.utc)
        return c.ApprovalReceipt.from_dict(
            {
                "schema_version": plan.schema_version,
                "plan_digest": plan_digest or plan.digest(),
                "approved_by": "human-reviewer",
                "issued_at": (now - timedelta(minutes=5)).isoformat(),
                "expires_at": (now + timedelta(minutes=55)).isoformat(),
                "run_nonce": "trusted-host-run-nonce",
                "provider": plan.provider,
                "model": plan.model,
                "adapter": plan.adapter,
                "backend": plan.backend,
                "capability_profile": plan.capabilities.profile,
                "capability_digest": plan.capabilities.digest(),
                "side_effects": list(plan.capabilities.side_effects),
            }
        )

    def configured_bundle(self, root, plan):
        bundle = (root / "configured-bundle").resolve()
        codex_root = bundle / "codex"
        codex_root.mkdir(parents=True)
        (codex_root / "promptfooconfig.yaml").write_text(
            json.dumps(
                {
                    "providers": [
                        {"id": "openai:codex-sdk", "config": {}},
                        {"id": "openai:codex-sdk", "config": {}},
                    ],
                    "tests": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        execution_config = {
            "schema_version": plan.schema_version,
            "plan_digest": plan.digest(),
            "provider": plan.provider,
            "provider_version": plan.provider_version,
            "model": plan.model,
            "model_version": plan.model_version,
            "adapter": plan.adapter,
            "adapter_version": plan.adapter_version,
            "backend": plan.backend,
            "resource_limits": dict(plan.resource_limits),
            "comparison_arms": list(plan.comparison_arms),
        }
        (bundle / "execution-config.json").write_text(
            json.dumps(execution_config, sort_keys=True) + "\n", encoding="utf-8"
        )
        manifest = {
            "status": "CONFIGURED_NOT_BOUND",
            "harness": "codex",
            "case_id": plan.case_id,
            "plan_digest": plan.digest(),
            "model": plan.model,
            "model_version": plan.model_version,
            "provider": plan.provider,
            "provider_version": plan.provider_version,
            "adapter": plan.adapter,
            "adapter_version": plan.adapter_version,
            "resource_limits": dict(plan.resource_limits),
        }
        manifest["provider_config_digest"] = ne._provider_config_digest(bundle, manifest)
        manifest["bundle_digest"] = ne._bundle_digest(bundle)
        (bundle / "manifest.json").write_text(
            json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8"
        )
        return bundle

    def fixture(self, root, *, known_secret_values=()):
        root = Path(root)
        plan = self.plan()
        bundle = self.configured_bundle(root, plan)
        command_line_tools = root / "CommandLineTools"
        command_line_tools.mkdir()
        home = root / "home"
        home.mkdir()
        protected = root / "protected"
        protected.mkdir()
        (protected / "read-canary").write_text("host-owned\n", encoding="utf-8")
        codex = root / "codex"
        codex.write_text("binary placeholder\n", encoding="utf-8")
        codex.chmod(0o700)
        policy = ch.compile_read_only_policy(
            workspace=bundle,
            codex_path=codex,
            command_line_tools_root=command_line_tools,
            home=home,
            mcp_servers=("cua_repl", "node_repl"),
            protected_roots=(protected,),
        )
        inventory = ci.load_inventory(Path(__file__).with_name("provider_capabilities_v0_2.json"))
        attestation = ch.attest_host(
            policy,
            expected_platform=(
                inventory.platform.system,
                inventory.platform.release,
                inventory.platform.machine,
            ),
            observed_platform=(
                inventory.platform.system,
                inventory.platform.release,
                inventory.platform.machine,
            ),
            expected_versions={
                "codex": inventory.required_versions["codex"],
                "promptfoo": inventory.required_versions["promptfoo"],
            },
            observed_versions={
                "codex": inventory.required_versions["codex"],
                "promptfoo": inventory.required_versions["promptfoo"],
            },
            login_status="Logged in using ChatGPT",
            observed_mcp_servers=("cua_repl", "node_repl"),
            environment={},
        )
        provider_config = {
            "provider": plan.provider,
            "provider_version": plan.provider_version,
            "adapter": plan.adapter,
            "adapter_version": plan.adapter_version,
            "backend": plan.backend,
            "profile": plan.capabilities.profile,
            "sandbox_mode": policy.profile_name,
            "boundary_launcher": list(policy.boundary_launcher),
            "outside_read_path": str(protected / "read-canary"),
            "outside_write_path": str(protected / "write-canary"),
            "network_host": "192.0.2.1",
            "network_port": 9,
            "secret_names": ["SYNTHETIC_PROBE_SECRET"],
            "forbidden_commands": ["codex", "docker", "osascript"],
            "connectors_enabled": [],
            "mcp_servers": [],
        }
        now = datetime.now(timezone.utc)
        request = ch.PreflightRequest(
            plan=plan,
            approval=self.approval(plan),
            inventory=inventory,
            policy=policy,
            attestation=attestation,
            bundle=bundle,
            provider_config=provider_config,
            artifact_directory=root / "host-artifacts",
            issued_at=(now - timedelta(minutes=1)).isoformat(),
            expires_at=(now + timedelta(minutes=30)).isoformat(),
            verifier_version="0.3.0",
            known_secret_values=tuple(known_secret_values),
        )
        request.artifact_directory.mkdir()
        return request

    def completed(self, status="PASS", observation="denied"):
        return SimpleNamespace(
            returncode=0,
            stdout=json.dumps({"status": status, "observation": observation}),
            stderr="",
        )

    def boundary_result(self, request, *, status="PASS", observation="denied", missing=False):
        digest = nb.provider_config_digest(request.provider_config)
        probe_ids = (
            "environment-secret",
            "network-egress",
            "read-outside-workspace",
            "secondary-tool-route",
            "write-inside-workspace",
            "write-outside-workspace",
        )
        results = tuple(
            nb.ProbeResult(probe_id, "boundary", status, observation, digest)
            for probe_id in probe_ids
        )
        if missing:
            results = results[:-1]
        return nb.NativeBoundaryResult(
            request.plan.digest(), digest, probe_ids, results, ()
        )

    def test_preflight_runs_all_six_probes_without_provider_dispatch(self):
        with TemporaryDirectory() as temp:
            request = self.fixture(temp)
            with patch("native_boundary.subprocess.run", return_value=self.completed()) as run:
                result = ch.run_trusted_preflight(request)

        self.assertEqual(run.call_count, 6)
        self.assertTrue(result.boundary.complete)
        commands = [call.args[0] for call in run.call_args_list]
        self.assertTrue(all(any(str(item).endswith(".py") for item in command) for command in commands))
        self.assertFalse(any("promptfoo" in str(item) for command in commands for item in command))

    def test_preflight_binds_plan_bundle_policy_workspace_nonce_and_tools(self):
        with TemporaryDirectory() as temp:
            request = self.fixture(temp)
            result = ch.run_trusted_preflight(
                request,
                boundary_runner=lambda *_args: self.boundary_result(request),
            )

            manifest = json.loads((request.bundle / "manifest.json").read_text())
            receipt = result.receipt
            self.assertEqual(receipt.plan_digest, request.plan.digest())
            self.assertEqual(receipt.run_nonce, request.approval.run_nonce)
            self.assertEqual(receipt.prepared_bundle_digest, manifest["bundle_digest"])
            self.assertEqual(ne._bundle_digest(request.bundle), manifest["bundle_digest"])
            self.assertEqual(receipt.provider_config_digest, manifest["provider_config_digest"])
            self.assertEqual(receipt.workspace_id, request.policy.workspace_id)
            self.assertEqual(result.policy_digest, request.policy.digest())
            self.assertEqual(receipt.enabled_tools, ("filesystem_read",))
            self.assertIn("shell", receipt.disabled_tools)
            self.assertTrue(result.policy_artifact.is_file())
            self.assertTrue(result.snapshot_artifact.is_file())
            self.assertTrue(result.probe_artifact.is_file())
            self.assertTrue(result.receipt_artifact.is_file())

    def test_preflight_blocks_failed_unknown_timed_out_or_missing_probe(self):
        for status, missing in (("FAIL", False), ("UNKNOWN", False), ("PASS", True)):
            with self.subTest(status=status, missing=missing), TemporaryDirectory() as temp:
                request = self.fixture(temp)
                with self.assertRaisesRegex(ch.CodexHostError, "probe"):
                    ch.run_trusted_preflight(
                        request,
                        boundary_runner=lambda *_args, s=status, m=missing: self.boundary_result(
                            request, status=s, missing=m
                        ),
                    )
                self.assertEqual(list(request.artifact_directory.iterdir()), [])

    def test_preflight_blocks_changed_approval_inventory_or_provider_config(self):
        with TemporaryDirectory() as temp:
            request = self.fixture(temp)
            wrong_approval = replace(request.approval, plan_digest="wrong-plan")
            wrong_inventory = replace(
                request.inventory,
                required_versions={**request.inventory.required_versions, "codex": "9.9.9"},
            )
            wrong_config = dict(request.provider_config, boundary_launcher=["/wrong/launcher"])
            for field, value in (
                ("approval", wrong_approval),
                ("inventory", wrong_inventory),
                ("provider_config", wrong_config),
            ):
                with self.subTest(field=field):
                    changed = replace(request, **{field: value})
                    with self.assertRaises(ch.CodexHostError):
                        ch.run_trusted_preflight(
                            changed,
                            boundary_runner=lambda *_args: self.boundary_result(changed),
                        )

    def test_preflight_artifacts_use_exclusive_durable_publication(self):
        with TemporaryDirectory() as temp:
            request = self.fixture(temp)
            result = ch.run_trusted_preflight(
                request,
                boundary_runner=lambda *_args: self.boundary_result(request),
            )
            original = result.receipt_artifact.read_bytes()
            with self.assertRaisesRegex(ch.CodexHostError, "already exists"):
                ch.run_trusted_preflight(
                    request,
                    boundary_runner=lambda *_args: self.boundary_result(request),
                )
            self.assertEqual(result.receipt_artifact.read_bytes(), original)

    def test_preflight_redacts_secret_like_observations(self):
        secret = "synthetic-sensitive-observation"
        with TemporaryDirectory() as temp:
            request = self.fixture(temp, known_secret_values=(secret,))
            result = ch.run_trusted_preflight(
                request,
                boundary_runner=lambda *_args: self.boundary_result(
                    request, observation=secret
                ),
            )
            serialized = "".join(
                path.read_text(encoding="utf-8")
                for path in (
                    result.policy_artifact,
                    result.snapshot_artifact,
                    result.probe_artifact,
                    result.receipt_artifact,
                )
            )
        self.assertNotIn(secret, serialized)
        self.assertIn("[REDACTED]", serialized)

    def test_preflight_never_invokes_promptfoo_or_a_model_subprocess(self):
        with TemporaryDirectory() as temp:
            request = self.fixture(temp)
            with patch("native_boundary.subprocess.run", return_value=self.completed()) as run:
                ch.run_trusted_preflight(request)

        for call in run.call_args_list:
            command = call.args[0]
            self.assertIn("sandbox", command)
            self.assertNotIn("exec", command)
            self.assertFalse(any("promptfoo" in str(item) for item in command))


if __name__ == "__main__":
    unittest.main()
