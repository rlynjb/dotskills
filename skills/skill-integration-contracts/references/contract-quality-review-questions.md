# Contract Quality Review Questions — CQ-01–CQ-06

**Optional reference for `skill-integration-contracts` (Stage 3).** These questions review the **design quality of proposed integration contracts**, not the overall quality of underlying skills (Stage 2 Q-01–Q-10) or actual runtime behavior (Stage 5). They do not create six mandatory contracts or new engineering stages.

**Source:** The six questions preserve the wording proposed in the Stage 3 discussion. The mappings and evidence prompts are explanatory design-review guidance, not independent standards.

## Canonical six questions

- **CQ-01 — Interface Clarity:** Are required and optional information clearly distinguished?
- **CQ-02 — Behavioral Guarantees:** Are preconditions, postconditions, and invariants clear and necessary?
- **CQ-03 — Ownership & Authority:** Are decision owners, permissions, and human approval boundaries explicit?
- **CQ-04 — Reliability & Feedback:** Are important failure conditions and feedback responsibilities defined?
- **CQ-05 — Evidence & Traceability:** Can contract decisions be traced to source evidence and Stage 2 findings?
- **CQ-06 — Compatibility & Flexibility:** Does the contract preserve standalone skill behavior without unnecessary coupling?

## Mapping to the six contract dimensions

### CQ-01 — Interface Clarity

- **Question:** Are required and optional information clearly distinguished?
- **Maps to:** Interface.
- **Inspect:** Check the handoff trigger and required versus optional context; avoid inventing mandatory dependencies.
- **Evidence:** IC-xx interface; producer/consumer source.
- **Boundary:** Assess the proposed contract, not actual implementation or runtime enforcement. Do not add unnecessary requirements merely to satisfy the question.

### CQ-02 — Behavioral Guarantees

- **Question:** Are preconditions, postconditions, and invariants clear and necessary?
- **Maps to:** Behavior.
- **Inspect:** Check what must be true before/after this handoff and what must stay unchanged without constraining internal reasoning.
- **Evidence:** IC-xx behavior, assumptions and source.
- **Boundary:** Assess the proposed contract, not actual implementation or runtime enforcement. Do not add unnecessary requirements merely to satisfy the question.

### CQ-03 — Ownership & Authority

- **Question:** Are decision owners, permissions, and human approval boundaries explicit?
- **Maps to:** Security, authority and trust.
- **Inspect:** Distinguish who proposes from who approves, and instructions from enforced runtime permissions.
- **Evidence:** IC-xx approval terms; D-xx owner decision; inspected source.
- **Boundary:** Assess the proposed contract, not actual implementation or runtime enforcement. Do not add unnecessary requirements merely to satisfy the question.

### CQ-04 — Reliability & Feedback

- **Question:** Are important failure conditions and feedback responsibilities defined?
- **Maps to:** Failure, feedback and fault isolation.
- **Inspect:** Check missing/conflicting information, safe standalone continuation or BLOCKED/NEEDS HUMAN, and return ownership.
- **Evidence:** IC-xx error/feedback terms; owner and source.
- **Boundary:** Assess the proposed contract, not actual implementation or runtime enforcement. Do not add unnecessary requirements merely to satisfy the question.

### CQ-05 — Evidence & Traceability

- **Question:** Can contract decisions be traced to source evidence and Stage 2 findings?
- **Maps to:** Observability and evidence.
- **Inspect:** Require actual inspected source links and supplied F-xx (Cx) if available; don't require or invent a Stage 2 audit.
- **Evidence:** IC-xx source evidence; D-xx links; real Stage 2 F-xx (Cx) when supplied.
- **Boundary:** Assess the proposed contract, not actual implementation or runtime enforcement. Do not add unnecessary requirements merely to satisfy the question.

### CQ-06 — Compatibility & Flexibility

- **Question:** Does the contract preserve standalone skill behavior without unnecessary coupling?
- **Maps to:** Compatibility and evolution.
- **Inspect:** Check independent starting paths, proportional version assumptions and optional rather than mandatory cross-skill context.
- **Evidence:** Each target SKILL.md standalone entry/outputs; IC-xx optional trigger and trade-off.
- **Boundary:** Assess the proposed contract, not actual implementation or runtime enforcement. Do not add unnecessary requirements merely to satisfy the question.

## Optional review and coverage rules

- **Default: off.** Read this reference only with `quality_review: on`, `contract_quality_review: on` (equivalent *within Stage 3*), or an explicitly requested subset such as `quality_questions: CQ-03,CQ-06`. These options do not activate Stage 2 Q-01–Q-10.
- **Full request:** assess CQ-01 through CQ-06 in order against **each actual proposed IC-xx card**. **Subset:** assess only selected CQ IDs in canonical order. Do not silently widen the scope.
- **Output:** Under report **Section 5 — Cross-Cutting Guarantees & Trade-offs**, after its usual concise material considerations and **before Section 6 — Human Decision Ledger**, add **Contract Quality Review Coverage (optional)** as a Markdown comparison table. First column: CQ ID + title + **complete original question text**. Other columns: proposed IC-xx contracts (at most two contract columns per group; for more contracts repeat selected CQ rows). For one contract, use only one IC column. If no meaningful IC exists, explain and omit an empty table.
- **Cell assessment:** `CLEAR` (clear and proportional as a **proposal**, not approved); `NEEDS CLARIFICATION` (material ambiguous/overprescriptive design); `NEEDS HUMAN` (unresolved owner/approval design decision); `NOT VERIFIED` (unavailable source or other required design evidence); or `NOT APPLICABLE` (whole criterion genuinely irrelevant). Pair the label with concise evidence/reason.
- **IDs:** Include the actual `IC-xx`, real `D-xx` when a human decision matters, and supplied Stage 2 `F-xx (Cx)` only when it exists. Don't invent a Stage 2 audit or a second issue-ID scheme. Full explanation and proposed wording stay in the existing IC and D cards; the table points to them instead of duplicating.
- **Certainty versus approval:** A source may be DOCUMENTED, an IC is PROPOSED, a D may be unresolved, and enforcement may be UNVERIFIED. A CQ status of `CLEAR` is **not** an APPROVED contract, code implementation, security guarantee or passed evaluation. Don't automatically create Stage 5 tests because ordinary traces were not supplied.
- **Minimality:** Keep standalone capabilities intact, preserve real required safety gates, and avoid forced coordinator adoption, mandatory version systems or excessive schemas. The quality review is a design-check, not a license to make all six dimensions equally detailed.

## Example cell values (illustrative only)

- `CLEAR — IC-01; [documented handoff source]`
- `NEEDS CLARIFICATION — IC-01; optional context described as required; D-01`
- `NEEDS HUMAN — IC-02; D-02 approval authority unresolved; [source]`
- `NOT VERIFIED — IC-01; producer source unavailable`

These are format examples, not actual evaluated skills or approved contracts.
