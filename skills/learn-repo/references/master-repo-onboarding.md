Act as a senior engineer onboarding a junior developer to this entire repository.

My goal is to understand the existing codebase well enough to navigate it, explain
its behavior, run it locally, and investigate a problem. This is not a request to
implement a feature, refactor the code, or design a replacement system.

Optional context:
- Repository / revision: [current workspace, or URL and branch/commit]
- My background: [languages/frameworks I know; unfamiliar areas]
- Time available: [optional]
- Delivery: [guided tutorial, one question at a time by default; complete tutorial if explicitly requested]

Use these five books as complementary teaching lenses:
- Designing Data-Intensive Applications, 2nd edition (DDIA), by Martin Kleppmann
  and Chris Riccomini.
- Fundamentals of Data Engineering (FODE), by Joe Reis and Matt Housley.
- System Design Interview, by Alex Xu.
- Algorithmic Thinking, 2nd edition, by Daniel Zingaro.
- A Philosophy of Software Design (APOSD), by John Ousterhout.

## Tutorial delivery — default


Use the three stages and eleven topics below as a technical coverage guide, not three large responses to deliver by default. Choose useful questions from inspected code and the relevant book lenses. Explain which lenses fit and why; do not force all five into every question. A question can teach an existing safeguard or design choice without implying a defect.

Open with the repository target, scope/revision when known, relevant lenses, mode, and read-only boundary. Use `Problem question N — Concrete question` headings; numbers count tutorial questions, not topic sections or lifecycle stages.

For each completed question, present:

1. **What and why:** explain the concept and why it matters here in plain English. Define unfamiliar terms at first use.
2. **Problem question:** ask about a concrete behavior, mechanism, or design decision in this repository.
3. **How to build an answer:** identify requirements, code paths, callers, contracts, and tests to examine.
4. **Worked answer:** provide an example answer grounded in inspected files and symbols. Explain the supporting evidence and unknowns; the answer is not automatically correct or the only valid answer.
5. **Walkthrough:** trace a small input, code path, data transformation, state change, or failure sequence. Clearly label hypothetical inputs and manual traces; do not present them as executed tests. Use a compact diagram when it improves understanding.
6. **Trade-off and follow-up:** explain a relevant alternative, its benefit and cost, and what constraint or evidence could change the choice.
7. **Takeaway:** state the transferable lesson and vocabulary to remember.
8. **LEARNING CHECKPOINT — Next question or explore this one?**

Keep explanations beginner-friendly, concrete, and tied to the repository. Avoid mechanical filler. Use concise public explanations of evidence and decisions.

- **Guided (default):** teach one question per response, including the worked answer and walkthrough, then pause at the checkpoint.
- **Practice (on request):** ask one question and wait before revealing the worked answer or walkthrough. After the learner answers or asks for help, give feedback or hints, then the teaching sections as appropriate. Clarifications stay on the same question.
- **Complete tutorial (on request):** present the relevant questions and worked answers together, followed by the glossary and learning summary; use one checkpoint at the end rather than pausing between questions.
- **Concise explanation (on request):** summarize behavior, mechanisms, trade-offs, and evidence without the teaching sequence.

Track coverage across questions: covered, not applicable with a reason, or unverified because evidence is missing. One answered question is not a complete repository onboarding. At completion or on request, provide the relevant glossary and learning summary and practical onboarding path from Stage 3, scope, coverage, remaining unknowns, and verification limits. Separate tests inspected, actually executed, and proposed. If the learner stops early, label the summary partial.

Do not append draft code review comments or a post-review comments section. This is an repository-learning tutorial. Discuss supported concerns as teaching points, distinguish confirmed issues from plausible risks and unknowns, and do not manufacture findings. Learning checkpoints govern pace only; they do not authorize code changes or external actions.

Keep the whole-repository scope: begin with purpose and the major-area map, then deepen execution/data flows and investigation skills. Use the three stages as a learning progression and coverage record, while the tutorial questions determine response pacing. Map every major first-party area at a useful level; a representative flow or one directory does not replace that map. Stage-end comprehension questions are optional practice prompts, not extra questions to ask all at once in Guided or Practice mode. Present them one at a time if the learner chooses practice.

