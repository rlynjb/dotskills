# Refine Skill — full staged workflow

This is the operational procedure for `refine-skill`. It preserves canonical
**Stages 0–11** and the conference-informed diagnosis workflow. Before initiating
any run or mutation, load [approval gates](approval-gates.md); for Stage 0 load
[structure validation](structure-validation.md); for Stages 2–4/9–10 load
[eval design](eval-design-guide.md); for Stage 6 load [methodology lenses](methodology-lenses.md).

## Scope and learning principle

Refine Skill accepts a raw prompt or an existing Agent Skill. Stage 0 validates
format and optionally proposes *minimal* normalization, not a wholesale rewrite.
Stages 1–11 teach the user to author evals, evaluate actual outputs, diagnose
causes, apply methodology lenses and improve behavior under approval gates.
Agent Skills is the source for format/eval **conventions**, while human gates
and specialist methodology are DotSkills extensions.

### Workflow trace — always visible

Keep the human oriented throughout the workflow, including stages that do not require
input.

Use the heading `Stage N — Step name` for every user-facing tutorial stage,
including stage openings, completion summaries, and resumed stages. Use the canonical
Procedure step number (0–11) and its step name below; do not renumber stages when
bootstrap is skipped, gates are batched, or an eval is repeated. Stage 0 is the structural check;
Stage 2 is case design; Stage 4 is grading. Explain Stage 0 briefly to beginners.

Under the heading, give the plain-English explanation and evidence. When the active
approval cadence requires a decision, put `HUMAN GATE — <specific decision>` on its
own line after that explanation, and state that the workflow is waiting. Otherwise
state `Status: Continuing`. Keep the stage heading separate from the approval label;
a heading or ordinary progress update is not itself a request for approval.
For a rerun or resumed discussion, retain the relevant stage number and identify the
iteration when useful rather than advancing the number just because a message was sent.

Example:

```text
Stage 2 — Design the eval case
Recommendation: use one synthetic change to check whether the review finds a known defect.
Explain the input, expected behavior, why this case matters, and how it will run safely.
HUMAN GATE — Approve or revise this case
Status: Waiting for approval
```

For every meaningful stage:
1. Announce the stage before beginning it, including its purpose and the immediate next
   action.
2. When the stage completes, report the concrete result, material finding or limitation,
   and the next stage.
3. Mark whether the workflow is continuing automatically or waiting at a `HUMAN GATE`.
4. Do not require a response to ordinary progress updates.
5. Do not expose private chain-of-thought, hidden reasoning, raw scratch work, or
   low-level tool chatter. Report only user-relevant state, evidence, decisions, and
   outcomes.
6. Keep updates concise enough to function as a usable execution trace rather than a
   transcript of every internal action.

A progress update is informational. A `HUMAN GATE` is blocking. If a stage contains
both, show the completed-stage result first, then present the gate that controls the next
action.

### Recommendation source labels — always visible

For every substantive recommendation, proposed behavior, diagnosis, specialist route, or
target-skill change, identify the basis using the applicable labels:

- **Methodology source:** use the exact conference-talk title when applying a
  conference-derived methodology principle. If multiple talks materially contribute,
  list each exact title. Do not substitute only the methodology skill name for the talk
  title.
- **Target-skill source:** name the target skill, reference, requirement, contract, or
  other domain material supplying task-specific guidance.
- **Eval / repository evidence:** name the case, run, trace, file, command result, or
  other observed evidence supporting a factual claim.
- **Model recommendation:** identify a choice, prioritization, or synthesis that the
  model is making rather than attributing it to a conference source or target skill.

A recommendation may use more than one label. Never imply that a conference talk
prescribed a specific eval case, diagnosis, or edit when that choice is model synthesis.
If the exact conference-talk title cannot be verified, mark the source title as
unverified rather than inventing one. Source labels are concise provenance summaries;
they do not expose private chain-of-thought.

Before making a methodology attribution, inspect the available source mapping,
relevant reference, or session notes and identify the specific principle it supports.
In a full DotSkills checkout, consult the methodology source table in skills/README.md
and relevant README/doc references when available. In an isolated installation, use
packaged sources or authorized retrieval; do not assume repository-only files exist.
A broad “session-derived principles” paragraph is not verification of an exact talk.

