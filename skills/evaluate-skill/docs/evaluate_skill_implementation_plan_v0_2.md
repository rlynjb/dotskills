# Evaluate Skill v0.2 End-to-End Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the complete v0.2 evaluation architecture: trusted run planning, verified provider-native execution, independent evidence, bounded mutation and mock profiles, conditional Docker fallback, and full Evaluate Skill workflow integration.

**Architecture:** Keep Promptfoo and the existing Claude/Codex integrations as execution drivers. Build one end-to-end feature in ordered checkpoints: the control plane binds approvals and capabilities; the selected native or Docker execution boundary runs one untrusted agent; the evidence plane independently records enforcement, actions, state and cleanup; Evaluate Skill consumes those separate execution, quality and safety results. Native isolation is proven first, and Docker is implemented only when a documented native capability gap requires it—never as a silent fallback.

**Tech Stack:** Python 3.9 standard library, `unittest`, JSON contracts, existing Promptfoo/Claude/Codex CLIs.

**Spec:** `skills/evaluate-skill/docs/evaluate_skill_execution_architecture_v0_2.md`

## Global Constraints

- Preserve the existing four phases, Stages 0–11, and human checkpoints.
- Existing skill-local `evals/evals.json` cases load without mandatory schema migration.
- Default deny: missing, stale, conflicting, or unverified capability evidence blocks execution.
- Target skill, fixture content, and model output cannot change policy, approvals, receipts, or grading instructions.
- No production credentials, live external writes, staging/cloud integrations, automatic publication, unattended CI, or permission escalation.
- Native and Docker are explicit approved backends; no silent provider, model, or backend fallback.
- A copied workspace, provider sandbox option, manifest boolean, or container label is not by itself an enforcement receipt.
- Provider-native output and independent safety evidence remain separate dimensions.
- Support the observed local baseline without claiming compatibility beyond it: Python 3.9.6, Promptfoo 0.125.1, Codex CLI 0.163.0, and Claude Code 2.1.302.
- Add no third-party Python dependency to the coordinator, policy, probe, evidence, or backend modules.

## Review Focus

- A plan or receipt whose digest differs by one field must block before `subprocess.run`.
- Unknown or omitted capability coverage must block rather than defaulting to supported.
- Provider, adapter, backend, model, or tool-version drift between plan, inventory, and receipt must block.
- Missing, stale, failed, or irrelevant negative probes must block the capability they are supposed to prove.
- Legacy boolean flags or a self-declared host manifest must not bypass the new plan/receipt gate.
- Provider authentication must remain outside the untrusted workload and never appear in fixtures, traces, results, or subprocess environments visible to the tested agent.
- Missing tool attempts, truncated traces, failed cleanup, or incomplete state comparison must produce `UNKNOWN` or `INCOMPLETE`, never a safety Pass.
- Disposable writes and mock calls must succeed only inside their approved roots/routes while protected host state remains unchanged.

---

### Task 1: Versioned Run-Plan and Receipt Contracts

**Files:**
- Create: `skills/evaluate-skill/runner/contracts.py`
- Create: `skills/evaluate-skill/runner/test_contracts.py`

**Interfaces:**
- Consumes: JSON objects supplied by the trusted coordinator or independently verified host.
- Produces: `CapabilityRequirements`, `RunPlan`, `ApprovalReceipt`, `EnforcementReceipt`, `ContractError`, and deterministic `RunPlan.digest() -> str`.

- [ ] **Step 1: Write failing contract tests**

Add tests named:

```python
test_run_plan_digest_is_stable_for_key_order
test_run_plan_digest_changes_for_any_material_field
test_run_plan_rejects_unknown_profile_or_backend
test_run_plan_requires_version_and_resource_pins
test_approval_receipt_must_match_plan_digest_and_scope
test_enforcement_receipt_requires_independent_verifier_and_probe_results
test_contract_rejects_unknown_fields
```

Use complete minimal fixtures and assert `ContractError` for missing, extra, or invalid values. The material run-plan fields are: schema version, case/rubric/skill/fixture revisions, provider/model/adapter versions, backend, capability profile and exact surfaces, resource limits, comparison arms, and evidence/cleanup requirements.

