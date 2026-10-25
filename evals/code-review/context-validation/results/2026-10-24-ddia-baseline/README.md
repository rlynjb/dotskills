# DDIA reference baseline — October 24, 2026

**Result: both reviews passed the four quality checks on the existing validation cases.**

The reviewers received the unchanged DDIA prompt library directly. This establishes
a baseline for that file before reorganizing its instructions.

| Case | Expected review | Recorded result |
| --- | --- | --- |
| case-01: validation exists in the caller | Recognize the guard and avoid a missing-validation false alarm. | PASS: no actionable issue; explanation identifies the guard, permitted entry point, and write. |
| case-02: validation is missing | Identify a reachable invalid write and explain the violated requirement. | PASS: one confirmed defect, with concrete invalid inputs and source evidence. |

Both reviews also passed supported-explanation, relevant-context-inspection,
and honest-verification checks. See the [scorecard](scorecard.md) and
[independent evidence audit](grading-audit.md).

## Exactly what was tested

- Source commit: `e1eda00b1d36b543e8a138b3726921b05ed3062c`.
- Guidance: `skills/code-review/references/code-review-ddia.md`, supplied unchanged.
- Reference Git blob: `758bfa1f0e1f593c597a2d72d8fffbe5bd4c81e1`.
- Reference SHA-256: `355db3a6ce1520d426503f6613a8dbe556e884869d9ce3d56b11f51c0e7b36fd`.
- Inputs: the existing [case-01](../../fixtures/case-01/) and
  [case-02](../../fixtures/case-02/) application snapshots and requirements.
- One fresh reviewer session per case, created with `fork_turns: none`.
- Same parent-inherited model, no model override; exact build, sampling settings,
  and reasoning-effort value were not exposed.
- Same task template and recorded local read/search/run interface.
- Node.js v24.22.1 for the reviewers' local verification.

Each workspace contained one guidance file, the three project files, and
`task.md`. No `SKILL.md`, context-quality guide, combined review reference,
other book lens, grader, fixture verifier, other case, or previous review was
supplied to the reviewer. Both before/after input-hash sets match.

This is a **direct DDIA reference baseline**, not a test of the current skill
wrapper and not a comparison with the earlier integrated skill runs. The
[task template](task-template.md) asks for a review and meaningful verification
limitations; it does not add instructions about inspecting callers or the expected
answer. The model's general instructions and tool environment still contribute
to its behavior.

## How it was graded

The [grading protocol](grading-protocol.md) was fixed before the reviewers ran.
It reuses the expected case behavior and Q1–Q4 from the
[existing grader](../../grader.md):

1. Correct conclusion.
2. Supported explanation.
3. Relevant context inspected.
4. Verification reported honestly.

The historical skill revisions and `SKILL.md`/context-guide loading checks in
that grader are inapplicable to this baseline. We instead checked that the exact
DDIA reference was accessed. Loading alone does not earn a quality pass.

The primary assistant graded the outputs against the code and recorded actions.
A separate evaluator received the same raw evidence and rubric without the
primary grades. Its independent grades agree. No human adjudication is claimed.

## Recorded reviews and execution

| Run | Original response | Recorded operations | Verification observed |
| --- | --- | --- | --- |
| 01 / case-01 | [Review](runs/run-01.md), [raw response](runs/run-01.raw.json) | [Trace](runs/run-01.trace.jsonl) | 27 invalid and 10 valid inputs, each with empty and populated arrays, plus repeated-call checks; 232 assertions passed. |
| 02 / case-02 | [Review](runs/run-02.md), [raw response](runs/run-02.raw.json) | [Trace](runs/run-02.trace.jsonl) | Five valid cases passed; one of 19 invalid cases met the rejection contract; the other 18 appended a record. |

Both local diagnostic processes exited with code 0. Run 02's program printed
contract failures instead of setting a nonzero exit code. Its review accurately
reported those failures. Finding the intentionally introduced defect is the
expected review outcome.

These counts describe the reviewers' chosen application checks, not additional
independent model evals or comparative skill scores.

The Markdown copies retain the response wording. Run 02's three Markdown hard
line breaks were normalized to blank-line paragraph separators; the raw JSON
preserves the captured response. The source and DDIA guidance were not changed.

## What the reads show about the prompt format

The existing DDIA file is a 1,471-line prompt library with calibration rules,
compact and master prompts, focused prompts, a workflow, and evidence rules.
It already tells the reviewer to check existing guards and surrounding behavior
before reporting missing validation.

Both sessions requested the entire file. Run 01 then reread lines 373–875;
run 02 reread lines 350–932. This records access to the current prompt library
without an authoring rewrite or a selected compact section pasted into the task.

The recorder retains the complete requested output. It does not retain the
enclosing tool-response budget, so model-visible truncation is unknown. These
records establish access, not complete comprehension or which embedded prompt
the model internally selected.

Both outputs remained within the supplied synchronous array-write contract.
Neither invented a requirement for database transactions, replication,
durability, retry deduplication, or a particular production workload.

**Interpretation:** the current text supplied usable guidance for these two
reviews. The result does not establish that its organization is optimal or that
every section has been validated. The broad reads give us an observable baseline
to compare after improving instruction selection; no token, cost, or latency
saving was measured.

## Limits and next work

This is one run per case under one host configuration. It contains no
no-guidance control and no reformatted-DDIA comparison, so it cannot establish
the prompt's causal benefit or the superiority of an instruction format.

The cases exercise validation boundaries and evidence calibration. They do not
test transaction atomicity, isolation, consistency, replication, retry safety,
schema evolution, or recovery. They also do not establish general review
reliability, statistical significance, skill triggering, or portability to other
harnesses.

Keep this baseline when reorganizing DDIA's instructions. Reuse the same cases
and task to check those behaviors again, then add targeted DDIA scenarios for
the guarantees we intend the lens to assess.

## Reproduction and evidence boundaries

Use the pinned source commit and copy only the selected fixture into
`project/` and the pinned DDIA file into `guidance/code-review-ddia.md`.
Expand [task-template.md](task-template.md) with the new workspace's absolute
path. Start a fresh reviewer session with the
[recorded launch template](recording/launch-template.txt), placing the
[recorder](recording/observe.py) and output trace outside the input workspace.
Keep the model and tool configuration consistent where possible.

The original suite's `prepare.py --skill before|after` recreates the earlier
integrated skill snapshots; it does not prepare this direct-reference baseline.

[manifest.json](manifest.json) records the source pins, exact task and input
hashes, raw response and trace hashes, agent identifiers, and grades.
[fixture-verification.txt](fixture-verification.txt) is the evaluator-only
fixture check captured before the reviewers ran.

The recording is a local observation protocol, not an operating-system sandbox
or provider-level audit. The supplied launch instructions and recorded actions
support setup validity within that boundary. They do not prove that all platform
activity is captured. Fresh-context setup is recorded from the launch calls;
absolute isolation beyond the recorded boundary remains unknown.

Parse the JSONL on the newline character `\n`, not Python's `splitlines()`:
some recorded test strings contain legal Unicode line-separator characters.
