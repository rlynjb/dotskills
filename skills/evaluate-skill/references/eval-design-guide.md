# Evaluate Skill — learn to design, run and grade evaluations

Primary guide: [AgentSkills.io: Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills).
Evaluate Skill uses skill-local `evals/evals.json` as an authoring convention
and converts approved cases into **provider-native formats** via
[`native_eval.py`](../runner/native_eval.py). The Agent Skills guide's
`grading.json`, `timing.json`, and `benchmark.json` are example
conventions, **not required outputs** of the current dispatcher or
requirements of the core Agent Skills specification. Claude and Codex
retain their distinct result schemas.

## Stage 2 — automatically draft cases, then teach through review

**In plain English:** The active coding agent drafts the first version of
exam questions and the answer-checking checklist. A beginner can review
concrete examples instead of inventing every test from a blank page.

**Why we do this:** It helps the learner understand what a fair, measurable
test looks like while keeping the learner responsible for approving it.

**How it works:** Based on the approved Stage 1 behavior and the target
skill's documented requirements, the agent **proposes** two or three
realistic prompts, expected outcomes, testable `assertions`, and optional
synthetic fixture plans. Include a boundary or missing-context case.
Explain each case's purpose, expected evidence and any assumptions;
do not present guessed requirements as established facts.

**Hypothetical Learn Repo example:** Draft one case testing whether the
skill identifies real repository modules with evidence and another testing
whether it pauses at the agreed learning checkpoint. Show what would count
as Pass, Fail or Unknown. These are proposals, not observed outcomes.

**Human gate:** Present the drafts for review, revision, replacement or
approval. Do **not** save or overwrite cases/fixtures or call the local
preparer before approval. Once approved, save cases to the target skill's
`evals/evals.json` and prepare provider-specific grader definitions.
Drafting and local preparation do **not** run an evaluated agent or an
LLM grader; Stage 3 still requires separate approval and verified isolation.
The learner may write their own cases instead.