- [ ] **Step 2: Run the tests and verify the contracts are absent**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_contracts.py -v`

Expected: FAIL because `contracts` cannot be imported.

- [ ] **Step 3: Implement strict dataclasses and canonical digesting**

In `contracts.py`, implement:

```python
class ContractError(ValueError): ...

@dataclass(frozen=True)
class CapabilityRequirements:
    profile: str
    filesystem_read: tuple[str, ...]
    filesystem_write: tuple[str, ...]
    shell: bool
    network: tuple[str, ...]
    mock_tools: tuple[str, ...]
    credentials: tuple[str, ...]
    side_effects: tuple[str, ...]
    evidence: tuple[str, ...]

@dataclass(frozen=True)
class RunPlan:
    ...
    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "RunPlan": ...
    def canonical_payload(self) -> dict[str, Any]: ...
    def digest(self) -> str: ...

@dataclass(frozen=True)
class ApprovalReceipt:
    ...
    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "ApprovalReceipt": ...

@dataclass(frozen=True)
class EnforcementReceipt:
    ...
    @classmethod
    def from_dict(cls, value: Mapping[str, Any]) -> "EnforcementReceipt": ...
```

Use sorted, separator-stable JSON and SHA-256 for the digest. Accept only profiles `no-tool`, `read-only`, `disposable-write`, and `mock-external`, and backends `native` and `docker`. Reject unknown fields instead of silently ignoring them.

- [ ] **Step 4: Run the contract tests**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_contracts.py -v`

Expected: all contract tests PASS.

- [ ] **Step 5: Commit the contracts**

```bash
git add skills/evaluate-skill/runner/contracts.py skills/evaluate-skill/runner/test_contracts.py
git commit -m "feat(evaluate-skill): add run plan contracts"
```

### Task 2: Pinned Provider Capability Inventory

**Files:**
- Create: `skills/evaluate-skill/runner/capability_inventory.py`
- Create: `skills/evaluate-skill/runner/provider_capabilities_v0_2.json`
- Create: `skills/evaluate-skill/runner/test_capability_inventory.py`

**Interfaces:**
- Consumes: the committed inventory JSON and observed executable versions.
- Produces: `CapabilityInventory`, `load_inventory(path: Path) -> CapabilityInventory`, `inspect_installed_versions() -> dict[str, str | None]`, and `validate_installed_versions(inventory, observed) -> list[str]`.

- [ ] **Step 1: Write failing inventory tests**

Add tests named:

```python
test_inventory_loads_pinned_local_baseline
test_every_capability_has_verified_unverified_or_unsupported_status
test_unverified_control_never_counts_as_enforced
test_missing_cli_is_reported_as_version_mismatch
test_provider_or_adapter_version_drift_is_reported
test_unknown_capability_name_is_rejected
```

Mock executable discovery and version output; tests must not call a model or install software.

- [ ] **Step 2: Run the tests and verify the inventory module is absent**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_capability_inventory.py -v`

Expected: FAIL because `capability_inventory` cannot be imported.

- [ ] **Step 3: Add the inventory schema and observed baseline**

Record Promptfoo 0.125.1, Codex CLI 0.163.0, and Claude Code 2.1.302. For each provider/backend/profile combination, record exact control names with status `verified`, `unverified`, or `unsupported`, plus the negative-probe IDs required to upgrade a claim to verified. Initially mark runtime confinement claims `unverified`; configuration availability is not enforcement evidence.

- [ ] **Step 4: Implement strict loading and version inspection**

Use `shutil.which` and hard-coded, argument-list subprocess calls only for `promptfoo --version`, `codex --version`, and `claude --version`. Return mismatches as data; do not install, update, authenticate, or execute providers.

- [ ] **Step 5: Run the inventory tests**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_capability_inventory.py -v`

Expected: all inventory tests PASS.

- [ ] **Step 6: Commit the inventory**

```bash
git add skills/evaluate-skill/runner/capability_inventory.py skills/evaluate-skill/runner/provider_capabilities_v0_2.json skills/evaluate-skill/runner/test_capability_inventory.py
git commit -m "feat(evaluate-skill): inventory provider capabilities"
```

### Task 3: Fail-Closed Backend Policy Assessment

**Files:**
- Create: `skills/evaluate-skill/runner/execution_policy.py`
- Create: `skills/evaluate-skill/runner/test_execution_policy.py`

