# Skill Responsibility & Overlap Audit — Report Template

Use as an **output guide, not a source of facts**. Replace all bracketed placeholders with actual findings and direct source links. Keep the seven section headings stable.

## 1. Executive Summary

- **Scope:** [Skills, revisions, known workflow.]
- **Available evidence:** [Files inspected; inaccessible files.]
- **Main observations:** [Two or three grounded findings.]
- **Unverified:** [Important evidence limits, such as traces not inspected; do not automatically create F-xx VERIFY or claim runtime failure.]

## 2. Individual Skill Assessments

**Use the original compact side-by-side layout.** The Primary and Supporting tables both have the same skill columns. Cells contain **short summaries only**. After each table, put any meaningful fields on **separate Markdown bullet lines** in an F-xx note directly underneath. No HTML tags or multi-line table cells.

**Primary considerations — analyze deeply, report compactly**

| Consideration | [Skill A] | [Skill B] |
| --- | --- | --- |
| 1. Inputs (C1) | **F-01 · CLARIFY** — Discovery wording sounds mandatory. [source] | Starts from a ticket or idea. [source] |
| 2. Responsibilities (C2) | **F-02 · KEEP** — Owns initial product requirements. [source] | Reviews requirements against evidence. [source] |
| 3. Outputs (C3) | Produces a draft PRD. [source] | Produces a requirements review. [source] |

**F-01 (C1) — [Skill A] · CLARIFY**
- **Finding:** Wording may imply discovery is required.
- **Evidence:** DOCUMENTED — [source]; potential impact INFERRED.
- **Assessment:** CLARIFY.
- **Why:** Could delay a valid provisional draft.
- **Recommendation:** Clarify optional discovery for human review.
- **Current wording:** "[Exact inspected text.]"
- **Concern:** [What an agent might misunderstand.]
- **Recommended wording — PROPOSED:** "[Source-aligned replacement.]"

**F-02 (C2) — [Skill A] · KEEP**
- **Finding:** Product requirements have a clear owner.
- **Evidence:** DOCUMENTED — [source].
- **Assessment:** KEEP.
- **Why:** Keeps a standalone deliverable.
- **Recommendation:** Preserve the current responsibility.

*The findings and sources above are illustrations only. Include an F-xx note for real material findings, not every routine cell; list the fields on separate lines.*

**Supporting considerations — identify issues, defer formal design**

| Consideration | [Skill A] | [Skill B] |
| --- | --- | --- |
| 4. Handoffs (C4) | Documented optional outbound context. [source] | Documented optional inbound context. [source] |
| 5. Boundaries (C5) | Drafts within authorized scope. [source] | Review-only, no silent upstream edits. [source] |
| 6. Feedback (C6) | Human owner reviews accepted proposals. [source] | Returns proposed changes and questions. [source] |

For material C4–C6 findings, show the same **F-xx (Cx) vertical notes immediately here**, before Section 3. Do not create separate tables or move the findings to the end of the report.

**C4 triage:** Clear documented handoff + missing runtime trace = ordinary evidence limit, not F-xx VERIFY. Create a finding only for material ambiguous/conflicting instructions (CLARIFY/REVISE), explicit unsupported runtime guarantees, user-requested execution assurance, or concrete security/reliability/authorization risk (targeted VERIFY).

**Quality Review Coverage (optional; only when Q review is requested)**

Show the **complete original question wording**, not only the Q-ID. The following table is a formatting **template**, not actual coverage or evidence. Replace all placeholders with inspected statuses, concise direct source links or evidence limitations, and related **existing** F-xx (Cx) IDs when material; otherwise omit the F reference. A full review uses all ten rows in canonical order, and `quality_questions` subset mode includes only the selected rows.