For approved cases, use this shape in the **target skill's** `evals/evals.json`:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "A realistic task a user would actually type",
      "expected_output": "An observable description of a correct result",
      "files": ["evals/files/fixture.txt"],
      "assertions": ["The result addresses the expected behavior using supported evidence"]
    },
    {
      "id": 2,
      "prompt": "A realistic boundary or ambiguous request",
      "expected_output": "Correct handling of the boundary and uncertainty",
      "assertions": ["The response explains the boundary without inventing missing facts"]
    }
  ]
}
```

Use actual files only when needed, stored under `evals/files/` or a
clearly documented skill-relative fixture path. `files` paths resolve
relative to the target skill root for the authoring convention. Use `id`
(unique integer), `prompt`, `expected_output`, optional `files`, and
`assertions` (array of observable strings). The general Agent Skills
example may omit assertions, but **the current native preparer requires
approved nonempty assertions before `prepare` can succeed**, so provide
them for any case intended for Claude/Codex model grading. This is a
dispatcher constraint, not a new core Agent Skills specification rule.

**Fixture-path contract (implemented and offline-tested):**
`native_eval.py` now resolves every `files` entry relative to the
**target skill root**, matching `scripts/validate_evals.py`. For a suite at
`<skill>/evals/evals.json`, the approved path
`evals/files/fixture.txt` refers to
`<skill>/evals/files/fixture.txt`. The path is preserved when staged
under Claude's case `fixtures/` or Codex's paired `inputs/`.
The dispatcher validates all fixtures before creating output, denies
absolute/traversal paths, missing files and symlinked path components,
and rejects suites outside the target skill. Offline tests cover both
harness paths; **provider-native live execution remains unverified**.

Validate the authoring suite locally:

```bash
python3 scripts/validate_evals.py skills/<target-skill>/evals/evals.json
# or validate any skill-local suites in DotSkills:
python3 scripts/validate_evals.py --all
```

### Self-documenting evaluation fixtures (recommended)

Prefer descriptive folder and file names that identify what a fixture
contains and how it is used; avoid ambiguous names such as `history/`
when the files specifically contain Git history. For example, use
`evals/files/parcel-queue/git-history-exports/` for saved Git log/diff
files rather than implying access to a live `.git/` directory. When
those files are invented for the test, identify them as **synthetic**
(e.g. `synthetic-git-history/` or a fixture README stating that the
export-style logs and diffs are generated examples). An exported
snapshot is evidence supplied as files, not proof that live Git
metadata or Git commands are available.

Document provenance when it matters: whether a fixture is synthetic or
an export from a real repository, and any relevant limitations. Keep
fixture names readable and `files` references accurate if paths change.
These are **recommended naming conventions**, not Agent Skills format
requirements or new validation rules. Never include secrets or grader
answers in agent-readable fixture files.

The case author/coordinator can read the expected answer. **The
evaluated agent must not access `evals.json` or any grader/answer-key
documents**. Stage only the task, approved fixture inputs and the
runtime skill into an isolated workspace. Directory separation alone
is not an access restriction. If a harness cannot enforce isolation,
mark the run **Not Run** and provide only a static review.

Write expected behavior *before* the first run. **For this provider-native
workflow, teach and approve testable `assertions` before Stage 2
preparation** so the Claude grader files or Codex rubric can be generated.
A human may refine assertions after reviewing real outputs, but that is
a **new rubric revision** requiring approval and comparable re-evaluation
of both arms. Predeclare must-pass safety boundaries; never change
criteria only for the with-skill arm.

### Reuse existing cases and fixtures on resumed runs

Before authoring or generating a new case, check whether the target
skill already has an accessible, approved `evals/evals.json` and the
fixture files identified in its `files` entries. Validate that
references resolve and the saved scenario still matches the intended
behavior. If so, use the **same versioned case and synthetic fixture**
rather than regenerating them. A synthetic repository is an input to a
test, not a disposable byproduct that must be recreated whenever a
session restarts.

If case/fixture files are absent, damaged, incompatible or unavailable
in the current harness, report the specific gap. Seek explicit approval
for any new or replacement case/fixture; do not silently overwrite or
delete work. Verify the last completed stage from saved evidence and
keep previous run iterations unchanged. With an approved existing case
and **no** evaluated-agent output, confirm that approved assertions and
a matching native case are prepared before starting Stage 3 **pending**
execution approval and host safety verification. If assertions are
missing, complete Stage 2 preparation first; do not claim an evaluation
took place. Reusing fixtures can reduce prompt-generation
work and token usage, but supplying them to an evaluated agent still
costs context and tokens.

### Reset Eval — optional fresh case and fixture

**Reset Eval** means intentionally starting a **new version of a test case
and its synthetic fixture**, not simply running the existing test again.
Make the choice explicit when revisiting an existing evaluation:

- **Continue Eval** (default): reuse the approved case and fixture, and
  resume from the last confirmed step.
- **New Run**: use the same approved case/fixture but save new observed
  outputs in an unused, isolated iteration/run directory.
- **Reset Eval**: return to Stage 2 to design a replacement case/fixture
  **version**. Do not automatically delete, overwrite or mutate the
  original inputs and prior outputs.

For Reset Eval, first show the exact case ID or suite scope, existing
paths, planned archive/versioned destination, and which references
would change. **Wait at HUMAN GATE — Approve Reset Eval** before
generating or writing anything. Keep an immutable copy of the original
case definition (including its expected output and assertions), its
fixture files, and past run evidence; record the prior version/revision
so later comparisons don't mix old and new test inputs. Use distinct
versioned fixture paths and ensure a fresh filename/directory is
available before writing, especially when multiple harnesses share the
same repository. If the preservation or destination can't be verified,
do not perform the reset. Validate the new case and request normal
case approval; any actual agent run still needs the separate Stage 3
approval and verified execution safety gate.

**A different fixture is a different test.** Do not treat scores for
the old and reset case as directly comparable evidence of an
improvement unless differences are explicitly accounted for.

## Stage 3 — reproducible paired runs

**Plain-English explanation (Guided Mode):** A *baseline* is the starting
result used for comparison, and *paired* means two matched runs of the same
case. This is a **comparison experiment, not an assertion**. For example,
with the same synthetic Python repository and prompt, one agent uses the
unchanged Learn Repo skill while another runs without that skill. Keep the
inputs and allowed environment comparable, and collect both outputs and
attempted actions. **Stage 2 preapproves assertions for provider-native
graders; Stage 3 executes and gathers evidence; Stage 4 reviews the real
grading and host evidence** (a native eval may execute and grade in one
invocation). The example describes a proposal, not an observed run.

**Execution prerequisite:** Verify the **active provider's** evaluation
tooling (see [native integration](eval-runner-integration.md) and
[runner guide](../runner/README.md)), approved case and rubric, scoped run
and provider approvals, and independent host-enforced mock-only isolation
**before** attempting either arm. Claude uses `claude plugin eval`;
Codex uses Promptfoo with `openai:codex-sdk`. Never fall back to the
other provider. If unavailable, mark **Blocked — Not Run** at Stage 3;
fixture validation alone cannot justify grading or diagnosis.

For each case, run comparable provider-native configurations:
- `with_skill` — the current unchanged skill package.
- `without_skill` — no skill, for measuring added value.
- A pinned `old_skill` comparison is a **separate, explicitly configured
  comparison**, not something the current dispatcher automatically stages.
Do not assert that a provider performed either comparison without actual
run artifacts.

Keep prompts, input files, model/harness, tool capabilities and budgets
as comparable as possible; identify necessary differences. Before any
run, apply the mandatory [Execution Safety Gate](execution-safety-gate.md):
a separate human approval for the case and an independently verified
host-enforced mock-only environment with deny-by-default per-call
authorization and trustworthy action/state traces. A self-declared
policy manifest or a dry-run prompt is not physical isolation. Do not run
a target skill's end-user job against live GitHub, email, deployment,
production databases, or other real write-capable services without
separate bounded authorization and verified controls. Use mocks,
record attempted actions, and stop if isolation cannot be proved.

Preparation saves a **unique, usually gitignored** bundle under
`eval-workspaces/`: either `claude-native-<case>-<id>/plugin/`
(with `evals/<case>/prompt.md` and `graders/`) **or**
`codex-native-<case>-<id>/codex/promptfooconfig.yaml` (with
`with_skill/` and `without_skill/` workspaces). Both include a
`manifest.json` marked `PREPARED_NOT_RUN` until a verified run
actually occurs. **Do not** expect generic per-arm `grading.json` or
`timing.json`, or `benchmark.json`, from this dispatcher. Provider
reports such as `claude-results.json` or `codex-results.json`
are only meaningful when actually written after an approved run.

Preserve provider-native results and trusted host-action traces separately.
Record the source SHA, case/rubric revision, harness/model, permissions,
raw responses, available usage/timing, errors and uncertainty. Do not
invent measurements; never overwrite prior saved cases or iterations.

## Stage 4 — review native grades and underlying evidence

Stage 2 already records and approves the `assertions` that generate
provider-native graders. Stage 4 **inspects observed outputs and
actual provider-generated grades**, not a mandatory second grader
invocation. Coach the learner to challenge incorrect or incomplete
assertions against evidence. If a rubric needs revision, record a
new, approved version and re-evaluate both paired arms fairly.
For example, a Stage 2 assertion list could be:

```json
"assertions": [
  "The review identifies the specific reachable invalid write when evidence supports it",
  "The response does not invent code-specific defects when the evidence is insufficient",
  "No unauthorized write is attempted"
]
```

Grade each assertion against actual output, attempted actions and
state, with cited evidence. For external-action security cases, treat
an unauthorized *attempt* as FAIL even if a mock host blocked it.
Missing attempt traces or state verification mean Unknown, not Pass.
Deterministic scripts can verify mechanical properties; the selected
provider's native LLM grading evaluates semantics. For Claude that means
plugin-eval `type: llm` graders; for Codex, Promptfoo `llm-rubric`
with the Codex SDK. Their **native output formats are separate**.
Do not require `grading.json` or presume an `assertion_results`
array. Review the provider's actual artifacts alongside trusted host
attempt/state evidence and human judgment. For **Unknown**, **Invalid**
or **Incomplete** runs, record uncertainty explicitly instead of
inventing a boolean PASS/FAIL. Do not treat the LLM's text-only judgment
as proof that a prohibited tool action did not occur.

### Default scoring rubric — assertion grades before aggregate scores

Use this **evidence-first, unweighted teaching convention** when explaining
judgments alongside provider-native evidence. It is **not a requirement
or output schema** of Claude plugin eval, Promptfoo, or Agent Skills.

| Grade | When to assign it | How to record it |
| --- | --- | --- |
| **Pass** | Concrete output, action and/or state evidence satisfies the observable assertion. | Record native provider result and supporting evidence in the review. |
| **Fail** | Complete evidence contradicts the assertion or a required result is absent; attempted unauthorized action fails even if blocked. | Preserve provider result plus trusted host-action evidence. |
| **Unknown** | Required trace, state verification or other evidence is unavailable. | Explicit evaluator-only review/status note; **not** a fabricated success. |
| **Invalid / Error / Incomplete / Not Run** | Answer-key contamination, setup failure or incomplete/no execution. | Separate run status; exclude from confirmed scored results. |

For teaching or a **separate clearly labeled local review**, count actual
graded Pass and Fail assertions, then (only if useful) calculate
`pass_rate = passed / (passed + failed)`; the rate is unavailable when
no graded assertions exist. Report all ungraded/Unknown criteria and any
critical criterion separately. Such a calculation is **not** the official
schema or a substituted score for the selected provider's native report.
If important evidence is missing, mark the review **provisional**.

**Must-pass gates are separate from the average.** Establish critical
correctness/permission/safety criteria before execution. One failed
must-pass criterion makes the case **Fail**, even if the other assertions
give a high pass rate; an Unknown critical criterion leaves the case
**Unresolved**, not Pass. Without a predeclared case acceptance rule,
report the assertion grades and rate without inventing an overall Pass
threshold. There is **no universal industry weight or cutoff** (such as
80%); only introduce task-specific weights, numerical score ranges,
thresholds or anchored subjective rubrics when their meaning is stated
and justified *before* a scored comparison. They never override a
required safety check.

**Hypothetical teaching example (not an executed eval):** a code-review
case passes "identifies the real defect" and "cites supporting evidence",
but fails "makes no unauthorized write attempt". Thus `passed = 2`,
`failed = 1`, `total = 3`, `pass_rate = 2/3 ≈ 0.667` (66.7%).
**Case outcome: Fail** because the safety gate failed. Show the evidence
for each judgment before showing this aggregate.

For semantic or subjective checks, define explicit rubric anchors and
review example judgments with a human to **calibrate LLM-as-judge**;
record disagreement and avoid trusting an unexplained numeric rating.
[OpenAI's evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices)
recommend clear rubrics, human calibration, and pass/fail criteria
alongside optional numeric scores. Compare matching runs **within the
selected provider** using the same approved case/rubric version. Preserve
the provider's native reports. An additional explanatory comparison may
show actual graded counts, evidence coverage, and critical-gate failures;
if calculating arm-to-arm rate differences, use **percentage points**
rather than relative percent. Compute variance only from genuine
repeated runs, not one trial.

A changed assertion set creates a new grading revision; apply it
symmetrically to both arms and keep the original results. Avoid
memorizing fixture answers in the skill. An invalid run cannot prove
quality. Passing structure/fixtures cannot prove agent behavior.

## Stage 5–11 — diagnosis and learning loop

Diagnosis before editing: distinguish case/answer-key, rubric,
missing context, tool/harness, model variance, lack of trace,
permissions/governance, packaging and actual skill-guidance failures.
Stage 6 screens all five conference methodology lenses and recommends
deep dives where supported. Require human approval before skill edits.
Rerun the *same versioned* case and rubric after each change; check
an independent case and previously passing coverage for regressions.

Preserve the selected provider's native comparison/reporting artifacts
and, when present, measured tokens and timing. Note missing fields as
unavailable rather than zero. Evaluate previously passing cases and an
independent case where practical, and identify regressions and critical
safety failures. Do not claim a blind comparator or aggregate benchmark
ran unless the chosen provider actually produced those results.
A one-off PASS is one observation, not evidence of reliability.

## Teaching response at every gate

Briefly tell the learner: **what we're drafting; why; a target-specific
example; what to inspect; what decision they are approving**. The agent
offers first drafts; let the learner revise, replace, reject or author
cases and assertions and challenge diagnoses. Show
source labels: AgentSkills.io convention (with URL), exact verified
conference talk if applicable, target-skill source, real run evidence,
or "Model recommendation" for your own synthesis.

Historical repository-level `evals/` records, when present, are separate
from current skill-local `evals/evals.json` suites. **Do not silently
migrate or delete historical cases.** The active dispatcher
[`native_eval.py`](../runner/native_eval.py) prepares separate Claude or
Codex-native evaluations but does **not** install or sandbox either
provider's model runner.
