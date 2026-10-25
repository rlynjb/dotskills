---
name: eval-driven-skill-development
description: "Develop or improve any agent skill from a raw prompt, partial draft, or existing skill package using human-gated normalization, representative eval cases, preserved run evidence, diagnosis before editing, methodology coverage checks, targeted specialist routing, approved changes, and regression checks. Use when creating a new skill, structuring a rough prompt into a skill, improving an existing skill, investigating a failed eval, or deciding which methodology should diagnose a weakness. Do not use it as the task skill that performs the end-user job itself."
---

# Eval-Driven Skill Development

## Objective

Develop or improve a target skill through evidence from actual eval runs rather than
adding instructions speculatively. The target may begin as a raw prompt, a partial
draft, or a structurally complete skill package.

This methodology owns two related activities:

1. **Bootstrap / normalize** an under-structured target into the smallest valid skill
   package needed to evaluate it.
2. **Refine behavior through eval evidence** once the target can be run and compared.

The target skill may be code review, investigation, refinement, learning, prompting,
or any other reusable skill.

This methodology is human-gated by default. The human remains the decision-maker at
methodology boundaries; recommendations, alternatives, feedback, and learning are part
of the workflow rather than afterthoughts.

## Operating modes

### Human-gated mode — default

Do not cross a human gate until the human explicitly approves the next action.

At each gate:
1. Show the evidence or decision being considered.
2. Make one clear recommendation and explain why it is preferred.
3. Offer a small number of materially different viable alternatives when useful.
4. Always allow the human to propose their own solution, constraint, concern, or opinion.
5. Allow the human to ask for more explanation, more alternatives, or a revised diagnosis.
6. Treat feedback as feedback, not approval.
7. If the human requests a revision or proposes an alternative, respond to it, explain
   relevant trade-offs, revise the proposal when warranted, and present the gate again.
8. Proceed only after explicit approval of the action currently gated.

The human may explicitly opt into a more autonomous mode for a particular session, but
do not infer that from silence or from approval of a different step.

### Learning mode — guided by default

Teach the methodology while doing the work. At each meaningful gate, briefly explain:
- the methodology concept currently in use;
- what it means in this concrete case;
- what evidence to notice;
- why the recommendation follows from that evidence.

When useful, invite the human to explain their reasoning in their own words, then respond
to that reasoning constructively and fill in missing considerations without reducing the
interaction to right/wrong grading.

Support three learning depths:
- **Guided** — default; concise concept explanation at relevant gates.
- **Deep dive** — more theory, examples, trade-offs, and connections to methodology.
- **Fast** — minimal teaching for concepts the human already understands.

Learning content, human feedback, answer keys, grading criteria, and recommendations must
remain outside the evaluated target skill's task context unless they are intentionally
part of the target skill's required input.

## Required context

Establish:
- The target capability and current maturity: raw prompt, partial draft, or valid skill
  package.
- The target skill and exact version when one already exists.
- Available source material, existing instructions, references, or package files.
- Repository or harness packaging conventions that apply to the target.
- One observable capability or failure to evaluate.
- The eval case and evaluator-only expected behavior when the eval stage begins.
- Model, harness, tools, permissions, and relevant limits.
- Original output plus available read/search/tool/command evidence when a run exists.
- The current human-gate decision and any human feedback that constrains the next step.

Keep answer keys and grading criteria out of the evaluated agent's input.

## Procedure

0. **Assess maturity and bootstrap the target when needed.**

   Classify the target as:
   - raw prompt or source material;
   - partial / inconsistently structured skill;
   - structurally valid skill package.

   If the target is raw or partial:
   - identify its intended task, triggers, exclusions, inputs, workflow, outputs, and
     tool boundaries;
   - inspect the applicable skill template and repository conventions;
   - propose the **smallest package structure** that makes the capability portable and
     evaluable;
   - treat the package-root `SKILL.md` as the entry point;
   - add `references/`, `scripts/`, `assets/`, or other support files only when a
     concrete need justifies them;
   - decide whether context requirements belong inline in `SKILL.md` or in a separate
     reference based on complexity, reuse, and progressive-loading needs;
   - do **not** create a `context-quality-and-requirements.md` file merely because a
     template or another skill has one;
   - identify required registration and structural validation steps for the repository.

   **Human gate:** show the current maturity assessment, proposed package structure,
   what would be created/moved/rewritten, and why. Let the human approve, revise,
   replace, or contribute their own structure before any target files are changed.

   After approval, make only the approved normalization changes and run the applicable
   structural validation. Passing structural validation means the package is well formed;
   it does not prove the skill behaves correctly.

   If the target is already structurally valid, state that bootstrap is unnecessary and
   continue without rewriting it merely to match a preferred style.

