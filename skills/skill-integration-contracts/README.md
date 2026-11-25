# Skill Integration Contracts — Stage 3

A **read-only integration-design skill** for defining minimal, evidence-backed contracts between one or more agent skills. It follows [Stage 2 Responsibility & Overlap Audit](../skill-responsibility-overlap-audit/README.md) in the DotSkills five-stage engineering planner. The goal is to make **connections predictable while keeping every independently useful skill flexible**.

## What it does

- Reviews Stage 1 workflow context and Stage 2 `F-xx (Cx)` findings when available, plus actual target `SKILL.md` evidence. Neither prior artifact is required to run a bounded Stage 3 review.
- Maps the **specific intended connection(s)** and their proposed producer, consumer, human owner and standalone paths—not every possible skill pair.
- Drafts proportional `IC-xx` contracts for interface, behavior, invariants, trust/approval, failure/feedback and observability/version assumptions **when applicable**.
- Explains changes in senior-to-junior plain English, with **source → consequence → smallest recommended agreement → trade-off**.
- Creates a `D-xx` **human decision ledger** and a bounded Stage 4 implementation handoff. Any `V-xx` validation idea is proposed for Stage 5, **not executed**.
- Optionally reviews updated source **after Stage 4** using `implementation_alignment_review: on`: approved design alignment, provisional design alignment, or source-based integration assessment, without changing targets or claiming runtime PASS.

## What it doesn't do

It never edits the target skills, writes formal implementation files into them, automatically invokes them, starts a coordinator, calls live Jira, runs a test harness, or approves a design on a user's behalf (including in implementation alignment mode). Written contracts do not imply runtime enforcement. No blanket approval is inferred from a prior audit recommendation.

## Quick start

```text
Use skill-integration-contracts on:
- [path to a target skill or skill document]
- [another target skill path, if applicable]
- [additional target skill paths, if applicable]

Stage 1 architecture: [optional link]
Stage 2 audit: [optional report with F-xx (Cx) findings]
Optional coordinator candidate: [existing SKILL.md or design file path, if available]

Design the minimal applicable standalone or cross-skill contracts.
Consider direct handoffs versus optional coordination only if relevant.
Preserve each skill's independent entry and output where supported.
Show IC-xx contracts and D-xx decisions with direct source evidence.
Do not edit skills, implement a coordinator, or execute evaluations.
```

The bracketed paths are placeholders: include **only actual, accessible files relevant to the scope**. The number of target skills is **not fixed**. For one skill, design its standalone entry/exit contract without inventing a partner. For multiple skills, examine only meaningful intended connections. This workflow is **skill- and domain-agnostic**; named project skills elsewhere in the documentation are examples, not mandatory inputs.

## Inputting an optional coordinator candidate — Stage 3

If the scope, supplied evidence or a Stage 2 audit raises a material **routing, sequencing, context-preservation or feedback** concern, an **existing** coordinator `SKILL.md` or design file **may** be supplied as an **additional input**. Label it `Optional coordinator candidate` and distinguish it from the **target skill(s)** whose standalone and integration contracts are being designed.

- **Coordinator file exists:** Supply its actual path and any available prior audit/architecture material. Inspect it as **candidate design evidence**, not proof that a coordinator is necessary, approved, installed or executable.
- **Only a coordinator recommendation exists:** Supply the target skill path(s) and any actual Stage 2 findings or other evidence. **Do not invent a coordinator path or create a file** simply to complete the input list.
- **No coordination concern:** Omit the coordinator entirely. A standalone-only review does not require a second skill or coordinator. For a multi-skill review, a simple user-selected handoff may be enough.
- **Stage 3 decision:** When applicable, compare minimal direct/user-chosen handoffs with an optional coordinator, preserve standalone paths, and propose proportionate `IC-xx` contracts and `D-xx` human decisions. Outcomes may be NOT NEEDED, a CONDITIONAL PROPOSAL, or DEFERRED; the candidate file is not approval.
- **Stage 4 follow-through:** Implement only the **explicitly approved** contracts/routing approach. If automatic dispatch is part of the approved design, independently verify and implement host/tool support; a `SKILL.md` instruction alone is not a running dispatcher. Stage 5 evaluates observed behavior.