**Interfaces:**
- Consumes: `RunPlan`, `ApprovalReceipt`, `EnforcementReceipt`, and `CapabilityInventory` from Tasks 1–2.
- Produces: `PolicyDecision(decision: str, backend: str | None, reasons: tuple[str, ...])` and `assess_run(plan, approval, enforcement, inventory) -> PolicyDecision`.

- [ ] **Step 1: Write failing policy tests**

Add tests named:

```python
test_verified_native_read_only_plan_is_approved
test_missing_or_mismatched_approval_blocks
test_unverified_required_native_capability_blocks
test_failed_or_missing_negative_probe_blocks
test_docker_is_never_selected_when_plan_approves_native
test_native_is_never_selected_when_plan_approves_docker
test_provider_model_adapter_or_backend_drift_blocks
test_unknown_required_evidence_blocks
test_self_declared_manifest_without_receipt_blocks
```

Each blocked decision must name the exact missing or conflicting field without exposing secrets.

- [ ] **Step 2: Run the tests and verify the policy module is absent**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_execution_policy.py -v`

Expected: FAIL because `execution_policy` cannot be imported.

- [ ] **Step 3: Implement `assess_run` with no fallback behavior**

Validate in this order: contract validity, plan digest binding, exact approval scope, installed-version pins, selected backend identity, capability coverage, relevant negative probes, enabled/disabled tool routes, state-verification method, and cleanup method. Return `APPROVED` only when every required claim is independently evidenced; otherwise return `BLOCKED`. Never change the plan's provider, model, backend, capabilities, or effects.

- [ ] **Step 4: Run the policy tests**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_execution_policy.py -v`

Expected: all policy tests PASS.

- [ ] **Step 5: Commit the policy gate**

```bash
git add skills/evaluate-skill/runner/execution_policy.py skills/evaluate-skill/runner/test_execution_policy.py
git commit -m "feat(evaluate-skill): add fail-closed execution policy"
```

### Task 4: Wire Contracts and Policy into the Native Dispatcher

**Files:**
- Modify: `skills/evaluate-skill/runner/native_eval.py`
- Modify: `skills/evaluate-skill/runner/test_native_eval.py`
- Modify: `skills/evaluate-skill/runner/README.md`
- Modify: `skills/evaluate-skill/references/eval-runner-integration.md`
- Modify: `skills/evaluate-skill/references/execution-safety-gate.md`

**Interfaces:**
- Consumes: the contract loaders and `assess_run` from Tasks 1–3.
- Produces: an `assess` CLI action and a `run` action that cannot reach `subprocess.run` without an `APPROVED` policy decision.

- [ ] **Step 1: Extend dispatcher tests with the new gate**

Add tests named:

```python
test_assess_prints_blocked_reasons_without_model_call
test_run_rejects_legacy_boolean_only_authorization
test_run_rejects_plan_receipt_digest_mismatch_before_model_call
test_run_rejects_unverified_capability_before_model_call
test_run_uses_exact_approved_provider_command_after_policy_approval
test_existing_prepare_claude_and_codex_cases_still_pass
```

Mock `subprocess.run` in all execution-gate tests. The one approved-path test may assert the exact command arguments but must not invoke a provider.

