# Audit Skill — Report Structure (junior-developer guide)

This is a **report template**, not a completed audit and not a second questionnaire. It shows how to arrange an audit so the reader can investigate the current skills before deciding on changes.

**For a real audit:** replace every placeholder with inspected source-backed information, direct file/line links, or an honest NOT VERIFIED / NOT FOUND IN INSPECTED SOURCES / NOT APPLICABLE. Never copy an example as a factual finding. Do not generate files or run target skills simply because this structure exists.

## Audit Skill — Overall View

_What I found:_ [Two to four plain-English sentences about current scope and notable observations.]  
_Why this matters:_ [Consequence of a material gap or source uncertainty, if evidenced.]  
_Inspected sources:_ [Targets, revisions, direct links, unavailable materials.]  
_Execution:_ NOT EXECUTED.

## Step 1 — Skill Responsibility & Overlap Assessment

**Use this six-part worksheet for each accessible target.** It is designed for SDI Step 1 thinking: **Observe → Question assumptions → Validate before solving**.

### Skill: [Target skill A — current source and revision]

**01 — Inputs**  
_Observed:_ [What the skill currently requires or accepts.]  
_Evidence:_ [Direct file/line link or NOT VERIFIED.]  
_Open question:_ [What still needs source confirmation?]

**02 — Responsibilities**  
_Observed:_ [What this skill owns, advises or decides; do not confuse shared information with shared decision authority.]  
_Evidence:_ [Direct file/line link or NOT VERIFIED.]  
_Open question:_ [Who owns an uncertain decision?]

**03 — Outputs**  
_Observed:_ [What the skill produces: fields, artifacts, statuses, evidence, unanswered questions.]  
_Evidence:_ [Direct file/line link or NOT VERIFIED.]  
_Open question:_ [Is any result or guarantee unclear?]

**04 — Handoffs**  
_Observed:_ [Documented producer → consumer relationship and information that must be preserved, or absence of a defined neighbor.]  
_Evidence:_ [Direct file/line link or NOT VERIFIED.]  
_Open question:_ [Does the next skill actually consume this output?]

**05 — Boundaries**  
_Observed:_ [Prohibited actions, human authority, permission restrictions and stop conditions. Written promises are not proof of enforcement.]  
_Evidence:_ [Direct file/line link or NOT VERIFIED.]  
_Open question:_ [Which permission or approval remains unverified?]

**06 — Feedback**  
_Observed:_ [Documented return/escalation path: trigger → owner → information returned → stop/reassess/continue. If not relevant, say why.]  
_Evidence:_ [Direct file/line link or NOT VERIFIED.]  
_Open question:_ [Where does an issue go when a later step needs reconsideration?]

### Skill: [Target skill B, if supplied]

Repeat **01 Inputs through 06 Feedback** using the same three fields. Never invent another skill or a relationship merely to fill the template.

### Cross-skill Responsibility & Overlap (when two or more skills are available)

_Intentional shared information:_ [What multiple skills read for different reasons; evidence.]  
_Duplicated decision ownership:_ [What two skills both claim to decide, if source-supported.]  
_Missing responsibility:_ [What has no documented accountable owner.]  
_Handoff gap:_ [Required output, data, or guarantee not clearly handed off.]  
_Feedback-routing gap:_ [When reconsideration is needed, what route or owner is missing.]  
_Why it matters:_ [Concrete risk in plain English.]

### Supporting Quality Checks (Q-01–Q-10)

For each accessible target, report all ten Q checks, with an evidence-based status and explanation. Expand significant findings using **Question / Check / Finding / Evidence / Status / Recommendation**. Include separate Agent Skills conformance, relevant harness compatibility and **as-is Mermaid diagrams with node explanations**. These are supporting checks, not a substitute for the six considerations.

## Step 2 — Proposed Skill Boundaries

**B-01 — [Decision title]**  
_Observed issue:_ [Link to Step 1 evidence; no invented duplication.]  
_Recommended owner:_ [Skill or human accountable for the decision.]  
_Owns / does not own:_ [Explicit responsibility and exclusion.]  
_Why this helps:_ [Practical consequence and rationale.]  
_Alternative / trade-off:_ [One meaningful alternative when relevant.]  
_Affects:_ [C-01, etc., if applicable.]  
_Status:_ PROPOSED.

Repeat only for material decisions. A proposal is **not** a current implementation.

## Step 3 — Skill Integration Contracts — PROPOSED

**C-01 — [Producer → Consumer, or standalone input/output contract]**  
_Depends on:_ B-01 [when relevant].  
_Trigger:_ [When the handoff may occur.]  
_Required inputs:_ [Minimal fields and source information.]  
_Expected outputs:_ [What the receiving stage can rely on.]  
_Guarantees:_ [Identity, provenance, unresolved questions and authorization that must survive.]  
_Failure / stop behavior:_ [What happens when required information is missing or invalid.]  
_Feedback route:_ [Trigger → responsible recipient → evidence returned → resume/stop decision, if applicable.]  
_Trust / human boundary:_ [Permissions and approvals; do not invent enforcement.]  
_Why this matters:_ [Failure or inconsistency this contract is intended to prevent.]  
_Status:_ PROPOSED — CONDITIONAL ON B-01 [when dependency is unapproved].

These contract cards are **proposals shown up front**. Do not mark them approved until the relevant boundary and contract wording are explicitly accepted.

## Consolidated Human Review

**Decision overview**  
- **B-01:** [Plain-English recommended choice], PROPOSED.  
- **C-01:** [Plain-English proposed contract], PROPOSED — CONDITIONAL ON B-01.

_What the choices mean:_ Approve = accept the exact wording; Revise = change it; Reject = decline; Defer = decide later.

_Sample reply:_ `Approve B-01 and C-01. Revise B-02: ... Defer C-02.`

## Step 4 — Validation Readiness (NOT EXECUTED)

_Current readiness:_ [PENDING APPROVAL / BLOCKED / NOT VERIFIED; explain why].  
_Required first:_ [Approvals, suitable environment/data, or missing evidence.]  
_Possible behavior to verify:_ [One to three concrete expected outcomes; no automatic live tests.]  
_Execution:_ NOT EXECUTED — separate authorization and a safe test workflow are required.

**After the necessary approvals**, expand into a sanitized **Given → When → Then** test plan, hand execution to a separately authorized runner or Evaluate Skill, and inspect real traces read-only when supplied.

---

**Keep this mental separation:** Step 1 observes current evidence; Steps 2 and 3 propose decisions and contracts; the human approves/revises; Step 4 prepares or reviews evidence of a separately authorized execution. The six considerations are the Step 1 investigation structure, not an additional framework to memorize.
