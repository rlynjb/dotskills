"""Regression tests for OpenAI runtime-only install and plugin packaging."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "adapters" / "openai"


class OpenAIRuntimeCopyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def cli(self, script, *args, success=True):
        process = subprocess.run(
            [sys.executable, str(ADAPTER / script), *map(str, args)],
            capture_output=True, text=True
        )
        self.assertEqual(
            process.returncode == 0, success,
            process.stdout + process.stderr
        )
        return process

    def test_copy_omits_refine_skill_evaluator_files(self):
        self.cli("install_codex.py", "--target", self.root, "--skill", "refine-skill")
        installed = self.root / ".agents" / "skills" / "refine-skill"
        self.assertTrue((installed / "SKILL.md").is_file())
        self.assertTrue((installed / "references" / "workflow.md").is_file())
        self.assertFalse((installed / "evals").exists())

    def test_link_rejected_when_evaluator_material_present(self):
        self.cli(
            "install_codex.py", "--target", self.root, "--skill", "refine-skill",
            "--link", success=False
        )
        self.assertFalse((self.root / ".agents" / "skills" / "refine-skill").exists())

    def test_plugin_excludes_evals(self):
        output = self.root / "plugin"
        self.cli("build_plugin.py", "--skill", "refine-skill", "--output", output)
        self.assertTrue((output / "skills" / "refine-skill" / "SKILL.md").is_file())
        self.assertFalse((output / "skills" / "refine-skill" / "evals").exists())
        self.assertIn("name", json.loads((output / "plugin.json").read_text()))


if __name__ == "__main__":
    unittest.main()
