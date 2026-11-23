# Skill Responsibility & Overlap Audit — Report Template

Use as an **output guide, not a source of facts**. Replace all bracketed placeholders with actual findings and direct source links. Keep the seven section headings stable.

## 1. Executive Summary

- **Scope:** [Skills, revisions, known workflow.]
- **Available evidence:** [Files inspected; inaccessible files.]
- **Main observations:** [Two or three grounded findings.]
- **Unverified:** [Important evidence limits.]

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
| 4. Handoffs (C4) | Optional outbound context. [source] | Optional inbound context. [source] |
| 5. Boundaries (C5) | Drafts within authorized scope. [source] | Review-only, no silent upstream edits. [source] |
| 6. Feedback (C6) | Human owner reviews accepted proposals. [source] | Returns proposed changes and questions. [source] |

For material C4–C6 findings, show the same **F-xx (Cx) vertical notes immediately here**, before Section 3. Do not create separate tables or move the findings to the end of the report.

**Quality review coverage (optional; only when requested):** After the Supporting table and any material Supporting F-xx notes, list the selected Q-01–Q-10 status for each inspected skill, citing evidence and referring to F-xx (Cx) when a material issue has already been explained. Use `PRESENT / PARTIAL / MISSING / NOT VERIFIED / NOT APPLICABLE`; do not add another comparison table or required report heading. A lens-only review does **not** require Q coverage. See [quality-review-questions.md](quality-review-questions.md) and [review-lenses.md](review-lenses.md).

**Layout contract:** For two or three skills, use exactly the two comparison tables above, in the same skill order. C1–C3 and C4–C6 are rows, never headings or separate per-consideration tables. Keep complete Finding/Evidence/Assessment/Why/Recommendation and Current wording/Concern/Recommended wording **outside** pipe-table cells, each on a new bullet line. Match F-xx IDs in table summaries to their vertical explanations. No HTML, huge inline cells, duplicated findings, or invented evidence. Stage 2 recommendations need human review; Stage 3 designs contracts.

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

- **Priority:** [High / Medium / Low]
- **Finding:** [F-xx, C1–C6, affected skill and assessment; refer to the vertical finding note rather than repeating its fields or recommended wording.]
- **Proposed change:** [Ownership/documentation proposal only; when appropriate, cite the per-skill proposed optional handoff, boundary, and feedback wording from section 2.]
- **Standalone integrity:** [Does each skill retain its own inputs, outputs and workflow? If not evidenced, what needs human confirmation?]
- **Documentation location:** [Per affected skill: proposed `Optional Handoffs` note in `SKILL.md`, plus a potential optional, directionally named local reference only if warranted; say whether that file actually exists.]
- **Planning status / Stage 3:** [PLANNED / PROPOSED — NOT IMPLEMENTED. Identify what Stage 3 must agree before any integration claim.]
- **Benefit / trade-off:** [Including cost of change.]
- **Human confirmation:** [Required? Who, if known?]

**Optional coordinator assessment — only for a material combined-workflow coordination concern**

- **Decision:** [NOT NEEDED / OPTIONAL COORDINATOR RECOMMENDED / DEFER — UNVERIFIED]
- **Evidence and problem:** [Link to observed/documented routing, sequencing, context, human-review or feedback issue; distinguish proposed goals from observed runtime failures.]
- **Simpler alternative:** [Existing optional handoffs and copyable next-action prompts; why sufficient or insufficient.]
- **Minimal coordinator role (only if recommended):** [Separately invoked workflow entry point; selects starting stage, sequences optional steps, carries references/IDs/revisions/open questions, routes proposed changes for human review, reports completion.]
- **Non-ownership:** [Underlying skills retain their own inputs, outputs, domain decisions and standalone invocation. Coordinator does not silently rewrite, approve, or run them.]
- **Suggested pattern (only if recommended):** [Router + sequential workflow by default, or evidence-based alternative. Do not design a dispatch contract here.]
- **Trade-off and validation:** [Added complexity, potential misrouting, availability of host/manual invocations and unknown runtime enforcement; actual multi-skill execution remains UNVERIFIED without traces.]
- **Human confirmation:** [Whether to investigate a separate optional `skills/<workflow-goal>-workflow/SKILL.md` in later stages, not permission to create it.]

If simple handoffs suffice, state **NOT NEEDED** with one reason; do not fill a long coordinator template. If facts are missing, **DEFER** and name the evidence needed. Do not create the coordinator skill in this audit.

## 6. Open Questions for Human Review

- [Question that would resolve a material ambiguity.]

## 7. Deferred Items for Integration-Contract Design

**Contract design questions — Stage 3 (when justified)**
- [Related F-xx/Cx; affected skill(s); unresolved handoff, guarantee, authorization, feedback, version or failure question; human decision needed. Do not draft the contract.]
- [For an optional coordinator proposal, note future routing, context preservation, approvals and host compatibility as open design questions.]

**Validation candidates — Stage 5 (PROPOSED, NOT EXECUTED; when justified)**
- [Related F-xx: Given a representative input, when an approved and authorized workflow runs, then a specific observable result should occur. Note the artifact/trace evidence needed and Stage 3 dependency.]
- [Do not invent test outcomes, enforceability, readiness or approvals; omit speculative scenarios with no relevant finding.]

**Not designed or executed in this audit.** No contract, architecture or evaluation result is approved.

**Evidence note:** A target file's instructions are `DOCUMENTED`, not `OBSERVED` runtime behavior. Missing source access means `NOT ASSESSED`, not a failing skill.
