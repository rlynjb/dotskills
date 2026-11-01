"""Offline tests: never call a real model or external service."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("refine_local_runner", HERE / "runner.py")
runner = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(runner)


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.skill = root / "sample-skill"
        self.skill.mkdir()
        (self.skill / "SKILL.md").write_text("An example read-only skill.", encoding="utf-8")
        refs = self.skill / "references"
        refs.mkdir()
        (refs / "guide.md").write_text("Read fixture evidence.", encoding="utf-8")
        fixtures = self.skill / "evals" / "files"
        fixtures.mkdir(parents=True)
        (fixtures / "input.txt").write_text("synthetic", encoding="utf-8")
        self.suite = self.skill / "evals" / "evals.json"
        self.case = {"id": 1, "prompt": "Read the input",
                     "expected_output": "An explanation with evidence",
                     "files": ["evals/files/input.txt"],
                     "assertions": ["Uses evidence"]}
        self.suite.write_text(json.dumps({"skill_name": "sample-skill",
                                          "evals": [self.case]}), encoding="utf-8")

    def test_only_agent_facing_files_are_staged(self):
        work = Path(self.temp.name) / "with"
        work.mkdir()
        runner.stage(self.suite, self.case, work, True)
        self.assertTrue((work / "inputs/evals/files/input.txt").is_file())
        self.assertTrue((work / "agent_skill/SKILL.md").is_file())
        self.assertTrue((work / "agent_skill/references/guide.md").is_file())
        self.assertFalse((work / "inputs/evals/evals.json").exists())
        self.assertFalse((work / "agent_skill/evals/evals.json").exists())

    def test_baseline_does_not_receive_skill(self):
        work = Path(self.temp.name) / "without"
        work.mkdir()
        runner.stage(self.suite, self.case, work, False)
        self.assertFalse((work / "agent_skill").exists())

    def test_fixture_path_escape_denied(self):
        with self.assertRaises(runner.Blocked):
            runner.fixture(self.skill, "../private")
        (self.skill / "evals/files/alias").symlink_to(self.skill / "SKILL.md")
        with self.assertRaises(runner.Blocked):
            runner.fixture(self.skill, "evals/files/alias")

    def test_host_manifest_is_required_and_checked(self):
        path = Path(self.temp.name) / "host.json"
        payload = {"mode": "mock", "verified_by": "independent-host",
                   "checks": {key: True for key in runner.CHECKS},
                   "mock_write_allowlist": []}
        path.write_text(json.dumps(payload), encoding="utf-8")
        self.assertEqual(runner.host_policy(path)["mode"], "mock")
        payload["checks"]["network_egress_blocked"] = False
        path.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaises(runner.Blocked):
            runner.host_policy(path)

    def test_no_model_call_without_approvals(self):
        args = type("Args", (), {"suite": self.suite, "case_id": 1,
               "approved_case": False, "approved_provider": False,
               "host_enforced": False, "synthetic_only": True})()
        with self.assertRaises(runner.Blocked):
            runner.paired(args)

    def test_both_harnesses_use_nonmutating_cli_modes(self):
        output = Path(self.temp.name) / "out.txt"
        claude = runner.argv_for("claude", "task", "agent", output)
        codex = runner.argv_for("codex", "task", "agent", output)
        self.assertIn("Read,Glob,Grep", claude)
        self.assertIn("plan", claude)
        self.assertIn("read-only", codex)
        self.assertNotIn("--full-auto", codex)
        self.assertNotIn("--dangerously-skip-permissions", claude)

    def test_codex_grader_uses_structured_schema(self):
        directory = Path(self.temp.name)
        final = directory / "last-message.txt"
        argv = runner.argv_for("codex", "grade output", "grader", final)
        self.assertIn("--output-schema", argv)
        schema = runner.load(directory / "grading.schema.json")
        self.assertIn("expectations", schema["properties"])

    def test_claude_grader_requires_pinned_instructions(self):
        args = type("Args", (), {"suite": self.suite, "case_id": 1,
           "grader_instructions": None, "grader_instructions_sha256": None,
           "harness": "claude"})()
        with self.assertRaises(runner.Blocked):
            runner.grade(args)

    def test_normalize_llm_grade_needs_evidence(self):
        good = {"expectations": [{"text": "Uses evidence", "passed": True,
                                  "evidence": "Output cites input.txt"}]}
        grade = runner.grade_result(good, ["Uses evidence"])
        self.assertEqual(grade["summary"]["pass_rate"], 1.0)
        self.assertIn("UNVERIFIED", grade["security_status"])
        bad = {"expectations": [{"text": "Wrong", "passed": True, "evidence": "?"}]}
        with self.assertRaises(runner.Blocked):
            runner.grade_result(bad, ["Uses evidence"])

    def test_parse_native_results(self):
        self.assertEqual(runner.parse_result("claude", json.dumps({"result": "ok"}),
                                             Path(self.temp.name) / "missing"), "ok")
        final_file = Path(self.temp.name) / "last.txt"
        final_file.write_text("response", encoding="utf-8")
        self.assertEqual(runner.parse_result("codex", "", final_file), "response")

    def test_later_assertions_do_not_change_stage2_case_digest(self):
        original = dict(self.case)
        revised = dict(original)
        revised["assertions"] = ["Additional semantic criterion"]
        self.assertEqual(runner.case_input_digest(original),
                         runner.case_input_digest(revised))

    def test_compare_requires_matching_real_grading_artifacts(self):
        import hashlib
        path = Path(self.temp.name) / "run"
        path.mkdir()
        digest = runner.case_input_digest(self.case)
        runner.save(path / "metadata.json", {
            "status": "EXECUTED_PENDING_HOST_TRACE_AUDIT_AND_GRADING",
            "case_id": 1, "harness": "claude", "case_sha256": digest})
        for arm, passed in (("with_skill", True), ("without_skill", False)):
            directory = path / arm
            directory.mkdir()
            expectations = [{"text": "Uses evidence", "passed": passed,
                             "evidence": "Observed output"}]
            runner.save(directory / "grading.json",
                        runner.grade_result({"expectations": expectations},
                                            ["Uses evidence"]))
        args = type("Args", (), {"suite": self.suite, "case_id": 1,
                                "harness": "claude", "run_dir": path})()
        result = runner.compare(args)
        self.assertEqual(result["delta_percentage_points"], 100)
        self.assertIn("PROVISIONAL", result["evaluation_status"])
        self.assertTrue((path / "comparison.json").is_file())

    def test_preflight_does_not_run_agent(self):
        self.assertEqual(runner.main(["preflight", "--suite", str(self.suite),
                                      "--case-id", "1"]), 0)


if __name__ == "__main__":
    unittest.main()
