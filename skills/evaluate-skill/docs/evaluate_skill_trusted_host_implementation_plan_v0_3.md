# Evaluate Skill Trusted Host v0.3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the trusted native host that can independently enforce and prove a pinned, read-only Codex evaluation boundary before Evaluate Skill runs a live paired case.

**Architecture:** Keep the existing coordinator, Promptfoo/Codex provider harness, evidence model, and review workflow. Add a host-owned policy compiler and preflight issuer before dispatch, inject the exact custom Codex permission profile into every provider arm, supervise the one bound Promptfoo command, normalize provider turn items into an independent trace, and publish state/cleanup evidence with fail-closed parsing. The native route trusts the pinned harness only to route agent-controlled operations through Codex's Seatbelt sandbox; version, configuration, negative probes, observed tool items, state, and cleanup are verified outside the evaluated agent.

**Tech Stack:** Python 3.9 standard library, `unittest`, Codex CLI `0.163.0` permission profiles and macOS Seatbelt, Promptfoo `0.125.1` Codex SDK adapter.

**Spec:** `skills/evaluate-skill/docs/evaluate_skill_trusted_host_design_v0_3.md`

## Global Constraints

- Implement only the pinned Darwin arm64, native, Codex, read-only route.
- Do not call a model in implementation or automated tests. Real `codex sandbox` probes are allowed because they run local commands without provider inference.
- A live paired Learn Repo run remains a separate, explicitly approved action with exact case, model, limits, cost, disclosure, retention, and output paths.
- Use only synthetic disposable fixtures. Never expose a production repository, credential, connector, MCP server, or host skill to the evaluated process.
- File-based ChatGPT authentication stays in the trusted harness. Refuse `OPENAI_API_KEY`, `CODEX_API_KEY`, or equivalent API-key environment authentication.
- The canonical custom permission profile must deny the filesystem root, grant only minimal runtime and the exact arm workspace as read-only, grant the pinned Command Line Tools runtime as read-only for probes, and disable command network.
- Disable host skill discovery, web search, apps/connectors, collaboration/nested agents, thread reuse, and every configured MCP server. Do not depend on ambient global Codex configuration.
- Do not combine legacy `sandbox_mode` with the custom permission profile. The named profile and its exact inline configuration are the single sandbox configuration source.
- Preserve execution, quality, and safety as independent statuses. Model output and LLM-as-judge grading never certify enforcement.
- Reject unknown schemas, tool-item types, cache hits, version drift, policy drift, identity ambiguity, partial arms, timeouts, interrupted output, state drift, and cleanup failures.
- Add no third-party Python dependency.
- Publish host artifacts outside evaluated workspaces using exclusive, synced, no-replace writes. Redact secret-like values before persistence.

## Review Focus

- Global Codex config and MCP precedence cannot re-enable a surface the host disabled.
- File-based authentication remains usable by the harness while API keys and auth files are absent from the evaluated command environment and trace.
- Promptfoo result schema, cache state, adapter/model identity, and raw Codex turn metadata are parsed fail-closed rather than inferred from expected config.
- Workspace and protected-root validation resists symlink substitution, overlap, and time-of-check/time-of-use errors; evidence publication never overwrites an existing artifact.
- Timeout, interruption, malformed output, nonzero exit, partial cleanup, or missing final trace events cannot yield a complete safety result.

---

### Task 1: Canonical Codex Host Policy and Attestation

**Files:**
- Create: `skills/evaluate-skill/runner/codex_host.py`
- Create: `skills/evaluate-skill/runner/test_codex_host.py`
- Modify: `skills/evaluate-skill/runner/native_boundary.py`
- Modify: `skills/evaluate-skill/runner/test_native_boundary.py`

**Interfaces:**
- Consumes: pinned inventory values, installed platform/tool observations, exact arm workspace, configured MCP server names, and the trusted process environment.
- Produces: `CodexHostPolicy`, `HostAttestation`, `compile_read_only_policy(...)`, `attest_host(...)`, and `CodexHostError`.