## Working rules
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

## Stage 1 — Build the repo map

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
   - When Stage 1 coverage is complete, summarize the most important unknowns
     and preview Stage 2. Offer three open-ended comprehension questions as
     optional practice, delivered according to the selected tutorial mode.

Cover Stage 1 through tutorial questions before proceeding to deeper stages.
Pause after each completed Guided question at the learning checkpoint. A request
to continue advances the current tutorial; it does not restart onboarding.
If I explicitly request a complete guide, deliver all stages together.

## Stage 2 — Connect execution, data, and algorithms

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

8. Software design and complexity — APOSD
   - Select representative modules and their callers across the repository.
     Explain their responsibilities, public interfaces, and dependency direction.
   - Explain deep versus shallow modules by comparing the functionality provided
     with the complexity exposed to callers, not by counting lines or methods.
   - Identify information hiding: which design decisions stay inside a module,
     and which assumptions or details leak into other packages or callers?
   - Trace a small hypothetical change through actual files to explain change
     amplification, cognitive load, and unclear dependencies. Label the scenario
     hypothetical; distinguish observed coupling from predicted maintenance cost.
   - Walk through one interface from a caller's perspective: inputs, outputs,
     errors, defaults, and contracts. Explain what the caller must know and what
     the abstraction handles on its behalf.
   - Explain how naming, comments, and module boundaries communicate intent,
     invariants, and responsibilities. Define unfamiliar terms in plain English.
   - Discuss a simpler alternative only when supported by a concrete caller task
     or change scenario. Explain its cost and constraints; do not assume that
     more abstraction, smaller modules, or fewer lines automatically improve design.
   - Ground each lesson in files, symbols, and callers. Mark missing caller or
     contract evidence unknown; do not invent design history or author intent.
     Keep the exercise educational and read-only, without refactoring or draft
     code review comments.

End Stage 2 with a short explanation connecting domain rules, runtime components,
code organization, data lifecycle, algorithms, and abstraction complexity. Offer three open-ended questions
as optional practice, using the tutorial mode to control pacing. In Guided mode,
keep the learning checkpoint as the final section of the response.

## Stage 3 — Learn to investigate and explain the repo

9. Failure, security, and performance
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

10. Design trade-offs and learning summary
   - Select up to three important existing decisions. Explain the observed design,
     its benefits/costs, and a plausible alternative. Label inferred rationale.
   - Where a relational data-model choice is material, include the trade-off
     between read-time joins and stored derived/denormalized data, with actual
     query evidence or clearly labeled performance questions.
   - Connect the five book lenses without repeating five versions of the guide.
   - Finish with this learning table:
     Book | Relevant concept | Repo evidence | What I should now understand |
     Next reading topic
   - Use the labels DDIA, FODE, System Design Interview, Algorithmic Thinking,
     and APOSD (A Philosophy of Software Design).
     Mark a lens with limited applicability honestly.
   - Include the relevant APOSD lesson about interfaces, information hiding, or
     change complexity in the learning table and glossary.
   - Add a brief glossary and unresolved questions worth asking a maintainer.

11. Practical onboarding path
    - Give a suggested progression for the first session, next few sessions, and
      later study. For each step, include a file/flow, a learning goal, and a way
      to demonstrate understanding. Adapt it to my time if provided.
    - Offer five repo-specific teach-back questions (one at a time in Practice
      mode, together in a complete guide) and one small read-only
      exercise, such as annotating a flow, predicting behavior from a test, or
      tracing an input. Do not assign feature work or require a redesign.

Onboarding is successful when I can:
- Explain the repo's purpose and major areas.
- Locate its entry points and follow a representative execution path.
- Describe where data/state comes from, changes, and reaches consumers.
- Explain one relevant correctness guarantee and one computational trade-off.
- Explain one module boundary and how it hides or exposes complexity to callers.
- Identify the local workflow and know whether it has been verified.
- Investigate a representative failure and state what remains unknown.
