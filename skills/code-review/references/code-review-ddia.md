# DDIA Code-Review Prompt Library

Quick-reference for reviewing a change with an AI coding agent, using *Designing Data-Intensive Applications* to judge whether the change preserves correctness, makes data guarantees explicit, handles failure safely, and scales in ways consistent with its real workload.

A normal review asks:

```text
Does this code work?
Are there bugs?
Are there tests?
```

A DDIA review also asks:

```text
What data is read or written?
Which store is authoritative?
What happens under concurrency, retries, lag, or partial failure?
What consistency and ordering guarantees does the user actually receive?
Will this still be correct when the data, traffic, or number of nodes grows?
```

DDIA should **complement, not replace** reviews for ordinary correctness, security, accessibility, maintainability, and product behavior.

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

| #  | Prompt                                                                      | What it does                                                             | Reach for it when                              |
| -- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------- |
| ★  | [**Compact daily**](#compact-daily-code-review-prompt)                      | 11-point pass in one shot, blocking vs optional                          | Default for data-affecting diffs               |
| 0  | [**Master**](#0-master-ddia-code-review-prompt)                             | Full 15-point review → 5 finding buckets                                 | Bigger or higher-risk data changes             |
| 1  | [**Understand the change**](#1-understand-the-change-first)                 | Reconstructs behavior and data flow before critique                      | First — don't review what you don't understand |
| 2  | [**Correctness**](#2-review-correctness)                                    | Bugs, races, duplicates, stale data, and partial failure                 | Always, before architecture                    |
| 3  | [**Data model**](#3-review-the-data-model)                                  | Entities, identifiers, invariants, normalization, ownership              | Schema or domain model changed                 |
| 4  | [**System of record**](#4-review-data-ownership-and-the-system-of-record)   | Authoritative vs derived data                                            | Multiple stores or caches exist                |
| 5  | [**Queries and indexes**](#5-review-queries-and-indexes)                    | Access patterns, scans, indexes, joins, pagination                       | Database queries changed                       |
| 6  | [**Transactions**](#6-review-transactions-and-concurrency)                  | Atomicity, isolation, lost updates, write skew                           | Multi-step or concurrent writes                |
| 7  | [**Consistency**](#7-review-consistency-and-ordering)                       | Read-your-writes, monotonicity, ordering, stale reads                    | Replicas, async flows, projections             |
| 8  | [**Idempotency**](#8-review-idempotency-retries-and-duplicate-effects)      | Safe retries and duplicate suppression                                   | APIs, workers, queues, webhooks                |
| 9  | [**Events and streams**](#9-review-events-queues-and-stream-processing)     | Delivery, ordering, offsets, replay, schema                              | Event-driven change                            |
| 10 | [**Derived data**](#10-review-caches-indexes-and-derived-data)              | Caches, projections, search indexes, rebuildability                      | Multiple representations changed               |
| 11 | [**Schema evolution**](#11-review-schema-and-encoding-evolution)            | Backward/forward compatibility and rollout safety                        | Schema or event format changed                 |
| 12 | [**Replication and partitioning**](#12-review-replication-and-partitioning) | Lag, failover, shard keys, hotspots, fan-out                             | Distributed storage involved                   |
| 13 | [**Failure and recovery**](#13-review-failure-handling-and-recovery)        | Partial failure, reconciliation, backups, repair                         | High-reliability path                          |
| 14 | [**Scale and operability**](#14-review-scale-and-operability)               | 10×/100× probes, monitoring, backpressure, capacity                      | Performance or production risk                 |
| 15 | [**Tests as guarantee evidence**](#15-review-tests-as-guarantee-evidence)   | Tests for invariants, concurrency, retry, and recovery                   | Reviewing test changes                         |
| A  | [**AI-generated change**](#a-reviewing-an-ai-generated-change)              | Skeptical pass for invented guarantees and distributed-system overdesign | Diff came from an agent                        |
| B  | [**Single query or write path**](#b-review-a-single-query-or-write-path)    | Zoomed review of one data operation                                      | Investigating a hot path                       |
| C  | [**New datastore or queue**](#c-review-a-new-datastore-cache-or-queue)      | Whether new infrastructure earns its complexity                          | New database, cache, broker, or index          |
| D  | [**Migration or backfill**](#d-review-a-migration-or-backfill)              | Rollout, compatibility, resumability, verification                       | Schema/data migration                          |
| E  | [**Review comments**](#e-producing-useful-review-comments)                  | Concrete, scenario-based, severity-tagged output                         | Turning findings into PR comments              |

Reference (not prompts): [Review workflow](#recommended-review-workflow) · [Manual-review questions](#questions-to-remember-during-manual-review) · [The four reviews](#the-overall-model)

---

## Compact daily code-review prompt

**What it does:** Runs the DDIA review as a single 11-point pass and separates blocking problems from optional improvements.

```text
Review this diff using principles from Designing Data-Intensive Applications.

Focus on:

1. Behavioral correctness and violated invariants
2. Data model and ownership
3. Read and write paths
4. Transactions and concurrency
5. Consistency and ordering
6. Idempotency and retry safety
7. Events, queues, and derived data
8. Schema compatibility
9. Failure and recovery
10. Scale and operational impact
11. Test quality

For every finding, provide:

- Evidence
- Concrete consequence
- Severity
- A realistic failure or workload scenario
- Smallest recommended improvement

Separate blocking issues from optional design improvements.

Do not claim atomicity, exactly-once delivery, strong consistency, durability,
or scalability unless the implementation and infrastructure prove it.

Calibrate every claim: distinguish CONFIRMED DEFECT, PLAUSIBLE RISK,
VERIFICATION GAP, and OPTIONAL IMPROVEMENT. Provide the evidence and
conditions for each; severity must match demonstrated impact, not a
hypothetical worst case. State what was inspected or actually tested,
and what was not. Zero findings is a valid result.
```

---

## 0. Master DDIA code-review prompt

**What it does:** The full 15-point pass producing five finding buckets. Each finding must be tied to a concrete workload, concurrency, or failure scenario.

```text
Review this change using principles from Designing Data-Intensive Applications.

Do not focus only on style or the happy path.

Evaluate:

1. What user or system behavior the change introduces or modifies.
2. Whether the implementation matches the intended behavior.
3. Which data entities, schemas, stores, and data flows are affected.
4. Which store is authoritative for each important value.
5. Whether the read and write access patterns match the storage and indexes;
   where relevant, compare normalized joins with denormalized/derived reads,
   including performance evidence, update cost, and freshness trade-offs.
6. Whether transaction boundaries preserve all important invariants.
7. Whether concurrent operations can produce anomalies.
8. What consistency and ordering guarantees the feature provides.
9. Whether retries, duplicate requests, or redelivery are safe.
10. Whether events, queues, caches, and derived views remain consistent enough.
11. Whether schema and encoding changes are backward and forward compatible.
12. Whether replication, partitioning, or failover assumptions are safe.
13. Whether partial failures and ambiguous outcomes are recoverable.
14. Whether the design remains safe and operable at 10× or 100× scale.
15. Whether tests verify the important guarantees and failure cases.

Separate findings into:

- Correctness and invariant issues
- Data-model and consistency issues
- Reliability and operability risks
- Testing gaps
- Optional improvements

For every finding:

- Cite the file, symbol, query, schema, migration, or configuration
- Explain the concrete consequence
- Give a realistic event sequence, concurrency scenario, or workload
- Suggest the smallest reasonable improvement
- Mark it as blocking, important, or optional

Clearly separate guarantees proven by code or configuration from assumptions.

Do not recommend distributed infrastructure merely because it could scale
further in theory.

Evidence calibration: check the relevant surrounding code, tests,
contracts, and configuration before declaring a defect. Distinguish
confirmed defects, plausible code-backed risks, verification gaps,
and optional improvements; attach preconditions to uncertain claims.
Severity must follow supported impact; do not label speculative future
scale, unmeasured latency, or unknown deployment behavior as a blocker.
Report the reviewed scope and which tests or checks were actually run.
If no actionable issues are supported, report zero findings with limits
rather than implying the entire repository is defect-free.
```

---

## 1. Understand the change first

**What it does:** Forces the agent to reconstruct the actual data behavior before criticizing it.

```text
Explain this change before reviewing it.

Identify:

- The user or system behavior being changed
- The entry points affected
- The main read and write paths
- Data entities and fields involved
- Stores read or written
- The system of record
- Transaction boundaries
- Events, queues, caches, or projections involved
- Existing behavior being replaced
- Important invariants
- Freshness and ordering expectations
- Assumptions made by the implementation

Separate what is directly confirmed by the diff from what you inferred.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 2. Review correctness

**What it does:** Standard correctness pass expanded for data-intensive failure modes.

```text
Review this change for behavioral and data correctness.

Look for:

- Incorrect assumptions
- Missing branches
- Null or undefined values
- Invalid state transitions
- Boundary conditions
- Race conditions
- Lost updates
- Read-modify-write conflicts
- Write skew
- Duplicate operations
- Out-of-order updates
- Stale data
- Partial success
- Ambiguous timeout outcomes
- Unsafe retries
- Backward compatibility problems
- Runtime values that violate static types
- Incorrect query filters
- Missing tenant or authorization constraints

For each issue, provide a concrete input, event sequence, or concurrent
execution that demonstrates the failure.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 3. Review the data model

**What it does:** Checks whether the logical model represents the domain clearly and preserves its invariants.

```text
Review every data entity, schema, document, event, or record introduced or
changed by this patch.

For each one, identify:

- Meaning
- Identifier
- Fields
- Relationships
- Cardinality
- Required and optional values
- Invariants
- Lifecycle
- Ownership
- Retention and deletion behavior
- Derived fields
- Denormalized fields
- Versioning fields

Look for:

- Unstable or ambiguous identifiers
- Missing uniqueness constraints
- Invalid states representable by the schema
- Relationships enforced only by application convention
- Fields with unclear ownership
- Mixed concerns in one record
- Unbounded collections
- Arrays or documents that can grow indefinitely
- Denormalized values without an update strategy
- Duplicated data whose writers, refresh path, or consistency rules are unclear
- Timestamps being used as unreliable ordering guarantees
- Soft deletion that queries may forget to honor

For relational changes, distinguish normalized facts and relationships from
persisted denormalized/derived copies. Explain the trade-off using this
implementation: read-time joins versus cheaper or simpler reads from copies,
balanced against extra storage, write amplification, update anomalies,
freshness, and consistency. Identify the system of record and how copies
are kept in sync. Do not claim either model is automatically superior.

Explain whether the data model makes valid states easy to represent and invalid
states difficult to create.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 4. Review data ownership and the system of record

**What it does:** Distinguishes authoritative data from caches, projections, indexes, and copies.

```text
Map the ownership of every important value affected by this change.

For each value, identify:

- System of record
- Authoritative writer
- Readers
- Other stores containing a copy
- Derived representations
- Cache representations
- Search-index representations
- Event representations
- Reconciliation mechanism
- Conflict-resolution rule
- Deletion propagation

Look for:

- Multiple writable sources of truth
- Derived data treated as authoritative
- Two services independently owning the same field
- Writes made directly to a projection
- Cache values that cannot be reconstructed
- Conflicting copies without a winner
- Ownership encoded only in tribal knowledge

For every duplicated representation, explain how updates propagate and what
happens when the copies disagree.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 5. Review queries and indexes

**What it does:** Checks whether the physical access strategy matches real reads and writes.

```text
Review every important query changed or introduced by this patch.

For each query, identify:

- Store
- Table, collection, or index
- Filter conditions
- Join conditions and join keys, including relationship cardinality
- Sort order
- Pagination approach
- Expected result size
- Expected frequency
- Relevant indexes
- Whether the index covers the query
- Locking behavior
- Query count per user request
- Projection/selected columns and any ORM-generated queries

Look for:

- Full scans
- Missing indexes
- Redundant indexes
- Incorrect composite-index order
- N+1 queries
- Unbounded result sets
- Offset pagination on large or changing datasets
- Queries that cannot use an index
- Large joins or fan-out
- Per-row remote calls
- Accidental cross-tenant reads
- Read amplification
- Write amplification caused by new indexes

For relational queries, explain what each join contributes to the result and
whether join fan-out, row counts, filter selectivity, indexes, data returned,
or N+1 lookups materially affect the read path. Trace the result to its
consumer using the existing data-flow evidence, without inventing another
flow. Where available, interpret query plans (e.g., EXPLAIN), timing,
query-count, or workload evidence; distinguish measured bottlenecks from
hypotheses and do not run production queries or EXPLAIN ANALYZE.

If useful, compare a read-time join with a stored derived/denormalized
representation and state the read latency, write/update work, storage,
freshness, and consistency trade-offs. Identify what evidence would justify
the alternative; do not prescribe denormalization merely because joins exist.

For each performance finding, describe the workload or data size at which it
becomes significant.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 6. Review transactions and concurrency

**What it does:** Reconstructs atomicity and isolation and tests every important invariant under concurrency.

```text
Review every transaction and multi-step write affected by this change.

For each operation, identify:

- Reads performed
- Writes performed
- Transaction start and end
- Isolation level
- Locks
- Optimistic concurrency checks
- Version or compare-and-set fields
- Unique and foreign-key constraints
- External side effects
- Retry behavior
- Timeout behavior

List every invariant that must remain true.

For each invariant, explain whether it is protected by:

- Database constraint
- Atomic statement
- Serializable transaction
- Lock
- Optimistic concurrency
- Single-writer design
- Idempotency key
- Application-level check
- Nothing visible

Search for:

- Lost updates
- Check-then-act races
- Double creation
- Double spending
- Write skew
- Read skew
- Phantom-dependent behavior
- External API calls inside transactions
- Events published before commit
- Events published after commit without atomic coordination
- Long-running transactions
- Deadlock risks

Use explicit interleavings to demonstrate concurrency problems.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 7. Review consistency and ordering

**What it does:** Forces precise statements about what readers and writers can observe.

```text
Review the consistency and ordering guarantees affected by this change.

Evaluate:

- Read-your-writes
- Monotonic reads
- Monotonic writes
- Consistent-prefix reads
- Causal ordering
- Per-key ordering
- Global ordering
- Snapshot consistency
- Linearizability
- Eventual consistency

For each relevant guarantee, explain:

- Whether user behavior requires it
- What mechanism provides it
- What evidence confirms it
- Where it can fail
- What the user or downstream system observes

Look for:

- Reads routed to lagging replicas after writes
- Old events overwriting newer state
- Timestamps used as total ordering
- Multiple consumers applying updates in different orders
- UI optimistic state diverging from server state
- Sequential operations processed concurrently
- Projections exposing partial logical updates
- Failover causing apparent time reversal

Replace vague phrases such as "eventually consistent" with a concrete account
of what can be stale, for how long, and with what consequence.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 8. Review idempotency, retries, and duplicate effects

**What it does:** Tests whether retrying after timeouts or redelivery can repeat business effects.

```text
Review every operation that may be retried, replayed, or delivered more than
once.

Consider:

- HTTP requests
- Webhooks
- Queue messages
- Scheduled jobs
- Background workers
- Database retries
- Client retries
- Manual reprocessing
- Event replay

For each operation, identify:

- Idempotency key
- Deduplication store
- Uniqueness constraint
- Processing marker
- Atomicity between deduplication and side effect
- Expiration policy
- Replay behavior
- External side effects
- Response returned for a duplicate

Look for:

- Deduplication recorded after the effect
- In-memory deduplication only
- Keys scoped too broadly or too narrowly
- Retried payment, email, inventory, or notification effects
- Consumers acknowledging before durable completion
- Failed operations marked complete
- Retries that change request meaning
- Non-idempotent upserts
- Duplicate events emitted after transaction retries

State the effective guarantee precisely:

- At-most-once
- At-least-once
- Effectively once for a bounded side effect
- Unknown

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 9. Review events, queues, and stream processing

**What it does:** Reviews delivery semantics, schema, ordering, replay, consumer state, and hidden coupling.

```text
Review every event, queue, log, or stream affected by this change.

Identify:

- Producer
- Event schema
- Broker, topic, or queue
- Partition key
- Ordering scope
- Consumer groups
- Consumers
- Offset or acknowledgement mechanism
- Retry policy
- Dead-letter behavior
- Retention
- Replay behavior
- Duplicate-delivery behavior
- Failure handling

Check whether:

- Publication is atomic with the source write
- Consumers are idempotent
- Event order is assumed but not guaranteed
- One poison message blocks a partition
- Acknowledgement happens too early
- Payloads omit data needed for replay
- Consumers depend on mutable external state
- Event schemas break delayed consumers
- Side effects are repeated during replay
- Reprocessing produces a different result
- Events describe facts or ambiguous commands
- Consumers rely on producer implementation details

Do not describe the flow as exactly once unless every relevant side effect is
covered by a proven end-to-end mechanism.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 10. Review caches, indexes, and derived data

**What it does:** Reviews secondary representations for freshness, invalidation, reconstruction, and disagreement handling.

```text
Review every cache, search index, materialized view, projection, aggregate, or
denormalized representation affected by this change.

For each one, identify:

- Source data
- Update mechanism
- Synchronous or asynchronous update
- Freshness expectation
- Cache key or document identifier
- Invalidation mechanism
- Rebuild process
- Backfill process
- Failure behavior
- Conflict rule
- Whether users read it directly

Look for:

- Cache invalidation before a transaction commits
- Database write succeeding while cache invalidation fails
- Unbounded cache staleness
- Cache stampedes
- Missing tenant or version information in keys
- Search documents that cannot be reconstructed
- Projections with no replay or reconciliation path
- Writes made to derived stores
- Derived values duplicated in multiple pipelines
- Deletes not propagating
- Old asynchronous updates overwriting newer values

Ask whether the derived representation can be deleted and rebuilt safely.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 11. Review schema and encoding evolution

**What it does:** Evaluates rolling deployments, delayed consumers, stored historical data, and replay compatibility.

```text
Review every schema or encoded data format changed by this patch.

Consider:

- Database schema
- API requests and responses
- JSON
- Protobuf
- Avro
- Events
- Cache values
- Search documents
- Export formats

For each change, identify:

- Producers
- Consumers
- Old readers
- Old writers
- New readers
- New writers
- Required fields
- Optional fields
- Defaults
- Unknown-field behavior
- Migration sequence
- Rollback behavior

Evaluate:

- Backward compatibility
- Forward compatibility
- Rolling-deployment safety
- Historical-data compatibility
- Event-replay compatibility
- External-client compatibility

Look for:

- Removing or renaming fields immediately
- Changing field meaning without versioning
- Type changes that old code cannot parse
- New required fields without defaults
- Enum additions that old consumers reject
- Destructive migrations before all readers change
- Dual-write periods with no reconciliation
- Application deployment depending on an instantaneous schema change

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 12. Review replication and partitioning

**What it does:** Checks whether distributed storage assumptions remain correct under lag, failover, skew, and data movement.

```text
Review how this change interacts with replication and partitioning.

For replication, identify:

- Writable leader or primary
- Read replicas
- Synchronous or asynchronous replication
- Read routing
- Failover behavior
- Replica lag assumptions
- Multi-region behavior

For partitioning, identify:

- Partition or shard key
- Routing logic
- Hot-key risk
- Cross-partition queries
- Cross-partition transactions
- Rebalancing behavior
- Large-tenant risk
- Secondary-index strategy

Look for:

- Read-after-write requests sent to replicas
- Authorization decisions made from stale data
- Acknowledged writes vulnerable during failover
- Sequential keys creating a hotspot
- Low-cardinality shard keys
- One tenant overwhelming one partition
- Fan-out queries introduced into hot paths
- Global uniqueness assumed across independent partitions
- Cross-shard updates treated as atomic
- Cached routing metadata becoming stale
- Rebalancing changing ordering or latency assumptions

Do not assume replication improves durability in the same way as backups.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 13. Review failure handling and recovery

**What it does:** Reviews partial success, ambiguous outcomes, reconciliation, restore, and repair.

```text
Review the failure and recovery behavior introduced or changed by this patch.

Consider failures involving:

- Application crash
- Database timeout
- Database unavailability
- Network partition
- Queue outage
- Consumer crash
- Cache outage
- Search-index outage
- External API timeout
- Disk exhaustion
- Leader failover
- Corrupt or malformed data
- Partial deployment

For each operation, explain:

- What may already have succeeded
- Whether the caller can know the outcome
- Whether retry is safe
- What data may become inconsistent
- How the inconsistency is detected
- How it is repaired
- Whether recovery is automatic or manual
- Whether data can be restored
- What monitoring or alerting exists

Look for missing:

- Reconciliation jobs
- Dead-letter queues
- Repair scripts
- Checkpoints
- Compensation logic
- Point-in-time recovery
- Backup verification
- Replay procedures
- Operational runbooks
- Alerts for lag, backlog, or divergence

Distinguish availability from correctness: returning a response is not success
if the underlying state is inconsistent.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 14. Review scale and operability

**What it does:** Probes the design at larger traffic and data volumes and checks whether operators can see and control failure.

```text
Review this change under 10× and 100× workload and data growth.

Evaluate:

- Read throughput
- Write throughput
- Query complexity
- Index size
- Row or document size
- Queue backlog
- Consumer throughput
- Cache hit rate
- Memory use
- Connection-pool pressure
- Lock contention
- Hot keys
- Cross-partition fan-out
- Batch-job duration
- Rebuild duration
- Deployment duration
- Recovery time

Look for:

- Work proportional to total dataset size
- Unbounded in-memory accumulation
- One request spawning many remote calls
- Missing pagination or limits
- Synchronous processing that should be bounded
- Unlimited retries
- No backpressure
- Polling loops with increasing load
- Metrics with unbounded cardinality
- Logging sensitive or excessive payloads
- No visibility into queue lag or replication lag
- No capacity limit or overload policy

For every concern, give:

- Triggering workload
- Expected symptom
- User-visible consequence
- Metric that would reveal it
- Smallest mitigation

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 15. Review tests as guarantee evidence

**What it does:** Determines whether tests prove data guarantees rather than only exercising a happy-path service method.

```text
Review the tests changed or added by this patch.

Determine whether they verify:

- User-visible behavior
- Data-model invariants
- Database constraints
- Transaction boundaries
- Concurrent updates
- Duplicate requests
- Retry behavior
- Out-of-order events
- Stale reads
- Partial failures
- Schema compatibility
- Event replay
- Projection rebuilding
- Migration resumability
- Recovery after interruption

Look for tests that:

- Mock the database so heavily that transaction behavior is not exercised
- Verify method calls instead of persisted outcomes
- Assume one execution order
- Use only one worker or request
- Never retry after an ambiguous timeout
- Do not test old and new schema versions together
- Ignore duplicate delivery
- Depend on sleeps rather than explicit synchronization
- Pass despite leaving inconsistent data
- Treat an in-memory substitute as proof of production-store behavior

Separate:

- Missing unit coverage
- Missing integration coverage
- Missing concurrency coverage
- Missing failure-injection coverage
- Optional load or soak testing

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## A. Reviewing an AI-generated change

**What it does:** Applies extra skepticism to common AI mistakes in data-intensive code.

```text
Review this AI-generated change skeptically using DDIA principles.

Look specifically for:

- Claimed exactly-once behavior based only on acknowledgements
- Retry logic without idempotency
- Check-then-write races
- Transactions assumed across multiple systems
- Events published separately from database commits
- Timestamps used as reliable global ordering
- Read replicas assumed to be current
- Cache used as an accidental system of record
- Schemas changed without compatibility analysis
- Missing indexes on new queries
- Indexes added without considering write cost
- Unbounded lists or scans
- Offset pagination on growing data
- In-memory deduplication
- Distributed locks used without lease or fencing analysis
- New queues, caches, or databases added without a concrete need
- Overconfident scalability claims without workload estimates
- Failure handling that only logs and continues
- Fake recovery paths that cannot reconstruct data

For each finding, require a concrete concurrency, retry, failure, or scale
scenario.

Prefer the simplest architecture that satisfies the actual correctness,
freshness, availability, and workload requirements.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## B. Review a single query or write path

**What it does:** Zooms in on one operation and reconstructs its full correctness and performance behavior.

```text
Review [query, endpoint, command, worker, or write path] using DDIA principles.

Identify:

- Input
- Output
- Data read
- Data written
- System of record
- Query plan or access pattern
- Joins, join keys/cardinality, query counts, and selected columns if relevant
- Indexes (and available plan/timing evidence, not invented measurements)
- Transaction boundary
- Isolation assumptions
- Concurrent writers
- Retry behavior
- Idempotency
- Events emitted
- Caches or projections updated
- Failure behavior
- Expected frequency and data volume

Then answer:

1. Is the result behaviorally correct?
2. Are all invariants protected under concurrency?
3. Can retry repeat a side effect?
4. Can readers observe stale or partial data?
5. Is the access pattern efficient at expected scale? What query/plan or
   workload evidence supports that judgment versus what needs measurement?
6. If relational reads are involved, what are the normalization versus
   denormalization trade-offs for joins, update work, duplicated storage,
   freshness, and consistency? Avoid assuming one approach is always faster.
7. What happens if the process crashes at each step?
8. Can the operation be safely replayed?
9. Which guarantee is proven and which is assumed?

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## C. Review a new datastore, cache, or queue

**What it does:** Tests whether adding infrastructure solves a real problem and whether its operational cost is understood.

```text
Review the new datastore, cache, search index, or queue introduced by this
change.

Identify:

- Concrete problem it solves
- Data stored or transported
- System of record
- Access pattern
- Freshness requirement
- Consistency requirement
- Throughput requirement
- Retention
- Failure behavior
- Recovery behavior
- Ownership
- Operational burden

Then ask:

- Why cannot the existing store or transport handle this requirement?
- Is this component authoritative or derived?
- Can it be rebuilt?
- How are dual writes coordinated?
- How are missed updates repaired?
- What consistency becomes weaker?
- What new failure modes appear?
- How is it monitored?
- How is it backed up or replayed?
- How is schema evolution handled?
- What happens during an outage?
- At what workload is the new component justified?

Classify it as:

- Necessary now
- Reasonable boundary
- Premature but low-risk
- Operationally under-specified
- Correctness risk
- Unnecessary complexity

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## D. Review a migration or backfill

**What it does:** Reviews online rollout, mixed-version compatibility, resumability, verification, and rollback.

```text
Review this schema migration, data migration, or backfill.

Identify:

- Old schema or representation
- New schema or representation
- Existing readers and writers
- Deployment order
- Compatibility period
- Data volume
- Batch size
- Locking behavior
- Runtime impact
- Resume checkpoint
- Idempotency
- Verification method
- Rollback plan
- Cleanup step

Check whether the process supports:

- Expand-and-contract rollout
- Old and new application versions running together
- Repeated execution
- Partial completion
- Process restart
- Concurrent production writes
- Throttling
- Progress monitoring
- Error quarantine
- Reconciliation
- Post-migration validation

Look for:

- Destructive schema changes too early
- Backfill and live writes racing
- Long table locks
- One giant transaction
- Offset-based backfill pagination
- Rows skipped or processed twice
- No deterministic checkpoint
- No count or checksum verification
- Cleanup before confidence is established
- Rollback that cannot restore transformed data

For every risk, describe the exact deployment or interruption scenario.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## E. Producing useful review comments

**What it does:** Converts findings into actionable comments grounded in concrete guarantees and failure cases.

```text
Turn the review findings into actionable pull-request comments.

For each comment, include:

- Severity: blocking, important, or optional
- File and symbol
- Concrete data or reliability problem
- Why it matters
- Realistic concurrency, retry, failure, or scale scenario
- Smallest recommended improvement

Do not write vague comments such as:

- "This is not scalable."
- "Use a transaction."
- "Make it idempotent."
- "This is eventually consistent."
- "Use Kafka."
- "Add caching."
- "Use a distributed lock."

Instead explain:

- Which invariant can fail
- Which operations interleave
- Which effect can be duplicated
- Which read can become stale
- Which message can be lost or reordered
- Which query grows poorly
- Which guarantee is absent
- How the proposed change establishes that guarantee
- What trade-off it introduces

Avoid speculative architecture advice not supported by the expected workload or
reliability requirement.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## Recommended review workflow

### Pass 1 — Understand and verify behavior

Run:

```text
1. Understand the change first
2. Review correctness
```

Goal:

```text
Understand what changed and find ordinary behavioral defects first.
```

### Pass 2 — Review data and access patterns

Run:

```text
3. Review the data model
4. Review data ownership and the system of record
5. Review queries and indexes
```

Goal:

```text
Understand what data exists, where truth lives, and how it is accessed.
```

### Pass 3 — Review correctness under time and concurrency

Run:

```text
6. Review transactions and concurrency
7. Review consistency and ordering
8. Review idempotency, retries, and duplicate effects
```

Goal:

```text
Determine whether the feature remains correct when operations overlap, retry,
or arrive out of order.
```

### Pass 4 — Review distributed and derived behavior

Run the relevant prompts:

```text
9. Review events, queues, and stream processing
10. Review caches, indexes, and derived data
11. Review schema and encoding evolution
12. Review replication and partitioning
```

Goal:

```text
Understand how copies, messages, schemas, and distributed storage behave.
```

### Pass 5 — Review production safety

Run:

```text
13. Review failure handling and recovery
14. Review scale and operability
15. Review tests as guarantee evidence
```

Goal:

```text
Determine whether failures are detectable, recoverable, and tested.
```

### Pass 6 — Produce comments

Run:

```text
E. Producing useful review comments
```

Goal:

```text
Turn the highest-value findings into concrete, proportionate PR feedback.
```

---

## Questions to remember during manual review

```text
What data changed?

Where is the system of record?

Which invariants must always hold?

What is the transaction boundary?

What happens when two requests run concurrently?

Can this operation be retried safely?

Can an event be duplicated, lost, or reordered?

Can the user read stale or partial data?

How are caches and projections repaired?

Can old and new schemas coexist?

What happens if the process crashes after each step?

What happens during replica lag or failover?

What becomes expensive at 10× data or traffic?

Which guarantee is proven?

Which guarantee is only assumed?
```

---

## The overall model

A complete data-intensive code review contains four different reviews:

```text
Behavior review
    Does the change do what the product expects?

Invariant review
    Does the data remain valid under concurrency and retries?

Distributed-systems review
    Do copies, messages, ordering, and failures behave safely?

Operational review
    Can the system scale, recover, and be understood in production?
```

DDIA primarily strengthens the last three. It should not replace the first.

---

## Guarantee-evidence rule

Never accept:

```text
This operation is exactly once because the message is acknowledged.
```

Require:

```text
The broker may redeliver the message.

The consumer writes the event ID and business update in one database
transaction. A unique constraint prevents a second application of the same
event ID.

This makes the database effect effectively once for that consumer. It does not
prove exactly-once behavior for an external email or payment request.
```

Likewise:

```text
Transaction ≠ distributed transaction

Retry ≠ idempotency

Acknowledgement ≠ exactly once

Replication ≠ backup

Read replica ≠ read-your-writes

Timestamp ≠ total ordering

Cache ≠ system of record

Queue ordering ≠ global ordering

Unique identifier ≠ duplicate prevention

Eventual consistency ≠ absence of guarantees
```

---

## Final code-review principle

The goal is not to ask:

```text
Does this use the right database or queue?
```

The better sequence is:

```text
What data changes?
Where is truth stored?
Which invariant must hold?
What can happen concurrently?
What can be stale, duplicated, lost, or reordered?
What happens after an ambiguous timeout?
How is inconsistency detected and repaired?
What breaks at larger scale?
Which guarantees are proven?
Which trade-offs make those guarantees possible?
```

Technology names are secondary. The real review is about data behavior, guarantees, failure modes, and operational consequences.
