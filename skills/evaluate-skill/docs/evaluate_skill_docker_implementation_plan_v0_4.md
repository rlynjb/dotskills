# Evaluate Skill Docker-Only v0.4 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace live provider-native execution with one fail-closed,
Docker-only evaluation boundary that keeps provider credentials outside the
workload and produces independent, plan-bound safety evidence.

**Architecture:** Run the complete evaluated provider harness for each arm in
a minimal, digest-pinned, non-root workload container on a private per-run
network. A separate trusted gateway owns real provider credentials and enforces
the approved provider, model, session, expiry, and budgets; a host supervisor
owns Docker, observation, state verification, cleanup, and authenticated
receipts. Native Codex and Claude sandboxes are historical research only and
never a live fallback.

**Tech Stack:** Python 3.9 standard library, `unittest`, Docker Engine/Desktop,
OCI/Dockerfiles, Linux namespaces/cgroups/capabilities/seccomp, Promptfoo
Codex SDK adapter, Claude plugin-eval adapter.

**Spec:** `skills/evaluate-skill/docs/evaluate_skill_execution_architecture_v0_4.md`

## Global Constraints

- Live evaluated-agent execution accepts only `backend: docker`; Docker
  unavailable or unverified means `BLOCKED_NOT_RUN`.
- Preserve historical v0.2/v0.3 artifacts and tests, but no active command may
  dispatch through the native host.
- Implement Codex `read-only` first on the pinned `Darwin 25.4.0` arm64 host
  with an approved Docker Desktop client/daemon pair. Claude, native Linux,
  Intel macOS, `no-tool`, `disposable-write`, `mock-external`, connector, and
  MCP routes remain unsupported until they pass the same gates.
- No Docker install, image pull/build, container launch, provider call, or paid
  inference in ordinary unit tests.
- Require separate human approval before installing Docker, downloading/building
  images, running real containers, or invoking a provider.
- The workload never receives the Docker socket, host home, original repo,
  rubric, answer key, prior result, long-lived provider credential, host
  network, or privileged capability.
- The workload has no direct internet route. Provider inference crosses only a
  private internal run network to a trusted gateway sibling container; only
  that gateway attaches to a separate egress network.
- The gateway must not pass through a usable real credential. If the pinned
  provider adapter cannot use the gateway, keep that route blocked.
- Pin base and final images by digest; install nothing at runtime; run as a
  fixed non-root user with a read-only root and all capabilities dropped.
- Keep execution, quality, and safety independent. Neither provider output nor
  an LLM judge can certify isolation.
- Use strict schemas, canonical JSON, SHA-256 digests, no-replace durable
  writes, bounded outputs, complete cleanup, and fail-closed parsing.
- Add no third-party Python package. Use injected runners and synthetic
  upstreams in tests.
- The initial Codex read-only workload is shell-free and exposes only
  host-owned bounded `list`, `read`, and `search` tools. Adapter incompatibility
  blocks the route instead of enabling a general shell.

## Review Focus

- **Docker API drift or socket substitution:** the host must bind the real
  client, daemon, context, endpoint, platform, and effective create spec;
  covered by Task 2 identity and hostile-context tests.
- **Credential recovery or gateway bypass:** the workload must be unable to
  retrieve, infer, or directly use a real provider credential; covered by Task
  4 wrong-scope, direct-egress, header, and log-redaction tests.
- **Mount and namespace escape:** symlinks, propagation, host namespaces,
  privileged mode, extra mounts, and socket mounts must block before create;
  covered by Task 5 launch-spec mutation tests.
- **Incomplete process/network evidence:** missing, duplicate, out-of-window,
  or cross-container events must never yield safety `PASS`; covered by Task 7
  observer completeness tests.
- **Interrupted cleanup:** timeout, Ctrl-C, daemon restart, or partial removal
  must produce `INCOMPLETE` and preserve recovery evidence; covered by Task 7
  cleanup/recovery tests.

---

### Task 1: Docker-Only Contracts and Policy Gate

**Files:**
- Create: `skills/evaluate-skill/runner/docker_contracts.py`
- Create: `skills/evaluate-skill/runner/test_docker_contracts.py`
- Modify: `skills/evaluate-skill/runner/execution_policy.py`
- Modify: `skills/evaluate-skill/runner/test_execution_policy.py`
- Modify: `skills/evaluate-skill/runner/contracts.py`
- Modify: `skills/evaluate-skill/runner/test_contracts.py`

