#!/usr/bin/env python3
"""Provider-native Refine Skill eval dispatch (experimental; isolated host required).

No cross-provider fallback. Preparing a case never starts a model.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import uuid

class Blocked(Exception):
    pass


def active_harness(env=None):
    env = os.environ if env is None else env
    claude = str(env.get('CLAUDECODE', '')).lower() not in ('', '0', 'false')
    codex = bool(env.get('CODEX_THREAD_ID') or env.get('CODEX_SESSION_ID'))
    if claude and codex:
        raise Blocked('Conflicting active Claude and Codex session markers; no fallback')
    if not (claude or codex):
        raise Blocked('Active harness unknown: cannot choose based on installed CLIs')
    return 'claude' if claude else 'codex'


def choose_harness(explicit, env=None, *, for_execution=False):
    try:
        discovered = active_harness(env)
    except Blocked as exc:
        if 'Conflicting' in str(exc) or for_execution or not explicit:
            raise
        return explicit  # Offline preparation only, not execution.
    if explicit and explicit != discovered:
        raise Blocked('Requested harness disagrees with active session: refusing cross-provider routing')
    return discovered


def safe_file(src, root):
    """Only accept regular files within root, with no symlinked path component."""
    src = Path(src)
    root = Path(root).resolve()
    try:
        relative = src.relative_to(root)
    except ValueError:
        raise Blocked(f'Source file outside target skill: {src}') from None
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise Blocked(f'Symlinked source path denied: {src}')
    if not src.is_file() or not src.resolve().is_relative_to(root):
        raise Blocked(f'Unsafe/missing source file: {src}')
    return src


def copy_skill(source, destination):
    source = source.resolve()
    entry = safe_file(source / 'SKILL.md', source)
    destination.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(entry, destination / 'SKILL.md')
    refs = source / 'references'
    if refs.is_dir():
        for src in refs.rglob('*'):
            if src.is_symlink():
                raise Blocked('Symlink in skill references')
            if src.is_file():
                safe_file(src, source)
                dst = destination / src.relative_to(source)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
    # Scripts/assets intentionally not staged until separately reviewed.


def get_case(suite, case_id):
    data = json.loads(suite.read_text(encoding='utf-8'))
    cases = data.get('evals', [])
    if not isinstance(cases, list):
        raise Blocked('Invalid evals array')
    matches = [c for c in cases if str(c.get('id')) == str(case_id)]
    if len(matches) != 1:
        raise Blocked('Case ID missing or not unique')
    case = matches[0]
    if not isinstance(case.get('prompt'), str) or not case['prompt'].strip():
        raise Blocked('No case prompt')
    assertions = case.get('assertions')
    if not isinstance(assertions, list) or not assertions or not all(isinstance(x, str) and x.strip() for x in assertions):
        raise Blocked('Approved assertions are required for native LLM grading')
    inputs = case.get('files') or []
    if not isinstance(inputs, list) or not all(isinstance(x, str) for x in inputs):
        raise Blocked('File fixtures must be a list of relative paths')
    return case, inputs


def fixture_sources(skill_root, inputs):
    """Resolve approved fixture paths relative to the *target skill root*.

    The evals.json convention, including scripts/validate_evals.py, uses
    skill-root-relative paths such as evals/files/fixture.txt. Never fall
    back to the suite directory or silently rewrite approved paths.
    """
    root = Path(skill_root).resolve()
    files = []
    for rel in inputs:
        relpath = Path(rel)
        if relpath.is_absolute() or not relpath.parts or '..' in relpath.parts:
            raise Blocked(f'Absolute/parent traversal fixture path refused: {rel}')
        files.append((safe_file(root / relpath, root), relpath))
    return files


def copy_inputs(skill_root, inputs, dst):
    for src, relpath in fixture_sources(skill_root, inputs):
        out = dst / relpath
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out)


def slug(value):
    val = re.sub(r'[^a-zA-Z0-9_-]', '-', str(value)).strip('-')
    if not val:
        raise Blocked('Invalid skill name or case ID')
    return val[:90]


def prepare(args, *, env=None):
    harness = choose_harness(args.harness, env)
    source = args.target_skill.resolve()
    if not source.is_dir():
        raise Blocked('Target skill directory does not exist')
    suite = safe_file(args.suite.resolve(), source)
    case, inputs = get_case(suite, args.case_id)
    # Fail before creating the output bundle when any fixture is unsafe/missing.
    fixture_sources(source, inputs)
    name = slug(source.name)
    case_name = slug(case['id'])
    base = args.output.resolve()
    base.mkdir(parents=True, exist_ok=True)
    bundle = base / f'{harness}-native-{case_name}-{uuid.uuid4().hex[:12]}'
    bundle.mkdir(exist_ok=False)
    metadata = dict(status='PREPARED_NOT_RUN', harness=harness, case_id=case['id'],
                    target_skill=str(source), suite=str(suite), native_result=None,
                    note='Preparation does not verify host isolation or run a model')
    if harness == 'claude':
        plugin = bundle / 'plugin'
        (plugin / '.claude-plugin').mkdir(parents=True)
        (plugin / '.claude-plugin' / 'plugin.json').write_text(json.dumps({
            'name': f'refine-eval-{name}', 'version': '0.0.1',
            'description': 'Temporary synthetic evaluation target; not for publication'
        }, indent=2), encoding='utf-8')
        copy_skill(source, plugin / 'skills' / name)
        case_dir = plugin / 'evals' / case_name
        grader_dir = case_dir / 'graders'
        grader_dir.mkdir(parents=True)
        prompt = '---\nruns: 3\nmax_turns: 10\nallowed_tools: [Read, Glob, Grep, Skill]\n---\n' + case['prompt'].strip() + '\n'
        (case_dir / 'prompt.md').write_text(prompt, encoding='utf-8')
        if inputs:
            copy_inputs(source, inputs, case_dir / 'fixtures')
            (case_dir / 'case.yaml').write_text('schema_version: "1.1"\nname: ' + case_name + '\ncontext:\n  add_dirs: [fixtures]\n', encoding='utf-8')
        for i, assertion in enumerate(case['assertions'], 1):
            (grader_dir / f'criterion-{i:02}.md').write_text(
                '---\ntype: llm\nfocus: last_message\n---\n'
                'PASS only if the following criterion is demonstrated by the answer; '
                'FAIL if missing, contradicted or unsupported. Cite specific evidence.\n'
                + assertion + '\n', encoding='utf-8')
        metadata['native_tool'] = 'claude plugin eval'
        metadata['native_format'] = 'plugin eval: prompt.md + graders/*.md; native JSON/HTML'
    elif harness == 'codex':
        cd = bundle / 'codex'
        (cd / 'with_skill' / '.agents' / 'skills').mkdir(parents=True)
        (cd / 'without_skill').mkdir(parents=True)
        (cd / 'judge').mkdir(parents=True)
        copy_skill(source, cd / 'with_skill' / '.agents' / 'skills' / name)
        if inputs:
            for arm in ('with_skill', 'without_skill'):
                copy_inputs(source, inputs, cd / arm / 'inputs')
        def provider(dir_name):
            return {'id': 'openai:codex-sdk', 'label': dir_name,
                    'config': {'working_dir': f'./{dir_name}', 'sandbox_mode': 'read-only',
                               'approval_policy': 'never', 'network_access_enabled': False,
                               'web_search_enabled': False, 'persist_threads': False,
                               'inherit_process_env': False, 'skip_git_repo_check': True}}
        judge = {'id': 'openai:codex-sdk', 'config': {
            'working_dir': './judge', 'sandbox_mode': 'read-only',
            'approval_policy': 'never', 'network_access_enabled': False,
            'web_search_enabled': False, 'inherit_process_env': False,
            'skip_git_repo_check': True, 'persist_threads': False}}
        config = {'description': f'Refine Skill synthetic case {case_name}',
                  'prompts': ['{{question}}'],
                  'providers': [provider('with_skill'), provider('without_skill')],
                  'tests': [{'vars': {'question': case['prompt'].strip()},
                             'assert': [{'type': 'llm-rubric',
                                         'value': 'PASS only if: ' + assertion +
                                                  '. FAIL for absent, contradicted, superficial or unsupported evidence.',
                                         'provider': judge} for assertion in case['assertions']]}],
                  'commandLineOptions': {'share': False, 'cache': False}}
        # JSON is valid YAML and preserves the precise provider-specific schema.
        (cd / 'promptfooconfig.yaml').write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')
        metadata['native_tool'] = 'promptfoo + openai:codex-sdk'
        metadata['native_format'] = 'Promptfoo: promptfooconfig.yaml + llm-rubric; native JSON'
    else:
        raise Blocked('Unknown harness')
    (bundle / 'manifest.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    return bundle


def native_command(bundle, manifest):
    harness = manifest['harness']
    if harness == 'claude':
        return ['claude', 'plugin', 'eval', str(bundle / 'plugin'), '--ablation', 'with-without',
                '--no-publish', '--json', str(bundle / 'claude-results.json')]
    if harness == 'codex':
        return ['promptfoo', 'eval', '--config', str(bundle / 'codex' / 'promptfooconfig.yaml'),
                '--no-cache', '--no-share', '--output', str(bundle / 'codex-results.json')]
    raise Blocked('Manifest harness invalid')


def execute(args, env=None):
    bundle = args.bundle.resolve()
    manifest = json.loads((bundle / 'manifest.json').read_text(encoding='utf-8'))
    harness = choose_harness(None, env, for_execution=True)
    if harness != manifest.get('harness'):
        raise Blocked('Prepared bundle belongs to another provider; no cross-provider execution')
    if manifest.get('status') != 'PREPARED_NOT_RUN':
        raise Blocked('Bundle is not a fresh prepared case')
    if not all([args.approved_case, args.approved_provider, args.host_enforced, args.synthetic_only]):
        raise Blocked('Explicit scoped approvals, synthetic-only input and independent host enforcement required')
    if not args.host_manifest or not args.host_manifest.is_file():
        raise Blocked('Independent execution host contract is required')
    host = json.loads(args.host_manifest.read_text(encoding='utf-8'))
    checks = ('disposable_workspace', 'mock_only_tools', 'no_live_credentials',
              'no_live_write_paths', 'no_unrestricted_shell', 'no_network_bypass',
              'child_agent_restrictions', 'per_tool_authorization', 'trusted_attempt_trace',
              'post_run_state_verification')
    if host.get('mode') != 'mock' or not host.get('verified_by') or any(host.get('checks', {}).get(k) is not True for k in checks):
        raise Blocked('Host manifest incomplete: host must independently enforce every check')
    # A JSON declaration cannot enforce any of these boundaries. The host MUST do so.
    cmd = native_command(bundle, manifest)
    binary = shutil.which(cmd[0])
    if not binary:
        raise Blocked(f'Native provider CLI unavailable: {cmd[0]}')
    # Never pull dependencies or run installers here.
    if harness == 'claude':
        env_override = dict(os.environ)
    else:
        env_override = dict(os.environ, PROMPTFOO_DISABLE_TELEMETRY='1',
                            PROMPTFOO_DISABLE_UPDATE='1', PROMPTFOO_DISABLE_SHARING='1',
                            PROMPTFOO_DISABLE_REMOTE_GENERATION='1')
    # The actual isolation policy is the responsibility of the independent host.
    result = subprocess.run(cmd, cwd=bundle, env=env_override, check=False)
    if result.returncode:
        raise Blocked(f'Native {harness} eval exited {result.returncode}; inspect provider output')
    # Do not claim a safety pass: require host-trusted trace/state audit and human review.
    print(f'PROVIDER_NATIVE_RESULTS_PENDING_HOST_AUDIT: {bundle}')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='action', required=True)
    sub.add_parser('inspect', help='detect active harness; never runs model')
    prep = sub.add_parser('prepare', help='prepare provider-native synthetic eval; no model run')
    prep.add_argument('--suite', type=Path, required=True)
    prep.add_argument('--case-id', required=True)
    prep.add_argument('--target-skill', type=Path, required=True)
    prep.add_argument('--output', type=Path, default=Path('eval-workspaces'))
    prep.add_argument('--harness', choices=['claude', 'codex'],
                      help='offline preparation only when no active harness marker exists')
    run = sub.add_parser('run', help='run provider-native command inside verified isolated host ONLY')
    run.add_argument('--bundle', type=Path, required=True)
    run.add_argument('--host-manifest', type=Path)
    run.add_argument('--approved-case', action='store_true')
    run.add_argument('--approved-provider', action='store_true')
    run.add_argument('--host-enforced', action='store_true')
    run.add_argument('--synthetic-only', action='store_true')
    opts = ap.parse_args(argv)
    try:
        if opts.action == 'inspect':
            print(json.dumps({'active_harness': active_harness(), 'model_executed': False}))
        elif opts.action == 'prepare':
            print('PREPARED_NOT_RUN:', prepare(opts))
        else:
            return execute(opts)
        return 0
    except (Blocked, OSError, ValueError, TypeError, json.JSONDecodeError) as e:
        print('BLOCKED_NOT_RUN:', e, file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