- [ ] **Step 1: Write failing policy and attestation tests**

Add tests named:

```python
test_compiled_policy_is_canonical_root_deny_read_only_and_network_off
test_compiled_policy_disables_every_mcp_web_apps_collaboration_and_skills
test_compiled_policy_uses_cli_config_without_legacy_sandbox_mode
test_attestation_refuses_api_key_environment_authentication
test_attestation_refuses_missing_file_login_platform_or_version_drift
test_attestation_rejects_symlink_or_overlapping_workspace
test_boundary_launcher_allows_repeated_flags_but_rejects_unsafe_values
```

Assert the exact generated `cli_config`, named permission profile, scrubbed child
environment, and launcher argv. Repeated `-c` flags are valid argv and must not
be rejected merely because they repeat. Tests mock observations and never invoke
a model.

- [ ] **Step 2: Run the focused tests and verify RED**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_codex_host.py \
  skills/evaluate-skill/runner/test_native_boundary.py -v
```

Expected: FAIL because `codex_host.py` and the new behavior do not exist.

- [ ] **Step 3: Implement the immutable policy compiler**

Define frozen, strictly validated dataclasses. Generate deterministic JSON-safe
configuration for `permissions.evaluate-skill-read-only`, with `:root = deny`,
`:minimal = read`, the exact workspace root and pinned Command Line Tools root
as read-only, and network disabled. Generate explicit false/disabled values for
web, apps, collaboration, host-skill discovery, thread persistence, and every
observed MCP server. Expose a canonical payload and SHA-256 digest.

Reject relative, missing, symlinked, writable-policy, or overlapping protected
paths. Construct argument arrays without `shell=True`, and construct a minimal
allowlisted environment containing no secret-bearing variables.

- [ ] **Step 4: Implement host attestation and safe repeated argv**

Validate Darwin/arm64, exact Codex/Promptfoo versions, file-based `codex login
status`, API-key absence, real workspace identity, and the observed MCP inventory.
Return observations as data without persisting raw authentication output.

Change `native_boundary` launcher parsing so duplicates remain forbidden for
set-like fields but are legal for ordered argv. Preserve NUL, empty-value,
absolute-executable, and length validation.

- [ ] **Step 5: Run focused and regression tests**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_codex_host.py \
  skills/evaluate-skill/runner/test_native_boundary.py \
  skills/evaluate-skill/runner/test_capability_inventory.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit Task 1**

```bash
git add skills/evaluate-skill/runner/codex_host.py \
  skills/evaluate-skill/runner/test_codex_host.py \
  skills/evaluate-skill/runner/native_boundary.py \
  skills/evaluate-skill/runner/test_native_boundary.py
git commit -m "feat(evaluate-skill): compile trusted Codex host policy"
```

### Task 2: No-Model Preflight and Receipt Issuance

**Files:**
- Modify: `skills/evaluate-skill/runner/codex_host.py`
- Modify: `skills/evaluate-skill/runner/test_codex_host.py`
- Modify: `skills/evaluate-skill/runner/native_boundary.py`
- Modify: `skills/evaluate-skill/runner/test_native_boundary.py`

**Interfaces:**
- Consumes: configured bundle, immutable run plan, approval receipt, pinned inventory, compiled host policy, protected roots, and artifact directory.
- Produces: `PreflightRequest`, `PreflightResult`, `run_trusted_preflight(...)`, canonical host-policy artifact, snapshots, and a short-lived `EnforcementReceipt`.

- [ ] **Step 1: Write failing preflight tests**

Add tests named:

```python
test_preflight_runs_all_six_probes_without_provider_dispatch
test_preflight_binds_plan_bundle_policy_workspace_nonce_and_tools
test_preflight_blocks_failed_unknown_timed_out_or_missing_probe
test_preflight_blocks_changed_approval_inventory_or_provider_config
test_preflight_artifacts_use_exclusive_durable_publication
test_preflight_redacts_secret_like_observations
test_preflight_never_invokes_promptfoo_or_a_model_subprocess
```

Use injected command runners and a call ledger. Assert the only allowed commands
are version/login inspection and local `codex sandbox -- <probe>` invocations.

- [ ] **Step 2: Run focused tests and verify RED**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_codex_host.py \
  skills/evaluate-skill/runner/test_native_boundary.py -v
```

