# Scorecard: validation context

Evaluator only. Copy this template for an actual comparison. Keep it outside the
reviewer's workspace and conversation. See [grader.md](grader.md) for the
expectations and grading rules.

## Comparison setup

- Date/time:
- Evaluator:
- Model and version:
- Harness and version:
- Model settings and tool access:
- Fixture revision or content hashes:
- Common request used:
- Any differences between runs:

| Arm | Pinned skill revision |
|---|---|
| Previous | `c6565141c5a5923235f80dd16a7ac680d58a1968` |
| Updated | `14abcdb4afe95c53a26522ab043fe1c0fc507421` |

Use fresh conversations and equivalent settings/access. Keep the selected
fixture identical between its previous and updated runs. Do not show reviewers
the rubric, private fixture checks, other case, or previous outputs.

## Run records

All model runs are initially **NOT RUN**. Replace statuses only with observed
results. Record validity as `VALID`, `INVALID`, or `UNKNOWN` after a run. Record
trace completeness so that an unavailable action is not mistaken for an action
that demonstrably never happened.

| Run | Case | Skill | Status | Validity | Output / trace locations | Trace completeness |
|---|---|---|---|---|---|---|
| 01 | `case-01` | Previous | NOT RUN | — | — | — |
| 02 | `case-01` | Updated | NOT RUN | — | — | — |
| 03 | `case-02` | Previous | NOT RUN | — | — | — |
| 04 | `case-02` | Updated | NOT RUN | — | — | — |

## Loading checks

Use `PASS`, `FAIL`, or `UNKNOWN` after each run. The guide check is `N/A` for the
previous skill because that snapshot does not contain it.

| Run | Selected `SKILL.md` loaded | Context guide loaded | Evidence or limitation |
|---|---|---|---|
| 01 | NOT RUN | N/A | — |
| 02 | NOT RUN | NOT RUN | — |
| 03 | NOT RUN | N/A | — |
| 04 | NOT RUN | NOT RUN | — |

## Quality checks

Grade each run against its established expectation before comparing the arms.
Use `PASS`, `FAIL`, or `UNKNOWN`; leave invalid runs ungraded and explain why.

| Run | Q1: Correct conclusion | Q2: Supported explanation | Q3: Context inspected | Q4: Honest verification |
|---|---|---|---|---|
| 01 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| 02 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| 03 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |
| 04 | NOT RUN | NOT RUN | NOT RUN | NOT RUN |

### Evidence notes

For each completed run, record the relevant review excerpt and actual code or
trace location. Explain failures, unknowns, contamination, and execution limits.

- Run 01:
- Run 02:
- Run 03:
- Run 04:

## Comparison notes

- Case 01, previous versus updated:
- Case 02, previous versus updated:
- Loading outcome, separately from review quality:
- Improvements supported by evidence:
- Regressions supported by evidence:
- Unknowns or invalid runs requiring another run:
- One targeted correction, if supported:

If both versions pass, record that no improvement was demonstrated on this
pair. Do not invent a percentage, count fixture checks as model passes, or infer
broad reliability from four runs.