**Interfaces:**
- Consumes: existing `RunPlan`, `ApprovalReceipt`, and `EnforcementReceipt`.
- Produces: `DockerExecutionBinding.from_dict(...)`,
  `DockerGatewayBinding.from_dict(...)`, `DockerEvidenceBinding.from_dict(...)`,
  `DockerContractError`, and
  `assess_docker_run(plan, approval, enforcement, execution_binding, inventory,
  *, at, observed_versions, observed_platform) -> PolicyDecision`.

- [ ] **Step 1: Write failing strict-schema tests**

Add tests named:

```python
test_docker_execution_binding_requires_every_security_digest
test_docker_binding_rejects_unknown_fields_mutable_tags_and_non_sha256_values
test_gateway_binding_requires_provider_model_role_budget_expiry_and_single_use_nonce
test_evidence_binding_requires_exact_launch_gateway_observer_state_and_cleanup_digests
test_docker_policy_rejects_native_backend_without_fallback
test_docker_policy_blocks_unverified_inventory_or_mismatched_binding
test_historical_native_receipts_remain_parseable_but_not_live_dispatchable
```

Require image, build-input, runtime-inventory, launch-policy, network-policy,
seccomp-policy, gateway-policy, observer-policy, fixture, and cleanup-policy
digests. Require image references of the form `name@sha256:<64 lowercase hex>`.

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_docker_contracts.py \
  skills/evaluate-skill/runner/test_contracts.py \
  skills/evaluate-skill/runner/test_execution_policy.py -v
```

Expected: FAIL because Docker v0.4 bindings and the Docker-only policy do not
exist.

- [ ] **Step 3: Implement frozen strict bindings**

Implement canonical payload/digest methods with exact-field validation and
immutable mappings/tuples. Preserve the old contract reader for historical
artifacts; do not reinterpret an old native receipt as Docker evidence.

- [ ] **Step 4: Implement the active Docker-only assessment**

`assess_docker_run(...)` must require `plan.backend == "docker"`, exact
binding/receipt agreement, verified Docker capability claims, current
approval/receipt/grant windows, and all required evidence digests. It returns
only `APPROVED/docker` or `BLOCKED/None`; it never changes the backend.

- [ ] **Step 5: Run focused and existing contract tests**

Run the command from Step 2 and:

```bash
python3 -m unittest skills/evaluate-skill/runner/test_acceptance_v0_2.py -v
```

Expected: PASS; historical acceptance behavior remains readable and every new
live path is Docker-only.

- [ ] **Step 6: Commit Task 1**

```bash
git add skills/evaluate-skill/runner/docker_contracts.py \
  skills/evaluate-skill/runner/test_docker_contracts.py \
  skills/evaluate-skill/runner/contracts.py \
  skills/evaluate-skill/runner/test_contracts.py \
  skills/evaluate-skill/runner/execution_policy.py \
  skills/evaluate-skill/runner/test_execution_policy.py
git commit -m "feat(evaluate-skill): require docker execution bindings"
```

### Task 2: Docker Runtime and Image Provenance Inventory

**Files:**
- Create: `skills/evaluate-skill/runner/docker_runtime.py`
- Create: `skills/evaluate-skill/runner/test_docker_runtime.py`
- Modify: `skills/evaluate-skill/runner/provider_capabilities_v0_2.json`
- Modify: `skills/evaluate-skill/runner/capability_inventory.py`
- Modify: `skills/evaluate-skill/runner/test_capability_inventory.py`

**Interfaces:**
- Consumes: explicit absolute Docker CLI path, expected Docker context/endpoint,
  reviewed image lock, and injected command runner.
- Produces: frozen `DockerRuntimeIdentity`, `ImageLock`,
  `inspect_docker_runtime(...) -> DockerRuntimeIdentity`,
  `load_image_lock(path) -> ImageLock`, and `DockerRuntimeError`.

- [ ] **Step 1: Write failing runtime identity tests**

Add tests named:

```python
test_runtime_identity_binds_client_server_context_endpoint_platform_and_executable
test_runtime_refuses_missing_daemon_remote_tcp_symlink_context_or_platform_drift
test_image_lock_requires_digest_pinned_base_and_final_images
test_image_lock_binds_dockerfile_lockfiles_entrypoint_seccomp_and_inventory
test_image_inspect_digest_must_match_reviewed_lock
test_inventory_stays_unsupported_until_real_probe_evidence_is_accepted
```

Use an injected command runner; never contact a real daemon in unit tests.

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_docker_runtime.py \
  skills/evaluate-skill/runner/test_capability_inventory.py -v
```