For each source label, add one plain-English sentence explaining its contribution:
- Target-skill source: what task requirement or behavior this source establishes.
- Eval / repository evidence: what was actually observed and where.
- Methodology source: which general evaluation principle the inspected source supports.
- Model recommendation: what the model chose or prioritized and why.

If provenance cannot be verified, say “Methodology attribution unverified” and name
the missing evidence and sources actually checked. Do not claim a search was performed
unless it was. Distinguish a title recorded in repository documentation from a claim
verified against original session material. Do not use “AGNTCon/MCPCon sessions” as a
substitute verified citation, or attach a known talk title solely because it sounds
relevant. Keep the proposed case or priority labeled Model recommendation when it is
model synthesis. If no methodology attribution is needed, say not applicable instead
of inventing one. Continue supported analysis unless the missing source is essential
to the decision; do not repeatedly ask for notes just to fill a label.

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

#### Beginner tutorial and case recommendations

When the human is new to evals or requests a tutorial, make Guided mode a hands-on,
plain-English tutorial. Do not assume unit-testing or eval experience. Explain an eval
as a structured check of whether an agent behaves as needed on a particular task.
Introduce terms when first needed: a case is one test situation; a baseline is the
starting result; a rubric is the checklist used to judge the result; a regression is
behavior that worked before but breaks after a change.

A stage title and source list alone do not satisfy the tutorial requirement.
Immediately below each stage heading, explain in plain English:
- **What we are doing:** the concrete activity and what we are not yet doing.
- **Why now:** the decision or uncertainty this stage resolves.
- **Example for this target:** a small illustration, labeled hypothetical if unobserved.
- **What this stage produces:** the artifact or decision the human will review.
Then give the recommendation and source explanations, followed by the existing gate.
Keep this compact; examples supplement evidence and never count as an executed eval.

At each stage, teach one small step before requesting a decision:
1. **What:** explain what we are doing in everyday language.
2. **Why:** explain what question this step answers and why it matters for this skill.
3. **How:** show the concrete input, proposed action, or evidence to inspect.
4. **Example:** use a small example tied to the actual target; label invented examples
   as hypothetical and do not assume missing target details.
5. **Your decision:** recommend the next bounded step and explain what approval allows.

Proactively recommend cases instead of asking the beginner to invent tests from scratch.
Inspect the target's intended behavior, requirements, and available failure evidence.
Offer one recommended first case and at most two useful alternatives, with a brief
reason for the priority. Prefer one observable behavior and a small synthetic fixture.
Consider normal behavior, a boundary/failure situation, missing information, and
unauthorized-action handling as coverage grows; do not require all cases at once.

For each proposed case, explain:
- the situation and exact neutral task/input the evaluated agent would receive;
- what good behavior looks like and which requirement establishes it;
- why this case is useful, what it tests, and what it cannot establish;
- how it would run safely using mocks or verified isolation;
- how to compare the output, attempted actions, and resulting state with expectations;
- what would count as Pass, Fail, or Unknown, with a short concrete example;
- the applicable recommendation source labels, distinguishing model-proposed cases
  from conference principles and observed evidence.

Show the learner the expectations and grading explanation, but keep them separate from
the evaluated agent's inputs. If essential context is missing, ask a focused question
or propose an explicitly provisional case; do not invent an authoritative answer key.
Obtain the existing case and execution approvals before running anything. A tutorial
request does not override the evaluation action boundary or authorize live actions.

After a run, walk through one actual observation against one expected behavior before
summarizing the grade. Explain whether the evidence points to the skill, the case,
the grader, or the environment, and why. Distinguish structural checks, hypothetical
walkthroughs, simulated runs, and observed agent runs; never present a teaching example
as executed evidence. Offer a gentle understanding check when useful, not a mandatory
quiz. Continue at the learner's pace and avoid dumping the whole methodology at once.

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
- Explicitly allowed and prohibited external effects; who authorizes each effect,
  and which host restrictions stop bypasses.
- Original output plus available read/search/tool/command evidence when a run exists.
- The current human-gate decision and any human feedback that constrains the next step.

Keep answer keys and grading criteria out of the evaluated agent's input.

## Procedure

