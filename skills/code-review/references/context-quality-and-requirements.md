# Code Review: Context Quality and Requirements

Define the information needed for a grounded code review and the rules
for selecting, checking, and using that information.

Gather enough relevant evidence to understand the review target and
justify the review's conclusions.

All reference paths below are relative to the code-review skill root.

## 1. Establish what is being reviewed

Identify:
- The review target: diff, PR, commit range, files, or feature.
- The revision or working-tree state being reviewed, when available.
- The review scope and any explicit exclusions.
- Expected behavior and acceptance criteria, when supplied.

Use the request and accessible sources to establish the target.
Ask a focused question if the target cannot be determined.

For a snapshot review without a diff, state that no before/after
comparison was available.

Missing optional requirements should limit conclusions without
preventing useful review of the available code.

## 2. Gather relevant implementation context

Start with:
- The review request.
- Applicable repository instructions.
- The diff or named review target.
- Enough surrounding code to understand the relevant behavior.
- Supplied requirements and acceptance criteria.

Retrieve additional information when it answers a concrete question:

- Callers:
  What inputs and guarantees reach this code?
  Is validation or authorization already performed at a relevant boundary?

- Callees and consumers:
  What does this code depend on?
  Which consumers could be affected by the changed behavior?

- Tests:
  What expected behavior and edge cases do the tests cover?

- Contracts, schemas, and configuration:
  What types, constraints, or runtime conditions affect the behavior?

- Documentation or history:
  What explains the intended behavior or resolves a specific uncertainty?

Before reading more, identify the question that the source should answer.
This does not need to be narrated to the user.

Search for relevant symbols or sections before reading large files.
Read enough surrounding code to avoid misleading isolated snippets.

Expand the investigation when necessary.
Do not load entire directories or unrelated history merely because
they are available.

## 3. Load review guidance progressively

From references/code-review.md, read:
- "Evidence and severity calibration (applies to every review prompt)".
- "Compact daily code-review prompt" for ordinary changes.

Use master or focused sections when the requested scope or investigation
requires them. Do not combine every prompt variant into one review.

Locate and read relevant sections when bounded reads are supported.
If a tool loads the entire file, do not claim that only an excerpt
was loaded.

Load specialized references when they help answer a relevant question:

- references/code-review-aposd.md:
  Responsibilities, interfaces, ownership, and design complexity.

- references/code-review-at.md:
  Algorithm correctness, invariants, boundary cases, and computational cost.

- references/code-review-ddia.md:
  Persistence, transactions, concurrency, retries, and consistency.

- references/code-review-fode.md:
  Data ingestion, transformations, quality, and consumer contracts.

- references/code-review-sdi.md:
  Service boundaries, system behavior, reliability, and scaling.

Apply basic correctness and design checks to every change.
Use specialized references for deeper investigation when relevant.

References help identify questions to investigate.
Findings still require evidence from the implementation, applicable
requirements, or actual execution.

Do not require a finding from every lens.

## 4. Verify candidate findings

Before reporting an issue, inspect relevant callers, guards, contracts,
and tests that could confirm or invalidate it.

Establish the conditions under which the issue would occur.
If reachability or impact remains uncertain, say so.

For example, before reporting missing input validation, check whether
an applicable caller or boundary already establishes the required
invariant.

Support consequential claims with actual source locations:
a file and symbol or line range, a document section, or a tool result.
Include the revision when available. Never invent source locations.

Keep these distinctions clear:
- What the inspected implementation does.
- What the request or applicable specification requires.
- What is inferred and still depends on assumptions.
- What remains unknown.

Distinguish tests read from tests actually executed.
Report execution results only when they are available.
A passing test supports only the behavior it checks.

Use the existing finding categories and severity guidance in
references/code-review.md.

Zero actionable findings is a valid result.

## 5. Handle missing, stale, and conflicting information

Do not invent requirements, workload assumptions, runtime conditions,
or test results.

When information is unavailable:
- Identify the missing evidence.
- Explain which conclusion it limits.
- Continue reviewing portions supported by available evidence.
- Ask for clarification when the missing information prevents a
  meaningful conclusion.

Treat previous review summaries as leads to verify.
Recheck affected evidence when the review target changes.

When sources disagree:
- Identify the conflicting claims and their sources.
- Compare their scope, revision, and applicability.
- Explain unresolved conflicts instead of silently choosing one claim.

Current code establishes implementation.
It does not automatically override an applicable requirement.

## 6. Stop when the review is sufficiently grounded

Stop gathering context when:
- The relevant behavior and surrounding path are understood.
- Candidate findings have been checked against applicable evidence.
- Remaining material gaps are identified.
- Conclusions can be supported or appropriately qualified.

Do not continue searching merely to produce additional findings.
Do not stop early merely to reduce the number of reads.

Keep task-specific findings and temporary workarounds in the review
notes. This guide should contain reusable review instructions.