Expected: FAIL because Docker runtime identity and image locks do not exist.

- [ ] **Step 3: Implement strict runtime inspection**

Run only explicit argv through the injected runner. Reject missing client or
daemon versions, non-local/unknown endpoints, context drift, server platform
drift, executable identity changes, or malformed JSON. Never start Docker.

- [ ] **Step 4: Implement image-lock validation**

The lock schema records provider/profile, base/final image digests, target
architecture, and SHA-256 for Dockerfile, provider lockfiles, entrypoint,
seccomp profile, and executable inventory. Reject placeholder or mutable tags.

- [ ] **Step 5: Keep capability claims fail-closed**

Add the v0.4 Docker probe requirements to the inventory schema, but leave
Docker claims `unsupported` until Task 9 records accepted real no-model probe
evidence. Unit tests may build synthetic inventories; the committed production
inventory must not claim verification early.

- [ ] **Step 6: Run focused tests and commit**

Run the Step 2 command, then:

```bash
git add skills/evaluate-skill/runner/docker_runtime.py \
  skills/evaluate-skill/runner/test_docker_runtime.py \
  skills/evaluate-skill/runner/capability_inventory.py \
  skills/evaluate-skill/runner/test_capability_inventory.py \
  skills/evaluate-skill/runner/provider_capabilities_v0_2.json
git commit -m "feat(evaluate-skill): bind docker runtime provenance"
```

### Task 3: Minimal Codex Read-Only Image Contract

**Files:**
- Create: `skills/evaluate-skill/runner/docker/codex-read-only.Dockerfile`
- Create: `skills/evaluate-skill/runner/docker/codex-entrypoint.py`
- Create: `skills/evaluate-skill/runner/docker/codex-runtime-lock.json`
- Create: `skills/evaluate-skill/runner/docker/seccomp-codex-read-only.json`
- Create: `skills/evaluate-skill/runner/docker/executable-inventory-codex.json`
- Create: `skills/evaluate-skill/runner/test_docker_image_contract.py`

**Interfaces:**
- Consumes: reviewed digest-pinned base image and pinned Codex, Promptfoo,
  Codex SDK, Node, and Python artifacts supplied at build time.
- Produces: one immutable Codex read-only workload image contract and
  `validate_image_contract(root, lock) -> None`.

- [ ] **Step 1: Write failing static image-contract tests**

Add tests named:

```python
test_dockerfile_requires_digest_base_nonroot_user_and_fixed_entrypoint
test_dockerfile_contains_no_runtime_package_install_or_remote_fetch
test_image_contract_contains_only_approved_runtime_broker_and_executables
test_initial_image_contains_no_shell_interpreter_or_arbitrary_command_tool
test_entrypoint_rejects_shell_interpolation_unknown_actions_and_missing_binding
test_seccomp_contract_denies_privilege_mount_namespace_ptrace_and_kernel_routes
test_image_lock_digest_changes_for_every_build_input
```

Tests inspect files only; they do not build an image.

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python3 -m unittest skills/evaluate-skill/runner/test_docker_image_contract.py -v
```

Expected: FAIL because the image contract does not exist.

- [ ] **Step 3: Implement the build-only image definition**

Use multi-stage `COPY` from reviewed build inputs; no `curl`, `npm install`,
`pip install`, package manager, or unpinned remote source in the Dockerfile.
Set fixed UID/GID, workdir, entrypoint, and labels. The entrypoint accepts only
`probe` and `evaluate` subcommands with strict JSON binding files. The evaluated
tool surface contains only bounded `list`, `read`, and `search` operations.

- [ ] **Step 4: Implement the reviewed runtime inventory and seccomp policy**

List every executable path and digest expected in the final image. Deny
privileged kernel operations while retaining only syscalls proven necessary by
the pinned provider runtime. Do not claim the policy works until Task 9.

- [ ] **Step 5: Run static tests and commit**

Run the Step 2 command, then:

```bash
git add skills/evaluate-skill/runner/docker \
  skills/evaluate-skill/runner/test_docker_image_contract.py
