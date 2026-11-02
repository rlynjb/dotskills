from contextlib import redirect_stderr, redirect_stdout
import copy
from datetime import datetime, timedelta, timezone
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import contracts as c
import codex_host as ch
import native_eval as n

class NativeRouteTests(unittest.TestCase):
    def setUp(self):
        self.version_patch = patch(
            'native_eval.inspect_installed_versions',
            return_value={
                'promptfoo': '0.125.1',
                'codex': '0.163.0',
                'claude': '2.1.302',
                'node': '22.23.1',
            },
        )
        self.version_patch.start()
        self.addCleanup(self.version_patch.stop)

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
        skill = bundle/'codex'/'with_skill'/'.agents'/'skills'/'test-skill'
        skill.mkdir(parents=True)
        (skill/'SKILL.md').write_text('synthetic skill\n', encoding='utf-8')
        (bundle/'codex'/'without_skill').mkdir(parents=True)
        for arm in ('with_skill', 'without_skill'):
            inputs = bundle/'codex'/arm/'inputs'
            inputs.mkdir()
            (inputs/'input.txt').write_text('synthetic fixture\n', encoding='utf-8')
        (bundle/'codex'/'promptfooconfig.yaml').write_text(json.dumps({
            'providers': [
                {'id': 'openai:codex-sdk', 'label': 'with_skill', 'config': {}},
                {'id': 'openai:codex-sdk', 'label': 'without_skill', 'config': {}},
            ],
            'tests': [{'vars': {'question': 'synthetic prompt'}, 'assert': [{
                'type': 'llm-rubric',
                'value': 'synthetic rubric',
                'provider': {'id': 'openai:codex-sdk', 'config': {}},
            }]}],
        }) + '\n', encoding='utf-8')
        manifest = {
            'status': 'PREPARED_NOT_RUN', 'harness': harness, 'case_id': '1',
        }
        manifest.update(n._staged_revisions(bundle, manifest))
        (bundle/'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
        return bundle

    def host_policy(self, root, bundle, *, mcp_servers=("cua_repl", "node_repl")):
        host_root = root / "trusted-host-inputs"
        host_root.mkdir(exist_ok=True)
        command_line_tools = host_root / "CommandLineTools"
        command_line_tools.mkdir(exist_ok=True)
        home = host_root / "home"
        home.mkdir(exist_ok=True)
        home.chmod(0o700)
        codex_home = home / ".codex"
        codex_home.mkdir(mode=0o700, exist_ok=True)
        auth = codex_home / "auth.json"
        if not auth.exists():
            auth.write_text("{}\n", encoding="utf-8")
        auth.chmod(0o600)
        protected = host_root / "protected"
        protected.mkdir(exist_ok=True)
        codex = host_root / "codex"
        if not codex.exists():
            codex.write_text("binary placeholder\n", encoding="utf-8")
            codex.chmod(0o700)
        promptfoo_runtime = host_root / "promptfoo-runtime"
        promptfoo_runtime.mkdir(exist_ok=True)
        promptfoo = promptfoo_runtime / "promptfoo"
        if not promptfoo.exists():
            promptfoo.write_text("binary placeholder\n", encoding="utf-8")
            promptfoo.chmod(0o700)
        node = host_root / "node"
        if not node.exists():
            node.write_text("binary placeholder\n", encoding="utf-8")
            node.chmod(0o700)
        codex_sdk = promptfoo_runtime / "node_modules" / "@openai" / "codex-sdk"
        codex_sdk.mkdir(parents=True, exist_ok=True)
        package = codex_sdk / "package.json"
        if not package.exists():
            package.write_text(
                '{"name":"@openai/codex-sdk","version":"0.163.0"}\n',
                encoding="utf-8",
            )
        return ch.compile_read_only_policy(
            workspace=bundle.resolve(),
            codex_path=codex,
            promptfoo_path=promptfoo,
            node_path=node,
            promptfoo_runtime_root=promptfoo_runtime,
            codex_sdk_root=codex_sdk,
            command_line_tools_root=command_line_tools,
            home=home,
            mcp_servers=mcp_servers,
            protected_roots=(protected,),
        )

    def plan_value(self):
        return {
            'schema_version': '0.2',
            'case_id': '1',
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

    def plan_value_for_bundle(self, bundle):
        value = self.plan_value()
        manifest = json.loads((bundle/'manifest.json').read_text(encoding='utf-8'))
        for field in (
            'case_revision', 'rubric_revision', 'skill_revision', 'fixture_revision'
        ):
            value[field] = manifest[field]
        return value

    def policy_files(
        self,
        root,
        *,
        verified,
        approval_digest=None,
        prepared_bundle_digest='prepared-bundle-sha256',
        provider_config_digest='provider-config-sha256',
        plan_value=None,
    ):
        plan_value = self.plan_value() if plan_value is None else plan_value
        plan = c.RunPlan.from_dict(plan_value)
        now = datetime.now(timezone.utc)
        issued_at = (now - timedelta(minutes=5)).isoformat()
        expires_at = (now + timedelta(minutes=55)).isoformat()
        approval = {
            'schema_version': plan.schema_version,
            'plan_digest': approval_digest or plan.digest(),
            'approved_by': 'human-reviewer',
            'issued_at': issued_at,
            'expires_at': expires_at,
            'run_nonce': 'synthetic-run-nonce',
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
            'issued_at': issued_at,
            'expires_at': expires_at,
            'run_nonce': 'synthetic-run-nonce',
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
            'provider_config_digest': provider_config_digest,
            'prepared_bundle_digest': prepared_bundle_digest,
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
                'provider-auth-gateway': 'PASS',
                'resource-limits': 'PASS',
                'write-inside-workspace': 'PASS',
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
        bundle = self.prepared_bundle(root)
        value = self.plan_value_for_bundle(bundle)
        plan = c.RunPlan.from_dict(value)
        configured = n.configure_prepared_bundle(
            bundle, plan, self.host_policy(root, bundle)
        )
        policy = self.policy_files(
            root,
            verified=verified,
            approval_digest=approval_digest,
            prepared_bundle_digest=configured['bundle_digest'],
            provider_config_digest=configured['provider_config_digest'],
            plan_value=value,
        )
        enforcement = c.EnforcementReceipt.from_dict(
            json.loads(policy.enforcement_receipt.read_text(encoding='utf-8'))
        )
        n.bind_prepared_bundle(bundle, plan, enforcement)
        nonce_ledger = root / 'trusted-nonce-ledger'
        nonce_ledger.mkdir()
        return SimpleNamespace(
            bundle=bundle, nonce_ledger=nonce_ledger, **vars(policy)
        )

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
            with self.assertRaisesRegex(n.Blocked, 'plan-configured'):
                n.native_command(
                    bundle, json.loads((bundle/'manifest.json').read_text())
                )
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
            with self.assertRaisesRegex(n.Blocked, 'plan-configured'):
                n.native_command(
                    bundle, json.loads((bundle/'manifest.json').read_text())
                )

    def test_run_rejects_legacy_boolean_only_authorization(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = self.prepared_bundle(root)
            run=SimpleNamespace(bundle=bundle,approved_case=False,approved_provider=False,
                host_enforced=False,synthetic_only=False,host_manifest=None)
            with patch('native_eval.subprocess.run') as mock_run:
                with self.assertRaises(n.Blocked): n.execute(run,env={'CODEX_THREAD_ID':'1'})
                self.assertFalse(mock_run.called)

    def test_supervised_claim_revalidates_and_consumes_nonce_before_dispatch(self):
        with TemporaryDirectory() as temp:
            args = self.run_opts(Path(temp), verified=True)
            plan = c.RunPlan.from_dict(json.loads(args.run_plan.read_text()))
            enforcement = c.EnforcementReceipt.from_dict(
                json.loads(args.enforcement_receipt.read_text())
            )

            execution_id, manifest = n.claim_supervised_execution(
                args.bundle, plan, enforcement, args.nonce_ledger
            )

            self.assertTrue(execution_id)
            self.assertEqual(manifest["status"], "RUNNING")
            self.assertEqual(manifest["execution_id"], execution_id)
            self.assertEqual(manifest["run_nonce"], enforcement.run_nonce)
            self.assertEqual(len(list(args.nonce_ledger.glob("*.json"))), 1)
            with self.assertRaisesRegex(n.Blocked, "fresh bound"):
                n.claim_supervised_execution(
                    args.bundle, plan, enforcement, args.nonce_ledger
                )

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

    def test_assess_rejects_installed_provider_version_drift(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            policy = self.policy_files(root, verified=True)
            with patch(
                'native_eval.inspect_installed_versions',
                return_value={
                    'promptfoo': '0.125.1',
                    'codex': '9.9.9',
                    'claude': '2.1.302',
                    'node': '22.23.1',
                },
            ):
                decision, _, _, _ = n.assess_inputs(policy)

        self.assertEqual(decision.decision, 'BLOCKED')
        self.assertTrue(
            any('installed_versions.codex' in reason for reason in decision.reasons)
        )

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

    def test_run_rejects_unbound_bundle_before_model_call(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            policy = self.policy_files(root, verified=True)
            args = SimpleNamespace(bundle=self.prepared_bundle(root), **vars(policy))
            with patch('native_eval.subprocess.run') as mock_run:
                with self.assertRaisesRegex(n.Blocked, 'bound'):
                    n.execute(args, env={'CODEX_THREAD_ID': '1'})
            self.assertFalse(mock_run.called)

    def test_binding_rejects_case_mismatch(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = self.prepared_bundle(root)
            original_value = self.plan_value_for_bundle(bundle)
            original_plan = c.RunPlan.from_dict(original_value)
            configured = n.configure_prepared_bundle(
                bundle, original_plan, self.host_policy(root, bundle)
            )
            policy = self.policy_files(
                root,
                verified=True,
                prepared_bundle_digest=configured['bundle_digest'],
                provider_config_digest=configured['provider_config_digest'],
                plan_value=original_value,
            )
            enforcement = c.EnforcementReceipt.from_dict(
                json.loads(policy.enforcement_receipt.read_text(encoding='utf-8'))
            )
            plan_value = dict(original_value)
            plan_value['case_id'] = 'different-case'
            with self.assertRaisesRegex(n.Blocked, 'case'):
                n.bind_prepared_bundle(
                    bundle, c.RunPlan.from_dict(plan_value), enforcement
                )

    def test_binding_rejects_unconfigured_bundle(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = self.prepared_bundle(root)
            plan = c.RunPlan.from_dict(self.plan_value_for_bundle(bundle))
            policy = self.policy_files(
                root,
                verified=True,
                prepared_bundle_digest=n._bundle_digest(bundle),
            )
            enforcement = c.EnforcementReceipt.from_dict(
                json.loads(policy.enforcement_receipt.read_text(encoding='utf-8'))
            )
            with self.assertRaisesRegex(n.Blocked, 'configured'):
                n.bind_prepared_bundle(bundle, plan, enforcement)

    def test_configure_materializes_exact_approved_model_and_revisions(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            target, suite = self.fixtures(root)
            bundle = n.prepare(
                self.opts(target, suite, root), env={'CODEX_THREAD_ID': 'test'}
            )
            prepared = json.loads(
                (bundle / 'manifest.json').read_text(encoding='utf-8')
            )
            value = self.plan_value()
            for field in (
                'case_revision', 'rubric_revision', 'skill_revision',
                'fixture_revision',
            ):
                value[field] = prepared[field]
            plan = c.RunPlan.from_dict(value)

            policy = self.host_policy(root, bundle)
            configured = n.configure_prepared_bundle(bundle, plan, policy)
            config = json.loads(
                (bundle / 'codex' / 'promptfooconfig.yaml').read_text(
                    encoding='utf-8'
                )
            )

            self.assertEqual(configured['status'], 'CONFIGURED_NOT_BOUND')
            self.assertEqual(configured['plan_digest'], plan.digest())
            self.assertEqual(
                configured['provider_config_digest'],
                n._provider_config_digest(bundle, configured),
            )
            provider_configs = [item['config'] for item in config['providers']]
            provider_configs += [
                assertion['provider']['config']
                for test in config['tests']
                for assertion in test['assert']
            ]
            self.assertTrue(provider_configs)
            for provider_config in provider_configs:
                self.assertEqual(provider_config['model'], plan.model_version)
                self.assertEqual(
                    provider_config['max_turns'], plan.resource_limits['max_turns']
                )
                self.assertEqual(
                    provider_config['cli_config'], policy.canonical_payload()['cli_config']
                )

    def test_configure_injects_exact_host_policy_into_both_arms_and_judge(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = self.prepared_bundle(root)
            plan = c.RunPlan.from_dict(self.plan_value_for_bundle(bundle))
            policy = self.host_policy(root, bundle)

            n.configure_prepared_bundle(bundle, plan, policy)
            config = json.loads(
                (bundle / 'codex' / 'promptfooconfig.yaml').read_text(encoding='utf-8')
            )
            provider_configs = [item['config'] for item in config['providers']]
            provider_configs.extend(
                assertion['provider']['config']
                for test in config['tests']
                for assertion in test['assert']
            )

            self.assertEqual(len(provider_configs), 3)
            expected_cli_config = policy.canonical_payload()['cli_config']
            expected_cli_env = dict(policy.process_environment)
            for provider_config in provider_configs:
                self.assertEqual(
                    provider_config['codex_path_override'], str(policy.codex_path)
                )
                self.assertEqual(provider_config['cli_config'], expected_cli_config)
                self.assertEqual(provider_config['cli_env'], expected_cli_env)
                self.assertEqual(provider_config['approval_policy'], 'never')
                self.assertEqual(provider_config['web_search_mode'], 'disabled')
                self.assertFalse(provider_config['persist_threads'])
                self.assertFalse(provider_config['inherit_process_env'])
                self.assertTrue(provider_config['enable_streaming'])

    def test_configure_removes_legacy_sandbox_mode_and_ambient_network_fields(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = self.prepared_bundle(root)
            config_path = bundle / 'codex' / 'promptfooconfig.yaml'
            config = json.loads(config_path.read_text(encoding='utf-8'))
            configs = [item['config'] for item in config['providers']]
            configs.extend(
                assertion['provider']['config']
                for test in config['tests']
                for assertion in test['assert']
            )
            for provider_config in configs:
                provider_config.update(
                    sandbox_mode='read-only',
                    network_access_enabled=True,
                    web_search_enabled=True,
                )
            config_path.write_text(json.dumps(config) + '\n', encoding='utf-8')
            plan = c.RunPlan.from_dict(self.plan_value_for_bundle(bundle))

            n.configure_prepared_bundle(bundle, plan, self.host_policy(root, bundle))
            configured = json.loads(config_path.read_text(encoding='utf-8'))
            configured_values = [item['config'] for item in configured['providers']]
            configured_values.extend(
                assertion['provider']['config']
                for test in configured['tests']
                for assertion in test['assert']
            )
            for provider_config in configured_values:
                self.assertNotIn('sandbox_mode', provider_config)
                self.assertNotIn('network_access_enabled', provider_config)
                self.assertNotIn('web_search_enabled', provider_config)

    def test_configure_disables_cache_sharing_telemetry_updates_and_remote_generation(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = self.prepared_bundle(root)
            plan = c.RunPlan.from_dict(self.plan_value_for_bundle(bundle))

            n.configure_prepared_bundle(
                bundle, plan, self.host_policy(root, bundle)
            )
            config = json.loads(
                (bundle / 'codex' / 'promptfooconfig.yaml').read_text(encoding='utf-8')
            )

            self.assertEqual(
                config['commandLineOptions'], {'cache': False, 'share': False}
            )
            self.assertEqual(
                config['env'],
                {
                    'PROMPTFOO_DISABLE_REMOTE_GENERATION': '1',
                    'PROMPTFOO_DISABLE_SHARING': '1',
                    'PROMPTFOO_DISABLE_TELEMETRY': '1',
                    'PROMPTFOO_DISABLE_UPDATE': '1',
                },
            )

    def test_configure_rejects_mismatched_arm_or_judge_policy(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = self.prepared_bundle(root)
            plan = c.RunPlan.from_dict(self.plan_value_for_bundle(bundle))
            policy = self.host_policy(root, bundle)
            n.configure_prepared_bundle(bundle, plan, policy)
            config_path = bundle / 'codex' / 'promptfooconfig.yaml'
            config = json.loads(config_path.read_text(encoding='utf-8'))
            config['providers'][0]['config']['cli_config']['features']['apps'] = True
            config_path.write_text(json.dumps(config) + '\n', encoding='utf-8')

            with self.assertRaisesRegex(n.Blocked, 'host policy'):
                n.validate_configured_host_policy(bundle, policy)

    def test_configure_digest_changes_for_any_host_policy_field(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = self.prepared_bundle(root)
            plan = c.RunPlan.from_dict(self.plan_value_for_bundle(bundle))
            policy = self.host_policy(root, bundle)
            manifest = n.configure_prepared_bundle(bundle, plan, policy)
            original = manifest['provider_config_digest']
            config_path = bundle / 'codex' / 'promptfooconfig.yaml'
            config = json.loads(config_path.read_text(encoding='utf-8'))
            config['providers'][0]['config']['cli_config']['features']['apps'] = True
            config_path.write_text(json.dumps(config) + '\n', encoding='utf-8')

            self.assertNotEqual(original, n._provider_config_digest(bundle, manifest))

    def test_configure_rejects_enabled_mcp_web_app_collaboration_or_thread_reuse(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = self.prepared_bundle(root)
            plan = c.RunPlan.from_dict(self.plan_value_for_bundle(bundle))
            policy = self.host_policy(root, bundle)
            n.configure_prepared_bundle(bundle, plan, policy)
            config_path = bundle / 'codex' / 'promptfooconfig.yaml'
            original = json.loads(config_path.read_text(encoding='utf-8'))

            def enable_mcp(value):
                value['cli_config']['mcp_servers']['cua_repl']['enabled'] = True

            def enable_app(value):
                value['cli_config']['features']['apps'] = True

            def enable_web(value):
                value['web_search_mode'] = 'live'

            def enable_collaboration(value):
                value['collaboration_mode'] = 'coding'

            def enable_thread_reuse(value):
                value['persist_threads'] = True

            for name, mutate in (
                ('mcp', enable_mcp),
                ('app', enable_app),
                ('web', enable_web),
                ('collaboration', enable_collaboration),
                ('thread', enable_thread_reuse),
            ):
                with self.subTest(name=name):
                    changed = copy.deepcopy(original)
                    mutate(changed['providers'][0]['config'])
                    config_path.write_text(json.dumps(changed) + '\n', encoding='utf-8')
                    with self.assertRaises(n.Blocked):
                        n.validate_configured_host_policy(bundle, policy)

    def test_configure_recomputes_staged_revisions_instead_of_trusting_manifest(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            target, suite = self.fixtures(root)
            bundle = n.prepare(
                self.opts(target, suite, root), env={'CODEX_THREAD_ID': 'test'}
            )
            plan = c.RunPlan.from_dict(self.plan_value_for_bundle(bundle))
            staged_skill = next(
                (bundle / 'codex' / 'with_skill' / '.agents' / 'skills').glob('*')
            ) / 'SKILL.md'
            staged_skill.write_text('tampered after preparation\n', encoding='utf-8')

            with self.assertRaisesRegex(n.Blocked, 'skill_revision claim'):
                n.configure_prepared_bundle(
                    bundle, plan, self.host_policy(root, bundle)
                )

    def test_claude_command_selects_approved_model_version(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            target, suite = self.fixtures(root)
            bundle = n.prepare(
                self.opts(target, suite, root), env={'CLAUDECODE': '1'}
            )
            prepared = json.loads(
                (bundle / 'manifest.json').read_text(encoding='utf-8')
            )
            value = self.plan_value()
            value.update(
                provider='anthropic',
                provider_version='2.1.302',
                adapter='promptfoo-claude-agent-sdk',
            )
            for field in (
                'case_revision', 'rubric_revision', 'skill_revision',
                'fixture_revision',
            ):
                value[field] = prepared[field]
            plan = c.RunPlan.from_dict(value)
            manifest = n.configure_prepared_bundle(bundle, plan)

            command = n.native_command(bundle, manifest)

            self.assertIn('--model', command)
            self.assertEqual(command[command.index('--model') + 1], plan.model_version)

    def test_binding_rejects_receipt_for_different_staged_bundle(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = self.prepared_bundle(root)
            plan_value = self.plan_value_for_bundle(bundle)
            plan = c.RunPlan.from_dict(plan_value)
            configured = n.configure_prepared_bundle(
                bundle, plan, self.host_policy(root, bundle)
            )
            policy = self.policy_files(
                root,
                verified=True,
                prepared_bundle_digest='wrong-bundle-digest',
                provider_config_digest=configured['provider_config_digest'],
                plan_value=plan_value,
            )
            enforcement = c.EnforcementReceipt.from_dict(
                json.loads(policy.enforcement_receipt.read_text(encoding='utf-8'))
            )
            with self.assertRaisesRegex(n.Blocked, 'prepared bundle digest'):
                n.bind_prepared_bundle(bundle, plan, enforcement)

    def test_run_rejects_staged_artifact_mutation_after_binding(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            args = self.run_opts(root, verified=True)
            (args.bundle/'codex'/'promptfooconfig.yaml').write_text(
                '{"mutated":true}\n', encoding='utf-8'
            )
            with patch('native_eval.subprocess.run') as mock_run:
                with self.assertRaisesRegex(n.Blocked, 'digest'):
                    n.execute(args, env={'CODEX_THREAD_ID': '1'})
            self.assertFalse(mock_run.called)

    def test_run_rejects_missing_provider_auth_gateway_proof(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            args = self.run_opts(root, verified=True)
            enforcement = json.loads(
                args.enforcement_receipt.read_text(encoding='utf-8')
            )
            del enforcement['probe_results']['provider-auth-gateway']
            args.enforcement_receipt.write_text(
                json.dumps(enforcement), encoding='utf-8'
            )
            with patch('native_eval.subprocess.run') as mock_run:
                with self.assertRaisesRegex(n.Blocked, 'provider-auth-gateway'):
                    n.execute(args, env={'CODEX_THREAD_ID': '1'})
            self.assertFalse(mock_run.called)

    def test_run_uses_exact_approved_provider_command_after_policy_approval(self):
        with TemporaryDirectory() as temp:
            args = self.run_opts(Path(temp), verified=True)
            completed = SimpleNamespace(returncode=0)
            def complete_run(*_args, **_kwargs):
                (args.bundle/'codex-results.json').write_text(
                    json.dumps({
                        'provider_identity': {
                            'provider': 'openai',
                            'provider_version': '0.163.0',
                            'model': 'approved-model',
                            'model_version': 'approved-snapshot',
                            'adapter': 'promptfoo-codex-sdk',
                            'adapter_version': '0.125.1',
                        },
                        'results': ['synthetic'],
                    }) + '\n', encoding='utf-8'
                )
                return completed
            stdout = StringIO()
            with patch('native_eval.shutil.which', return_value='/approved/bin/promptfoo'), patch(
                'native_eval.subprocess.run', side_effect=complete_run
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
            self.assertEqual(mock_run.call_args.kwargs['timeout'], 120)
            manifest = json.loads(
                (args.bundle/'manifest.json').read_text(encoding='utf-8')
            )
            self.assertEqual(manifest['status'], 'PENDING_HOST_AUDIT')
            self.assertEqual(manifest['plan_digest'], c.RunPlan.from_dict(
                json.loads(args.run_plan.read_text(encoding='utf-8'))
            ).digest())

            with patch('native_eval.subprocess.run') as second_run:
                with self.assertRaisesRegex(n.Blocked, 'fresh bound'):
                    n.execute(args, env={'CODEX_THREAD_ID': '1'})
            self.assertFalse(second_run.called)

    def test_run_rejects_observed_model_snapshot_mismatch(self):
        with TemporaryDirectory() as temp:
            args = self.run_opts(Path(temp), verified=True)
            completed = SimpleNamespace(returncode=0)

            def complete_run(*_args, **_kwargs):
                (args.bundle/'codex-results.json').write_text(json.dumps({
                    'provider_identity': {
                        'provider': 'openai',
                        'provider_version': '0.163.0',
                        'model': 'approved-model',
                        'model_version': 'wrong-snapshot',
                        'adapter': 'promptfoo-codex-sdk',
                        'adapter_version': '0.125.1',
                    },
                    'results': ['synthetic'],
                }), encoding='utf-8')
                return completed

            with patch('native_eval.shutil.which', return_value='/approved/bin/promptfoo'), patch(
                'native_eval.subprocess.run', side_effect=complete_run
            ):
                with self.assertRaisesRegex(n.Blocked, '(?i)provider result identity'):
                    n.execute(args, env={'CODEX_THREAD_ID': '1'})

    def test_external_nonce_ledger_blocks_bundle_rollback_replay(self):
        with TemporaryDirectory() as temp:
            args = self.run_opts(Path(temp), verified=True)
            bound_manifest = (args.bundle/'manifest.json').read_text(encoding='utf-8')
            completed = SimpleNamespace(returncode=0)

            def complete_run(*_args, **_kwargs):
                (args.bundle/'codex-results.json').write_text(json.dumps({
                    'provider_identity': {
                        'provider': 'openai',
                        'provider_version': '0.163.0',
                        'model': 'approved-model',
                        'model_version': 'approved-snapshot',
                        'adapter': 'promptfoo-codex-sdk',
                        'adapter_version': '0.125.1',
                    },
                    'results': ['synthetic'],
                }), encoding='utf-8')
                return completed

            with patch('native_eval.shutil.which', return_value='/approved/bin/promptfoo'), patch(
                'native_eval.subprocess.run', side_effect=complete_run
            ) as provider_run:
                self.assertEqual(n.execute(args, env={'CODEX_THREAD_ID': '1'}), 0)
                (args.bundle/'codex-results.json').unlink()
                (args.bundle/'.execution-claim').unlink()
                (args.bundle/'manifest.json').write_text(
                    bound_manifest, encoding='utf-8'
                )
                with self.assertRaisesRegex(n.Blocked, 'nonce'):
                    n.execute(args, env={'CODEX_THREAD_ID': '1'})

            self.assertEqual(provider_run.call_count, 1)

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

    def test_docker_prepare_and_configure_materialize_provider_bundle_without_host_policy(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            target, suite = self.fixtures(root)
            opts = self.opts(target, suite, root)
            opts.harness = 'codex'
            opts.execution_backend = 'docker'
            bundle = n.prepare(opts, env={})
            manifest = json.loads((bundle / 'manifest.json').read_text(encoding='utf-8'))
            self.assertEqual(manifest['execution_backend'], 'docker')
            self.assertIn('-docker-', bundle.name)

            value = self.plan_value_for_bundle(bundle)
            value['schema_version'] = '0.4'
            value['backend'] = 'docker'
            value['resource_limits'].update({
                'max_cpus': 1.0,
                'max_memory_bytes': 536870912,
                'max_pids': 64,
                'max_tmpfs_bytes': 33554432,
            })
            plan = c.RunPlan.from_dict(value)
            configured = n.configure_prepared_bundle(bundle, plan)
            self.assertEqual(configured['status'], 'CONFIGURED_NOT_BOUND')
            self.assertNotIn('host_policy_digest', configured)
            promptfoo = json.loads(
                (bundle / 'codex' / 'promptfooconfig.yaml').read_text(encoding='utf-8')
            )
            for provider in promptfoo['providers']:
                self.assertEqual(
                    provider['config']['provider_transport'], 'trusted-gateway'
                )
                self.assertFalse(provider['config']['inherit_process_env'])


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
