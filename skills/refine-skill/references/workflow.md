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

For every stage opening, progress update, completion or resumed stage, first show
the phase label from the **four-phase map below**, then the unchanged
canonical stage heading. The phase label is a navigation aid, not an
additional step or approval gate.

Use the heading `Stage N — Step name (P of 12)` for every user-facing
stage, including stage openings, progress updates, completion summaries and
resumed stages. `N` is the canonical Procedure number **0–11** and `P = N + 1`
is its one-based position in the **12-stage workflow**. For example,
`Stage 3 — Run paired baselines (4 of 12)` means the fourth stage is current,
not that four stages have been completed. Keep the stage title and progress
counter visible so learners never have to recalculate their position. Do not
renumber or advance the counter when Stage 0 is brief, a gate is batched, an
iteration repeats, or work resumes at an earlier stage. The position indicates
where the workflow is currently focused; it is **not a completion percentage**.
Stage 0 is the structural check; Stage 2 is case design; Stage 4 is grading.
Explain Stage 0 briefly to beginners.

Under the heading, give the plain-English explanation and evidence. When the active
approval cadence requires a decision, put `HUMAN GATE — <specific decision>` on its
own line after that explanation, and state that the workflow is waiting. Otherwise
state `Status: Continuing`. Keep the stage heading separate from the approval label;
a heading or ordinary progress update is not itself a request for approval.
For a rerun or resumed discussion, retain the relevant stage number and identify the
iteration when useful rather than advancing the number just because a message was sent.

Example:

```text
Phase 1 of 4 — Preparation
Stage 2 — Design the eval case (3 of 12)
Recommendation: use one synthetic change to check whether the review finds a known defect.
Explain the input, expected behavior, why this case matters, and how it will run safely.
HUMAN GATE — Approve or revise this case
Status: Waiting for approval
```

