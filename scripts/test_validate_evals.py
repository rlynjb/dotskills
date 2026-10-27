"""Unit tests for optional Agent Skills evals.json validation."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("validate_evals.py")
spec = importlib.util.spec_from_file_location("dotskills_validate_evals", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(validator)


class EvalDefinitionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name) / "example-skill"
        (root / "evals" / "files").mkdir(parents=True)
        (root / "SKILL.md").write_text("---\nname: example-skill\ndescription: Test skill.\n---\n# Example\n")
        (root / "evals" / "files" / "task.txt").write_text("safe fixture")
        self.path = root / "evals" / "evals.json"
        self.data = {
            "skill_name": "example-skill",
            "evals": [
                {"id": 1, "prompt": "Inspect this", "expected_output": "Correct outcome",
                 "files": ["evals/files/task.txt"]}
            ]
        }

    def write(self):
        self.path.write_text(json.dumps(self.data), encoding="utf-8")

    def test_valid_initial_cases_without_assertions(self):
        self.write()
        self.assertEqual(validator.validate_suite(self.path), [])

    def test_valid_cases_with_assertions(self):
        self.data["evals"][0]["assertions"] = ["The output cites a file"]
        self.write()
        self.assertEqual(validator.validate_suite(self.path), [])

    def test_invalid_duplicate_id_and_missing_expected_output(self):
        self.data["evals"].append({"id": 1, "prompt": "Another task"})
        self.write()
        issues = validator.validate_suite(self.path)
        self.assertTrue(any("duplicate id" in issue for issue in issues), issues)
        self.assertTrue(any("expected_output" in issue for issue in issues), issues)

    def test_prevents_path_traversal(self):
        self.data["evals"][0]["files"] = ["../secret.txt"]
        self.write()
        self.assertTrue(any("unsafe fixture" in i for i in validator.validate_suite(self.path)))

    def test_rejects_missing_files_and_wrong_skill_name(self):
        self.data["skill_name"] = "other-skill"
        self.data["evals"][0]["files"] = ["evals/files/missing.txt"]
        self.write()
        issues = validator.validate_suite(self.path)
        self.assertTrue(any("skill_name" in i for i in issues))
        self.assertTrue(any("missing or symlinked fixture" in i for i in issues))


if __name__ == "__main__":
    unittest.main()