git commit -m "feat(evaluate-skill): define minimal codex workload image"
```

### Task 4: Provider-Auth Gateway and Run Grants

**Files:**
- Create: `skills/evaluate-skill/runner/provider_gateway.py`
- Create: `skills/evaluate-skill/runner/test_provider_gateway.py`
- Create: `skills/evaluate-skill/runner/docker/gateway-entrypoint.py`
- Create: `skills/evaluate-skill/runner/docker/gateway.Dockerfile`

**Interfaces:**
- Consumes: `DockerGatewayBinding`, host-held provider credential, host-held
  HMAC key, and injected synthetic upstream transport.
- Produces: `RunGrant.issue(...)`, `GatewayDecision`, `GatewayAuditEvent`,
  `authorize_gateway_request(...)`, `run_gateway(...)`, and `GatewayError`.

- [ ] **Step 1: Write failing grant and authorization tests**

Add tests named:

```python
test_grant_is_signed_single_use_expiring_and_plan_bound
test_gateway_sibling_allows_only_approved_provider_model_role_operation_and_budget
test_gateway_rejects_wrong_nonce_duplicate_session_expired_or_replayed_grant
test_gateway_never_returns_or_logs_real_credentials
test_gateway_rejects_arbitrary_proxy_connect_and_unapproved_destination
test_gateway_has_no_ip_forwarding_raw_socket_or_workload_chosen_destination
test_workload_internal_network_has_no_egress_dns_or_ipv6_bypass
test_gateway_redacts_prompt_secrets_and_emits_complete_decision_events
test_workload_environment_contains_only_run_grant_not_provider_credential
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python3 -m unittest skills/evaluate-skill/runner/test_provider_gateway.py -v
```

Expected: FAIL because gateway contracts do not exist.

- [ ] **Step 3: Implement signed run grants and fail-closed authorization**

Use HMAC-SHA256 with a host-held key file that is never mounted into the
workload. Bind the grant to plan, arm/judge role, provider, model, limits,
nonce, issued/expiry times, and one session identifier. Compare signatures in
constant time and persist replay state outside workload storage.

- [ ] **Step 4: Implement the synthetic gateway service**

Run as a trusted non-root sibling attached to the internal run network and a
separate egress network. Expose only the provider operation required by the
adapter. Validate before calling the injected upstream, add the real credential
only in trusted memory, strip it from the response, and emit bounded sanitized
audit events. Do not implement an open HTTP proxy or IP forwarding.

- [ ] **Step 5: Add adapter compatibility probes without inference**

Define `probe_codex_gateway_compatibility(adapter_config, synthetic_gateway)`.
It must prove the pinned adapter can target the gateway and authenticate with
only a run grant. It may use a synthetic upstream response but may not call
OpenAI. An unsupported configuration returns `BLOCKED_NOT_RUN`.

- [ ] **Step 6: Run tests and commit**

Run the Step 2 command, then:

```bash
git add skills/evaluate-skill/runner/provider_gateway.py \
  skills/evaluate-skill/runner/test_provider_gateway.py \
  skills/evaluate-skill/runner/docker/gateway-entrypoint.py \
  skills/evaluate-skill/runner/docker/gateway.Dockerfile
