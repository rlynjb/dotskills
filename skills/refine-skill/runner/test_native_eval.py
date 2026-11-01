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
        suite = root/'evals.json'
        suite.write_text(json.dumps({'evals':[{'id':1,'prompt':'Summarize the input.',
             'expected_output':'a summary', 'assertions':['Includes an accurate summary'] }]}))
        return target,suite

    def test_prepare_claude_is_native_and_isolated(self):
        with TemporaryDirectory() as temp:
            root = Path(temp); target,suite = self.fixtures(root)
            opts = SimpleNamespace(target_skill=target,suite=suite,case_id='1',output=root/'out',harness=None)
            bundle = n.prepare(opts,env={'CLAUDECODE':'1'})
            self.assertTrue((bundle/'plugin'/'evals'/'1'/'graders'/'criterion-01.md').exists())
            self.assertTrue((bundle/'plugin'/'skills'/'test-skill'/'SKILL.md').exists())
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

if __name__=='__main__': unittest.main()
