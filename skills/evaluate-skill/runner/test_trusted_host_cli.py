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
        promptfoo_path = request.policy.promptfoo_path
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
            "--node-path", str(request.policy.node_path),
            "--promptfoo-runtime-root", str(request.policy.promptfoo_runtime_root),
            "--codex-sdk-root", str(request.policy.codex_sdk_root),
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
                "codex": "0.163.0",
                "promptfoo": "0.125.1",
                "node": "22.23.1",
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
            "codex_executable_digest": request.policy.codex_executable.digest,
            "promptfoo_executable_digest": (
                request.policy.promptfoo_executable.digest
            ),
            "node_executable_digest": request.policy.node_executable.digest,
            "promptfoo_runtime_digest": request.policy.promptfoo_runtime_digest,
            "codex_sdk_digest": request.policy.codex_sdk_digest,
            "observer_id": pt.OBSERVER_ID,
            "observer_version": pt.OBSERVER_VERSION,
        }
        path = Path(root) / "live-authorization.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def run_argv(
        self, root, request, authorization, *, promptfoo_path=None, node_path=None
    ):
        binary = request.policy.promptfoo_path if promptfoo_path is None else Path(
            promptfoo_path
        )
        node = request.policy.node_path if node_path is None else Path(node_path)
        ledger = Path(root) / "nonce-ledger"
        ledger.mkdir()
        return [
            "run",
            "--run-plan", str(Path(root) / "run-plan.json"),
            "--bundle", str(request.bundle),
            "--preflight-directory", str(request.artifact_directory),
            "--artifact-directory", str(request.artifact_directory),
            "--promptfoo-path", str(binary.resolve()),
            "--node-path", str(node.resolve()),
            "--nonce-ledger", str(ledger),
            "--live-authorization", str(authorization),
            "--protected-root", str(request.policy.protected_roots[0]),
        ]

    def trusted_runner(self, request, calls):
        helper = self.helper()

        def launch(argv, **kwargs):
            calls.append((tuple(argv), kwargs))
            promptfoo_process_id = 2900

            def wait_for_result():
                document = helper.promptfoo_document(
                    SimpleNamespace(bundle=request.bundle)
                )
                (request.bundle / "codex-results.json").write_text(
                    json.dumps(document), encoding="utf-8"
                )
                sessions = []
                for result_index, (arm, session) in enumerate((
                    ("with-skill", "session-with"),
                    ("without-skill", "session-without"),
                )):
                    for role, assertion_index, session_id in (
                        ("arm", -1, session),
                        ("judge", 0, f"judge-{arm}"),
                    ):
                        sessions.append(pt.ObservedSessionIdentity(
                            role=role,
                            arm_name=arm,
                            result_index=result_index,
                            assertion_index=assertion_index,
                            session_id=session_id,
                            execution_id=kwargs["execution_id"],
                            process_id=3000 + len(sessions),
                            parent_process_id=promptfoo_process_id,
                            executable_digest=kwargs["expected_executable_digest"],
                            observed_at=kwargs["observation_started_at"],
                            provider=request.plan.provider,
                            provider_version=request.plan.provider_version,
                            model=request.plan.model,
                            model_version=request.plan.model_version,
                            adapter=request.plan.adapter,
                            adapter_version=request.plan.adapter_version,
                            provider_config_digest=json.loads(
                                (
                                    request.artifact_directory
                                    / "enforcement-receipt.json"
                                ).read_text()
                            )["provider_config_digest"],
                        ))
                observer_trace = json.dumps({
                    "schema_version": pt.OBSERVER_SCHEMA_VERSION,
                    "observer_id": kwargs["expected_observer_id"],
                    "observer_version": kwargs["expected_observer_version"],
                    "execution_id": kwargs["execution_id"],
                    "promptfoo_process_id": promptfoo_process_id,
                    "executable_digest": kwargs["expected_executable_digest"],
                    "provider_config_digest": kwargs[
                        "expected_provider_config_digest"
                    ],
                    "sessions": [session.__dict__ for session in sessions],
                    "command_decisions": [],
                }, sort_keys=True).encode("utf-8")
                return ch.SupervisedProcessResult(
                    returncode=0,
                    stdout=b"stdout",
                    stderr=b"",
                    provider_process_id=promptfoo_process_id,
                    observer_trace=observer_trace,
                )

            return ch.SupervisedProcessHandle(
                process_group_id=promptfoo_process_id,
                wait_for_result=wait_for_result,
                terminate_and_reap=lambda: None,
            )

        return launch

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

    def test_run_rejects_executable_or_mcp_drift_before_dispatch(self):
        with TemporaryDirectory() as temp:
            request, preflight_argv, dependencies = self.setup_preflight(temp)
            self.assertEqual(th.main(preflight_argv, dependencies=dependencies), 0)
            receipt = c.EnforcementReceipt.from_dict(json.loads(
                (request.artifact_directory / "enforcement-receipt.json").read_text()
            ))
            ne.bind_prepared_bundle(request.bundle, request.plan, receipt)
            authorization = self.live_authorization(temp, request)
            calls = []
            deps = replace(
                dependencies, trusted_process_runner=self.trusted_runner(request, calls)
            )

            drifted = Path(temp) / "different-promptfoo"
            drifted.write_text("synthetic replacement\n", encoding="utf-8")
            drifted.chmod(0o700)

            self.assertEqual(
                th.main(
                    self.run_argv(
                        temp, request, authorization, promptfoo_path=drifted
                    ),
                    dependencies=deps,
                ),
                2,
            )
            self.assertEqual(calls, [])

        with TemporaryDirectory() as temp:
            request, preflight_argv, dependencies = self.setup_preflight(temp)
            self.assertEqual(th.main(preflight_argv, dependencies=dependencies), 0)
            receipt = c.EnforcementReceipt.from_dict(json.loads(
                (request.artifact_directory / "enforcement-receipt.json").read_text()
            ))
            ne.bind_prepared_bundle(request.bundle, request.plan, receipt)
            authorization = self.live_authorization(temp, request)
            calls = []
            deps = replace(
                dependencies,
                inspect_mcp_servers=lambda *_args: (
                    *request.policy.disabled_mcp_servers, "evil"
                ),
                trusted_process_runner=self.trusted_runner(request, calls),
            )

            self.assertEqual(
                th.main(self.run_argv(temp, request, authorization), dependencies=deps),
                2,
            )
            self.assertEqual(calls, [])

    def test_post_dispatch_failure_reports_incomplete_and_model_may_have_executed(self):
        with TemporaryDirectory() as temp:
            request, preflight_argv, dependencies = self.setup_preflight(temp)
            self.assertEqual(th.main(preflight_argv, dependencies=dependencies), 0)
            receipt = c.EnforcementReceipt.from_dict(json.loads(
                (request.artifact_directory / "enforcement-receipt.json").read_text()
            ))
            ne.bind_prepared_bundle(request.bundle, request.plan, receipt)
            authorization = self.live_authorization(temp, request)
            calls = []

            def failed_runner(*args, **kwargs):
                calls.append((args, kwargs))
                return ch.SupervisedProcessHandle(
                    process_group_id=1,
                    wait_for_result=lambda: ch.SupervisedProcessResult(
                        returncode=7,
                        stdout=b"",
                        stderr=b"failed",
                        provider_process_id=1,
                        observer_trace=b"failed-observer-trace",
                    ),
                    terminate_and_reap=lambda: None,
                )

            deps = replace(dependencies, trusted_process_runner=failed_runner)
            output = StringIO()
            with redirect_stdout(output):
                status = th.main(
                    self.run_argv(temp, request, authorization), dependencies=deps
                )

        payload = json.loads(output.getvalue())
        self.assertEqual(status, 2)
        self.assertEqual(len(calls), 1)
        self.assertEqual(payload["status"], "INCOMPLETE")
        self.assertTrue(payload["model_executed"])

    def test_keyboard_interrupt_after_dispatch_reports_incomplete(self):
        with TemporaryDirectory() as temp:
            request, preflight_argv, dependencies = self.setup_preflight(temp)
            self.assertEqual(th.main(preflight_argv, dependencies=dependencies), 0)
            receipt = c.EnforcementReceipt.from_dict(json.loads(
                (request.artifact_directory / "enforcement-receipt.json").read_text()
            ))
            ne.bind_prepared_bundle(request.bundle, request.plan, receipt)
            authorization = self.live_authorization(temp, request)

            def interrupted_runner(*_args, **_kwargs):
                return ch.SupervisedProcessHandle(
                    process_group_id=1,
                    wait_for_result=lambda: (_ for _ in ()).throw(
                        KeyboardInterrupt()
                    ),
                    terminate_and_reap=lambda: None,
                )

            deps = replace(
                dependencies, trusted_process_runner=interrupted_runner
            )
            output = StringIO()
            with redirect_stdout(output):
                status = th.main(
                    self.run_argv(temp, request, authorization), dependencies=deps
                )

        payload = json.loads(output.getvalue())
        self.assertEqual(status, 2)
        self.assertEqual(payload["status"], "INCOMPLETE")
        self.assertTrue(payload["model_executed"])

    def test_run_rejects_runtime_executable_or_ambient_config_mutation(self):
        for mutation in (
            "replace-promptfoo",
            "replace-node",
            "add-runtime-chunk",
            "edit-sdk-package",
            "add-config",
        ):
            with self.subTest(mutation=mutation), TemporaryDirectory() as temp:
                request, preflight_argv, dependencies = self.setup_preflight(temp)
                self.assertEqual(th.main(preflight_argv, dependencies=dependencies), 0)
                receipt = c.EnforcementReceipt.from_dict(json.loads(
                    (request.artifact_directory / "enforcement-receipt.json").read_text()
                ))
                ne.bind_prepared_bundle(request.bundle, request.plan, receipt)
                authorization = self.live_authorization(temp, request)
                if mutation == "replace-promptfoo":
                    request.policy.promptfoo_path.write_text(
                        "same path, changed executable\n", encoding="utf-8"
                    )
                    request.policy.promptfoo_path.chmod(0o700)
                elif mutation == "replace-node":
                    request.policy.node_path.write_text(
                        "same path, changed node\n", encoding="utf-8"
                    )
                    request.policy.node_path.chmod(0o700)
                elif mutation == "add-runtime-chunk":
                    (request.policy.promptfoo_runtime_root / "late-chunk.js").write_text(
                        "mutated runtime\n", encoding="utf-8"
                    )
                elif mutation == "edit-sdk-package":
                    (request.policy.codex_sdk_root / "package.json").write_text(
                        '{"name":"@openai/codex-sdk","version":"9.9.9"}\n',
                        encoding="utf-8",
                    )
                else:
                    (request.policy.home / ".codex" / "config.toml").write_text(
                        "[mcp_servers.evil]\ncommand='evil'\n", encoding="utf-8"
                    )
                calls = []
                deps = replace(
                    dependencies,
                    trusted_process_runner=self.trusted_runner(request, calls),
                )

                status = th.main(
                    self.run_argv(temp, request, authorization), dependencies=deps
                )

                self.assertEqual(status, 2)
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