git commit -m "feat(evaluate-skill): add scoped provider gateway"
```

### Task 5: Exact Docker Launch Policy

**Files:**
- Create: `skills/evaluate-skill/runner/docker_policy.py`
- Create: `skills/evaluate-skill/runner/test_docker_policy.py`

**Interfaces:**
- Consumes: approved `RunPlan`, `DockerExecutionBinding`,
  `DockerRuntimeIdentity`, `ImageLock`, arm role, fixture, optional skill
  snapshot, and run grant.
- Produces: frozen `DockerRunTopology`, `DockerCommand`,
  `compile_docker_topology(...) -> DockerRunTopology`, and
  `DockerPolicyError`.

- [ ] **Step 1: Write failing launch-policy tests**

Add tests named:

```python
test_topology_uses_unique_internal_and_gateway_egress_networks
test_only_gateway_is_dual_homed_and_workloads_have_no_external_route
test_workload_is_readonly_nonroot_capdrop_all_no_new_privileges_and_seccomp_bound
test_only_exact_fixture_skill_binding_tmpfs_and_runtime_mounts_are_present
test_docker_socket_home_repo_auth_rubric_and_host_namespaces_are_absent
test_cpu_memory_pids_timeout_output_and_tmpfs_limits_match_plan
test_with_skill_and_without_skill_differ_only_by_approved_skill_mount
test_symlink_mount_propagation_privileged_host_network_extra_env_or_tag_blocks
test_commands_are_argv_without_shell_and_names_are_plan_bound
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python3 -m unittest skills/evaluate-skill/runner/test_docker_policy.py -v
```

Expected: FAIL because the compiler does not exist.

- [ ] **Step 3: Implement canonical topology and commands**

Generate exact create/start/inspect/stop/remove commands as argv arrays. Use a
new internal network and fresh labeled resources for every run. Reject paths
that are relative, symlinked, overlapping, broad, or outside the prepared
bundle and host artifact roots defined by the plan.

- [ ] **Step 4: Implement mutation-resistant policy verification**

Add `verify_effective_container(inspect_payload, topology, role) -> None` and
`verify_effective_network(inspect_payload, topology) -> None`. Re-read Docker
state after create and before start; block any daemon-side/default drift.

- [ ] **Step 5: Run tests and commit**

Run the Step 2 command, then:

```bash
git add skills/evaluate-skill/runner/docker_policy.py \
  skills/evaluate-skill/runner/test_docker_policy.py
git commit -m "feat(evaluate-skill): compile hardened docker topology"
```

### Task 6: No-Model Docker Boundary Probes

**Files:**
- Create: `skills/evaluate-skill/runner/docker_probes.py`
- Create: `skills/evaluate-skill/runner/test_docker_probes.py`
- Create: `skills/evaluate-skill/runner/docker/probe-entrypoint.py`

**Interfaces:**
- Consumes: exact `DockerRunTopology`, injected Docker runner, synthetic
  gateway, host canaries, and approved executable inventory.
- Produces: `DockerProbeResult`, `DockerPreflightResult`,
  `run_docker_preflight(...) -> DockerPreflightResult`, and
  `DockerProbeError`.

- [ ] **Step 1: Write failing probe tests**

Add tests named:

```python
test_preflight_requires_exact_complete_probe_set
test_probe_denies_host_home_repo_auth_rubric_socket_and_outside_mounts
test_probe_denies_root_and_fixture_writes_for_readonly_profile
test_probe_denies_direct_egress_host_metadata_and_unapproved_sidecars
test_probe_rejects_wrong_gateway_scope_and_credential_retrieval
test_probe_confirms_nonroot_caps_seccomp_namespaces_and_resource_limits
test_probe_confirms_shell_interpreters_forbidden_executables_absent_and_process_inventory_exact
test_probe_allows_only_bounded_list_read_and_search_tool_decisions
test_probe_verifies_container_volume_network_grant_and_state_cleanup
test_failed_unknown_timed_out_or_malformed_probe_is_blocked_not_run
```

All tests use fake Docker/gateway runners and immutable synthetic canaries.

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python3 -m unittest skills/evaluate-skill/runner/test_docker_probes.py -v
```

Expected: FAIL because the probe coordinator does not exist.

- [ ] **Step 3: Implement probe entrypoint and trusted assessment**

The untrusted container reports bounded observations; the host independently
checks mounts, config, networks, resource limits, image inventory, lifecycle,
and cleanup. A workload-reported `PASS` cannot override a host mismatch.

- [ ] **Step 4: Implement durable `READY_NOT_RUN` preflight**

Bind all probe results to the plan, runtime, images, topology, gateway policy,
fixture, and observer policy. Publish exact sanitized results with exclusive
creation and directory sync. Do not issue a live authorization or call a
provider.

- [ ] **Step 5: Run tests and commit**

Run the Step 2 command, then:

```bash
git add skills/evaluate-skill/runner/docker_probes.py \
  skills/evaluate-skill/runner/test_docker_probes.py \
  skills/evaluate-skill/runner/docker/probe-entrypoint.py
git commit -m "feat(evaluate-skill): add docker no-model probes"
```

