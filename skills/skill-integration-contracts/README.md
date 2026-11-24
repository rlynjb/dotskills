# Skill Integration Contracts — Stage 3

A **read-only integration-design skill** for defining minimal, evidence-backed contracts between one or more agent skills. It follows [Stage 2 Responsibility & Overlap Audit](../skill-responsibility-overlap-audit/README.md) in the DotSkills five-stage engineering planner. The goal is to make **connections predictable while keeping every independently useful skill flexible**.

## What it does

- Reviews Stage 1 workflow context and Stage 2 `F-xx (Cx)` findings when available, plus actual target `SKILL.md` evidence. Neither prior artifact is required to run a bounded Stage 3 review.
- Maps the **specific intended connection(s)** and their proposed producer, consumer, human owner and standalone paths—not every possible skill pair.
- Drafts proportional `IC-xx` contracts for interface, behavior, invariants, trust/approval, failure/feedback and observability/version assumptions **when applicable**.
- Explains changes in senior-to-junior plain English, with **source → consequence → smallest recommended agreement → trade-off**.
- Creates a `D-xx` **human decision ledger** and a bounded Stage 4 implementation handoff. Any `V-xx` validation idea is proposed for Stage 5, **not executed**.

## What it doesn't do

It never edits the target skills, writes formal implementation files into them, automatically invokes them, starts a coordinator, calls live Jira, runs a test harness, or approves a design on a user's behalf. Written contracts do not imply runtime enforcement. No blanket approval is inferred from a prior audit recommendation.

## Quick start

```text
Use skill-integration-contracts on:
- skills/first-skill
- skills/second-skill

Stage 1 architecture: [optional link]
Stage 2 audit: [optional report with F-xx (Cx) findings]

Design the minimal optional handoff and human approval boundaries.
Preserve both skills' standalone inputs, workflow and outputs.
Show IC-xx contracts and D-xx decisions with direct source evidence.
Do not edit skills, implement a coordinator, or execute evaluations.
```

For a single skill, ask for its standalone entry/exit contract. For multiple independent skills, the tool considers **only meaningful intended connections** and can recommend that no integration contract is needed.

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
- [`evals/evals.json`](evals/evals.json) — **defined scenarios/assertions, not evidence the skill was behaviorally evaluated**.

The shared [Senior Engineer → Junior Developer Communication Guideline](../../docs/senior-engineer-mentoring-communication.md) supplies the common teaching style without adding more skill stages.
