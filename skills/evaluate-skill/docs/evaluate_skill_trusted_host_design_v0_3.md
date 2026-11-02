# Evaluate Skill Trusted Host Design v0.3

**Status:** Approved direction, implementation pending.

**Scope:** A fail-closed, Codex-first trusted host for the native `read-only`
evaluation profile on the pinned macOS platform. It is the prerequisite for a
live `with-skill` / `without-skill` Learn Repo evaluation. Claude, writable
profiles, live connectors, MCP servers, and Docker remain blocked until they
receive equivalent enforcement and evidence.

## 1. Intent

Evaluate Skill already validates immutable run plans, approvals, capability
inventories, enforcement receipts, provider results, evidence bundles, and
review transitions. What it does not yet own is the trusted process that makes
the enforcement receipt true.

The v0.3 trusted host fills that gap for one narrow route:

- provider: OpenAI through `openai:codex-sdk`;
- adapter: Promptfoo `0.125.1` with Codex CLI `0.163.0`;
- platform: Darwin `25.4.0`, arm64;
- backend/profile: native macOS, read-only;
- fixtures: synthetic, disposable, and already approved;
- effects: no workspace writes, outside reads, outbound tool network, MCP,
  connectors, nested agents, or external side effects.

The host does not grade quality and does not treat an LLM judgment as safety
evidence. Promptfoo and the Codex SDK continue to execute and grade the paired
case. The host independently constrains command execution, captures the run,
checks state, and supplies the evidence needed by Evaluate Skill.

## 2. Binding security facts

The implementation relies on two facts that are both configured and tested:

