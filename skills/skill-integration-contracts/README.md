# Skill Integration Contracts — Stage 3

A **read-only integration-design skill** for defining minimal, evidence-backed contracts between one or more agent skills. It follows [Stage 2 Responsibility & Overlap Audit](../skill-responsibility-overlap-audit/README.md) in the DotSkills five-stage engineering planner. The goal is to make **connections predictable while keeping every independently useful skill flexible**.

## What it does

- Reviews Stage 1 workflow context and Stage 2 `F-xx (Cx)` findings when available, plus actual target `SKILL.md` evidence. Neither prior artifact is required to run a bounded Stage 3 review.
- Maps the **specific intended connection(s)** and their proposed producer, consumer, human owner and standalone paths—not every possible skill pair.
- Drafts proportional `IC-xx` contracts for interface, behavior, invariants, trust/approval, failure/feedback and observability/version assumptions **when applicable**.
- Explains changes in senior-to-junior plain English, with **source → consequence → smallest recommended agreement → trade-off**.
- Creates a `D-xx` **human decision ledger** and a bounded Stage 4 implementation handoff. Any `V-xx` validation idea is proposed for Stage 5, **not executed**.
- Optionally compares **approved** IC-xx/D-xx terms with updated source **after Stage 4** using `implementation_alignment_review: on`, without changing target files or claiming runtime PASS.

## What it doesn't do

It never edits the target skills, writes formal implementation files into them, automatically invokes them, starts a coordinator, calls live Jira, runs a test harness, or approves a design on a user's behalf (including in implementation alignment mode). Written contracts do not imply runtime enforcement. No blanket approval is inferred from a prior audit recommendation.

## Quick start

```text
Use skill-integration-contracts on:
- skills/first-skill
- skills/second-skill

Stage 1 architecture: [optional link]
Stage 2 audit: [optional report with F-xx (Cx) findings]
Optional coordinator candidate: [existing SKILL.md or design file path, if available]

Design the minimal optional handoff and human approval boundaries.
Preserve both skills' standalone inputs, workflow and outputs.
Show IC-xx contracts and D-xx decisions with direct source evidence.
Do not edit skills, implement a coordinator, or execute evaluations.
```

For a single skill, ask for its standalone entry/exit contract. For multiple independent skills, the tool considers **only meaningful intended connections** and can recommend that no integration contract is needed.

## Inputting an optional coordinator candidate — Stage 3

If Stage 2 identified a meaningful routing, sequencing, context-preservation or feedback issue, **you can provide an existing coordinator file as an additional input** when running Stage 3. Label it `Optional coordinator candidate`, **separate from the two target skills** being integrated.

- **Coordinator file already exists:** Supply its actual `SKILL.md` path or existing design-document path, plus the target skill paths and any Stage 2 audit. The file is evidence of a **candidate design**, not proof that the coordinator is needed, approved, installed or executable.
- **Only a Stage 2 coordinator recommendation exists:** Supply the two target skills and the Stage 2 audit; **do not invent a third path or create a coordinator first**. Stage 3 can still assess whether simple handoffs are sufficient.
- **Stage 3 decision:** Compare manual/user-selected handoffs with a separately invoked optional coordinator, examine each skill's standalone path, and propose only justified `IC-xx` routing contracts and `D-xx` human decisions. A coordinator may be **NOT NEEDED**, **CONDITIONAL / PROPOSED**, or **DEFERRED**; it is not assumed to be the chosen design.
- **Stage 4 follow-through:** Implement a coordinator or routing mechanism **only when the specific design is approved**. If actual automatic dispatch is required, verify and implement the relevant host/tool support rather than treating `SKILL.md` wording as executable dispatch. Stage 5 tests observed behavior.

### Example — two skills and an existing coordinator file

```text
Use skill-integration-contracts on:
- [actual path to skill A/SKILL.md]
- [actual path to skill B/SKILL.md]

Stage 2 audit: [actual audit report path]
Optional coordinator candidate: [actual path to coordinator SKILL.md or design document]

Compare direct optional handoffs against the candidate coordinator.
Carry forward material Stage 2 findings and preserve standalone paths.
Propose only justified IC-xx contracts and D-xx human decisions.
Do not implement, invoke or assume the coordinator is approved.
```

All bracketed paths are placeholders; supply actual accessible files. If no coordinator file exists, omit that line rather than substituting a nonexistent path.

## Optional Contract Quality Review

**Default: off.** Like Stage 2's optional Quality Review Questions, Stage 3 offers **CQ-01–CQ-06** to examine the **proposed integration contracts**, not the skill packages themselves.

