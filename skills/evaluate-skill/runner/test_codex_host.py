import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import codex_host as ch


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


if __name__ == "__main__":
    unittest.main()
