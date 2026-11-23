# Skill Responsibility & Overlap Audit — Report Template

Use as an **output guide, not a source of facts**. Replace all bracketed placeholders with actual findings and direct source links. Keep the seven section headings stable.

## 1. Executive Summary

- **Scope:** [Skills, revisions, known workflow.]
- **Available evidence:** [Files inspected; inaccessible files.]
- **Main observations:** [Two or three grounded findings.]
- **Unverified:** [Important evidence limits.]

## 2. Individual Skill Assessments

**Use the same side-by-side orientation in BOTH tables.** The first column is always `Consideration`; the remaining columns are the **same skill names, in the same order**. Primary C1–C3 and Supporting C4–C6 are **rows**, never headings or separate per-skill tables. This exact structure is required for two- or three-skill audits.

**Primary considerations — analyze in detail**

| Consideration | [Skill A] | [Skill B] |
| --- | --- | --- |
| 1. Inputs (C1) | **F-01 (C1)** **Finding:** Discovery reads as mandatory. **Evidence:** DOCUMENTED [source]. **Assessment:** CLARIFY. **Why:** Could delay a provisional draft. **Recommendation:** Clarify discovery as optional when justified. | Accepts a ticket or idea; no upstream brief is required. [Source] |
| 2. Responsibilities (C2) | **F-02 (C2)** **Finding:** Owns initial product requirements. **Evidence:** DOCUMENTED [source]. **Assessment:** KEEP. **Why:** The PRD remains useful on its own. **Recommendation:** Preserve ownership. | Reviews requirements against evidence and proposes clarifications. [Source] |
| 3. Outputs (C3) | **F-03 (C3)** **Finding:** A readiness phrase may be unclear. **Evidence:** DOCUMENTED [source]; risk INFERRED. **Assessment:** CLARIFY. **Why:** Readers may confuse document completeness with implementation approval. **Recommendation:** Clarify what readiness means. | Produces a review with unresolved items. [Source] |
| ↳ F-03 wording (C3) | **Current wording:** "[Exact sourced phrase]." **Concern:** [Specific risk of misinterpretation.] **Recommended wording — PROPOSED:** "[Supported clarification]." | — |

**Supporting considerations — identify issues; defer detailed design**

| Consideration | [Skill A] | [Skill B] |
| --- | --- | --- |
| 4. Handoffs (C4) | Optional PRD context may be passed to refinement; no automatic invocation. [Source] | Consumes an existing PRD optionally; the standalone path remains available. [Source] |
| 5. Boundaries (C5) | Drafts within authorization; cannot publish or approve new scope without permission. [Source] | Review-only; proposes changes rather than editing the PRD. [Source] |
| 6. Feedback (C6) | Human owner reviews proposed updates. [Source] | Returns questions and proposed changes to the owner. [Source] |

*Everything above is illustrative, not an audit of real skills. In actual output, replace the placeholders with inspected evidence. Include the `↳ F-xx wording` row **only when needed**, immediately under that consideration in the **same table**.*

**Mandatory layout checks**

- **Two tables, not one table per consideration:** exactly one Primary comparison table and one Supporting comparison table for two or three skills; headers match in column names and order.
- The **only first-column main row labels** are C1–C3 in Primary and C4–C6 in Supporting; optional F-xx wording detail rows immediately follow the finding they clarify.
- **Never transpose Primary** into a table with considerations as column headings or skill names as row labels. A header such as `| Consideration | 2. Responsibilities (C2) |` is an incorrect layout.
- Use one physical Markdown line per table row. Within cells use short inline labeled sentences, not HTML, bullets, or embedded newlines. Escape literal pipe characters inside quotes.
- Material items use **F-xx** and brief Finding / Evidence / Assessment / Why / Recommendation inline. KEEP may be appropriate; do not force findings in every cell. If exact wording is lengthy, use one immediately adjacent detail row in the **same table**, not a third comparison table or a detached findings section.
- Preserve source provenance: **DOCUMENTED** describes inspected instructions; **INFERRED** labels plausible effects; **UNVERIFIED** means evidence is missing; **PROPOSED** describes a recommendation. Do not invent quotes or execution results.
- Related considerations may say `Related: F-xx (Cx)` without duplicating the finding. Section 5 consolidates actionable F-xx work rather than reproducing paragraphs.
- For four or more skills, use repeated two- or three-skill groups **with the same fixed orientation** and an overall synthesis covering all selected skills. If a host cannot render tables, use consideration-first blocks as a fallback instead of emitting malformed Markdown.
- Proposed C4–C6 integration details remain optional and clearly labeled **PLANNED / PROPOSED — NOT IMPLEMENTED**; source details belong only in the relevant skill's cell. Stage 3 still defines contracts.

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

**Summarize, don't repeat:** Consolidate material CLARIFY/REVISE/ADD and VERIFY work by the **F-xx identifiers in C1–C6 table cells**, with independent High/Medium/Low priorities. For wording concerns, point to the replacement in that cell rather than repeating it. KEEP generally requires no implementation item. If no change is justified, say so.

- **Priority:** [High / Medium / Low]
- **Finding:** [F-xx, C1–C6, affected skill and assessment; refer to that table cell rather than repeating its five fields or recommended wording.]
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

- [Unresolved handoff, guarantees, trust, versioning, failure handling, observability, or feedback questions.]
- [If a separate coordinator is proposed: future routing conditions, context-passing expectations, approval gates, runtime compatibility and evaluation — not contracts written here.]
- **Not designed in this audit.** No contract or architecture decision is approved.

**Evidence note:** A target file's instructions are `DOCUMENTED`, not `OBSERVED` runtime behavior. Missing source access means `NOT ASSESSED`, not a failing skill.
