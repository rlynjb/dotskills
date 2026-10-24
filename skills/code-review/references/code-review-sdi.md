# System Design Code-Review Prompt Library

Quick-reference for reviewing a change with an AI coding agent, using system-design principles from Alex Xu's *System Design Interview* material to judge whether the system meets its requirements, has clear boundaries, scales appropriately, handles failure, and remains operable without unnecessary distributed-system complexity.

A normal review asks:

```text
Does this code work?
Are there bugs?
Are there tests?
```

A system-design review also asks:

```text
What requirement does this component serve?
What is the request and data flow?
Where is state stored?
What happens when traffic grows?
Where are the bottlenecks?
What happens when a dependency fails?
What should be synchronous versus asynchronous?
What consistency does the user actually need?
How will we know when the system is unhealthy?
How can the architecture evolve without a rewrite?
```

System Design should **complement, not replace** reviews for ordinary correctness, APOSD, DDIA, security, maintainability, and product behavior.

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

| # | Prompt | What it does | Reach for it when |
|---|---|---|---|
| ★ | [**Compact daily**](#compact-daily-system-design-review-prompt) | 12-point architecture review in one pass | Default for architecture-affecting changes |
| 0 | [**Master**](#0-master-system-design-code-review-prompt) | Full requirements → architecture → scale → reliability review | Bigger features or services |
| 1 | [**Understand the system**](#1-understand-the-system-first) | Reconstructs architecture before critique | First — don't review what you don't understand |
| 2 | [**Requirements**](#2-review-requirements) | Functional and non-functional requirements | Architecture decisions depend on unknown needs |
| 3 | [**Request and data flow**](#3-review-the-request-and-data-flow) | Traces end-to-end execution and state movement | Multi-service or multi-component changes |
| 4 | [**API boundaries**](#4-review-api-and-service-boundaries) | Contracts, ownership, retries, compatibility | APIs or service boundaries changed |
| 5 | [**Storage**](#5-review-storage-and-access-patterns) | Storage fit, queries, read/write patterns | Database or persistence changed |
| 6 | [**Scale**](#6-review-scale-and-bottlenecks) | Finds the first likely bottleneck | Performance or growth matters |
| 7 | [**Caching**](#7-review-caching) | Cache usefulness, freshness, and invalidation | Cache added or modified |
| 8 | [**Async processing**](#8-review-asynchronous-processing) | Queues, workers, retries, delivery | Background processing involved |
| 9 | [**Reliability**](#9-review-reliability-and-failure-handling) | Failure, timeout, retry, recovery | Production-critical flow |
| 10 | [**Observability**](#10-review-observability-and-operation) | Metrics, logs, tracing, alerts | Production operation matters |
| 11 | [**Evolution**](#11-review-evolution-and-future-changes) | Tests architecture against realistic future change | Design or boundaries are being evaluated |
| A | [**AI-generated design**](#a-reviewing-an-ai-generated-system-design) | Detects unjustified distributed-system complexity | Architecture came from an agent |

---

## Compact daily system-design review prompt

**What it does:** Runs the main system-design checks in one pass and separates real risks from optional architecture improvements.

```text
Review this diff from a system-design perspective.

Focus on:

1. Functional behavior
2. Non-functional requirements
3. System boundaries and ownership
4. Request and data flow
5. API contracts
6. Storage and access patterns
7. Scaling and bottlenecks
8. Caching
9. Synchronous versus asynchronous work
10. Failure handling and recovery
11. Observability and operability
12. Test and operational readiness

For every finding, provide:

- Evidence
- Concrete consequence
- Severity
- A realistic traffic, workload, growth, or failure scenario
- Smallest reasonable improvement

Separate findings into:

- Correctness issues
- Scalability risks
- Reliability risks
- Operational risks
- Optional improvements

Clearly distinguish current problems from future concerns.

Do not introduce distributed infrastructure unless the workload, reliability,
latency, or ownership requirements justify the added complexity.

Calibrate every claim: distinguish CONFIRMED DEFECT, PLAUSIBLE RISK,
VERIFICATION GAP, and OPTIONAL IMPROVEMENT. Provide the evidence and
conditions for each; severity must match demonstrated impact, not a
hypothetical worst case. State what was inspected or actually tested,
and what was not. Zero findings is a valid result.
```

---

## 0. Master System Design code-review prompt

**What it does:** Performs the full architecture review beginning with requirements rather than technology choices.

```text
Review this change using system-design principles.

Start with requirements and architecture before suggesting technologies.

Evaluate:

1. What user or system requirement the change serves.
2. Functional requirements.
3. Non-functional requirements such as latency, availability, throughput,
   durability, and consistency.
4. Major system components and their responsibilities.
5. Request flow through the system.
6. Data flow and state ownership.
7. API and service boundaries.
8. Database and storage choices.
9. Read and write access patterns.
10. Caching strategy.
11. Synchronous versus asynchronous processing.
12. Expected bottlenecks and scaling behavior.
13. Failure modes and recovery behavior.
14. Monitoring, metrics, logging, tracing, and operational readiness.
15. Whether the architecture can evolve without unnecessary rewrites.

Separate findings into:

- Requirement and architecture issues
- Boundary and ownership issues
- Scalability risks
- Reliability and operability risks
- Testing gaps
- Optional improvements

For every finding:

- Cite the relevant file, service, API, schema, configuration, or component
- Explain the concrete consequence
- Give a realistic workload, growth, or failure scenario
- Suggest the smallest reasonable improvement
- Mark it as blocking, important, or optional

Clearly separate:

- Requirements
- Confirmed implementation behavior
- Assumptions
- Current problems
- Future scalability concerns

Do not design for hypothetical billions of users unless the requirements justify
it.

Prefer the simplest architecture that satisfies current requirements while
leaving reasonable room for growth.

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

## 1. Understand the system first

**What it does:** Reconstructs the surrounding architecture and traces a representative request before criticizing individual components.

```text
Explain the system around this change before reviewing it.

Identify:

- User or client
- Entry points
- Major components
- Services involved
- APIs involved
- Databases
- Caches
- Queues
- External dependencies
- Background workers
- Read path
- Write path
- State ownership
- Deployment boundaries

Then trace one representative request end to end.

Use this form:

Client
→ entry point
→ service or component
→ storage / dependency
→ response

For write paths, also show:

Write
→ persistence
→ event or queue if any
→ downstream processing
→ derived state if any

Identify:

- Where network boundaries are crossed
- Where persistent state changes
- Which component is authoritative for each important value
- Which steps are synchronous
- Which steps are asynchronous
- Where failure can interrupt the flow

Separate architecture confirmed by the code or configuration from inference.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 2. Review requirements

**What it does:** Prevents architecture decisions from being made against invented traffic, latency, or consistency requirements.

```text
Identify the requirements implied by this change.

Functional requirements:

- What must the system do?
- Who uses it?
- What operations must be supported?
- What behavior is required when an operation succeeds?
- What behavior is required when it fails?

Non-functional requirements:

- Expected traffic
- Read/write ratio
- Latency target
- Availability requirement
- Durability requirement
- Consistency requirement
- Data volume
- Data growth rate
- Geographic distribution
- Security requirements
- Recovery expectations

For every important requirement classify it as:

- Confirmed
- Implied
- Unknown

Then identify architecture decisions that depend on unknown requirements.

Do not invent scale numbers.

When information is missing, state:

- What needs to be known
- Which design decision depends on it
- Whether the current design is still reasonable without that information

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 3. Review the request and data flow

**What it does:** Examines latency, coupling, state movement, and failure across the complete path instead of reviewing components in isolation.

```text
Trace every important request or data flow introduced or modified by this
change.

For each flow identify:

- Entry point
- Services or modules called
- Network boundaries crossed
- Databases accessed
- Cache accesses
- External APIs
- Queue or event publication
- Background processing
- Response path
- State changed

Look for:

- Excessive sequential network calls
- Fan-out
- Duplicate data fetching
- N+1 service calls
- Hidden synchronous dependencies
- Circular dependencies
- Multiple sources of truth
- Long request chains
- Unnecessary data movement
- Repeated serialization or transformation
- A failure in one dependency blocking unrelated behavior

For each issue explain:

- The concrete flow
- Latency impact
- Failure impact
- Scale impact
- Smallest reasonable improvement

Review the whole path rather than optimizing individual components in
isolation.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 4. Review API and service boundaries

**What it does:** Checks whether responsibilities and contracts are clear and whether callers are insulated from implementation details.

```text
Review the APIs and service boundaries affected by this change.

For each boundary identify:

- Responsibility
- Owner
- Request contract
- Response contract
- Error contract
- Authentication
- Authorization
- Timeout behavior
- Retry behavior
- Idempotency behavior
- Pagination where relevant
- Rate limiting where relevant
- Versioning
- Backward compatibility

Look for:

- Multiple components owning the same responsibility
- Callers needing internal implementation knowledge
- Chatty interfaces
- Interfaces that expose storage details
- APIs requiring fragile call ordering
- Ambiguous error semantics
- Unsafe automatic retries
- Breaking contract changes
- Overly broad APIs
- Service boundaries introduced without meaningful ownership separation

For every issue explain whether it is:

- A correctness problem
- A coupling problem
- A scalability problem
- An operational problem

Prefer clear ownership and simple contracts over unnecessary service
fragmentation.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 5. Review storage and access patterns

**What it does:** Evaluates storage from real reads and writes rather than choosing a database by popularity.

```text
Review the storage design affected by this change.

Identify:

- Data being stored
- System of record
- Authoritative writer
- Readers
- Read patterns
- Write patterns
- Query patterns
- Expected volume
- Growth pattern
- Relationships
- Required indexes
- Retention requirements
- Consistency requirements

Then evaluate whether the storage model fits those needs.

Look for:

- Full scans
- Hot records
- Unbounded rows or documents
- Expensive joins
- N+1 queries
- Poor partition keys
- Excessive write amplification
- Duplicate authoritative data
- Missing indexes
- Access patterns fighting the schema
- Technology choices based only on preference

For each storage recommendation explain:

Workload:
Current behavior:
Problem:
Proposed change:
Trade-off:

Do not recommend SQL, NoSQL, sharding, or another datastore merely because it
is common in system-design interviews.

Tie storage decisions to actual access patterns and requirements.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 6. Review scale and bottlenecks

**What it does:** Finds what will actually constrain the system first and avoids premature distributed-system design.

```text
Analyze how this system behaves as workload grows.

Consider:

- Request rate
- Concurrent users
- Read/write ratio
- Data size
- Payload size
- Network traffic
- CPU
- Memory
- Database connections
- Thread or worker pools
- External API quotas
- Queue depth
- Storage growth

Identify the first likely bottleneck.

Evaluate the system at:

- Current scale
- 10× scale
- 100× scale

For every scaling concern answer:

1. What resource becomes constrained?
2. Why?
3. What symptom would users or operators see?
4. How would we measure or detect it?
5. At approximately what workload does it matter?
6. What is the simplest reasonable mitigation?

Distinguish:

- Current bottleneck
- Near-term risk
- Long-term hypothetical concern

Do not jump immediately to:

- Sharding
- Microservices
- Distributed queues
- Multi-region architecture
- Complex caching

unless the workload justifies them.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 7. Review caching

**What it does:** Determines whether a cache solves a real problem and whether stale or invalid data is handled safely.

```text
Review the existing or proposed caching strategy.

Identify:

- What is cached
- Why it is cached
- Cache key
- Source of truth
- TTL
- Invalidation strategy
- Write/update strategy
- Expected hit rate
- Stale-data tolerance
- Failure behavior
- Size or eviction policy

Look for:

- Cache used as the source of truth
- Missing invalidation
- Incorrect cache keys
- Cross-user or cross-tenant leakage
- Cache stampedes
- Hot keys
- Unbounded growth
- Caching highly volatile data
- Stale data causing incorrect behavior
- Cache added without evidence of a bottleneck

For each cache explain:

What latency or load problem does it solve?
What happens on a cache miss?
What happens when cached data is stale?
What happens when the cache is unavailable?
Can the cache be rebuilt from the authoritative source?

Do not recommend caching merely because data is read frequently.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 8. Review asynchronous processing

**What it does:** Checks whether background processing or queues solve a concrete latency, throughput, or decoupling problem.

```text
Identify asynchronous work affected by this change and work that may reasonably
move outside the synchronous request path.

For each asynchronous flow identify:

- Producer
- Event or job
- Queue or broker
- Consumer
- Message contract
- Ordering requirements
- Retry policy
- Duplicate handling
- Failure behavior
- Dead-letter behavior
- Completion tracking
- User-visible state

Evaluate whether asynchronous processing improves:

- User latency
- Throughput
- Resilience
- Decoupling
- Burst handling

Also evaluate complexity introduced:

- Eventual consistency
- Retries
- Duplicate processing
- Debugging difficulty
- Operational overhead
- Ordering problems

For every recommendation explain why synchronous or asynchronous execution is
the better trade-off.

Do not introduce a queue merely because background processing appears more
scalable.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 9. Review reliability and failure handling

**What it does:** Forces the review to consider dependency failure, ambiguous outcomes, retries, and recovery.

```text
Assume every important dependency can fail independently.

For each dependency ask:

- What happens if it is slow?
- What happens if it times out?
- What happens if it returns an error?
- What happens if it succeeds but the caller never receives the response?
- What happens if it becomes unavailable?
- What happens if a retry repeats the operation?

Review:

- Timeouts
- Retries
- Backoff
- Idempotency
- Circuit breaking where justified
- Fallback behavior
- Partial failure
- Recovery
- Data reconciliation
- Duplicate side effects
- Dependency isolation

For every important failure mode provide a concrete sequence such as:

1. Service A sends request.
2. Service B commits the write.
3. Network response is lost.
4. Service A retries.
5. Explain what happens next.

Then determine whether the resulting behavior is safe.

Do not claim high availability merely because replicas, multiple instances, or
multiple services exist.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 10. Review observability and operation

**What it does:** Checks whether an engineer could understand and diagnose the change after it reaches production.

```text
Review whether this change can be understood and operated in production.

Check whether the important behavior is visible through:

- Structured logs
- Metrics
- Error rates
- Latency
- Throughput
- Saturation
- Queue depth
- Cache hit rate
- Database health
- Dependency failures
- Distributed tracing
- Dashboards
- Alerts

For every important failure mode ask:

How would an engineer know this is happening?

Identify:

- Signal
- Metric or log
- Expected normal range if known
- Failure symptom
- Action an engineer could take

Look for:

- Failures that are silently swallowed
- Logs without useful identifiers
- High-volume logs with little diagnostic value
- Missing latency measurements
- Missing dependency visibility
- Alerts that are not actionable

Avoid recommending observability simply to collect more data.

Prefer signals tied to user impact, system health, or an actionable operational
decision.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 11. Review evolution and future changes

**What it does:** Uses realistic future changes to test whether today's architecture has healthy boundaries.

```text
Evaluate how this architecture would respond to realistic future changes.

Consider scenarios such as:

- 10× traffic
- New client application
- New API consumer
- New data field
- New query pattern
- Additional region
- New downstream consumer
- New authentication requirement
- New event consumer
- Storage migration
- Replacement of an external dependency

For each relevant scenario identify:

- Components that would need to change
- Interfaces that would change
- Data migrations required
- Operational impact
- Whether unrelated components would also need modification

Look for:

- Change amplification
- Overly coupled boundaries
- Hard-coded assumptions
- Shared state with unclear ownership
- Interfaces tied to one implementation
- Irreversible technology choices

Distinguish:

- A structural weakness visible today
- A reasonable future concern
- Pure speculation

Do not redesign the system for hypothetical future requirements.

Use future scenarios only to expose weaknesses in today's architecture.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## A. Reviewing an AI-generated system design

**What it does:** Applies extra skepticism to architecture generated by coding agents or LLMs, especially unnecessary distributed-system complexity.

```text
Review this AI-generated architecture skeptically.

Look specifically for:

- Microservices with no clear ownership boundary
- Queues with no asynchronous requirement
- Caches with no demonstrated bottleneck
- Multiple databases without a workload reason
- Premature sharding
- Event-driven architecture added only for sophistication
- Kubernetes or orchestration added without operational need
- Invented traffic numbers
- Invented latency or availability requirements
- Claims of high availability without failure analysis
- Claims of exactly-once processing without proof
- Replication without a clear consistency model
- Technology choices made before requirements were understood
- Components added because they commonly appear in system-design diagrams
- Distributed complexity solving a problem the application does not have

Reconstruct the design in this order:

Requirements
→ workload
→ constraints
→ simplest viable architecture
→ expected bottleneck
→ justified improvement

For every major component ask:

1. What concrete requirement does it satisfy?
2. What happens if we remove it?
3. What complexity does it introduce?
4. What workload justifies it?
5. Is there a simpler alternative?

Clearly separate:

- Required components
- Reasonable optional components
- Premature complexity

Prefer the least complex architecture that satisfies the actual requirements.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```
