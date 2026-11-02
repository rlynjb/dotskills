# Evaluate Skill — provider-specific evaluation workflows (experimental)

[`native_eval.py`](native_eval.py) prepares and digest-binds provider-specific
synthetic cases. [`trusted_host.py`](trusted_host.py) is the separate native
Codex enforcement entry point. It compiles the deny-by-default profile, runs
the six local probes, issues bound preflight artifacts, and supervises the
single-use paired command. Neither entry point provides cross-provider fallback.

Before dispatch, the runner now loads a versioned run plan, scoped human
approval receipt, independent enforcement receipt, and pinned capability
inventory. `assess` validates those inputs and the installed provider/tool
versions without running a model. `bind` records the exact approved plan,
resource limits, and staged-artifact digest. `run` uses the same fail-closed
assessment and accepts only that fresh, bound bundle before executable
discovery or provider dispatch.

| Active harness | Execution | Grading | Native result format |
| --- | --- | --- | --- |
| Claude Code | Claude's `claude plugin eval`, with-skill and without-skill via `--ablation with-without` | Claude plugin-eval `graders/*.md` using `type: llm` | Claude plugin-eval JSON / review artifacts |
| Codex | Promptfoo with the `openai:codex-sdk` provider in separate with-skill and without-skill workspaces | Promptfoo `llm-rubric` assertions configured to use the same Codex SDK provider | Promptfoo JSON results |

