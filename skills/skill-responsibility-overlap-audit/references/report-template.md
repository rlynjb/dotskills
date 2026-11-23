# Skill Responsibility & Overlap Audit — Report Template

Use as an **output guide, not a source of facts**. Replace all bracketed placeholders with actual findings and direct source links. Keep the seven section headings stable.

## 1. Executive Summary

- **Scope:** [Skills, revisions, known workflow.]
- **Available evidence:** [Files inspected; inaccessible files.]
- **Main observations:** [Two or three grounded findings.]
- **Unverified:** [Important evidence limits.]

## 2. Individual Skill Assessments

For **two or three skills**, use side-by-side tables. Keep long citations and explanation below the table.

**Primary considerations — detailed**

| Consideration | [Skill A] | [Skill B] |
| --- | --- | --- |
| 1. Inputs | [Required/optional, sources] | [Required/optional, sources] |
| 2. Responsibilities | [Owned activities/decisions] | [Owned activities/decisions] |
| 3. Outputs | [Artifacts/decisions] | [Artifacts/decisions] |

**Supporting considerations — issues only**

| Consideration | [Skill A] | [Skill B] |
| --- | --- | --- |
| 4. Handoffs | [Current handoff and issue, if any] | [Current handoff and issue, if any] |
| 5. Boundaries | [Current ownership/authority and issue] | [Current ownership/authority and issue] |
| 6. Feedback | [Current revision path and issue] | [Current revision path and issue] |

**Meaningful per-skill assessment notes (only for consequential findings):**

**[Skill] — [Consideration number: finding title]**
- *Finding:* [What the sources describe or leave unclear.]
- *Evidence:* [DOCUMENTED / OBSERVED / INFERRED / UNVERIFIED / NOT ASSESSED, plus direct links or explicit evidence gap.]
- *Assessment:* [KEEP / CLARIFY / REVISE / ADD / VERIFY.]
- *Why:* [Plain-English reason or consequence.]
- *Recommendation:* [Smallest next step, including keep as-is or targeted verification, with human review for changes.]

Repeat only when meaningful; don't force a five-field record for every cell. **KEEP** can be the correct outcome. If a documented output and an inferred handoff differ in certainty, state both evidence statuses. No five extra table columns.

**Optional instruction wording review — only if the finding concerns material wording ambiguity:**

- *Current wording:* ["Exact short quote" from the inspected source, with direct file and line/section evidence.]
- *Concern:* [What a reader or agent could incorrectly infer; why it matters. Label potential behavior **INFERRED** unless genuinely observed.]
- *Recommended wording — PROPOSED:* [Minimal, ready-to-copy replacement preserving the verified intent and authority boundaries; or **VERIFY** the intended rule first if ambiguous.]

Keep this **within** the relevant per-skill finding, not in another consideration or table. Do not expand healthy KEEP findings or style-only preferences into rewrites. A quote is DOCUMENTED; an untested consequence is INFERRED; the rewrite is PROPOSED and requires human review. Never invent source text, remove required safety prerequisites, or assume unclear approval status is resolved.

**Proposed optional connection documentation — per affected skill (only if justified by a row 4–6 issue):**

**Status for this section: PLANNED / PROPOSED — NOT IMPLEMENTED, NOT CONTRACTED, NOT VERIFIED.** This is a Stage 2 investigation record to guide Stage 3 design, *not* a claim that the skills already exchange information or call one another.

