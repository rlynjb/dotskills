from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import contracts as c
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

    def prepared_bundle(self, root, harness='codex'):
        bundle = root/'prepared-bundle'
        (bundle/'codex').mkdir(parents=True)
        (bundle/'codex'/'promptfooconfig.yaml').write_text('{}\n', encoding='utf-8')
        (bundle/'manifest.json').write_text(json.dumps({
            'status': 'PREPARED_NOT_RUN', 'harness': harness, 'case_id': '1'
        }), encoding='utf-8')
        return bundle

    def plan_value(self):
        return {
            'schema_version': '0.2',
            'case_id': 'read-only-case',
            'case_revision': 'case-sha256',
            'rubric_revision': 'rubric-sha256',
            'skill_revision': 'skill-sha256',
            'fixture_revision': 'fixture-sha256',
            'provider': 'openai',
            'provider_version': '0.163.0',
            'model': 'approved-model',
            'model_version': 'approved-snapshot',
            'adapter': 'promptfoo-codex-sdk',
            'adapter_version': '0.125.1',
            'backend': 'native',
            'capabilities': {
                'profile': 'read-only',
                'filesystem_read': ['fixture'],
                'filesystem_write': [],
                'shell': False,
                'network': [],
                'mock_tools': [],
                'credentials': [],
                'side_effects': [],
                'evidence': ['action-trace', 'protected-state'],
            },
            'resource_limits': {
                'max_seconds': 120,
                'max_turns': 10,
                'max_output_bytes': 200000,
                'max_cost_usd': 1.0,
            },
            'comparison_arms': ['with-skill', 'without-skill'],
            'evidence_requirements': ['provider-result', 'host-audit'],
            'cleanup_requirements': ['workspace-removed', 'state-verified'],
        }

    def policy_files(self, root, *, verified, approval_digest=None):
        plan_value = self.plan_value()
        plan = c.RunPlan.from_dict(plan_value)
        approval = {
            'schema_version': plan.schema_version,
            'plan_digest': approval_digest or plan.digest(),
            'approved_by': 'human-reviewer',
            'provider': plan.provider,
            'model': plan.model,
            'adapter': plan.adapter,
            'backend': plan.backend,
            'capability_profile': plan.capabilities.profile,
            'capability_digest': plan.capabilities.digest(),
            'side_effects': list(plan.capabilities.side_effects),
        }
        enforcement = {
            'schema_version': plan.schema_version,
            'plan_digest': plan.digest(),
            'verified_by': 'trusted-host-verifier',
            'verifier_version': '1.0',
            'provider': plan.provider,
            'provider_version': plan.provider_version,
            'model': plan.model,
            'model_version': plan.model_version,
            'adapter': plan.adapter,
            'adapter_version': plan.adapter_version,
            'backend': plan.backend,
            'backend_version': 'verified-boundary-v1',
            'capability_profile': plan.capabilities.profile,
            'effective_policy_digest': plan.capabilities.digest(),
            'workspace_id': 'disposable-workspace-id',
            'probe_results': {
                'read-outside-workspace': 'PASS',
                'write-outside-workspace': 'PASS',
                'secondary-tool-route': 'PASS',
                'network-egress': 'PASS',
                'environment-secret': 'PASS',
                'action-trace-completeness': 'PASS',
                'state-snapshot': 'PASS',
                'cleanup-verification': 'PASS',
            },
            'enabled_tools': ['filesystem_read'],
            'disabled_tools': ['filesystem_write', 'shell', 'network', 'mock_tools'],
            'state_verification_method': 'tree-digest-v1',
            'cleanup_method': 'remove-and-verify-v1',
        }
        inventory_path = Path(__file__).with_name('provider_capabilities_v0_2.json')
        inventory = json.loads(inventory_path.read_text(encoding='utf-8'))
        if verified:
            for claim in inventory['claim_sets']['native-unverified'].values():
                claim['status'] = 'verified'
        values = {
            'run-plan.json': plan_value,
            'approval.json': approval,
            'enforcement.json': enforcement,
            'inventory.json': inventory,
        }
        paths = {}
        for name, value in values.items():
            path = root/name
            path.write_text(json.dumps(value), encoding='utf-8')
            paths[name] = path
        return SimpleNamespace(
            run_plan=paths['run-plan.json'],
            approval_receipt=paths['approval.json'],
            enforcement_receipt=paths['enforcement.json'],
            capability_inventory=paths['inventory.json'],
        )

    def run_opts(self, root, *, verified=True, approval_digest=None):
        policy = self.policy_files(
            root, verified=verified, approval_digest=approval_digest
        )
        return SimpleNamespace(bundle=self.prepared_bundle(root), **vars(policy))

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

    def test_run_rejects_legacy_boolean_only_authorization(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = self.prepared_bundle(root)
            run=SimpleNamespace(bundle=bundle,approved_case=False,approved_provider=False,
                host_enforced=False,synthetic_only=False,host_manifest=None)
            with patch('native_eval.subprocess.run') as mock_run:
                with self.assertRaises(n.Blocked): n.execute(run,env={'CODEX_THREAD_ID':'1'})
                self.assertFalse(mock_run.called)

    def test_assess_prints_blocked_reasons_without_model_call(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            policy = self.policy_files(root, verified=False)
            stderr = StringIO()
            argv = [
                'assess',
                '--run-plan', str(policy.run_plan),
                '--approval-receipt', str(policy.approval_receipt),
                '--enforcement-receipt', str(policy.enforcement_receipt),
                '--capability-inventory', str(policy.capability_inventory),
            ]
            with patch('native_eval.subprocess.run') as mock_run, redirect_stderr(stderr):
                self.assertEqual(n.main(argv), 2)
            self.assertFalse(mock_run.called)
            self.assertIn('BLOCKED_NOT_RUN', stderr.getvalue())
            self.assertIn('capabilities.filesystem_read', stderr.getvalue())

    def test_run_rejects_plan_receipt_digest_mismatch_before_model_call(self):
        with TemporaryDirectory() as temp:
            args = self.run_opts(Path(temp), approval_digest='wrong-digest')
            with patch('native_eval.subprocess.run') as mock_run:
                with self.assertRaisesRegex(n.Blocked, 'approval.plan_digest'):
                    n.execute(args, env={'CODEX_THREAD_ID': '1'})
            self.assertFalse(mock_run.called)

    def test_run_rejects_unverified_capability_before_model_call(self):
        with TemporaryDirectory() as temp:
            args = self.run_opts(Path(temp), verified=False)
            with patch('native_eval.subprocess.run') as mock_run:
                with self.assertRaisesRegex(n.Blocked, 'capabilities.filesystem_read'):
                    n.execute(args, env={'CODEX_THREAD_ID': '1'})
            self.assertFalse(mock_run.called)

    def test_run_uses_exact_approved_provider_command_after_policy_approval(self):
        with TemporaryDirectory() as temp:
            args = self.run_opts(Path(temp), verified=True)
            completed = SimpleNamespace(returncode=0)
            stdout = StringIO()
            with patch('native_eval.shutil.which', return_value='/approved/bin/promptfoo'), patch(
                'native_eval.subprocess.run', return_value=completed
            ) as mock_run, redirect_stdout(stdout):
                self.assertEqual(n.execute(args, env={'CODEX_THREAD_ID': '1'}), 0)
            self.assertIn('PENDING_HOST_AUDIT', stdout.getvalue())
            expected = n.native_command(
                args.bundle.resolve(),
                json.loads((args.bundle/'manifest.json').read_text(encoding='utf-8')),
            )
            self.assertEqual(mock_run.call_args.args[0], ['/approved/bin/promptfoo', *expected[1:]])
            self.assertEqual(mock_run.call_args.kwargs['cwd'], args.bundle.resolve())
            self.assertFalse(mock_run.call_args.kwargs['check'])

    def test_existing_prepare_claude_and_codex_cases_still_pass(self):
        for harness, env in (
            ('claude', {'CLAUDECODE': '1'}),
            ('codex', {'CODEX_THREAD_ID': '1'}),
        ):
            with self.subTest(harness=harness), TemporaryDirectory() as temp:
                root = Path(temp)
                target, suite = self.fixtures(root)
                bundle = n.prepare(self.opts(target, suite, root), env=env)
                manifest = json.loads((bundle/'manifest.json').read_text(encoding='utf-8'))
                self.assertEqual(manifest['harness'], harness)
                self.assertEqual(manifest['status'], 'PREPARED_NOT_RUN')


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
