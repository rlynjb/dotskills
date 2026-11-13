# Optional learning references — REAZN

**Use this reference only when the invoking user enables `learn: on`.** A standard REAZN assessment uses SDI and evidence-backed reasoning without book suggestions. This is a **topic-to-chapter lookup**, not a second framework, a list of compulsory reading, or a substitute for inspecting the actual system/process.

## Output contract

- Add a short **`*Further reading:`** line **inside each materially relevant finding**, after its source/evidence, verdict or reasoning lines. Include **book title, edition/volume, chapter number and title**, plus a short **`*Study focus:`** line explaining which *specific concept in this finding* the chapter helps explore.
- **Compact spacing applies to learning fields:** no blank line between the item heading, factual labels, `*Further reading:` or `*Study focus:`. Separate complete findings by exactly **one blank line** (or the Step 2 divider). In Markdown, use two trailing spaces for nonfinal field lines so each label renders on its own line without paragraph gaps.
- **Literal-label rendering:** The leading `*` is a visible asterisk, **not** a bullet marker or emphasis. In Markdown output escape it as `\*Further reading:` / `\*Study focus:` so it renders literally. In plain text or fenced examples use `*Further reading:` / `*Study focus:`. No space after `*`; factual labels such as `Source:` and `Evidence:` remain unchanged.
- The study reference is **educational context only**. It is **not** a citation proving the finding or a justification for an unverified design. Keep actual source evidence in the existing `Evidence:` / `Source:` field, and explain any assumptions normally.
- Suggest a chapter only when the finding genuinely concerns its topic, choosing **at most one strong matching chapter per item** by default. Skip irrelevant items, avoid repeating the same chapter without a distinct reason, and avoid flooding the report with a generic list of all six books. Do not add a standalone learning section, additional SDI step, quiz, exercise, checkpoint, or interactive mode.
- Never invent chapter names/numbers, page references, quotations, links, measured behavior or causal findings. Confirm edition-specific chapters using these documented tables of contents or another authoritative edition-matched source. If the exact chapter cannot be confirmed, omit the numbered recommendation rather than guessing.
- If `learn: off` or unspecified, **do not output any `*Further reading:` or `*Study focus:` fields, optional-learning placeholders, chapter suggestions or references to this guide**.

## Six-book chapter lookup