- `quality_review: on` or `contract_quality_review: on` checks all six contract-quality questions.
- `quality_questions: CQ-03,CQ-06` checks only those selected questions.
- Without either option, the four-step design workflow and seven report sections remain unchanged.

**Output:** An optional **Contract Quality Review Coverage** Markdown table inside **Section 5 — Cross-Cutting Guarantees & Trade-offs**, before Section 6's human decision ledger. Each row displays the full CQ question and each column an actual **IC-xx** contract. Cells have a brief `CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE` design assessment and real **D-xx / Stage 2 F-xx (Cx)** references where relevant.

```text
Use skill-integration-contracts on:
- skills/first-skill
- skills/second-skill

Stage 2 audit: [optional report]
quality_review: on

Design the minimal IC-xx contracts, assess CQ-01–CQ-06,
then show the D-xx human decisions.
Preserve standalone skill behavior; do not edit or execute.
```

A `CLEAR` contract is a readable proposal—not a human-approved design or a tested integration.

## Optional conference-derived Review Lenses and Further Reading

**Default off.** This Stage 3 option parallels Stage 2's conference lenses, but evaluates **proposed integration contracts**, not the individual skills.

- `review_lenses: relevant`: choose only lenses supported by actual target/IC context, explaining relevance.
- `review_lenses: [context-engineering, security-and-trust]`: explicitly choose these lenses (also available: `reliability-and-workflow`, `evaluation-and-observability`, `lifecycle-and-portability`).
- `quality_review: on` can run together with lenses. When both are enabled, **Section 5** shows Contract Quality Review Coverage first, Review Lens Coverage second, and **Conference Sources & Further Reading** third. A lens-only run does not imply CQ review took place.

**Conference learning sources in the result:** The Further Reading table gives the **topic**, **talk title**, **speaker**, and **direct PDF link** for each relevant selected-lens source, plus a **YouTube session link only when matched** in the saved conference YouTube/PDF spreadsheet. This is a learning reference, not evidence that a target IC is correct, approved or enforced.

```text
Use skill-integration-contracts on:
- skills/first-skill
- skills/second-skill

Stage 2 audit: [optional]
quality_review: on
review_lenses: relevant

Draft minimal IC-xx proposals, show contract quality and lens coverage,
then include sources by topic, title, speaker, PDF and matched YouTube.
Keep the skills independent; do not edit or run anything.
```

## Optional Industry Framework Review

A third optional review, mirroring Stage 2's [Industry Framework Review Lenses](../skill-responsibility-overlap-audit/references/industry-framework-review-lenses.md) but adapting the questions to **proposed Stage 3 integration contracts** rather than existing skill responsibilities. **Default off.**

- `industry_framework_review: relevant` selects only applicable industry frameworks for the drafted IC-xx contracts.
- `industry_framework_review: on` considers all five proportionately.
- `industry_frameworks: [aws-agentic-ai-lens, cmu-sei-atam]` selects only those two; the [reference](references/industry-framework-review-lenses.md) lists all five IDs.

**Output:** In Section 5, the **Industry Framework Review Coverage** table compares proposed IC-xx cards against the adapted design questions. **Official Industry Framework Sources & Further Reading** immediately follows with publisher, framework type, version, topic and direct official links. These are design reviews, not certified compliance, security proof or runtime evaluations. This independent option does not silently turn on CQ or conference review.

```text
Use skill-integration-contracts on:
- PRD Development
- Refine Requirements

industry_framework_review: relevant
```

The normal four-step procedure, standalone protections and D-xx human decision gate are already built in.

## Optional Implementation Alignment Review — after Stage 4

Use `implementation_alignment_review: on` when you have **approved Stage 3 integration contracts**, made the corresponding **Stage 4 changes**, and want to recheck whether the modified skill files align with the approved design. This remains **inside Skill Integration Contracts**, without creating another skill or using Review Implementation.

**It is instructions, not a script.** The review reads approved IC-xx/D-xx wording and the current changed skill source, then gives a source-level comparison. It never edits files, invokes skills, executes tests or certifies runtime behavior.

### What to provide

- **Approved Stage 3 design:** Link or path to the exact `IC-xx` contracts, `D-xx` decisions and explicit human approval of that version.
- **Implementation:** Link or paths to the modified `SKILL.md` files/references and, when available, the Git branch, commit or base/head diff.
- **Scope:** The intended producer → consumer connection(s). Other Stage 1/2 evidence is optional.

### Copyable invocation

```text
Use skill-integration-contracts on:
- skills/first-skill
- skills/second-skill

implementation_alignment_review: on

Approved Stage 3 design: [path or link to approved IC-xx/D-xx]
Implemented revision: [branch, commit, diff or current file paths]
```

