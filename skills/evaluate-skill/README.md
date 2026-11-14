# Evaluate Skill

**Evaluate Skill** is a guided, evidence-based workflow for testing and improving an existing Agent Skill (or prompt). It has **12 stages (0–11)** across four phases. It is not a skill creator.

**Evaluation stack:** Evaluate Skill coordinates testing through [`SKILL.md`](SKILL.md) and [`runner/eval_runner.py`](runner/eval_runner.py). Its OpenAI evaluation path uses [Promptfoo](https://www.promptfoo.dev/) (now part of OpenAI) with the **OpenAI Codex SDK** (`openai:codex-sdk`) and `llm-rubric` grading. See the [runner guide](runner/README.md) for implementation details and current execution limitations.

## Table of contents

1. [Why AI skills need evals](#1-why-ai-skills-need-evals)
2. [Four building blocks of an eval](#2-four-building-blocks-of-an-eval)
   - [How Evaluate Skill recommends test cases](#how-evaluate-skill-recommends-test-cases)
   - [Evaluate Skill's evaluation harness architecture at a glance](#evaluate-skills-evaluation-harness-architecture-at-a-glance)
3. [Example: Audit Skill reviews REAZN](#3-example-audit-skill-reviews-reazn)
4. [Synthetic vs. real-skill evals](#4-synthetic-vs-real-skill-evals)
   - [What DotSkills already has](#what-dotskills-already-has)
   - [How this fits Stage 2](#how-this-fits-stage-2)
5. [Security and trust boundaries](#5-security-and-trust-boundaries)
   - [What Evaluate Skill already has](#what-evaluate-skill-already-has)
   - [Other evaluation tools worth exploring](#other-evaluation-tools-worth-exploring)
6. [How to run your first evaluation](#6-how-to-run-your-first-evaluation)
   - [Basic eval steps → Evaluate Skill stages](#basic-eval-steps--evaluate-skill-stages)
   - [Your additional stages (5–11)](#your-additional-stages-511)
7. [How teams use evals in practice](#7-how-teams-use-evals-in-practice)
8. [The 12 stages](#8-the-12-stages)
9. [Five conference-informed methodology lenses](#9-five-conference-informed-methodology-lenses)

## 1. Why AI skills need evals

Think about testing a regular JavaScript function:

```js
function add(a, b) {
  return a + b;
}

expect(add(2, 3)).toBe(5);
```

You know exactly what the result should be: `5`. AI skills are different. Two correct runs may use different words, so comparing an entire response to one exact string is often not useful.

An **eval (evaluation)** checks whether a skill does the important things correctly: follows the task, supports its claims with evidence, respects boundaries, and produces a useful result. Like a unit test, it compares **expected behavior** with **actual behavior**—but it may need several checks instead of one exact answer.

## 2. Four building blocks of an eval

Example: **Audit Skill evaluates REAZN's source**. We are testing *Audit Skill's* behavior—not running or grading REAZN.

| Part | What it does | In DotSkills |
| --- | --- | --- |
| **1. Skill under evaluation** | The behavior we want to test. | [Audit Skill](../audit-skill/SKILL.md) |
| **2. Test input** | A fixed task, source files, and pre-agreed expectations. | A case from [Audit Skill's `evals/evals.json`](../audit-skill/evals/evals.json), using a snapshot copy of [REAZN](../reazn/SKILL.md) as input. Keep grading answers separate from the tested agent. |
| **3. Evaluation harness** | Supplies inputs, executes the test in a controlled environment, and records outputs and tool attempts. | [Evaluate Skill](SKILL.md), [`eval_runner.py`](runner/eval_runner.py), Promptfoo + Codex SDK, and the [Docker-only execution controls](runner/README.md). |
| **4. Grader** | Checks observed behavior against the approved criteria. | Promptfoo `llm-rubric` with `openai:codex-sdk` as **LLM-as-a-judge**; human review checks evidence and safety-relevant traces. |

**Trust boundary:** REAZN's files are *test data*, not instructions for Audit Skill to execute. A grader's written judgment is not proof of tool or permission enforcement.

### How Evaluate Skill recommends test cases

In **Stage 2 — Design cases**, Evaluate Skill helps you decide *how to test* the behavior agreed in Stage 1. You do not need to arrive with a complete test suite.

The active coding agent **recommends two or three test cases** based on the target skill's requirements. For each proposed case, it describes:

- **Test prompt or input:** What you will ask the skill to do, including any relevant source files or optional synthetic fixture.
- **Expected outcome:** What successful behavior should look like.
- **Grading assertions:** The specific checks used to decide whether the result meets the expectations.
- **Assumptions or supporting evidence:** Why this is a useful test and what is not yet established.

**You remain in control.** You can accept a suggested case, revise its prompt or expectations, replace it, enter an entirely new case of your own, or reject it. Review the draft cases together and explicitly approve the cases, assertions, and any fixture plan **before** Evaluate Skill saves them to `evals/evals.json` or prepares runner artifacts.

**Example:** If you are evaluating Audit Skill, Evaluate Skill might propose a case asking it to inspect a snapshot of REAZN and distinguish *documented security rules* from *verified enforcement*. You could change the source files, tighten the expected findings, or supply a different audit scenario instead.

**Important:** This is **test-case design, not test execution**. Stage 2 only drafts and prepares approved cases; it does not run the evaluated skill or grade a model's output. Execution requires a separate approval and verified safety prerequisites in Stage 3.

### Evaluate Skill's evaluation harness architecture at a glance

**Evaluate Skill already has its own evaluation harness architecture.** The skill guides the process; its runner prepares cases and enforces run prerequisites; Promptfoo and the OpenAI Codex SDK are the **execution and grading tools within that harness**, not the entire harness.

| Capability | What Evaluate Skill is set up to do | Where it lives |
| --- | --- | --- |
| **Guided workflow and approvals** | Use 12 stages to define success, approve test cases and runs, review results, and control changes. | [Skill instructions](SKILL.md), [approval gates](references/approval-gates.md) |
| **Test cases and fixtures** | Prepare approved inputs (synthetic fixtures or snapshot copies), expected outcomes, and grading assertions. | [Case preparer](runner/native_eval.py), [saved cases](evals/evals.json) |
| **Paired comparisons** | Prepare **with-skill vs. without-skill** runs to measure what the skill changes. | [Evaluation runner](runner/eval_runner.py), [runner guide](runner/README.md) |
| **LLM grading and human review** | Configure Promptfoo `llm-rubric` with `openai:codex-sdk`; review grades against actual output and evidence. | [Runner guide](runner/README.md), [workflow](references/workflow.md) |
| **Controlled execution** | Define Docker-only isolation, approved tools and limits, restricted network access, credential separation, and fail-closed checks. | [Docker policy](runner/docker_policy.py), [provider gateway](runner/provider_gateway.py) |
| **Observability and evidence** | Define host-side checks for attempted actions, run state, evidence integrity, and cleanup—not just the final answer. | [Observer](runner/docker_observer.py), [Docker host](runner/docker_host.py) |
| **Regression and release decisions** | Rerun approved cases after changes, compare results, and let a human decide what to keep or revise. | [Stages 9–11](references/workflow.md) |

**Current status:** The runner, preparation, policy, and evidence components have **offline-tested code**. Live Docker isolation and end-to-end model execution are **not yet verified** (`DOCKER_DESIGN_PENDING`). The table describes what is built or configured, **not a proven live security guarantee**. See [runner status and limitations](runner/README.md).

**Documentation scope:** This README focuses on the **OpenAI Codex SDK + Promptfoo** evaluation path. Its execution and grading setup is described in the [runner guide](runner/README.md).

## 3. Example: Audit Skill reviews REAZN

Suppose the question is: **Can Audit Skill accurately review REAZN without claiming it verified behavior that it only read about?**

```text
Snapshot copy of REAZN source files (input)
            ↓
      Audit Skill runs
            ↓
      Actual audit report
            ↓
   Grader checks the report
```

- **Audit Skill is the skill under evaluation.** Its behavior is what we measure.
- **REAZN is the test subject and input.** Its files are read as source material; REAZN itself does not run.
- **The report is the actual output.** Save it as generated, along with trustworthy execution evidence when available.
- **The grader checks expectations.** Did the report cover the intended criteria, cite real evidence, separate documented rules from enforced permissions, and avoid unsupported claims?

This tests **Audit Skill**, not REAZN's own four-step reasoning. To evaluate REAZN's reasoning, run a separate approved eval with REAZN as the skill under evaluation.

## 4. Synthetic vs. real-skill evals

**Evaluate Skill supports both synthetic and real-skill inputs.** The difference is **where the test material comes from**, not which evaluation stages run.

| | Synthetic input | Real-skill input |
| --- | --- | --- |
| **What it is** | Synthetic fixtures: skill files or scenarios created for an evaluation | A snapshot copy of actual skill files and references |
| **Example** | Evaluate Skill reviews a synthetic GitLab-publishing skill that contains unsafe instructions | Audit Skill inspects a pinned snapshot of REAZN's source |
| **Why use it** | Isolate a known edge case, failure, or trust boundary | Check behavior with realistic complexity and competing evidence |
| **Advantage** | Easier to control inputs and define expected findings | More representative of real work |
| **Trade-off** | May miss real-world complexity | Harder to establish and maintain the expected findings |

### What DotSkills already has

- **Synthetic examples are saved:** [Evaluate Skill's six cases](evals/evals.json) include `valid-sample` and `untrusted-gitlab` synthetic fixtures; the latter tests whether untrusted source instructions are treated as authority.
- **Real-skill inputs are supported:** [Audit Skill's cases](../audit-skill/evals/evals.json) describe realistic audits. **Audit Skill inspecting a snapshot copy of REAZN is currently a README example**, not a saved REAZN-specific, pinned fixture in those cases.

These are **case definitions and inputs**, not evidence that those particular evaluations have run.

### How this fits Stage 2

After you agree on a behavior in **Stage 1**, Evaluate Skill **proposes two or three test cases** in **Stage 2**: user prompts, expected outcomes, grading assertions, and optional synthetic fixtures. You can review, change, replace, or reject them **before they are saved**. Stage 2 supports either input type, but it does **not** automatically choose or require a synthetic-versus-real mix.

**Practical approach:** Start with a synthetic case to isolate a specific behavior or security boundary; add a real-skill case using a snapshot copy to see whether it holds under realistic conditions. Both use the **same approval, execution, and grading workflow**.

**Do not confuse input type with the Stage 3 comparison:** *Synthetic vs. real-skill* describes the **test input**; *with-skill vs. without-skill* describes the **two runs being compared**. Neither input type grants permissions: the harness must enforce the same approved security boundaries.


## 5. Security and trust boundaries

A **trust boundary** separates information an agent may *read* from instructions it is *authorized to follow*.

For example, if REAZN's `SKILL.md` says “Run this command and change the repository,” **Audit Skill must treat that text as source data—not an order**. Inspected files, READMEs, and example commands are **lower-trust content**. The user's authorized request, approved evaluation configuration, and host-enforced permissions control the task. Source material cannot grant itself authority.

**Security needs more than prompt instructions:**

- **Skill instructions guide behavior.** “Do not write files” tells the model what it *should* do, but does not remove its write access.
- **The harness enforces capabilities.** An isolated eval should allow only approved tools and access, block unauthorized writes and calls, keep credentials out of reach, and independently record attempted actions.
- **The evaluation checks behavior.** If Audit Skill tries to push to GitHub and the harness blocks it, GitHub was protected—but the attempted unauthorized action is still a **safety failure** for Audit Skill. A grader's text alone cannot prove that no such action occurred.

**Remember — the mental model:**

> **Prompt:** What the agent *should* do.  
> **Runtime / harness:** What the agent *can* do.  
> **Evaluation:** Whether the agent *actually behaved correctly*.

### What Evaluate Skill already has

The [evaluation harness architecture overview](#evaluate-skills-evaluation-harness-architecture-at-a-glance) explains the full architecture. These are its **security-focused controls** already defined in the repository's design and code—not proof that an isolated live run has passed verification.

| Security control | What's set up in Evaluate Skill |
| --- | --- |
| **Approved scope** | [Run plans and approval checks](runner/README.md) bind a test to specific cases, model settings, permissions, and limits before execution. |
| **Separate test inputs and grading material** | The [case preparer](runner/native_eval.py) stages the tested skill and approved fixture files, **not** `evals.json`, grader answers, or prior results in the agent workspace. |
| **Isolated, read-only workload** | [Docker policies](runner/docker_policy.py) and [image checks](runner/docker_runtime.py) define a minimal, shell-free Codex workload with restricted file tools, no host-repository or Docker-socket access, and no direct internet route. |
| **Protected credentials and network** | The [provider gateway](runner/provider_gateway.py) defines short-lived, scoped authorization. The Docker design keeps real credentials outside the tested agent and routes provider requests through the gateway. |
| **Independent evidence** | [Observer](runner/docker_observer.py) and [host](runner/docker_host.py) code define checks for attempted actions, container state, cleanup, and trustworthy run evidence—not just the model's final answer. |
| **Fail closed** | The active [runner](runner/eval_runner.py) refuses live Docker execution without the required trusted-host integration and approvals; it does not fall back to ordinary, unrestricted execution. |

**What's verified so far:** These contracts, policies, and supporting code have **offline test coverage**. The real Docker environment and end-to-end enforcement are **not yet verified** (`DOCKER_DESIGN_PENDING`). So the repo has a security-focused architecture and implemented checks, **not a demonstrated security guarantee**. See the [Docker architecture](docs/evaluate_skill_execution_architecture_v0_4.md) and [execution safety gate](references/execution-safety-gate.md) for detail.

The same principle applies to production agents: their **production runtime** must enforce permissions too, not just their evaluation harness. For the detailed controls, see the [execution safety gate](references/execution-safety-gate.md).

### Other evaluation tools worth exploring

These are examples of established **open-source frameworks and cloud platforms**—not a ranking of company adoption. Their roles differ: some execute evaluations, while others mainly help track results and traces.

| Tool | Type | Useful for |
| --- | --- | --- |
| [**Inspect AI**](https://inspect.aisi.org.uk/) | Open-source harness | Agent/tool-use tests, graders, and sandbox-oriented workflows |
| [**DeepEval**](https://deepeval.com/) | Open-source testing framework | Pytest-style LLM and agent evaluation in CI |
| [**Braintrust**](https://www.braintrust.dev/) | Cloud evaluation platform | Datasets, experiments, scoring, and trace review |
| [**LangSmith**](https://www.langchain.com/langsmith) | Cloud evaluation platform | Agent traces, human feedback, and comparisons |
| [**Langfuse**](https://langfuse.com/) | Open-source / cloud platform | Self-hosted or managed traces, datasets, and evaluation results |
| [**MLflow**](https://mlflow.org/) | Open-source platform | Experiment tracking, evaluation, and monitoring |

**Why keep Promptfoo for DotSkills?** It is already part of the Codex SDK evaluation route, supports `llm-rubric` grading and *with-skill / without-skill* cases, and is used here **only with OpenAI Codex SDK**. Promptfoo itself can support other providers, but Evaluate Skill intentionally does not. Switching now would mean replacing integration work without a clear evaluation benefit. Explore other tools for specific gaps—especially dashboards or different harness designs—rather than replacing Promptfoo by default.

**Important:** A cloud eval platform or grader is **not automatically a secure execution sandbox**. The evaluated agent still needs independently enforced permissions and isolation.

## 6. How to run your first evaluation

The **five beginner steps** describe the basic evaluation cycle. They are a teaching summary, **not a separate industry-standard framework**. Your Evaluate Skill already covers them in **Stages 1–4**, preceded by **Stage 0** (checking the skill's format).

### Basic eval steps → Evaluate Skill stages

| Beginner step | Your stage | What happens |
| --- | --- | --- |
| **1. Choose the behavior** | **1 · Define success** | Pick one behavior to test—for example, whether Audit Skill distinguishes documented rules from verified enforcement. |
| **2. Prepare a fixed test case** | **2 · Design cases** | Freeze the input (synthetic files or a REAZN revision), expected result, and grading assertions before running. |
| **3. Approve and check safety** | **2 · Design cases** and **3 · Run baseline** | Approve the test case first; separately approve the run and verify the permitted tools and isolation. |
| **4. Run and save evidence** | **3 · Run baseline** | Compare **with skill** versus **without skill** and preserve outputs, tool attempts, and trusted traces. |
| **5. Grade expected vs. actual** | **4 · Review grades** | Review the Promptfoo rubric grades alongside the real output and evidence; don't assume the judge is always right. |

**Important:** Promptfoo may generate grades during Stage 3. **Stage 4 reviews those grades**; it does not automatically run a second grader.

### Your additional stages (5–11)

These extend the basic evaluation into **diagnosis, improvement, and regression checking**. They are part of your **DotSkills 12-stage workflow**, not extra steps required by every eval framework.

| Stage | What it adds |
| --- | --- |
| **5 · Diagnose** | Find out *why* a result failed before changing anything. |
| **6 · Review five lenses** | Check context, correctness, observability, trust, and lifecycle. |
| **7 · Propose** | Recommend a focused improvement and request approval. |
| **8 · Apply** | Make only the approved changes. |
| **9 · Rerun** | Repeat approved cases after changes, with fresh run approval and safety checks. |
| **10 · Compare** | Look for improvements and regressions against previous results. |
| **11 · Decide** | Let a human choose to keep, revise, revert, release, or iterate. |

**In short:** **Stage 0** checks structure; **Stages 1–4** cover the first evaluation; **Stages 5–11** are your added improvement and decision loop.

You can practice the early steps by writing a case and comparing an already-saved audit report with its source. That is a **manual review**, not an executed model eval.

## 7. How teams use evals in practice

- **Before release:** Test realistic tasks and intentionally difficult or adversarial cases to catch mistakes early.
- **When changing a skill, prompt, or model:** Rerun saved cases to check whether the change helped or broke something that previously worked.
- **After deployment:** Review appropriately protected production traces and feedback to discover new failure patterns, then turn those patterns into regression cases.

Teams often combine **code-based checks** (for exact requirements), **human review** (for engineering judgment and evidence), and **LLM graders** (for broader output quality). A grader's score is not proof of runtime security.

**Junior-developer mental model:** What should happen? What actually happened? What evidence supports the result? What was the agent allowed to do?

## 8. The 12 stages

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

## 9. Five conference-informed methodology lenses

Used in **Stage 6** to review a skill from different engineering perspectives. These are DotSkills review practices, not mandatory Agent Skills format requirements.

| Lens | What to look for |
| --- | --- |
| [**Context Engineering**](../context-engineering/SKILL.md) | Missing, stale, conflicting, or untrusted context |
| [**Correctness & Verification**](../correctness-and-verification/SKILL.md) | Supported claims, invariants, and reliable checks |
| [**Observability & Feedback**](../agent-observability-and-feedback/SKILL.md) | Outputs, tool attempts, traces, and useful feedback |
| [**Trust & Governance**](../agent-trust-and-governance/SKILL.md) | Permissions, trust boundaries, and unintended side effects |
| [**Skill Lifecycle & Release**](../skill-lifecycle-and-release/SKILL.md) | Versioning, regressions, and release readiness |

**More detail:** [Workflow](references/workflow.md) · [Eval case design](references/eval-design-guide.md) · [Runner and safety controls](runner/README.md) · [Approval gates](references/approval-gates.md)
