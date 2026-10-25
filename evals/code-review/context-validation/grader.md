# Grader: validation context

Evaluator only. Do not put this file, the scorecard, fixture checks, or the other
case in the reviewer's workspace or conversation.

## What this eval measures

Can the code-review skill use surrounding code to distinguish an existing
validation boundary from a reachable missing-validation defect?

This is a snapshot review, without a before/after code diff. Each case has the
same requirements and persistence helper. Grade each attempt independently against its selected case.

## Established expectations

In both cases, `createUser(input, users)` is the sole external entry point.
Valid input is a non-null, non-array object whose `name` is a string with
`name.trim().length > 0`. Reject invalid input before writing. Store only the
supplied `name`, unmodified. Direct external calls to the internal persistence
helper are outside the stated contract.

| Case | Established behavior | Expected review result |
|---|---|---|
| `case-01` | `create-user.cjs` checks the input and throws `TypeError` before `saveUser` for invalid input. `save-user.cjs` performs the write after that guard. | Recognize the applicable validation boundary. Do not report missing validation in the helper as an existing defect on this path. |
| `case-02` | `create-user.cjs` calls the same persistence helper without the guard. For example, `{ name: '   ' }` reaches the store. | Report a reachable missing-validation defect. Explain the invalid input, the unguarded call, and the write that violates the requirement. |

The claim in `case-02` need not be that every invalid input is accepted. One
supported invalid input reaching a write establishes the defect. Do not require
exact wording or a particular severity label if the impact is accurately stated.

An optional suggestion to duplicate validation in the helper is not itself a
false alarm when clearly labeled optional. Presenting that suggestion as a
current defect in `case-01` is a false alarm. Requiring stored names to be trimmed
would contradict the supplied requirement to preserve the name.

## 1. Check run validity before grading

Record the model, harness, settings, selected fixture, skill revision, and the
available output/trace in `scorecard.md`.

The preparation helper offers these historical skill snapshots:

- Previous: `c6565141c5a5923235f80dd16a7ac680d58a1968`.
- Updated: `14abcdb4afe95c53a26522ab043fe1c0fc507421`.

A run is invalid if it used the wrong fixture or skill, mixed skill versions,
modified the implementation, or was exposed to the answer key, private fixture
checks, other case, another run's answer, or evaluator corrections. Rerun in a
fresh conversation with the intended inputs; do not treat an invalid run as a
skill failure.

If setup cannot be verified, record `UNKNOWN` validity and explain the gap. A
missing trace does not prove that contamination or a setup error occurred.

Check loading separately from review quality:

| Loading check | Previous skill | Updated skill |
|---|---|---|
| Selected snapshot's `SKILL.md` was loaded | Required | Required |
| Selected snapshot's `references/context-quality-and-requirements.md` was loaded | `N/A` | Required |

Use `PASS`, `FAIL`, or `UNKNOWN` for these checks. Base them on observed reads or
equivalent recorded loading, not the reviewer's self-report alone. A valid run
that loaded the updated skill but skipped its guide has a loading failure; its
quality can still be assessed independently. Loading the guide does not earn a
quality pass.

## 2. Grade each run against its case

Use `PASS`, `FAIL`, or `UNKNOWN` for every check and cite the output or trace
evidence. Grade each attempt independently.

| Check | `PASS` | `FAIL` | `UNKNOWN` |
|---|---|---|---|
| **Q1: Correct conclusion** | `case-01`: explicitly recognizes no missing-validation defect on the guarded path. `case-02`: identifies the reachable invalid write. | Reports an existing missing-validation defect in `case-01`, or misses/dismisses it in `case-02`. | Output is missing, truncated, or too ambiguous to determine the conclusion. |
| **Q2: Supported explanation** | Explains the relevant boundary and write path using actual source locations and the supplied requirement. In `case-02`, supplies a concrete failing input or an equally precise failure condition. | Invents locations or requirements; asserts reachability without support; gives only generic validation advice as the finding. A complete answer with no grounding fails this check. | The available output is insufficient to assess its support. |
| **Q3: Relevant context inspected** | Recorded reads/searches establish the requirement, entry-point guard or its absence, and the persistence behavior. Equivalent retrieved excerpts count; no particular read order is required. | A complete trace shows that necessary surrounding evidence was skipped. | Trace is absent or incomplete, so inspection cannot be established. |
| **Q4: Verification reported honestly** | Claims about inspection, tests, and execution match the available record. Running no tests is acceptable when reported accurately. | A complete record contradicts a claim, such as saying tests passed when only files were read or syntax was checked. | A claim cannot be verified because the relevant record is unavailable or incomplete. |

Do not use missing telemetry as proof that a read or test did not happen. With a
complete trace, an unsupported claim of execution is a failure; with an
incomplete trace, record the uncertainty. Note any execution failures and how
they limit the conclusion.

No finding by itself is not sufficient for `case-01` to pass the eval. The
reviewer must establish why the permitted path is guarded. Likewise, naming
"validation" in `case-02` without explaining the invalid write is insufficient.

## 3. Save the case result

A valid attempt passes when Q1–Q4 all pass. Any UNKNOWN leaves that criterion
unverified. Record loading diagnostics separately. Save the response, trace,
run conditions, and grades together in the selected case’s `results/<run-id>/`.
Investigate a failure before changing the skill, then record a new attempt.
A passing case does not establish broad review reliability.

## Fixture checks are not model results

The evaluator-side checks establish that valid inputs are stored in both cases,
invalid inputs are rejected without a write in `case-01`, and an invalid name is
persisted in `case-02`. Passing those checks verifies the cases and answer key.
It does not mean a reviewer ran, found the defect, or passed this eval. Leave
model results as `NOT RUN` until actual outputs and records exist.
