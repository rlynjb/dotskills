# Evaluate Skill — provider evaluation integration (experimental)

> **Active execution decision:** OpenAI Codex case and result formats are
> retained, but the [Docker-only v0.4 architecture](../docs/evaluate_skill_execution_architecture_v0_4.md)
> requires every live evaluated arm to run inside the verified Docker boundary.
> Native provider sandboxes are not execution backends or fallbacks. The code
> is implemented and offline tested; until real Docker provisioning and all
> no-model probes are accepted, status is `DOCKER_DESIGN_PENDING` and live
> execution is **Blocked — Not Run**.

This guide explains how Stages 3–4 and 9–10 use **Promptfoo with the
OpenAI Codex SDK**, without fallback to another provider. See
[the runner guide](../runner/README.md) and
[`eval_runner.py`](../runner/eval_runner.py) for the command interface.

## Supported evaluation path

| Environment | Test execution | LLM-as-judge | Result format |
| --- | --- | --- | --- |
| **OpenAI Codex** | Promptfoo with `openai:codex-sdk` in paired workspaces | Promptfoo `llm-rubric` with `openai:codex-sdk` as judge | Promptfoo result artifacts |

Promptfoo is [now part of OpenAI](https://www.promptfoo.dev/about/), but
its CLI explicitly invokes the Codex SDK; the SDK does not automatically run
Promptfoo. The preparer recognizes Codex session markers
(`CODEX_THREAD_ID` / `CODEX_SESSION_ID`) or an explicit `codex` selection
for offline preparation. Unsupported sessions/providers are rejected.
Session markers are not trusted proof of runtime isolation.

## Stage 2: approved inputs

Prepare a versioned target skill and synthetic evaluation case. Record its
prompt, expected behavior, fixture references, and approved grading
`assertions`. The native preparer requires nonempty assertions at preparation
time. Keep the actual evaluated-agent input separate from the grader's
expectations; check each provider's real execution and grading isolation.
Preserve the approved source case and fixture files unmodified.

## Stage 3: execute only after host verification

1. Confirm the selected harness and that its exact native evaluation tool is
   installed, trusted and compatible. Do not silently install dependencies.
2. Obtain scoped human approval for this run, plus authorization to send data
   to the selected provider. At work, proprietary material is prohibited by
   default unless the organization approves the precise disclosure.
3. Verify a **separate host-enforced** execution boundary: disposable
   workspaces, mock-only per-tool authorization, no live secrets or external
   writes, no shell/API/network/child-agent bypasses, evaluator-only material
   isolated, and trusted attempted-action/state auditing. A manifest, an LLM
   prompt, or a built-in sandbox option is **not proof**.
4. Prepare the correct provider case using `eval_runner.py prepare`; check the
   generated files and native tool flags against the **installed versions**.
5. Construct and approve the versioned run plan. Run `eval_runner.py configure`
   to materialize its exact model snapshot, limits, and staged revision pins.
   The independent host then verifies those executable settings and issues an
   enforcement receipt binding both configuration and bundle digests.
6. Require the matching approval receipt, enforcement receipt, and pinned
   capability inventory. Run
   `native_eval.py assess` first. A plan, receipt, version, capability, probe,
   tool-route, state-check, or cleanup mismatch is **Blocked — Not Run**.
7. Inspect the generated artifacts, then run `native_eval.py bind` to bind the
   prepared bundle's artifact digest and resource limits to the exact approved
   plan. A changed or reused bundle is **Blocked — Not Run**.
8. Require `eval_runner.py docker-preflight`: exact runtime/image provenance,
   shell-free tool surface, internal workload network, provider gateway,
   negative probes, observer, state method, and cleanup policy. The command and
   enforcement code exist, but real provisioning/probes are not yet accepted,
   so current status is `DOCKER_DESIGN_PENDING` and execution stops as
   **Blocked — Not Run**.
   Do not substitute the historical `trusted_host.py` native preflight.
9. After a real preflight is accepted, live dispatch additionally requires a fresh
   `APPROVED_LIVE_RUN` object bound to the complete Docker preflight, a protected
   consumed-nonce ledger, and the approved Docker supervisor/gateway/observer.
   Preserve provider-native output, normalized per-arm results, quality data,
   gateway and tool decisions, container evidence, state, and cleanup. Never
   infer identity from expected config or the provider's own claim alone.
10. Finalize both arms against the manifest execution ID, receipt nonce, and raw
   source-result digest with separate provider and host-evidence outcomes. Apply
   `next_stage_decision` and persist an append-only `write_stage_checkpoint`
   record bound to the plan digest. Stage 4 is available only when both arms
   completed and aggregate safety is `PASS`.
11. If a requirement fails, stop **Stage 3 — Blocked / Not Run** and preserve
   the case, approvals, and any observed errors. Never use a different provider
   as a fallback.

## Stage 4: grade using the selected provider only

- Use Promptfoo `llm-rubric` assertions with `openai:codex-sdk` as
  the grading provider. Preserve native Promptfoo results and independently
  observed evidence.
- Independently review factual/safety criteria against trusted action traces
  and resulting state. An LLM grade of response text cannot certify that no
  unauthorized tool call was attempted. Missing or unreliable evidence must
  be labeled Unknown, never silently passed.
- Do not invent a single universal output schema, numerical cutoff, or
  average across incompatible provider reports.

## Stages 9–10: rerun and compare

Rerun the same approved case and rubric within the **same provider** in fresh,
comparable contexts. Use the provider's own output and reporting tools to
compare revisions, plus human review of regressions and attempted actions.
Do not claim provider-native blind comparison or cross-platform metric
normalization unless the selected tool has actually produced that evidence.
Final skill changes remain subject to the existing human approval gates.
Stage 9 uses a new scoped approval, enforcement receipt and checkpoint; it
cannot advance to Stage 10 after blocked/incomplete/infrastructure-error
execution or failed/unknown safety.

## What is implemented and what remains unverified

Docker-only v0.4 is the approved live architecture and its offline
implementation is present. Docker provisioning has not been approved through
this workflow, no reviewed image has been resolved or probed, and no provider
route is verified. Status is therefore `DOCKER_DESIGN_PENDING` / **Blocked —
Not Run** with no native fallback.

The v0.3 implementation adds the native Codex read-only trusted host: exact
policy compilation; isolated file-login/API-key refusal; pinned Node, Codex,
and Promptfoo executables; sealed Promptfoo and Codex SDK runtime trees; six
immutable local probes; single-use supervision; strict Promptfoo/Codex parsing;
one versioned, fresh, process-bound observer attestation covering arm and judge
sessions; dispatch-time authorization checks; bounded process output,
protected/disposable snapshots, no-follow cleanup, append-only recovery states,
and durable paired evidence. Legacy boolean authorization and self-declared
host manifests remain insufficient. It does not bundle or install provider
tools, supply credentials, or support live writable, mock-external,
connector, MCP, or Docker routes.

The acceptance suite is
[`test_acceptance_v0_2.py`](../runner/test_acceptance_v0_2.py). No end-to-end
live model evaluation has been demonstrated. The 2026-11-02 native run passed
five probes and failed the inert secondary-process route. That implementation
is retained as historical evidence and regression coverage, not as an active
execution option.

The Evaluate Skill's twelve stages, guided teaching, methodology lenses,
fixture preservation and human approval gates remain unchanged.
