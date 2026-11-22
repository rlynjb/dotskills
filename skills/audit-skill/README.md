# Audit Skill

**Audit Skill is now a guided, human-reviewed design audit for one or more agent skills.** It discovers what exists, proposes better responsibility boundaries, lets you approve or revise them, then proposes handoff contracts for another human review. Finally, it prepares a validation checklist and can inspect genuine test evidence.

It stays **read-only**. It does not execute the target skills, edit their files, approve decisions on your behalf, or silently start Evaluate Skill.

## Table of contents

1. [Why this skill exists](#1-why-this-skill-exists)
2. [The four steps and two human gates](#2-the-four-steps-and-two-human-gates)
3. [What a first run looks like](#3-what-a-first-run-looks-like)
4. [How to approve or revise a boundary](#4-how-to-approve-or-revise-a-boundary)
5. [How to approve a handoff contract](#5-how-to-approve-a-handoff-contract)
6. [What validation means here](#6-what-validation-means-here)
7. [Q-01–Q-10 and evidence](#7-q-01q-10-and-evidence)
8. [Run your own audit](#8-run-your-own-audit)
9. [Skill boundaries and safety](#9-skill-boundaries-and-safety)

## 1. Why this skill exists

Imagine four coding-agent skills that participate in an engineering workflow. Each skill has its own `SKILL.md`, but there are unanswered design questions:

- Two skills both check whether requirements are complete. Which one makes the final decision?
- The output from one skill is useful to the next, but no one defined which fields are required.
- A skill silently assumes an unanswered question was resolved.
- A workflow looks correct on paper, but nobody has observed it execute end-to-end.

Audit Skill helps separate four things:

1. **What exists** in the inspected source.
2. **What you propose** should change.
3. **What a human explicitly approves** as a design decision.
4. **What has actually been implemented and observed** in a tested environment.

Those are separate claims. Approving a recommendation does not mean someone edited the skills, and a documented safety rule does not prove the host enforces it.

## 2. The four steps and two human gates

```text
  STEP 1 — Responsibility & overlap audit
  Inspect current SKILL.md files, dependencies, Q-01–Q-10
                         |
  STEP 2 — Define boundaries
  Recommend owner / non-owner / decision authority
                         |
                  HUMAN GATE A
             Approve / revise / defer
                         |
  STEP 3 — Define handoff contracts
  Recommend producer / consumer / fields / guarantees
                         |
                  HUMAN GATE B
             Approve / revise / defer
                         |
  STEP 4 — Validation preparation
  Test scenario / expected behavior / evidence review
                         |
              Separate authorized test
                (Codex / Evaluate Skill)
```

There is no extra mode selector. The same workflow handles one or multiple skills.

**First response:** Audit Skill completes Step 1 and recommends the Step 2 boundary decisions. It then **stops** for your review. It does **not** interrupt you between every Q-01–Q-10 finding.

**Second response (after Gate A):** It incorporates your boundary decisions and drafts Step 3 handoff contracts. It stops at **Gate B**.

**Third response (after Gate B):** It shows what is approved, what is still pending, and a realistic Step 4 validation handoff.

If a decision is deferred, only the work that depends on that decision is blocked. You can still discuss or approve unrelated boundaries.

## 3. What a first run looks like

For a single target, Audit Skill inventories responsibilities, prohibited actions, inputs, outputs, ownership, and internal boundaries. It will not invent other skills to manufacture an overlap finding.

For multiple targets, it independently assesses every accessible skill and compares them afterward.

A Step 1 report includes:

- **Audit Skill — At a Glance:** source revision, inspected/unavailable files, current responsibilities, and `NOT EXECUTED`.
- **Q-01–Q-10:** ten evidence-backed checklist markers and ten short findings **per accessible skill**.
- **As-is Mermaid diagram:** the actual documented workflow, distinguishing unknown edges from established behavior.
- **Responsibility/overlap comparison:** unique responsibilities, shared context, duplicated decisions, conflicting instructions, unowned work, and missing handoffs.
- **Agent Skills standards and runtime compatibility:** documented format/conformance, dependencies, and any unverified claims about Codex or another host.
- **Boundary decision proposals:** short `B-xx` items that need your input.

### Example — four engineering skills

Suppose these are your selected targets:

- PRD Development
- Refine Requirements
- Jira Ticket Decomposition
- Sprint Assessment

A *hypothetical* Step 1 finding is that Refine Requirements and Sprint Assessment both describe checking acceptance criteria. That is a **shared concern**, not necessarily a conflict. The audit should identify the actual decision each skill owns, using links to the inspected source.

A candidate `B-01` recommendation could be:

> **Decision B-01 — Who owns requirements clarity?**
>
> **Observed:** Two skills examine acceptance criteria.
>
> **Recommendation:** Refine Requirements owns detailed requirements clarification. Sprint Assessment consumes that result when judging sprint readiness and reports missing evidence instead of silently rewriting the requirements.
>
> **Alternative:** Both skills independently clarify requirements, but that risks contradictory decisions and duplicated work.
>
> **Status:** PROPOSED — your review required.

This is an **illustrative proposal**, not an assertion about what the four current skills do. The actual audit must inspect their source and cite lines first.

## 4. How to approve or revise a boundary

At **Gate A**, Audit Skill should show you decision IDs, recommended owners, exclusions, evidence, and trade-offs. You can respond naturally:

```text
Approve B-01 and B-02. Defer B-03.
```

Or:

```text
Revise B-01. Sprint Assessment should identify missing
requirements, but it should not change acceptance criteria.
Keep the rest of the recommendation.
```

For revisions, Audit Skill restates the **new wording** and asks for your confirmation of that changed decision. It must not label the new wording APPROVED based only on the old approval.

Each decision is tracked with a status:

- **PROPOSED** — the skill recommended it.
- **APPROVED** — you explicitly approved the specific wording.
- **REVISED** — the recommendation was changed; final approval is still required.
- **REJECTED** — not adopted.
- **DEFERRED** — pending a later decision.

**Important:** This is approval of the *design decision in the conversation*. It is not authorization to modify files, run agents, or claim that a team or manager signed off.

## 5. How to approve a handoff contract

Once the relevant boundaries are approved, Audit Skill moves to Step 3. It keeps contracts **lightweight**: enough clarity for two skills to cooperate reliably without designing a giant schema prematurely.

A proposed contract should explain:

- **Producer → consumer:** which skill provides information and which skill consumes it.
- **When:** conditions required before the handoff is allowed.
- **Inputs and outputs:** required and optional fields; expected result states.
- **Guarantees:** information that must not be lost or silently changed.
- **Failure handling:** what happens when information is missing, contradictory, malformed, or unavailable.
- **Trust and authority:** source provenance, sensitive information, and human approval boundaries.
- **Compatibility:** schema/version requirements where they actually matter.

### Example — not an implemented contract

```text
C-01 — Refine Requirements → Jira Ticket Decomposition

Required input:
  - Ticket or requirement identity
  - Refined requirements and acceptance criteria
  - Source references
  - Open questions and unresolved decisions

Expected output:
  - Candidate decomposition with traceable source links
  - Explicit blocked/needs-clarification state when appropriate

Must preserve:
  - Original identity, sources, open questions, approval state

Missing data:
  - Mark NEEDS HUMAN; do not invent acceptance criteria

Status: PROPOSED — requires Gate B approval
```

This is a teaching example; the real contract must be adapted to the current files and your approved boundaries.

At **Gate B**, you can approve `C-01`, revise a field, or defer a contract. Anything dependent on a deferred boundary stays `CONDITIONAL` and cannot be finalized.

## 6. What validation means here

**Audit Skill prepares validation, but it does not run the workflow.**

After your approvals, it can give you a representative scenario and a checklist to use in a separate, explicitly authorized Codex execution. The important checks include:

- Does the right skill own each decision?
- Are input and output fields passed correctly between skills?
- Do original sources and unanswered questions survive?
- Does missing information result in `BLOCKED` or `NEEDS HUMAN` instead of a made-up answer?
- Are approval, security and tool permissions respected?
- Are errors and partial failures visible?
- Is runtime evidence available for any portability or reliability claim?

If you already performed an authorized run and supply traces or results, Audit Skill can **inspect that evidence read-only**, comparing it with the approved contract. It must distinguish genuine observed behavior from a source document's promise.

For **executing and grading** behavior, use [Evaluate Skill](../evaluate-skill/SKILL.md) under its own authorization and sandbox restrictions. Check its current runner status rather than assuming live evaluations are available. A `READY TO TEST` label does not mean `TESTED` or `PASSED`.

## 7. Q-01–Q-10 and evidence

These ten criteria remain the canonical static/evidence-based review underneath Step 1. They are **not** ten new approval gates:

- **Q-01 — Purpose & boundaries:** What does the skill own and avoid?
- **Q-02 — Activation & discovery:** When and how does it activate?
- **Q-03 — Structure, inputs & dependencies:** What resources does it need?
- **Q-04 — Workflow & orchestration:** How does it make decisions, delegate, stop, and ask for approval?
- **Q-05 — Contracts & outputs:** What enters and leaves? What are the guarantees and failure rules?
- **Q-06 — Context & trust:** Are sources current, attributable, and safely treated?
- **Q-07 — Permissions & effects:** What can the skill change, and who enforces that?
- **Q-08 — Failure & stop behavior:** What happens when something fails or is missing?
- **Q-09 — Evals & observability:** Are there real executed checks or just proposed tests?
- **Q-10 — Lifecycle & portability:** Who maintains it and what runtimes are supported?

For a checked criterion, Audit Skill needs **appropriate evidence**. A documented output format may support a documented contract, but prompt-only read-only language cannot prove host permission enforcement. Defined eval cases cannot prove a live run.

The finding for every Q uses the same **Question → Check → Finding → Evidence → Status → Recommendation** layout. Claims must link directly to inspected files/lines. It separates:

- **DOCUMENTED INSTRUCTIONS:** written behavior.
- **IMPLEMENTED CHECK:** validator/guard in inspectable code or config.
- **OBSERVED RESULT:** actual authorized execution evidence.
- **NOT VERIFIED:** insufficient evidence.

Read [Q-01–Q-10 explained with examples](references/coverage-checklist-examples.md) for the junior-friendly walkthrough.

## 8. Run your own audit

**Single skill:**

```text
Use audit-skill on Refine Requirements.
Inspect its SKILL.md and material references.
Give the full Step 1 Q-01–Q-10 evidence-backed review.
Then recommend B-xx responsibility/boundary decisions
and stop at Gate A for my approval.
Do not edit or execute anything.
```

**Four skills together:**

```text
Use audit-skill on PRD Development, Refine Requirements,
Jira Ticket Decomposition, and Sprint Assessment.

Step 1: inspect all accessible SKILL.md files and references;
show evidence-backed responsibility/overlap findings.
Step 2: recommend a clear owner, non-owner, and decision authority
for every material overlap or gap. Let me approve or revise
the B-xx decisions at Gate A.

After my approval, propose lightweight C-xx handoff contracts
at Gate B. Once those are approved, prepare the validation
scenario and checks. Do not run tests or change files.
```

For a shorter follow-up, refer to a decision ID, such as `Revise B-02`, `Approve C-01`, or `Explain why Q-05 is partial`.

See also the [Sprint Assessment worked example](references/sprint-assessment-audit.md).

## 9. Skill boundaries and safety

Audit Skill's role is **evidence-backed inspection and human-gated design review**. It does not become an implementation agent or execution harness just because a human approves a design.

- **Audit Skill:** inspect, compare, recommend, record human design choices, draft contracts, prepare/check validation evidence.
- **Evaluate Skill:** separately authorized execution/evaluation, grading, diagnosis, and improvement under its current safety gates.
- **The human/team:** approve architectural ownership and interface contracts; authorize implementation, data access, and execution separately.

The practical mental model is:

**Inspected source → recommended boundary → human-approved boundary → proposed contract → human-approved contract → separate test evidence.**

The four user-facing steps here are not the same as the four SDI engineering-reasoning steps. Audit Skill may use SDI *internally* to reason about scope, design, contracts, and trade-offs, but you should only have one guided review process to follow.