**Agent/tool and source trace (every stage):** After the plain-English
*what / why / next*, add a concise **Agent/tool** and **Sources** line
when walking through each stage. State the active coding harness
(Claude Code or Codex), then name any provider runner, grader, or
methodology specialist actually used; otherwise say **no separate tool
invoked**. Identify target files, local references and real run reports,
plus any verified external documentation or service consulted. Label
resources that are merely *available* as such, not as accessed.
Differentiate **prepared / planned / blocked** from **actually invoked**.
Stage 2's dispatcher prepares files without running a model; Stages 3
and 9 conditionally invoke the selected provider after authorization and
independent isolation; Stage 4 reads grades that may already have been
produced in Stage 3; Stage 10 does not assume a new automatic comparator.
Stage 6 reviews five local lenses but invokes a specialist only after
the existing approval gate. See the per-stage
[agent/tool/source map](../README.md#agent-tool-and-source-map).
This trace is for clarity, not authorization to trigger tools or fetch
external data.

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

### Four-phase map — progress orientation

Group the 12 existing stages into **four phases** to reduce cognitive load.
Show the applicable phase **before** the stage heading; don't change the
Stage 0–11 numbering, existing human gates, ordering or run restrictions.

| Phase | Stages | What the learner is doing |
| --- | --- | --- |
| **Phase 1 of 4 — Preparation** | **0–2** | Validate the skill, choose one observable behavior, and design safe eval cases and fixtures. |
| **Phase 2 of 4 — Evaluation** | **3–4** | Run approved paired comparisons in a verified safe host (or mark Not Run), then grade the collected evidence. |
| **Phase 3 of 4 — Diagnosis & improvement** | **5–8** | Diagnose the failure, screen methodology in Stage 6, propose a small fix, and apply only approved changes. |
| **Phase 4 of 4 — Verification & decision** | **9–11** | Rerun comparable cases, check regressions and independent evidence, then make a human keep/revise/revert decision. |

**Methodology distinction:** Stage 6 is **one shared methodology review
stage**, not a separate stage for each methodology skill. It briefly
screens all five lenses (context, correctness, observability, trust and
lifecycle), marks relevance based on observed evidence, and recommends
at most a justified deep dive. Do not automatically invoke all five
specialists; specialist execution still requires the existing human
gate. A user-selected full-lens learning mode does not add stages.

Sample progress:

```text
Phase 2 of 4 — Evaluation
Stage 3 — Run paired baselines (4 of 12)
What we're doing: run the same approved case in clean contexts with and
without the skill (or compare against a pinned old version).
Why: measure the skill's contribution, not just whether one answer looks good.
Next: only launch after approved, verified mock-only isolation; collect
outputs for Stage 4 grading. Otherwise report Not Run.
Status: Waiting for approval
```

The phase and stage numbers reflect **current focus**, not percent done;
if an iteration revisits an earlier stage, update both labels to match.

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

#### Stage-by-stage plain-English walkthroughs (Guided Mode)

Use these as **teaching prompts**, not text to recite mechanically. At the start of
**every Stage 0–11**, before presenting technical plans or source labels, briefly
answer **What are we doing? Why does it matter? Example for this target?
What happens next?** Explain unfamiliar terms on first use. Tailor the
illustration to the selected target skill and actual case; the Learn Repo examples
below are **hypothetical**, not evidence of completed runs. Keep each stage
introduction short, then show its real evidence, next bounded action and any
required human gate. Do not say a run, edit, approval or grade happened unless
there is evidence that it did.

- **Stage 0 — Validate structure.**
  **What:** Check the skill package's required format.
  **Why:** A valid skill needs no formatting changes.
  **Example:** Learn Repo has a valid `SKILL.md` with name and description.
  **Next:** Report validation, or seek approval for only the necessary repair.
- **Stage 1 — Frame one observable behavior.**
  **What:** Choose one thing the target skill should demonstrably do.
  **Why:** A focused goal gives the eval a clear purpose.
  **Example:** Learn Repo should identify the important modules in a supplied
  repository and ground its explanation in the provided files.
  **Next:** Confirm intended behavior, scope and prohibited actions.
- **Stage 2 — Design and write eval cases.**
  **What:** Write a realistic prompt, expected behavior and safe input fixture.
  **Why:** We need a reproducible test before evaluating the agent.
  **Example:** Supply an invented Python CLI repository such as `parcel-queue`;
  describe success in `expected_output` and approve testable `assertions`
  before native case preparation. An after-run rubric change is a new
  approved version, never a silent adjustment.
  **Next:** Review and approve the case, rubric and fixture; no model has run.
- **Stage 3 — Run paired baselines.**
  **What:** Perform the same case in separate fresh contexts, once **with the
  unchanged skill** and once **without the skill** (or against a pinned older
  version). A *baseline* is the comparison starting result; *paired* means
  matched test conditions.
  **Why:** See what difference the skill makes, not just whether one answer
  sounds good.
  **Example:** Give the same `parcel-queue` prompt and fixture to Learn Repo
  with its instructions and to a no-skill agent; capture both outputs and
  attempted tool actions. This pair is an **experiment, not an assertion**.
  **Next:** Confirm the selected provider's native tooling, scoped run and
  provider approvals, and the mock-only Execution Safety Gate. Otherwise mark
  **Not Run**. Stage 4 reviews the grades and real evidence from the run.
- **Stage 4 — Grade actual outputs.**
  **What:** Compare observed outputs/actions against the expected behavior
  using testable *assertions* (individual checks).
  **Why:** Evidence-backed Pass, Fail or Unknown is more useful than a feeling.
  **Example:** Check whether both first-party modules were identified using
  supplied file evidence; grade both paired arms with the same rubric.
  **Next:** Show evidence and uncertainties for human review before diagnosis.
- **Stage 5 — Diagnose before editing.**
  **What:** Find the reason for a failed or uncertain check.
  **Why:** A bad fixture or missing tool trace is not necessarily a bad skill.
  **Example:** An absent module in the output may reflect omitted fixture
  files rather than weak Learn Repo instructions.
  **Next:** Classify the likely failure source before proposing changes.
- **Stage 6 — Screen methodology lenses.**
  **What:** Check context, correctness, observability, trust and lifecycle.
  **Why:** A single failure may reflect a broader system issue.
  **Example:** Missing tool traces suggest an observability gap, while an
  unauthorized write attempt raises a trust/permission concern.
  **Next:** Recommend a specialist deep dive only if justified and approved.
- **Stage 7 — Propose the smallest improvement.**
  **What:** Draft a targeted change, without editing yet.
  **Why:** General improvements are preferable to memorizing one test answer.
  **Example:** Propose clearer file-evidence instructions rather than inserting
  `parcel-queue` module names into Learn Repo.
  **Next:** Show trade-offs and exact files; wait for edit approval.
- **Stage 8 — Apply the approved change.**
  **What:** Make only the accepted edits.
  **Why:** Keep the experiment's intervention small and auditable.
  **Example:** Update a specific Learn Repo instruction and record its diff.
  **Next:** Preserve version evidence and prepare a comparable rerun.
- **Stage 9 — Rerun approved evaluations.**
  **What:** Rerun the case we tried to fix **and relevant previously passing
  cases**, each with its original approved prompt and grading rules.
  **Why:** See whether the fix helped without breaking an old behavior.
  **Example:** Reuse the `parcel-queue` architecture case, plus an approved
  case that checks whether Learn Repo pauses at a learning checkpoint.
  **Next:** Approve the exact rerun scope and pass the execution safety gate
  again, or mark **Not Run**.
- **Stage 10 — Check regression and independence.**
  **What:** Compare new evidence with earlier results to see whether any
  behavior that passed before now fails (a *regression*).
  **Why:** Improving one case can conceal new failures.
  **Example:** An architecture explanation now passes, but the approved
  checkpoint-pausing case that used to pass fails: that is a regression.
  If no comparable prior result exists, say so rather than claiming failure.
  **Next:** Present before/after evidence, safety outcomes and limitations.
- **Stage 11 — Human decides.**
  **What:** Choose to keep, revise, revert, release or iterate.
  **Why:** A test result informs a decision; it does not make it automatically.
  **Example:** Keep a Learn Repo improvement only after reviewing the
  comparable grades and any regressions.
  **Next:** Record the decision and preserve cases, rubrics and evidence for
  future changes. Explain that future regression reruns require fresh scope,
  approval and safety verification; accepting a skill never authorizes an
  unattended external model evaluation.

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

### Resume an existing evaluation without rebuilding it

A new invocation still performs the **brief Stage 0 structure check**.
Before Stage 1/2 case planning, inspect the **currently accessible**
target skill and any already-persisted `evals/evals.json`, referenced
fixture paths, run outputs, version metadata, and recorded human decisions.
Do not infer persistence just because an earlier chat reported creation;
confirm the artifacts in the current workspace.

- **Reuse by default:** If an approved case and its synthetic fixture
  already exist and are usable, preserve them exactly. Do not repeat
  case generation or regenerate/overwrite/delete/move files just because
  the user reopened Refine Skill or changed harnesses. Verify references,
  expected behavior and revision; read only what is needed to orient
  and complete the next stage.
- **Resume from evidence, not a guess:** Use saved case/run data to name
  the last **confirmed** completed stage and next unfinished one.
  Example: a valid `evals/evals.json` plus fixture, but **no** model-run
  outputs, means Stage 3 is next **only if** the case also has approved
  assertions and the provider-native case has been prepared. Otherwise
  finish Stage 2 preparation first. Do **not** claim Stage 3 executed.
  An absent or incomplete run stays Not Run/Unknown rather than a pass.
  When the stage is ambiguous, explain the evidence and ask a targeted
  question rather than silently resetting the workflow.
- **Existing-eval choices:** When an accessible saved case exists and
  the learner needs a next action, present **Continue Eval** (default:
  resume from evidence), **New Run** (same case and fixture; fresh
  isolated outputs), or **Reset Eval** (new case/fixture version).
  Explain that these are distinct choices: a new run is **not** a new
  test case, and Reset Eval is **not** a destructive delete command.
- **Reset Eval (on explicit request only):** Treat this as a new Stage 2
  design iteration, not a new numbered stage. Before any write, identify
  exactly which case or suite is being reset, the old case/fixture
  paths, any previous outputs, the new version/path, and the expected
  effect on comparisons. Show a short preservation/archival plan and a
  precise **HUMAN GATE — Approve Reset Eval**. A request to *show or
  include* the option is not approval to execute a reset.
  After approval, preserve old `evals.json` case definitions,
  assertions, fixtures and run outputs as immutable historical evidence;
  write newly generated cases/fixtures to a separate versioned path
  and update only the approved references after verifying the archive.
  If safe preservation or unique path allocation cannot be ensured,
  stop and report the blocker rather than overwriting anything. Recheck
  the new case's expected behavior and obtain its Stage 2 approval
  before any new Stage 3 execution or safety gate.
- **No destructive reset by default:** For changed requirements, broken
  fixtures, missing referenced paths, or a desired fresh start, first
  show what would change, the evidence for it, and alternatives.
  Seek explicit approval before creating replacements, regenerating,
  overwriting or deleting any existing case, fixture or run artifacts.
  Preserve prior versions and evaluator-only information.
- **Fresh execution still needs fresh safeguards:** Reuse the *case*,
  not old run authorization. Before every evaluated-agent run, obtain
  the scoped human run approval and independently verified mock-only
  Execution Safety Gate. Put newly produced outputs into a **new**
  iteration workspace rather than overwriting an old iteration.
- **Cross-harness limitation:** Reuse works only if the files are
  accessible in that workspace or explicitly retrieved. If unavailable,
  report that limitation instead of inventing saved artifacts or results.
  Reuse usually avoids tokens spent **regenerating** fixtures; it does
  not make fixture-reading or execution context free.

Explain the resume decision in the same four-phase/stage navigation
format, e.g. `Phase 2 of 4 — Evaluation` and
`Stage 3 — Run paired baselines (4 of 12)`, with a clear `Not Run`
status and a pending case/run gate where applicable. Do not restart
stages solely to produce a new counter, and do not treat this policy as
permission to skip analysis when requirements have actually changed.

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
   and any non-negotiable safety criteria. **Draft and approve detailed
   `assertions` before native case preparation**; the dispatcher uses them
   to generate provider-specific grading definitions. Revisit assertions
   after observed outputs only as a new approved rubric revision, applied
   fairly to both arms. When the target has external tools or side effects,
   include security regression
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
   In Guided Mode, first explain that this is a controlled comparison experiment:
   the same case runs with and without the skill (or with an old snapshot), so
   we can see the skill's added effect. This pair is **not an assertion**;
   assertions are individual criteria used to grade the two outputs in Stage 4.
   Explicitly distinguish the proposed run from an executed run, and explain
   that evidence collection is not yet a score.
   For the first iteration, run each approved case in clean contexts **with**
   the unchanged skill and **without** it when a no-skill comparison is
   meaningful. For skill revisions, a pinned **old_skill** snapshot may be
   compared through a **separately configured and approved** provider-native
   setup; the current dispatcher only prepares with-skill/without-skill
   pairs. When the target began as a raw prompt, name its baseline
   explicitly (raw prompt or no skill). Use the same prompt, fixture,
   allowed environment and model/harness where comparable. A fresh session
   for each arm prevents leakage; do not share skill-specific instructions
   with the no-skill arm.
   Before presenting a launch option, follow the
   [provider-native evaluation integration](eval-runner-integration.md).
   Detect and independently verify the active harness. For **Claude Code**,
   prepare Claude plugin-eval cases and use Claude's paired execution and
   `type: llm` graders. For **Codex**, prepare Promptfoo cases using
   `openai:codex-sdk` as both execution and `llm-rubric` grading provider.
   These are distinct tools and result formats; **never mix providers**.
   Confirm the selected native tooling and its actual supported flags
   in the independently verified host. The provider's CLI, an evaluator
   prompt, prepared fixture or configuration file is **not** a safety sandbox.
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
   **Blocking rule:** If the runner is absent/unconfigured, scoped approval is
   absent, isolation is not independently verified, or the required traces
   cannot be captured, **stop the refinement workflow at Stage 3**. Record
   **Blocked — Not Run**, identify the exact missing prerequisite, and preserve
   the case, fixture, stage and any prior evidence for later resumption.
   Present a runner-setup/safety-remediation path and wait there. Do **not**
   auto-advance through Stages 4–11, produce speculative skill edits,
   or report a completed behavioral evaluation. A separate optional **static
   review** can be offered, but must be labeled non-behavioral and must not
   advance the numbered evaluation stages. If the host later becomes ready,
   require a fresh scoped run approval and execution safety check.

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

4. **Preserve and review actual grades and evidence.**
   Stage 2 already recorded and approved `assertions` in `evals/evals.json`
   and prepared the active provider's grader definitions. Preserve actual
   outputs, attempted tool actions, host traces, configuration, errors,
   and limits for **both** arms. Stage 4 examines the **native grades and
   observed evidence** produced by the run; it does not automatically call
   a second grader. Use Claude plugin-eval `type: llm` graders **only**
   for Claude, and Promptfoo `llm-rubric` with the Codex SDK **only**
   for Codex. Do not mix grader instructions, reports or result schemas.
   If evidence reveals a rubric defect, propose a new approved rubric
   revision and rerun/regrade **both** arms fairly; keep earlier results.
   Prefer deterministic checks for mechanical properties and human review
   of subjective quality. An LLM grading output does **not** prove that
   no unauthorized tool attempt occurred. Keep the provider's native
   results alongside independent host-action/state traces. Do not
   promise a generic `grading.json` or invent a missing score.
   Record Unknown/Invalid/Error/Incomplete/Not Run and the limitation
   explicitly, without fabricating PASS. A local teaching pass rate
   (`passed / (passed + failed)`, where the denominator is nonzero)
   is optional and **not** a provider-native schema. Missing safety
   evidence makes the case provisional; never declare an overall Pass
   with failed or unresolved must-pass correctness/safety checks. No
   universal weighting formula or cutoff applies; define any task-specific
   threshold before comparison and explain it to the learner.

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
   This is **one Stage 6 for all five methodology lenses**, not five separate
   stages. A specialist deep dive is optional, evidence-driven and human-gated.

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

9. **Re-run approved evaluations.**
   Include the targeted case and relevant previously passing cases as
   regression coverage when explicitly approved. Reuse each case's original
   versioned prompt, fixture and grading rules; new or revised cases must
   return to Stage 2 for approval. Prepare a **new unique native bundle**
   for each selected provider-native evaluation;
   do not overwrite earlier evidence or presume an `iteration-N` folder
   exists. Hold prompt, fixtures, expected output and the *versioned*
   assertions fixed across arms and use comparable conditions. If a
   rubric/answer key must change, approve and record its revision, then
   rerun both arms using that same revision before claiming improvement.

   **Human gate before execution:** confirm the exact case set and
   comparison being run, and independently verify isolation for every run.

10. **Check regressions and independence.**
    Review previously passing cases rerun under the Stage 9 execution gate,
    plus an approved independent case when practical; do not launch model
    evaluations in this review stage without the Stage 9 approval and safety
    checks. For verified comparable paired outputs, use the current provider's
    supported result and comparison features only. Preserve Claude's
    evaluation reports or Promptfoo's Codex results **without inventing
    a shared score format**. An optional provider-specific viewer or
    comparator is only an observed result if it actually ran.
    No model judgment can override a failed safety requirement.
    Compare evidence, assertion outcomes, human feedback, timing and
    tokens. Save provider-native benchmark artifacts where supported.
    Treat multiple runs as required for reliability/variance claims; do not
    invent averages or standard deviation for one attempt. A correct answer
    with an unauthorized attempted action still fails its safety criterion.
    Keep the GitLab write, indirect API/shell, and missing-evidence cases from
    Refine Skill's self-evals as regressions when relevant; do not interpret
    a mocked safety pass as proof about live connectors.

    **Human gate:** present before/after evidence, regressions, remaining uncertainty, and
    a recommendation about whether to keep, revise, revert, or investigate further.

11. **Accept or continue.**
    Keep useful cases as regression coverage only after human approval. Preserve
    versioned cases, rubrics and reports so future skill, model, or harness
    updates can be checked against previously working behavior. Explain that
    continuous regression testing is reuse across future changes, **not a
    new stage or automatic authorization** for live model runs; each later
    evaluated-agent execution still needs scoped approval and verified
    isolation. Record unresolved limits, rejected alternatives, package-structure
    decisions, and the next independent case when useful.

## Output

Maintain a concise user-visible workflow trace during execution. At any point, the human
should be able to tell the current stage, the most recent completed result, whether the
workflow is continuing or blocked, and what comes next.

Return:
- Target skill/capability and current maturity.
- Bootstrap / normalization status and approved package changes, if any.
- Current phase (X of 4), methodology stage, one-based stage position (P of 12), and pending human gate.
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