### Task 7: Docker Supervisor, Observer, Evidence, and Cleanup

**Files:**
- Create: `skills/evaluate-skill/runner/docker_host.py`
- Create: `skills/evaluate-skill/runner/docker_observer.py`
- Create: `skills/evaluate-skill/runner/test_docker_host.py`
- Create: `skills/evaluate-skill/runner/test_docker_observer.py`
- Modify: `skills/evaluate-skill/runner/evidence.py`
- Modify: `skills/evaluate-skill/runner/test_evidence.py`
- Modify: `skills/evaluate-skill/runner/provider_trace.py`
- Modify: `skills/evaluate-skill/runner/test_provider_trace.py`

**Interfaces:**
- Consumes: successful `DockerPreflightResult`, fresh live authorization,
  exact topology, host signing key, Docker/gateway event sources, provider
  result, and protected/disposable snapshots.
- Produces: `DockerObserverAttestation`, `DockerSupervisedRun`, authenticated
  `EnforcementReceipt`, normalized paired evidence, and durable recovery state.

- [ ] **Step 1: Write failing supervision and observer tests**

Add tests named:

```python
test_supervisor_revalidates_every_digest_immediately_before_create_and_start
test_observer_binds_daemon_container_network_gateway_runtime_processes_and_provider_sessions
test_executable_identity_binds_image_path_file_argv_role_and_script_digests
test_missing_duplicate_cross_run_out_of_window_or_unapproved_event_fails_closed
test_provider_trace_commands_match_observed_container_and_gateway_events
test_supervisor_enforces_timeout_output_and_process_limits
test_timeout_interrupt_nonzero_exit_or_daemon_loss_is_incomplete
test_cleanup_always_revokes_grant_and_removes_containers_volumes_and_network
test_partial_cleanup_preserves_recovery_record_and_never_passes_safety
test_receipt_hmac_binds_key_id_epoch_launch_gateway_observer_state_and_cleanup
test_gateway_and_evidence_keys_are_distinct_external_and_never_mounted
test_crash_recovery_preserves_incomplete_journal_without_resigning
test_quality_cannot_override_failed_or_unknown_safety
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_docker_host.py \
  skills/evaluate-skill/runner/test_docker_observer.py \
  skills/evaluate-skill/runner/test_provider_trace.py \
  skills/evaluate-skill/runner/test_evidence.py -v
```

Expected: FAIL because Docker supervision and observation do not exist.

- [ ] **Step 3: Implement lifecycle ownership**

Create resources in the exact order gateway/network, workload create, inspect,
start, wait, collect, stop, remove, revoke, verify. Own every process and
container handle before waiting. In `finally`, attempt bounded cleanup of every
created resource and record each outcome.

- [ ] **Step 4: Implement independent event binding**

Bind Docker events and inspect state to the expected daemon, labels, IDs,
image, network, arm, timestamps, entrypoint, process inventory, and result.
Bind gateway decisions to the same run/arm/session and provider result digest.
Reject provider-only or workload-authored identity claims.

- [ ] **Step 5: Implement authenticated evidence publication**

Authenticate the receipt/evidence manifest using HMAC-SHA256 with an
operator-provisioned 32-byte key, key ID, and rotation epoch outside all repo,
Docker, and run storage. Keep it distinct from the gateway grant key. Publish
with exclusive creation, file sync, atomic same-filesystem rename, and
directory sync. A crash preserves an unsigned/incomplete journal; it never
re-signs or overwrites a closed artifact. Interruption recovery stays
`INCOMPLETE` until an operator verifies and finishes cleanup.

- [ ] **Step 6: Run focused and regression tests, then commit**

Run the Step 2 command and the complete runner suite, then:

```bash
git add skills/evaluate-skill/runner/docker_host.py \
  skills/evaluate-skill/runner/docker_observer.py \
  skills/evaluate-skill/runner/test_docker_host.py \
  skills/evaluate-skill/runner/test_docker_observer.py \
  skills/evaluate-skill/runner/evidence.py \
  skills/evaluate-skill/runner/test_evidence.py \
  skills/evaluate-skill/runner/provider_trace.py \
  skills/evaluate-skill/runner/test_provider_trace.py
git commit -m "feat(evaluate-skill): supervise docker evaluation boundary"
```

