# Independent DDIA baseline audit

Evaluator: `/root/audit_ddia_baseline`, fresh context. The evaluator received
the fixed rubric, outputs, traces, manifest, and source evidence without the
primary grades. The audit was read-only and did not rerun the model reviews.

## Independent grades

**Both runs PASS Q1–Q4 and DDIA-reference loading. Input/setup validity is PASS
within the recorded boundary**, with the isolation and delivery limitations below.

Event numbers refer to JSONL records parsed using `'\n'`.

| Check | Run 01 — case-01 | Run 02 — case-02 |
| --- | --- | --- |
| Q1: Correct conclusion | PASS. Explicitly finds no actionable issue and explains why the internal helper's lack of duplicate validation is not a defect. | PASS. Identifies the reachable invalid write through createUser → saveUser, including missing, non-string, and blank names. |
| Q2: Supported explanation | PASS. Correctly cites create-user.cjs:4–11 guarding the call at line 14, save-user.cjs:2–4, and requirements lines 5–15. Preserves the supplied name instead of requiring trimming. | PASS. Correctly cites the unguarded call at create-user.cjs:3–4, write at save-user.cjs:1–4, and requirements lines 6–11. Supplies concrete invalid inputs and accurately notes that null throws while other invalid values reach the write. |
| Q3: Relevant context inspected | PASS. Trace events 3, 5, 6 return the full requirements, helper, and guarded entry point. | PASS. Trace events 2, 5, 7 return the full requirements, helper, and unguarded entry point. |
| Q4: Verification reported honestly | PASS. Event 8 executes the recorded Node harness, returns Node v24.22.1, 27 invalid inputs, 10 valid inputs, 232 assertions, result PASS, exit 0. Its two seeded states and repeated-call checks substantiate the final verification table. | PASS. Event 8 returns Node v24.22.1, valid 5/5, invalid-contract checks 1/19, and 18 failure records each showing error null and appended 1. Exit 0 means the diagnostic harness completed; the review correctly reports the contract failures. |
| DDIA-reference loading | PASS. Events 2 and 7 read the exact reference. | PASS. Events 4 and 6 read the exact reference. |
| Input/setup validity, recorded boundary | PASS, qualified below. | PASS, qualified below. |

## Loading and instruction-selection evidence

- Both initial DDIA reads record lines 1–1471, covering the entire reference:
  calibration rules, compact/master prompts, numbered and lettered focused
  prompts, workflow, and concluding evidence rules.
- Run 01 rereads 373–875: sections 5–13 and the opening of section 14.
- Run 02 rereads 350–932: the latter portion of section 4, sections 5–14,
  and the section 15 heading.
- Every recorded read's stdout exactly matches the corresponding numbered source
  range. No truncation appears inside the recorded stdout. The recorder does not
  capture the enclosing tool response or its output budget, so model-visible
  truncation is UNKNOWN. The rereads alone do not prove truncation occurred.
- The reference SHA-256 and Git blob match the manifest.
- The record establishes reads, not which embedded prompt the reviewer internally
  selected. Both outputs remain within the declared synchronous array-write scope
  and invent no database, concurrency, durability, retry-deduplication, or
  distributed-system requirement.
- All 16 recorded operations have exit 0 and empty stderr. The original
  SKILL.md/context-guide loading checks are inapplicable under the fixed protocol.

## Integrity and setup checks

The evaluator independently recalculated and matched:

- The reference SHA-256/blob hash, grader blob hash, protocol hash, recorder hash,
  and task-template hash.
- Both original trace hashes, original raw-response hashes, and eight-event counts.
- Every source-read hash against its assigned fixture/reference/task and manifest.
- Every before/after input hash: all five inputs per run match each other and
  the preserved source files.
- Each task against the template expanded with its assigned workspace.

The Markdown outputs preserve the original raw-response wording. Run 01 adds
a terminal newline; Run 02 converts three Markdown hard line breaks to blank-line
paragraph separators and adds a terminal newline. These are formatting
differences, not substantive changes.

After the audit, extra blank lines at the end of the Markdown copies were
removed for whitespace validation. The raw responses and wording are unchanged.

The manifest identifies parent-inherited model, no override, exact build/sampling
unavailable, and ChatGPT collaboration subagents with fork_turns=none.
The task/launch materials supply only the assigned project and DDIA guidance;
recorded commands use those assigned inputs. No recorded operation exposes the
answer key, other case, other review, or evaluator correction.

## Limits

Fresh context is manifest-attested, not independently established by a complete
launch/session transcript. The recorder is not an OS sandbox and cannot prove
absence of unrecorded accesses, transient edits restored before the final hash,
or other off-record contamination. Absolute isolation beyond the recorded
boundary is UNKNOWN, not a demonstrated failure.

These two successful outputs support the narrow validation-boundary and
evidence-calibration expectations. They do not establish broad review reliability,
distributed-systems competence, a causal benefit from DDIA guidance, or
superiority of one instruction format; no no-guidance or reformatted-DDIA
comparison exists here.
