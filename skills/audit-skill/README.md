# Audit Skill

**Audit Skill gives you the whole engineering picture before asking for decisions.** It inspects the skills as they exist, recommends responsibility boundaries, drafts the corresponding handoff contracts, and presents all three parts **in one initial overview**.

You can then approve, revise, reject, or defer **individual boundaries and contracts**, or approve a clearly identified compatible set. No automatic architectural decisions, edits, or test executions.

## Table of contents

1. [Why this skill exists](#1-why-this-skill-exists)
2. [The overview-first four-step workflow](#2-the-overview-first-four-step-workflow)
3. [What the first report contains](#3-what-the-first-report-contains)
4. [Step 1 — Inspect responsibilities and overlap](#4-step-1--inspect-responsibilities-and-overlap)
5. [Step 2 — Propose boundaries](#5-step-2--propose-boundaries)
6. [Step 3 — Propose handoff contracts](#6-step-3--propose-handoff-contracts)
7. [Review and revise decisions together](#7-review-and-revise-decisions-together)
8. [Step 4 — Prepare validation](#8-step-4--prepare-validation)
9. [Q-01–Q-10 and evidence](#9-q-01q-10-and-evidence)
10. [Try it with your skills](#10-try-it-with-your-skills)
11. [Responsibilities and safety](#11-responsibilities-and-safety)

## 1. Why this skill exists

Imagine four skills in a development workflow. They may each look fine individually, but the **relationships** are unclear:

- Two skills both inspect acceptance criteria. Which one owns the final decision?
- A downstream skill needs a field the upstream skill never guarantees.
- A missing requirement quietly turns into an assumption.
- Everyone agrees with an architecture diagram but nobody has verified the workflow in Codex.

If you approve skill boundaries before seeing the handoff contracts, you might miss how those decisions change the flow. **The new design deliberately shows Steps 1, 2, and 3 together**, before your first decision.

The key distinction is between **CURRENT DOCUMENTED**, **PROPOSED**, **HUMAN-APPROVED DESIGN**, **IMPLEMENTED CHECK**, and **OBSERVED RESULT**. Each means something different.

## 2. The overview-first four-step workflow

```text
  STEP 1 — Responsibility & overlap audit
  Inspect SKILL.md files, dependencies, Q-01–Q-10
                         |
  STEP 2 — Proposed boundaries
  Who owns each decision? What must each skill not do?
                         |
  STEP 3 — Proposed handoff contracts
  Inputs / outputs / guarantees / failures / dependencies
                         |
              ONE COMPLETE OVERVIEW
             Steps 1 + 2 + 3 together
                         |
                HUMAN REVIEW
   Approve / revise / reject / defer B-xx and C-xx
                         |
  STEP 4 — Validation preparation
  Expected behavior / sample scenario / evidence
                         |
             Separate authorized run
               (Codex / Evaluate Skill)
```

There is **one consolidated human review stage**, not an earlier Gate A and a later Gate B. The human may take several turns to revise decisions. The skill should not advance an unresolved path as if approved.

**First response:** show the full analysis and both types of proposals. **Later responses:** address your chosen decisions, update dependencies, and prepare Step 4 when the relevant decisions are approved.

## 3. What the first report contains

Begin with **Audit Skill — Overall View**, a skimmable summary of:

- **Each skill today:** purpose, current responsibilities, outputs and any important uncertainties.
- **How skills relate:** which responsibilities are unique, shared, duplicated, conflicting, or unowned.
- **Proposed boundaries:** `B-01`, `B-02`, and so on, each with an accountable owner, exclusions and trade-offs.
- **Proposed contracts:** `C-01`, `C-02`, and so on, showing how data should move and what must be preserved.
- **Dependencies:** which proposed contract depends on which proposed boundary.
- **Review ledger:** one place to see what you can approve/revise/reject/defer.

The report also contains **source-backed supporting evidence**: per-skill Q-01–Q-10 coverage checklists, material findings, as-is Mermaid diagrams, Agent Skills format checks, and runtime compatibility limitations. The full ten six-field Q explanations may be expanded on request. This keeps a four-skill audit skimmable instead of burying the proposed architecture under dozens of repetitive fields.

**Nothing in this first report is automatically approved.**

## 4. Step 1 — Inspect responsibilities and overlap

Audit Skill examines authorized source files, starting with `SKILL.md` and material references, including resources, scripts, agents, schemas, and existing eval evidence.

For **one skill**, it assesses responsibility boundaries and internal/input-output contracts. It never invents a second skill simply to find an overlap.

For **multiple skills**, it first assesses each independently, then compares:

- **Unique ownership:** one skill performs a job and decides its result.
- **Shared context:** two skills both use the same information, but have different responsibilities.
- **Duplicated decision ownership:** two skills both claim to make the same authoritative decision.
- **Conflict:** instructions or ownership claims disagree.
- **Unowned responsibility:** the workflow needs a decision, but no skill owns it.
- **Handoff gap:** producer and consumer disagree about information or failure behavior.

Do not confuse an as-is flow with a proposed future architecture. Every material conclusion should have a real file/line source link.

## 5. Step 2 — Propose boundaries

A recommendation is expressed as a named `B-xx` decision. It explains what exists, the recommended owner, what that skill should **not** own, alternatives and trade-offs.

### Example B-01 — Requirements clarity versus sprint readiness

*Hypothetical example, not a result of a fresh source audit.*

- **Observed concern:** Refine Requirements and Sprint Assessment may both inspect requirements.
- **Recommendation:** Refine Requirements owns detailed requirements clarification. Sprint Assessment consumes that conclusion for sprint readiness and reports missing requirements without silently rewriting them.
- **Alternative:** Both independently re-decide requirements clarity, potentially duplicating work and creating conflicts.
- **Affects contracts:** C-01.
- **Status:** PROPOSED.

The Audit Skill **does not pause here**. It proceeds to propose the affected contract so you can assess the boundary and its consequences together.

## 6. Step 3 — Propose handoff contracts

Each `C-xx` proposal describes the minimum useful agreement between producer and consumer:

- Who produces the result and who consumes it.
- When the handoff can happen.
- Required/optional inputs and expected outputs.
- Guarantees and invariants: source references, ticket identity, unresolved questions, and approval state, as appropriate.
- What happens on missing inputs, errors, conflicting information or partial failures.
- Trust, permission and compatibility boundaries.

### Example C-01 — Refine Requirements → Sprint Assessment

*Illustrative and conditional on proposed B-01.*

```text
Producer: Refine Requirements
Consumer: Sprint Assessment

Inputs:
  - Ticket identity
  - Assessed requirements and acceptance criteria
  - Evidence/source links
  - Unresolved questions and any human decisions

Expected consumer behavior:
  - Assess sprint readiness from the supplied evidence
  - Report BLOCKED or NEEDS HUMAN if required inputs are missing
  - Do not silently invent or change acceptance criteria

Must preserve:
  - Original identity, provenance, open questions, approvals

Depends on: B-01
Status: PROPOSED — CONDITIONAL ON B-01
```

This contract **appears in the first report**, even though B-01 is not approved yet. It is **not an implemented, enforced, or approved contract**.

## 7. Review and revise decisions together

After seeing the whole picture, you can give feedback naturally:

```text
Approve B-01 and C-01.
Revise B-02 so Sprint Assessment can report missing
requirements but cannot edit acceptance criteria.
Defer C-02.
```

The skill should:

1. Record the explicit decisions for the exact displayed wording.
2. Mark B-02 **REVISED** and show its updated wording for your confirmation.
3. Re-check any C-xx proposals that depend on B-02; show changed terms and request new approval.
4. Preserve unrelated approvals; mark deferred/blocked dependencies clearly.
5. Only move a path to validation preparation once its **relevant** boundaries and contracts are approved.

**You may approve B-01 and C-01 together** if the wording is clear and consistent. The skill processes boundary approval first, then contract approval. If you revise B-01, C-01 must be checked against that revision rather than implicitly approved.

Available decisions: **APPROVE, REVISE, REJECT, DEFER**. A vague “looks good” is not automatic blanket approval of conflicting or unseen choices.

The decision ledger records IDs, wording, current source revision, dependencies and status. An approval in the conversation is **design approval**, not permission to edit GitHub files, run agents or claim the team approved it.

## 8. Step 4 — Prepare validation

After the relevant B and C items are approved, Audit Skill proposes a representative, sanitized scenario and an evidence-based checklist:

- Did each skill make only the decisions it owns?
- Did the handoff preserve required inputs, sources, unanswered questions and approval states?
- Did missing data produce BLOCKED/NEEDS HUMAN rather than a guessed answer?
- Were errors and partial failures handled properly?
- Did runtime permissions and human approval requirements hold?
- Were relevant output formats and orchestration claims demonstrated by traces?

**Audit Skill itself does not run tests.** A separately authorized Codex or [Evaluate Skill](../evaluate-skill/SKILL.md) workflow can execute tests when its tool permissions and environment safety controls permit it. Check the evaluation runner's actual current status rather than assuming live end-to-end tests work.

If genuine authorized trace evidence is supplied, Audit Skill may inspect it **read-only** and compare observed behavior to the approved contracts. READY TO TEST does **not** mean TESTED or PASSED.

## 9. Q-01–Q-10 and evidence

The existing ten engineering checks remain the foundation of the audit. They are **review criteria**, not ten separate approval prompts.

- **Q-01 — Purpose & boundaries:** purpose, users, prohibited actions.
- **Q-02 — Activation & discovery:** invocation, triggers and wrong-trigger behavior.
- **Q-03 — Structure, inputs & dependencies:** source resources, environment and missing files.
- **Q-04 — Workflow & orchestration:** stages, decisions, delegation and approvals.
- **Q-05 — Contracts & outputs:** inputs, outputs, validation, invariants and failed handoffs.
- **Q-06 — Context & trust:** source provenance, freshness, contradictions and untrusted inputs.
- **Q-07 — Permissions & effects:** allowed changes and host/tool enforcement.
- **Q-08 — Failure & stop behavior:** errors, retries, partial outcomes and escalation.
- **Q-09 — Evals & observability:** actual test definitions/results, traces and gaps.
- **Q-10 — Lifecycle & portability:** versioning, rollback, maintenance and supported harnesses.

For every accessible skill, Audit Skill checks all ten and gives a short coverage checklist. When you request a detailed finding (or a significant gap needs explanation), the standard six fields are **Question → Check → Finding → Evidence → Status → Recommendation**.

Evidence states:

- **DOCUMENTED INSTRUCTIONS** = source claims a behavior.
- **IMPLEMENTED CHECK** = inspected code/config contains a validator or guard.
- **OBSERVED RESULT** = genuine authorized run/trace evidence.
- **NOT VERIFIED** = source or runtime evidence is insufficient.

See [Q-01–Q-10 with examples](references/coverage-checklist-examples.md). A prompt saying “read-only” does not prove enforced permissions; eval definitions do not prove the tests were run.

## 10. Try it with your skills

**Four-skill overview:**

```text
Use audit-skill to inspect PRD Development,
Refine Requirements, Jira Ticket Decomposition,
and Sprint Assessment.

In the first response, give me one overview covering:
Step 1 — current responsibilities, overlap and gaps;
Step 2 — all proposed B-xx ownership boundaries;
Step 3 — all proposed C-xx handoff contracts,
including their dependencies on B-xx decisions.

Show source evidence and Q-01–Q-10 coverage.
Do not pause for approvals between Steps 1–3.

After presenting the entire picture, let me approve,
revise, reject or defer individual B-xx and C-xx items.
Then prepare Step 4 validation when relevant decisions
are approved. Do not run tests or edit files.
```

**Single-skill overview:**

```text
Use audit-skill on Refine Requirements.
Inspect the current skill and its material references,
propose any B-xx boundary improvements and any
meaningful C-xx invocation/output contract.
Show Steps 1–3 together, then ask for my review.
Do not fabricate neighboring skills or execute anything.
```

**Follow-up review:**

```text
Approve B-01 and C-01 as written.
Revise B-02: Sprint Assessment can flag missing criteria,
but cannot rewrite them. Show dependent contracts.
Defer C-03.
```

A multi-skill teaching example is in [Sprint Assessment worked example](references/sprint-assessment-audit.md).

## 11. Responsibilities and safety

- **Audit Skill:** inspect existing skills, compare responsibilities, propose boundaries/contracts, record human design choices, prepare validation scenarios and inspect supplied evidence.
- **Evaluate Skill:** separately authorized behavioral evaluation, grading and diagnostics, under its own current safety and sandbox restrictions.
- **Human/team:** approve architecture and contracts, authorize actual source changes and live execution separately.

The four visible steps of this workflow are **not** four new SDI reasoning stages. Audit Skill may use SDI internally for scope, design, contracts, and trade-offs.

**Mental model: inspect all skills → see boundaries and contracts together → approve/revise decisions → validate in a separate authorized run.**
