# Eval-Driven Skill Development

A repeatable, human-gated workflow for turning rough skill material into a valid skill package and then improving that skill through representative evals, preserved evidence, targeted methodology diagnosis, and regression checks.

Use this workflow for any DotSkills skill: code review, requirements refinement, investigation, learning, rehearsal, or decision support. DDIA code review is a worked example below, not a restriction on the workflow.

The operational source of truth is [`skills/eval-driven-skill-development/SKILL.md`](../skills/eval-driven-skill-development/SKILL.md). This guide explains the workflow in practical terms.

## Table of contents

- [Current workflow](#current-workflow)
- [Operating contract](#operating-contract)
  - [Human-gated by default](#human-gated-by-default)
  - [User-visible workflow trace](#user-visible-workflow-trace)
  - [Guided learning](#guided-learning)
- [What you are evaluating](#what-you-are-evaluating)
- [End-to-end workflow](#end-to-end-workflow)
- [0. Bootstrap or normalize the target](#0-bootstrap-or-normalize-the-target)
- [1. Frame one observable behavior](#1-frame-one-observable-behavior)
- [2. Define the cases and the answer key](#2-define-the-cases-and-the-answer-key)
- [3. Run the baseline eval](#3-run-the-baseline-eval)
  - [Before each run](#before-each-run)
  - [During each run](#during-each-run)
  - [After each run](#after-each-run)
- [4. Grade meaning and inspect the evidence](#4-grade-meaning-and-inspect-the-evidence)
- [5. Diagnose before changing the skill](#5-diagnose-before-changing-the-skill)
- [6. Methodology coverage scan and specialist routing](#6-methodology-coverage-scan-and-specialist-routing)
- [7. Propose and apply the smallest justified change](#7-propose-and-apply-the-smallest-justified-change)
- [8. Compare, check regressions, and expand coverage](#8-compare-check-regressions-and-expand-coverage)
- [Worked progression: DDIA review](#worked-progression-ddia-review)
- [Reusable case outline](#reusable-case-outline)
- [How much subject knowledge do you need?](#how-much-subject-knowledge-do-you-need)
- [Where the pieces belong](#where-the-pieces-belong)

## Current workflow

Eval-driven skill development now covers two connected activities:

1. **Bootstrap / normalize** a raw prompt, source material, or partial draft into the smallest valid skill package needed for evaluation.
2. **Refine behavior through eval evidence** after the target can be run and compared.

You do not need to manually turn a rough prompt into a finished skill before starting. The workflow first assesses maturity, proposes the package structure, and pauses at a human gate before creating, moving, or rewriting target-skill files.

The bootstrap stage does **not** create every possible support file. A separate context-quality reference, script, asset, or other package file is added only when a concrete need justifies it. Short, always-needed context rules normally stay in `SKILL.md`; substantial or conditionally loaded material can move to `references/` when complexity, reuse, or progressive loading warrants that split.

After bootstrap, eval design and execution remain part of the same workflow, but human gates still control consequential transitions: behavior selection, case approval, baseline execution, grading acceptance, specialist routing, target-skill edits, comparable reruns, and keep/revise/revert decisions.

## Operating contract

### Human-gated by default

The methodology is an operating workflow, not an autonomous batch process. At each human gate it should:

1. show the evidence or decision under consideration;
2. make one clear recommendation and explain why;
3. offer a small number of materially different alternatives when useful;
4. allow the human to propose a different solution, concern, constraint, or hypothesis;
5. treat feedback as feedback, not approval;
6. revise the proposal when warranted;
7. proceed only after explicit approval of the action currently gated.

Ordinary analysis and preparation can continue without a response when no human gate is defined.

### User-visible workflow trace

Every meaningful stage should produce a concise user-facing execution trace, even when that stage does not require input.

A progress update should state:

- what stage just completed;
- the concrete result, finding, or limitation;
- what comes next;
- whether the workflow is continuing or waiting at a **HUMAN GATE**.

Progress updates are informational and non-blocking. Only an explicit **HUMAN GATE** pauses the workflow.

The trace exposes workflow state, evidence, decisions, and outcomes—not private chain-of-thought, raw scratch work, or low-level tool chatter.

Example:

```text
Bootstrap assessment complete — target is a partial draft.
Next: propose the smallest valid package. Continuing.

Package proposal ready.
HUMAN GATE — approve or revise the proposed structure.

Approved normalization applied; structural validation passed.
Next: define one observable behavior to evaluate. Continuing.
```

### Guided learning

The default interaction teaches the methodology while doing the work. At meaningful gates, briefly explain the concept in use, what it means for the current skill, which evidence matters, and why the recommendation follows.

Supported learning depths:

- **Guided** — concise explanation at relevant gates.
- **Deep dive** — more theory, examples, trade-offs, and connections.
- **Fast** — minimal teaching for familiar concepts.

Learning content, human feedback, answer keys, and grading criteria must stay outside the evaluated target skill's task context unless intentionally required by that task.

## What you are evaluating

An eval observes an agent performing a task with a particular skill, model, harness, context, and tool setup. Its results describe that combination under the tested conditions. They do not establish that the instruction file alone caused the outcome.

| Item | Purpose |
| --- | --- |
| Skill | Reusable instructions and references that guide the agent. |
| Eval case | A particular task, its inputs, and evaluator-only expectations and grading criteria. |
| Eval suite | A collection of cases covering different situations. |
| Run | One attempt at one case under a recorded configuration. |
| Grader or rubric | Checks the completed output and available action evidence against the case criteria. |
| Baseline | A recorded starting result used for later comparisons, including failures and unknowns. |

For code review, an application unit test checks what the application does. A reviewer eval checks whether the agent correctly assesses that behavior. Buggy application code can fail its unit test while the reviewer passes by correctly finding the defect.

You can give the agent the full relevant skill while a case checks one narrow capability. There is no requirement to test each instruction sentence in isolation.

## End-to-end workflow

```mermaid
flowchart TD
    A[Assess target maturity] --> B{Raw or partial?}
    B -->|Yes| C[Propose smallest valid skill package]
    C --> G0[HUMAN GATE: approve normalization]
    G0 --> D[Apply approved structure and validate]
    B -->|No| E[Keep existing package]
    D --> F[Define one observable behavior]
    E --> F
    F --> G1[HUMAN GATE: approve behavior]
    G1 --> H[Draft neutral eval case and grading]
    H --> G2[HUMAN GATE: approve case]
    G2 --> I[Choose baseline and run configuration]
    I --> G3[HUMAN GATE: approve execution]
    G3 --> J[Run baseline and preserve evidence]
    J --> K[Grade]
    K --> G4[HUMAN GATE: inspect or challenge grade]
    G4 --> L[Diagnose failure or uncertainty]
    L --> M[Scan all methodology layers]
    M --> R{Evidence supports specialist?}
    R -->|Context failure| CE[context-engineering]
    R -->|Correctness or verification failure| CV[correctness-and-verification]
    R -->|Version, regression, portability, release| LR[skill-lifecycle-and-release]
    R -->|Trace, telemetry, production feedback| OF[agent-observability-and-feedback]
    R -->|Authority, provenance, permissions, risk| TG[agent-trust-and-governance]
    R -->|No specialist needed| N[Develop smallest justified improvement]
    CE --> G5[HUMAN GATE: approve routing]
    CV --> G5
    LR --> G5
    OF --> G5
    TG --> G5
    G5 --> N
    N --> G6[HUMAN GATE: approve target-skill change]
    G6 --> O[Apply approved change]
    O --> G7[HUMAN GATE: approve comparable rerun]
    G7 --> P[Rerun same case]
    P --> Q[Regression and independent cases]
    Q --> G8[HUMAN GATE: keep, revise, revert, or continue]
    G8 --> Z[Record result and next case]
```

The coverage scan considers every methodology layer, but it does **not** invoke every specialist. Routing is evidence-driven and human-approved.

Keep every run record, including unsuccessful attempts. A completed cycle can end with an unresolved limitation; it does not need to manufacture a passing result.

## 0. Bootstrap or normalize the target

Classify the target as:

- raw prompt or source material;
- partial or inconsistently structured skill;
- structurally valid skill package.

If the target is raw or partial, identify its intended task, triggers, exclusions, required inputs and context, procedure, output expectations, tool boundaries, and repository packaging conventions.

Then propose the **smallest valid package** that makes the capability portable and evaluable. In DotSkills, `SKILL.md` is the package entry point. Add `references/`, `scripts/`, `assets/`, or other support files only when a concrete need justifies them.

Bootstrap decision rules:

- normalize only enough structure to make the capability clear, portable, and evaluable;
- do not confuse template completeness with behavioral quality;
- keep task-specific runtime rules in the target skill and reusable methodology in methodology skills;
- prefer inline guidance when it is short and always needed;
- prefer a reference when material is substantial, conditionally loaded, independently maintained, or would make `SKILL.md` difficult to scan;
- create a dedicated context-requirements reference only when enough task-specific context rules justify one;
- do **not** create `context-quality-and-requirements.md` merely because another skill has one;
- identify required catalog registration and structural validation;
- treat structural validation as repository-health evidence, not proof of behavioral quality.

**HUMAN GATE:** show the maturity assessment, proposed structure, exactly what would be created/moved/rewritten/retained, and why. Apply only the approved normalization changes.

If the target is already structurally valid, state that bootstrap is unnecessary and continue without rewriting it merely to match a preferred style.

## 1. Frame one observable behavior

Start with a small, observable objective. Write down the intended task, required context, scope, and what the agent should do when evidence is missing.

| Skill | Example capability to evaluate |
| --- | --- |
| DDIA code review | Distinguish a partial-update defect from a protected operation or an unresolved storage guarantee. |
| Requirements refinement | Inspect an existing implementation pattern before proposing requirements, and distinguish established facts from stakeholder questions. |
| Repository investigation | Trace a behavior through relevant callers and dependencies without inventing unseen implementation details. |
| Decision support | Identify missing decision evidence and apply the specified workflow without inventing inputs or unauthorized effects. |

Define success as behavior you can inspect. For example, “explain which mutation survives a failed operation and which requirement it violates” is more useful than “give a thorough review.”

Decide whether you are testing a reference directly, the whole skill package, skill selection, or an end-to-end workflow. A direct reference test does not also test whether the harness selects and loads the right skill.

**HUMAN GATE:** present the target behavior, recommendation, alternatives, and open feedback path. Obtain approval before finalizing the evaluation direction.

## 2. Define the cases and the answer key

Each case includes what the agent receives and what the evaluator checks. Keep those parts separate when executing the case, even if they are stored in one authoring file.

| Part | What to include | Who receives it during a run? |
| --- | --- | --- |
| Identity and capability | Stable case ID and the behavior being measured. | Eval coordinator. Avoid revealing the diagnosis through names. |
| Input | Neutral task, realistic requirements, files, context, and allowed tools. | Agent under evaluation. |
| Expected behavior | Correct conclusion, essential explanation, or appropriate handling of uncertainty. | Evaluator. |
| Grading | Required behavior, unacceptable claims or actions, and evidence needed for each check. | Evaluator. |
| Answer-key evidence | Requirement, reproduction, authoritative source, or expert review establishing the expectation. | Evaluator. |

For a review capability, begin with contrasting cases: a defect exists, the relevant protection exists, and evidence is insufficient. For other skills, use the equivalent normal, boundary, and missing-context situations. Add cases as you discover distinct failure modes; useful coverage matters more than case count.

Verify the expected answer before relying on it. Small executable examples help establish code behavior; complex repository changes may also require requirements, integration evidence, or expert review. An LLM can draft a case, but its confidence is not proof that the answer key is correct.

Keep task wording neutral. “Review this transfer against its requirements” gives an assignment. “Find the debit that survives a rejected transfer” reveals the diagnosis.

**HUMAN GATE:** present the proposed case, what it tests, and the evaluator-only grading intent. The human can approve, revise, replace, or contribute a different case before execution.

## 3. Run the baseline eval

For an existing skill, run the unchanged target on the approved case. For a new or newly bootstrapped skill, choose an explicit baseline such as no skill, the raw source prompt, the pre-normalization instructions, or the approved normalized draft. Make the baseline choice explicit so the later comparison has a clear meaning.

To explore coverage, keep one skill version fixed and run it across different cases. To compare a skill change, hold each case and its rubric fixed and run both skill versions under comparable conditions. If you correct a case or rubric, version the correction and reassess both sides before claiming improvement.

**HUMAN GATE before execution:** confirm the baseline, run configuration, and that hidden teaching or evaluator-only information will not enter the evaluated task context.

### Before each run

- [ ] Identify the exact skill/reference version and case version or hashes.
- [ ] Record the model, harness, settings, tools, permissions, and time or token budget where available.
- [ ] Confirm the fixture and expected behavior agree; distinguish intentional missing context from a setup mistake.
- [ ] Prepare only the agent-facing inputs. Exclude answer keys, private verification scripts, other variants, and earlier outputs.
- [ ] Start a fresh session without the eval-authoring conversation or previous answers.
- [ ] Configure workspace access restrictions where supported. A working directory alone is not an access-control boundary.

### During each run

- [ ] Provide the task and selected guidance through the intended harness workflow.
- [ ] Avoid hints or mid-run corrections. If intervention is needed, record it as a different or invalid attempt under the protocol.
- [ ] Preserve the original response and available read/search/tool/command trace.
- [ ] Record errors, timeouts, unavailable tools, and changes to the fixture or other state.

### After each run

- [ ] Check whether the intended guidance was supplied or loaded, using the available evidence.
- [ ] Check for answer-key access or other contamination before grading.
- [ ] Record output and trace locations, trace limitations, run status, and validity.
- [ ] Grade the output separately from the loading diagnostics. Loading a guide is not itself a quality improvement.

**How this works today:** DotSkills has a [manual code-review eval package](../evals/code-review/context-validation/README.md), preparation and fixture-verification helpers, and recorded results. It does not yet have a general automated model-evaluation runner. A capable coding-agent harness can execute the documented helper commands and coordinate authorized steps, but you must still launch the evaluated agent, capture its result, and grade it. A script that prepares files or verifies a fixture does not perform all those steps automatically.

The existing preparation helper selects a historical skill snapshot for one case at a time. Its `before` and `after` labels identify those snapshots; neither selects the current skill. Recorded attempts, including direct-DDIA runs, live in each case’s `results/` folder.

## 4. Grade meaning and inspect the evidence

Define the grading criteria before the run. A numeric score is optional: start with **Pass / Fail / Unknown** for each criterion and a short evidence note. Define how those checks combine if you need an overall case result; do not hide a critical failure inside an average.

For a review, check whether the conclusion is correct, its explanation connects concrete behavior to the requirement, and source or execution claims are supported. Grade essential meaning, allowing different wording. “Consider transactions” does not establish that the reviewer found a particular partial-update defect.

Use deterministic checks for observable facts such as changed file hashes or recorded command results. Use a precise rubric for semantic judgments. A cited path existing does not prove it supports a claim, and a plausible final answer does not prove a tool was used. If using an LLM judge, calibrate its decisions against human review, especially disagreements and borderline cases.

Keep these outcomes distinct:

| Situation | Treatment |
| --- | --- |
| A completed, valid response contradicts an established requirement. | Fail the relevant quality check. |
| The case deliberately omits decisive evidence, and the agent identifies that limit accurately. | This can pass the uncertainty criterion. |
| The trace does not establish whether the agent inspected a file or ran a command. | Mark that process check Unknown. |
| The agent accessed the answer key. | Mark the run Invalid; repeat without contamination. |
| No completed response exists, or execution stopped. | Record Not Run, Error, or Incomplete as appropriate; do not invent a quality grade. |

Execution reliability may be a separate measured objective. Record those failures even when there is no completed response to grade.

**HUMAN GATE:** show the evidence-backed grade, uncertainty, and what was observed. The human can challenge the grade, add observations, or request more evidence before diagnosis proceeds.

## 5. Diagnose before changing the skill

A failed check is evidence to investigate, not an automatic instruction to rewrite the prompt.

| Possible cause | Next action |
| --- | --- |
| Incorrect or ambiguous expected answer | Recheck requirements and evidence; correct and version the case or rubric. |
| Required context accidentally absent | Repair the setup, or explicitly make missing-context behavior the objective. |
| Skill not loaded, tool unavailable, or execution interrupted | Repair or document the harness/setup issue. |
| Judge interprets the rubric incorrectly | Clarify the rubric and audit previous judgments affected by the change. |
| Skill guidance leads to the wrong decision | Make a targeted instruction change addressing the general reasoning weakness. |
| Results vary across attempts | Repeat under the same conditions and retain all attempts; do not select only favorable outputs. |

Improve the reusable procedure, not a memorized answer. For example, require checking relevant callers and storage guarantees before reporting an atomicity defect, rather than teaching the exact names and balances in one fixture.

Follow [source ownership](sources.md) when editing imported references: preserve locked snapshots, put adapted guidance in a separate file, or deliberately update upstream content and its lock through the documented process.

## 6. Methodology coverage scan and specialist routing

After diagnosis, scan all five methodology layers so important failure classes are not skipped. Record each layer as **relevant**, **not evidenced**, or **currently not applicable**.

| Methodology skill | Trigger it when the evidence suggests... | Typical signals |
| --- | --- | --- |
| [`context-engineering`](../skills/context-engineering/SKILL.md) | The target skill is using the wrong amount, quality, provenance, freshness, or stopping behavior for context. | Missing necessary context, distracting/excessive context, stale or conflicting context, untrusted contamination, context inertia, premature stopping, unnecessary continued search. |
| [`correctness-and-verification`](../skills/correctness-and-verification/SKILL.md) | The problem is whether conclusions are correct and sufficiently supported. | Unsupported claims, missed invariants, incorrect boundary/failure-path reasoning, weak deterministic verification, confusion between observed and intended behavior, evidence that cannot establish the claimed scope. |
| [`skill-lifecycle-and-release`](../skills/skill-lifecycle-and-release/SKILL.md) | The problem involves version comparison, regression safety, portability, CI/CD, model/harness changes, release readiness, or rollback. | A proposed skill revision, a model/harness upgrade, regressions, cross-harness differences, release evidence, compatibility questions. |
| [`agent-observability-and-feedback`](../skills/agent-observability-and-feedback/SKILL.md) | The final answer alone cannot explain what failed, or production feedback needs to become eval coverage. | Missing trace evidence, unclear tool/context trajectory, runtime/state/infrastructure failures, latency/cost questions, production incidents, missing telemetry. |
| [`agent-trust-and-governance`](../skills/agent-trust-and-governance/SKILL.md) | The task crosses authority, provenance, permission, approval, sensitive-action, or risk boundaries. | Untrusted context, external side effects, sensitive tools/data, unclear authorization, identity or provenance questions, high-impact decisions, insufficient approval or runtime controls. |

The scan is broad; invocation is narrow. **Do not run every specialist automatically.** The entry-point methodology recommends a specialist only when evidence supports that diagnosis.

```mermaid
flowchart TD
    A[Eval result + preserved evidence] --> B[Diagnose before editing]
    B --> C[Coverage scan across all five layers]
    C --> D{What does the evidence support?}
    D -->|Context quality / retrieval / stopping| CE[context-engineering]
    D -->|Claims / invariants / verification| CV[correctness-and-verification]
    D -->|Version / regression / portability / release| LR[skill-lifecycle-and-release]
    D -->|Trace / telemetry / production feedback| OF[agent-observability-and-feedback]
    D -->|Authority / provenance / permissions / risk| TG[agent-trust-and-governance]
    D -->|No specialist needed| N[Continue with direct diagnosis]
    CE --> G[HUMAN GATE: approve specialist routing]
    CV --> G
    LR --> G
    OF --> G
    TG --> G
    G --> H[Specialist returns diagnosis + recommendation]
    N --> I[Develop proposed improvement]
    H --> I
    I --> J[HUMAN GATE: approve target-skill change]
```

A specialist normally returns evidence, diagnosis, teaching, recommendations, alternatives, and unresolved questions to `eval-driven-skill-development`. It does **not** independently edit the target skill, run a gated comparison, or make the final keep/release decision.

Useful specialist handoff:

```text
Target skill and version:
Target maturity / package state:
Capability under test:
Case and expected behavior:
Observed behavior:
Relevant output/trace evidence:
Known setup limitations:
Current failure hypothesis:
Methodology coverage scan:
Human constraints or feedback relevant to diagnosis:
Question for the specialist methodology:
```

**HUMAN GATE:** explain the diagnosis and coverage scan, recommend one specialist or no specialist, offer alternatives, and accept the human's own routing hypothesis. Invoke a specialist only after explicit approval.

## 7. Propose and apply the smallest justified change

Use the diagnosis or approved specialist output to formulate the smallest general change supported by evidence. The proposed change may revise `SKILL.md`, restructure guidance, add or remove a supporting reference, change a task-specific context rule, or adjust another package file when justified.

Do not encode the current eval case's specific answer into the target skill.

**HUMAN GATE:** present the proposed change, why it is preferred, trade-offs, viable alternatives, files affected, and an open path for the human's own solution. Do not modify the target skill until the human explicitly approves the change.

After approval, make only the approved change. If implementation reveals that a materially different structure, file, or behavior change is needed, stop and return to the gate instead of expanding scope silently.

## 8. Compare, check regressions, and expand coverage

**HUMAN GATE before the comparable rerun:** confirm the exact before/after comparison being executed.

Rerun the same approved case with its case and rubric held fixed, then rerun the existing suite after a change, including cases that previously passed. For a large suite, record which subset ran and why, then complete the intended regression coverage before making a suite-wide claim. Also test independent cases that did not drive the edit.

| Before | After | Supported conclusion |
| --- | --- | --- |
| Fail | Pass | Improvement on that case under the tested conditions. |
| Pass | Fail | Regression to investigate. |
| Pass | Pass | No improvement demonstrated by that pass/fail criterion. |
| Fail | Fail | The measured problem remains. |
| Unknown or invalid | Any result | Resolve the evidence or validity issue before making that comparison. |

Repeat cases to examine consistency. One attempt is one observation, not a reliability estimate. Preserve skill and case versions, the rubric, raw outputs, available traces, scores, and limitations so another run can be compared fairly.

Grow from controlled diagnostic examples toward representative real tasks. Separate teaching examples inside the skill from independent evaluation cases; repeatedly tuning on the same examples can exaggerate apparent progress. A few passes do not establish broad skill quality or portability across harnesses.

**HUMAN GATE:** present before/after evidence, regressions, remaining uncertainty, and a recommendation to keep, revise, revert, or investigate further.

## Worked progression: DDIA review

This is an illustrative development cycle, not a report of newly executed evals.

1. **Observe a mistake:** the reviewer reports a partial-update defect because it sees two writes.
2. **Establish the facts:** inspect the caller and storage contract. Both writes participate in one transaction whose rollback guarantee covers the specified failure path. The transaction's name alone is insufficient evidence.
3. **Capture the case:** supply that code, contract, and neutral review task; keep the expected recognition of protection with the evaluator.
4. **Record the unchanged skill's behavior:** run the case in a fresh session. If the false alarm recurs, preserve the output and grade it against the evidence.
5. **Improve the general instruction:** require checking caller-level boundaries and the relevant storage guarantees before alleging a partial update.
6. **Check all three situations:** rerun the protected case, a case where a debit really survives rejection, and a case where the storage guarantee is unavailable.

| Case input | Expected reviewer behavior |
| --- | --- |
| Source debit remains after destination validation fails. | Explain the surviving mutation and the unchanged-on-failure requirement it violates. |
| A verified transaction rolls back both writes on the specified failure. | Recognize that protection and avoid the original false alarm within the supplied scope. |
| Relevant storage implementation and guarantees are unavailable. | Explain what cannot be established and identify the evidence needed. |

The goal is better judgment across these situations. Fewer findings by itself is not evidence of improvement.

## Reusable case outline

For a ready-to-copy folder structure, use the
[case template](../templates/case/README.md). Start with the case goal, fill
in `input/`, establish `expected.md`, define `grading.md`, then retain actual
attempts in `results/`. The reviewer receives only `input/` and the selected
skill guidance. This template applies to code, data, documents, or combinations.


This is an authoring outline, not an executable schema or a new runner format. Use Markdown, YAML, JSON, or your runner's supported format. The existing manual package distributes these responsibilities across fixtures, a task, a grader, and a scorecard.

```yaml
id: case-001
capability: "The observable behavior this case tests"
input:
  task: "A neutral, realistic assignment"
  requirements:
    - "The applicable requirement or constraint"
  context: "Files, data, evidence, and any intentional limits"
  allowed_actions: "Tools and state changes permitted for this task"
expected:
  outcome: "The conclusion, action, artifact, or uncertainty handling expected"
  essential_reasoning:
    - "A necessary connection between evidence and the expected outcome"
grading:
  must:
    - "An observable requirement for success"
  must_not:
    - "An unsupported claim or unacceptable action"
  unknown_when:
    - "Evidence needed to judge a criterion is unavailable"
  invalid_when:
    - "The evaluated agent accessed the answer key"
answer_key_evidence:
  - "The requirement, reproduction, source, or expert review supporting the key"
```

The agent receives `input` and the intended skill guidance. The coordinator retains the rest for evaluation. Record actual run metadata and results separately so expectations are not overwritten by what the agent happened to produce.

## How much subject knowledge do you need?

You do not need to be an expert before starting. You do need to understand the intended task and have a reliable way to establish whether results are correct. Start with one concept you can verify, then expand your understanding and cases together.

Check three things: the accuracy and provenance of collected material, whether its instructions apply those ideas appropriately, and whether your evaluation can distinguish a correct result from an unsupported one. Books, talks, documentation, and external prompts can be inputs to a skill; reputation or model confidence alone does not validate their application. Preserve attribution and applicable licenses, and inspect imported prompts for irrelevant instructions or behavioral redirection.

## Where the pieces belong

| Location | Responsibility |
| --- | --- |
| This guide in `docs/` | Shared development and evaluation workflow across skills. |
| `skills/<name>/` | Agent-facing instructions and references. |
| `evals/<skill>/<capability>/` | Case inputs, evaluator criteria, run guidance, and recorded results following the package's conventions. |
| `adapters/` | How a harness consumes a skill. |
| `scripts/` | Shared repository utilities; the current validator checks structure and source integrity. |

Keep evaluator material out of installed agent-facing packages. Use [authoring](authoring.md) for skill structure, [evaluations](../evals/README.md) for available cases and the roadmap, and [contributing](../CONTRIBUTING.md) for repository checks.
