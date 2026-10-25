# First eval: context for input validation

**Question:** Does the code-review skill reach a justified conclusion about
whether invalid input can reach a write?

This is one manual eval with two small synthetic cases. It comes with runnable
code, a common task, an answer key, and a blank scorecard. Model reviews have
**not been run** as part of creating this eval.

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

## 4. Repeat for all four combinations

Use a new output directory and fresh conversation every time:

| Review | `--case` | `--skill` | Example `--output` |
| --- | --- | --- | --- |
| 1 | case-01 | before | ../dotskills-review-01 |
| 2 | case-01 | after | ../dotskills-review-02 |
| 3 | case-02 | before | ../dotskills-review-03 |
| 4 | case-02 | after | ../dotskills-review-04 |

These are four independent runs, not a conversation containing both versions.
Within a case, keep the project content and request identical except for the
workspace path. Only the selected skill package changes.

## 5. Grade, then compare

Use [grader.md](grader.md) yourself, or in a separate evaluator session after
the reviews. Record each check and its evidence in a copy of
[scorecard.md](scorecard.md). Keep all evaluator material outside review sessions.

Grade each output against the known case facts before looking at old versus new.
The four shared quality checks are:

1. Correct conclusion.
2. Relevant context established.
3. Claims grounded in source evidence.
4. Verification reported honestly.

Use **Pass / Fail / Unknown**, with separate skill-loading diagnostics.
Reading the new guide does not by itself demonstrate better review quality.
No model-based judge or aggregate numeric score is needed for this first pass.

An old failure becoming a new pass is an improvement on that case. Both passing
means no demonstrated gain there; both failing means the problem remains; a new
failure after an old pass is a regression to inspect. Unknown evidence prevents
a conclusion on that check. Record inconclusive comparisons as such.

One pair of cases is an initial diagnostic. It cannot prove that the guide caused
a general improvement. The prior skill already contains evidence-calibration
guidance and may also pass. Preserve the cases and raw results before expanding
to a real code change or automating repeated runs.
