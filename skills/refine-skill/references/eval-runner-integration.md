# Refine Skill — Claude/Codex evaluation integration (experimental)

**Integration status: dual-harness adapter implemented; live model evaluations NOT RUN.**
The skill-local [runner](../runner/README.md) implements experimental paired
CLI execution, model-based assertion grading, and a provisional comparison for
**both** Claude Code and Codex. Neither provider's complete Skill Creator or
evaluation framework is installed by this adapter. No verified isolated host or
end-to-end Claude/Codex model test is available yet. Keep adapter files under
`skills/refine-skill/`; run only in a separately approved, independently
verified execution host.

## Harness selection: what is actually implemented

The selected CLI `--harness claude` or `--harness codex` chooses **both**
the evaluated-agent runtime and its LLM judge. The runner currently defaults
to `claude` if no harness is given; callers should pass `--harness`
explicitly. Merely invoking Refine Skill within Codex does **not**
automatically prove the runner will select Codex.

| Selected harness | Paired execution | LLM-as-judge | Integration limit |
| --- | --- | --- | --- |
| **Claude** | `claude -p` using restricted CLI options and separate workspaces | Claude model prompted with a locally reviewed, SHA-256-pinned copy of Anthropic Skill Creator's `agents/grader.md` | **Not** Anthropic's complete Skill Creator subagent execution/benchmark/viewer installation |
| **Codex (OpenAI)** | `codex exec --json --sandbox read-only` using separate workspaces | Codex model asked to grade assertions; `--output-schema` constrains the response JSON | **Not** OpenAI's separate official evaluation runner or Plugin Eval engine; this is a custom Codex CLI adapter |
| **Both** | With-skill and without-skill, same case and fixture | Evidence-based assertion checks + human review | Python `compare` calculates assertion pass-rate differences; no blind comparator agent or review viewer |

