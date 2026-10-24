# Repo Onboarding Prompt Library

Use these prompts with an AI agent that can inspect the target repository. The goal is to help a junior developer build a working mental model of the **whole codebase**: what it does, how its parts fit together, how data moves, and how to run and investigate it.

This is an onboarding workflow, not a feature implementation request. Representative flows are examples used to understand the repo; they do not define the scope.

## Index

| Prompt / reference | Use it when |
| --- | --- |
| [Master repo onboarding](#master-repo-onboarding-prompt) | First contact with an unfamiliar repository |
| [Quick repo orientation](#quick-repo-orientation-prompt) | You need a shorter first pass |
| [Teach-back self-test](#teach-back-self-test) | You want to check your understanding after onboarding |
| [Four book lenses](#four-book-lenses) | You want to connect the implementation to your reading |
| [Keep the layers distinct](#keep-the-layers-distinct) | You need to distinguish domain, system, and software design |

## Four book lenses

Use the books to explain evidence in the repository. They are complementary perspectives, not four separate summaries or a checklist of technologies every repo must use.

| Book | Onboarding perspective | Questions to connect to the repo |
| --- | --- | --- |
| **Designing Data-Intensive Applications, 2nd edition (DDIA)** — Martin Kleppmann and Chris Riccomini | Data models, storage, correctness, reliability, and distributed-system trade-offs | What is authoritative data? What guarantees exist when data changes? What happens during concurrent updates or partial failure? |
| **Fundamentals of Data Engineering (FODE)** — Joe Reis and Matt Housley | The data engineering lifecycle and its operational responsibilities | Where does data originate, enter, get stored, change, and reach consumers? Who owns its quality, security, and operation? |
| **System Design Interview** — Alex Xu | Requirements, system boundaries, component responsibilities, capacity, and bottlenecks | How does the existing architecture serve its users? Which constraints explain the design? What evidence would identify a scaling limit? |
| **Algorithmic Thinking, 2nd edition** — Daniel Zingaro | Problem decomposition, data structures, algorithm selection, and complexity | What computational problem does this code solve? How does its approach work, why is it correct, and what input size drives its cost? |

Use **DDIA** and **FODE** after defining them. Keep **System Design Interview** and **Algorithmic Thinking** written out in learning summaries.

These lenses do not cover every onboarding concern. Also inspect the repo's setup, framework conventions, module organization, testing, and development workflow.

## Master repo onboarding prompt

**How to use:** Run this in the target repo, or provide its URL and accessible revision. Fill in the optional context if helpful. The default is staged teaching: first establish the repo map, then deepen it.

```text
Act as a senior engineer onboarding a junior developer to this entire repository.

My goal is to understand the existing codebase well enough to navigate it, explain
its behavior, run it locally, and investigate a problem. This is not a request to
implement a feature, refactor the code, or design a replacement system.

Optional context:
- Repository / revision: [current workspace, or URL and branch/commit]
- My background: [languages/frameworks I know; unfamiliar areas]
- Time available: [optional]
- Delivery: [staged by default; complete guide if explicitly requested]

Use these four books as complementary teaching lenses:
- Designing Data-Intensive Applications, 2nd edition (DDIA), by Martin Kleppmann
  and Chris Riccomini.
- Fundamentals of Data Engineering (FODE), by Joe Reis and Matt Housley.
- System Design Interview, by Alex Xu.
- Algorithmic Thinking, 2nd edition, by Daniel Zingaro.

Working rules:
- Inspect the repository before explaining it. Read applicable repo instructions,
  README/docs, manifests, configuration, entry points, tests, and CI/deployment
  files. Use these to decide which implementation files to inspect next.
- Identify the repo type: application, monorepo, library, CLI, pipeline,
  infrastructure/configuration repo, or a combination. Adapt the guide to it.
- Map every major first-party package, application, or subsystem at a useful
  level. Inspect representative code across those areas; do not narrow the
  entire onboarding to the first feature or directory you find.
- Do not read every file indiscriminately. State the areas inspected, areas not
  inspected, revision when available, and any access limitations. If repo access
  is unavailable, ask for the tree and essential files; do not invent a guide.
- Tie repo-specific claims to file paths and symbols, configuration keys, tests,
  schemas, or documentation. Add line references when available.
- Label observations as Verified, Inferred, or Unknown where the distinction
  matters. Code/config evidence does not prove a production deployment or load.
  Report conflicts between docs and implementation.
- Explain terms in plain language before using jargon. Introduce each concept
  through a concrete repo example. Separate essentials from optional depth.
- Connect book concepts only where relevant. A frontend repo, CLI, library, or
  dotfiles repo may have no database, queues, analytics pipeline, or distributed
  system. Say "not observed" or "not applicable" and explain briefly.
- Do not invent book quotations, chapter numbers, page references, author intent,
  design history, or reasons the team chose an approach. Use topic names unless
  the exact edition/source is available and the reference can be verified.
- Keep this read-only by default. Explain setup commands and their effects.
  Distinguish commands you actually ran from commands you only inspected.
  Use local examples and redact secret values.

Stage 1 — Build the repo map

1. Purpose and boundaries
   - Explain the user or developer problem this repo solves and its main outputs.
   - Describe the main capabilities, actors, domain terms, relationships, and
     important rules/invariants. Explain domain rules separately from code types.
   - Clarify what lives inside this repo and what depends on external systems.

2. Repository and architecture map
   - Give an annotated map of the important top-level directories and packages.
     Group generated code and third-party dependencies rather than cataloging them.
   - For each major area, identify its responsibility, entry point, dependencies,
     public interface, and a representative file to inspect.
   - Distinguish system design (runtime components and communication) from
     software design (modules, functions, interfaces, and dependency direction).
   - Show a concise architecture diagram grounded in the actual repo. Distinguish
     build-time tooling from runtime components; do not imply folders are services.
   - Use System Design Interview to relate requirements to component boundaries
     and trade-offs. Explain the architecture that exists before discussing scale.

3. Local development and first reading path
   - Identify required runtimes, package managers, dependency/lockfiles, setup
     docs, environment variable names, fixtures, and local dependencies.
   - Explain the documented install, run, build, lint/type-check, and test commands,
     their working directories, and what successful execution should look like.
     Flag missing prerequisites or unverified commands.
   - Explain the existing CI checks and contribution conventions.
   - Recommend up to five files to read first, in order, with the question each
     file answers. Then give a short route into each remaining major subsystem.
   - End with three open-ended comprehension questions, the most important
     unknowns, and a preview of Stage 2.

Deliver Stage 1 first and wait for me to say "continue." Do not wait between its
individual sections. If I explicitly request a complete guide, deliver all stages.

Stage 2 — Connect execution, data, and algorithms

4. Trace representative existing flows
   - Select two or three flows that collectively connect the repo's main areas.
     Where present, include a read path and a state-changing or asynchronous path.
     For smaller repos, use one flow and explain why it is representative.
   - Adapt examples to the repo: a user action, CLI command, exported library call,
     pipeline run, configuration load, or build/install process.
   - For each flow, trace the entry point, important calls, boundaries, data/state
     changes, output, and error path. Cite actual files and symbols at each step.
   - Follow one representative data field across relevant interfaces and seams
     (such as an API contract, adapter, shared package, or module boundary).
     Show its source, producers/consumers, and where it is validated, renamed,
     mapped, combined, or otherwise transformed; identify the responsible
     function and whether the original value is preserved or replaced.
   - Distinguish data assembled on read (for example, with a join) from stored
     derived or denormalized data. Where stored copies exist, identify the source
     of truth and the observed refresh/synchronization path, or mark it unknown.
     Do not presume every flow uses a database or needs data duplication.
   - Walk through a small concrete input and resulting output without exposing
     private data. Explain how a developer would locate and observe each step.
   - List major areas these examples do not cover and where to explore them next.

5. Data lifecycle — FODE
   - Map data sources/generation, ingestion, storage, transformation, and serving
     to actual code or configuration. Storage can appear at several stages; do
     not force the lifecycle into a single linear pipeline.
   - Identify producers, consumers, formats/contracts, validation, ownership,
     freshness, lineage, and data-quality checks where visible.
   - Distinguish operational application data from analytical/ML data. Explain
     whether batch, streaming, or orchestration exists.
   - Connect relevant lifecycle undercurrents: security, data management, DataOps,
     data architecture, orchestration, and software engineering.
   - Explain what is missing or unknown rather than inventing a data platform.

6. Data behavior and guarantees — DDIA
   - Explain the repo's data models, access patterns, schemas, indexes, and
     serialization/versioning where present.
   - Where relational queries exist, map table relationships, join keys,
     cardinality, filters, projections, and relevant indexes to a real read path.
     Account for ORM-generated queries and N+1 lookups when observable.
   - Evaluate query performance with available plans, timings, tests, or query
     counts; distinguish measured findings from hypothetical costs of joins,
     row counts, selectivity, indexes, and data returned. Never invent timings
     or execute production queries or EXPLAIN ANALYZE.
   - Compare normalized relationships and read-time joins with any observed
     denormalized or stored-derived alternative: effects on read cost, writes,
     storage, update anomalies, source-of-truth ownership, freshness, and
     refresh/sync complexity. Discuss when an alternative might make sense,
     not an unsupported verdict that one data model is always faster.
   - Identify the source of truth and derived state, including client state,
     caches, materialized outputs, or replicated copies.
   - Trace actual transaction boundaries, concurrent updates, cache invalidation,
     retries, and idempotency. Explain the guarantee and its limits in plain terms.
   - Discuss replication, partitioning, consistency, and batch/stream processing
     only if evidence makes them relevant. Do not infer a strong guarantee from
     a database name or a "transaction" wrapper alone.
   - Use a concrete failure scenario to explain reliability and correctness:
     what persists, what can be lost or duplicated, and how recovery works.

7. Computational reasoning — Algorithmic Thinking
   - Select two or three meaningful examples from inspected code, if available:
     lookup/deduplication, sorting/filtering, traversal, scheduling, parsing,
     aggregation, or another computational task.
   - State each problem, inputs, outputs, constraints, chosen data structure,
     approach, and correctness condition.
   - Walk through a tiny example and explain the clues that make this approach fit.
   - Define input-size variables before giving time/space complexity. State
     assumptions, including expected versus worst-case behavior when relevant.
   - Separate in-memory algorithm cost from database queries, network latency,
     and external-library behavior. Do not assign unsupported Big-O to opaque calls.
   - Compare a simple alternative and when the trade-off would matter. Keep this
     explanatory; do not implement a replacement or force advanced algorithms
     into a repo whose code does not use them.

End Stage 2 with a short explanation connecting domain rules, runtime components,
code organization, data lifecycle, and algorithms. Ask three open-ended questions
and wait for "continue," unless I requested the complete guide.

Stage 3 — Learn to investigate and explain the repo

8. Failure, security, and performance
   - Show where validation, authentication/authorization, error handling,
     logging/metrics, timeouts, and retries live, when applicable.
   - Trace one failure from its origin to its visible result and recovery path.
   - Identify representative tests for important rules and failure behavior.
     Distinguish tested behavior from assumptions or missing coverage.
   - Explain how to investigate one representative issue: where to start,
     what evidence to collect, and how to distinguish plausible causes.
   - Use System Design Interview to discuss the likely first bottleneck under a
     stated hypothetical workload. Label estimates and assumptions; suggest what
     to measure before asserting a production bottleneck or scaling requirement.

9. Design trade-offs and learning summary
   - Select up to three important existing decisions. Explain the observed design,
     its benefits/costs, and a plausible alternative. Label inferred rationale.
   - Where a relational data-model choice is material, include the trade-off
     between read-time joins and stored derived/denormalized data, with actual
     query evidence or clearly labeled performance questions.
   - Connect the four book lenses without repeating four versions of the guide.
   - Finish with this learning table:
     Book | Relevant concept | Repo evidence | What I should now understand |
     Next reading topic
   - Use the labels DDIA, FODE, System Design Interview, and Algorithmic Thinking.
     Mark a lens with limited applicability honestly.
   - Add a brief glossary and unresolved questions worth asking a maintainer.

10. Practical onboarding path
    - Give a suggested progression for the first session, next few sessions, and
      later study. For each step, include a file/flow, a learning goal, and a way
      to demonstrate understanding. Adapt it to my time if provided.
    - Finish with five repo-specific teach-back questions and one small read-only
      exercise, such as annotating a flow, predicting behavior from a test, or
      tracing an input. Do not assign feature work or require a redesign.

Onboarding is successful when I can:
- Explain the repo's purpose and major areas.
- Locate its entry points and follow a representative execution path.
- Describe where data/state comes from, changes, and reaches consumers.
- Explain one relevant correctness guarantee and one computational trade-off.
- Identify the local workflow and know whether it has been verified.
- Investigate a representative failure and state what remains unknown.
```

## Quick repo orientation prompt

Use this for a compact overview before deeper onboarding.

```text
Onboard me as a junior developer to this whole repository in one concise pass.
Inspect the repo first, adapt to its type, and cover all major first-party areas.

1. What does this repo do, for whom, and what are its boundaries?
2. Map its major directories/packages, responsibilities, and entry points.
3. Explain its domain model, runtime architecture, and code organization separately.
4. Identify the local setup, run, and check commands; state whether they were run.
5. Trace one representative flow and identify the important areas it does not cover.
6. Connect relevant evidence to DDIA (2nd edition), FODE, System Design Interview
   (Alex Xu), and Algorithmic Thinking (2nd edition, Daniel Zingaro).
7. Explain one failure path, one design trade-off, and the main unknowns.
8. Recommend up to five first files to read, each with a learning goal.

Cite files and symbols. Separate verified behavior from inference. Define jargon,
do not assume missing infrastructure, and use topic names rather than unverified
book chapter/page references. Keep the workflow read-only; do not implement changes.
End with three open-ended comprehension questions and one small tracing exercise.
```

## Teach-back self-test

Use this after either orientation prompt.

```text
Interview me about this repository one open-ended question at a time.
Start with purpose and navigation, then cover architecture, execution/data flow,
correctness, relevant algorithms, and investigating failures.

Wait for my answer before giving feedback. When it is incomplete, ask a targeted
follow-up or give a small hint before explaining the missing part. Ground your
feedback in the inspected repo's files and symbols.

Connect relevant explanations to DDIA, FODE, System Design Interview, or
Algorithmic Thinking. Do not introduce infrastructure or algorithms absent from
the repo. Keep this about understanding the existing codebase, not feature work.

After five questions, summarize what I understand, what needs another pass, and
the next file or flow to revisit. Do not claim to hide or erase earlier messages.
```

## Keep the layers distinct

| Layer | What it explains | Evidence to inspect |
| --- | --- | --- |
| Domain model | Real-world concepts, relationships, and rules | Domain types, validation, tests, product docs |
| System design | Runtime components, boundaries, and communication | Entry points, API contracts, runtime/deployment configuration |
| Software design | How code is organized inside those components | Modules, interfaces, imports, functions, framework conventions |
| Data lifecycle and guarantees | How data moves and what remains correct | Schemas, transformations, storage calls, transaction/retry behavior |
| Computational foundations | How code solves a specific problem | Data structures, algorithms, loops, constraints, tests |

For example, in a skill-tree app, a prerequisite is a domain relationship; a UI
calling an API is system design; a graph repository interface is software design;
saving progress and refreshing derived state concern data flow and correctness;
and checking for a cycle is an algorithmic problem. This example illustrates the
layers—it is not an architecture to assume in the target repo.

## Book references

These official pages establish the books and topic scope. The prompt's repo
onboarding structure is an adaptation, not a quoted framework from any one book.

- [Designing Data-Intensive Applications, 2nd edition — O'Reilly](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/)
- [Fundamentals of Data Engineering — O'Reilly](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/)
- [System Design Interview — ByteByteGo](https://bytebytego.com/courses/system-design-interview)
- [Algorithmic Thinking, 2nd edition — No Starch Press](https://nostarch.com/node/745)