| Quality question | [Skill A] | [Skill B] |
| --- | --- | --- |
| **Q-01 — Purpose & boundaries** — Does the skill explain its job, intended users, when not to use it and prohibited actions? | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] |
| **Q-02 — Activation & discovery** — Are discovery, invocation, trigger conditions and incorrect-trigger handling defined for its intended host? | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] |
| **Q-03 — Structure, inputs & dependencies** — Are entry points, required inputs, resources/context, tools, environment assumptions and unavailable-source handling established? | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] |
| **Q-04 — Workflow & orchestration** — Are workflow stages, decision rules, applicable delegation/aggregation and human gates defined? | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] |
| **Q-05 — Contracts & outputs** — Are required inputs, outputs, validation, invariants, ownership and failed handoffs defined? | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] |
| **Q-06 — Context & trust** — Are evidence provenance, freshness, contradictions, untrusted input treatment and source-backed conclusions addressed? | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] |
| **Q-07 — Permissions & effects** — Are permitted effects, authorization boundaries, least privilege and applicable host/tool/server enforcement evidenced? | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] |
| **Q-08 — Failure & stop behavior** — Are missing resources, errors, partial outcomes, relevant retries/timeouts, stopping and escalation handled? | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] |
| **Q-09 — Evals & observability** — Are evaluation cases, existing runs/traces, grading, known gaps and regression evidence identified accurately? | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] |
| **Q-10 — Lifecycle & portability** — Are ownership, versions, review/rollback, dependencies and claimed harness compatibility supported? | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] | [Status] — [brief source / evidence limit]; [F-xx (Cx) if material] |

**Rules:** Put this optional comparison table **after** the Supporting C4–C6 table and related F-xx notes, still inside Section 2. For a single skill, use `Quality question | [Skill A]`. With three or more skills, group them into comparison tables with **at most two skill columns** per group, repeating the same selected canonical Q rows for complete coverage. Keep all statuses/source links concise and F-xx references attached to the existing C-row findings. Never replace the C1–C6 tables, create a new numbered report section, add HTML tags, or invent status values, findings, or observed runs. A lens-only or default run does **not** generate the Q table.

**Review Lens Coverage (optional; only when lenses requested)**

A diagnostic index linked to **existing F-xx (Cx)** findings, not a new findings section. The five rows below use the actual **Stage 2 source-defined review questions** from [review-lenses.md](review-lenses.md). An actual report shows only named lenses or evidence-supported relevant lenses. For `review_lenses: relevant`, explain which lenses apply and why. If Q review was also requested, place this table **after Quality Review Coverage**; otherwise immediately after the Supporting C4–C6 findings.

| Lens & diagnostic questions | [Skill A] | [Skill B] |
| --- | --- | --- |
| **Context Engineering** — Are provenance, revisions, evidence gaps and contradictions preserved? Is the source of truth identified? Are instructions found inside untrusted documents treated as data rather than authority? Does a consumer treat another skill's output as evidence rather than silently inheriting its decision authority? *C1 Inputs; C4 Handoffs; C5 Boundaries. Q-03, Q-06.* | [Concise source-backed observation; F-xx (Cx) if material] | [Concise source-backed observation; F-xx (Cx) if material] |
| **Security & Trust** — What is the real permission boundary? Is least privilege enforced by tool/host/server controls? How does the skill handle untrusted instructions, missing approval and unauthorized effects? If one skill or coordinator delegates to another, who authorizes the next action and what authority actually transfers? *C1 Inputs; C4 Handoffs; C5 Boundaries; C6 Feedback. Q-06, Q-07.* | [Concise source-backed observation; F-xx (Cx) if material] | [Concise source-backed observation; F-xx (Cx) if material] |
| **Reliability & Workflow** — Are conditions for proceeding, stopping or returning clear? Are failed/missing handoffs surfaced rather than hidden? Does a proposed coordinator actually solve an evidenced coordination issue? When a result is incomplete, blocked, pending or needs human input, is the next responsible owner identifiable? *C2 Responsibilities; C4 Handoffs; C5 Boundaries; C6 Feedback. Q-04, Q-05, Q-08.* | [Concise source-backed observation; F-xx (Cx) if material] | [Concise source-backed observation; F-xx (Cx) if material] |
| **Evaluation & Observability** — Are critical user journeys, fixtures, baselines and evaluation criteria clear? Are output, trajectory and outcome distinguished? Are eval definitions separated from actual runs, tool traces, token cost and failure evidence? Is an apparently redundant skill or additional layer backed by a concrete responsibility or meaningful outcome rather than a speculative cost claim? *C2 Responsibilities; C3 Outputs; C6 Feedback. Q-09.* | [Concise source-backed observation; F-xx (Cx) if material] | [Concise source-backed observation; F-xx (Cx) if material] |
| **Lifecycle & Portability** — Is there one current source of truth, with recorded owner/version? Are linked resources present? Are claimed hosts actually tested? Is review, rollback and release evidence available? Do multiple skills or instruction files repeat conflicting or stale versions of the same boundary rule? *Cross-cutting C2 Responsibilities; C4 Handoffs; C5 Boundaries. Q-03, Q-10.* | [Concise source-backed observation; F-xx (Cx) if material] | [Concise source-backed observation; F-xx (Cx) if material] |

