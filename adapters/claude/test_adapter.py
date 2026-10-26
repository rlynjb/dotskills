"""Filesystem/CLI regression tests; no Claude account or model calls required."""
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / 'adapters' / 'claude'


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name)

    def run_cli(self, script, *args, ok=True):
        result = subprocess.run([sys.executable, str(ADAPTER / script), *map(str, args)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return result

    def test_install_preview_copy_and_conflict(self):
        self.run_cli('install_claude.py', '--target', self.target, '--dry-run')
        self.assertFalse((self.target / '.claude').exists())
        self.run_cli('install_claude.py', '--target', self.target)
        installed = self.target / '.claude' / 'skills'
        self.assertEqual(len(list(installed.iterdir())), 6)
        for package in installed.iterdir():
            for file in (ROOT / 'skills' / package.name).rglob('*'):
                if file.is_file():
                    self.assertEqual(file.read_bytes(), (package / file.relative_to(ROOT / 'skills' / package.name)).read_bytes())
        marker = installed / 'refine-skill' / 'local.txt'
        marker.write_text('keep')
        self.run_cli('install_claude.py', '--target', self.target, ok=False)
        self.assertTrue(marker.exists())
        self.run_cli('install_claude.py', '--target', self.target, '--force')
        self.assertFalse(marker.exists())

    def test_selection_and_preflight(self):
        for args in [('--skill', 'missing'), ('--skill', 'code-review'),
                     ('--all', '--category', 'methodology')]:
            self.run_cli('install_claude.py', '--target', self.target, *args, ok=False)
        self.assertFalse((self.target / '.claude').exists())
        existing = self.target / '.claude' / 'skills' / 'context-engineering'
        existing.mkdir(parents=True)
        self.run_cli('install_claude.py', '--target', self.target, ok=False)
        self.assertFalse((existing.parent / 'refine-skill').exists())

    def test_plugin_layout_zip_and_hidden_exclusion(self):
        output = self.target / 'plugin'
        self.run_cli('build_plugin.py', '--all', '--output', output, '--zip')
        manifest = json.loads((output / '.claude-plugin' / 'plugin.json').read_text())
        self.assertEqual(manifest['name'], 'dotskills-methodology')
        catalog = json.loads((ROOT / 'catalog.json').read_text())['skills']
        expected = {s['name'] for s in catalog if s.get('exposed') is not False}
        self.assertEqual({p.name for p in (output / 'skills').iterdir()}, expected)
        self.assertFalse((output / 'plugin.json').exists())
        with zipfile.ZipFile(self.target / 'plugin.zip') as archive:
            self.assertIn('.claude-plugin/plugin.json', archive.namelist())
            for file in output.rglob('*'):
                if file.is_file():
                    self.assertEqual(file.read_bytes(), archive.read(file.relative_to(output).as_posix()))
        self.run_cli('build_plugin.py', '--output', output, ok=False)
        self.run_cli('build_plugin.py', '--output', output, '--force', '--skill', 'code-review-ddia')
        self.assertEqual([p.name for p in (output / 'skills').iterdir()], ['code-review-ddia'])

    def test_unsafe_paths(self):
        self.run_cli('build_plugin.py', '--output', ROOT / 'skills', '--force', ok=False)
        self.run_cli('build_plugin.py', '--name', '../escape', ok=False)
        external = self.target / 'external'
        external.mkdir()
        (external / 'keep').write_text('safe')
        project = self.target / 'project'
        project.mkdir()
        (project / '.claude').symlink_to(external, target_is_directory=True)
        self.run_cli('install_claude.py', '--target', project, '--force', ok=False)
        self.assertEqual((external / 'keep').read_text(), 'safe')

    def test_custom_build_preview_and_deduplication(self):
        output = self.target / 'new' / 'plugin'
        self.run_cli('build_plugin.py', '--output', output, '--dry-run')
        self.assertFalse(output.parent.exists())
        self.run_cli('build_plugin.py', '--output', output, '--name', 'my-skills',
                     '--skill', 'refine-skill', '--skill', 'refine-skill')
        self.assertEqual(len(list((output / 'skills').iterdir())), 1)
        self.assertEqual(json.loads((output / '.claude-plugin/plugin.json').read_text())['name'], 'my-skills')


if __name__ == '__main__':
    unittest.main()
