import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import native_eval as n

class NativeRouteTests(unittest.TestCase):
    def test_detection(self):
        self.assertEqual(n.active_harness({'CLAUDECODE':'1'}), 'claude')
        self.assertEqual(n.active_harness({'CODEX_THREAD_ID':'abc'}), 'codex')
        with self.assertRaises(n.Blocked): n.active_harness({})
        with self.assertRaises(n.Blocked): n.active_harness({'CLAUDECODE':'1','CODEX_THREAD_ID':'abc'})
        with self.assertRaises(n.Blocked): n.choose_harness('codex', {'CLAUDECODE':'1'})
        with self.assertRaises(n.Blocked): n.choose_harness(None, {}, for_execution=True)

    def fixtures(self, root):
        target = root/'test-skill'; target.mkdir()
        (target/'SKILL.md').write_text('---\nname: test-skill\ndescription: test\n---\nUse details.\n')
        folder = target/'evals'
        folder.mkdir()
        source = folder/'files'/'input.txt'
        source.parent.mkdir()
        source.write_text('synthetic fixture', encoding='utf-8')
        suite = folder/'evals.json'
        suite.write_text(json.dumps({'evals':[{'id':1,'prompt':'Summarize the input.',
             'expected_output':'a summary',
             'files':['evals/files/input.txt'],
             'assertions':['Includes an accurate summary'] }]}))
        return target,suite

    def set_case_files(self, suite, paths):
        cases = json.loads(suite.read_text(encoding='utf-8'))
        cases['evals'][0]['files'] = paths
        suite.write_text(json.dumps(cases), encoding='utf-8')

    def opts(self, target, suite, root):
        return SimpleNamespace(target_skill=target, suite=suite, case_id='1',
                               output=root/'out', harness=None)

    def test_prepare_claude_is_native_and_isolated(self):
        with TemporaryDirectory() as temp:
            root = Path(temp); target,suite = self.fixtures(root)
            opts = SimpleNamespace(target_skill=target,suite=suite,case_id='1',output=root/'out',harness=None)
            bundle = n.prepare(opts,env={'CLAUDECODE':'1'})
            self.assertTrue((bundle/'plugin'/'evals'/'1'/'graders'/'criterion-01.md').exists())
            self.assertTrue((bundle/'plugin'/'skills'/'test-skill'/'SKILL.md').exists())
            self.assertEqual((bundle/'plugin'/'evals'/'1'/'fixtures'/'evals'/'files'/'input.txt').read_text(),
                             'synthetic fixture')
            self.assertTrue((bundle/'plugin'/'evals'/'1'/'case.yaml').exists())
            self.assertFalse((bundle/'plugin'/'evals'/'1'/'fixtures'/'evals'/'evals.json').exists())
            cmd = n.native_command(bundle, json.loads((bundle/'manifest.json').read_text()))
            self.assertEqual(cmd[:3],['claude','plugin','eval'])
            self.assertNotIn('promptfoo', str(bundle))

    def test_prepare_codex_is_native_and_isolated(self):
        with TemporaryDirectory() as temp:
            root = Path(temp); target,suite = self.fixtures(root)
            opts = SimpleNamespace(target_skill=target,suite=suite,case_id='1',output=root/'out',harness=None)
            bundle = n.prepare(opts,env={'CODEX_THREAD_ID':'xyz'})
            config = json.loads((bundle/'codex'/'promptfooconfig.yaml').read_text())
            self.assertEqual([x['id'] for x in config['providers']],['openai:codex-sdk']*2)
            self.assertEqual(config['tests'][0]['assert'][0]['provider']['id'],'openai:codex-sdk')
            self.assertEqual(config['tests'][0]['assert'][0]['type'],'llm-rubric')
            self.assertTrue((bundle/'codex'/'with_skill'/'.agents'/'skills'/'test-skill'/'SKILL.md').exists())
            self.assertFalse((bundle/'codex'/'without_skill'/'.agents').exists())
            for arm in ('with_skill', 'without_skill'):
                self.assertEqual((bundle/'codex'/arm/'inputs'/'evals'/'files'/'input.txt').read_text(),
                                 'synthetic fixture')
                self.assertFalse((bundle/'codex'/arm/'inputs'/'evals'/'evals.json').exists())
            cmd = n.native_command(bundle,json.loads((bundle/'manifest.json').read_text()))
            self.assertEqual(cmd[0], 'promptfoo')

    def test_execution_denied_before_model_call(self):
        with TemporaryDirectory() as temp:
            root = Path(temp); target,suite=self.fixtures(root)
            opts = SimpleNamespace(target_skill=target,suite=suite,case_id='1',output=root/'out',harness=None)
            bundle=n.prepare(opts,env={'CLAUDECODE':'1'})
            run=SimpleNamespace(bundle=bundle,approved_case=False,approved_provider=False,
                host_enforced=False,synthetic_only=False,host_manifest=None)
            with patch('subprocess.run') as mock_run:
                with self.assertRaises(n.Blocked): n.execute(run,env={'CLAUDECODE':'1'})
                self.assertFalse(mock_run.called)
            with self.assertRaises(n.Blocked): n.execute(run,env={'CODEX_THREAD_ID':'1'})


    def test_rejects_unsafe_fixtures_without_creating_a_bundle(self):
        for fixture in ('../outside.txt', 'evals/../../outside.txt',
                        'evals/files/missing.txt', '.', '/etc/passwd', 'files/input.txt'):
            with self.subTest(path=fixture), TemporaryDirectory() as temp:
                root = Path(temp); target, suite = self.fixtures(root)
                self.set_case_files(suite, [fixture])
                opts = self.opts(target, suite, root)
                with self.assertRaises(n.Blocked):
                    n.prepare(opts, env={'CODEX_THREAD_ID': 'test'})
                self.assertFalse(opts.output.exists(), 'rejected inputs must not create a bundle')

    def test_rejects_symlinked_file_and_directory(self):
        with TemporaryDirectory() as temp:
            root = Path(temp); target, suite = self.fixtures(root)
            source = target/'evals'/'files'/'input.txt'
            alias = source.parent/'alias.txt'
            alias.symlink_to(source)
            self.set_case_files(suite, ['evals/files/alias.txt'])
            with self.assertRaises(n.Blocked):
                n.prepare(self.opts(target, suite, root), env={'CLAUDECODE': '1'})
            directory_alias = target/'evals'/'linked'
            directory_alias.symlink_to(source.parent, target_is_directory=True)
            self.set_case_files(suite, ['evals/linked/input.txt'])
            with self.assertRaises(n.Blocked):
                n.prepare(self.opts(target, suite, root), env={'CODEX_THREAD_ID': 'test'})
            self.assertFalse((root/'out').exists())

    def test_rejects_suite_outside_target_or_symlinked(self):
        with TemporaryDirectory() as temp:
            root = Path(temp); target, suite = self.fixtures(root)
            other = root/'external.json'
            other.write_text(suite.read_text())
            with self.assertRaises(n.Blocked):
                n.prepare(self.opts(target, other, root), env={'CLAUDECODE': '1'})
            alias = target/'evals'/'linked.json'
            alias.symlink_to(suite)
            with self.assertRaises(n.Blocked):
                n.prepare(self.opts(target, alias, root), env={'CLAUDECODE': '1'})
            self.assertFalse((root/'out').exists())

if __name__=='__main__': unittest.main()