1. **Frame the target and behavior.**
   Define one observable expected behavior for the target skill. For a new or newly
   bootstrapped skill, define the intended capability before optimizing its instructions.

   **Human gate:** present the target, behavior, recommendation, alternatives, and an open
   feedback path. Obtain approval before finalizing the evaluation direction.

2. **Design the eval case.**
   Draft a neutral case plus evaluator-only expected behavior and grading criteria. Do not
   encode the answer into the evaluated agent's input.

   **Human gate:** present the proposed case and what it tests. Let the human approve,
   revise, replace, or contribute their own case before execution.

3. **Run the unchanged baseline.**
   For an existing skill, run the unchanged target skill on the approved case in a fresh
   task context. For a new or bootstrapped skill, establish an appropriate baseline such
   as no skill, the raw source prompt, current instructions, or the approved normalized
   draft. Make the baseline choice explicit before execution.

   **Human gate before execution:** confirm the run configuration and that no hidden
   teaching or evaluator information will enter the task context.

4. **Preserve and grade the evidence.**
   Preserve output, trace, configuration, errors, and limitations. Grade without forcing
   certainty: Pass, Fail, Unknown, Invalid, Error, or Incomplete are valid outcomes.

   **Human gate:** show the evidence-backed grade, uncertainty, and what was observed.
   Let the human challenge the grade, add observations, or request more evidence before
   diagnosis proceeds.

5. **Diagnose before editing.**
   Determine whether the cause is the case, rubric, missing context, harness/tooling,
   model variability, package structure, or target-skill guidance. A failed eval is not
   permission to edit.

6. **Perform a methodology coverage scan and recommend specialist routing when needed.**

   Consider every major methodology layer so important failure classes are not skipped:
   - **Context engineering:** missing, stale, conflicting, distracting, excessive, or
     prematurely stopped context.
   - **Correctness and verification:** unsupported claims, broken invariants, weak
     evidence, or missing deterministic checks.
   - **Skill lifecycle and release:** versioning, regressions, portability, CI,
     compatibility, or release readiness.
   - **Agent observability and feedback:** unclear trajectory, insufficient telemetry,
     weak process/outcome signals, or missing production feedback.
   - **Agent trust and governance:** authority, provenance, permissions, approvals,
     unsafe actions, or risk-control gaps.

   Record whether each layer is relevant, not evidenced, or currently not applicable.
   **Do not invoke every specialist automatically.** Recommend a specialist only when the
   observed evidence supports that diagnosis.

   **Human gate:** explain the diagnosis and coverage scan, teach the relevant concept in
   learning mode, recommend one specialist or no specialist, offer alternatives, and
   accept the human's own routing hypothesis. Invoke a specialist only after explicit
   approval.

7. **Develop a proposed improvement.**
   Use the diagnosis or specialist output to formulate the smallest general change
   supported by evidence. The proposed change may revise `SKILL.md`, restructure
   guidance, add/remove a supporting reference, change a context rule, or adjust another
   package file when justified. Do not encode the case's specific answer into the target
   skill.

   **Human gate:** present the proposed change, why it is preferred, trade-offs, viable
   alternatives, files affected, and an open path for the human's own solution. Do not
   modify the target skill until the human explicitly approves the change.

8. **Apply the approved change.**
   Make only the approved target-skill change. If implementation reveals a materially
   different structure, file, or behavior change is needed, stop and return to the human
   gate instead of expanding scope silently.

9. **Re-run the same eval.**
   Hold the case and rubric fixed and use comparable run conditions.

   **Human gate before execution:** confirm the exact comparison being run.