**[Skill A] — PROPOSED wording, NOT YET IMPLEMENTED**
- *Standalone use:* [Existing starting inputs, complete workflow and own outputs; if unverified or currently dependent, say so.]
- *Optional handoff:* [When another skill's existing output is available, it may be supplied as **optional context**. The skill never requires or auto-runs its partner.]
- *Responsibilities:* [What Skill A owns; what remains with Skill B.]
- *Boundaries:* [No automatic invocation, unauthorized edit/publish/approval, or change to another skill's decisions.]
- *Feedback:* [Report proposed changes and open questions to the correct human owner; no silent upstream edits.]
- *Documentation placement:* [PROPOSED `Optional Handoffs` note in this skill's `SKILL.md`. If substantial details justify it, name a proposed skill-local `references/<source>-to-<destination>-handoff.md`; if absent, label **PLANNED — NOT CREATED**. Otherwise say **SKILL.md only**.]
- *Stage 3 follow-up:* [The still-undecided handoff fields, compatibility/approval requirements, feedback routing, and verification questions; do not draft contracts here.]
- *Planning status:* [PLANNED / PROPOSED — NOT IMPLEMENTED or explicitly evidenced current state.]
- *Evidence / open design question:* [Direct links; note gaps and who needs to confirm.]

**[Skill B] — PROPOSED wording, NOT YET IMPLEMENTED**
- *Standalone use:* [How Skill B starts, finishes and produces useful outputs without Skill A.]
- *Optional handoff:* [If Skill A's output exists, Skill B may consume it as context, not as a prerequisite.]
- *Responsibilities:* [What Skill B owns and must not overwrite.]
- *Boundaries:* [No required/autonomous invocation or unauthorized side effects.]
- *Feedback:* [What Skill B returns as suggestions/questions for Skill A's owner to review.]
- *Documentation placement:* [PROPOSED `Optional Handoffs` note in this skill's `SKILL.md`. Use a directionally named local reference **only for substantial guidance**; indicate whether it exists or is **PLANNED — NOT CREATED**. Reverse feedback uses the opposite direction.]
- *Stage 3 follow-up:* [Formal details and human decisions still needed before integration.]
- *Planning status:* [PLANNED / PROPOSED — NOT IMPLEMENTED or explicitly evidenced current state.]
- *Evidence / open design question:* [Direct links; note gaps and who needs to confirm.]

**Illustrative workflow choices — not verified by this template:**
- Run **Skill A alone**.
- Run **Skill B alone**.
- Run **Skill A**, optionally supply its result to **Skill B**, then let the responsible human owner review any suggested updates.

If either skill currently **requires** the other's output, do not label standalone use as supported. Record the dependency as-is and propose any optionalization **conditionally**. If there is no relevant issue, omit these recommendation blocks; do not fabricate a connection. Documented boundaries do not prove runtime restrictions.

**File placement decision:** In this Stage 2 report, recommend a brief **planned** `Optional Handoffs` section inside each affected `SKILL.md`, so a future reviewer understands the direction without assuming the connection already works. Use a **proposed** skill-local reference only if field mappings, examples, conflict-resolution guidance or conditional cases make the explanation substantial. Name single-direction files `<source>-to-<destination>-handoff.md` (plural `handoffs` only for several transitions); reuse existing suitable files when possible. The owning skill's `SKILL.md` can link to its **own** reference and say when to read it. Never require a shared file or partner skill to understand or run standalone. All paths and edits in this template are **PROPOSED**, not completed.

**Evidence and interpretation:** Use the per-skill five-field notes above for material findings; keep any other source references concise. Do not repeat the same evidence or rationale in a second list.

For **one skill**, use the six considerations as vertical labeled sections instead; state that cross-skill comparisons are not applicable.

For **four or more skills**, repeat concise side-by-side groups of two or three, then summarize *every skill* in an overall ownership synthesis. Only group skills based on relevant comparisons; do not drop other material relationships.

## 3. Cross-Skill Responsibility & Overlap Findings

For each real overlap, align the involved skills, then explain it below.

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

**Summarize, don't repeat:** Consolidate material CLARIFY/REVISE/ADD and VERIFY work from earlier findings, with source links and independently assigned High/Medium/Low priorities. For wording concerns, point to the proposed replacement in Section 2 rather than repeating the before/after text. KEEP generally requires no implementation item. If no change is justified, say so.

- **Priority:** [High / Medium / Low]
- **Finding:** [Source-linked skill/consideration and assessment label; refer back to section 2 instead of repeating the full rationale.]
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