1. Codex uses macOS Seatbelt for spawned commands. The official Codex
   [sandbox documentation](https://developers.openai.com/codex/sandboxing)
   distinguishes the sandbox boundary from approval policy and states that
   spawned tools inherit that boundary.
2. Current Codex permission profiles can deny the filesystem root, allow only
   the minimal runtime plus the active workspace, and disable command network.
   The official [permission profile documentation](https://learn.chatgpt.com/codex/permissions)
   provides the workspace-only/root-deny pattern used here.

Those facts are not accepted from configuration alone. Before a receipt is
issued, the exact compiled profile must pass the repository-owned negative
probes through the installed `codex sandbox` binary.

## 3. Trust boundaries

| Component | Trusted for | Not trusted for |
| --- | --- | --- |
| Coordinator | Approved plan, case, budgets, and human approval | Physical enforcement |
| Trusted host | Policy compilation, version/auth checks, probes, process supervision, state snapshots, trace normalization, cleanup, and receipt publication | Quality grading |
| Promptfoo/Codex harness | Provider call, paired execution, provider-native output, LLM-rubric grading | Safety certification |
| Evaluated agent and skill | Producing an answer inside the approved workspace | Any enforcement or evidence claim |
| Evaluate Skill evidence audit | Binding identities and deciding execution/safety completeness | Inferring missing evidence |

The pinned Codex CLI, SDK, and Promptfoo adapter are part of the native route's
trusted computing base for one narrow fact: every agent-controlled command and
tool operation they expose must be routed through Codex's command sandbox. The
host does not trust them to *report* that this happened; it pins their exact
versions, injects and re-reads the effective policy, runs OS-enforced negative
probes, rejects unapproved tool-item types, and verifies post-run state. A
harness that can bypass Seatbelt is therefore version drift or a failed native
capability, not something this layer tries to contain. Removing that routing
trust would require putting the complete harness and its auth boundary inside
a separately isolated VM/container and belongs to the conditional fallback,
not this native-first implementation.

The Codex harness remains outside the evaluated command sandbox so it can use
the user's existing file-based ChatGPT authentication. Spawned agent commands
run under the narrower custom permission profile and cannot read the auth file
or any other path outside the disposable workspace. API-key environment
authentication is refused for this route because those values could enter a
child environment; `OPENAI_API_KEY` and `CODEX_API_KEY` must be unset.

## 4. Native read-only policy

The host compiles one canonical permission profile named
`evaluate-skill-read-only`:

- `:root = "deny"`;
- `:minimal = "read"`;
- the exact arm workspace root is `read`;
- the pinned Command Line Tools runtime is `read` for immutable Python probes;
- network is disabled;
- no writable root is granted;
- host skill discovery is disabled;
- every configured MCP server is explicitly disabled;
- web search, apps/connectors, collaboration/nested agents, and thread reuse
  are disabled;
- Promptfoo process-environment inheritance, cache, sharing, telemetry,
  updates, and remote generation are disabled.

The plan records restricted shell use as enabled because Codex reads fixture
files through sandboxed commands. Shell availability is not unrestricted
authority: the same root-deny, no-write, and no-network policy applies to every
spawned command. Secondary routes capable of starting another agent or host
automation process are explicitly denied and probed.

The compiled profile is injected into every with-skill, without-skill, and
judge Codex provider configuration through `cli_config`. Legacy
`sandbox_mode` fields are removed so they cannot override the named permission
profile. The exact resulting Promptfoo file is part of the provider-config
digest already bound by `native_eval.py`.

## 5. Host lifecycle

### 5.1 Preflight — no model call

1. Load the configured bundle, run plan, approval receipt, and pinned
   capability inventory.
2. Confirm exact platform and installed versions.
3. Require file-based ChatGPT login, unset API-key variables, disabled
   connectors/MCP, a real non-symlink workspace, and protected roots outside
   that workspace.
4. Compile the canonical Codex permission profile and confirm it exactly
   matches the configured provider file.
5. Run all immutable negative probes through `codex sandbox` with a scrubbed
   environment: secret absence, network denial, outside read denial, inside
   and outside write denial, and secondary-route denial.
6. Snapshot protected and disposable roots without following symlinks.
7. Issue a short-lived `EnforcementReceipt` only when every probe passes and
   bind it to the plan, provider config, prepared bundle, workspace, run nonce,
   tools, state method, and cleanup method.

Any unknown result is `BLOCKED_NOT_RUN`. The preflight never calls a model.

### 5.2 Supervised execution — live and separately authorized

1. Revalidate the plan, approval, receipt, inventory, bundle digest, and
   single-use nonce.
2. Capture a host-owned `run_start` event before provider dispatch.
3. Execute only the exact Promptfoo command already bound by the manifest,
   with a minimal environment and hard timeout/output limits.
4. Parse the Promptfoo `0.125.1` JSON schema fail-closed. Preserve provider
   output and LLM-rubric judgments, while extracting each Codex response's raw
   turn items into sanitized host trace events.
5. Reject missing arms, unexpected providers, MCP/web/collaboration items,
   malformed command items, absent session identity, cache hits, or model and
   adapter drift. Add provider identity only after the trusted parser verifies
   the pinned configuration and observed Codex session metadata.
6. Snapshot state again, compare protected/disposable roots, and record the
   provider-result digest.
7. Remove the disposable agent workspaces, verify cleanup, close the trace,
   and publish evidence with no-replace durable writes.
8. Leave execution, quality, and safety as separate statuses for human review.

Provider output without a complete host audit remains incomplete. A failed or
interrupted arm cannot make the pair complete.

## 6. Evidence and receipts

Host artifacts live outside the evaluated workspaces and contain no auth
material. They include:

- canonical host-policy JSON and digest;
- preflight probe results;
- before/after state snapshots and diffs;
- sanitized trace events derived from supervised process and provider turn
  items;
- stdout/stderr digests rather than unrestricted raw logs;
- per-arm provider result and source-result digests;
- cleanup result;
- enforcement receipt and final `EvidenceBundle` payloads.

Receipt issuance and evidence publication use exclusive creation, file sync,
and directory sync. Existing artifacts are never overwritten. Secret-like
values are redacted before persistence.

## 7. Failure behavior

The host blocks before a model call when any of these are true:

- platform or installed version drift;
- API-key environment authentication is present or ChatGPT file login is
  unavailable;
- provider configuration does not contain the exact compiled policy;
- any MCP, connector, web, collaboration, or host-skill surface is enabled;
- a probe fails, is unknown, times out, or cannot execute immutably;
- the approval, nonce, plan, bundle, or provider-config digest differs;
- protected roots overlap the disposable workspace;
- snapshot, receipt, or durable-publication guarantees are unavailable.

After dispatch, malformed output, identity ambiguity, a cache hit, trace
truncation, protected-state change, cleanup failure, timeout, or nonzero exit is
an infrastructure error or safety failure—not a partial pass.

## 8. Non-goals

- No general-purpose sandbox service.
- No claim that Promptfoo itself supplies isolation.
- No live Claude route in this change.
- No writable or mock-external profile in this change.
- No Docker implementation unless this exact native route exposes a verified
  gap that cannot be closed safely.
- No automatic live model call during implementation or tests.
- No capability-inventory promotion to `verified` until an explicitly approved
  live paired proof completes with preserved evidence.

## 9. Acceptance

The implementation is ready for a scoped live proof only when:

1. all existing offline suites remain green;
2. new tests prove deterministic policy compilation, strict Promptfoo config,
   environment/auth refusal, preflight receipt binding, trace parsing, state
   comparison, cleanup, and fail-closed execution;
3. the real installed `codex sandbox` passes all six negative probes without a
   model call;
4. repository docs continue to report live provider proof as not run;
5. a fresh code review finds no Critical or Important issue.

The subsequent live Learn Repo evaluation still requires presentation and
approval of the exact case, model snapshot, maximum turns, duration, output,
cost, disclosure, retention, and evidence paths.
