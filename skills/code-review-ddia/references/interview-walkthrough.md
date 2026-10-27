# DDIA Review Using Microsoft's Engineering Lifecycle

## Contents

- [Purpose and source boundaries](#purpose-and-source-boundaries)
- [Technical excellence topics](#technical-excellence-topics)
- [The repeated teaching format](#the-repeated-teaching-format)
- [Stage 1 — Problem solving](#stage-1--problem-solving)
- [Stage 2 — Design](#stage-2--design)
- [Stage 3 — Coding](#stage-3--coding)
- [Stage 4 — Testing](#stage-4--testing)
- [Worked miniature](#worked-miniature)
- [Coverage of the Master DDIA rubric](#coverage-of-the-master-ddia-rubric)
- [Research sources](#research-sources)

## Purpose and source boundaries

Use Microsoft's **Engineering lifecycle** areas as the primary teaching structure:
Problem solving, Design, Coding, and Testing. Use its **Technical excellence** areas
to select relevant subjects within that structure. Microsoft's page describes
assessment areas, not a mandatory four-round interview sequence; the numbered stages
here are a DotSkills teaching adaptation.

Keep DDIA as the technical review lens throughout all four stages. Start from the
actual implementation and requirements, not an imagined greenfield system. Explain
existing protections as well as supported issues. Zero findings is a valid outcome.

This remains a code-review skill with guided learning and optional interview practice.
A Coding stage means inspecting and explaining existing code by default. It does not
authorize writing code, editing files, or executing a target skill against real services.
Hands-on coding requires a separate user request and a bounded local/synthetic scope.
An explanation of code does not establish the learner's ability to implement it.

The questions, examples, and DDIA mappings below are original DotSkills adaptations,
not official Microsoft interview questions, a hiring rubric, or conference methodology.
Do not invent DDIA chapter/page citations. Preserve links to preparation sources and
distinguish source principles from inspected evidence and model recommendations.

## Technical excellence topics

Select topics based on the target and the learner's goal; do not cover every area
in every session. State which topics apply and why. The source list is role-dependent,
not a universal mastery checklist.

| Topic | Application within this DDIA tutorial |
| --- | --- |
| Algorithms | Explain relevant computation, complexity, and correctness. |
| Data structures | Compare actual lookup, ordering, memory, and traversal choices. |
| System design and distributed systems | Apply DDIA to ownership, storage, consistency, failure, and scale. |
| AI / ML | When present, inspect data/model pipeline reliability; do not claim DDIA alone evaluates model quality. |
| Data science | When present, examine data correctness and transformations; identify statistical questions needing separate expertise. |
| Computer networking | When relevant, examine protocol behavior, timeouts, retries, and failure assumptions. |

Unrelated ML, statistics, or networking exercises do not become mandatory DDIA checks.
If the user wants a broader exercise outside this skill's scope, explain the boundary.

## The repeated teaching format

For each stage, use a small, relevant selection of the following:

1. **What and why:** explain the stage's goal and why it matters.
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
stay true; idempotency means repeating an operation has the same intended effect;
Big O describes how resource use grows with input size. Use concrete examples before
terminology. Give concise public explanations of evidence and decisions, not private
chain-of-thought. Do not fill every slot mechanically when it adds no teaching value.

In Guided mode, provide the worked answer rather than requiring the user to guess.
In Practice mode, hold back the worked answer until the user responds or requests
help; ask one question at a time. Give feedback on correctness, evidence, clarity,
and trade-offs without inventing a company hiring score. Resume the same stage after
a clarification or explanation request.

Keep teaching examples labeled hypothetical and separate from findings about actual
code. Link the source title when using a research-derived preparation principle;
label target-code evidence and model-proposed recommendations separately.

## Stage 1 — Problem solving

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

## Stage 2 — Design

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

Connect the proposed or existing design to Stage 1's requirements. Discuss ownership,
transaction boundaries, consistency, schema evolution, replication, and recovery only
where applicable. Explain which properties come from a design contract and which still
need implementation verification in Stage 3.

Ask: “What alternative would you consider, and which constraint changes your choice?”
Model an answer that names the invariant, benefit, cost, and evidence needed. Keep
capacity estimates hypothetical unless sourced; use them only when they affect a
decision. Prefer the smallest justified change over an unnecessary redesign.

## Stage 3 — Coding

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

### Analyze algorithms and data structures

Use relevant DSA reasoning alongside DDIA design reasoning. Define n (and m, k, or
other variables) before claiming complexity. Trace loops, lookups, sorting, recursion,
or graph traversal from actual code. Distinguish average, worst-case, and amortized
bounds when they matter; state data-structure assumptions and auxiliary space.

Example questions:
- What is the simplest correct approach, and where does its cost grow?
- Could a set, map, heap, index, or batching help, and what semantics must be preserved?
- How do duplicates, ordering, memory limits, or hot keys change the choice?
- What evidence would justify a cache, queue, replica, or partitioning?
- What changes at 10× load, and which part is only a hypothesis?

Do not equate in-memory Big O with database latency or end-to-end request time.
Database plans, I/O, network calls, contention, payload size, and workload distribution
may dominate. Estimate capacity only when it informs a decision, label assumed
numbers, and show units. Never report a calculation as a measured benchmark.
Do not describe CAP as an unrestricted “pick any two” rule.

Compare the current approach with one justified alternative: benefit, cost, invariant
preserved, and conditions where you would choose differently. Do not recommend
distributed infrastructure merely because it could scale further in theory.
If no meaningful DSA analysis applies, explain that briefly and retain DDIA coverage.

### Optional hands-on practice

For an explicitly requested coding exercise, help the learner choose a familiar
language, propose a small implementation task, and let them write it before showing
a worked solution when in Practice mode. Prefer runnable code for the exercise;
label pseudocode as explanatory rather than a tested implementation. Stay within
authorized local fixtures and carry the result into Stage 4. Do not silently modify
the repository during a review or treat a learning checkpoint as write authorization.

## Stage 4 — Testing

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

Deliver the original review categories: correctness/invariants, data model/consistency,
reliability/operability, testing gaps, and optional improvements. Deduplicate root
causes. Every finding needs inspected evidence, conditions, consequence, smallest
reasonable improvement, claim class, and calibrated severity.

Use confirmed defect, plausible risk, verification gap, and optional improvement
accurately. Explain existing safeguards as well as supported problems. Zero findings
is valid. End with scope, verification limits, and a compact coverage summary.

Then model a short interview recap:
“Here is the goal and invariant; here is the path I inspected; here is the main
supported finding or safeguard; here is the trade-off; here is what I tested and
what still needs evidence.”
Do not invent a defect, certainty, a hiring verdict, or a recommendation to fill
this sentence. Suggest one useful follow-up learning question.

## Worked miniature

This is a hypothetical teaching example, not a finding about the user's repository.

Suppose a batch function keeps the first record for each ID in input order. It scans
an ever-growing list of accepted IDs for every input item. Requirements specify
integer IDs and a maximum batch of 1,000 records; no measured latency is supplied.

- **Stage 1 — Problem solving:** “Must we preserve order and which duplicate wins?” The supplied
  contract says first occurrence wins. Faster code must preserve that behavior.
- **Stage 2 — Design:** Input IDs [7, 2, 7] yields [7, 2]. The third item is skipped.
- **Stage 3 — Coding:** For n distinct records, repeated linear membership scans take O(n²)
  comparisons overall and O(n) storage. A hash set alongside the ordered output
  can give expected O(n) processing and O(n) space, assuming expected O(1) membership.
  It does not guarantee constant-time lookup in every worst case.
- **Explain the trade-off:** A set adds implementation/memory overhead but can reduce
  repeated scans. With bounded batches and no timings, this is an optional improvement,
  not proof of a performance incident.
- **DDIA connection:** In-memory deduplication within one batch does not establish
  idempotency across retried requests or multiple workers. Inspect persistence and
  transaction semantics before claiming either a duplicate-write bug or protection.
- **Stage 4 — Testing:** Propose empty input, repeated IDs, distinct IDs, and first-occurrence/order
  checks. Separately test any established retry contract in isolation. None has run
  merely because this walkthrough described it.

A useful sample answer is: “I would preserve first-occurrence order, replace repeated
membership scans with a set if profiling justifies it, and verify retry safety
separately. Batch deduplication alone does not prove distributed idempotency.”

## Coverage of the Master DDIA rubric

Keep all 15 dimensions even when the tutorial spotlights only a few. Track each as
reviewed (with result), not applicable (why), or not verified (missing evidence).
Do not force irrelevant dimensions into findings.

| Master rubric dimension | Main tutorial stage |
| --- | --- |
| 1. Changed behavior; 2. Match to intent | 1 and 3 |
| 3. Entities/stores/flows; 4. Authoritative values | 2 |
| 5. Access patterns, storage, indexes | 2 and 3 |
| 6. Transactions/invariants; 7. Concurrency; 8. Consistency/ordering | 3 |
| 9. Retries/duplicates; 10. Events/caches/derived views | 3 |
| 11. Schema/encoding compatibility | 3 |
| 12. Replication/partitioning/failover | 2 and 3 |
| 13. Partial failures/recovery | 3 |
| 14. Scale and operability | 2 and 3 |
| 15. Tests of guarantees/failures | 4 |

## Research sources

Checked 2026-10-26. These are preparation sources, not guarantees of interview content.

- [Microsoft — Technical interviewing](https://careers.microsoft.com/v2/global/en/hiring-tips/technical-interviewing.html):
  **primary framework**: Engineering lifecycle provides the four teaching areas;
  Technical excellence supplies role-relevant topic choices. Numbering these areas
  as tutorial stages and embedding DDIA are DotSkills adaptations.
Supplementary sources below inform examples and techniques; they do not define the
primary stage structure.

- [Amazon — Software development interview topics](https://amazon.jobs/content/en-gb/how-we-hire/interview-prep/software-development-topics):
  lists coding, algorithms, data structures, databases, and distributed computing;
  emphasizes applying knowledge rather than memorizing details.
- [Atlassian — Engineering interview handbook](https://www.atlassian.com/company/careers/resources/interviewing/engineering):
  describes practical questions, reliability/cost constraints, and changing trade-offs;
  does not prescribe a single correct solution.
- [Hello Interview — Delivery Framework](https://www.hellointerview.com/learn/system-design/in-a-hurry/delivery):
  proposes requirements, entities/interfaces, high-level design, and deep dives,
  with estimates when they influence a design decision.

The DDIA mapping, stage numbering, questions, and worked miniature are original
model-proposed adaptations for DotSkills. They are not copied company questions or conference methods.