- [ ] **Step 2: Run the dispatcher tests and verify the new CLI is absent**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_native_eval.py -v`

Expected: new tests FAIL because receipt-aware assessment is not implemented.

- [ ] **Step 3: Add receipt-aware `assess` and strengthen `run`**

Add CLI inputs:

```text
assess --run-plan PLAN --approval-receipt APPROVAL --enforcement-receipt ENFORCEMENT --capability-inventory INVENTORY
run --bundle BUNDLE --run-plan PLAN --approval-receipt APPROVAL --enforcement-receipt ENFORCEMENT --capability-inventory INVENTORY
```

Remove the legacy boolean flags as sufficient authorization. Keep preparation behavior and provider-native result formats unchanged. `run` calls `assess_run` before executable discovery or `subprocess.run`; a blocked decision prints `BLOCKED_NOT_RUN` and returns nonzero.

- [ ] **Step 4: Update runner and safety documentation**

Document the new contracts, distinguish plan/receipt validation from physical enforcement, and state that the first slice still does not provision a native sandbox, Docker backend, independent verifier, model credentials, or action-trace collector.

- [ ] **Step 5: Run all offline evaluation and safety tests**

Run:

```bash
python3 -m unittest discover -s skills/evaluate-skill/runner -p 'test_*.py' -v
python3 -m unittest scripts/test_refine_eval_safety.py -v
python3 scripts/validate_evals.py --all
python3 scripts/validate_skill_repository_integrity.py
git diff --check
```

Expected: all tests and validators PASS; no model/provider evaluation command runs.

- [ ] **Step 6: Commit the dispatcher integration**

```bash
git add skills/evaluate-skill/runner skills/evaluate-skill/references/eval-runner-integration.md skills/evaluate-skill/references/execution-safety-gate.md
git commit -m "feat(evaluate-skill): gate runs with approved plans"
```

### Task 5: Native Enforcement Probes and Receipt Generation

**Files:**
- Create: `skills/evaluate-skill/runner/native_boundary.py`
- Create: `skills/evaluate-skill/runner/test_native_boundary.py`
- Create: `skills/evaluate-skill/runner/probes/read_outside_workspace.py`
- Create: `skills/evaluate-skill/runner/probes/write_outside_workspace.py`
- Create: `skills/evaluate-skill/runner/probes/network_egress.py`
- Create: `skills/evaluate-skill/runner/probes/environment_secret.py`
- Create: `skills/evaluate-skill/runner/probes/secondary_tool_route.py`

**Interfaces:**
- Consumes: an approved `RunPlan`, selected provider configuration, disposable workspace, and host-owned probe definitions.
- Produces: `ProbeResult`, `NativeBoundaryResult`, and `run_native_preflight(plan, workspace, provider_config) -> NativeBoundaryResult`; a trusted host may convert only a complete successful result into an `EnforcementReceipt`.

- [ ] **Step 1: Write failing native-boundary tests**

Add tests named:

```python
test_read_only_profile_runs_every_relevant_negative_probe
test_probe_failure_or_missing_result_blocks_receipt
test_probe_cannot_be_redefined_by_fixture_or_skill
test_probe_output_redacts_environment_values
test_provider_config_drift_invalidates_probe_result
test_native_boundary_never_claims_connector_or_mcp_isolation_without_probe
```

- [ ] **Step 2: Run the tests and verify the boundary module is absent**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_native_boundary.py -v`

Expected: FAIL because `native_boundary` cannot be imported.

- [ ] **Step 3: Implement host-owned capability probes**

Use immutable probe IDs and argument-list subprocess calls. Probes return only status, sanitized observations and the capability they test; they never print file contents, credentials, tokens or arbitrary environment values. A provider option such as `sandbox_mode: read-only` remains an input claim until the corresponding read/write/process/network probes pass in the effective runtime.

- [ ] **Step 4: Run native-boundary tests**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_native_boundary.py -v`

Expected: all tests PASS without invoking a model.

- [ ] **Step 5: Commit native preflight support**

```bash
git add skills/evaluate-skill/runner/native_boundary.py skills/evaluate-skill/runner/test_native_boundary.py skills/evaluate-skill/runner/probes
git commit -m "feat(evaluate-skill): add native enforcement probes"
```

### Task 6: Independent Host Evidence and State Audit

**Files:**
- Create: `skills/evaluate-skill/runner/evidence.py`
- Create: `skills/evaluate-skill/runner/test_evidence.py`
- Modify: `scripts/refine_eval_safety.py`
- Modify: `scripts/test_refine_eval_safety.py`

**Interfaces:**
- Consumes: plan digest, enforcement receipt, host-originated JSONL events, protected-state snapshot and approved disposable-state snapshot.
- Produces: `ExecutionStatus`, `SafetyStatus`, `EvidenceBundle`, `snapshot_tree(root, exclusions) -> StateSnapshot`, and `audit_evidence(plan, receipt, events, before, after) -> EvidenceAudit`.

- [ ] **Step 1: Write failing evidence tests**

Add tests named:

```python
test_complete_read_only_trace_and_unchanged_state_passes
test_truncated_trace_is_unknown
test_missing_post_run_snapshot_is_unknown
test_blocked_prohibited_attempt_is_safety_fail
test_allowed_disposable_write_is_recorded_without_changing_protected_state
test_changed_protected_file_is_safety_fail
test_unknown_event_type_is_not_silently_ignored
test_trace_redacts_known_secret_values
```

- [ ] **Step 2: Run the tests and verify the evidence module is absent**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_evidence.py -v`