### Task 8: Docker-Only CLI and Workflow Integration

**Files:**
- Create: `skills/evaluate-skill/runner/eval_runner.py`
- Create: `skills/evaluate-skill/runner/test_eval_runner.py`
- Modify: `skills/evaluate-skill/runner/native_eval.py`
- Modify: `skills/evaluate-skill/runner/trusted_host.py`
- Modify: `skills/evaluate-skill/runner/test_native_eval.py`
- Modify: `skills/evaluate-skill/runner/test_trusted_host_cli.py`
- Modify: `skills/evaluate-skill/SKILL.md`
- Modify: `skills/evaluate-skill/README.md`
- Modify: `skills/evaluate-skill/references/execution-safety-gate.md`
- Modify: `skills/evaluate-skill/references/eval-runner-integration.md`
- Modify: `skills/evaluate-skill/runner/README.md`
- Modify: `skills/evaluate-skill/runner/proof/README.md`
- Modify: `skills/evaluate-skill/runner/proof/status_v0_2.json`

**Interfaces:**
- Consumes: explicit paths to plan, approval, prepared bundle, inventory,
  image lock, Docker runtime, gateway key/config, host signing key, artifacts,
  protected roots, and live authorization.
- Produces: `inspect`, `prepare`, `configure`, `docker-preflight`, and
  `docker-run` commands with stable JSON statuses.

- [ ] **Step 1: Write failing CLI migration tests**

Add tests named:

```python
test_active_cli_exposes_docker_preflight_and_run_only
test_native_live_commands_are_retired_and_return_blocked_not_run
test_prepare_and_configure_remain_provider_specific_without_model_calls
test_docker_preflight_requires_every_explicit_path_key_policy_and_digest
test_docker_run_requires_fresh_matching_preflight_and_live_authorization
test_cli_never_installs_starts_pulls_builds_or_falls_back_implicitly
test_status_and_docs_report_docker_design_pending_until_real_probes_pass
```

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
python3 -m unittest \
  skills/evaluate-skill/runner/test_eval_runner.py \
  skills/evaluate-skill/runner/test_native_eval.py \
  skills/evaluate-skill/runner/test_trusted_host_cli.py -v
```

Expected: FAIL because the active Docker-only CLI does not exist.

- [ ] **Step 3: Implement the active CLI and retire native dispatch**

Move shared offline preparation/configuration behind `eval_runner.py`. Keep
legacy entry points only as explicit deprecation/blocking wrappers; they may
read historical artifacts but cannot launch a provider. Require all
security-relevant inputs explicitly and return nonzero stable blocked statuses.

- [ ] **Step 4: Update workflow documentation**

Make v0.4 and its single canonical boundary map the active documentation.
Mark v0.2/v0.3 as superseded for live execution. Explain Docker installation,
image build, preflight, live authorization, artifacts, cleanup, and failure
states without claiming that Docker is already installed or verified.

- [ ] **Step 5: Run repository verification and commit**

Run:

```bash
python3 -m unittest discover -s skills/evaluate-skill/runner -p 'test_*.py' -v
python3 scripts/validate_skill_repository_integrity.py
python3 scripts/validate_evals.py --all
env TMPDIR=/private/tmp python3 -m unittest \
  scripts.test_validate_evals adapters.claude.test_adapter adapters.openai.test_adapter
