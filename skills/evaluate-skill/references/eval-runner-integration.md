# Evaluate Skill — native evaluation integration (experimental)

This guide explains how Stages 3–4 and 9–10 use the coding harness's **own
evaluation workflow**, with no cross-provider substitution. See
[the runner guide](../runner/README.md) and
[`native_eval.py`](../runner/native_eval.py) for the available dispatcher
and command interface.

## Select the provider before preparing or executing

| If Evaluate Skill runs in... | Test execution | LLM-as-judge | Result ownership |
| --- | --- | --- | --- |
| **Claude Code** | Claude `plugin eval` with `--ablation with-without` | Claude evaluation grader files (`type: llm`) | Claude evaluation reports/artifacts |
| **Codex** | Promptfoo with OpenAI's `openai:codex-sdk` provider, paired workspaces | Promptfoo `llm-rubric` with `openai:codex-sdk` as judge | Promptfoo result artifacts |

Promptfoo is [now part of OpenAI](https://www.promptfoo.dev/about/), but it
remains a separate, open-source, multi-provider evaluation framework. In the
Codex route, the **Promptfoo CLI explicitly invokes the Codex SDK** to run
cases and obtain LLM-rubric grading judgments. Ownership does not mean the
Codex SDK automatically invokes Promptfoo or provides a built-in evaluation
service. Likewise, the Claude route invokes Claude's plugin evaluation
interface, not the standalone description-trigger test.

The dispatcher detects `CLAUDECODE` or `CODEX_THREAD_ID` /
`CODEX_SESSION_ID`. The active host must independently verify its identity;
environment variables alone are not a security boundary. Conflicting or
unknown execution context blocks; a binary's presence is not sufficient.
Offline preparation permits an explicit harness argument only when no marker
is available. **Never run Codex to substitute for Claude or vice versa.**

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
4. Prepare the correct native case using `native_eval.py prepare`; check the
   generated files and native tool flags against the **installed versions**.
5. When all gates are independently verified, invoke `native_eval.py run`
   **inside the approved host**. Preserve the provider's raw results and the
   host's audit traces. Do not infer results from a prepared config file.
6. If a requirement fails, stop **Stage 3 — Blocked / Not Run** and preserve
   the case, approvals, and any observed errors. Never use a different provider
   as a fallback.

## Stage 4: grade using the selected provider only

- **Claude:** Use the native plugin eval's `graders/*.md` evaluation files
  with `type: llm`. Preserve Claude's result schema and native evidence.
- **Codex:** Use the Promptfoo `llm-rubric` assertions, each configured with
  `openai:codex-sdk` as the grading provider. Preserve Promptfoo's native
  output schema and evidence; no Anthropic grading instructions are injected.
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

## What is implemented and what remains unverified

`native_eval.py` prepares provider-specific case definitions, selects a
harness without runtime fallback, checks declared run prerequisites, and
dispatches the corresponding CLI command. It does not bundle or install
Claude, Promptfoo, or the Codex SDK, and it does not provide an independently
isolated execution host. The CLI flags, provider case formats and real grader
behavior must be tested against reviewed, pinned installations.

Offline tests exist in [`test_native_eval.py`](../runner/test_native_eval.py).
No end-to-end live model evaluation has been demonstrated here. Until a
separate host and run evidence are verified, the correct status is
**experimental integration — model evaluation Not Run**.

The Evaluate Skill's twelve stages, guided teaching, methodology lenses,
fixture preservation and human approval gates remain unchanged.
