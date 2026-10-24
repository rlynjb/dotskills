# Code Review Prompt Library

A unified code-review prompt for an AI coding agent, combining five book lenses without running five repetitive reviews:

- **APOSD** — *A Philosophy of Software Design*: complexity, module depth, information hiding, ownership, and change amplification.
- **AT** — *Algorithmic Thinking*: problem definition, algorithmic correctness, data structures, invariants, and complexity.
- **DDIA** — *Designing Data-Intensive Applications*: data ownership, transactions, consistency, idempotency, and failure guarantees.
- **FODE** — *Fundamentals of Data Engineering*: data lifecycle, source and consumer contracts, pipelines, quality, governance, and operations.
- **SDI** — *System Design Interview*: requirements, end-to-end architecture, interfaces, scale, reliability, and evolution.

**Purpose:** Review what changed, establish whether it is correct, identify complexity or risk introduced by the change, and recommend only improvements justified by evidence. Keep the five source libraries as specialized references; this file is the integrated entry point.

A review should answer:

~~~text
Does the change solve the right problem correctly?
Is the implementation understandable and appropriately scoped?
Are the algorithm, data guarantees, lifecycle, and architecture fit for the actual workload?
What evidence supports the conclusions?
What should be fixed now, and what can reasonably wait?
~~~

---

## Evidence and severity calibration (applies to every review prompt)

**Use this rule for master, compact, and focused prompts.** Each copyable
prompt below also includes a concise reminder, so standalone prompts still
calibrate claims. The goal is accuracy, not a long list of possible problems.

- **Ground findings in inspected evidence:** cite actual code, relevant call
  paths, tests, contracts, config, or results. Check existing guards,
  validations, and surrounding behavior before claiming something is missing.
- **Label the claim, not just its severity:**
  - **Confirmed defect:** a contradiction of a supported requirement or a
    reproducible error/failure, with the relevant conditions established.
  - **Plausible risk:** a code-supported failure scenario whose likelihood,
    reachability, or real-world impact still needs verification; state the
    preconditions and uncertainty.
  - **Verification gap:** needed evidence is inaccessible or checks were not
    performed; this is not automatically a bug.
  - **Optional improvement:** a design/performance alternative with a
    justified trade-off, not a defect by default.
- **Calibrate severity separately:** use **blocking** only for an evidenced
  release-stopping correctness, security, data-loss, or agreed-contract issue;
  **important** for consequential supported concerns; **optional** for
  nonurgent improvements. Unknown impact is not automatically high severity.
- **Do not overclaim:** a hypothetical failure is not an observed incident;
  a theoretical complexity concern is not measured slowness; absent tests
  are not proof the code is wrong; code inspection is not proof of production
  behavior, load, cost, or deployment configuration.
- **Report the review boundary:** say whether this is a diff, feature path,
  representative sample, or broader repository inspection. List meaningful
  gaps in files, environments, tests, or tools. Never claim the entire repo
  is safe or free of issues when only part was inspected.
- **State verification honestly:** distinguish tests/benchmarks actually run
  and their outcomes from tests merely read or recommended. Don't invent
  outputs, metrics, exploitability, root causes, or stakeholder intent.
- **Prefer precision over volume:** deduplicate shared root causes and permit
  **zero actionable findings**. If none are supported, say "No actionable
  issues found in the inspected scope," with limitations, not "bug-free."

## Index