Expected: FAIL because `evidence` cannot be imported.

- [ ] **Step 3: Implement deterministic state and trace auditing**

Hash relative paths, types, modes and contents without following symlinks. Compare protected and approved-disposable roots separately. Preserve `BLOCKED`, `INCOMPLETE`, `INFRA_ERROR`, `PASS`, `FAIL`, and `UNKNOWN` without collapsing them into one score. Refactor the CLI helper to call the shared evidence logic while preserving its existing commands.

- [ ] **Step 4: Run evidence and legacy safety tests**

Run:

```bash
python3 -m unittest skills/evaluate-skill/runner/test_evidence.py -v
python3 -m unittest scripts/test_refine_eval_safety.py -v
```

Expected: all evidence and existing safety tests PASS.

- [ ] **Step 5: Commit the evidence plane**

```bash
git add skills/evaluate-skill/runner/evidence.py skills/evaluate-skill/runner/test_evidence.py scripts/refine_eval_safety.py scripts/test_refine_eval_safety.py
git commit -m "feat(evaluate-skill): add independent evidence audit"
```

### Task 7: Provider-Native Read-Only Execution Proof

**Files:**
- Modify: `skills/evaluate-skill/runner/native_eval.py`
- Modify: `skills/evaluate-skill/runner/test_native_eval.py`
- Create: `skills/evaluate-skill/runner/test_provider_proof.py`
- Create: `skills/evaluate-skill/runner/proof/README.md`

**Interfaces:**
- Consumes: approved plan, matching receipts, verified native boundary, paired prepared bundle and provider authentication held outside the tested workload.
- Produces: provider-native results plus a versioned `EvidenceBundle`; no synthetic aggregate score.

- [ ] **Step 1: Write failing provider-proof orchestration tests**

Add tests named:

```python
test_each_arm_gets_independent_equivalent_fixture
test_answer_key_and_prior_results_are_absent_from_both_arms
test_provider_auth_is_not_in_agent_environment_or_trace
test_native_result_without_host_audit_is_incomplete
test_complete_provider_result_and_host_audit_preserve_three_status_dimensions
test_interrupted_arm_does_not_mark_pair_completed
```

- [ ] **Step 2: Run orchestration tests and verify proof support is absent**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_provider_proof.py -v`

Expected: FAIL on missing proof orchestration.

- [ ] **Step 3: Implement paired native-proof orchestration**

Keep provider commands in `native_eval.py`, but require the Task 3 policy decision, Task 5 boundary result and Task 6 evidence collector. Save each arm and provider-native result under a unique run identity. Do not expose authentication material to the agent workspace or include it in evidence.

- [ ] **Step 4: Run offline proof tests**

Run: `python3 -m unittest discover -s skills/evaluate-skill/runner -p 'test_*.py' -v`

Expected: all offline tests PASS; provider commands remain mocked.

- [ ] **Step 5: HUMAN GATE — authorize one synthetic native proof per provider**

Before any real provider call, show the exact case, fixture, model/provider, expected cost/budget, authentication boundary, capabilities, negative probes, external data disclosure and evidence paths. Run only providers that receive explicit scoped approval and whose installed interface passes the capability inventory. A missing approval or enforcement guarantee records `BLOCKED — NOT RUN`, not a skipped test.

- [ ] **Step 6: Preserve observed proof artifacts and grade the capability claims**

For each approved provider, require a genuine paired result, complete host evidence, unchanged protected state and cleanup result. Update capability statuses to `verified` only for the exact tested version/platform/profile. Do not extrapolate to untested tools, MCP, connectors, models or operating systems.

- [ ] **Step 7: Commit native proof integration and non-secret evidence metadata**

```bash
git add skills/evaluate-skill/runner
git commit -m "feat(evaluate-skill): prove native read-only execution"
```

### Task 8: Disposable-Write and Mock-External Profiles

**Files:**
- Create: `skills/evaluate-skill/runner/mock_dispatch.py`
- Create: `skills/evaluate-skill/runner/test_mock_dispatch.py`
- Create: `skills/evaluate-skill/runner/test_execution_profiles.py`
- Modify: `skills/evaluate-skill/runner/native_boundary.py`
- Modify: `skills/evaluate-skill/runner/evidence.py`

**Interfaces:**
- Consumes: approved `disposable-write` or `mock-external` plan, exact write roots, immutable mock tool registry and host-classified tool requests.
- Produces: `MockRegistry`, `authorize_tool_call(registry, plan, request) -> ToolDecision`, profile-specific enforcement receipts and state evidence.

- [ ] **Step 1: Write failing profile tests**

Add tests named:

```python
test_disposable_write_succeeds_only_inside_approved_root
test_out_of_root_write_and_symlink_escape_are_blocked_and_recorded
test_mock_tool_id_effect_and_destination_are_host_owned
test_live_http_shell_connector_and_child_agent_bypasses_are_denied
test_allowed_mock_call_is_logged_with_sanitized_arguments
test_mock_state_and_protected_state_are_audited_separately
```

- [ ] **Step 2: Run tests and verify profile support is absent**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_mock_dispatch.py skills/evaluate-skill/runner/test_execution_profiles.py -v`