You do **not** need to repeat the alignment procedure in the prompt.

### How to read the result

The alignment mode uses a **separate five-section report**, not the default seven-section design report:

1. **Review Scope & Approved Baseline** — exact approved IC-xx/D-xx, authorized decision scope, source revisions.
2. **Contract Alignment Coverage** — one material guarantee per row and **ALIGNED / PARTIALLY ALIGNED / MISMATCH / NOT VERIFIED** source-level verdict.
3. **Material Gaps & Evidence Limits** — source-backed differences and the smallest proposed correction.
4. **Next Stage & Iteration Handoff** — Stage 4 source fixes, separate Stage 3 design revisions needing human approval, or Stage 5 testing.
5. **Stage 5 Candidates — NOT EXECUTED** — only justified runtime tests to carry forward.

A contract can be **ALIGNED — DOCUMENTED SOURCE** while its runtime execution remains **NOT VERIFIED**. The mode never treats a missing trace alone as a failed implementation.

**Iteration loop:** Approve IC/D in Stage 3 → implement in Stage 4 → run this alignment review → correct Stage 4 mismatches and rerun the same approved design. If the approved **design must change**, revise it in a separate Stage 3 design pass and get specific new approval before implementing that change. Stage 5 performs actual behavioral evaluations.

**Approval requirement:** An explicit, identifiable approved design version is necessary for an authoritative alignment verdict. If only proposals or incomplete decisions are available, the result says **APPROVED BASELINE NOT VERIFIED**. No approval or contract wording is invented.

**Interaction with other options:** `quality_review`, `review_lenses` and `industry_framework_review` are for **design mode**; turning on implementation alignment chooses the alignment-only report. Run a separate design review to reassess the contract itself.

**Detailed procedure and reusable report:** [references/implementation-alignment-review.md](references/implementation-alignment-review.md).

## How to read the report

The seven stable headings are **Executive Summary**, **Current Skill Boundaries & Stage 2 Evidence**, **Proposed Interaction & Ownership Map**, **Proposed Integration Contract Cards**, **Cross-Cutting Guarantees & Trade-offs**, **Human Decision Ledger & Open Questions**, and **Stage 4 Implementation Handoff & Stage 5 Candidates**.

**IDs:**
- `C1–C6` = considerations in the Stage 2 audit.
- `F-xx` = findings from that audit, used only if an actual report supplies them.
- `IC-xx` = newly proposed integration contract cards.
- `D-xx` = human design decisions and their statuses.
- `V-xx` = candidate checks for separately authorized Stage 5 work.
- `CQ-xx` = optional Stage 3 Contract Quality Review questions.

**Status guidance:** PROPOSED means suggested, CONDITIONAL — NEEDS HUMAN means dependent on an unresolved ownership/permission decision, APPROVED — DESIGN ONLY means a human explicitly accepted an exact design version. None imply that integration is implemented or the agent actually ran.

## How to keep it flexible

**A handoff contract governs the connection, not every internal reasoning step.** If a skill accepts a feature idea independently and can optionally use a PRD, the contract must not quietly turn the PRD into a mandatory prerequisite. True safety/data requirements remain mandatory.

An optional coordinator contract is useful only when documented or expressly requested routing complexity merits the extra role. A `SKILL.md` cannot prove automatic dispatch by itself.

## Files

- [`SKILL.md`](SKILL.md) — canonical invocation, four-step procedure and report boundaries.
- [`references/contract-design-guide.md`](references/contract-design-guide.md) — six relevant contract dimensions, explanations and trade-off questions.
- [`references/report-template.md`](references/report-template.md) — copyable seven-section report, vertical IC/D cards, and optional CQ coverage table.
- [`references/contract-quality-review-questions.md`](references/contract-quality-review-questions.md) — canonical CQ-01–CQ-06 and coverage rules.
- [`references/review-lenses.md`](references/review-lenses.md) — five optional conference lenses with topics, speakers, PDF sources and matched YouTube links.
- [`references/industry-framework-review-lenses.md`](references/industry-framework-review-lenses.md) — five official industry references adapted to Stage 3 contract review.
- [`references/implementation-alignment-review.md`](references/implementation-alignment-review.md) — optional post-Stage-4 approved-contract/source alignment procedure and separate five-section output template.
- [`evals/evals.json`](evals/evals.json) — **defined scenarios/assertions, not evidence the skill was behaviorally evaluated**.

The shared [Senior Engineer → Junior Developer Communication Guideline](../../docs/senior-engineer-mentoring-communication.md) supplies the common teaching style without adding more skill stages.
