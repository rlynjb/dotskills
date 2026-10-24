# System Learning Implementation Prompt Library

Quick-reference for understanding a specific implementation with an AI coding agent. Use the diff, changed files, tests, and surrounding code to learn how the change works and how it fits into the system.

The prompts connect relevant evidence to **DDIA (2nd edition)**, **Fundamentals of Data Engineering (FODE)**, **System Design Interview** by Alex Xu, and **Algorithmic Thinking (2nd edition)** by Daniel Zingaro.

Use the **master** for the full explanation, **compact** for a first pass, and a **focused prompt** when you want to understand one part more deeply. For whole-repo onboarding, use [System Learning Repo](system-learning-repo.md).

---

## Index

| # | Prompt | What it does | Reach for it when |
| --- | --- | --- | --- |
| 0 | [**Master**](#0-master-implementation-learning-prompt) | Full explanation using all four book lenses | You want a thorough understanding of a change |
| ★ | [**Compact**](#compact-implementation-learning-prompt) | Short overview of behavior, flow, mechanisms, and trade-offs | First pass or a small change |
| 1 | [**Trace one flow**](#1-trace-one-execution-and-data-flow) | Connects a concrete input to calls, state changes, and output | You understand individual functions but not how they fit together |
| 2 | [**Mechanism deep dive**](#2-understand-one-mechanism) | Explains one mechanism, guarantee, or algorithm step by step | A concept or code path still feels unclear |
| 3 | [**Design decisions**](#3-understand-design-decisions-and-trade-offs) | Relates the design to requirements, constraints, and alternatives | You understand what was built and want to understand the choices |
| 4 | [**Failure walkthrough**](#4-walk-through-failure-and-concurrency) | Follows a concrete failure or concurrent execution | You want to understand correctness and recovery |
| 5 | [**Teach-back**](#5-teach-back-self-test) | Tests understanding one open-ended question at a time | After an explanation, to check what you can explain yourself |

---

## 0. Master implementation learning prompt

**What it does:** Explains the implementation through behavior, data lifecycle, mechanisms, requirements, system design, algorithms, read/write paths, failures, vocabulary, and a learning summary.

**How to use:** Run it with access to the relevant request or ticket, diff, changed files, tests, and surrounding code. The original prompt below is preserved unchanged; the other prompts are optional companions.

```text
# Agent Implementation Mechanism Explainer

You are helping me understand code that a coding agent implemented.

Your goal is not just to summarize the diff. Your goal is to teach me the mechanisms behind the implementation using:

- Fundamentals of Data Engineering: data engineering lifecycle
- Designing Data-Intensive Applications (DDIA), 2nd Edition: reliable, scalable, maintainable data-system mechanisms
- System Design Interview by Alex Xu: requirements, architecture, capacity, component choices, bottlenecks, and tradeoffs
- Algorithmic Thinking by Daniel Zingaro, 2nd Edition: problem decomposition, pattern recognition, algorithm selection, correctness, and complexity

Assume I am a developer trying to build vocabulary and intuition. Connect what the coding agent built to the underlying ideas from these four resources, without forcing an irrelevant concept into the explanation.

Teach me to reason from problem -> requirements -> algorithm/data flow -> system design -> implemented code -> failure modes. Distinguish code-backed facts from proposed design alternatives.

## Inputs

Use any available context:

- User request or ticket
- Agent final summary
- Git diff
- Changed files
- Tests
- Migrations
- New APIs
- Jobs, queues, streams, caches, stores, or external calls
- Existing code paths the implementation depends on

Do not invent behavior. Separate observed facts from inferences.

## 1. What Did The Agent Implement?

Explain plainly:

- What changed?
- What user/system behavior was added or modified?
- What files/modules were involved?
- What is the main data movement?
- What is the main state change?
- What was deliberately not changed?

Then give a one-paragraph summary suitable for a developer reading the PR.

## 2. FODE Data Engineering Lifecycle View

Map the implementation onto the FODE lifecycle:

- Generation: where the data, event, or request originates
- Ingestion: how data enters this system or component
- Storage: where data is persisted or cached
- Transformation: how data is validated, enriched, joined, filtered, derived, or normalized
- Serving: how data is exposed to users, APIs, jobs, models, dashboards, or downstream systems

Also identify lifecycle undercurrents:

- Security
- Data management
- DataOps
- Data architecture
- Orchestration
- Software engineering

For each stage, say whether the implementation changed it, depends on it, or leaves it untouched.

## 3. ASCII Data Flow Diagram

Create an ASCII diagram showing the overall data flow.

Use this style:

[Generation]
    |
    v
[Ingestion / API Boundary]
    |
    v
[Validation / Authorization]
    |
    v
[Transformation / Business Logic]
    |
    +--------------------+
    |                    |
    v                    v
[Primary Storage]     [Cache / Index / Queue]
    |                    |
    v                    v
[Serving Layer] ---> [User / Client / Downstream Consumer]

Customize the diagram to the actual implementation.

Label:

- APIs
- functions/classes
- databases/tables
- queues/topics
- caches
- indexes
- background jobs
- external services
- read paths
- write paths
- sync vs async boundaries
- contract/module seams, field-level transformations, and their owning functions
- source-of-truth versus derived data where relevant

After the diagram, explain the flow step by step. For one representative field,
trace its value across the relevant boundaries from origin to consumer: show
where it is validated, renamed, mapped, combined, or modified, with file/symbol
evidence. Distinguish joins or other read-time composition from persistently
stored derived/denormalized copies; for stored copies, explain the observable
sync or refresh mechanism (or say if it is unknown). Do not assume either
approach is present unless the code supports it.

## 4. DDIA Mechanism Explanation

Explain the implementation using DDIA-style mechanisms.

Cover only the mechanisms that are actually relevant:

- Data model and query shape
- Storage and retrieval
- Indexes and access patterns
- Encoding, serialization, and schema evolution
- Replication or replica lag
- Partitioning, sharding, or hot keys
- Transactions
- Isolation levels
- Idempotency
- Concurrency control
- Distributed coordination
- Caching and derived data
- Change data capture
- Event streams and queues
- Batch jobs and backfills
- Materialized views or projections
- Fault tolerance and recovery
- Observability
- Maintainability and evolvability

If this implementation uses relational data or SQL, also investigate the
data-model and query-performance trade-offs (DDIA, 2nd edition):
- Identify the relevant entities/tables, primary and foreign keys, cardinality,
  and which facts are stored once versus duplicated or derived. Explain what
  is normalized or denormalized in THIS code, not what it ought to be.
- Follow the actual query shape: joins and join keys, filters, selected columns,
  sorting, limits, aggregation, and any ORM-generated queries or repeated
  per-item lookups (N+1). Show how the result maps into the API or caller.
- Explain what each join accomplishes, what relationship it represents,
  and how row counts, selectivity, indexes, query count, and returned data
  volume could affect cost under a stated workload.
- If indexes, query plans, EXPLAIN output, timings, or tests are available,
  use them to distinguish observed behavior from potential bottlenecks.
  Explain relevant plan operations in plain language. Never invent query
  plans or latency; do not run production queries or EXPLAIN ANALYZE.
- Compare the existing approach with a plausible alternative only when
  useful: read-time joins versus stored denormalized columns, a materialized
  view, or other derived data. Discuss read latency/query complexity,
  write/update cost, additional storage, consistency/freshness, and the
  refresh or invalidation mechanism. Identify the source of truth.
- State when normalization helps avoid update anomalies and when
  denormalization might help a demonstrated read-heavy access pattern.
  Neither approach is automatically faster or more correct for every workload.

Keep this section evidence-based and read-only. If there is no relevant
relational model or query, mark it not applicable rather than inventing one.

For each relevant mechanism, use this format:

Mechanism:
Where it appears in the code:
What guarantee it provides:
What it does NOT guarantee:
Failure mode:
Developer vocabulary to remember:

Do not claim strong consistency, exactly-once processing, atomicity, durability, or fault tolerance unless the code actually provides a mechanism for it.

## 5. Functional Requirements Recovered From The Code

Infer the functional requirements the agent appears to have implemented.

For each requirement:

- Requirement
- Evidence in code
- Main function/module responsible
- Input
- Output
- State change
- Error behavior
- Test coverage, if any

Mark each as one of:

- Confirmed
- Inferred
- Unclear

## 6. Nonfunctional Requirements Recovered From The Code

Infer the nonfunctional requirements implied by the implementation.

Look for:

- Latency
- Throughput
- Availability
- Reliability
- Consistency
- Durability
- Scalability
- Data freshness
- Ordering
- Security
- Privacy
- Operability
- Maintainability
- Evolvability

For each:

- Requirement
- Evidence
- DDIA concept involved
- Whether the implementation supports it well
- Risk or missing mechanism

## 7. System Design View (Alex Xu)

Explain the implementation as a small system-design case study, using Alex Xu's requirements-first and tradeoff-oriented approach.

### Requirements And Constraints

- What problem is the design solving, and for whom?
- Which functional and nonfunctional requirements from Sections 5 and 6 drive the design?
- What assumptions or constraints are visible in the code (existing infrastructure, APIs, scale, dependencies)?
- What traffic, data volume, read/write ratio, latency, or availability targets are actually known? If not known, say "not specified" rather than inventing numbers.

### Architecture And Design Decisions

- Identify the main components and their responsibilities.
- Show how requests and data move between components; connect to the Section 3 diagram.
- Explain why the observed design may use a database, cache, index, queue, worker, API, or other building block.
- Identify likely bottlenecks, single points of failure, and scaling limits only where supported by evidence.
- Explain relevant alternatives (for example: synchronous vs asynchronous, cache vs direct query, SQL vs NoSQL, push vs pull) and why a team might choose each.

For each significant decision, use:

Design decision:
Evidence in code:
Requirement it addresses:
Tradeoff (benefit and cost):
When this design might stop working well:
Alternative worth considering:
What I would ask in a system-design interview or review:

Finish with a concise high-level design walkthrough. Do not pretend this feature is a large distributed system if it is not.

## 8. Algorithmic Thinking View (Daniel Zingaro)

Explain the problem-solving logic behind the implementation, not just which functions were written.

### Problem Decomposition And Pattern Recognition

- State the computational problem in terms of inputs, outputs, constraints, and edge cases.
- Break the implementation into smaller subproblems and explain their dependencies.
- Identify the relevant data structures and why they fit the operations performed.
- Look for recognizable patterns such as hash lookup, counting, grouping, sorting, two pointers, binary search, traversal, recursion, greedy choice, dynamic programming, or graph search **only when the code warrants them**.
- If there is no notable textbook algorithm, explain the practical control-flow, lookup, or data-transformation pattern instead.

### Correctness And Efficiency

For each meaningful algorithm or transformation, provide:

Problem being solved:
Code location:
Approach / pattern:
Step-by-step reasoning or short pseudocode:
Correctness argument / key invariant:
Time complexity (define input size n and any other variables):
Space complexity:
Important edge cases:
Potentially simpler or more efficient alternative:
How to recognize this pattern next time:

- Explain complexity in terms of actual operations; do not assume a database call or network request is O(1) in end-to-end latency.
- Distinguish measured performance from theoretical complexity.
- Point out tests that validate the invariant, boundary cases, or algorithmic assumptions.

Finish with one transferable problem-solving heuristic I can reuse in future code reviews or DSA problems.

## 9. Read Path And Write Path

Explain the read path and write path separately.

### Write Path

Describe:

- What starts the write?
- What validation happens?
- What data is written?
- Where is it written?
- Is it transactional?
- What happens on retry?
- What happens on partial failure?
- What downstream effects occur?

### Read Path

Describe:

- What starts the read?
- What store is queried?
- What indexes or filters matter?
- If joins are involved, what tables/keys and query shape produce the result,
  and what plan or measurements (if available) support performance claims?
- Is the data fresh or possibly stale?
- Is derived data involved?
- What happens when data is missing?
- What does the caller receive?

## 10. Failure And Concurrency Walkthrough

Teach me what can go wrong.

Use concrete scenarios:

- Two users act at the same time
- Request is retried
- Job runs twice
- Database write succeeds but downstream action fails
- Cache is stale
- Event arrives out of order
- Deployment happens during schema change
- External service times out
- Backfill is interrupted

For each scenario:

Scenario:
Sequence:
Expected behavior:
Mechanism that handles it:
Missing mechanism, if any:
Risk level:

## 11. Concept Glossary

Create a glossary of the most important FODE, DDIA, system-design, and algorithmic-thinking terms that appear in this implementation.

For each term:

- Term
- Plain-English meaning
- Where it appears in this implementation
- Why it matters
- Related DDIA / FODE / Alex Xu / Zingaro topic

Prefer terms that help me think like a software engineer who can reason about algorithms, system design, and data systems.

## 12. Learning Summary

Finish with:

1. The core mechanism this implementation relies on
2. The most important data flow to remember
3. The strongest guarantee the system now provides
4. The weakest or least-proven guarantee
5. The FODE lifecycle stages this touched
6. The DDIA concepts I should study next
7. The key design decision or tradeoff from System Design Interview I should remember
8. The algorithmic pattern, invariant, or complexity lesson from Algorithmic Thinking I should remember
9. Three questions I should ask in code review (covering design, correctness, and failure modes)
10. One small hands-on exercise to reinforce the most relevant concept

Keep the tone educational, precise, and developer-friendly.
```

---

## Compact implementation learning prompt

**What it does:** Gives a short first pass before deciding which area deserves a deeper explanation.

```text
Help me understand this implementation as a junior developer. Inspect the
request, diff, changed files, relevant tests, and surrounding code available to you.

Explain concisely:
1. What behavior changed and what problem it solves.
2. The important files and their responsibilities.
3. One representative execution/data flow, from input to output.
4. The main mechanism or algorithm and why it works.
5. One important guarantee, its limits, and a relevant failure scenario.
6. One design trade-off and the constraints that make it matter; if relevant,
   include join/query cost versus denormalized reads and update complexity.
7. Which concepts from DDIA (2nd edition), FODE, System Design Interview
   (Alex Xu), and Algorithmic Thinking (2nd edition, Daniel Zingaro) are relevant.

Cite files and symbols. Separate observed behavior, inferred rationale, and
unknowns. Define unfamiliar terms, skip irrelevant book concepts, and do not
invent scale targets or guarantees. Explain the existing implementation without
making code changes.

End with three files to read next, each with a question it answers, and one
small read-only exercise.
```

---

## 1. Trace one execution and data flow

**What it does:** Makes the connections between components concrete by following one real input through the implementation.

```text
Teach me how one representative flow in this implementation works end to end.
Inspect the changed code and the existing code paths it depends on. Choose a
flow relevant to the change, or use the flow I specify.

Start with a small concrete input. Trace:
- The entry point and important calls, citing files and symbols.
- Validation, authorization, and component boundaries where present.
- How data changes shape and where state is read or written.
- For one representative field: its source, consumers, contract/module seams,
  and exact validation, renaming, mapping, or transformation points; cite the
  functions responsible.
- Whether related data is assembled at read time or stored redundantly. If a
  derived copy exists, identify the source of truth and how updates propagate
  (or mark the synchronization behavior unknown).
- Synchronous/asynchronous boundaries and downstream effects where present.
- The final output and one relevant error path.

Use a concise Mermaid diagram where it helps, followed by the step-by-step
walkthrough. Distinguish changed behavior from existing behavior.

Connect the flow to FODE's lifecycle and DDIA's source-of-truth/derived-state
concepts only where relevant. Explain terms plainly, separate code evidence from
inference, and identify any step that cannot be verified.

Keep this read-only. End by asking me to predict the output or state change for
one nearby input; wait for my answer before explaining it.
```

---

## 2. Understand one mechanism

**What it does:** Turns an unfamiliar mechanism or algorithm into a concrete example you can reason about.

```text
Help me understand one mechanism in this implementation:
[mechanism, algorithm, function, or concept; if omitted, choose a central one].

Inspect its code, callers, and relevant tests. Explain:
1. The problem it solves, its inputs/outputs, and why it is needed here.
2. A plain-English mental model, followed by a tiny concrete example.
3. The execution steps and state changes, with file/symbol citations.
4. The key invariant or guarantee, how the code supports it, and its limits.
5. A relevant edge case or failure and the actual handling.
6. A simpler alternative and the conditions under which it would fit.

Connect it to the relevant lens: DDIA, FODE, System Design Interview (Alex Xu),
or Algorithmic Thinking (2nd edition, Daniel Zingaro). Do not force all four into
the explanation.

For algorithms, define input sizes and assumptions before analyzing time/space
complexity. Separate in-memory cost from database/network behavior. For other
mechanisms, explain the operational costs that are actually supported by evidence.

Separate facts from inference. Keep this read-only and finish with one
recognition rule I can reuse when I encounter a similar problem.
```

---

## 3. Understand design decisions and trade-offs

**What it does:** Explains how requirements and constraints relate to the observed design without inventing the team's rationale.

```text
Teach me the important design decisions in this implementation. Inspect the
request, code, tests, configuration, and design documentation available to you.

Choose up to three decisions. For each, explain:
- The observed design and its code evidence.
- The requirement or constraint it appears to address.
- The benefit, cost, and assumptions.
- A plausible alternative and when it would be appropriate.
- What evidence would help determine whether the current choice is working.

For a relational data-model decision, compare normalized tables and read-time
joins with any relevant denormalized/derived alternative. Explain the observed
join keys, indexes, query shape, and likely read/write, storage, and freshness
costs. Use execution plans or measurements only if available; do not infer a
performance problem from the presence of a join.

Use System Design Interview (Alex Xu) for requirements and component trade-offs,
DDIA for data guarantees, FODE for lifecycle/operational concerns, and Algorithmic
Thinking for computational choices only when relevant.

Distinguish documented intent from your inferred explanation. Say "not specified"
for unknown workloads or targets. Do not assert a bottleneck without evidence;
label hypothetical scenarios and estimates.

Explain the existing implementation without changing or redesigning it.
End with three questions I could ask the author to resolve important unknowns.
```

---

## 4. Walk through failure and concurrency

**What it does:** Shows what happens when execution is interrupted, repeated, or interleaved with another operation.

```text
Help me understand failure and concurrency in this implementation. Inspect the
relevant code, dependencies, and tests before selecting scenarios.

Choose up to three applicable scenarios, such as invalid input, a timeout,
a retry, duplicate processing, concurrent updates, stale state, or partial failure.
Do not assume queues, caches, transactions, or distributed components exist.

For each scenario:
1. State the starting state and triggering event.
2. Walk through the calls and state changes in order, citing files/symbols.
3. Explain the visible result and any lasting side effects.
4. Identify the mechanism that prevents, detects, or recovers from the problem.
5. Explain the guarantee's limits and what remains unknown.
6. Point to relevant tests and distinguish tested behavior from assumptions.

Connect relevant correctness/recovery concepts to DDIA, lifecycle effects to
FODE, component boundaries to System Design Interview, and invariants to
Algorithmic Thinking. Explain only the lenses that help this scenario.

Keep this read-only. Finish with one investigation path: the files, logs, or
state I would inspect first to distinguish the most plausible causes.
```

---

## 5. Teach-back self-test

**What it does:** Checks whether you can explain the implementation yourself and identifies the next area to revisit.

```text
Interview me about this implementation one open-ended question at a time.

Use the inspected code and tests to ground your questions. Start with the
problem and behavior, then move through execution/data flow, mechanisms,
design trade-offs, correctness, and relevant algorithms.

Wait for my answer before giving feedback. If my answer is incomplete, ask a
targeted follow-up or give a small hint before explaining the missing part.
Cite the relevant file and symbol in your feedback.

Connect explanations to DDIA, FODE, System Design Interview (Alex Xu), or
Algorithmic Thinking (2nd edition, Daniel Zingaro) where relevant. Do not ask
about infrastructure or algorithms absent from this implementation.

After five questions, summarize what I can explain, what needs another pass,
and the next file or flow to revisit. Keep this read-only.
```