Expected: FAIL on absent preflight behavior.

- [ ] **Step 3: Implement preflight orchestration**

Validate the existing plan, approval, configured bundle, provider-config digest,
and inventory before any probe. Re-read the generated Promptfoo configuration
and require exact equality with the compiled host policy. Snapshot protected and
disposable roots without following symlinks.

Run the six existing immutable probes through the compiled absolute `codex
sandbox` launcher: environment-secret absence, network denial, outside-read
denial, secondary-route denial, inside-write denial, and outside-write denial.
Treat execution errors, timeouts, unknown results, or missing results as blocked.

- [ ] **Step 4: Issue and publish the bound receipt**

Construct the existing `EnforcementReceipt` only after all probes pass. Bind its
nonce and metadata to the plan, approval, provider configuration, prepared
bundle, policy digest, workspace identity, tool versions, state method, cleanup
method, and probe results. Publish canonical policy, snapshots, and receipt with
exclusive create, file sync, and directory sync. Never replace an existing path.

- [ ] **Step 5: Run focused and policy tests**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_codex_host.py \
  skills/evaluate-skill/runner/test_native_boundary.py \
  skills/evaluate-skill/runner/test_execution_policy.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit Task 2**

```bash
git add skills/evaluate-skill/runner/codex_host.py \
  skills/evaluate-skill/runner/test_codex_host.py \
  skills/evaluate-skill/runner/native_boundary.py \
  skills/evaluate-skill/runner/test_native_boundary.py
git commit -m "feat(evaluate-skill): issue verified native preflight receipts"
```

### Task 3: Strict Promptfoo Provider Configuration

**Files:**
- Modify: `skills/evaluate-skill/runner/native_eval.py`
- Modify: `skills/evaluate-skill/runner/test_native_eval.py`
- Modify: `skills/evaluate-skill/runner/test_provider_proof.py`

**Interfaces:**
- Consumes: prepared bundle and `CodexHostPolicy` from Tasks 1–2.
- Produces: configured paired Promptfoo file whose every Codex provider and judge carries the exact host `cli_config`, plus a bound provider-config digest.

- [ ] **Step 1: Write failing configuration tests**

Add tests named:

```python
test_configure_injects_exact_host_policy_into_both_arms_and_judge
test_configure_removes_legacy_sandbox_mode_and_ambient_network_fields
test_configure_disables_cache_sharing_telemetry_updates_and_remote_generation
test_configure_rejects_mismatched_arm_or_judge_policy
test_configure_digest_changes_for_any_host_policy_field
test_configure_rejects_enabled_mcp_web_app_collaboration_or_thread_reuse
```

Assert all three provider configurations are identical for security-relevant
fields; only the arm working directory and role-specific model settings may
differ.

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_native_eval.py \
  skills/evaluate-skill/runner/test_provider_proof.py -v
```

Expected: FAIL because the old file uses legacy `sandbox_mode` and lacks the
compiled host policy.

- [ ] **Step 3: Inject and re-read the canonical policy**

Require a `CodexHostPolicy` when configuring the supported native live route.
Write its exact `cli_config` into with-skill, without-skill, and judge providers.
Remove legacy sandbox and network fields that could take precedence. Keep
approval `never`, process-environment inheritance false, thread persistence
false, and streaming/raw turn capture enabled as required by the pinned adapter.

After writing, reload the file and compare every security-relevant field to the
policy. Include the canonical host-policy digest in the configured bundle and
provider-config digest.

- [ ] **Step 4: Run focused and acceptance tests**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_native_eval.py \
  skills/evaluate-skill/runner/test_provider_proof.py \
  skills/evaluate-skill/runner/test_acceptance_v0_2.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit Task 3**

```bash
git add skills/evaluate-skill/runner/native_eval.py \
  skills/evaluate-skill/runner/test_native_eval.py \
  skills/evaluate-skill/runner/test_provider_proof.py
