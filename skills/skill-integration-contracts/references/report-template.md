# Skill Integration Contracts — Stage 3 Report Template

This is an **output template, not a source of target facts or approvals**. Replace brackets with actual inspected evidence. Keep the seven section titles and the source-backed junior-friendly explanations. `F-xx (Cx)` refers only to real prior Stage 2 findings; `IC-xx`, `D-xx` and `V-xx` are report-local Stage 3 references.

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

- **Intended connection:** [Producer → consumer; when chosen, required vs optional, and explicit standalone alternatives.]
- **Proposed decision owner:** [Who owns product/domain decisions, technical decisions, human approval, feedback resolution. Don't guess names.]
- **Simpler path vs coordinator:** [NOT NEEDED / CONDITIONAL PROPOSAL / DEFER; why.]
- **Human checkpoints:** [What requires explicit human action, not just an AI suggestion.]
- **Diagram when useful:**

```text
[Skill A standalone input] -> [Skill A output]
               |
               +-- optional context, user/authorized workflow chooses -->
                                              [Skill B standalone input or optional context]
                                              [Skill B review result] -> [Human owner decides]
```

The diagram is **illustrative**, not evidence of actual dispatch or existing tool integration.

## 4. Proposed Integration Contract Cards

Write **one vertical card per material connection**. Don't create one card per category, and don't fill irrelevant fields.

**IC-01 — [Source skill] → [Target skill] (PROPOSED / CONDITIONAL — NEEDS HUMAN / APPROVED — DESIGN ONLY)**

- **Purpose:** [Why this specific handoff helps.]
- **Sources / Stage 2 link:** [Direct source links, revision and real `F-xx (Cx)` if available; distinguish DOCUMENTED from INFERRED.]
- **Producer / consumer / owner:** [Who supplies, who reviews, who authorizes; distinguish producer's domain ownership from consumer's.]
- **Trigger and standalone path:** [When optional/required handoff occurs; how each skill can still run independently or what truly required prerequisite exists.]
- **Inputs:** [Only genuinely required fields for this handoff vs optional context; source/revision, provenance and unresolved questions when applicable.]
- **Outputs / postconditions:** [Minimum usable result and what successful completion promises.]
- **Preconditions / invariants:** [What must be true before a handoff; what must remain unchanged, e.g. source ID, unresolved decisions, approval status.]
- **Failure and feedback:** [Missing/conflicting inputs → safe continuation / BLOCKED / NEEDS HUMAN; owner to whom changes are proposed; when work can resume.]
- **Trust / approval / permitted effects:** [Who can propose, edit, publish or approve; documented instructions vs runtime enforcement assumptions.]
- **Observability / compatibility (if relevant):** [Minimum evidence/IDs, optional format revisions and known host assumptions; don't promise unverified functionality.]
- **Why / trade-off:** [Concrete downstream failure prevented, alternative and cost of extra requirements.]
- **Dependencies and status:** [Related `D-xx`; `PROPOSED` or `CONDITIONAL — NEEDS HUMAN` until explicit sign-off; never claim implemented.]

For one skill, name `IC-01 — [Skill] standalone entry/exit`; don't invent a producer. When a contract is not relevant, omit it rather than inserting empty fields.

## 5. Cross-Cutting Guarantees & Trade-offs

Capture only material constraints **not already clear** in contract cards.

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