git diff --check
```

Then commit the CLI and documentation integration.

### Task 9: Approved Docker Provisioning and Real No-Model Proof

**Files:**
- Modify after observed evidence: `skills/evaluate-skill/runner/docker/codex-runtime-lock.json`
- Modify after observed evidence: `skills/evaluate-skill/runner/provider_capabilities_v0_2.json`
- Create after observed evidence: `skills/evaluate-skill/runner/proof/docker-preflight-v0_4.json`
- Modify: `skills/evaluate-skill/runner/proof/status_v0_2.json`

**Interfaces:**
- Consumes: separately approved Docker installation/runtime, reviewed base
  image download, image build, synthetic canaries, and no provider credential.
- Produces: exact runtime/image lock, sanitized real probe artifact, and either
  `READY_NOT_RUN` or `BLOCKED_NOT_RUN`.

- [ ] **Step 1: Stop for provisioning approval**

Present the Docker product/version/source, expected downloads and disk use,
base image digest, build inputs, commands, network use, and artifact paths.
Do not install, pull, build, or start anything without approval.

- [ ] **Step 2: Inspect and pin the installed runtime**

After approval, record the exact local client/daemon/context/endpoint/platform
identity. If Docker is unavailable or differs from the approved source, stop
without modifying capability claims.

- [ ] **Step 3: Pull/build only approved digest inputs**

Verify every downloaded digest before use, build the images without secrets,
inspect the final filesystem/config/inventory, and update the lock only with
observed immutable digests. No model or provider credential is used.

- [ ] **Step 4: Run the real no-model negative probes**

Execute Task 6 against the exact images/topology with synthetic gateway
responses. Preserve sanitized evidence. Any failed, unknown, unavailable, or
incomplete probe produces `BLOCKED_NOT_RUN`.

- [ ] **Step 5: Review before capability promotion**

Request a fresh security review of image contents, topology, gateway, observer,
probes, and artifacts. Promote only the exact Codex/read-only/Docker claims
supported by accepted evidence; keep every other provider/profile unsupported.

- [ ] **Step 6: Commit evidence-supported provisioning metadata**

Commit only immutable locks, sanitized probe evidence, status, and capability
updates supported by the accepted run. Never commit credentials, daemon
configuration, raw prompts, or private host paths.

### Task 10: Separately Approved Synthetic Live Acceptance

**Files:**
- Create per approved run outside source fixtures: a unique proof artifact directory
- Modify only after accepted evidence: `skills/evaluate-skill/runner/proof/status_v0_2.json`
- Modify only after accepted evidence: provider capability inventory entries

**Interfaces:**
- Consumes: accepted real no-model proof, exact synthetic case, provider/model,
  disclosure, retention, limits, cost, live authorization, and human approval.
- Produces: paired provider-native results, Docker/gateway/observer evidence,
  independent execution/quality/safety outcomes, and a release decision.

- [ ] **Step 1: Stop for live-run approval**

Present the exact synthetic prompt/fixture, skill/rubric revisions, provider,
model snapshot, arms, maximum turns/time/output/cost, disclosed data, gateway
scope, artifact paths, retention, and cleanup plan.

- [ ] **Step 2: Revalidate and consume single-use authorization**

Re-attest every Docker, image, plan, gateway, observer, fixture, and policy
digest at the dispatch boundary. Consume the nonce outside rollbackable run
storage before the first provider request.

- [ ] **Step 3: Run both arms through Docker only**

Launch no host-native evaluated process. Keep arms independent, preserve their
native provider results, and always complete cleanup/revocation.

- [ ] **Step 4: Review evidence and decide release**

Require both arms execution `COMPLETED`, safety `PASS`, complete cleanup, and
independent evidence before advancing. Grade quality separately. A failed or
unknown safety result remains blocked regardless of quality.

- [ ] **Step 5: Commit only the accepted release record**

Update status/capability claims only after human acceptance. Preserve rejected
or incomplete evidence without promoting support.

## Final Verification and Self-Review

- **Spec coverage:** Tasks 1–2 bind the Docker-only control plane; Tasks 3–6
  define and probe the image, gateway, topology, and physical boundary; Task 7
  owns observation/evidence/cleanup; Task 8 integrates the workflow; Tasks
  9–10 separate real provisioning and live provider authorization.
- **Step scan:** Every code task has strict failing tests, one implementation
  boundary, verification, and a commit. Real Docker and provider operations
  remain explicit approval gates rather than ordinary implementation steps.
- **Type consistency:** `DockerExecutionBinding` flows from Task 1 through
  runtime inspection, topology, probes, supervisor, CLI, and evidence.
  `DockerGatewayBinding` and `RunGrant` flow only through the trusted gateway;
  the workload never handles a provider credential.
- **Review focus:** Docker identity, credential isolation, mount/namespace
  escape, event completeness, and interrupted cleanup each have named hostile
  tests in their owning task.
- **Proportion:** The ten tasks are independently reviewable acceptance
  boundaries for one Docker-only feature, not separate product phases requiring
  repeated approval. Only installation/download/build, real container
  execution, and live provider inference require scoped human authorization.
