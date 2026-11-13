# Optional learning references — Refine Requirements Light

**Use this reference only when the invoking user enables `learn: on`.** The normal Refine Requirements Light assessment uses SDI and evidence-backed reasoning without book suggestions. This is a **topic-to-chapter lookup**, not a second framework, a list of compulsory reading, or a substitute for inspecting the actual system/process.

## Output contract

- Add a short **`Further reading:`** line **inside each materially relevant finding**, after its source/evidence, verdict or reasoning lines. Include **book title, edition/volume, chapter number and title**, plus a short **`Study focus:`** line explaining which *specific concept in this finding* the chapter helps explore.
- The study reference is **educational context only**. It is **not** a citation proving the finding or a justification for an unverified design. Keep actual source evidence in the existing `Evidence:` / `Source:` field, and explain any assumptions normally.
- Suggest a chapter only when the finding genuinely concerns its topic, choosing **at most one strong matching chapter per item** by default. Skip irrelevant items, avoid repeating the same chapter without a distinct reason, and avoid flooding the report with a generic list of five books. Do not add a standalone learning section, additional SDI step, quiz, exercise, checkpoint, or interactive mode.
- Never invent chapter names/numbers, page references, quotations, links, measured behavior or causal findings. Confirm edition-specific chapters using these documented tables of contents or another authoritative edition-matched source. If the exact chapter cannot be confirmed, omit the numbered recommendation rather than guessing.
- If `learn: off` or unspecified, **do not output any `Further reading:` or `Study focus:` fields, optional-learning placeholders, chapter suggestions or references to this guide**.

## Five-book chapter lookup

Choose from these five books already used by [Learn Implementation](../../learn-implementation/references/master-implementation-learning.md). The chapter guide there is the internal provenance for these pointers; edition and chapter mapping is duplicated here only so Refine Requirements Light can package its own optional reference independently.

### 1. Alex Xu — *System Design Interview — An Insider's Guide*, Volume 1

- **Chapter 3 — A Framework for System Design Interviews:** problem framing; clarifying scope, high-level design, deep dives and trade-offs. Helpful across domains **only where the analogy is useful**.
- **Chapter 2 — Back-of-the-envelope Estimation:** defensible capacity/sizing assumptions; only when scale/estimation actually matters.
- **Chapter 1 — Scale From Zero To Millions Of Users:** growth, capacity and system-design scaling mechanisms; not a default for every ticket or process.
- Edition/volume reference: [Volume 1 contents](https://www.harvard.com/book/9798664653403).

### 2. Martin Kleppmann and Chris Riccomini — *Designing Data-Intensive Applications*, 2nd edition (2026)

- **Chapter 1 — Trade-Offs in Data Systems Architecture:** competing data-system design choices and architectural boundaries.
- **Chapter 2 — Defining Nonfunctional Requirements:** reliability, scale, operational qualities and measurable constraints.
- **Chapter 3 — Data Models and Query Languages:** data models, schema fit and query representation.
- **Chapter 4 — Storage and Retrieval:** indexes, lookup patterns, persistence/retrieval costs.
- **Chapter 8 — Transactions:** transactions, concurrency and correctness of writes.
- **Chapter 12 — Stream Processing:** event streams and continuous processing where genuinely relevant.
- Edition-matched reference: [Second-edition TOC](https://www.oreilly.com/library/view/designing-data-intensive-applications/9781098119058/). **Do not substitute chapter numbers from the first edition.**

### 3. Joe Reis and Matt Housley — *Fundamentals of Data Engineering* (2022)

- **Chapter 2 — The Data Engineering Lifecycle:** source → ingestion → storage → transformation → serving and associated ownership.
- **Chapter 5 — Data Generation in Source Systems:** source data creation and source-system behavior.
- **Chapter 6 — Storage:** storage constraints and architectural choices.
- **Chapter 7 — Ingestion:** ingestion patterns and movement of incoming data.
- **Chapter 8 — Queries, Modeling, and Transformation:** transformations, models and query needs.
- **Chapter 9 — Serving Data for Analytics, Machine Learning, and Reverse ETL:** delivery to analytical or ML consumers.
- Reference: [Publisher's TOC](https://www.oreilly.com/library/view/fundamentals-of-data/9781098108298/).

### 4. Daniel Zingaro — *Algorithmic Thinking*, 2nd edition

- **Chapter 1 — Hash Tables:** keyed lookups, membership and hash structures.
- **Chapter 2 — Trees and Recursion:** recursive traversal and hierarchical structures.
- **Chapter 3 — Memoization and Dynamic Programming:** overlapping subproblems/caching intermediate results in algorithms.
- **Chapter 5 — Graphs and Breadth-First Search:** graph connectivity, traversal and shortest unweighted paths.
- **Chapter 7 — Binary Search:** ordered search and monotonic decision problems.
- Reference: [Publisher's TOC](https://nostarch.com/algorithmic-thinking-2nd-edition). Use only when the actual or credibly proposed mechanism relates to the chapter.

### 5. John Ousterhout — *A Philosophy of Software Design*, 2nd edition (2021)

- **Chapter 4 — Modules Should Be Deep:** useful interfaces and well-contained complexity.
- **Chapter 5 — Information Hiding (and Leakage):** reducing coupling and exposing only necessary knowledge.
- **Chapter 6 — General-Purpose Modules are Deeper:** justified, reusable abstractions and appropriate interfaces.
- **Chapter 20 — Designing for Performance:** performance trade-offs guided by real needs and measurements.
- Reference: [Author's second-edition notes](https://web.stanford.edu/~ouster/cgi-bin/book.php).

## How to choose

- **Requirements, scope, estimation:** Alex Xu, Volume 1, Chapter 3 (or Chapter 2 when estimating); DDIA 2e Chapter 2 for **real NFRs**.
- **Service/module contracts, boundaries, data ownership:** Ousterhout Chapters 4–6 or DDIA 2e Chapter 1; choose the one directly relevant to the finding.
- **Actual queries, storage, transactions, event streams:** relevant DDIA 2e chapters; FODE for data pipelines and ingestion/serving.
- **Concrete algorithms, complex traversals, search patterns:** matching Zingaro chapter only when that data structure or algorithm is present or a plausible material alternative.
- **Non-code process/agent-skill work:** do **not** force database, algorithms or software-module readings onto a workflow. Use Alex Xu Chapter 3 if it genuinely helps system-level problem framing; otherwise **omit** a chapter for that finding.

**Illustrative formatting; not evidence for a real project:**

```text
Area: API ownership
What exists today: The inspected service owns the write operation.
Evidence: [verified path/symbol]
Verdict: FOLLOW
Why: Preserves the existing ownership boundary.
Further reading: A Philosophy of Software Design, 2nd ed. — Chapter 5, Information Hiding (and Leakage).
Study focus: Why limiting internal implementation details at a boundary reduces coupling.
```

When learning is disabled, the last two lines are absent. All other findings, IDs, decisions, evidence labels, source links, diagrams, and one-pass boundaries remain unchanged.