git commit -m "feat(evaluate-skill): bind Codex host policy to Promptfoo"
```

### Task 4: Fail-Closed Promptfoo Result and Trace Parser

**Files:**
- Create: `skills/evaluate-skill/runner/provider_trace.py`
- Create: `skills/evaluate-skill/runner/test_provider_trace.py`
- Modify: `skills/evaluate-skill/runner/evidence.py`
- Modify: `skills/evaluate-skill/runner/test_evidence.py`

**Interfaces:**
- Consumes: Promptfoo `0.125.1` ResultsFile JSON, bound configured-provider identity, and observed Codex session identity records.
- Produces: `ParsedProviderRun`, per-arm `ProviderResult`, sanitized `AuditEvent` values, source-result digests, and `ProviderTraceError`.

- [ ] **Step 1: Write failing parser tests**

Add tests named:

```python
test_parser_requires_exactly_one_with_skill_and_one_without_skill_result
test_parser_requires_pinned_provider_model_adapter_and_session_identity
test_parser_rejects_cache_hits_missing_raw_turns_or_unknown_schema
test_parser_rejects_mcp_web_collaboration_file_change_and_unknown_item_types
test_parser_normalizes_command_items_without_persisting_secrets_or_raw_logs
test_parser_rejects_malformed_incomplete_or_duplicate_command_items
test_parser_keeps_quality_grades_separate_from_safety_events
test_parser_binds_each_normalized_trace_to_source_result_digest
```

Use minimal, versioned fixtures modeled on the installed Promptfoo schema and
Codex raw turn items. Do not accept a caller-supplied identity assertion unless
it is bound to independently observed session metadata.

- [ ] **Step 2: Run parser tests and verify RED**

Run:

```bash
python3 -m unittest skills/evaluate-skill/runner/test_provider_trace.py -v
```

Expected: FAIL because `provider_trace.py` does not exist.

- [ ] **Step 3: Implement strict schema and identity parsing**

Require the pinned ResultsFile shape and exactly the approved two comparison
arms. Resolve provider/model/adapter identity from the bound configuration and
observed Codex session metadata, then require agreement. Reject missing session
IDs, cache flags or cache-derived results, unexpected providers, duplicate arms,
and unknown required fields rather than defaulting them.

- [ ] **Step 4: Normalize sanitized trace events**

Parse each `response.raw` Codex turn. Allow only explicitly enumerated
message/reasoning/command-execution item types needed by this read-only route.
Reject file changes, MCP calls, web items, collaboration items, or unknown tool
items. Persist command argv or a canonical digest only after redaction; persist
stdout/stderr digests and bounded metadata, not unrestricted logs. Emit source
result and provider-result digests and keep rubric grades as quality data only.

- [ ] **Step 5: Run parser and evidence tests**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_provider_trace.py \
  skills/evaluate-skill/runner/test_evidence.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit Task 4**

```bash
git add skills/evaluate-skill/runner/provider_trace.py \
  skills/evaluate-skill/runner/test_provider_trace.py \
  skills/evaluate-skill/runner/evidence.py \
  skills/evaluate-skill/runner/test_evidence.py
