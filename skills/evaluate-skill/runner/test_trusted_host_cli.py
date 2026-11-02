from contextlib import redirect_stdout
from dataclasses import asdict, replace
from datetime import datetime, timedelta, timezone
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest

import codex_host as ch
import contracts as c
import native_eval as ne
import provider_trace as pt
import test_codex_host as tch
import trusted_host as th


class TrustedHostCliTests(unittest.TestCase):
    def helper(self):
        return tch.TrustedSupervisorTests()

    def setup_preflight(self, root):
        helper = self.helper()
        request = helper.fixture(root)
        root = Path(root)
        plan_path = root / "run-plan.json"
        approval_path = root / "approval.json"
        provider_config_path = root / "provider-config.json"
        plan_path.write_text(
            json.dumps(request.plan.canonical_payload()), encoding="utf-8"
        )
        approval_path.write_text(json.dumps({
            **asdict(request.approval),
            "side_effects": list(request.approval.side_effects),
        }), encoding="utf-8")
        provider_config_path.write_text(
            json.dumps(request.provider_config), encoding="utf-8"
        )
        promptfoo_path = root / "promptfoo-preflight"
        promptfoo_path.write_text("synthetic promptfoo\n", encoding="utf-8")
        promptfoo_path.chmod(0o700)
        inventory_path = Path(__file__).with_name("provider_capabilities_v0_2.json")
        argv = [
            "preflight",
            "--run-plan", str(plan_path),
            "--approval-receipt", str(approval_path),
            "--capability-inventory", str(inventory_path),
            "--bundle", str(request.bundle),
            "--artifact-directory", str(request.artifact_directory),
            "--codex-path", str(request.policy.codex_path),
            "--promptfoo-path", str(promptfoo_path.resolve()),
            "--command-line-tools-root", str(request.policy.command_line_tools_root),
            "--home", str(request.policy.home),
            "--protected-root", str(request.policy.protected_roots[0]),
            "--provider-config", str(provider_config_path),
            "--issued-at", request.issued_at,
            "--expires-at", request.expires_at,
            "--verifier-version", request.verifier_version,
        ]
        dependencies = th.HostDependencies(
            inspect_versions=lambda *_args: {
                "codex": "0.163.0", "promptfoo": "0.125.1"
            },
            inspect_platform=lambda: request.attestation.platform,
            inspect_login=lambda *_args: "Logged in using ChatGPT",
            inspect_mcp_servers=lambda *_args: request.policy.disabled_mcp_servers,
            inspect_environment=lambda: {},
            boundary_runner=lambda *_args: helper.boundary_result(request),
            trusted_process_runner=None,
        )
        return request, argv, dependencies

    def live_authorization(self, root, request):
        receipt_path = request.artifact_directory / "enforcement-receipt.json"
        receipt_digest = th.file_digest(receipt_path)
        now = datetime.now(timezone.utc)
        value = {
            "schema_version": "0.3",
            "decision": "APPROVED_LIVE_RUN",
            "authorized_by": "human-reviewer",
            "issued_at": (now - timedelta(minutes=1)).isoformat(),
            "expires_at": (now + timedelta(minutes=10)).isoformat(),
            "plan_digest": request.plan.digest(),
            "run_nonce": request.approval.run_nonce,
            "provider": request.plan.provider,
            "model_version": request.plan.model_version,
            "backend": request.plan.backend,
            "capability_profile": request.plan.capabilities.profile,
            "preflight_receipt_digest": receipt_digest,
            "preflight_artifact_digest": th.preflight_artifact_digest(
                request.artifact_directory
            ),
        }
        path = Path(root) / "live-authorization.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def run_argv(self, root, request, authorization):
        binary = Path(root) / "promptfoo"
        binary.write_text("synthetic promptfoo\n", encoding="utf-8")
        binary.chmod(0o700)
        ledger = Path(root) / "nonce-ledger"
        ledger.mkdir()
        return [
            "run",
            "--run-plan", str(Path(root) / "run-plan.json"),
            "--bundle", str(request.bundle),
            "--preflight-directory", str(request.artifact_directory),
            "--artifact-directory", str(request.artifact_directory),
            "--promptfoo-path", str(binary.resolve()),
            "--nonce-ledger", str(ledger),
            "--live-authorization", str(authorization),
            "--protected-root", str(request.policy.protected_roots[0]),
        ]

    def trusted_runner(self, request, calls):
        helper = self.helper()

        def run(argv, **kwargs):
            calls.append((tuple(argv), kwargs))
            document = helper.promptfoo_document(SimpleNamespace(bundle=request.bundle))
            (request.bundle / "codex-results.json").write_text(
                json.dumps(document), encoding="utf-8"
            )
            sessions = tuple(
                pt.ObservedSessionIdentity(
                    arm_name=arm,
                    session_id=session,
                    provider=request.plan.provider,
                    provider_version=request.plan.provider_version,
                    model=request.plan.model,
                    model_version=request.plan.model_version,
                    adapter=request.plan.adapter,
                    adapter_version=request.plan.adapter_version,
                    provider_config_digest=json.loads(
                        (request.artifact_directory / "enforcement-receipt.json").read_text()
                    )["provider_config_digest"],
                )
                for arm, session in (
                    ("with-skill", "session-with"),
                    ("without-skill", "session-without"),
                )
            )
            return ch.SupervisedProcessResult(0, b"stdout", b"", sessions)

        return run

    def test_preflight_cli_never_dispatches_provider(self):
        with TemporaryDirectory() as temp:
            request, argv, dependencies = self.setup_preflight(temp)
            provider_calls = []
            dependencies = replace(
                dependencies,
                trusted_process_runner=lambda *args, **kwargs: provider_calls.append(args),
            )
            output = StringIO()
            with redirect_stdout(output):
                status = th.main(argv, dependencies=dependencies)

        self.assertEqual(status, 0)
        self.assertEqual(provider_calls, [])
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["status"], "READY_NOT_RUN")
        self.assertFalse(payload["model_executed"])

    def test_run_cli_requires_fresh_matching_preflight_and_explicit_live_authorization(self):
        with TemporaryDirectory() as temp:
            request, preflight_argv, dependencies = self.setup_preflight(temp)
            self.assertEqual(th.main(preflight_argv, dependencies=dependencies), 0)
            receipt = c.EnforcementReceipt.from_dict(json.loads(
                (request.artifact_directory / "enforcement-receipt.json").read_text()
            ))
            ne.bind_prepared_bundle(request.bundle, request.plan, receipt)
            authorization = self.live_authorization(temp, request)
            calls = []
            run_dependencies = replace(
                dependencies, trusted_process_runner=self.trusted_runner(request, calls)
            )
            argv = self.run_argv(temp, request, authorization)

            output = StringIO()
            with redirect_stdout(output):
                status = th.main(argv, dependencies=run_dependencies)

        self.assertEqual(status, 0)
        self.assertEqual(len(calls), 1)
        self.assertEqual(json.loads(output.getvalue())["status"], "COMPLETED")

        with TemporaryDirectory() as temp:
            request, preflight_argv, dependencies = self.setup_preflight(temp)
            self.assertEqual(th.main(preflight_argv, dependencies=dependencies), 0)
            receipt = c.EnforcementReceipt.from_dict(json.loads(
                (request.artifact_directory / "enforcement-receipt.json").read_text()
            ))
            ne.bind_prepared_bundle(request.bundle, request.plan, receipt)
            authorization = self.live_authorization(temp, request)
            value = json.loads(authorization.read_text())
            value["plan_digest"] = "wrong-plan"
            authorization.write_text(json.dumps(value))
            calls = []
            deps = replace(dependencies, trusted_process_runner=self.trusted_runner(request, calls))
            self.assertEqual(th.main(self.run_argv(temp, request, authorization), dependencies=deps), 2)
            self.assertEqual(calls, [])

    def test_cli_reports_blocked_not_run_without_secret_values(self):
        secret = "synthetic-cli-secret"
        with TemporaryDirectory() as temp:
            request, argv, dependencies = self.setup_preflight(temp)
            dependencies = replace(
                dependencies,
                inspect_environment=lambda: {"OPENAI_API_KEY": secret},
            )
            output = StringIO()
            with redirect_stdout(output):
                status = th.main(argv, dependencies=dependencies)

        self.assertEqual(status, 2)
        self.assertNotIn(secret, output.getvalue())
        self.assertEqual(json.loads(output.getvalue())["status"], "BLOCKED_NOT_RUN")

    def test_cli_refuses_implicit_paths_backend_fallback_and_overwrite(self):
        with TemporaryDirectory() as temp:
            request, argv, dependencies = self.setup_preflight(temp)
            self.assertEqual(th.main(argv[:-2], dependencies=dependencies), 2)

        with TemporaryDirectory() as temp:
            request, argv, dependencies = self.setup_preflight(temp)
            plan_path = Path(temp) / "run-plan.json"
            value = json.loads(plan_path.read_text())
            value["backend"] = "docker"
            plan_path.write_text(json.dumps(value))
            self.assertEqual(th.main(argv, dependencies=dependencies), 2)

        with TemporaryDirectory() as temp:
            request, argv, dependencies = self.setup_preflight(temp)
            (request.artifact_directory / "host-policy.json").write_text("preserve")
            self.assertEqual(th.main(argv, dependencies=dependencies), 2)
            self.assertEqual(
                (request.artifact_directory / "host-policy.json").read_text(), "preserve"
            )

    def test_real_probe_command_is_separate_from_live_provider_command(self):
        with TemporaryDirectory() as temp:
            request, argv, dependencies = self.setup_preflight(temp)
            boundary_calls = []
            provider_calls = []
            dependencies = replace(
                dependencies,
                boundary_runner=lambda plan, bundle, config: (
                    boundary_calls.append((plan, bundle, config))
                    or self.helper().boundary_result(request)
                ),
                trusted_process_runner=lambda *args, **kwargs: provider_calls.append(args),
            )
            self.assertEqual(th.main(argv, dependencies=dependencies), 0)

        self.assertEqual(len(boundary_calls), 1)
        self.assertEqual(provider_calls, [])
        probe_launcher = boundary_calls[0][2]["boundary_launcher"]
        self.assertIn("sandbox", probe_launcher)
        self.assertNotIn("promptfoo", " ".join(probe_launcher))


if __name__ == "__main__":
    unittest.main()