**Ownership and integration are distinct:** `claude plugin eval` is Claude
tooling. [Promptfoo is now part of OpenAI](https://www.promptfoo.dev/about/)
and remains an [open-source, multi-provider framework](https://www.promptfoo.dev/blog/promptfoo-joining-openai/).
Evaluate Skill explicitly invokes the Promptfoo CLI for the Codex route;
Promptfoo uses the `openai:codex-sdk` provider for execution and LLM-rubric
grading. This is not a grading service automatically bundled into the Codex
SDK. No Anthropic grader prompt is passed to Codex, and no Codex rubric is
substituted for Claude's native graders. Do not describe these paths as
identical implementations.

## Harness selection: no substitution

- `native_eval.py inspect` checks for a Claude session via `CLAUDECODE`,
  or a Codex session via `CODEX_THREAD_ID` / `CODEX_SESSION_ID`.
- Preparation selects the detected harness. `--harness` is permitted only
  for **offline preparation** when detection is unavailable; conflicting
  session markers and mismatches are blocked.
- Execution requires an identifiable active session matching the prepared
  case. The presence of a CLI binary alone is **not** harness identification.
- If the native tool, credentials, approval, or independent isolation are
  missing, report **Blocked — Not Run**. Never switch providers.

These environment markers are a convenience, not a trusted attestation of
the actual caller. The separately enforced host must verify provider identity
and routing before running a model.

## Prepare synthetic cases — no model calls

Run these commands from the DotSkills repository root with a saved, approved
case. The case in `evals/evals.json` must have an `id`, `prompt`,
`expected_output`, and nonempty `assertions`. Existing input fixtures
(`files`) must be synthetic and approved. The case and source files remain
unchanged; each preparation gets its own output directory.

```bash
python3 skills/evaluate-skill/runner/native_eval.py inspect

python3 skills/evaluate-skill/runner/native_eval.py prepare \
  --suite skills/example-skill/evals/evals.json \
  --case-id 1 \
  --target-skill skills/example-skill \
  --output eval-workspaces
```

`inspect` will fail if a known harness is not exposed in the environment.
For **offline-only** fixture preparation, `prepare` also accepts
`--harness claude` or `--harness codex`, but a live evaluation must still
prove the actual current harness. The example paths are placeholders.

The preparer writes a manifest with `PREPARED_NOT_RUN` status and one of:

- Claude: `plugin/.claude-plugin/plugin.json`, `plugin/skills/<skill>/`,
  `plugin/evals/<case>/prompt.md`, and `graders/criterion-*.md`.
- Codex: `codex/promptfooconfig.yaml`, separate `with_skill/` and
  `without_skill/` workspaces, and `llm-rubric` assertions with the
  `openai:codex-sdk` grader provider.

**Important:** Static fixture generation and model/tool instructions do not
establish that the provider accepted the case or that isolation works.

## Configure the approved provider settings — no model calls

After approving a `RunPlan` whose case, rubric, skill, and fixture revision
pins match the prepared manifest, materialize the executable provider settings:

```bash
python3 skills/evaluate-skill/runner/native_eval.py configure \
  --bundle /isolated/eval-workspaces/PREPARED-BUNDLE \
  --run-plan /trusted/run-plan.json
```

This changes the manifest to `CONFIGURED_NOT_BOUND`, writes an exact
`execution-config.json`, selects the approved model snapshot in the actual
Claude command or Promptfoo provider configs, applies the approved turn/cost
settings to those configs, and records provider-config and staged-bundle
digests. The independent host verifier must inspect this exact configuration
before issuing its enforcement receipt. A staged revision mismatch blocks
configuration; manifest claims alone are not trusted.

## Assess a pinned run — no model calls

```bash
python3 skills/evaluate-skill/runner/native_eval.py assess \
  --run-plan /trusted/run-plan.json \
  --approval-receipt /trusted/approval-receipt.json \
  --enforcement-receipt /trusted/enforcement-receipt.json \
  --capability-inventory skills/evaluate-skill/runner/provider_capabilities_v0_2.json
```

The plan digest binds case, revisions, provider/model/adapter versions,
backend, capability surfaces, budgets, comparison arms, evidence, and cleanup.
The approval must match that exact plan. Approval and enforcement receipts
must have a shared run nonce and current, timezone-aware validity windows no
longer than two hours. The pinned inventory also requires an exact operating
system release and architecture fingerprint. The
enforcement receipt must match the plan, provider-configuration digest,
prepared-bundle digest, and independently identified runtime, tools, probes,
state check, and cleanup method. Unknown fields, version drift, missing probes, unverified
claims, and backend/provider substitution produce `BLOCKED_NOT_RUN`.

This is contract and policy validation, not physical enforcement. A caller
cannot make a run safe by authoring JSON that says its probes passed. Receipt
provenance and the controls it describes must be established outside the
evaluated workload.

## Bind the inspected bundle — no model calls

After `configure`, inspect the staged configuration and fixtures, obtain the
independent receipt for those exact digests, and run `assess`. Then bind that
exact bundle to the approved policy inputs:

```bash
python3 skills/evaluate-skill/runner/native_eval.py bind \
  --bundle /isolated/eval-workspaces/PREPARED-BUNDLE \
  --run-plan /trusted/run-plan.json \
  --approval-receipt /trusted/approval-receipt.json \
  --enforcement-receipt /trusted/enforcement-receipt.json \
  --capability-inventory skills/evaluate-skill/runner/provider_capabilities_v0_2.json
```

Binding changes the manifest from `CONFIGURED_NOT_BOUND` to `BOUND_NOT_RUN` and
records the plan digest, resource limits, and a digest of every staged input.
Changing a staged file after binding blocks execution. A bound bundle is
single-use; interrupted and completed attempts cannot be silently replayed.

## Live execution — approved host only

### Trusted Codex preflight — no model call

After `configure`, run the native boundary preflight with explicit absolute
paths. The full command requires `--run-plan`, `--approval-receipt`,
`--capability-inventory`, `--bundle`, `--artifact-directory`, `--codex-path`,
`--promptfoo-path`, `--node-path`, `--promptfoo-runtime-root`,
`--codex-sdk-root`, `--command-line-tools-root`, `--home`, at least one
`--protected-root`, `--provider-config`, `--issued-at`, `--expires-at`, and
`--verifier-version`:

```bash
python3 skills/evaluate-skill/runner/trusted_host.py preflight \
  --run-plan /trusted/run-plan.json \
  --approval-receipt /trusted/approval.json \
  --capability-inventory /trusted/provider-capabilities.json \
  --bundle /isolated/PREPARED-BUNDLE \
  --artifact-directory /trusted/RUN-ARTIFACTS \
  --codex-path /absolute/bin/codex \
  --promptfoo-path /sealed/promptfoo-runtime/dist/src/entrypoint.js \
  --node-path /absolute/bin/node \
  --promptfoo-runtime-root /sealed/promptfoo-runtime \
  --codex-sdk-root /sealed/promptfoo-runtime/node_modules/@openai/codex-sdk \
  --command-line-tools-root /Library/Developer/CommandLineTools \
  --home /trusted/codex-home \
  --protected-root /protected/source \
  --provider-config /trusted/native-boundary-config.json \
  --issued-at 2026-11-02T12:00:00Z \
  --expires-at 2026-11-02T12:30:00Z \
  --verifier-version 0.3.0
```

`READY_NOT_RUN` means only that the exact local policy, versions, login mode,
MCP inventory, bundle, snapshots, and six no-model probes were bound and
published. It does not authorize or start Promptfoo. The artifacts are
`host-policy.json`, `preflight-snapshots.json`, `preflight-probes.json`, and
`enforcement-receipt.json`, plus a digest printed for the complete set.

The Promptfoo runtime must be a nonempty, symlink-free sealed tree. The
Promptfoo entry point must be inside it, and the Codex SDK must be at the exact
Node resolution path shown above. Preflight binds and rechecks the Node, Codex,
and Promptfoo executable identities plus the complete Promptfoo and SDK tree
digests immediately before dispatch. It also rejects any competing
`node_modules/@openai/codex-sdk` found through Promptfoo's config-directory or
working-directory ancestor search, so an unbound package cannot shadow the
attested SDK. The isolated home may contain only
`.codex/auth.json`, with directory mode `0700` and file mode `0600`; ambient
Codex config, plugins, skills, or other files block the run.

After review, bind that receipt with `native_eval.py bind`. A live `run`
additionally requires a short-lived `APPROVED_LIVE_RUN` authorization bound to
the plan, nonce, receipt digest, complete preflight-artifact digest, and exact
trusted observer ID/version. Receipt and authorization expiry are rechecked at
the dispatch boundary. The
standalone CLI deliberately returns `BLOCKED_NOT_RUN` unless an approved host
embedding supplies the trusted process runner and independent Codex session
observer. Promptfoo's own result cannot self-attest that identity.

The trusted runner is a lifecycle launcher, not a one-shot callback. It must
return the Promptfoo process-group ID plus wait and terminate/reap operations
before the host waits for completion. The host invokes termination/reaping in
a `finally` block, binds the reported Promptfoo PID to that process group, and
rejects a runner that cannot provide this ownership contract.

The host observer must cover both arm sessions and every LLM-rubric judge
session. Each observation is bound to the current execution ID, process ID,
supervised Promptfoo parent process, Codex executable digest, timestamp,
raw observer-attestation digest, result index,
provider/model/adapter identity, and provider-config digest. Missing, replayed,
duplicate, or extra sessions block completion. Post-dispatch failures report
`INCOMPLETE` with `model_executed: true`; they are never rewritten as a
pre-dispatch `BLOCKED_NOT_RUN` result. The exact versioned observer JSON is
durably preserved rather than reconstructed from parallel caller claims.
Ctrl-C after dispatch terminates the supervised process group, cleans the
disposable workspaces, and follows the same incomplete path.

The injected observer is a trusted host authority, not evidence supplied by
Promptfoo or the evaluated model. This repository validates its approved
identity, schema, freshness, parent/child process binding, and complete arm and
judge set, but does not ship the production host integration that collects
those observations. Therefore the standalone live route remains blocked.

On 2026-11-02 the installed profile passed five of six probes. The inert
secondary-process canary was executable, so preflight correctly remained
blocked and no receipt-ready live route was accepted. This verified gap must
not be waived; it is the trigger for the separately approved conditional
Docker fallback.

The following accepts only a fresh `BOUND_NOT_RUN` bundle and is a command contract for a **separately provisioned, independently
verified isolated host**, not an instruction to run untrusted skills in an
ordinary shell:

```bash
python3 skills/evaluate-skill/runner/native_eval.py run \
  --bundle /isolated/eval-workspaces/PREPARED-BUNDLE \
  --nonce-ledger /trusted/consumed-run-nonces \
  --run-plan /trusted/run-plan.json \
  --approval-receipt /trusted/approval-receipt.json \
  --enforcement-receipt /trusted/enforcement-receipt.json \
  --capability-inventory /trusted/provider-capabilities.json
```

The legacy dispatcher invokes only the selected native command, but it does
not replace `trusted_host.py` supervision:

- Claude: `claude plugin eval <prepared-plugin> --ablation with-without
  --model <approved-snapshot> --no-publish --json <output>`
- Codex: `promptfoo eval --config <prepared-config> --no-cache --no-share
  --output <output>`

Review and pin the installed tool versions and their supported CLI flags.
Do not allow runtime package installation or unreviewed dependency execution.
The enforcement receipt must also contain successful host evidence for the
provider-authentication gateway and resource-limit enforcement. The dispatcher
applies the approved wall-clock timeout, rejects missing/invalid or oversized
provider output, and requires the result to carry an exact observed
provider/model/adapter identity matching the plan. The provider wrapper or
trusted parser must produce that identity attestation from the actual response;
absence or drift is an infrastructure error, never a safety or quality pass.

Before dispatch, the runner atomically consumes the receipt nonce in the
trusted `--nonce-ledger`, which must be an existing directory outside the
rollbackable prepared bundle. Deleting or rolling back bundle-local results,
claims, or the manifest cannot make the nonce reusable. The ledger must itself
be protected and append-only at the host boundary. The dispatcher then moves
the single-use manifest through `RUNNING` to either
`PENDING_HOST_AUDIT` or `INFRA_ERROR`. These checks do not replace host
confinement or prove that provider-native turn/cost controls work.

The safety requirement is **host-enforced**, not merely declared: disposable
workspaces, mock-only tool authorization, no live credentials/writes,
network and shell/API bypass prevention, child-agent restrictions, independent
attempted-action traces and post-run state checks. The manifest and
receipt files **cannot provide these controls themselves**.
Follow [Execution Safety Gate](../references/execution-safety-gate.md).
Work-related prompts, code and outputs may be sent to a provider **only**
with the appropriate employer/provider approval.

Provider-generated judgments are **not a safety pass**. Confirm that the
native outputs exist, review assertions and host traces, and make the human
keep/revise/revert decision within Evaluate Skill. Never invent grades or
comparison metrics.

After the provider result is parsed by the trusted host into both arms, the
supervisor records `HOST_AUDIT_COMPLETE` only after exact session identity,
protected state, cleanup, and durable per-arm evidence all pass.
`proof_pair_from_supervised` and `write_stage_checkpoint` revalidate every
arm's receipt nonce, execution ID, source-result digest, provider identity and
evidence digest. `next_stage_decision` then keeps execution, quality,
and safety independent. Stage 3/9 advances only when the exact pair completed
with safety `PASS`. `write_stage_checkpoint` records that decision with the
schema version, plan digest, run/receipt/execution IDs, provider-result and
evidence-bundle digests, full host evidence payloads, arm statuses and reasons;
it publishes through a durable no-replace operation and refuses
to overwrite an existing checkpoint so resumptions retain prior evidence. A
directory-sync failure rolls back the visible destination before reporting
failure; consumers must not infer success from a failed publication call.

## Offline tests and current limits

```bash
python3 -m unittest discover -s skills/evaluate-skill/runner -p 'test_*.py' -v
```

- Offline tests exercise contracts, inventory loading, compiled host policy,
  routing, case preparation, fixture security, immutable probes, host evidence,
  expanded-profile authorization/audit interfaces, transition gates,
  append-only recovery records, and refusal paths only.
- No real Claude or Codex evaluation has been verified end to end in this
  environment. The native Codex host implementation and no-model probes exist;
  a live independent session observer and approved paired proof are still absent.
- Native tool compatibility, ablation behavior, evaluator-only rubric
  isolation, actual grader responses, trace integrity, and result parsing
  still require approved-host validation. The preparer requires assertions
  before it can build native grader definitions.
- **Fixture paths are skill-root-relative**, matching
  `scripts/validate_evals.py`: a case stored in `<skill>/evals/evals.json`
  can reference `evals/files/example.txt`, resolved from `<skill>/`.
  The dispatcher stages the same approved path in Claude's `fixtures/`
  or in **both** Codex `inputs/` workspaces. It rejects missing files,
  absolute paths, parent traversal, symlinked files/directories, and
  suites outside the selected target skill **before** creating a bundle.
  It does not copy `evals.json` into either evaluated-agent workspace.
- **Offline fixture regression tests:** the dispatcher suite covers Claude,
  Codex, fixture-path isolation, policy assessment, legacy-flag rejection,
  and blocked execution. These tests do **not** verify live models,
  provider-native format compatibility, or actual host isolation.
- The prototype does not aggregate native results across providers into a
  single score. Keep provider output schemas separate. Compare revisions
  within each provider using actual supported reports and human review.
- The trusted host compiles a native read-only Codex profile, normalizes Codex
  turn items, snapshots state, cleans workspaces, and publishes no-replace
  evidence. It does not implement Claude, writable, mock-external, connector,
  MCP, or Docker execution, and it never supplies model credentials. The
  committed inventory remains unverified until a separately approved paired
  live proof completes with an independently observed session identity.