git commit -m "feat(evaluate-skill): normalize trusted provider traces"
```

### Task 5: Supervised Execution, State Verification, and Cleanup

**Files:**
- Modify: `skills/evaluate-skill/runner/codex_host.py`
- Modify: `skills/evaluate-skill/runner/test_codex_host.py`
- Modify: `skills/evaluate-skill/runner/native_eval.py`
- Modify: `skills/evaluate-skill/runner/test_native_eval.py`
- Modify: `skills/evaluate-skill/runner/test_provider_proof.py`

**Interfaces:**
- Consumes: single-use preflight result and receipt, configured bundle, exact bound Promptfoo command, protected/disposable roots, and an injected process runner.
- Produces: `SupervisedRunResult`, closed host trace, verified state/cleanup records, normalized paired provider results, and final evidence inputs.

- [ ] **Step 1: Write failing supervision tests**

Add tests named:

```python
test_supervisor_runs_only_exact_bound_command_with_minimal_environment
test_supervisor_revalidates_single_use_nonce_plan_bundle_policy_and_receipt
test_supervisor_records_start_before_dispatch_and_end_after_cleanup
test_supervisor_enforces_timeout_output_limit_and_nonzero_exit_failure
test_supervisor_blocks_partial_malformed_or_interrupted_provider_output
test_supervisor_blocks_protected_state_change_or_cleanup_failure
test_supervisor_publishes_per_arm_results_and_evidence_without_overwrite
test_supervisor_never_marks_execution_quality_or_safety_from_each_other
```

All tests use an injected fake process runner. Include interruption between each
durable state transition and assert the recovered status remains incomplete.

- [ ] **Step 2: Run focused tests and verify RED**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_codex_host.py \
  skills/evaluate-skill/runner/test_native_eval.py \
  skills/evaluate-skill/runner/test_provider_proof.py -v
```

Expected: FAIL on absent supervisor behavior.

- [ ] **Step 3: Implement exact-command supervision**

Revalidate every binding immediately before dispatch and atomically consume the
nonce. Record `run_start`, execute exactly the manifest command as an argv array
with the scrubbed environment, hard timeout, and bounded output capture, then
parse the result through `provider_trace.py`. Do not infer success from exit zero
alone. Record process-output digests and fail closed on any ambiguity.

- [ ] **Step 4: Verify state, cleanup, and durable evidence**

Capture after snapshots, compare all protected roots, and require only approved
read-only workspace effects. Remove each disposable arm workspace, verify it is
gone without traversing unsafe symlinks, close the trace, and publish normalized
results/evidence with exclusive synced writes. Leave the run incomplete on any
timeout, interruption, state drift, parse failure, or cleanup failure.

- [ ] **Step 5: Run supervision and evidence suites**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_codex_host.py \
  skills/evaluate-skill/runner/test_native_eval.py \
  skills/evaluate-skill/runner/test_provider_trace.py \
  skills/evaluate-skill/runner/test_provider_proof.py \
  skills/evaluate-skill/runner/test_evidence.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit Task 5**

```bash
git add skills/evaluate-skill/runner/codex_host.py \
  skills/evaluate-skill/runner/test_codex_host.py \
  skills/evaluate-skill/runner/native_eval.py \
  skills/evaluate-skill/runner/test_native_eval.py \
  skills/evaluate-skill/runner/test_provider_proof.py
git commit -m "feat(evaluate-skill): supervise native provider execution"
```

### Task 6: Trusted Host CLI, Real Local Probe, and Workflow Documentation

**Files:**
- Create: `skills/evaluate-skill/runner/trusted_host.py`
- Create: `skills/evaluate-skill/runner/test_trusted_host_cli.py`
- Modify: `skills/evaluate-skill/runner/README.md`
- Modify: `skills/evaluate-skill/README.md`
- Modify: `skills/evaluate-skill/SKILL.md`
- Modify: `skills/evaluate-skill/references/eval-runner-integration.md`
- Modify: `skills/evaluate-skill/references/execution-safety-gate.md`
- Modify: `skills/evaluate-skill/runner/proof/README.md`
- Modify: `skills/evaluate-skill/runner/proof/status_v0_2.json`

**Interfaces:**
- Consumes: explicit CLI paths for plan, approval, configured bundle, inventory, workspaces, protected roots, and artifact directory.
- Produces: `preflight` and `run` commands, machine-readable blocked/ready results, and operator documentation.

- [ ] **Step 1: Write failing CLI tests**

Add tests named:

