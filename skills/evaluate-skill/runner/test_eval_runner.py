from contextlib import redirect_stdout
from dataclasses import replace
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import native_eval
import trusted_host

try:
    import eval_runner
except ModuleNotFoundError:
    eval_runner = None


def digest(character="a"):
    return character * 64


class EvalRunnerTests(unittest.TestCase):
    def require_runner(self):
        self.assertIsNotNone(eval_runner, "active Docker-only CLI must exist")
        return eval_runner

    def invoke(self, argv, dependencies=None):
        runner = self.require_runner()
        output = StringIO()
        with redirect_stdout(output):
            status = runner.main(argv, dependencies=dependencies or runner.EvalRunnerDependencies())
        return status, json.loads(output.getvalue())

    def test_active_cli_exposes_docker_preflight_and_run_only(self):
        runner = self.require_runner()
        self.assertEqual(
            runner.command_names(),
            ("inspect", "prepare", "configure", "docker-preflight", "docker-run"),
        )
        self.assertNotIn("native-run", runner.command_names())
        self.assertNotIn("run", runner.command_names())

    def test_native_live_commands_are_retired_and_return_blocked_not_run(self):
        output = StringIO()
        with redirect_stdout(output):
            status = native_eval.main(["run"])
        self.assertEqual(status, 2)
        self.assertEqual(json.loads(output.getvalue())["status"], "BLOCKED_NOT_RUN")

        output = StringIO()
        with redirect_stdout(output):
            status = trusted_host.main(["preflight"])
        self.assertEqual(status, 2)
        value = json.loads(output.getvalue())
        self.assertEqual(value["status"], "BLOCKED_NOT_RUN")
        self.assertFalse(value["model_executed"])

        output = StringIO()
        with patch("sys.argv", ["native_eval.py", "run"]), redirect_stdout(output):
            status = native_eval.main()
        self.assertEqual(status, 2)
        self.assertEqual(json.loads(output.getvalue())["status"], "BLOCKED_NOT_RUN")

    def test_prepare_and_configure_remain_provider_specific_without_model_calls(self):
        runner = self.require_runner()
        calls = []

        def offline(action, values):
            calls.append((action, dict(values)))
            return {"status": action.upper() + "D_NOT_RUN", "provider": values["provider"]}

        deps = runner.EvalRunnerDependencies(
            prepare=lambda values: offline("prepare", values),
            configure=lambda values: offline("configure", values),
            docker_preflight=lambda _values: self.fail("preflight must not run"),
            docker_run=lambda _values: self.fail("live run must not run"),
        )
        with TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "skill"
            target.mkdir()
            suite = root / "evals.json"
            suite.write_text("{}\n", encoding="utf-8")
            bundle = root / "bundle"
            bundle.mkdir()
            plan = root / "plan.json"
            plan.write_text("{}\n", encoding="utf-8")
            status, value = self.invoke(
                [
                    "prepare", "--provider", "openai", "--suite", str(suite),
                    "--case-id", "case-1", "--target-skill", str(target),
                    "--output", str(root / "out"),
                ],
                deps,
            )
            self.assertEqual(status, 0)
            self.assertEqual(value["provider"], "openai")
            status, value = self.invoke(
                [
                    "configure", "--provider", "anthropic", "--bundle", str(bundle),
                    "--run-plan", str(plan),
                ],
                deps,
            )
            self.assertEqual(status, 0)
            self.assertEqual(value["provider"], "anthropic")
        self.assertEqual([item[0] for item in calls], ["prepare", "configure"])

    def security_args(self, root, action="docker-preflight"):
        names = (
            "run-plan", "approval-receipt", "prepared-bundle", "capability-inventory",
            "execution-binding", "gateway-binding", "evidence-binding", "image-lock",
            "docker-path", "gateway-key", "gateway-config", "evidence-key",
            "seccomp-policy", "executable-inventory", "artifact-directory",
        )
        argv = [action]
        for name in names:
            path = root / name
            if name in ("prepared-bundle", "artifact-directory"):
                path.mkdir(exist_ok=True)
            else:
                path.write_text("{}\n", encoding="utf-8")
            argv.extend(["--" + name, str(path)])
        argv.extend(
            [
                "--docker-context", "desktop-linux",
                "--docker-endpoint", "unix:///var/run/docker.sock",
                "--expected-runtime-digest", digest("1"),
                "--expected-image-digest", digest("2"),
                "--expected-gateway-policy-digest", digest("3"),
                "--expected-observer-policy-digest", digest("4"),
                "--expected-cleanup-policy-digest", digest("5"),
                "--protected-root", str(root / "protected"),
            ]
        )
        (root / "protected").mkdir(exist_ok=True)
        if action == "docker-run":
            preflight = root / "preflight-artifact"
            authorization = root / "live-authorization"
            preflight.write_text("{}\n", encoding="utf-8")
            authorization.write_text("{}\n", encoding="utf-8")
            argv.extend(["--preflight-artifact", str(preflight)])
            argv.extend(["--live-authorization", str(authorization)])
        return argv

    def test_docker_preflight_requires_every_explicit_path_key_policy_and_digest(self):
        runner = self.require_runner()
        calls = []
        deps = runner.EvalRunnerDependencies(
            docker_preflight=lambda values: calls.append(values) or {
                "status": "READY_NOT_RUN", "model_executed": False
            }
        )
        with TemporaryDirectory() as temp:
            argv = self.security_args(Path(temp))
            status, value = self.invoke(argv[:-2], deps)
            self.assertEqual(status, 2)
            self.assertEqual(value["status"], "BLOCKED_NOT_RUN")
            self.assertEqual(calls, [])
            status, value = self.invoke(argv, deps)
            self.assertEqual(status, 0)
            self.assertEqual(value["status"], "READY_NOT_RUN")
            self.assertEqual(len(calls), 1)

    def test_docker_run_requires_fresh_matching_preflight_and_live_authorization(self):
        runner = self.require_runner()
        calls = []
        deps = runner.EvalRunnerDependencies(
            docker_run=lambda values: calls.append(values) or {
                "status": "COMPLETED", "model_executed": True
            }
        )
        with TemporaryDirectory() as temp:
            argv = self.security_args(Path(temp), "docker-run")
            incomplete = argv[:-2]
            status, value = self.invoke(incomplete, deps)
            self.assertEqual(status, 2)
            self.assertEqual(value["status"], "BLOCKED_NOT_RUN")
            self.assertEqual(calls, [])
            status, value = self.invoke(argv, deps)
            self.assertEqual(status, 0)
            self.assertTrue(value["model_executed"])
            self.assertEqual(len(calls), 1)

    def test_cli_never_installs_starts_pulls_builds_or_falls_back_implicitly(self):
        runner = self.require_runner()
        status, value = self.invoke(["inspect"])
        self.assertEqual(status, 0)
        self.assertEqual(value["active_backend"], "docker")
        self.assertEqual(value["status"], "DOCKER_DESIGN_PENDING")
        self.assertFalse(value["model_executed"])
        self.assertEqual(value["implicit_actions"], [])
        self.assertEqual(value["fallback_backend"], None)

    def test_status_and_docs_report_docker_design_pending_until_real_probes_pass(self):
        runner = self.require_runner()
        runner_root = Path(runner.__file__).resolve().parent
        status = json.loads((runner_root / "proof" / "status_v0_2.json").read_text())
        self.assertEqual(status["active_architecture"], "docker-only-v0.4")
        self.assertEqual(status["status"], "BLOCKED_NOT_RUN")
        self.assertEqual(status["architecture_status"], "DOCKER_DESIGN_PENDING")
        self.assertFalse(status["real_docker_probes_passed"])
        self.assertFalse(status["live_model_executed"])
        for relative in (
            "../SKILL.md", "../README.md", "README.md", "proof/README.md",
            "../references/execution-safety-gate.md",
            "../references/eval-runner-integration.md",
        ):
            text = (runner_root / relative).resolve().read_text(encoding="utf-8")
            self.assertIn("eval_runner.py", text)
            self.assertIn("DOCKER_DESIGN_PENDING", text)


if __name__ == "__main__":
    unittest.main()
