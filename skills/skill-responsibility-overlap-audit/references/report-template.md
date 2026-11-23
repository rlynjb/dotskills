# Skill Responsibility & Overlap Audit — Report Template

Use as an **output guide, not a source of facts**. Replace all bracketed placeholders with actual findings and direct source links. Keep the seven section headings stable.

## 1. Executive Summary

- **Scope:** [Skills, revisions, known workflow.]
- **Available evidence:** [Files inspected; inaccessible files.]
- **Main observations:** [Two or three grounded findings.]
- **Unverified:** [Important evidence limits.]

## 2. Individual Skill Assessments

Keep the **original side-by-side comparison**. Use standard Markdown pipe tables with a short, **single physical line per row**—even when the text wraps naturally in a terminal. No HTML line-break tags, embedded newlines, or bullet lists inside cells. Every material finding belongs beside its C1–C6 consideration; do not create separate Finding A/B/C sections.

**Primary considerations — analyze in detail**

| Consideration | [Skill A] | [Skill B] |
| --- | --- | --- |
| 1. Inputs (C1) | **F-01 (C1)** **Finding:** Discovery reads as mandatory. **Evidence:** DOCUMENTED [source]. **Assessment:** CLARIFY. **Why:** Could delay a valid draft. **Recommendation:** Permit a provisional draft with gaps recorded. | Accepts a ticket or idea; no upstream PRD is required. [Source] |
| 2. Responsibilities (C2) | **F-02 (C2)** **Finding:** Owns initial product requirements. **Evidence:** DOCUMENTED [source]. **Assessment:** KEEP. **Why:** A complete PRD remains usable alone. **Recommendation:** Preserve ownership. | Reviews requirements against evidence and proposes clarifications. [Source] |
| 3. Outputs (C3) | Produces a PRD with open questions. [Source] | Produces a requirements review with unresolved items. [Source] |

**Supporting considerations — identify issues; defer detailed design**

| Consideration | [Skill A] | [Skill B] |
| --- | --- | --- |
| 4. Handoffs (C4) | Optional PRD context may be passed to refinement; no automatic invocation. [Source] | Consumes an existing PRD optionally; the standalone path remains available. [Source] |
| 5. Boundaries (C5) | Drafts within authorization; cannot publish or approve new scope without permission. [Source] | Review-only; proposes changes rather than editing the PRD. [Source] |
| 6. Feedback (C6) | Human owner reviews proposed updates. [Source] | Returns open questions and proposed changes to the owner. [Source] |

*All content above is a formatting illustration, not findings about real skills. Replace every placeholder with inspected evidence; omit F-xx when no significant finding exists.*

**Optional adjacent wording detail — use only when exact text would overload the cell**

| Consideration | [Skill A] | [Skill B] |
| --- | --- | --- |
| 1. Inputs (C1) | **F-01 (C1) — CLARIFY:** Discovery sounds mandatory; propose provisional drafting. [Source] | [Concise current behavior.] |
| ↳ F-01 wording (C1) | **Current wording:** "[Exact source quote]." **Concern:** [Specific inferred misinterpretation.] **Recommended wording — PROPOSED:** "[Evidence-supported replacement]." | — |

This is an **alternative illustration of the C1 row**, not a third required table or duplicated finding. In a real report, the adjacent detail row appears immediately under the corresponding C1–C6 row **in that same existing table**.

**Rules for all six considerations**

- For material items, use **F-01, F-02, ...** in the affected skill cell and brief **Finding / Evidence / Assessment / Why / Recommendation** sentences. KEEP is a valid outcome; do not force a change or a five-field record into every cell.
- Keep each cell short and source-backed. Long exact wording may go into **one neighboring row** linked by its F-xx and Cx. Do not add a separate findings section, extra table columns, or formatted HTML.
- Preserve source provenance: **DOCUMENTED** for source instructions, **INFERRED** for possible effects, **UNVERIFIED** when evidence is absent, and **PROPOSED** for recommended replacements. Do not invent quotes or observed execution.
- For related considerations, say `Related: F-xx (Cx)` rather than repeating the entire finding. In later sections, reference F-xx instead of restating five fields.
- Keep optional integration directions within C4–C6: handoff in C4, decision authority in C5, owner-reviewed feedback in C6. Mark potential integrations **PLANNED / PROPOSED — NOT IMPLEMENTED** and any absent suggested reference **PLANNED — NOT CREATED**. Neither skill must automatically invoke the other.
- For four or more skills, break into groups of two or three skill columns, with an overall synthesis covering every selected skill. If the terminal cannot render Markdown tables acceptably, use **consideration-first vertical blocks** with the same skill and C/F identifiers—not raw markup.

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
