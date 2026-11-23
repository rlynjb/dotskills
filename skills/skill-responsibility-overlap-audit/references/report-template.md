# Skill Responsibility & Overlap Audit — Report Template

Use as an **output guide, not a source of facts**. Replace all bracketed placeholders with actual findings and direct source links. Keep the seven section headings stable.

## 1. Executive Summary

- **Scope:** [Skills, revisions, known workflow.]
- **Available evidence:** [Files inspected; inaccessible files.]
- **Main observations:** [Two or three grounded findings.]
- **Unverified:** [Important evidence limits.]

## 2. Individual Skill Assessments

**Put material findings directly inside each skill's consideration cell.** Use one `Consideration` column with `C1`–`C6` labels, and one column per skill. No separate "Finding A/B/C" section. For each material finding, use report-local `F-01`, `F-02`, etc., and keep the five fields on separate visual lines **within the cell** using Markdown `<br>`. These are templates, not actual audit claims.

**Primary considerations — analyze in detail**

| Consideration | [Skill A] | [Skill B] |
| --- | --- | --- |
| 1. Inputs (C1) | [Short description of inputs; expand here if a material finding exists.] | [Short description of inputs; expand here if a material finding exists.] |
| 2. Responsibilities (C2) | **F-01 (C2) — [Short title]**<br>**Finding:** [Relevant ownership finding.]<br>**Evidence:** [DOCUMENTED — direct source]<br>**Assessment:** KEEP<br>**Why:** [Why preserving this ownership helps.]<br>**Recommendation:** Keep as-is. | [Use F-02 (C2) with the same fields when meaningful; otherwise summarize current responsibilities.] |
| 3. Outputs (C3) | [Concise supported output summary, or five fields for an important issue.] | [Concise supported output summary, or five fields for an important issue.] |

**Supporting considerations — identify issues; defer detailed design**

| Consideration | [Skill A] | [Skill B] |
| --- | --- | --- |
| 4. Handoffs (C4) | **F-03 (C4) — [Short title]**<br>**Finding:** [Handoff wording is ambiguous.]<br>**Evidence:** [DOCUMENTED phrase at source; risk INFERRED]<br>**Assessment:** CLARIFY<br>**Why:** [A consumer might assume an unintended prerequisite.]<br>**Recommendation:** [Propose a clearer optional handoff.]<br>**Current wording:** "[Exact sourced passage]"<br>**Concern:** [Specific misleading interpretation.]<br>**Recommended wording — PROPOSED:** "[Source-aligned revision.]" | [Concise handoff summary, or an F-xx with the same fields.] |
| 5. Boundaries (C5) | [Source-backed boundary summary, or F-xx finding. If related to F-03, say `Related: F-03 (C4)` without repeating that note.] | [Source-backed ownership and authority; expand only when material.] |
| 6. Feedback (C6) | [Source-backed feedback path; expand only when material.] | [Source-backed feedback path; expand only when material.] |

**Layout rules**

- Material findings stay **in the row where they were discovered** and in the affected **skill's column**. The examples F-01 and F-03 above illustrate format only; assign sequential IDs to real findings in consideration order, then skill order. Keep IDs stable when revising the same report if the underlying finding has not changed.
- Use **Finding / Evidence / Assessment / Why / Recommendation** for meaningful issues or useful KEEP judgments. Do not force five fields for every routine cell or assign fictitious findings simply to fill rows.
- Add **Current wording / Concern / Recommended wording — PROPOSED** only for materially ambiguous or conflicting instructions. Quote the real text and link the exact source; distinguish DOCUMENTED wording from INFERRED risk. If the intended rule is not established, recommend VERIFY rather than invent a rewrite.
- If one finding relates to another consideration, give it one **primary C-row** and use a brief **Related: F-xx (Cx)** link from other rows. Do not duplicate the full finding or invent a second ID solely for cross-reference.
- When C4–C6 reveal a real planned optional connection, place the relevant proposal **inside those cells**: C4 for optional context and proposed handoff reference location, C5 for standalone boundaries and no auto-invocation, and C6 for proposed feedback/owner review. Mark nonimplemented integration **PLANNED / PROPOSED — NOT IMPLEMENTED** and missing proposed files **PLANNED — NOT CREATED**. Do not automatically create a shared dependency or a coordinator.
- When multiple findings share one cell, label each with its own F-xx and put a short `<br><br>` separator between them. Keep each field to approximately one sentence where possible, but do not omit evidence or necessary quoted context just to shorten the cell. If a table becomes too wide or long, split the skill columns into smaller groups while retaining all findings.
- For one skill, use the same C1–C6 progression with its mini-records in each consideration's block. If a host cannot render `<br>` inside Markdown tables, use consideration-first blocks containing skill-labeled mini-records **at that consideration**, not detached findings after the audit.

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
