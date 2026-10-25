# First eval: context for input validation

**Question:** Does the code-review skill reach a justified conclusion about
whether invalid input can reach a write?

This manual eval contains two small synthetic cases. Start with one case:
prepare its input, run the reviewer, grade the response, and save that attempt.
There is no required cross-case summary or comparison step.

## What the cases establish

| Case | Code behavior | Expected review conclusion |
| --- | --- | --- |
| case-01 | The only external entry point validates before calling the storage helper. | No missing-validation defect on this path. |
| case-02 | The same entry point calls the identical helper without the guard. | Identify that invalid input reaches the store, violating the requirement. |

Both are **snapshot reviews** of the complete input-validation and write path.
There is no code diff. The requirements are identical and deliberately define
the complete application boundary, so the expected answers are checkable.

The guard is the only implementation difference. The helper does not validate
in either case. A reviewer needs the surrounding calling path to decide whether
that absence is a defect.

This is a small synthetic diagnostic, not the real-change walkthrough from the
Phase 1 plan. It does not cover distracting, missing, stale, or conflicting
context, broad code-review reliability, or skill triggering.

## Case layout

Both cases now follow the [shared case template](../../templates/case/README.md):

- [case-01](cases/case-01/README.md): guarded input-validation path.
- [case-02](cases/case-02/README.md): reachable invalid write.

Each case contains `input/task.md`, `input/requirements.md`, application code in
`input/materials/mock-app/`, `expected.md`, `grading.md`, and `results/`.
Only input material and the selected skill guidance go to the reviewer.

Each case’s `results/` folder contains its recorded reviews, traces, and grades.
Historical attempts are preserved; they do not establish the current skill’s quality.
The preparation helper creates a flat review workspace without evaluator answers.

## 1. Verify the cases

From the DotSkills root, with Python 3.11+, Git, and Node.js 18+ available:

```bash
node evals/code-review/context-validation/verify-fixtures.cjs
```

This evaluator-only check confirms valid writes in both cases, rejection before
writes in case-01, and reproducible invalid writes in case-02. A passing command
means the **fixtures match the answer key**. It gives no score for either skill.

## 2. Prepare one review

```bash
python3 evals/code-review/context-validation/prepare.py \
  --case case-01 --skill before --output ../dotskills-review-01
```

The helper creates a new directory outside the checkout containing only:

- `project/`: one case's source files and public requirements.
- `skill/`: the complete code-review package from the selected Git revision.
- `task.md`: the common review request with the workspace path filled in.

Record the command's printed metadata with your evaluator notes. It identifies
the case, skill commit, eval source commit, and fixture digest. If it reports
uncommitted eval changes, commit or record that exact diff before comparing runs.
Do not paste the preparation output into the review conversation.

The skill versions are pinned:

| Selection | Git revision | Meaning |
| --- | --- | --- |
| before | `c6565141c5a5923235f80dd16a7ac680d58a1968` | Skill before the context-guide update. |
| after | `14abcdb4afe95c53a26522ab043fe1c0fc507421` | Skill including the context guide and its loading procedure. |

If a shallow checkout lacks either commit, fetch the history before preparing.
The helper refuses to overwrite an existing output directory.

## 3. Run in a fresh coding-agent conversation

Open the prepared directory as the agent's workspace and submit its `task.md`.
Use a fresh session with no previous review or this eval-authoring conversation.
Keep the model, harness, settings, tools, permissions, and time budget the same.
Do not add reminders about callers, validation, or the expected answer.

Configure access to the prepared workspace only where your harness supports it.
Do not attach DotSkills itself, the other case, the other skill version, grader
notes, the verification script, or past answers. The preparation helper copies
files; it does **not** create an access-control sandbox. A working directory
alone does not prevent a tool from reading elsewhere.

Save the final response and available read/search/command trace outside the
review workspace. If evaluator answers or other variants were accessed, mark
the run invalid and repeat in a clean workspace. Missing trace evidence should
be marked unknown, not assumed to show a read or a command.

## 4. Grade and save this attempt

Use this case’s `expected.md` and `grading.md` with the shared [grader](grader.md).
Copy the [single-attempt scorecard](scorecard.md) into this case’s
`results/<run-id>/grade.md`. Save the actual response, available trace, preparation
metadata, and run conditions alongside it.

Grade Q1–Q4 as **Pass / Fail / Unknown**, with source or trace evidence. Record
loading diagnostics separately. Invalid attempts should be repeated in a clean
session; missing evidence remains Unknown.

## 5. Decide the next step

If the result fails, inspect the evidence and identify the cause before changing
the skill. Rerun the same case in a fresh session and save a new attempt. If it
passes, keep the result and choose another case when ready. You do not need to
run both cases or both historical skill snapshots for one eval attempt.

The helper’s `before` and `after` options select historical whole-skill snapshots;
neither tests the current individual-book workflow. To evaluate the current DDIA
reference, supply its exact file and revision with one case’s input in a fresh
workspace and record that setup. Mark SKILL.md loading N/A when only a reference
is supplied. The helper does not run the model or grade its response.