```python
test_preflight_cli_never_dispatches_provider
test_run_cli_requires_fresh_matching_preflight_and_explicit_live_authorization
test_cli_reports_blocked_not_run_without_secret_values
test_cli_refuses_implicit_paths_backend_fallback_and_overwrite
test_real_probe_command_is_separate_from_live_provider_command
```

Invoke `main(argv, dependencies=...)` directly with fakes. Do not run a model.

- [ ] **Step 2: Run CLI tests and verify RED**

Run:

```bash
python3 -m unittest skills/evaluate-skill/runner/test_trusted_host_cli.py -v
```

Expected: FAIL because `trusted_host.py` does not exist.

- [ ] **Step 3: Implement narrow preflight and run commands**

Require every security-relevant path and identity explicitly. `preflight` may
inspect versions/login and run local sandbox probes but cannot dispatch
Promptfoo. `run` requires a fresh matching receipt plus an explicit live-run
authorization object already bound by Evaluate Skill. Return stable JSON status
and nonzero exit codes on blocked or incomplete states.

- [ ] **Step 4: Prove the installed native boundary without a model**

Run the six repository-owned probes through the installed absolute Codex binary
and the compiled custom permission profile, with a scrubbed environment. Record
only the sanitized probe result in the local proof directory. This is a native
boundary preflight, not a live provider evaluation, and must leave live status
as `BLOCKED_NOT_RUN` until the later separately approved paired proof.

- [ ] **Step 5: Update workflow and operator documentation**

Document the trusted-host boundary, exact prerequisites, artifact locations,
preflight/run separation, live approval requirement, failure meanings, cleanup,
and why the LLM judge cannot certify safety. Keep unsupported Claude, writable,
mock-external, connector, MCP, and Docker routes visibly blocked.

- [ ] **Step 6: Run all repository verification**

Run:

```bash
python3 -m unittest discover -s skills/evaluate-skill/runner -p 'test_*.py' -v
python3 skills/validate_skills.py
python3 skills/validate_references.py
git diff --check
```

Expected: all tests and validators PASS. Confirm no live provider subprocess was
started and `status_v0_2.json` still reports live proof as not run.

- [ ] **Step 7: Commit Task 6**

```bash
git add skills/evaluate-skill/runner/trusted_host.py \
  skills/evaluate-skill/runner/test_trusted_host_cli.py \
  skills/evaluate-skill/runner/README.md \
  skills/evaluate-skill/README.md \
  skills/evaluate-skill/SKILL.md \
  skills/evaluate-skill/references/eval-runner-integration.md \
  skills/evaluate-skill/references/execution-safety-gate.md \
  skills/evaluate-skill/runner/proof/README.md \
  skills/evaluate-skill/runner/proof/status_v0_2.json
git commit -m "docs(evaluate-skill): integrate trusted native host"
```

## Final Verification and Review

- [ ] Run the full Evaluate Skill runner suite, skill validators, reference validators, and `git diff --check` from a clean feature worktree.
- [ ] Re-run the real six-probe Codex sandbox preflight without a model call.
- [ ] Confirm the main checkout's unrelated user files are untouched.
- [ ] Review the full feature diff against the design and the five review-focus risks above.
- [ ] Request a fresh code review. Resolve every Critical or Important finding with a regression test and rerun verification.
- [ ] Confirm live provider proof remains `BLOCKED_NOT_RUN`; present the exact live Learn Repo case and limits for separate user approval rather than starting it automatically.

## Self-Review Checklist

- Does any ambient global Codex configuration take precedence over, merge with,
  or escape the generated profile?
- Can any auth value enter a sandboxed child, fixture, stdout/stderr artifact,
  normalized trace, or failure message?
- Can config-only expected identity be mistaken for observed provider/session
  identity?
- Can a symlink swap, path overlap, stale file descriptor, or artifact overwrite
  invalidate state or receipt evidence?
- Can a cache hit, unknown tool item, partial arm, timeout, signal, nonzero exit,
  interrupted write, or failed cleanup become a pass?
- Are execution success, rubric quality, and safety evidence kept independently
  reviewable at every transition?
