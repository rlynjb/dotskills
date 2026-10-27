# DDIA Codebase Problem Questions

## Contents

- [Purpose and source boundaries](#purpose-and-source-boundaries)
- [DDIA topic scope](#ddia-topic-scope)
- [The repeated teaching format](#the-repeated-teaching-format)
- [Choosing problem questions](#choosing-problem-questions)
- [Requirements and behavior](#requirements-and-behavior)
- [Data ownership and design](#data-ownership-and-design)
- [Implementation and data guarantees](#implementation-and-data-guarantees)
- [Verification questions](#verification-questions)
- [Post-review comment example](#post-review-comment-example)
- [Worked miniature](#worked-miniature)
- [Coverage of the Master DDIA rubric](#coverage-of-the-master-ddia-rubric)
- [Source boundaries](#source-boundaries)

## Purpose and source boundaries

Use DDIA as the sole technical review lens. Explore the authorized codebase and
select useful, varied questions about data-intensive behavior from real implementation
details. Do not require a fixed topic order or a question from every topic.
The question-led tutorial format is a DotSkills teaching adaptation.

Keep DDIA as the technical review lens throughout the questions. Start from the
actual implementation and requirements, not an imagined greenfield system. Explain
existing protections as well as supported issues. Zero findings is a valid outcome.

This remains a code-review skill with guided learning and optional interview practice.
Discussing implementation means inspecting and explaining existing code by default. It does not
authorize writing code, editing files, or executing a target skill against real services.
Hands-on coding requires a separate user request and a bounded local/synthetic scope.
An explanation of code does not establish the learner's ability to implement it.

The questions, examples, and DDIA mappings below are original DotSkills adaptations.
Do not present them as verbatim book material, official company questions, or
conference methodology. Do not invent DDIA chapter/page citations. Distinguish
book concepts, inspected code evidence, and model recommendations.

## DDIA topic scope

Choose relevant topics from the Master DDIA rubric, including:

- Data models, authoritative data, storage, indexes, and access patterns.
- Encoding, schema evolution, and compatibility.
- Transactions, invariants, concurrency, consistency, and ordering.
- Replication, partitioning, failover, and distributed-system failure.
- Retries, idempotency, recovery, and duplicate processing.
- Batch/stream processing, events, caches, and derived views.
- Reliability, scalability, operability, and tests of these guarantees.

State which DDIA concept each question teaches and why it matters to the inspected
code. Discuss implementation mechanics only to support that concept. Do not create
standalone algorithm/data-structure drills, general architecture interviews, AI/ML,
data science, or networking reviews. An AI pipeline may still be reviewed for its
data consistency or recovery guarantees; model quality is outside this skill.
If the scoped code has no meaningful DDIA concern, say so instead of filling the
tutorial with unrelated topics or inventing findings.

## The repeated teaching format

For each problem question, use the following teaching scaffold:

1. **What and why:** explain the question's learning goal and why it matters.
2. **Problem question:** state the concrete behavior, concern, or decision to examine
   in the target code. Use this label in Guided and Practice mode, rather than
   “Interview-style question.” For example: “What happens if this request is retried
   after the first attempt commits?” A question does not imply a defect exists.
3. **How to build an answer:** name the requirements and evidence to examine.
4. **Worked answer:** demonstrate a concise answer supported by inspected files,
   symbols, tests, or supplied contracts. If evidence is missing, model an honest
   answer such as “I cannot establish that guarantee from the available code.”
5. **Walkthrough:** trace a small input, request, state change, or failure sequence.
6. **Trade-off and follow-up:** explain one relevant alternative and what new evidence
   or constraint would change the answer.
7. **Takeaway:** summarize what the learner should notice.

Define technical terms at first use. For example, an invariant is a rule that must
stay true; idempotency means repeating an operation has the same intended effect. Use concrete examples before
terminology. Give concise public explanations of evidence and decisions, not private
chain-of-thought. Do not fill every slot mechanically when it adds no teaching value.

In Guided mode, provide the worked answer rather than requiring the user to guess.
In Practice mode, hold back the worked answer until the user responds or requests
help; ask one question at a time. Give feedback on correctness, evidence, clarity,
and trade-offs without inventing a company hiring score. Resume the same question after
a clarification or explanation request.

Keep teaching examples labeled hypothetical and separate from findings about actual
code. Link the source title when using a research-derived preparation principle;
label target-code evidence and model-proposed recommendations separately.

## Choosing problem questions

Inspect the authorized repository or change scope before choosing questions. Sample
relevant entry points, data paths, tests, and callers; state what was inspected and
do not describe a sample as an exhaustive codebase search. Prioritize consequential
behavior, surprising safeguards, and useful trade-offs. A question may teach why
correct code works; it need not expose a bug.

Default to one `Problem question N — Concrete question` at a time. Number questions
for navigation, not lifecycle stages. Vary code paths and topics to build breadth.
If random questions are requested, shuffle relevant candidates after inspection;
never substitute generic puzzles for the target code or fabricate defects.
Offer a next question from a different relevant topic when useful.

The sections below are an optional question pool, not sequential stages. Choose
and combine them freely. For example, start with a transaction's invariant, then
examine retry safety elsewhere, then schema compatibility in a consumer. Keep the
variety within DDIA.

## Requirements and behavior

Inspect the target change, surrounding behavior, and available requirements first.
Then state scope, revision, user goal, and exclusions. If no target is identifiable,
ask for the code, diff, or repository path; do not substitute an invented target.

Explain:
- Functional requirements: what a user or system must be able to do.
- Non-functional requirements: relevant qualities such as response time, throughput,
  availability, durability, recovery, or cost.
- Data invariants: correctness rules such as one charge per request or no negative stock.

Record requirement status as confirmed (with source), inferred, proposed, or unknown.
Do not silently turn an interview assumption into a product requirement. Ask only the
missing questions that materially change the review; continue supported analysis.

Example questions:
- What does success mean for this operation, and what is out of scope?
- What must remain true if two requests arrive together?
- Which latency or load target is established, and which still needs clarification?

Answer scaffold: “The required behavior is X, established by Y. The invariant is Z.
We know A about the workload; B is unknown, so I will not assume a scale problem.”

## Data ownership and design

Identify actual entry points, API or function contracts, entities, authoritative
stores, and read/write paths. Explain how a request passes through the implementation.
Use a compact diagram only when it clarifies relationships that prose cannot.
Do not invent queues, caches, shards, or microservices absent from the evidence.

Example questions:
- Which component owns this value? Is another copy derived or authoritative?
- What input reaches this function, and what state can it change?
- Why does this access pattern fit the schema, index, or chosen data structure?

Answer scaffold: “This entry point calls A, which changes B in store C. D is a
derived copy. The contract establishes E; the inspected implementation guarantees F.”
Explain the difference between intended architecture and observed implementation.

### Compare design choices through DDIA

Connect the proposed or existing design to the established requirements. Discuss ownership,
transaction boundaries, consistency, schema evolution, replication, and recovery only
where applicable. Explain which properties come from a design contract and which still
need implementation verification.

Ask: “What alternative would you consider, and which constraint changes your choice?”
Model an answer that names the invariant, benefit, cost, and evidence needed. Keep
capacity estimates hypothetical unless sourced; use them only when they affect a
decision. Prefer the smallest justified change over an unnecessary redesign.

## Implementation and data guarantees

### Inspect implementation and guarantees

Choose a concrete path and walk through the successful case, then a relevant failure
or interleaving. Inspect transaction boundaries, locks/constraints, retry behavior,
duplicate handling, consistency, ordering, events, projections, and compatibility.
An outer transaction may already protect apparently separate writes; inspect callers.

Example questions:
- What happens if the second write fails after the first succeeds?
- What if the caller times out after the server commits and then retries?
- Can two workers process the same message? Which guarantee prevents duplicate effects?
- Can old and new versions read each other's data during deployment?

Answer scaffold: “Under condition X, operations A and B occur in this order. Guard C
does/does not cover both. The supported outcome is D, affecting invariant E.”
When discussing alternatives, distinguish transaction atomicity from isolation and
idempotency; one does not automatically supply all three guarantees.

### Examine storage and operational trade-offs

Connect access patterns, indexes, caching, batching, replication, and partitioning
to actual requirements and evidence. Explain the read/write cost, consistency,
durability, and recovery consequences of a justified alternative.
Do not equate in-memory complexity with database latency or end-to-end request time.
Query plans, I/O, contention, network calls, and workload distribution may dominate.
Label estimates and assumptions; do not present them as measured benchmarks.
Do not describe CAP as an unrestricted "pick any two" rule or recommend distributed
infrastructure merely because it could scale further in theory.

### Optional hands-on practice

For an explicitly requested coding exercise, help the learner choose a familiar
language, propose a small implementation task, and let them write it before showing
a worked solution when in Practice mode. Prefer runnable code for the exercise;
label pseudocode as explanatory rather than a tested implementation. Stay within
authorized local fixtures and verify the result with safe checks. Do not silently modify
the repository during a review or treat a learning checkpoint as write authorization.

## Verification questions

Recommend a small normal case, boundary case, and relevant failure/concurrency case.
For each, state input/setup, expected behavior and its source, what would be observed,
and which guarantee it tests. Explain that testing implementation behavior differs
from grading how well a reviewer recognized that behavior.

Trace a sample by hand when useful, labeling it a walkthrough rather than an executed
test. Inspect test isolation and side effects before any execution. Never post comments,
create issues, mutate real data, deploy, push code, or run production/load tests as
part of the tutorial. Use only authorized safe checks; if safe execution is uncertain,
describe the test and mark it not run. Do not claim missing tests prove a defect.

Example questions:
- Which assertion would distinguish the correct result from this failure?
- Would this test catch the bug, or only exercise the happy path?
- What remains unverified after it passes?

Report tests actually executed, tests only inspected, and proposed tests separately.

### Review report and interview recap

When the scoped review is complete or the user requests a recap, deliver the original review categories: correctness/invariants, data model/consistency,
reliability/operability, testing gaps, and optional improvements. Deduplicate root
causes. Every finding needs inspected evidence, conditions, consequence, smallest
reasonable improvement, claim class, and calibrated severity.

Use confirmed defect, plausible risk, verification gap, and optional improvement
accurately. Explain existing safeguards as well as supported problems. Zero findings
is valid. End with scope, verification limits, and a compact coverage summary.

For an early recap, clearly label partial coverage and outstanding checks.
Then model a short interview recap:
“Here is the goal and invariant; here is the path I inspected; here is the main
supported finding or safeguard; here is the trade-off; here is what I tested and
what still needs evidence.”
Do not invent a defect, certainty, a hiring verdict, or a recommendation to fill
this sentence. Suggest one useful follow-up learning question.

## Post-review comment example

After teaching and any checkpoint, append **Post-review — Draft code review comments**
using the rules in SKILL.md. For a complete report, place it after the scope and
verification summary. Keep the comment itself natural and concise, suitable for
an inline review rather than an interview answer.

Hypothetical example only: suppose an inspected handler acknowledges a message
before saving it, and the established contract requires redelivery after a failed
save. A draft anchored to the verified acknowledgement line could read:

> Acknowledging here means a failed save will prevent this message from being
> redelivered, so the update can be lost. Could we acknowledge only after the save
> succeeds and add a test for a failed save?

In a real review, show the actual file and verified line above the comment and
check surrounding error handling before making this claim. Do not reuse this
example as a finding without evidence. If the discussion only explained a safeguard
or a hypothetical risk, state that no actionable comment is warranted.

## Worked miniature

This is a hypothetical teaching example, not a finding about the user's repository.

Suppose a message consumer records an account credit and acknowledges the message.
The established contract permits redelivery and requires each event to affect the
balance once. In this hypothetical implementation, a unique event-ID record and
the balance update commit in the same database transaction; acknowledgement follows.

- **Problem question:** "What happens if the process crashes after committing the
  credit but before acknowledging the message?"
- **How to build an answer:** inspect the redelivery contract, transaction boundary,
  unique constraint, and duplicate-handling path.
- **Worked answer:** the message may arrive again. If the consumer treats a unique
  event-ID conflict as an already processed event and skips the credit, the same
  event does not increase the balance twice. Verify that the ID record and credit
  really share a transaction and that the duplicate path handles the conflict.
- **Walkthrough:** event E commits one credit; the process crashes; E is redelivered;
  the existing event ID prevents a second credit; the consumer acknowledges E.
- **Trade-off and follow-up:** persistent deduplication requires storage and a
  retention policy. Deleting IDs too early may allow an old event to apply again.
  This database guarantee does not automatically cover external side effects.
- **Verification:** propose tests for a crash before commit, redelivery after commit,
  and concurrent delivery of the same ID. These tests have not run merely because
  the walkthrough described them.
- **Takeaway:** reliable retry behavior depends on persistent identity, atomic state
  changes, and correct duplicate handling, not only the acknowledgement order.

No actionable review comment is warranted if inspection confirms the required
safeguards. The hypothetical example is not evidence of a defect in the target code.

## Coverage of the Master DDIA rubric

Keep all 15 dimensions even when the tutorial spotlights only a few. Track each as
reviewed (with result), not applicable (why), or not verified (missing evidence).
Do not force irrelevant dimensions into findings.

| Master rubric dimension | Related question topics |
| --- | --- |
| 1. Changed behavior; 2. Match to intent | Requirements and observed behavior |
| 3. Entities/stores/flows; 4. Authoritative values | Data ownership and flows |
| 5. Access patterns, storage, indexes | Design choices and implementation guarantees |
| 6. Transactions/invariants; 7. Concurrency; 8. Consistency/ordering | Implementation and failure scenarios |
| 9. Retries/duplicates; 10. Events/caches/derived views | Implementation and failure scenarios |
| 11. Schema/encoding compatibility | Implementation and failure scenarios |
| 12. Replication/partitioning/failover | Design choices and implementation guarantees |
| 13. Partial failures/recovery | Implementation and failure scenarios |
| 14. Scale and operability | Design choices and implementation guarantees |
| 15. Tests of guarantees/failures | Verification |

## Source boundaries

Use the [Master DDIA code-review rubric](master-ddia-code-review.md) as this skill's
operational review checklist. It is an adaptation of Designing Data-Intensive
Applications concepts, not the book's verbatim text or chapter structure.
The questions, teaching format, and worked examples are model-proposed DotSkills
adaptations. Cite available book material accurately when used; otherwise name the
concept and state the source limitation rather than inventing a quotation or page.
Company interview topic lists do not determine this skill's scope.