| # | Prompt or section | Use it when |
| --- | --- | --- |
| ★ | [Compact daily code-review prompt](#compact-daily-code-review-prompt) | Default for most diffs |
| 0 | [Master five-lens code-review prompt](#0-master-five-lens-code-review-prompt) | Significant changes or comprehensive review |
| 1 | [Understand and trace the change](#1-understand-and-trace-the-change) | Always, before critique |
| 2 | [APOSD — design and complexity](#2-aposd--design-and-complexity) | Module or interface design changed |
| 3 | [AT — algorithms and invariants](#3-at--algorithms-and-invariants) | Logic, collections, or computation changed |
| 4 | [DDIA — data guarantees](#4-ddia--data-guarantees) | Durable data, concurrency, caches, or messaging changed |
| 5 | [FODE — data lifecycle](#5-fode--data-lifecycle) | Data sources, pipelines, models, or consumers changed |
| 6 | [SDI — system architecture](#6-sdi--system-architecture) | APIs, services, dependencies, scale, or operations changed |
| 7 | [Cross-lens synthesis](#7-cross-lens-synthesis) | Several lenses identify the same risk or disagree |
| 8 | [AI-generated change review](#8-ai-generated-change-review) | The change was produced with an AI coding agent |
| 9 | [Finding and verification format](#9-finding-and-verification-format) | Writing actionable review comments |
| — | [Recommended review workflow](#recommended-review-workflow) | Choosing pass order |
| — | [Review principles](#review-principles) | Applying evidence and avoiding overengineering |
| — | [Source prompt libraries](#source-prompt-libraries) | A focused, deeper book-specific review |

---

## How to use this master

Supply the AI coding agent with the diff, PR, changed files, or feature scope. If available, include the requirement, expected behavior, constraints, tests, and production context. Ask it to read the directly affected call sites, contracts, tests, and configuration—not only isolated diff lines.

**Scope the lenses rather than forcing them.** Apply APOSD and basic correctness broadly. Activate AT, DDIA, FODE, or SDI in depth only where the change touches their concerns. Mark other lenses **not applicable** with a short reason; do not invent findings to fill all five categories.

| Lens | Typical triggers | Primary question |
| --- | --- | --- |
| **APOSD** | New modules, abstractions, APIs, responsibilities, state ownership, refactors | Did complexity become better hidden, or merely move to callers? |
| **AT** | Algorithms, loops, traversal, parsing, searches, collections, hot paths | Is the solution correct for its input constraints, and is its cost appropriate? |
| **DDIA** | Databases, writes, events, queues, replicas, caches, migrations | Are the claimed data guarantees true under retries, concurrency, and failure? |
| **FODE** | Ingestion, ETL/ELT, transforms, warehouses, analytics, ML data, backfills | Does the change produce trustworthy data for its actual consumers? |
| **SDI** | Cross-service flows, APIs, storage choices, caching, async work, operations | Does the end-to-end design satisfy the real requirements without excess complexity? |

**Do not confuse cross-cutting concerns with separate findings.** An unclear source of truth may implicate APOSD, DDIA, and SDI, but should usually become **one** finding with several lens tags.

---

## Compact daily code-review prompt

**What it does:** Runs one practical pass across the five lenses, filtering for relevance and prioritizing concrete issues.

~~~text
Review this diff using five book lenses:
APOSD (software design), AT (algorithmic thinking), DDIA (data-intensive systems),
FODE (data engineering), and SDI (system design).

First explain the behavior and requirements affected by the change.
Inspect the directly related call paths, contracts, tests, and configuration.

Evaluate only the lenses that apply:

1. Correctness: changed behavior, invariants, regressions, edge cases, and tests.
2. APOSD: module depth, information hiding, duplicated design knowledge,
   responsibility/state ownership, temporal coupling, and change amplification.
3. AT: problem constraints, algorithm and data-structure choices, invariants,
   boundary inputs, and time/space complexity.
4. DDIA: authoritative data, read/write paths, relevant normalization/
   denormalization and join/query trade-offs, indexes, transactions,
   consistency, ordering, retries, idempotency, schema evolution, and recovery.
5. FODE: source/consumer contracts, ingestion, transformation, lineage,
   quality, governance, orchestration, cost, and operational readiness.
6. SDI: requirements, request/data flow, APIs, storage, bottlenecks,
   sync/async decisions, reliability, observability, and future change.

For each actual finding, provide the exact file/line or symbol, evidence,
expected versus observed or plausible behavior, a concrete scenario, severity
(blocking / important / optional), and the smallest reasonable improvement.

Deduplicate overlaps between lenses. Separate confirmed bugs from risks,
assumptions, and future concerns. If a lens is not relevant, say so briefly.

Do not invent system guarantees or workload requirements.
Do not recommend abstractions, optimizations, or infrastructure without need.
Do not modify the code. End with targeted verification steps.

Calibrate every claim: distinguish CONFIRMED DEFECT, PLAUSIBLE RISK,
VERIFICATION GAP, and OPTIONAL IMPROVEMENT. Provide the evidence and
conditions for each; severity must match demonstrated impact, not a
hypothetical worst case. State what was inspected or actually tested,
and what was not. Zero findings is a valid result.
~~~

---

## 0. Master five-lens code-review prompt

**What it does:** Full integrated review from change intent through correctness, design, data and pipeline guarantees, architecture, and verifiable review comments. Use for larger or higher-risk changes.

~~~text
Act as a pragmatic code reviewer using these five lenses:

- APOSD: A Philosophy of Software Design
- AT: Algorithmic Thinking
- DDIA: Designing Data-Intensive Applications
- FODE: Fundamentals of Data Engineering
- SDI: System Design Interview

Review the supplied change and only the surrounding implementation necessary
to understand its consequences. Do not edit files or make changes.

PASS 1 — ESTABLISH INTENT AND SCOPE
1. Summarize the user/system behavior added, removed, or changed.
2. Identify the requirements, inputs, outputs, constraints, and assumptions.
3. Identify relevant files, call sites, public interfaces, state, data contracts,
   queries, jobs, services, and tests.
4. Distinguish confirmed requirements from inferred requirements. If evidence
   is missing, say what must be checked; do not silently invent context.

PASS 2 — TRACE EXECUTION AND DATA
5. Trace the affected path from entry point to outcome:
   input -> validation -> computation -> state/read/write -> output/side effect.
6. For multi-component changes, show an ASCII flow diagram when it helps.
7. Identify state owners and sources of truth; mark synchronous/asynchronous
   boundaries, external calls, failure points, and data transformations.
8. Trace at least one normal path and the relevant error, retry, concurrent,
   and boundary paths. State where tracing was limited by missing code.

PASS 3 — APPLY THE RELEVANT LENSES

APOSD — SOFTWARE DESIGN
9. Do modules hide meaningful complexity, or expose details to their callers?
10. Are abstractions shallow, responsibilities scattered, interfaces bloated,
    design knowledge duplicated, or call ordering implicitly required?
11. Is mutable state owned clearly? Are error details translated at the right
    boundary? Will a likely future change require unrelated edits?
12. Are names and control flow obvious, and do tests depend on behavior rather
    than fragile internal implementation details?

AT — ALGORITHMIC THINKING
13. Is the problem correctly represented, including constraints and input
    assumptions? Does the chosen algorithm/data structure fit the operations?
14. State the key invariants, where established and preserved, and how the
    algorithm terminates and produces the desired result.
15. Probe counterexamples: empty, minimal, maximal, duplicate, malformed,
    adversarial, or boundary inputs as relevant.
16. Analyze time and auxiliary space growth, and identify any performance
    problem under a realistic workload—not only theoretical Big-O.

DDIA — DATA AND DISTRIBUTED GUARANTEES
17. Identify entities, identifiers, models, schemas, authoritative stores,
    read/write paths, and access patterns. Are indexes and queries suitable?
    For relevant relational changes, examine normalization vs. denormalization,
    join keys/cardinality, N+1 queries, indexes, and query-plan evidence.
    Compare read/query costs against duplicated storage, write/update cost,
    freshness, and consistency. Do not assume joins are inherently slow.
18. Review atomicity, isolation, concurrency anomalies, consistency,
    ordering, retry safety, duplicate effects, and idempotency.
19. Review caches, events, queues, projections, schema/encoding evolution,
    migrations, replicas, partitions, and partial-failure recovery if present.
20. Describe guarantees the implementation actually proves. Do not infer
    exactly-once behavior, durability, strong consistency, or recoverability
    from library names, acknowledgments, or optimistic comments.

FODE — DATA ENGINEERING LIFECYCLE
21. Locate the change in generation -> storage -> ingestion ->
    transformation -> serving. Identify its upstream owners and consumers.
22. Review source contracts, format/grain, late or missing data, schema drift,
    replay, deduplication, transformation meaning, lineage, and freshness.
23. Check consumer expectations, quality tests, metadata, ownership, privacy,
    access control, retention, and governance proportionate to data sensitivity.
24. Review orchestration dependencies, backfills, DataOps, reproducibility,
    observability, rollback, cost, and operational ownership if relevant.
25. Do not confuse a successful pipeline run with trustworthy consumer data.

SDI — SYSTEM DESIGN
26. Relate the design to functional and non-functional requirements:
    latency, availability, throughput, consistency, and cost as applicable.
27. Trace end-to-end requests, service/API boundaries, storage, network calls,
    caching, synchronous vs asynchronous work, and failure propagation.
28. Identify real bottlenecks, fan-out, unnecessary coupling, reliability gaps,
    recovery behavior, and useful metrics/logs/tracing.
29. Consider realistic growth and evolution, without assuming extreme scale
    or introducing distributed components without demonstrated need.

PASS 4 — RECONCILE AND PRIORITIZE
30. Group repeated observations into a single root-cause finding.
31. Separate proven defects, plausible risks, unverified assumptions, and
    optional design opportunities. State which lens or lenses support each.
32. Judge tradeoffs against current behavior and constraints. Prefer the
    smallest correct improvement; do not optimize for abstract purity.
33. Review test evidence for changed behavior, invariants, boundaries,
    concurrency, data quality, failure/recovery, and integration contracts.

REQUIRED OUTPUT

1. Change summary — behavior, scope, and constraints.
2. Lens applicability — APOSD / AT / DDIA / FODE / SDI:
   applicable, limited, or not applicable, with one-line reasons.
3. Execution/data-flow trace — concise steps or ASCII diagram if useful.
4. Findings — ordered blocking, important, optional. Each finding includes:
   - Descriptive title and lens tags
   - Exact file and line/symbol/contract evidence
   - Problem and concrete consequence
   - Reproduction, input, event sequence, workload, or failure scenario
   - Expected vs actual behavior, or explicitly qualified risk
   - Smallest reasonable improvement
   - Verification/test that would support the recommendation
5. Verification gaps — what was tested, what was not, and which assumptions
   require code, configuration, infrastructure, or production evidence.
6. Overall assessment — highest-priority action and whether any blockers remain.

If no actionable issues are found, say so. Do not generate speculative findings
to satisfy the template. Review security, privacy, accessibility, and ordinary
correctness where relevant; the book lenses do not replace these checks.

Evidence calibration: check the relevant surrounding code, tests,
contracts, and configuration before declaring a defect. Distinguish
confirmed defects, plausible code-backed risks, verification gaps,
and optional improvements; attach preconditions to uncertain claims.
Severity must follow supported impact; do not label speculative future
scale, unmeasured latency, or unknown deployment behavior as a blocker.
Report the reviewed scope and which tests or checks were actually run.
If no actionable issues are supported, report zero findings with limits
rather than implying the entire repository is defect-free.
~~~

---

## 1. Understand and trace the change

**What it does:** Builds the factual map shared by every lens. Review intent before implementation style.

~~~text
Before reviewing this change, reconstruct the behavior it implements.

Identify:
- Requirement and expected user/system outcome
- Entry point, inputs, validation, outputs, and side effects
- The execution path through functions, modules, services, and tools
- What data is generated, read, transformed, stored, cached, or emitted
- Authoritative state and owners of each important decision
- Error, retry, concurrency, and edge paths relevant to this change
- Tests and contracts that establish expected behavior

Use a concise ASCII flow diagram if the path crosses several components.
List what is proven from the code versus what is assumed or unavailable.

Do not critique architecture until this path is understood.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
~~~

---

## 2. APOSD — design and complexity

**What it does:** Finds complexity that leaks across boundaries or makes future changes unnecessarily expensive.

~~~text
Review the change through A Philosophy of Software Design.

For each relevant module or interface, ask:
- What complexity is hidden from callers? Is the module deep or shallow?
- Does a wrapper merely rename or forward operations?
- Is design knowledge duplicated, even if code text is not?
- Who owns each responsibility, rule, validation, and mutable state value?
- Are callers forced to know implementation details or temporal call ordering?
- Do interface parameters, flags, error types, or side effects leak complexity?
- Will a plausible next change require edits in many unrelated locations?
- Do tests exercise public behavior or couple to private implementation steps?

Find concrete design costs and the smallest localized repair.
Do not add a layer merely to reduce line count or satisfy a pattern.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
~~~

**Highest-value connections:** APOSD ownership should agree with DDIA's system of record and SDI's service boundaries. APOSD change amplification should agree with FODE's source/consumer contract evolution.

---

## 3. AT — algorithms and invariants

**What it does:** Verifies not only that a solution looks plausible, but why it is correct for the problem and constraints.

~~~text
Review this logic through Algorithmic Thinking.

1. Define the problem, input/output contract, constraints, and assumptions.
2. Identify the chosen algorithm, representation, data structures, and
   operations performed most frequently.
3. State each important invariant and show initialization, preservation,
   termination, and why it implies the result is correct.
4. Try counterexamples covering relevant boundary and adversarial inputs.
5. Derive time and auxiliary-space complexity using actual input dimensions.
6. Compare alternatives only if constraints or measured workload justify them.
7. Check tests for input classes, invariants, and regression counterexamples.

For each issue, give a failing input or a concrete scale scenario, and the
smallest justified fix. Distinguish proof, assumption, and optimization.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
~~~

**Highest-value connections:** Algorithm-level improvements do not automatically improve SDI's end-to-end latency; check I/O, remote calls, storage, and fan-out before prioritizing an optimization.

---

## 4. DDIA — data guarantees

**What it does:** Tests claims about durable state and behavior under concurrent, duplicate, stale, reordered, or failed operations.

~~~text
Review the affected data paths through Designing Data-Intensive Applications.

For every relevant value, operation, or event:
- Which store is authoritative? Which copies are derived or cached?
- What are the read/write paths, transactions, isolation level, and indexes?
- If relational queries matter, how do join keys/cardinality, indexes, query
  counts, and available plans/timings affect performance at the real workload?
- Would normalized read-time joins or stored denormalized/derived data better
  meet those needs, considering write overhead, duplication, consistency,
  freshness, and refresh/invalidation responsibilities?
- What happens under two concurrent operations or a partial write?
- What happens after timeout, crash, retry, redelivery, or replay?
- Which effects are idempotent? What key or constraint enforces that?
- What consistency and ordering guarantees can callers really rely on?
- How are schema evolution, migrations, backfills, and stale readers handled?
- How do recovery, replication, partitioning, and operational tooling affect it?
- Which tests or infrastructure settings prove these guarantees?

Use one explicit event sequence or concurrency interleaving per risk.
Treat performance as measured only when plans/benchmarks support it;
otherwise identify what to measure and label estimates as hypothetical.
Distinguish documented expectation from implemented guarantee.
Do not claim exactly once, atomicity, durability, or strong consistency
without supporting evidence.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
~~~

**Remember:** Retry is not idempotency. Acknowledgment is not exactly once. Replication is not a backup. A cache is not automatically a source of truth.

---

## 5. FODE — data lifecycle

**What it does:** Follows data from its origin to its consumers, including the organizational and operational contracts around the code.

~~~text
Review this data-affecting change through Fundamentals of Data Engineering.

Trace generation -> storage -> ingestion -> transformation -> serving.

Identify:
- Upstream systems, owners, extraction constraints, and contracts
- Storage location, data grain, format, partitioning, and retention
- Ingestion mode; late data, schema drift, checkpoints, replay, and dedupe
- Transformations, joins, null rules, business definitions, lineage,
  incremental behavior, and freshness expectations
- Named downstream consumers and their access, quality, and SLA needs
- Sensitive data, least privilege, governance, ownership, and metadata
- Scheduling, dependency management, backfills, reproducibility, DataOps,
  rollback, quality alerts, and incident recovery
- Tool costs and ongoing operational burden relative to actual needs

Report a concrete consumer or pipeline consequence, not a generic
recommendation to adopt more tools. A pipeline that runs is not necessarily
a pipeline that serves correct, trustworthy data.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
~~~

**Highest-value connections:** DDIA asks whether data updates have valid guarantees; FODE asks whether trustworthy data arrives with the right meaning, freshness, ownership, and availability for the consumer.

---

## 6. SDI — system architecture

**What it does:** Tests the behavior of the whole request path against real requirements, scale, and operational constraints.

~~~text
Review this change through System Design Interview principles.

Start with functional and non-functional requirements, not technology choices.

Trace the affected request and data flow across components, APIs, network
calls, state stores, caches, queues, background workers, and the response path.

Check:
- Clear responsibilities, API contracts, and data ownership
- Sequential calls, fan-out, N+1 behavior, and likely bottlenecks
- Storage/read/write fit and the first actual capacity constraint
- Cache correctness, freshness, ownership, and invalidation
- Why work is synchronous or asynchronous
- Timeout, retry, backpressure, degraded operation, and recovery behavior
- Availability, latency, throughput, consistency, monitoring, tracing,
  operational readiness, and realistic future change

Differentiate a current defect from a future limit. State the workload or
requirement that makes any infrastructure change worthwhile.
Prefer the simplest architecture that meets current constraints.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
~~~

---

## 7. Cross-lens synthesis

**What it does:** Reconciles overlapping observations instead of emitting multiple reviews that contradict or repeat one another.

| Intersection | Reconciliation question |
| --- | --- |
| APOSD + AT | Does the simplest clear design still preserve algorithmic correctness and needed performance? |
| APOSD + DDIA | Is there one explicit owner for each invariant and source of truth? |
| APOSD + SDI | Does a new boundary actually hide complexity, or add another hop and more coupling? |
| AT + SDI | Is local compute really the bottleneck, or is end-to-end I/O dominating? |
| DDIA + FODE | Are update/replay guarantees consistent with pipeline freshness, lineage, and data quality? |
| DDIA + SDI | Do storage and consistency choices satisfy user-visible requirements under failure? |
| FODE + SDI | Is the serving architecture proportionate to downstream workload, SLAs, and operational cost? |

~~~text
Combine the five lens assessments into one prioritized review.

For every overlapping concern:
1. Identify the underlying root cause, not five descriptions of the symptom.
2. State which lenses apply and where they agree or disagree.
3. Explain the specific correctness, maintenance, performance, data,
   operational, or cost tradeoff.
4. Recommend the smallest intervention that addresses the proven risk.
5. Separate immediate fixes from concerns that require additional evidence.

Never recommend a deeper abstraction, faster algorithm, stronger data
guarantee, new pipeline tool, or distributed component solely on principle.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
~~~

---

## 8. AI-generated change review

**What it does:** Adds skepticism when a coding agent has generated a plausible but unverified implementation.

~~~text
Review this AI-generated change using all relevant master lenses.

Look for:
- Invented requirements, configuration assumptions, or unverified APIs
- Plausible-looking algorithm errors and unhandled boundary inputs
- Shallow wrappers, needless abstractions, duplicated rules, scattered state
- Unsubstantiated claims about transactions, exactly-once effects, retries,
  consistency, cache freshness, or recoverability
- A successful-looking data pipeline with missing contracts or quality checks
- Premature caches, services, queues, distributed scaling, or platform tools
- Tests that only mock implementation details or mirror the generated logic
- Missing evidence about real workloads, failures, costs, and operations

Identify concrete faults without penalizing code simply because AI wrote it.
Avoid rewriting working code solely for elegance. Separate confirmed findings
from suspicions requiring tests or environment verification.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
~~~

---

## 9. Finding and verification format

Use one set of findings, **not five parallel lists**. Each item can carry multiple lens tags.

~~~text
[Blocking | Important | Optional] Concise title
Lenses: APOSD / AT / DDIA / FODE / SDI (only applicable tags)
Location: path:line, symbol, API, schema, query, job, or config
Evidence: what the relevant code/config/test actually shows
Impact: concrete failure, confusion, cost, or change-amplification consequence
Scenario: input, timeline, concurrent sequence, workload, or consumer example
Expected vs actual: observed behavior, or a clearly qualified potential risk
Recommendation: smallest reasonable improvement
Verification: focused test, inspection, metric, or reproduction

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
~~~

**Severity:**

| Severity | Standard |
| --- | --- |
| **Blocking** | Demonstrable wrong behavior, broken invariant/contract, credible security or data-loss issue, or unacceptable risk that should be addressed before merging |
| **Important** | Material maintainability, reliability, performance, data-quality, or operational issue supported by the change and realistic usage |
| **Optional** | Justified simplification or improvement that does not block the current requirements |

When evidence is unavailable, identify a **verification gap**, not an invented bug. Cite code locations whenever possible; if only a diff or summary was supplied, say what could not be inspected.

Example of a strong finding:

~~~text
[Blocking] Retry can apply a purchase twice
Lenses: DDIA, SDI
Location: src/payments/consumer.ts:handlePayment
Evidence: The handler writes a payment but does not guard against a repeated
event ID. The queue may redeliver an unacknowledged message.
Impact: A timed-out worker could write the same business effect again.
Scenario: Handler commits; acknowledgment fails; message is redelivered.
Recommendation: Persist an idempotency key with the business effect using
a transaction/unique constraint appropriate to the store.
Verification: Replay the same event ID twice and assert one durable effect.
~~~

Do not manufacture findings to populate every severity or lens.

---

## Recommended review workflow

1. **Understand before judging.** Read the diff, requirements, affected call paths, contracts, state ownership, and tests.
2. **Run the compact review.** Establish correctness first and select only applicable lenses.
3. **Deepen selectively.** Use the master or focused lens prompts for substantial risks. Follow the linked source libraries when a specialized review is needed.
4. **Trace real scenarios.** Construct counterexamples, concurrent/retry timelines, consumer journeys, failure paths, or representative workloads.
5. **Verify evidence.** Read tests, schema, settings, and infrastructure where accessible. Run relevant tests when permitted; report explicitly when they were not run.
6. **Consolidate.** Deduplicate overlapping lens comments; rank blocking, important, and optional.
7. **Report concisely.** Provide actionable findings and verification. If nothing actionable is found, say so with any important limits to confidence.

---

## Review principles

- **Correctness before elegance.** First establish that changed behavior meets requirements.
- **Evidence before claims.** Code, contracts, tests, and infrastructure establish guarantees; names, frameworks, and comments do not.
- **Context before optimization.** Algorithms, databases, queues, and platforms must fit actual input sizes, traffic, data volume, and team constraints.
- **Prefer localized complexity.** Reward modules that hide complexity, not extra layers that spread it.
- **Look at the whole flow.** Follow data and effects through the system rather than reviewing a function, database, or service in isolation.
- **Treat consumers as part of correctness.** A technically successful transform can still serve inaccurate, stale, insecure, or unusable data.
- **Separate now from later.** Current defects, justified risks, and speculative future improvements have different priorities.
- **Do not equate coverage with confidence.** Tests must exercise contracts, invariants, failure modes, and user-visible results.
- **Respect review scope.** Do not modify source code unless explicitly asked. Do not assert that tests ran if they did not.
- **Be useful to the developer.** Every actionable comment should explain why it matters and how to verify the smallest change.

---

## Source prompt libraries

The master integrates the common decision process. Keep these files for deeper, targeted prompts and examples:

| Lens | Original library |
| --- | --- |
| APOSD | [code-review-aposd.md](./code-review-aposd.md) |
| AT | [code-review-at.md](./code-review-at.md) |
| DDIA | [code-review-ddia.md](./code-review-ddia.md) |
| FODE | [code-review-fode.md](./code-review-fode.md) |
| SDI | [code-review-sdi.md](./code-review-sdi.md) |