Expected: FAIL on missing mock/profile interfaces.

- [ ] **Step 3: Implement immutable mock dispatch and bounded writes**

Bind `mock.*` identifiers to local implementations outside fixture control. Default write allowlists to empty. Resolve and verify every filesystem path against the approved disposable root without following symlinks. Record attempted blocked operations as safety failures where observable.

- [ ] **Step 4: Run profile and full offline tests**

Run:

```bash
python3 -m unittest skills/evaluate-skill/runner/test_mock_dispatch.py skills/evaluate-skill/runner/test_execution_profiles.py -v
python3 -m unittest discover -s skills/evaluate-skill/runner -p 'test_*.py' -v
```

Expected: all tests PASS without live external calls.

- [ ] **Step 5: Commit expanded profiles**

```bash
git add skills/evaluate-skill/runner
git commit -m "feat(evaluate-skill): add bounded write and mock profiles"
```

### Task 9: Conditional Docker Fallback

**Files:**
- Create when required: `skills/evaluate-skill/runner/docker_boundary.py`
- Create when required: `skills/evaluate-skill/runner/test_docker_boundary.py`
- Create when required: `skills/evaluate-skill/runner/docker/Dockerfile`
- Create when required: `skills/evaluate-skill/runner/docker/entrypoint.py`
- Modify: `skills/evaluate-skill/runner/execution_policy.py`

**Interfaces:**
- Consumes: a documented native capability gap from Tasks 7–8 and a separately approved `backend: docker` run plan.
- Produces when required: `DockerBoundaryResult` with equivalent probe, mount, network, process, secret, tool-route, resource and cleanup evidence.

- [ ] **Step 1: Decide whether Docker is required from observed native gaps**

Record one of two evidence-backed outcomes: `NOT REQUIRED` because every approved v1 profile is verified natively, or `REQUIRED` with the exact unsupported capability. This decision is not based on preference or case complexity.

- [ ] **Step 2: If required, write failing Docker boundary tests**

Add tests named:

```python
test_container_uses_read_only_root_and_explicit_workspace_mount
test_network_is_none_unless_mock_network_is_exactly_approved
test_host_credentials_and_socket_are_not_mounted
test_cpu_memory_process_and_duration_limits_are_required
test_native_and_docker_receipts_are_not_interchangeable
test_container_cleanup_and_post_run_state_are_verified
```

- [ ] **Step 3: If required, implement the smallest provider-compatible backend**

Reuse the same Promptfoo/provider configuration and grading path. Do not build a second agent loop or grader. Require reviewed image inputs, no runtime installation, a read-only root, explicit disposable mounts, deny-by-default network, scrubbed environment, non-root user, bounded resources and complete probes.

- [ ] **Step 4: Verify the Docker backend or the documented not-required decision**

Run Docker unit/command-construction tests and, after a separate approval, the same negative-probe suite used for native execution. If provider authentication cannot remain outside the workload, record `BLOCKED` and do not weaken credential isolation.

- [ ] **Step 5: Commit only evidence-supported Docker work**

```bash
git add skills/evaluate-skill/runner
git commit -m "feat(evaluate-skill): add verified docker fallback"
```

If Docker is not required, replace this commit with a documented ruling in the execution ledger and make no placeholder backend.

### Task 10: Workflow Integration, Acceptance Scenarios, and Release Decision

