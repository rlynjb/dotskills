# Skill Integration Contracts — Stage 3 Report Template

This is the **default contract-design output template**, not a source of target facts or approvals. Replace brackets with actual inspected evidence. Keep the seven section titles and the source-backed junior-friendly explanations. `F-xx (Cx)` refers only to real prior Stage 2 findings; `IC-xx`, `D-xx` and `V-xx` are report-local Stage 3 references.

**Optional post-Stage-4 review:** When `implementation_alignment_review: on` is explicitly selected, use [implementation-alignment-review.md](implementation-alignment-review.md) and its **separate five-section source alignment report** instead of these seven design-mode sections. Don't silently rerun contract design, revise an approved baseline, change skill files or perform Stage 5 tests.

## 1. Executive Summary

- **Goal and integration scope:** [Which user goal and skill connection(s), not all possible pairs.]
- **Inspected sources:** [Exact skill paths/revisions, Stage 1 reference if supplied, Stage 2 report if supplied, current contracts if any.]
- **Recommendation:** [Smallest workable manual/optional handoff or bounded coordinator choice; status PROPOSED.]
- **Important uncertainty:** [Missing owner/permission decisions, absent source data or host evidence; don't invent a runtime failure.]

## 2. Current Skill Boundaries & Stage 2 Evidence

For 2–3 skills, keep a **compact side-by-side table**; don't put long findings inside cells:

| Consideration | [Producer skill] | [Consumer skill] |
| --- | --- | --- |
| Starting inputs | [Own required/optional inputs + direct source] | [Own required/optional inputs + direct source] |
| Owned responsibility | [What it decides + source] | [What it decides + source] |
| Independent outputs | [Complete standalone artifact + source] | [Complete standalone artifact + source] |
| Existing connection | [Documented vs proposed optional output; source] | [Documented vs proposed consumption; source] |
| Approval / feedback | [Decision authority + source] | [Return route + source] |

**Material Stage 2 findings carried forward:** [`F-01 (C4)` → affected contract/decision, direct audited source, or `No Stage 2 findings supplied`.] Treat original recommendations as *proposals*, not adopted design.

For a single skill, use a short vertical profile instead of inventing a second table column. For four or more, group by actual interaction to stay readable and summarize the overall flow.

## 3. Proposed Interaction & Ownership Map

Describe **only the connection(s) actually under review**; a local interaction is not necessarily the full workflow. **Choose details based on inspected source, supplied findings, justified design proposals or explicit user intent**, and identify DOCUMENTED vs PROPOSED paths. Keep the existing broader architecture intact unless a change is explicitly designed and approved.

- **Intended connection / standalone entry:** [Actual producer → consumer or one skill's own entry/exit; optional versus genuinely required context; avoid inventing a partner or independent behavior.]
- **Relevant interaction pattern — only if explanatory value:** [Name the **evidenced or explicitly proposed** behavior, e.g. direct handoff, conditional next-step branch, human approval gate, justified sequence, fan-out/fan-in, optional coordinator or conditional feedback. In **one or two sentences**, state **what initiates the path, what happens/which owner chooses, why it helps, and one material trade-off or constraint**. Label PROPOSED or NOT VERIFIED where appropriate; no pattern catalogue or mandatory new architecture. If no distinct pattern matters, **omit this item**.]
- **Proposed decision owner:** [Who produces, consumes, clarifies or approves a consequential change; do not guess.]
- **Conditional feedback route — include only when material:** [Identify an evidenced or specifically proposed return for clarification/revision: triggering finding, owner, approval requirement, what may change if authorized, and whether to revisit the affected step or continue without changes. Label a newly suggested loop PROPOSED. If no meaningful feedback path applies, **omit this bullet and the loop illustration**.]
- **Why standalone skills matter — include only when relevant:** [One or two team-facing sentences **only if** independent invocation, optional handoff or selective re-entry is supported by the evidence or is a justified design choice. Explain the practical branching/iteration benefit, and retain contract, actual prerequisite and human-approval boundaries. If standalone use is unsupported, contradictory or not relevant, describe the real dependency/uncertainty instead; **do not assert flexibility as a fact**.]
- **Simpler path vs coordinator — only if a coordination choice is material:** [NOT NEEDED / CONDITIONAL PROPOSAL / DEFER, with evidence and trade-off. Feedback alone does not require a coordinator.]
- **Human checkpoints — when applicable:** [Actual/proposed approval boundaries; distinguish a suggestion from an authorized change.]
- **ASCII diagram — only when it clarifies an actual relevant branch/return path:** [Use **plain ASCII** inside a fenced `text` code block. Keep short node labels and a narrow, vertical layout suitable for chat. Use simple ASCII arrows/connectors (`|`, `v`, `-->`, `+--`); **never Mermaid or render-dependent diagrams**. Omit absent branches and label proposed routing. If prose is enough, omit the diagram entirely.]

**Illustrative plain-ASCII example — use only when a material feedback path applies:**

```text
[Skill A result]
       |
       | optional, user-chosen handoff
       v
[Skill B result]
       |
       v
{Material change needed?}
  | No  --> [Continue selected path]
  |
  + Yes --> [Owner reviews proposal]
                  |
                  v
           {Revision approved?}
             | No  --> [Defer / continue]
             |
             + Yes --> [Update owned artifact]
                            |
                            +--> [Revisit affected step
                                  only if necessary]
```

This is **ASCII text**, meant to remain readable directly in chat without rendering. It is **not a mandatory stage or loop**. If no material feedback path is supported, use a shorter one-way ASCII flow if useful, or simply describe the interaction in prose. Do not imply that a Markdown skill file executes dispatch, that an upstream revision was approved, or that an observed run occurred.

**Conditional, team-ready rationale (include only when the inspected interaction supports it):** "These skills can be used independently, with explicit handoffs when chosen. That lets us return a material finding to the responsible owner and revisit only affected work, without forcing one rigid sequence. Contracts and approvals still govern every connection." Adapt the statement to actual capabilities; never present it as a generic guarantee about all skills.

## 4. Proposed Integration Contract Cards

Write **one vertical card per material connection**. Don't create one card per category, and don't fill irrelevant fields.

**IC-01 — [Source skill] → [Target skill] (PROPOSED / CONDITIONAL — NEEDS HUMAN / APPROVED — DESIGN ONLY)**

- **Purpose:** [Why this specific handoff helps.]
- **Sources / Stage 2 link:** [Direct source links, revision and real `F-xx (Cx)` if available; distinguish DOCUMENTED from INFERRED.]
- **Producer / consumer / owner:** [Who supplies, who reviews, who authorizes; distinguish producer's domain ownership from consumer's.]
- **Trigger and standalone path:** [When optional/required handoff occurs; how each skill can still run independently or what truly required prerequisite exists; include any **material pattern-specific routing/branch condition** from Section 3 without re-explaining the pattern.]
- **Inputs:** [Only genuinely required fields for this handoff vs optional context; source/revision, provenance and unresolved questions when applicable.]
- **Outputs / postconditions:** [Minimum usable result and what successful completion promises.]
- **Preconditions / invariants:** [What must be true before a handoff; what must remain unchanged, e.g. source ID, unresolved decisions, approval status.]
- **Failure and feedback:** [Missing/conflicting inputs → safe continuation / BLOCKED / NEEDS HUMAN; owner to whom changes are proposed; when work can resume.]
- **Trust / approval / permitted effects:** [Who can propose, edit, publish or approve; documented instructions vs runtime enforcement assumptions.]
- **Observability / compatibility (if relevant):** [Minimum evidence/IDs, optional format revisions and known host assumptions; don't promise unverified functionality.]
- **Why / trade-off:** [Concrete downstream failure prevented, alternative and cost of extra requirements; link to a material Section 3 pattern only when it affects the guarantee.]
- **Dependencies and status:** [Related `D-xx`; `PROPOSED` or `CONDITIONAL — NEEDS HUMAN` until explicit sign-off; never claim implemented.]

For one skill, name `IC-01 — [Skill] standalone entry/exit`; don't invent a producer. When a contract is not relevant, omit it rather than inserting empty fields.

## 5. Cross-Cutting Guarantees & Trade-offs

Capture only material constraints **not already clear** in contract cards. When Section 3 identifies a relevant interaction pattern, Section 5 discusses its **cross-connection consequences** (such as shared ownership, coupling, failures, authorization or context provenance) **only if** they are material and not already addressed by the specific IC-xx cards. Do not repeat a pattern glossary, recreate its diagram or add an extra framework just because a pattern has a name.

- **Authorization and trust:** [Source/evidence; expected human approval; host/tool enforcement NOT VERIFIED when not inspected.]
- **Reliability and feedback:** [A meaningful failure/partial-result rule and which consumer is affected.]
- **Observability and compatibility:** [Only necessary source IDs, expected revisions and host assumptions.]
- **Trade-off / simplest alternative:** [Manual optional handoff vs additional coordination/required fields; why chosen.]
- **Out of scope:** [Unnecessary schemas, speculative retries, premature orchestration, eval execution.]

If no cross-cutting issue is material, say `No additional cross-cutting rules beyond IC-xx` instead of repeating all six categories.

**Contract Quality Review Coverage (optional; only when requested)**

This is a **design-quality comparison of the proposed IC-xx contracts**, not an assessment of the underlying skills and not evidence that any contract is approved or executed. The full six-question template below uses [contract-quality-review-questions.md](contract-quality-review-questions.md). Render it **after the concise cross-cutting considerations in Section 5**, before the numbered Section 6 decision ledger.

| Contract-quality question | [IC-01 — Contract / connection] | [IC-02 — Contract / connection] |
| --- | --- | --- |
| **CQ-01 — Interface Clarity** — Are required and optional information clearly distinguished? | [Status — short reason/source; D-xx and F-xx if real] | [Status — short reason/source; D-xx and F-xx if real] |
| **CQ-02 — Behavioral Guarantees** — Are preconditions, postconditions, and invariants clear and necessary? | [Status — short reason/source; D-xx and F-xx if real] | [Status — short reason/source; D-xx and F-xx if real] |
| **CQ-03 — Ownership & Authority** — Are decision owners, permissions, and human approval boundaries explicit? | [Status — short reason/source; D-xx and F-xx if real] | [Status — short reason/source; D-xx and F-xx if real] |
| **CQ-04 — Reliability & Feedback** — Are important failure conditions and feedback responsibilities defined? | [Status — short reason/source; D-xx and F-xx if real] | [Status — short reason/source; D-xx and F-xx if real] |
| **CQ-05 — Evidence & Traceability** — Can contract decisions be traced to source evidence and Stage 2 findings? | [Status — short reason/source; D-xx and F-xx if real] | [Status — short reason/source; D-xx and F-xx if real] |
| **CQ-06 — Compatibility & Flexibility** — Does the contract preserve standalone skill behavior without unnecessary coupling? | [Status — short reason/source; D-xx and F-xx if real] | [Status — short reason/source; D-xx and F-xx if real] |

**Populate with:** a concise `CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE` design status; source evidence or limitation; and real **IC-xx**, **D-xx** or supplied Stage 2 **F-xx (Cx)** pointers when material. Keep full rationale in the existing IC/D cards; don't duplicate detailed findings or generate a new ID family. `CLEAR` does **not** imply APPROVED — DESIGN ONLY, implemented, enforced, or tested. An unverified runtime is not automatically a design defect.

**Mode and layout:** The table appears only with `quality_review: on`, `contract_quality_review: on`, or a `quality_questions: CQ-…` subset. Full mode uses all six questions in canonical order; subset mode only selected rows. For **one contract**, show just one IC column; for **three or more**, group up to two IC columns and repeat selected CQ rows. Don't create placeholder contracts or mandatory requirements to populate the table. Keep each row one Markdown line, no HTML breaks or multiline field lists in cells. If no meaningful IC exists, explain and omit the empty table. Seven numbered report headings remain unchanged.

**Review Lens Coverage (optional; only when lenses requested)**

This is a comparison of **proposed IC-xx contracts**, using full diagnostic questions and relevant contract-dimension mappings from [review-lenses.md](review-lenses.md). The five rows below are a **format example**, not actual findings or a requirement to run every lens. Include only explicitly named lenses or lenses selected as relevant from inspected evidence.

| Review lens & diagnostic questions | [IC-01 — Contract / connection] | [IC-02 — Contract / connection] |
| --- | --- | --- |
| **Context Engineering** — Does the handoff identify only the context the receiver actually needs, with source/revision and unresolved questions? Can the consumer separate upstream facts, assumptions and approvals? Does it treat untrusted source text as data, not authority? *Dimensions: Interface; Observability and evidence; Security, authority and trust.* | [Brief status, direct target source and real IC/D/F link] | [Brief status, direct target source and real IC/D/F link] |
| **Security & Trust** — Who requests and authorizes the next action? Can the receiving agent gain greater authority than the user or producer granted? Which permissions must be enforced by host/tool/server controls instead of prompt text, and what happens when trusted definitions change? *Dimensions: Security, authority and trust; Behavior; Compatibility and evolution.* | [Brief status, direct target source and real IC/D/F link] | [Brief status, direct target source and real IC/D/F link] |
| **Reliability & Workflow** — Does the contract distinguish completed, needs-input, blocked, pending and failed states where necessary? Who owns each return path and next decision? Is optional coordinator routing separated from actual runtime dispatch, durable state and retries? *Dimensions: Behavior; Failure, feedback and fault isolation; Interface.* | [Brief status, direct target source and real IC/D/F link] | [Brief status, direct target source and real IC/D/F link] |
| **Evaluation & Observability** — Can a reviewer trace each material IC-xx term to the inspected source and the relevant D-xx decision? Which minimal identifiers, statuses and error reasons must survive a handoff? Does the contract distinguish documented intent from observed execution without demanding unnecessary telemetry? *Dimensions: Observability and evidence; Interface; Security, authority and trust.* | [Brief status, direct target source and real IC/D/F link] | [Brief status, direct target source and real IC/D/F link] |
| **Lifecycle & Portability** — Can the consumer tell which source and contract revision its inputs reflect? Which changes require a new review or approval? Can each skill still run independently if a connected skill, tool definition or host capability changes? *Dimensions: Compatibility and evolution; Interface; Security, authority and trust.* | [Brief status, direct target source and real IC/D/F link] | [Brief status, direct target source and real IC/D/F link] |

**Output rules:** Place this after optional CQ coverage if CQ was requested, otherwise after ordinary Section 5 notes. Use short `CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE` statuses, real inspected target source links and existing IC-xx/D-xx/Stage 2 F-xx (Cx) pointers only where material. One IC uses one column; 3+ ICs use groups of at most two columns, repeating selected lens rows. Use mapped contract dimensions in lens-only mode, **not CQ IDs suggesting CQ questions ran**. No new numbered heading, new findings scheme or repeated detailed proposals.

**Conference Sources & Further Reading (optional; include when lenses run)**

Below is a **format example with one primary conference presentation per lens**. In a real report, include the relevant sources for only the selected lenses from [review-lenses.md](review-lenses.md), with their actual topic, title, speaker and direct PDF link plus video only where a saved title/speaker match exists. Source readings **explain engineering concepts**, whereas inspected target source files support actual contract diagnoses. Neither a PDF nor a video is evidence that IC-xx was enforced or tested.

| Lens / Topic | Session title / Speaker | Slides | Video |
| --- | --- | --- | --- |
| Context Engineering — Interface boundaries | **Don't Share the Database: Interface Contracts Between Isolated AI Agents** — Martin Bliss | [PDF](https://drive.google.com/file/d/1E4J2rfYLoN-H9wnK_K3f6bGshiwmDUmo/view) | — |
| Security & Trust — Delegation | **When Agents Spawn Agents: Securing Recursive Delegation in Multi-Agent Systems** — Anishma Mavuram | [PDF](https://drive.google.com/file/d/1_jXpA_vFEBAAPYeklZmliAs9jNWZTyWx/view) | [YouTube](https://www.youtube.com/watch?v=glxs_6J-7sQ) |
| Reliability & Workflow — Messaging | **Agentic Messaging Primitives in MCP** — Caitie McCaffrey | [PDF](https://drive.google.com/file/d/1OwyNvZGpIFDnc9KchDq5uER9DpgzLG4g/view) | [YouTube](https://www.youtube.com/watch?v=iNV5-YkPHW4&t=21711s) |
| Evaluation & Observability — Evidence | **Prove What Your Agent Did: Tamper-Evident Audit Trails for MCP Tool Calls** — Vikas Luthra | [PDF](https://drive.google.com/file/d/1ZiZn1h8IuQDEjBVibU8gzortXJABLidk/view) | — |
| Lifecycle & Portability — Versioning | **Stop Writing Agents, Declare Them: Declarative Agent Architecture in Production** — Chris Knuteson | [PDF](https://drive.google.com/file/d/1f9v2ZupSLbcik_AkKJgtfVu9mmVZ5jjI/view) | — |

Keep both lens subsections within Section 5, ahead of the Section 6 decision ledger; no HTML breaks or fabricated URLs.

**Industry Framework Review Coverage (optional; only when industry review is requested)**

This is an **industry-informed design review of the proposed IC-xx contract cards**, not an audit of current skill responsibilities or a compliance check. The five rows below are a **template** showing the exact **adapted Stage 3 questions**, not quotations of normative framework requirements. In actual reports include only frameworks selected by `industry_frameworks: [...]`, source-justified `industry_framework_review: relevant`, or all five proportionately for `industry_framework_review: on`.

| Framework & contract-design questions | [IC-01 — Contract / connection] | [IC-02 — Contract / connection] |
| --- | --- | --- |
| **ISO/IEC 25010:2023 — Software Product Quality** — Are the specific quality attributes relevant to this connection translated into clear, proportional IC-xx guarantees, rather than vague promises? Is the consumer told which guarantees it can rely on, with quality trade-offs and exception conditions disclosed where material? Does the agreement preserve the standalone functionality and maintainability of both skills? *Dimensions: Behavior; Compatibility and evolution; Interface; Failure, feedback and fault isolation.* | [CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE; actual IC/D/source] | [CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE; actual IC/D/source] |
| **AWS Well-Architected Agentic AI Lens** — Do IC-xx cards identify producers, consumers and human owners without creating redundant coordination or coupling? Are consequential permissions, human gates, and failure/feedback outcomes clear for each material connection? Is a proposed coordinator justified against a simpler manual optional handoff? Are observability, cost and latency expectations proportional to the selected workflow rather than speculatively required? *Dimensions: Interface; Behavior; Security, authority and trust; Failure, feedback and fault isolation; Observability and evidence.* | [CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE; actual IC/D/source] | [CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE; actual IC/D/source] |
| **NIST AI Risk Management Framework (AI RMF 1.0)** — Does the proposed integration identify who governs and approves consequential decisions, including where human intervention is required? Are material trust/authority assumptions and foreseeable harms explicit enough for the reviewer to choose or defer the agreement? Do source provenance, unresolved concerns and monitoring/validation ownership remain traceable without claiming that a risk-control mechanism already exists? *Dimensions: Security, authority and trust; Observability and evidence; Behavior; Failure, feedback and fault isolation.* | [CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE; actual IC/D/source] | [CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE; actual IC/D/source] |
| **CMU SEI Architecture Tradeoff Analysis Method (ATAM)** — Which user or stakeholder goal justifies the proposed handoff contract? What realistic quality scenario would expose the design's most important risk or ambiguity? Have the smallest viable option, alternative and trade-off been explained in the linked IC-xx/D-xx cards without pretending the alternative was implemented or tested? *Dimensions: Behavior; Failure, feedback and fault isolation; Compatibility and evolution; Security, authority and trust.* | [CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE; actual IC/D/source] | [CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE; actual IC/D/source] |
| **OWASP Top 10 for Agentic Applications (2026)** — Does the contract preserve the distinction between untrusted content and authorized instructions, with an identified human/tool decision boundary? Could the proposed handoff allow an agent or coordinator to misuse tools, broaden delegated authority, poison another skill's context, or create cascading failure? Are relevant mitigations, stop conditions and unresolved host-enforcement assumptions represented only where they are material? *Dimensions: Security, authority and trust; Interface; Failure, feedback and fault isolation; Compatibility and evolution.* | [CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE; actual IC/D/source] | [CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE; actual IC/D/source] |

**Assessment and comparison rules:** Each cell gives concise `CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE` with an actual inspected target/design source link or explicit evidence limit and existing IC-xx, D-xx and supplied Stage 2 F-xx (Cx) pointers where material. A `CLEAR` proposed contract is not approved, implemented, enforced or tested. The substantive clarification goes into the original IC-xx card, and any approval/ownership issue into the Section 6 D-xx ledger. Never generate separate framework findings or new contracts just to fill rows. For one IC use one contract column; for 3+ ICs use tables of at most two contract columns, repeating selected framework rows. Industry-only mode never silently triggers CQ or conference-lens review.

**Official Industry Framework Sources & Further Reading (optional; required when industry review is requested)**

Immediately after industry coverage, still inside **Section 5**, include one or two **direct publisher URLs per selected framework**, including its type, topic and edition. The five entries below are a **full-mode formatting example**, not a list to reproduce unconditionally for a `relevant` or named subset run. Source links in [industry-framework-review-lenses.md](industry-framework-review-lenses.md) are the reference.

| Framework / type | Topic or official section | Publisher & version | Official URL |
| --- | --- | --- | --- |
| **ISO/IEC 25010:2023 — International Standard** | Product-quality model | ISO/IEC, 2023 | [Official publisher link](https://www.iso.org/standard/78176.html) |
| **AWS Agentic AI Lens — Vendor architecture guidance** | Agent handoffs, security, reliability, cost | AWS, June 2026 | [Official publisher link](https://docs.aws.amazon.com/wellarchitected/latest/agentic-ai-lens/agentic-ai-lens.html) |
| **NIST AI RMF 1.0 — Voluntary risk framework** | AI risk ownership, governance and oversight | NIST, 2023; revision in progress | [Official publisher link](https://airc.nist.gov/airmf-resources/airmf/) |
| **CMU SEI ATAM — Architecture-evaluation method** | Quality scenarios and design trade-offs | CMU SEI | [Official publisher link](https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/) |
| **OWASP Agentic Top 10 (2026) — Community security guidance** | Tool, identity, context and inter-agent risks | OWASP GenAI Security Project, 2026 | [Official publisher link](https://genai.owasp.org/top-10-for-agentic-applications-2026/) |

**Evidence and status boundary:** Framework publications justify the adapted design questions; inspected source files, actual supplied Stage 2 findings and proposed IC/D wording justify contract-specific conclusions. A framework reference does not establish compliance, a completed formal ATAM, AWS deployment or Well-Architected review, an OWASP security test or a Stage 5 evaluation. When multiple optional modes run, report Section 5 order is: ordinary cross-cutting notes → CQ coverage → conference lens coverage and sources → industry framework coverage and official sources → Section 6 human decision ledger. Only include enabled optional tables; keep all seven numbered report sections.

## 6. Human Decision Ledger & Open Questions

Present **all materially distinct choices before inviting approval**, one vertical block per decision:

**D-01 — [Specific ownership, handoff or permission choice]**

- **Links:** [`IC-01`; source and `F-xx (Cx)` if present.]
- **Recommended decision (PROPOSED):** [Exact wording.]
- **Why / alternative / trade-off:** [What this prevents; reasonable smaller or different choice.]
- **Human reviewer:** [Known owner or UNKNOWN — needs identification.]
- **Status:** PROPOSED / CONDITIONAL — NEEDS HUMAN / APPROVED — DESIGN ONLY / REVISE REQUESTED / REJECTED / DEFERRED.
- **Question to resolve:** [One concrete open choice; don't bury it in generic wording.]

**Decision rule:** Only record an explicit human-approved *design version* as APPROVED — DESIGN ONLY. A vague reaction does not approve unseen choices. Approval does not authorize Stage 4 edits, runtime permissions or test execution. If D-01 changes, dependent IC-01 remains conditional until the amended text is reviewed.

## 7. Stage 4 Implementation Handoff & Stage 5 Candidates

- **Stage 4 — proposed changes:** [Affected existing `SKILL.md` and/or confirmed local reference path; propose only the smallest change. Never claim a new file exists or create/modify target files in this skill.]
- **Prerequisites:** [`D-xx / IC-xx` that must receive specific human approval first.]
- **Preserve standalone behavior:** [How neither skill depends on automatic invocation of another.]
- **Stage 5 candidates — PROPOSED, NOT EXECUTED:** [`V-01`: Given a representative input, when an **approved** integration runs in an **authorized** host, then an observable output/approval/failure rule must hold; name needed trace/artifact evidence only if material.]
- **Current status:** [DESIGN PROPOSAL ONLY — NOT IMPLEMENTED, NOT RUN, NOT VERIFIED.]

**Final human gate:** Present the available choices: `Approve D-01 and IC-01`; `Revise D-02: ...`; `Defer IC-02`. Ask for decisions only **after** presenting the proposal. Do not silently move to Stage 4.
