---
name: eval-driven-skill-development
description: "Develop or improve any agent skill using representative eval cases, preserved run evidence, diagnosis before editing, human-gated decisions, guided learning, targeted changes, and regression checks. Use when creating a new skill, improving an existing skill, investigating a failed eval, or deciding which methodology should diagnose a skill failure. Do not use it as the task skill that performs the end-user job itself."
---

# Eval-Driven Skill Development

## Objective

Improve a target skill through evidence from actual eval runs instead of adding
instructions speculatively. The target skill may be code review, investigation,
refinement, learning, prompting, or any other reusable skill.

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
- The target skill and exact version, or the proposed capability if creating a new skill.
- One observable capability or failure to evaluate.
- The eval case and evaluator-only expected behavior.
- Model, harness, tools, permissions, and relevant limits.
- Original output plus available read/search/tool/command evidence when a run exists.
- The current human-gate decision and any human feedback that constrains the next step.

Keep answer keys and grading criteria out of the evaluated agent's input.

## Procedure

1. **Frame the target and behavior.**
   Define one observable expected behavior for the target skill. If creating a new skill,
   define the intended capability before drafting implementation instructions.

   **Human gate:** present the target, behavior, recommendation, alternatives, and an open
   feedback path. Obtain approval before finalizing the evaluation direction.

2. **Design the eval case.**
   Draft a neutral case plus evaluator-only expected behavior and grading criteria. Do not
   encode the answer into the evaluated agent's input.

   **Human gate:** present the proposed case and what it tests. Let the human approve,
   revise, replace, or contribute their own case before execution.

3. **Run the unchanged baseline.**
   For an existing skill, run the unchanged target skill on the approved case in a fresh
   task context. For a new skill, establish an appropriate baseline such as no skill,
   current instructions, or an initial draft only after that baseline choice is approved.

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
   model variability, or target-skill guidance. A failed eval is not permission to edit.

6. **Recommend specialist routing when needed.**
   Route a confirmed target-skill weakness to the relevant methodology:
   - missing, stale, conflicting, distracting, or excessive context → `context-engineering`
   - unsupported claims, broken invariants, or weak verification → `correctness-and-verification`
   - versioning, regressions, portability, CI, or release → `skill-lifecycle-and-release`
   - unclear trajectory, insufficient telemetry, or production feedback → `agent-observability-and-feedback`
   - authority, provenance, permissions, approvals, or unsafe actions → `agent-trust-and-governance`

   **Human gate:** explain the diagnosis, teach the relevant concept in learning mode,
   recommend one specialist or no specialist, offer alternatives, and accept the human's
   own routing hypothesis. Invoke a specialist only after explicit approval.

7. **Develop a proposed improvement.**
   Use the diagnosis or specialist output to formulate the smallest general change
   supported by evidence. Do not encode the case's specific answer into the target skill.

   **Human gate:** present the proposed change, why it is preferred, trade-offs, viable
   alternatives, and an open path for the human's own solution. Do not modify the target
   skill until the human explicitly approves the change.

8. **Apply the approved change.**
   Make only the approved target-skill change. If implementation reveals a materially
   different change is needed, stop and return to the human gate instead of expanding
   scope silently.

9. **Re-run the same eval.**
   Hold the case and rubric fixed and use comparable run conditions.

   **Human gate before execution:** confirm the exact comparison being run.

10. **Check regressions and independence.**
    Run relevant previously passing cases and an independent case when practical.

    **Human gate:** present before/after evidence, regressions, remaining uncertainty, and
    a recommendation about whether to keep, revise, revert, or investigate further.

11. **Accept or continue.**
    Keep useful cases as regression coverage only after human approval. Record unresolved
    limits, rejected alternatives, and the next independent case when useful.

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
Capability under test:
Case and expected behavior:
Observed behavior:
Relevant output/trace evidence:
Known setup limitations:
Current failure hypothesis:
Human constraints or feedback relevant to diagnosis:
Question for the specialist methodology:
```

The specialist diagnoses the failure; it does not automatically edit the target skill.

## Output

Return:
- Target skill and capability.
- Current methodology stage and pending human gate.
- Case and run status.
- Evidence-backed diagnosis.
- Relevant learning concept and explanation depth used.
- Specialist methodology used, if any.
- Recommendation, alternatives considered, and human feedback that changed the plan.
- Targeted change proposed or made.
- Before/after result and regression status.
- Remaining uncertainty and next independent case.

## Decision rules

- Human-gated mode is the default.
- A failed eval is evidence to investigate, not an automatic prompt rewrite.
- Human feedback is not implicit approval.
- Specialist invocation is a recommendation until the human approves it.
- Target-skill edits require explicit approval in human-gated mode.
- A plausible final answer does not prove a file or tool was used.
- Preserve unsuccessful attempts and infrastructure failures.
- Hold the case and rubric fixed when comparing skill versions.
- Treat model or harness changes as possible regression triggers.
- Keep learning content outside the evaluated agent's context unless intentionally required.
- Prefer general behavioral rules over patches that merely solve the current eval case.

## Session-derived principles

This operational method synthesizes the AGNTCon/MCPCon sessions on real agent
evaluations, agent regression testing, EvalBench, shipping agent skills safely, context
engineering, verification, observability, and trust: evaluate realistic user journeys,
start mutating evals from known state, keep comparisons reproducible, treat skills like
versioned software, preserve human judgment at consequential methodology boundaries,
learn from concrete failures, and re-run coverage when the skill, model, harness, or
tools change.