10. **Check regressions and independence.**
    Run relevant previously passing cases and an independent case when practical.

    **Human gate:** present before/after evidence, regressions, remaining uncertainty, and
    a recommendation about whether to keep, revise, revert, or investigate further.

11. **Accept or continue.**
    Keep useful cases as regression coverage only after human approval. Record unresolved
    limits, rejected alternatives, package-structure decisions, and the next independent
    case when useful.

## Bootstrap decision rules

Use these rules when turning rough material into a skill package:

- Normalize only enough structure to make the capability clear, portable, and evaluable.
- Do not confuse template completeness with behavioral quality.
- Keep task-specific runtime rules in the target skill; keep methodology in the
  methodology skills.
- Prefer inline guidance when it is short and always needed.
- Prefer a supporting reference when guidance is substantial, conditionally loaded,
  independently maintainable, or would make the entry point harder to scan.
- Create a dedicated context-requirements reference only when the target has enough
  task-specific context rules to justify one.
- Do not create files solely because another skill has them.
- Do not delete useful source material during normalization unless the human explicitly
  approves that deletion.
- Structural validation is a prerequisite for repository health, not evidence that the
  skill succeeds at its task.

## Standard human gate

Use a compact structure like:

```text
HUMAN GATE — <decision>

Evidence / current state:
<what happened or what is being proposed>

Concept in use:
<short learning-mode explanation when relevant>

My recommendation:
<one preferred option and why>

Other viable options:
A. <materially different alternative>
B. <materially different alternative>

Your choices:
1. Approve the recommendation
2. Choose an alternative
3. Give my own solution / opinion / constraint
4. Revise with my feedback
5. Ask for more recommendations
6. Explain this concept more deeply
7. Challenge the diagnosis or evidence
8. Skip this action when safe
9. Stop the methodology session

Your thoughts:
<free-form human input>
```

Do not dump many equally weighted options. Make a recommendation. Alternatives should
exist to support judgment, not to avoid judgment.

A human response that contains thoughts, questions, or revisions without explicit
approval does not authorize the gated action.

## Failure handoff

When invoking a specialist methodology, pass:

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

The specialist diagnoses the failure; it does not automatically edit the target skill.

## Output

Return:
- Target skill/capability and current maturity.
- Bootstrap / normalization status and approved package changes, if any.
- Current methodology stage and pending human gate.
- Case and run status.
- Evidence-backed diagnosis.
- Methodology coverage scan across context, correctness, lifecycle, observability, and
  trust/governance.
- Relevant learning concept and explanation depth used.
- Specialist methodology used, if any.
- Recommendation, alternatives considered, and human feedback that changed the plan.
- Targeted change proposed or made, including affected files.
- Before/after result and regression status.
- Remaining uncertainty and next independent case.

## Decision rules

- Human-gated mode is the default.
- A raw prompt or partial draft may be bootstrapped before behavioral evals begin.
- Bootstrap changes require explicit approval just like later target-skill edits.
- A failed eval is evidence to investigate, not an automatic prompt rewrite.
- Human feedback is not implicit approval.
- Perform the methodology coverage scan; do not automatically invoke every specialist.
- Specialist invocation is a recommendation until the human approves it.
- Target-skill edits require explicit approval in human-gated mode.
- A plausible final answer does not prove a file or tool was used.
- Preserve unsuccessful attempts and infrastructure failures.
- Hold the case and rubric fixed when comparing skill versions.
- Treat model or harness changes as possible regression triggers.
- Keep learning content outside the evaluated agent's context unless intentionally required.
- Prefer general behavioral rules over patches that merely solve the current eval case.
- Let eval evidence justify new support files or structural complexity rather than adding
  them preemptively.

## Session-derived principles

This operational method synthesizes the AGNTCon/MCPCon sessions on real agent
evaluations, agent regression testing, EvalBench, shipping agent skills safely, context
engineering, verification, observability, and trust: evaluate realistic user journeys,
start mutating evals from known state, keep comparisons reproducible, treat skills like
versioned software, preserve human judgment at consequential methodology boundaries,
learn from concrete failures, normalize rough capabilities before measuring them when
needed, and re-run coverage when the skill, model, harness, tools, or package structure
change.
