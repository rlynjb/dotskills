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

**Proposed optional connection documentation — per affected skill (only if justified by a row 4–6 issue):**

**[Skill A] — PROPOSED wording, NOT YET IMPLEMENTED**
- *Standalone use:* [Existing starting inputs, complete workflow and own outputs; if unverified or currently dependent, say so.]
- *Optional handoff:* [When another skill's existing output is available, it may be supplied as **optional context**. The skill never requires or auto-runs its partner.]
- *Responsibilities:* [What Skill A owns; what remains with Skill B.]
- *Boundaries:* [No automatic invocation, unauthorized edit/publish/approval, or change to another skill's decisions.]
- *Feedback:* [Report proposed changes and open questions to the correct human owner; no silent upstream edits.]
- *Documentation placement:* [PROPOSED: `SKILL.md` only, or `SKILL.md` plus own `references/<source>-to-<destination>-handoff.md` if transfer details are substantial. Explain why. Preserve essential rules in `SKILL.md`.]
- *Evidence / open design question:* [Direct links; note gaps and who needs to confirm.]

**[Skill B] — PROPOSED wording, NOT YET IMPLEMENTED**
- *Standalone use:* [How Skill B starts, finishes and produces useful outputs without Skill A.]
- *Optional handoff:* [If Skill A's output exists, Skill B may consume it as context, not as a prerequisite.]
- *Responsibilities:* [What Skill B owns and must not overwrite.]
- *Boundaries:* [No required/autonomous invocation or unauthorized side effects.]
- *Feedback:* [What Skill B returns as suggestions/questions for Skill A's owner to review.]
- *Documentation placement:* [PROPOSED: `SKILL.md` only, or `SKILL.md` plus its own optional `references/<source>-to-<destination>-handoff.md`, with a reason. A reverse-feedback file uses the opposite direction.]
- *Evidence / open design question:* [Direct links; note gaps and who needs to confirm.]

**Illustrative workflow choices — not verified by this template:**
- Run **Skill A alone**.
- Run **Skill B alone**.
- Run **Skill A**, optionally supply its result to **Skill B**, then let the responsible human owner review any suggested updates.

If either skill currently **requires** the other's output, do not label standalone use as supported. Record the dependency as-is and propose any optionalization **conditionally**. If there is no relevant issue, omit these recommendation blocks; do not fabricate a connection. Documented boundaries do not prove runtime restrictions.

**File placement decision:** Prefer a brief `Optional handoffs` section inside each affected `SKILL.md`. Use a skill-local reference only if field mappings, examples, conflict-resolution guidance or conditional cases make the explanation substantial. Name single-direction files `<source>-to-<destination>-handoff.md` (plural `handoffs` only for several transitions); reuse existing suitable files when possible. The owning skill's `SKILL.md` can link to its **own** reference and say when to read it. Never require a shared file or partner skill to understand or run standalone. All paths and edits in this template are **PROPOSED**, not completed.

**Evidence and interpretation (vertical notes):**

- **[Skill A] — [Claim, status]:** [Direct file/line link]. [Why it matters.]
- **[Skill B] — [Claim, status]:** [Direct file/line link]. [Why it matters.]

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

- **Priority:** [High / Medium / Low]
- **Finding:** [Problem and linked evidence.]
- **Proposed change:** [Ownership/documentation proposal only; when appropriate, cite the per-skill proposed optional handoff, boundary, and feedback wording from section 2.]
- **Standalone integrity:** [Does each skill retain its own inputs, outputs and workflow? If not evidenced, what needs human confirmation?]
- **Documentation location:** [Per affected skill: `SKILL.md` only, or `SKILL.md` plus optional directionally named local reference; reason; reuse existing suitable files.]
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
