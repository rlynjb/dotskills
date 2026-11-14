# Evaluate Skill

**Evaluate Skill** is a guided, evidence-based workflow for testing and improving an existing Agent Skill (or prompt). It has **12 stages (0–11)** across four phases. It is not a skill creator.

**Evaluation stack:** [Promptfoo](https://www.promptfoo.dev/) (now part of OpenAI) + the **OpenAI Codex SDK**. Evaluate Skill coordinates the process through [`SKILL.md`](SKILL.md) and [`runner/eval_runner.py`](runner/eval_runner.py). Promptfoo runs approved cases using `openai:codex-sdk` and grades outputs with `llm-rubric`. See the [runner guide](runner/README.md) for execution details.

## 1. Four building blocks of an eval

Example: **Audit Skill evaluates REAZN's source**. We are testing *Audit Skill's* behavior—not running or grading REAZN.

| Part | What it does | In DotSkills |
| --- | --- | --- |
| **1. Skill under evaluation** | The behavior we want to test. | [Audit Skill](../audit-skill/SKILL.md) |
| **2. Test input** | A fixed task, source files, and pre-agreed expectations. | A case from [Audit Skill's `evals/evals.json`](../audit-skill/evals/evals.json), using a frozen copy of [REAZN](../reazn/SKILL.md) as input. Keep grading answers separate from the tested agent. |
| **3. Evaluation harness** | Supplies inputs, executes the test in a controlled environment, and records outputs and tool attempts. | [Evaluate Skill](SKILL.md), [`eval_runner.py`](runner/eval_runner.py), Promptfoo + Codex SDK, and the [Docker-only execution controls](runner/README.md). |
| **4. Grader** | Checks observed behavior against the approved criteria. | Promptfoo `llm-rubric` with `openai:codex-sdk` as **LLM-as-a-judge**; human review checks evidence and safety-relevant traces. |

**Trust boundary:** REAZN's files are *test data*, not instructions for Audit Skill to execute. A grader's written judgment is not proof of tool or permission enforcement.

## 2. The 12 stages

| Phase | Stage | What happens |
| --- | --- | --- |
| **Prepare** | **0 · Validate** | Check the target skill's `SKILL.md` format. |
| | **1 · Define success** | Choose the behavior to test and what counts as success or failure. |
| | **2 · Design cases** | Draft test inputs, expected outcomes, and grading assertions; **get approval**. |
| **Evaluate** | **3 · Run baseline** | With separate approval and verified isolation, run comparable cases **with and without the skill**; preserve outputs and traces. |
| | **4 · Review grades** | Review the actual results and Promptfoo grades; check the evidence rather than blindly accepting a score. |
| **Improve** | **5 · Diagnose** | Identify whether problems come from the skill, case, grader, context, permissions, or environment. |
| | **6 · Review five lenses** | Check the five methodology lenses below for additional risks or gaps. |
| | **7 · Propose** | Recommend the smallest evidence-supported change; **get edit approval**. |
| | **8 · Apply** | Make only the approved changes and preserve the diff. |
| **Verify** | **9 · Rerun** | With fresh run approval and isolation, rerun approved cases and relevant regression checks. |
| | **10 · Compare** | Compare before/after results, including anything that previously passed. |
| | **11 · Decide** | A human chooses to keep, revise, revert, release, or iterate. |

**Remember:** Preparing cases is not running an eval. Stages 3 and 9 run tests; Stages 4 and 10 review existing results. Promptfoo may grade during execution—Stage 4 does **not** automatically launch a second grader.

## 3. Five conference-informed methodology lenses

Used in **Stage 6** to review a skill from different engineering perspectives. These are DotSkills review practices, not mandatory Agent Skills format requirements.

| Lens | What to look for |
| --- | --- |
| [**Context Engineering**](../context-engineering/SKILL.md) | Missing, stale, conflicting, or untrusted context |
| [**Correctness & Verification**](../correctness-and-verification/SKILL.md) | Supported claims, invariants, and reliable checks |
| [**Observability & Feedback**](../agent-observability-and-feedback/SKILL.md) | Outputs, tool attempts, traces, and useful feedback |
| [**Trust & Governance**](../agent-trust-and-governance/SKILL.md) | Permissions, trust boundaries, and unintended side effects |
| [**Skill Lifecycle & Release**](../skill-lifecycle-and-release/SKILL.md) | Versioning, regressions, and release readiness |

**More detail:** [Workflow](references/workflow.md) · [Eval case design](references/eval-design-guide.md) · [Runner and safety controls](runner/README.md) · [Approval gates](references/approval-gates.md)