The provider-specific CLI commands and grading prompt live in
[`runner/runner.py`](../runner/runner.py). OpenAI documents
[`codex exec --json` and `--output-schema`](https://learn.chatgpt.com/docs/non-interactive-mode);
these are Codex CLI capabilities, **not** a dedicated OpenAI skill-evaluation
runner or prepackaged LLM grader.

## Anthropic Skill Creator reference components (not all installed)

Source: [Anthropic Skill Creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md).
Inspect the installed/version-pinned upstream files before invoking them:

| Component | Official location | Use in Refine Skill |
| --- | --- | --- |
| **Behavioral execution** | `SKILL.md` — “Running and evaluating test cases” | The *coordinating Claude host* launches independent with-skill and without-skill (or pinned old-skill) **subagents**. There is no standalone general-purpose behavioral `run_eval.py` command. |
| **LLM grader** | [`agents/grader.md`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/agents/grader.md) | Evidence-based assertion grading from actual transcripts and output artifacts. It is an agent instruction, not a separately installed model or a security sandbox. |
| **Blind comparator** | [`agents/comparator.md`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/agents/comparator.md) | Optional unbiased A/B assessment when both outputs exist. |
| **Analyzer** | [`agents/analyzer.md`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/agents/analyzer.md) | Explain observed differences; avoid overfitting. |
| **Benchmark aggregation** | `scripts/aggregate_benchmark.py` | Summarize actual, comparable assertion grades and metrics. |
| **Human review** | `eval-viewer/generate_review.py` | Show outputs and benchmark when the approved upstream tool is available. |
| **Description trigger test** | `scripts/run_eval.py` | **Different test:** checks whether a skill description gets triggered. It is **not** Stage 3's behavioral runner and must not be used as proof of behavioral quality. |

The upstream Skill Creator is licensed separately (Apache-2.0 for the
skill-creator package); retain its license and review dependencies before
installing or copying code. Prefer referencing the installed, reviewed,
version-pinned upstream component rather than silently vendoring scripts.

## Stage 3 — execution handshake (mandatory)

1. Confirm the exact approved target-skill revision, eval case, expected
   behavior, fixture revision, model/harness, and with-skill/baseline pairing.
   The existing case/fixture is reused; do **not** regenerate it.
2. Determine whether the host actually supports independently isolated
   behavioral subagents (or an equivalent evaluated-agent runner).
   **A mere `SKILL.md`, Claude CLI installation, trigger-test script,
   successful fixture validation, or Grader prompt is not proof of this.**
3. Require an independent host to enforce the
   [Execution Safety Gate](execution-safety-gate.md): isolated disposable
   workspace, mock-only per-call tool dispatch, no production credentials,
   no unrestricted shells or network/tool routes, evaluator-only material
   hidden, trusted attempt trace and post-run state verification. **Prompt
   instructions are not a sandbox.**
4. Require scoped case/run approval for this execution, plus any separate
   organizational approval to send source code to an external model provider.
   At work, deny by default when that approval/provider boundary is unknown.
5. If and only if the host enforcement is verified, run the same neutral
   prompt and approved synthetic fixture in separate clean contexts:
   `with_skill` and `without_skill` (or `old_skill`). Keep answer keys
   and grading criteria outside *both* evaluated-agent contexts. Record the
   immutable skill/case versions, runner/model version, inputs, final outputs,
   complete tool-attempt traces, trusted result state and available timing/
   token metrics in unique, non-overwriting iteration/run directories.
6. If any prerequisite is missing, stop **at Stage 3 — Blocked / Not Run**.
   Name the missing capability and preserve approved cases. Do **not**
   proceed to Stage 4–11 as though the eval ran.

**Runtime availability:** Claude Code and Codex have different execution
interfaces. Anthropic Skill Creator subagent instructions do not magically
become a cross-harness executable. A verified provider/host adapter is
required for each supported harness. Do not run `claude -p`, arbitrary
shell commands, external network tools, or unreviewed third-party scripts
as an unsafe fallback.

## Stage 4 — grading (after verified behavioral outputs exist)

- Apply deterministic checks first where they establish meaningful behavior.
- For **Claude**, the experimental runner passes reviewed, SHA-256-pinned
  Anthropic `agents/grader.md` instructions to a separate Claude CLI grader
  invocation; it does **not** start the original Skill Creator grader subagent.
  For **Codex**, the runner prompts the Codex model directly and requests
  structured JSON via `--output-schema`; this is our own grader integration,
  not OpenAI's separate evaluation framework.
- Provide only approved evaluator-side expectations and actual outputs.
  Neither path may send unchecked secrets or proprietary data to an
  unapproved provider.
- Record each testable assertion as `text`, `passed` and `evidence`.
  Preserve the same versioned rubric for both comparison arms. Record
  Unknown/unverifiable items separately; never make them fabricated Pass.
- Use host-generated action/state evidence for safety checks. A grader
  reading a final answer alone cannot certify absence of unauthorized
  attempted writes. Human review is always available; LLM-as-judge is
  optional, not a substitute for the host safety gate.
- Do not treat a high average score as overriding any failed required
  safety or correctness criterion.

## Stage 10 — comparative analysis and human review

- The current cross-harness adapter's `compare` action calculates both
  arms' assertion pass rates and their percentage-point difference. It
  does **not** run an LLM blind comparator or aggregate multiple trials.
- Anthropic's `agents/comparator.md`, `scripts/aggregate_benchmark.py`,
  and `eval-viewer/generate_review.py` are **upstream optional references**,
  not integrated stages. A separate reviewed integration could use them
  with actual, compatible evidence; never imply they already ran.
- OpenAI's separate [Plugin Eval tooling](https://github.com/openai/plugins/tree/main/plugins/plugin-eval)
  is **not installed or invoked** by this adapter. Connecting such a tool
  would require a distinct compatibility and security review.
- Distinguish missing metrics from zeros, and do not invent variance from
  one trial. Human feedback and release decisions remain human-gated.

## What remains before we can claim integration is complete

- Review and pin the Anthropic grader instructions on an approved Claude
  host, and verify Codex CLI execution and structured grading separately.
  The narrow adapter exists but is still experimental.
- Establish and independently verify a safe host with an actual
  behavioral-agent execution interface, mock tools, per-call authorization,
  trusted action traces and state checks.
- Run a synthetic paired evaluation end-to-end for **both harnesses**;
  prove evaluator-only information stays hidden, no live writes are reachable,
  and execution and grader outputs follow the expected schema. Do not claim
  a comparator-agent test: that feature is not implemented.
- Re-run the committed tests and validate blocked/missing-run behavior.
  Until these checks succeed, report **adapter experimental; behavioral
  eval Not Run**.

This preserves Refine Skill's 12 stages, four-phase navigation, learning
format, source provenance labels, opt-in Reset Eval and per-gate approvals.