**Cells:** Short finding diagnosis with direct **inspected skill evidence** and existing **F-xx (Cx)** only when material; otherwise `No material issue identified — [source]`, `NOT APPLICABLE — [reason]` or `NOT ASSESSED — [missing source]`. Full Finding/Evidence/Assessment/Why/Recommendation stays in the original vertical note under the relevant Cx table. A missing execution trace alone is not a VERIFY finding. With three or more skills, group comparisons into tables with **at most two skill columns**, repeating selected rows; one skill gets one skill column.

**Conference Sources & Further Reading (optional; only when lenses requested)**

Show this **immediately after Review Lens Coverage, still inside Section 2**. The five rows below are a **formatting example with one primary session per lens**, not a claim that these exact sources apply to every case. For each selected lens, choose 1–3 actually relevant sessions from [review-lenses.md](review-lenses.md), preserving topic, **exact session title and speaker**, direct **saved PDF**, and **matched YouTube** where available. If there is no matched video, show `—`, not an invented URL. Consolidate repeated presentations across lenses and do not list unrelated sources.

| Lens / Topic | Conference session & speaker | PDF | YouTube |
| --- | --- | --- | --- |
| Context Engineering — Provenance and untrusted stored context | **Trustworthy Context Is Untrusted by Default** — Shub Argha | [PDF](https://drive.google.com/file/d/19aoCF7WZ2GfVi7vb5ISZHIPKkQOtjjz1/view) | — |
| Security & Trust — Delegation boundaries, who acts under whose authority | **When Agents Spawn Agents: Securing Recursive Delegation in Multi-Agent Systems** — Anishma Mavuram | [PDF](https://drive.google.com/file/d/1_jXpA_vFEBAAPYeklZmliAs9jNWZTyWx/view) | [YouTube](https://www.youtube.com/watch?v=glxs_6J-7sQ) |
| Reliability & Workflow — Completion, additional-input, asynchronous and progress states | **Agentic Messaging Primitives in MCP** — Caitie McCaffrey | [PDF](https://drive.google.com/file/d/1OwyNvZGpIFDnc9KchDq5uER9DpgzLG4g/view) | [YouTube](https://www.youtube.com/watch?v=iNV5-YkPHW4&t=21711s) |
| Evaluation & Observability — Critical user journeys and costs of over-broad skills | **Building an Agentic Eval Pipeline: Battle-Tested Lessons with EvalBench** — Kurtis Van Gent and Haoyu Wang | [PDF](https://drive.google.com/file/d/1us0-hWJPMvH7dw2ZGoCvbRRUtJBFSyBf/view) | — |
| Lifecycle & Portability — One source of truth; concise instructions and stale-rule detection | **AGENTS.md Is the New CONTRIBUTING.md: A Field Report from One Year of Agent-Friendly Monorepos** — Unnati Mishra | [PDF](https://drive.google.com/file/d/1ICV_vH6Q5qAAu-2sodIs03Ffbxv6Tl4P/view) | — |

**Source distinction:** Session slides and recordings support the *engineering questions and further learning*, not findings about the inspected skill. F-xx findings require direct skill source links or supplied real run evidence. Source links in this table should be directly clickable. The video matches are from the user's saved title/speaker YouTube–PDF index; no claim is made that a recording was watched. **Lens-only does not activate Q-01–Q-10** despite the Q mapping in the first table.

**Layout contract:** Both optional lens subsections stay within Section 2, after any optional Q table, and do not change the seven numbered report sections or the two core C1–C6 tables. No HTML breaks, giant skill cells or duplicate findings. Default and Q-only reports omit both lens tables.

**Industry Framework Review Coverage (optional; only when industry review is enabled)**

A **framework-informed Stage 2 diagnosis**, not an independent audit, certification or behavioral validation. The five rows below show the reference's **adapted investigation questions**, which are **not verbatim published requirements**. In the actual report include only the named `industry_frameworks` selection, frameworks justified by `industry_framework_review: relevant`, or all five (with NOT APPLICABLE if needed) for `industry_framework_review: on`.

| Framework & investigation questions | [Skill A] | [Skill B] |
| --- | --- | --- |
| **ISO/IEC 25010:2023 — Software Product Quality** — Which relevant product-quality concerns (for example, functional suitability, reliability, security, maintainability, compatibility or performance efficiency) are within this skill's responsibility? Are those expectations, outputs and exclusions documented rather than merely implied? Does a shared quality concern cause an actual ownership gap or only legitimate collaboration? *C1 Inputs; C2 Responsibilities; C3 Outputs; C5 Boundaries. Related optional Q-01, Q-03, Q-05.* | [Status; brief target evidence/limit; real F-xx (Cx) only if material] | [Status; brief target evidence/limit; real F-xx (Cx) only if material] |
| **AWS Well-Architected Agentic AI Lens** — Are current agent/skill roles, success boundaries and intended handoffs clear, including who owns each part? Are tool/security boundaries, human gates, failure expectations and monitoring claims appropriately documented? Is a coordinator's responsibility supported by real workflow needs rather than assumed to be mandatory? *C2 Responsibilities; C3 Outputs; C4 Handoffs; C5 Boundaries; C6 Feedback. Related optional Q-04, Q-05, Q-07, Q-08, Q-09.* | [Status; brief target evidence/limit; real F-xx (Cx) only if material] | [Status; brief target evidence/limit; real F-xx (Cx) only if material] |
| **NIST AI Risk Management Framework (AI RMF 1.0)** — Who currently owns risk decisions, human oversight, change authorization and escalation for the selected skill? Are the intended uses, assumptions, boundaries and material AI risks documented? Are governance, risk assessment and claimed measurement/monitoring responsibilities distinguished from evidence that those practices actually occur? *C1 Inputs; C2 Responsibilities; C5 Boundaries; C6 Feedback. Related optional Q-01, Q-06, Q-07, Q-09.* | [Status; brief target evidence/limit; real F-xx (Cx) only if material] | [Status; brief target evidence/limit; real F-xx (Cx) only if material] |
| **CMU SEI Architecture Tradeoff Analysis Method (ATAM)** — What stakeholder goal or quality scenario makes this responsibility/handoff question important? Which quality attributes or responsibilities could compete, such as reliability versus simplicity or security versus flexibility? Does current source evidence reveal a material risk, ambiguity or trade-off worth discussing with a human owner? *C2 Responsibilities; C3 Outputs; C4 Handoffs; C5 Boundaries; C6 Feedback. Related optional Q-01, Q-04, Q-05, Q-08.* | [Status; brief target evidence/limit; real F-xx (Cx) only if material] | [Status; brief target evidence/limit; real F-xx (Cx) only if material] |
| **OWASP Top 10 for Agentic Applications (2026)** — Does the inspected skill expose or delegate tool use, accept source instructions, retain memory or exchange context across agents, and if so who owns the risk? Are relevant threats such as tool misuse, identity/privilege abuse, memory/context poisoning, insecure inter-agent communication or cascading failures addressed or explicitly deferred? Are claimed security restrictions actually enforced by an inspected tool/host or merely written in prompt text? *C1 Inputs; C2 Responsibilities; C4 Handoffs; C5 Boundaries; C6 Feedback. Related optional Q-06, Q-07, Q-08.* | [Status; brief target evidence/limit; real F-xx (Cx) only if material] | [Status; brief target evidence/limit; real F-xx (Cx) only if material] |

**Coverage rules:** Use concise `PRESENT / PARTIAL / MISSING / NOT VERIFIED / NOT APPLICABLE` based on inspected **target skill** evidence, direct source links/evidence limitations and real material **F-xx (Cx)** only. Keep detailed F-xx explanations under original C1–C6 tables. With one skill use one skill column; for 3+ skills group at most two skill columns per comparison and repeat selected rows. No general VERIFY findings solely for missing traces, no new framework finding IDs, and no implication that optional Q or conference questions were run.

**Official Industry Framework Sources & Further Reading (optional)**

Immediately below industry coverage, still within Section 2, include direct **official publisher links** for selected frameworks only. This full example is for formatting; the reference provides additional original links. Identify the source type accurately because these are not all international standards.

| Framework / type | Topic or official section | Publisher & version | Official URL |
| --- | --- | --- | --- |
| **ISO/IEC 25010:2023 — International Standard** | Software product-quality model | ISO/IEC, 2023 | [Official source](https://www.iso.org/standard/78176.html) |
| **AWS Agentic AI Lens — Vendor architecture guidance** | Agent roles, handoffs and operational risks | AWS, June 2026 | [Official source](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentic-ai-lens.html) |
| **NIST AI RMF 1.0 — Voluntary risk framework** | Govern, Map, Measure and Manage | NIST, 2023; revision in progress | [Official source](https://airc.nist.gov/airmf-resources/airmf/) |
| **CMU SEI ATAM — Architecture evaluation method** | Quality scenarios, risks and trade-offs | CMU Software Engineering Institute | [Official source](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) |
| **OWASP Agentic Top 10 (2026) — Community security guidance** | Agent-specific threat categories | OWASP GenAI Security Project, 2026 | [Official source](https://genai.owasp.org/top-10-for-agentic-applications-2026/) |

**Industry-review scope:** The presence of an official-source link supports the adapted *question*, not the correctness of an audited skill or compliance with an external framework. This is not a completed ATAM, AWS workload review, NIST conformity assessment, ISO certification, OWASP exploit test, implementation or Stage 5 behavioral evaluation. Keep all original seven numbered headings; place these two subsections **after** optional Quality Review Coverage and optional Conference Review Lens Coverage plus conference readings, before Section 3. Neither industry subsection appears unless opted in.

**Core layout contract:** Retain the original two C1–C6 comparison tables and F-xx notes. Append only enabled optional views in this order: Quality Review Coverage, Conference Review Lens Coverage and sources, then Industry Framework Review Coverage and official sources. These are not new C1–C6 or findings tables. Keep full findings out of cells and preserve the seven numbered headings.

## 3. Cross-Skill Responsibility & Overlap Findings

For each real overlap, align the involved skills and reference the originating **F-xx (Cx)** cells; explain only the relationship or impact not already stated there.

| Activity | [Skill A] | [Skill B] | Classification |
| --- | --- | --- | --- |
| [Same activity] | [Its role] | [Its role] | [Intentional/shared, complementary, unnecessary duplication, conflicting, unclear] |

- **Why it matters:** [Consequence or legitimate benefit.]
- **Evidence:** [Direct links for each skill.]
- **Tentative ownership clarification:** [Proposed only, or none warranted.]

## 4. Missing Responsibilities & Gaps

- **Gap:** [What is missing or uncertain.]
- **Affected skills:** [Names.]
- **Evidence status / links:** [DOCUMENTED / INFERRED / UNVERIFIED.]
- **Potential effect:** [Specific consequence.]

## 5. Prioritized Recommendations

**Summarize, don't repeat:** Consolidate material CLARIFY/REVISE/ADD and VERIFY work by the **F-xx IDs in C1–C6 table cells and their immediate vertical findings**, with independent High/Medium/Low priorities. For wording concerns, point to the proposed replacement in the F-xx note rather than repeating it. KEEP generally requires no implementation item. If no change is justified, say so.

**An ordinary NOT VERIFIED scope note is not an actionable recommendation without a specific VERIFY trigger.**

- **Priority:** [High / Medium / Low]
- **Finding:** [F-xx, C1–C6, affected skill and assessment; refer to the vertical finding note rather than repeating its fields or recommended wording.]
- **Proposed change:** [Ownership/documentation proposal only; when appropriate, cite the per-skill proposed optional handoff, boundary, and feedback wording from section 2.]
- **Standalone integrity:** [Does each skill retain its own inputs, outputs and workflow? If not evidenced, what needs human confirmation?]
- **Skill cleanup:** [Per affected skill: evidence-backed responsibility, input/output, boundary or feedback clarification; cite existing passages when relevant. Do not prescribe new filenames, directories, reference artifacts or placement.]
- **Planning status / Stage 3:** [PLANNED / PROPOSED — NOT IMPLEMENTED. Identify what Stage 3 must agree before any integration claim.]
- **Benefit / trade-off:** [Including cost of change.]
- **Human confirmation:** [Required? Who, if known?]

**Optional coordinator assessment — only for a material combined-workflow coordination concern**

- **Decision:** [NOT NEEDED / OPTIONAL COORDINATOR RECOMMENDED / DEFER — UNVERIFIED]
- **Evidence and problem:** [Link to observed/documented routing, sequencing, context, human-review or feedback issue; distinguish proposed goals from observed runtime failures.]
- **Simpler alternative:** [Existing optional handoffs and copyable next-action prompts; why sufficient or insufficient.]
- **Minimal coordinator role (only if recommended):** [Separately invoked workflow entry point; selects starting stage, sequences optional steps, carries references/IDs/revisions/open questions, routes proposed changes for human review, reports completion.]
- **Non-ownership:** [Underlying skills retain their own inputs, outputs, domain decisions and standalone invocation. Coordinator does not silently rewrite, approve, or run them.]
- **Deferred design questions (only if recommended):** [Specific coordination needs or constraints that Stage 3 must address; do not select a routing/orchestration pattern or design an entry-point artifact here.]
- **Trade-off and validation:** [Added complexity, potential misrouting, availability of host/manual invocations and unknown runtime enforcement; actual multi-skill execution remains UNVERIFIED without traces.]
- **Human confirmation:** [Whether to investigate a separate optional coordination responsibility in later stages, not approval of a pattern or permission to create a file.]

If simple handoffs suffice, state **NOT NEEDED** with one reason; do not fill a long coordinator template. If facts are missing, **DEFER** and name the evidence needed. Do not create the coordinator skill in this audit.

## 6. Open Questions for Human Review

- [Question that would resolve a material ambiguity.]

## 7. Deferred Items for Integration-Contract Design

**Contract design questions — Stage 3 (when justified)**
- [Related F-xx/Cx; affected skill(s); unresolved handoff, guarantee, authorization, feedback, version or failure question; human decision needed. Defer contract drafting, naming conventions, artifact placement, directory structure and applicable interaction-pattern design to Stage 3.]
- [For an optional coordinator proposal, note future routing, context preservation, approvals and host compatibility as open design questions.]

**Validation candidates — Stage 5 (PROPOSED, NOT EXECUTED; only when materially justified or explicitly requested)**
- [Related F-xx: Given a representative input, when an approved and authorized workflow runs, then a specific observable result should occur. Note the artifact/trace evidence needed and Stage 3 dependency.]
- [Do not invent test outcomes, enforceability, readiness or approvals; omit speculative scenarios with no relevant finding.]

**Not designed or executed in this audit.** No contract, architecture or evaluation result is approved.

**Evidence note:** A target file's instructions are `DOCUMENTED`, not `OBSERVED` runtime behavior. Missing source access means `NOT ASSESSED`, not a failing skill.
