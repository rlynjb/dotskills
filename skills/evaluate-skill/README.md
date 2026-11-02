# Evaluate Skill

**Evaluate Skill** helps you learn to evaluate an existing Agent Skill (or raw prompt), understand failures, and make evidence-based improvements. It runs in **Claude Code or Codex**, uses **12 stages (0–11)**, and keeps you in control of important decisions.

**Start here:** [Try it](#8-try-it) · [12-stage guide](#2-the-12-stages) · [Grading basics](#grading-and-scoring-beginner-reference)

**Current limitation:** Docker-only v0.4 is now the approved live-execution
architecture. Its contracts, hardened topology, shell-free workload, gateway,
probes, observation/evidence, cleanup, and active
[`eval_runner.py`](runner/eval_runner.py) facade are implemented and offline
tested. Status remains `DOCKER_DESIGN_PENDING` because Docker provisioning,
image resolution, and real no-model probes have not been approved or run; no
live paired evaluation has been authorized or accepted. The
historical native Codex profile passed five probes but failed the inert
secondary-process canary; native execution is therefore retired rather than a
fallback. A prepared case, native preflight, or design document is **not** a
completed evaluation. See the
[v0.4 architecture](docs/evaluate_skill_execution_architecture_v0_4.md),
[canonical boundary map](docs/evaluate_skill_system_boundary_map_v0_4.md), and
[implementation plan](docs/evaluate_skill_docker_implementation_plan_v0_4.md).

## Table of contents

- [1. Workflow at a glance](#1-workflow-at-a-glance)
- [2. The 12 stages](#2-the-12-stages)
  - [Agent, tool, and source map](#agent-tool-and-source-map)
  - [Plain-English stage guide](#plain-english-walkthrough-what-happens-next-at-each-stage)
  - [Evaluation and refinement loop](#evaluation-and-refinement-loop)
  - [Grading and scoring: beginner reference](#grading-and-scoring-beginner-reference)
- [3. Five methodology lenses](#3-five-conference-informed-methodology-lenses)
- [4. Files and evaluation cases](#4-file-and-evaluation-structure)
- [5. Claude and Codex evaluation routes](#5-provider-specific-evaluation-workflow)
- [6. Approvals and safety](#6-approval-execution-and-safety)
- [7. What Evaluate Skill adds](#7-what-evaluate-skill-adds)
- [8. Try it](#8-try-it)

## 1. Workflow at a glance

Evaluate Skill checks a skill's format, agrees on the behavior to test, drafts evaluations for your approval, reviews results, proposes improvements, and checks for regressions. **It is not a full skill creator.**

**Stage 0** checks the [Agent Skills format](https://agentskills.io/specification). The minimum package is a folder containing a `SKILL.md` file with valid YAML `name` and `description` fields and Markdown instructions. Other folders are optional. **Valid skills proceed unchanged.** If the format is invalid or the input is a raw prompt, Evaluate Skill proposes only the smallest structural fix and waits for approval.

Evaluate Skill is **Guided by default**: it explains unfamiliar concepts when useful, shows practical examples, and pauses at approval gates. **Deep dive** and **Fast** learning modes are also available.

## 2. The 12 stages

The four phases below organize the same **Stages 0–11** in both Claude Code and Codex. They do not add steps. Stage 2 **prepares** approved cases, Stages 3 and 9 **execute** them only when approved and safely isolated, and Stages 4 and 10 **review** actual evidence.

### Agent, tool, and source map

**Evaluate Skill vs. Claude Code vs. Codex — stage matrix.** Evaluate Skill supplies the **12-stage methodology** inside whichever coding agent is active. **Claude Code** and **Codex** are alternative provider evaluation formats, **not** two agents that run together. Future live execution for either format requires the same Docker-only boundary. The matrix describes what each path *would* do; it does not claim any tool was invoked.

#### Phase 1 — Preparation (Stages 0–2)

| Stage | Evaluate Skill (shared workflow) | Claude Code (when active) | Codex (when active) |
| --- | --- | --- | --- |
| **0 · Validate** | Check the target `SKILL.md` against the Agent Skills format; propose a minimal repair only if needed. | Guide the structure check; **no eval command**. | Same structure check; **no eval command**. |
| **1 · Define success** | Agree on one observable behavior, success criteria, and permitted/prohibited effects with the human. | Guide the discussion; **no eval command**. | Guide the discussion; **no eval command**. |
| **2 · Design cases** | Draft 2–3 cases, expectations, and assertions. **Human approval** is required before saving or preparing cases. | After approval, `eval_runner.py prepare --provider anthropic` writes Claude plugin-eval cases and `type: llm` grader files. **Not Run**. | After approval, `eval_runner.py prepare --provider openai` writes Promptfoo cases with `openai:codex-sdk` and `llm-rubric`. **Not Run**. |

#### Phase 2 — Evaluation (Stages 3–4)

| Stage | Evaluate Skill (shared workflow) | Claude Code (when active) | Codex (when active) |
| --- | --- | --- | --- |
| **3 · Run baseline** | Require **separate run approval** and independently verified mock-only isolation; otherwise **Blocked — Not Run**. | If authorized and isolated, run paired comparisons through `claude plugin eval --ablation with-without`. | If authorized and isolated, run paired workspaces through `promptfoo eval` using `openai:codex-sdk`. |
| **4 · Review grades** | Inspect actual outputs, native grades, tool-attempt traces, and uncertainty; do **not** run a second grader automatically. | Review Claude's `type: llm` grades and trusted host evidence from Stage 3. | Review Promptfoo `llm-rubric` grades and trusted host evidence from Stage 3. |

#### Phase 3 — Diagnosis and improvement (Stages 5–8)

| Stage | Evaluate Skill (shared workflow) | Claude Code (when active) | Codex (when active) |
| --- | --- | --- | --- |
| **5 · Diagnose** | Determine whether the issue is in the skill, case, grader, context, permissions, or environment **before editing**. | Analyze the observed Claude results; **no native eval command**. | Analyze the observed Codex results; **no native eval command**. |
| **6 · Review five lenses** | Screen context, correctness, observability, trust, and lifecycle; request approval for any justified specialist deep dive. | Guided methodology review; **no automatic specialist invocation**. | Same guided methodology review; **no automatic specialist invocation**. |
| **7 · Propose** | Explain the smallest supported improvement, alternatives, and affected files; **wait for edit approval**. | Present proposal in Claude Code; **no edit yet**. | Present proposal in Codex; **no edit yet**. |
| **8 · Apply** | Apply **only approved changes** and preserve the diff/version evidence. | The active Claude Code agent edits approved files only. | The active Codex agent edits approved files only. |

#### Phase 4 — Verification and decision (Stages 9–11)

| Stage | Evaluate Skill (shared workflow) | Claude Code (when active) | Codex (when active) |
| --- | --- | --- | --- |
| **9 · Rerun** | Request **fresh run approval and isolation**; rerun fixed cases/rubrics, including relevant previously passing cases. | Repeat approved `claude plugin eval` runs; preserve Claude-native results. | Repeat approved `promptfoo eval` / Codex SDK runs; preserve Promptfoo-native results. |
| **10 · Compare** | Compare observed before/after evidence and regressions; **no automatic new comparator**. | Review comparable Claude-native reports and host traces. | Review comparable Promptfoo-native reports and host traces. |
| **11 · Decide** | **Human chooses** keep, revise, revert, release, or iterate; record evidence and open risks. | Guide the final decision; **no automatic release**. | Guide the final decision; **no automatic release**. |

**Source and evidence map:** Stage **0** uses the target `SKILL.md` and [Agent Skills specification](https://agentskills.io/specification); Stages **1–2** use the target requirements and [eval design guide](references/eval-design-guide.md); Stages **3/9** use approved cases, the [runner guide](runner/README.md), and independently verified host controls; Stages **4/10** require actual provider-native reports and trusted action/state traces; Stages **5–8** use observed failure evidence and the [methodology lenses](references/methodology-lenses.md); Stage **11** uses versioned results and the human's decision. Documentation links are reference material, **not automatic network requests**.

**Important:** Neither harness substitutes for the other. Native evaluation commands may **execute and grade in the same run**, so Stage 4 **reviews** grades from Stage 3 rather than launching a second grader. Stage 6 does not automatically run five specialist agents. A prepared case, structural check, or offline test is **not** a completed model evaluation.

### Plain-English walkthrough: what happens next at each stage

| Phase | Stage | What happens and why |
| --- | --- | --- |
| **Preparation** | **0 · Validate** | Check `SKILL.md` structure. Leave a valid skill alone; ask before minimal formatting fixes. |
| | **1 · Define success** | Agree on **one observable behavior**, what success means, and what the skill must not do. |
| | **2 · Design cases** | The agent drafts **2–3 realistic tests**, expected results, and grading assertions. **You review and approve** before cases or fixtures are saved or prepared. No evaluated agent or grader runs yet. |
| **Evaluation** | **3 · Run baseline** | With separate approval and verified isolation, run the same case **with and without the skill** in fresh contexts. The command may produce LLM grades too; otherwise **Blocked — Not Run**. |
| | **4 · Review grades** | Inspect those grades, outputs, and evidence. **Do not assume the grader is correct** or run a second grader automatically. |
| **Diagnosis and improvement** | **5 · Diagnose** | Find the cause: skill instructions, test case, grader, context, permissions, or environment. **No edits yet.** |
| | **6 · Review five lenses** | Check wider issues such as context quality, correctness, safety and lifecycle. Deep dives need justification and approval. |
| | **7 · Propose** | Show the smallest supported improvement and its trade-offs. **You approve, request revision, or stop.** |
| | **8 · Apply** | Change **only the approved files**, preserving a diff and earlier version. |
| **Verification and decision** | **9 · Rerun** | With **new run approval and isolation**, repeat the target case **and relevant previously passing cases**, preserving original rubrics and saving separate results. |
| | **10 · Compare** | Compare results within the same provider. Did the change help? Did anything that used to pass now fail (a **regression**)? |
| | **11 · Decide** | **You choose** keep, revise, revert, release or iterate. Preserve approved tests and results for future changes. |

**Example — Learn Repo:** Stage 1 defines “explain real modules and pause at checkpoints.” In Stage 2 the agent proposes an architecture test and a checkpoint test; **you approve them**. After an authorized Stage 3 run, Stage 4 checks the actual results. If you approve an improvement in Stage 7, Stages 9–10 retest both behaviors before you decide at Stage 11. These are **illustrative steps, not a record of executed tests**.

### Evaluation and refinement loop

```mermaid
flowchart LR
    A["0–2 · Prepare and approve cases"] --> B{"Stage 3 · Run approved and isolated?"}
    B -->|No| X["Blocked · Not Run"]
    B -->|Yes| C["3–4 · Execute and review grades"]
    C --> D["5–6 · Diagnose and screen lenses"]
    D --> E["7 · Propose improvement"]
    E --> F{"Approve edit?"}
    F -->|No| Y["Revise proposal or stop"]
    F -->|Yes| G["8 · Apply approved edit"]
    G --> H{"Stage 9 · Rerun approved and isolated?"}
    H -->|No| X
    H -->|Yes| I["9–10 · Rerun and compare"]
    I --> J{"11 · Your decision"}
    J -->|Revise| E
    J -->|Keep or revert| K["Record outcome"]
```

### Grading and scoring: beginner reference

**Rubric = what matters · Grader = who checks · Grade = judgment · Score = summary · Acceptance rule = decision.** There is no universal AI pass percentage.

| Core component | Meaning | When |
| --- | --- | --- |
| **Rubric criteria** | The behaviors being checked, such as “identify real modules” or “pause at a checkpoint.” | Draft and approve in **Stage 2**. |
| **Grading rules** | What counts as **Pass, Fail, or Unknown** for each criterion. | Define in **Stage 2**, verify in **Stage 4**. |
| **Grader** | Code, an LLM judge, or a person applying those rules to observed output. | Configure in **Stage 2**; the approved run may grade in **Stage 3**. |
| **Points / score** | Optional numbers summarizing judgments; useful for comparisons, not proof of quality. | Define scoring rules in **Stage 2**, interpret results in **Stages 4 and 10**. |
| **Acceptance rules** | Required thresholds, **must-pass conditions**, and what to do with missing evidence. | Agree in **Stage 2**; apply when reviewing results; **you decide in Stage 11**. |

**Example:** Learn Repo passes “correct modules” and “file evidence” but fails a **mandatory checkpoint**. An illustrative 1-point-per-pass score is **2/3 (about 67%)**, yet the case **fails** because the mandatory criterion failed. This is an example, **not an actual run or a default scoring formula**.

Five checks help you judge whether the grade itself is trustworthy:

| Check | Ask yourself | Relevant stages |
| --- | --- | --- |
| **Ground truth / reference answer** | What source establishes what's correct? For Learn Repo, do the actual fixture files support the claim? | **2, 4** |
| **Grader selection** | Should this be checked by code, an LLM, or a person? | **2, 4** |
| **Grader calibration** | Does the grader agree with trusted, human-reviewed examples? | **2, 4** |
| **Evidence and traces** | What did the agent say, access, attempt or change? Is evidence missing? | **3, 4** |
| **Coverage and repeated trials** | Do cases include boundaries and safety checks? Are passes consistent across repeated runs? | **2, 3, 9, 10** |

**What Evaluate Skill uses today:** Both configured routes use **LLM graders**: Claude plugin-eval `type: llm` or Promptfoo `llm-rubric` with `openai:codex-sdk`. The active coding agent drafts assertions in Stage 2; that **does not run a grader**. Deterministic checks and human review can verify objective or safety requirements, but the dispatcher **does not automatically select among three grading systems**.

**Read results in this order:** individual criteria and mandatory failures → actual output and tool traces → overall score. Missing required evidence is **Unknown**, not Pass. Setup errors, incomplete runs and **Not Run** are not agent failures. A single trial cannot establish reliability; compare versioned cases and repeated runs when authorized.

## 3. Five conference-informed methodology lenses

Stage 6 screens these **five local references**; a specialist deep dive is conditional and needs approval.

| Lens | What it checks |
| --- | --- |
| [Context Engineering](../context-engineering/SKILL.md) | Missing, stale, conflicting or untrusted context |
| [Correctness & Verification](../correctness-and-verification/SKILL.md) | Factual support, invariants and reliable checks |
| [Observability & Feedback](../agent-observability-and-feedback/SKILL.md) | Outputs, tool attempts, traces and feedback |
| [Trust & Governance](../agent-trust-and-governance/SKILL.md) | Permission boundaries and unsafe side effects |
| [Skill Lifecycle & Release](../skill-lifecycle-and-release/SKILL.md) | Versioning, regressions and release readiness |

These lenses and approval gates are **DotSkills practices**, not Agent Skills format requirements.

## 4. File and evaluation structure

`SKILL.md` is the entry point for any skill. **The target skill owns its evaluation cases**, not Evaluate Skill. The usual layout is:

```text
skills/
├── evaluate-skill/
│   ├── SKILL.md                  # Runtime instructions
│   ├── references/              # Detailed guides
│   ├── runner/eval_runner.py    # Active Docker-only workflow facade
│   ├── runner/native_eval.py    # Historical/offline provider helpers
│   └── evals/                   # Unexecuted Evaluate Skill starter cases
└── <target-skill>/
    ├── SKILL.md
    └── evals/
        ├── evals.json           # Case ID, prompt, expected output, assertions
        └── files/              # Optional approved synthetic fixtures
```

- **Stage 2:** After your approval, cases are saved in the target's `evals/evals.json`. The dispatcher requires **nonempty, approved assertions**. Optional `files` paths are relative to the **target skill root**.
- **Preparing is not running:** `eval_runner.py prepare` creates a **new, provider-specific Docker bundle** with status `PREPARED_NOT_RUN`. No model response, grade or benchmark is created by preparation.
- **Reuse instead of overwriting:** On later invocations, reuse existing approved cases and fixtures. Save new run results separately. Changing a case or rubric requires a **new approved version**, so comparisons remain fair.

See the [evaluation design guide](references/eval-design-guide.md) for case examples and the [runner guide](runner/README.md) for exact Claude/Codex bundle layouts.

## 5. Provider-specific evaluation workflow

Evaluate Skill uses **only the provider of your active coding session**, never a fallback to the other one.

| Active session | Evaluation command | LLM grading | Results |
| --- | --- | --- | --- |
| **Claude Code** | `claude plugin eval` with paired `--ablation with-without` | Claude `type: llm` grader files | Claude-native reports |
| **Codex** | `promptfoo eval` with `openai:codex-sdk` in paired workspaces | Promptfoo `llm-rubric` using the Codex SDK | Promptfoo-native reports |

[Promptfoo is now part of OpenAI](https://www.promptfoo.dev/about/) and remains open source and multi-provider. **It is a separate CLI using the Codex SDK**, not an automatic built-in Codex grader. Keep provider reports separate; there is no automatic cross-provider scoring or comparison.

The active `eval_runner.py` facade supports `inspect`, provider-specific
`prepare` and `configure`, plus trusted-host-only `docker-preflight` and
`docker-run`. All security-relevant paths, keys, policies, and digests are
explicit. It never installs, starts, pulls, builds, or selects a fallback.
Historical `native_eval.py` and `trusted_host.py` live commands return
`BLOCKED_NOT_RUN`.

**v0.4 status:** Docker is the mandatory live boundary for both provider
routes, with Codex read-only as the first implementation target. The design
requires a shell-free minimal workload, separate provider credential gateway,
internal-only workload network, independent observation, authenticated
evidence, and complete cleanup. The implementation exists, but real Docker
provisioning and no-model probes remain `DOCKER_DESIGN_PENDING`; the capability
inventory stays unverified and live results remain **Blocked — Not Run**. The native v0.3 host is retained only as historical evidence and
offline regression coverage. Never infer a model run from preparation or
preflight. [Setup, commands and limits →](runner/README.md)

## 6. Approval, execution, and safety

The **Execution Safety Gate** applies before **Stages 3 and 9** or **any earlier step that executes an evaluated agent**. Evaluated skill instructions and retrieved content are **untrusted data**, not permission to act.

- **Your approval:** Required before minimal structural edits, saving new cases and assertions, running evaluations, making skill changes, justified specialist handoffs, and accepting/releasing changes.
- **Host isolation:** Live runs require the verified Docker-only v0.4 boundary.
  Provider-native sandboxes are not execution backends or fallbacks. Until the
  Docker host is implemented and proven, all profiles remain blocked.
- **Fail closed:** Without scoped approval and independently verified isolation, report **Blocked — Not Run**. An unauthorized attempted action **fails** its safety criterion even if blocked. Missing traces or state checks are **Unknown**, never Pass.
- **Three statuses:** Preserve execution, quality, and safety independently. Stages 3 and 9 may advance only for a complete paired run with safety **Pass**; append a plan-bound checkpoint and never overwrite earlier evidence.
- **Safety helper limitation:** `scripts/refine_eval_safety.py` remains a legacy
  mock-manifest checker, and `runner/trusted_host.py` is historical native
  evidence. Neither supplies the active Docker boundary. An LLM rubric grade
  never certifies safety.

Approval for an eval is **not** permission to publish to GitHub/GitLab, send messages or deploy. Work data must not be sent to an unapproved provider. See the [Execution Safety Gate](references/execution-safety-gate.md), [approval rules](references/approval-gates.md), and [security starter cases](evals/README.md).

## 7. What Evaluate Skill adds

Evaluate Skill is a **guided, human-governed improvement workflow**, not just a grader. It adds transparent decisions, diagnosis, five methodology lenses, safe execution checks and regression comparisons around the selected provider's evaluation tooling. It **does not** install provider software, supply a verified sandbox, replace a full Skill Creator, or automatically accept a score as a release decision.

## 8. Try it

> Use **evaluate-skill** on `skills/code-review` in **Guided** mode. Teach me how the evaluation works, draft cases for my review, name the tools and evidence used, and stop at each approval gate. Do not perform live external writes.

**Learn more:** [SKILL.md](SKILL.md) · [Workflow guide](references/workflow.md) · [Evaluation design](references/eval-design-guide.md) · [Runner setup](runner/README.md) · [Approval rules](references/approval-gates.md)

**Optional local structure checks** (from DotSkills root):

```bash
python3 scripts/validate_skill_repository_integrity.py
python3 scripts/validate_evals.py --all
```

These commands check **structure**, not actual model performance.
