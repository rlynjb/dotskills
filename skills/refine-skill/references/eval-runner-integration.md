# Refine Skill — Anthropic Skill Creator evaluation adapter

**Integration status: documented / NOT RUN.** This reference connects the
existing Refine Skill stages to Anthropic's Skill Creator workflow. It does
**not** install Anthropic's components, spawn an agent, configure isolation, or
verify an end-to-end evaluation. Do not describe it as a working runner merely
because this reference exists. Keep all integration files under
`skills/refine-skill/`; use an external, approved execution host.

## Upstream components and their actual responsibilities

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
- Optionally use an independently configured Anthropic Grader subagent
  following `agents/grader.md`, giving it only the necessary evaluator-side
  expected assertions, trusted transcripts and outputs, **not** unchecked
  secrets or proprietary data sent to an unapproved provider.
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

- When actual paired outputs and comparable grades exist, optionally
  invoke Anthropic's `agents/comparator.md` with blinded A/B content.
  Hide which arm is which from the comparator; store the mapping separately
  for the evaluator. A blind preference is supplementary, not a safety pass.
- If a reviewed upstream Skill Creator installation and trusted outputs
  are available, use `scripts/aggregate_benchmark.py` and
  `eval-viewer/generate_review.py` with their documented input schemas.
  These tools summarize/review completed runs; they do not execute the
  behavioral task or enforce sandboxing.
- Distinguish missing metrics from zeros, and do not invent variance from
  one trial. Human feedback and release decisions remain human-gated.

## What remains before we can claim integration is complete

- Install/review a pinned version of Skill Creator on the intended
  host or implement and test a narrow equivalent adapter.
- Establish and independently verify a safe host with an actual
  behavioral-agent execution interface, mock tools, per-call authorization,
  trusted action traces and state checks.
- Run a synthetic paired evaluation end-to-end; prove evaluator-only
  information stays hidden, no live writes are reachable, outputs are
  captured, and the Grader/Comparator outputs follow the expected schema.
- Validate blocked/missing-run behavior and regression tests. Until these
  checks succeed, report **integration planned; behavioral eval Not Run**.

This preserves Refine Skill's 12 stages, four-phase navigation, learning
format, source provenance labels, opt-in Reset Eval and per-gate approvals.