**Files:**
- Modify: `skills/evaluate-skill/SKILL.md`
- Modify: `skills/evaluate-skill/README.md`
- Modify: `skills/evaluate-skill/references/workflow.md`
- Modify: `skills/evaluate-skill/references/eval-runner-integration.md`
- Modify: `skills/evaluate-skill/references/execution-safety-gate.md`
- Modify: `skills/evaluate-skill/runner/README.md`
- Modify: `skills/evaluate-skill/docs/evaluate_skill_execution_architecture_v0_2.md`
- Modify: `skills/evaluate-skill/docs/evaluate_skill_system_boundary_map_v0_2.md`
- Create: `skills/evaluate-skill/runner/test_acceptance_v0_2.py`

**Interfaces:**
- Consumes: all control, execution and evidence-plane interfaces from Tasks 1–9.
- Produces: Stage 3/9 orchestration with explicit execution, quality and safety statuses; resumable versioned evidence; accurate user-facing documentation.

- [ ] **Step 1: Write failing end-to-end acceptance tests**

Cover every v1 acceptance scenario from the architecture document, including read-only, disposable-write, mock-external, prompt injection, copied-workspace rejection, conditional Docker, missing approval/credentials/receipt, truncated traces, paired baselines and independent Evaluate Skill self-test.

- [ ] **Step 2: Run acceptance tests and verify workflow gaps**

Run: `python3 -m unittest skills/evaluate-skill/runner/test_acceptance_v0_2.py -v`

Expected: FAIL only on missing Stage 3/9 workflow integration and status propagation.

- [ ] **Step 3: Integrate the implementation into Stages 3 and 9**

Keep existing human gates. Prepare locally in Stage 2, require a versioned approved plan and enforcement receipt in Stages 3/9, preserve native result schemas, review provider grades and independent evidence in Stages 4/10, and never auto-advance after `BLOCKED`, `INCOMPLETE`, `INFRA_ERROR`, safety `FAIL`, or safety `UNKNOWN`.

- [ ] **Step 4: Update documentation from observed implementation evidence**

Mark only verified profiles/providers/backends implemented. Keep unverified combinations explicit. Explain that future runs still require scoped approval, current capability checks, fresh receipts and isolated evidence even after v0.2 ships.

- [ ] **Step 5: Run the complete verification suite**

Run:

```bash
python3 -m unittest discover -s skills/evaluate-skill/runner -p 'test_*.py' -v
python3 -m unittest scripts/test_refine_eval_safety.py -v
python3 scripts/validate_evals.py --all
python3 scripts/validate_skill_repository_integrity.py
git diff --check
```

Expected: all offline tests and repository validators PASS. Any live acceptance evidence is reported separately with its provider/profile/version and must not be inferred from offline success.

- [ ] **Step 6: Commit the completed workflow integration**

```bash
git add skills/evaluate-skill scripts/refine_eval_safety.py scripts/test_refine_eval_safety.py
git commit -m "feat(evaluate-skill): complete v0.2 execution architecture"
```

## Self-Review Record

- **Spec coverage:** Tasks 1–4 implement M1–M2; Tasks 5–7 implement the native M3 proof and evidence plane; Task 8 implements expanded M4 profiles; Task 9 implements Docker only when observed native gaps require it; Task 10 completes M5 workflow integration and every v1 acceptance scenario.
- **Step scan:** Every unconditional code task has a failing-test step, minimal implementation step, verification command and commit boundary. Live provider and Docker operations retain explicit security/side-effect gates.
- **Type consistency:** All execution paths consume the same `RunPlan`, `ApprovalReceipt`, `EnforcementReceipt`, `CapabilityInventory`, `PolicyDecision` and `EvidenceBundle`. `native_eval.py` remains the sole provider-command dispatcher; Docker reuses it rather than adding another agent loop.
- **Review Focus coverage:** Digest tampering, unknown capability claims, version drift and legacy bypass are covered in Tasks 1–4; probe completeness, auth isolation, trace/state gaps and cleanup in Tasks 5–7; bounded writes, tool bypass and mock state in Task 8; backend mismatch and container escape surfaces in Task 9; blocked-state propagation and regression coverage in Task 10.
- **Proportion:** This is one master feature plan with ten testable checkpoints. The checkpoints are execution order and review boundaries, not separate feature plans or repeated human approval phases; only security-sensitive live runs, provider disclosure/cost and Docker execution pause for scoped approval.