### Generic invocation — any relevant skill set

```text
Use skill-integration-contracts on:
- [target skill path]
- [another target skill path, if applicable]
- [additional target skill paths, if applicable]

Stage 2 audit: [audit report, if available]
Optional coordinator candidate: [existing coordinator SKILL.md or design file, if available]

Assess only meaningful standalone and producer-consumer boundaries.
Where justified, compare direct handoffs with optional coordinator routing.
Carry forward evidence and human approval boundaries.
Propose IC-xx contracts and D-xx decisions; do not implement changes.
```

Omit inapplicable lines; the template is **not** a fixed two-skill or three-skill workflow. The coordinator candidate is a distinct optional **source of evidence**, never automatically an additional component to deploy.

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

Use `implementation_alignment_review: on` to assess actual implemented instructions and handoff references. It works after clearing chat or when approval records are unavailable. It is **read-only instructions, not a script**: no edits, skill invocation, test execution or runtime certification.

### Three adaptive review modes

| Available evidence | Automatic mode | Source-level verdicts |
| --- | --- | --- |
| Exact design plus verified human approval | Approved Design Alignment | ALIGNED / PARTIALLY ALIGNED / MISMATCH / NOT VERIFIED |
| Independent specific proposal, approval unverified | Provisional Design Alignment | CONSISTENT WITH PROPOSAL / PARTIALLY CONSISTENT / MISMATCH (against proposal) / NOT VERIFIED |
| Current implementation/source only | Source-Based Integration Assessment | DOCUMENTED / INCONSISTENT / GAP IDENTIFIED / NOT VERIFIED |

No new flag. Mixed scopes use the appropriate basis per term. Missing approval is reported as **APPROVED BASELINE NOT VERIFIED** but does not stop the review. Implementation/diffs cannot establish approval or serve as their own independent design baseline.

### What to provide

- **Target implementation:** Paths to changed/current skill files, handoff references and relevant config/code; branch, revision/diff when available.
- **Scope:** Actual skills or connections.
- **Optional design evidence:** Independent exact IC/D version and explicit approval, or a specific proposed design. If absent, use available source. Stage 1/2 evidence may also be supplied.

### Copyable invocation

```text
Use skill-integration-contracts on:
- skills/first-skill
- skills/second-skill

implementation_alignment_review: on
```

Optionally supply the revision/diff and approved or proposed design path. No need to preserve prior chat or repeat report instructions.

### How to read the result

All modes use the same **five-section report**:

1. **Review Scope & Approved Baseline** — mode, evidence basis, actual source revision, approval status and limits.
2. **Contract Alignment Coverage** — source-backed table with mode-specific verdicts; source-based review examines documented behavior, mutual consistency and material gaps, not invented approved clauses.
3. **Material Gaps & Evidence Limits** — actual contradictions, gaps and uncertainties; absent approval is not itself a source defect.
4. **Next Stage & Iteration Handoff** — proposed Stage 4 corrections, separate Stage 3 clarification/approval when needed, and scoped Stage 5 validation.
5. **Stage 5 Candidates — NOT EXECUTED** — visible explanation, four practical steps and named Given–When–Then cards, even without approved baseline when evidence justifies them.

A documented behavior, provisional consistency, or ALIGNED — DOCUMENTED SOURCE verdict does not prove runtime execution or permission enforcement.