0. **Validate Agent Skills structure; normalize only when needed.**

   Every Refine Skill invocation begins with a short check against the *minimum*
   [Agent Skills Quickstart](https://agentskills.io/skill-creation/quickstart)
   and [Specification](https://agentskills.io/specification) contract.
   Read [structure validation](structure-validation.md) for exact rules.

   - **Valid skill:** Check the package-root `SKILL.md`, YAML `name` and
     `description`, naming rules, and Markdown body. Report
     "Structure: valid — no changes needed." Advance to Stage 1 without
     reformatting, adding optional files, or revising guidance.
   - **Invalid/partial package or raw prompt:** Identify the precise missing
     requirements. Propose the smallest folder/`SKILL.md` conversion or repair.
     Preserve source material, intended behavior, tool/safety boundaries, and
     working references. Mark invented triggers or ambiguous semantics as
     proposed, not established.
   - **Human gate for any change:** Show a small tree and a readable new-file
     preview or diff. Wait for explicit approval before any create/move/rewrite.
     The human may supply alternatives or use a separate Skill Creator.
   - **After approval:** Apply only approved formatting changes. Run
     `skills-ref validate` if available and the existing DotSkills integrity
     check where appropriate; report exact commands/results or "Not Run".
     A format pass is not evidence of output quality. Move to Stage 1 only
     when valid or when an explicitly documented validation limitation is
     accepted by the human.

   `references/`, `scripts/`, `assets/`, and `evals/` are optional; no
   directory other than `SKILL.md` is required by the format. Do not
   turn Stage 0 into a complete skill-creation or content-redesign exercise.

1. **Frame the target and behavior.**
   Define one observable expected behavior for the target skill. For a new or newly
   bootstrapped skill, define the intended capability before optimizing its instructions.

   In beginner mode, explain that the target is the skill being evaluated, while the
   behavior is one observable thing we want it to do. Translate a broad goal into a
   focused statement before designing files, running a case, or assigning a grade.

   Hypothetical teaching example:
   - Broad goal: “Make Review Remote MR better.”
   - Focused behavior: “When the supplied mock MR context is missing a required diff,
     the reviewer identifies that gap and requests the needed information rather
     than inventing code-specific findings.”
   - Why start here: missing evidence can make every later conclusion unreliable.
     This priority is a model recommendation unless an inspected source prescribes it.
   - What we will inspect later: whether the response names the missing diff, requests
     it, and avoids unsupported findings. These are proposed observations, not results.
   - Stage 1 output: the target/version, one proposed behavior, why it matters,
     scope/exclusions, and an inventory of allowed vs. forbidden tool actions.
     Stage 2 will supply the concrete fixture and grading checklist.
   Adapt the example to the actual target and its established requirements; do not
   assume every skill needs an MR diff. Approval here selects the evaluation direction,
   not a live execution or an edit to the target skill.

   **Human gate:** present the target, behavior, recommendation, applicable source
   labels, alternatives, and an open feedback path. Obtain approval before finalizing
   the evaluation direction.

2. **Design the eval case.**
   Proactively recommend a first case using the tutorial and case-recommendation guidance
   above; explain the what, why, and how before asking the human to approve it.
   In Guided mode, coach the learner to draft two or three varied, realistic user
   prompts (including a boundary case), descriptions of expected outputs, and
   optional safe input fixtures. Record the approved definitions in the *target*
   skill's `evals/evals.json` using the Agent Skills guide's `skill_name` and
   `evals` fields; each case has `id`, `prompt`, `expected_output` and optional
   `files`. Ask the learner to try writing a case before supplying a worked
   example; offer assisted mode on request. Start with observable expectations
   and any non-negotiable safety criteria. Add or refine detailed `assertions`
   after inspecting the first outputs, as the official guide recommends.
   When the target has external tools or side effects, include security regression
   coverage for unauthorized actions, injected authority, indirect CLI/API bypass,
   and missing trace evidence as appropriate; require no real service writes.
   Validate the JSON structure, paths and evaluator isolation before execution.
   See [eval design](eval-design-guide.md). Do not encode the answer into the
   evaluated agent's task input.

   **Human gate:** present the proposed case and what it tests. Let the human approve,
   revise, replace, or contribute their own case before execution.

   Use this review checklist unless the active gate cadence explicitly batches it:
   - Is the behavior being tested clear and observable?
   - Is the task neutral rather than revealing the diagnosis?
   - Is the expected answer established by requirements, source evidence, execution,
     contract, or another reliable answer-key basis?
   - Does the expected answer match the context and tools the evaluated agent will
     actually receive?
   - Does the rubric grade essential meaning rather than exact wording?
   - Can a critical error fail the relevant criterion instead of being averaged away?
   - Is evaluator-only material isolated from the evaluated task context?

3. **Run the unchanged baseline and paired evaluation.**
   For the first iteration, run each approved case in clean contexts **with**
   the unchanged skill and **without** it when a no-skill comparison is
   meaningful. For skill revisions, compare the current version with a pinned
   **old_skill** snapshot. When the target began as a raw prompt, name its
   baseline explicitly (raw prompt or no skill). Use the same prompt, fixture,
   allowed environment and model/harness where comparable. A fresh session
   for each arm prevents leakage; do not share skill-specific instructions
   with the no-skill arm.
   Save outputs and available trace, errors, metadata, tokens and duration in
   separate per-iteration workspaces; see [eval design](eval-design-guide.md).
   Never claim a paired run happened when only one arm was executed.

   **Human gate before execution:** confirm the run configuration and that no hidden
   teaching or evaluator information will enter the task context.

   **MANDATORY Execution Safety Gate** (not a new numbered stage): load
   [execution-safety-gate.md](execution-safety-gate.md). Obtain case/run approval
   and independent host evidence of mock-only isolation, denied live credentials,
   network, shell/API and child-agent bypasses, restricted evaluator material,
   interposed tool authorization, and complete trace/state verification.
   When available, run `python3 scripts/refine_eval_safety.py preflight
   <host-manifest.json>`. `MANIFEST_VALID` alone is not proof of enforcement.
   If controls cannot actually be verified, do **not** launch: mark **Not Run**,
   document gaps, and continue with static analysis.

   Execution review checklist:
   - Are live write paths disabled and the mock/disposable environment verified?
   - Are allowed effects and any separately approved live exception recorded?
   - Are the exact target-skill and case versions identified?
   - Are model, harness, tools, permissions, and relevant budgets recorded?
   - Will the evaluated agent receive only agent-facing inputs?
   - Is the run fresh enough to avoid leakage from authoring or earlier answers?
   - Are answer keys, grading notes, private verification material, and prior outputs
     excluded?
   - Are intentional missing-context conditions distinguished from setup mistakes?

4. **Preserve and grade the evidence.**
   Preserve raw outputs, attempted tool actions, trace, configuration, errors and
   limitations for **both** arms. After the first round, coach the learner to
   write precise, observable `assertions` in `evals/evals.json`, as appropriate.
   The human-readable `expected_output` must exist *before* the first run;
   assertions drafted after seeing outputs must not silently favor one arm.
   Apply the same versioned rubric to both arms (regrade or rerun both after
   material edits). Prefer deterministic scripts for mechanical checks,
   calibrated LLM judgment for semantic checks and human review for
   subjective quality. Preserve concrete evidence per assertion in
   `grading.json`; record missing/unavailable evidence as Unknown in an
   explicit local extension or review note rather than inventing a PASS.
   Grade without forcing certainty: Pass, Fail, Unknown, Invalid, Error,
   or Incomplete are valid local outcomes.

   In Guided mode, explain grading before presenting the result:
   - **Expected behavior:** what should happen, defined before the run from verified
     requirements or answer-key evidence; it is not the run's generated answer.
   - **Actual result:** what the agent said and did during the run.
   - **Rubric:** the checklist that compares actual behavior with those expectations.
   - **Grade:** the judgment for each checklist item, supported by observed evidence.

   Show each criterion as: expected behavior, actual observation, evidence location,
   grade, and a plain-English reason. Explain what the learner should inspect, rather
   than only announcing a score. Grade meaning and behavior, not exact wording unless
   the task explicitly requires an exact format or value. Keep expectations and rubrics
   evaluator-only during execution, even when explaining them to the learner.

   Use this hypothetical illustration when helpful: a review correctly identifies a
   known defect but attempts to post to GitLab despite posting being prohibited. Finding
   the defect passes; avoiding unauthorized posting fails even if the write was blocked.
   If action evidence is missing, that action check is Unknown, not automatically Pass.
   A good answer does not cancel a failed action boundary. Do not present this illustration
   as an observed run or perform a live post to demonstrate it.

   Invite the learner to inspect three things: what was expected, what the evidence
   shows actually happened, and why that supports the grade. If they challenge the grade,
   inspect the evidence and rubric before assuming the skill needs changing.

   **Human gate:** show the evidence-backed grade, uncertainty, and what was observed.
   Let the human challenge the grade, add observations, or request more evidence before
   diagnosis proceeds.

   Result review checklist:
   - Were unauthorized actions attempted or performed, including through scripts or child agents?
   - Does the host evidence include every blocked/allowed call and verified
     unchanged external state, or must the security result be Unknown?
   - Did the agent answer the intended task?
   - Does the conclusion match the established answer-key evidence?
   - Does the explanation connect concrete evidence to the requirement or expected
     behavior?
   - Are any claims unsupported or outside the supplied evidence?
   - Are claims about files, tools, commands, or reads supported by trace evidence when
     that process claim matters?
   - Did the agent preserve uncertainty when decisive evidence was unavailable?
   - Was the run contaminated by answer-key material, hints, or prior results?
   - Did harness, tool, timeout, or setup failures materially affect the result?
   - Does the assigned grade actually follow from the rubric?
   - Would the same meaning receive the same grade if phrased differently?

5. **Diagnose before editing.**
   Ask **"What actually failed?"** before changing anything. Classify the evidence as one
   or more of:
   - case / answer-key problem;
   - grading / rubric problem;
   - missing, stale, conflicting, excessive, or otherwise bad context;
   - harness, tool, timeout, or environment problem;
   - model variability;
   - package / adapter structure problem;
   - observability or missing-trace problem;
   - trust, provenance, permission, approval, or governance problem;
   - actual target-skill guidance problem.

   A failed eval is not permission to edit. Only edit the target skill when the evidence
   supports that diagnosis or when the human explicitly approves a different bounded
   experiment.

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
   **Screen all five lenses every cycle**, recording relevant, not evidenced, or not applicable.
   **Do not invoke every specialist automatically.** Recommend a deep dive when observed
   evidence supports it, or when the human requests full-lens learning mode.
   Read [methodology lenses](methodology-lenses.md) before interpreting this scan.

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
   Use a new `iteration-N` workspace. Hold prompt, fixtures, expected output and
   the *versioned* assertions fixed across arms; use comparable conditions.
   If a broken assertion or answer key must change, record its revision and
   regrade/rerun both configurations before claiming an improvement.

   **Human gate before execution:** confirm the exact comparison being run.

10. **Check regressions and independence.**
    Run relevant previously passing cases and an independent case when practical.
    Compare evidence, assertion pass/fail outcomes, human feedback, timing and
    tokens. Save `benchmark.json` when both arms have comparable runs.
    Treat multiple runs as required for reliability/variance claims; do not
    invent averages or standard deviation for one attempt. A correct answer
    with an unauthorized attempted action still fails its safety criterion.
    Keep the GitLab write, indirect API/shell, and missing-evidence cases from
    Refine Skill's self-evals as regressions when relevant; do not interpret
    a mocked safety pass as proof about live connectors.

    **Human gate:** present before/after evidence, regressions, remaining uncertainty, and
    a recommendation about whether to keep, revise, revert, or investigate further.

11. **Accept or continue.**
    Keep useful cases as regression coverage only after human approval. Record unresolved
    limits, rejected alternatives, package-structure decisions, and the next independent
    case when useful.

## Output

Maintain a concise user-visible workflow trace during execution. At any point, the human
should be able to tell the current stage, the most recent completed result, whether the
workflow is continuing or blocked, and what comes next.

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
- Recommendation, its applicable source labels, alternatives considered, and human feedback that changed the plan.
- Targeted change proposed or made, including affected files.
- Before/after result and regression status.
- Remaining uncertainty and next independent case.

## Decision rules

- Human-gated per-gate mode is the default; batched and delegated/fast cadences require
  explicit opt-in and a clear authorization boundary.
- Keep the workflow trace visible at every meaningful stage, even when no human input is
  required.
- Label substantive recommendations by source; when a methodology recommendation is
  conference-derived, use the exact conference-talk title and keep model synthesis
  explicitly separate.
- Ordinary trace updates never imply approval is needed; only an explicit `HUMAN GATE`
  blocks progress.
- Trace workflow state and evidence, not private chain-of-thought or low-level internal
  reasoning.
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