Choose from the six books also supported by [Learn Implementation](../../learn-implementation/references/master-implementation-learning.md). The existing five-book chapter references follow that guide; chapter numbers for the sixth book are verified against [Manning's second-edition chapter-by-chapter contents](https://livebook.manning.com/learn/ai-agents-in-action-second-edition). The mapping is duplicated here so REAZN packages its optional reference independently.

### 1. *System Design Interview — An Insider's Guide*, Volumes 1 and 2

**Volume 1 — Alex Xu (framework and fundamentals)**

- **Volume 1, Chapter 3 — A Framework for System Design Interviews:** problem framing; clarifying scope, high-level design, deep dives and trade-offs. Useful across domains only where the analogy fits.
- **Volume 1, Chapter 2 — Back-of-the-envelope Estimation:** capacity and sizing assumptions only when estimation matters.
- **Volume 1, Chapter 1 — Scale From Zero To Millions Of Users:** growth and scaling mechanisms only when relevant.
- Volume 1 contents: [Alex Xu's book comparison and chapter list](https://blog.bytebytego.com/p/system-design-interview-books-volume).

**Volume 2 — Alex Xu and Sahn Lam (deeper case studies and trade-offs)**

These are **case studies**, not replacements for the four-step SDI reasoning framework. Recommend them only when the finding actually involves the described design problem. Preserve **Volume 2** in every numbered recommendation so Chapter 4 is not confused with Volume 1.

- **Volume 2, Chapter 1 — Proximity Service:** proximity search and geographic discovery design.
- **Volume 2, Chapter 2 — Nearby Friends:** nearby-user discovery and location-update workflows.
- **Volume 2, Chapter 3 — Google Maps:** mapping/navigation services and relevant geographic data flows.
- **Volume 2, Chapter 4 — Distributed Message Queue:** asynchronous delivery, messaging boundaries and queue design.
- **Volume 2, Chapter 5 — Metrics Monitoring:** metrics collection, monitoring pipelines and observability.
- **Volume 2, Chapter 6 — Ad Click Event Aggregation:** event ingestion, aggregation and data pipelines.
- **Volume 2, Chapter 7 — Hotel Reservation:** reservation/inventory workflows and consistency under concurrent requests.
- **Volume 2, Chapter 8 — Distributed Email Service:** large-scale message delivery, queues and retry/failure handling.
- **Volume 2, Chapter 9 — S3-like Object Storage:** object storage and storage/retrieval design.
- **Volume 2, Chapter 10 — Real-time Gaming Leaderboard:** continuously updated ranking/leaderboard design.
- **Volume 2, Chapter 11 — Payment System:** payment workflow boundaries and transaction correctness.
- **Volume 2, Chapter 12 — Digital Wallet:** transfers, balances and ledger/data-consistency concerns.
- **Volume 2, Chapter 13 — Stock Exchange:** trading workflow design, ordering and latency considerations.
- Volume 2 authors/contents: [Alex Xu's ByteByteGo book comparison and full chapter list](https://blog.bytebytego.com/p/system-design-interview-books-volume) and [Google Books bibliographic entry](https://books.google.com/books/about/System_Design_Interview_An_Insider_s_Gui.html?id=1Sr7zgEACAAJ).


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

### 6. Micheal Lanham — *AI Agents in Action*, Second Edition (Manning, June 2026)

- **Chapter 1 — The rise of AI agents:** distinguish assistants from agents, five functional agent layers, tool-using behavior, and multi-agent models.
- **Chapter 2 — Core components: Large language models, prompting, and agents:** prompting, agent inputs/typed outputs, tool integration and traces.
- **Chapter 3 — Actions with Model Context Protocol for AI agents:** MCP clients/servers, tools/resources/prompts, local/remote integration and protocol boundaries.
- **Chapter 4 — Architecting and building multi-agent systems:** single-agent vs. multi-agent trade-offs, orchestration, handoffs and guardrails.
- **Chapter 5 — Agent reasoning and planning:** decomposition, planning, ReAct and alternate reasoning patterns when actually relevant.
- **Chapter 6 — Working with memory and knowledge RAG for agents:** retrieval, hybrid search, indexed knowledge and agent memory, including context freshness.
- **Chapter 7 — Building robust agents with evaluation and feedback:** regression/evaluation design, rubrics, grounding, human feedback and observability.
- **Chapter 8 — Deploying agents and agentic systems:** deployment, identity, tool safety, timeouts, versioning, reliability and production boundaries.
- **Chapter 9 — Understanding the agentic loop:** inner/task/meta loops, stop conditions, long-running task state and orchestration.
- **Chapter 10 — Exploring the cognitive agent that thinks, monitors, and adapts:** metacognitive checks, confidence gates and stagnation detection; only for genuinely relevant adaptive-agent designs.
- Chapter numbers and names are from [Manning's second-edition chapter-by-chapter contents](https://livebook.manning.com/learn/ai-agents-in-action-second-edition). [Publisher book page](https://www.manning.com/books/ai-agents-in-action-second-edition). **Manning is the publisher; Micheal Lanham is the author.** The second-edition numbering must not be inferred from the first edition.

## How to choose

- **Requirements, scope, estimation:** Alex Xu, Volume 1, Chapter 3 (or Chapter 2 when estimating); DDIA 2e Chapter 2 for **real NFRs**. Volume 2 complements these with specific case studies rather than another general-purpose reasoning framework.
- **Service/module contracts, boundaries, data ownership:** Ousterhout Chapters 4–6 or DDIA 2e Chapter 1; choose the one directly relevant to the finding.
- **Actual queries, storage, transactions, event streams:** relevant DDIA 2e chapters; FODE for data pipelines and ingestion/serving. When useful, choose a matching **Alex Xu & Sahn Lam Volume 2** case study: Chapter 4 for a distributed queue, Chapter 5 for metrics, Chapter 7 for booking concurrency, Chapter 9 for object storage, or Chapters 11–12 for payments/transfers.
- **Concrete algorithms, complex traversals, search patterns:** matching Zingaro chapter only when that data structure or algorithm is present or a plausible material alternative.
- **AI-agent / agent-skill design:** use Lanham, 2nd ed., Chapter 1 or 2 for agent scope and tools, Chapter 3 for real MCP boundaries, Chapter 4 for multi-agent handoffs, Chapter 5 for planning, Chapter 6 for RAG/memory, Chapter 7 for evals/feedback, Chapter 8 for deployment/security, or Chapter 9 for looping/stop conditions. Pick the **one** closest to the specific finding, not all of them.
- **Non-code business process:** do **not** force AI-agent, database, algorithm or software-module readings onto a workflow. Use Alex Xu Chapter 3 if it genuinely helps structured problem framing; otherwise **omit** a chapter for that finding.

**Illustrative formatting; not evidence for a real project:**

```text
Area: API ownership
What exists today: The inspected service owns the write operation.
Evidence: [verified path/symbol]
Verdict: FOLLOW
Why: Preserves the existing ownership boundary.
*Further reading: A Philosophy of Software Design, 2nd ed. — Chapter 5, Information Hiding (and Leakage).
*Study focus: Why limiting internal implementation details at a boundary reduces coupling.
```

When learning is disabled, the last two lines are absent. All other findings, IDs, decisions, evidence labels, source links, diagrams, and one-pass boundaries remain unchanged.