**Reading Section 5:** Each justified V-xx has a descriptive title, purpose/guarantee with explicit approved/proposed/documented basis, validation level, Given — Test setup, When — Execution, Then — Assertions, Expected evidence, and Status: NOT EXECUTED. Preserve actual prior IDs when relevant. Check coverage of scoped expectations; start with the smallest useful level and prepare controlled cases in a separately authorized Stage 5 task (Evaluate Skill where supported or another controlled test). Collect evidence before PASS/FAIL/INCONCLUSIVE. Missing approval does not prevent candidate preparation or separately authorized testing of documented/proposed expectations, but those tests cannot establish approved-contract compliance. No automatic execution, approval or deployment authority follows.

**Iteration loop:** Correct approved implementation mismatches against unchanged design in Stage 4; changes to intended agreement need Stage 3 review and new approval. In provisional/source review, clarify actual contradictions or ownership gaps and propose the smallest correction. Recover or independently approve a design if authoritative alignment is needed. Save exact approved IC/D terms and approval as durable records for future reviews; recommended, not mandatory.

**Interaction with other options:** `quality_review`, `review_lenses` and `industry_framework_review` remain design-mode options. Alignment uses only its five-section report. Run a separate design review to revise/approve a contract.

**Detailed procedure and reusable report:** [references/implementation-alignment-review.md](references/implementation-alignment-review.md).

## How to read the report

The seven stable headings are **Executive Summary**, **Current Skill Boundaries & Stage 2 Evidence**, **Proposed Interaction & Ownership Map**, **Proposed Integration Contract Cards**, **Cross-Cutting Guarantees & Trade-offs**, **Human Decision Ledger & Open Questions**, and **Stage 4 Implementation Handoff & Stage 5 Candidates**.

**Section 3 — Required ASCII interaction map for meaningful integrations:** The interaction map describes **the actual scoped relationship**, not a replacement for the broader workflow. Add a conditional feedback route **only if** inspected sources, meaningful findings or the intended design support returning a material issue to an owner; otherwise omit the loop. Explain why independent skills enable flexible branching/re-entry **only when their documented or proposed boundaries justify that point**—never claim that a genuinely required dependency is optional. A coordinator or repeated execution is not implied. Contracts, real prerequisites and human authority remain explicit. Other material patterns (such as a simple handoff, conditional branch, human gate, justified sequence or optional routing) may receive the same concise **what happens → who decides → why → trade-off** explanation when grounded in the selected skills. **Section 4** turns applicable pattern behavior into specific IC-xx guarantees; **Section 5** covers significant cross-cutting trade-offs without duplicating the cards. **Whenever a meaningful documented or proposed cross-skill integration is in scope, Section 3 must include a compact ASCII interaction map in a fenced `text` block—not Mermaid—even for a simple one-way handoff.** Prose explains the map rather than replacing it. Show optional/required paths, applicable owners, approval gates and feedback branches; omit unsupported return paths, not the required map. A standalone-only map without a meaningful cross-skill connection remains optional when useful; if no meaningful connection is established, state that rather than inventing one. No compulsory pattern checklist or invented orchestration. See [Section 3's conditional example](references/report-template.md#3-proposed-interaction--ownership-map) and the [pattern explanation guide](references/contract-design-guide.md#explaining-relevant-interaction-patterns).

**Section 4 — Explain before specifying (junior-friendly):** Each IC-xx card leads the reader from the concept to the exact agreement:

- **A. Understanding the proposed integration** — what is proposed, why it matters, and the problem it solves.
- **B. How it would work in practice** — a short, clearly hypothetical walkthrough when it adds understanding; optional ASCII only when a material route is clearer that way. Omit B when the concept is already clear.
- **C. Technical contract** — precise applicable guarantees organized by six stable contract dimensions, with short plain-English questions, concise subfield bullets, and context-specific explanations of technical terms.
- **D. Evidence and decisions** — distinguish documented behavior and Stage 2 evidence from the proposed changes and unverified enforcement; include direct links, decision dependencies and status.

This is a reading hierarchy inside Section 4, not extra report stages. Keep simple cards compact, avoid repeating the audit or walkthrough, and retain engineering rigor. See the [Section 4 template and example](references/report-template.md#4-proposed-integration-contract-cards).

**Section 4C — Consistent engineering vocabulary:** Use only applicable dimensions, in the following order and with their original numbers (skip irrelevant headings):

- **1. Interface — What do we exchange?**
- **2. Behavioral Guarantees — What must be true before, after and throughout?**
- **3. Ownership, Security & Authority — Who controls what?**
- **4. Reliability & Feedback — What happens when something goes wrong or needs revision?**
- **5. Observability & Traceability — How can we understand and trace what happened?**
- **6. Compatibility & Evolution — How do we preserve compatibility as things change?**

Use lightweight RFC-inspired **MUST / MUST NOT / SHOULD / MAY** wording for meaningful mandatory, prohibited, recommended or optional terms respectively, without overstating approval or runtime enforcement. Preconditions (before), postconditions (successful result) and invariants (what stays true at relevant boundaries) sit together under Behavioral Guarantees. Avoid duplicate guarantees, invented fields, required upstream skills or unnecessary telemetry. The six dimensions are a communication vocabulary, not a new checklist or mandatory schema.

**Self-contained dependencies:** **Dependencies** and **Status** are separate. State each prerequisite or decision in plain English and why it affects the contract; distinguish optional context from required prerequisites. A D-xx decision reference includes its title/question and maps to the same decision in Section 6, which links back to the affected IC-xx. Never use an unexplained key. If no dependencies are identified, say **None identified**. Contract approval status remains independent.

**IDs:**
- `C1–C6` = considerations in the Stage 2 audit.
- `F-xx` = findings from that audit, used only if an actual report supplies them.
- `IC-xx` = newly proposed integration contract cards.
- `D-xx` = human design decisions and their statuses.
- `V-xx` = named validation scenario candidates for separately authorized Stage 5 work; their IDs do not define fixed test categories.
- `CQ-xx` = optional Stage 3 Contract Quality Review questions.

**Status guidance:** PROPOSED means suggested, CONDITIONAL — NEEDS HUMAN means dependent on an unresolved ownership/permission decision, APPROVED — DESIGN ONLY means a human explicitly accepted an exact design version. None imply that integration is implemented or the agent actually ran.

## Handoff artifact design — Stage 3

Stage 2 investigates existing skills and proposes responsibility clarifications; **Stage 3 decides the handoff filenames, folder placement and local ownership**. Section 7 carries the concrete artifact plan into Stage 4 after human design approval.

- Keep essential standalone behavior and concise handoff rules in each skill's own `SKILL.md`. Plan local references for substantial handoff details, or when the user requests separate files for affected skills; a simple connection can otherwise remain in `SKILL.md` with a reason.
- Use `references/<source>-to-<destination>-handoff.md` for a single direction; use a descriptive `-handoffs.md` suffix for a genuinely multi-transition file. Reverse feedback gets its own direction when separately documented.
- Inspect existing references, reuse suitable files, and avoid mandatory shared files or cross-skill imports. Each participating skill owns its own instructions. Keep producer/consumer role-specific content consistent with the associated IC-xx.
- In Section 7, provide owner, path, CREATE / UPDATE / REUSE / NO NEW FILE, linked IC-xx, role, contents, local link changes and design approval status. Use an illustrative directory tree when useful.

For example, when separate files are justified or requested:

```text
skills/
  skill-a/
    SKILL.md
    references/
      skill-a-to-skill-b-handoff.md
  skill-b/
    SKILL.md
    references/
      skill-a-to-skill-b-handoff.md
      skill-b-to-skill-a-handoff.md  # only if reverse feedback applies
```

These are illustrative, proposed paths. Existing files must be inspected before reuse, revision or a proposed rename. **Stage 3 does not create folders or files, edit skills or implement routing.** Stage 4 implements the approved plan.

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
