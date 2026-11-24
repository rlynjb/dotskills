---
name: skill-integration-contracts
description: "Stage 3 read-only integration contract design for AI agent skills, plus optional post-Stage-4 implementation alignment review against explicitly human-approved IC-xx/D-xx contracts. Draft traceable handoff guarantees and decisions, or inspect changed skill source for alignment, mismatches and next-stage routing. Does not edit skills, invoke agents, execute tests, implement integration or grant approval."
---

# Skill Integration Contracts — Stage 3

## Purpose and boundaries

Act as a senior software engineer helping a developer design **how independently useful skills may connect**. This is **Stage 3 — Integration Design** in the five-stage engineering planner. Stage 2 ([Skill Responsibility & Overlap Audit](../skill-responsibility-overlap-audit/SKILL.md)) investigates what skills currently own; **this skill proposes the agreements their connection should satisfy**, explains why, and collects decisions for human review. It is domain- and harness-agnostic; do not assume any fixed PRD, ticket or sprint workflow.

Use when asked to define handoff contracts, interface guarantees, feedback/error boundaries, human approval requirements, or an optional coordinator's limited routing agreement. Support **one standalone skill**, a **single actual connection**, or an **entire approved/intended workflow**. A Stage 2 audit is helpful but not mandatory.

**This skill owns:** in **default design mode**, read-only evidence review; proportional interface, behavior, trust, reliability, observability and compatibility agreement proposals; lightweight IC-xx cards, D-xx human decisions, and a Stage 4 handoff. In **optional implementation alignment mode**, a post-Stage-4, read-only comparison of **specific approved IC-xx/D-xx terms** against updated skill source and a routed fix/validation handoff.

**This skill does not own:** changing target `SKILL.md` or scripts, selecting product/technical scope for an owner, installing a coordinator, invoking other skills, executing agents/tests, publishing results, creating Jira tickets, or granting runtime permissions. **Stage 4 implements** human-approved designs; **Stage 5 tests** actual runtime behavior. Even an ALIGNED source-level review is **not** proof that host permissions, dispatch or workflow behavior were exercised.

## Inputs and scope

Inspect what is accessible and authorized:

- **Targets:** one or more target skill directories, `SKILL.md` files, links or supplied documents, plus referenced materials relevant to the selected connection.
- **Optional Stage 1 architecture:** phases, intended route, existing feedback paths and human gates.
- **Optional Stage 2 audit:** material `F-xx (Cx)` findings, affected skills, source links, proposed optional handoffs, unresolved ownership questions, evidence status, and reviewer responses.
- **Existing decisions and environment:** exact approved boundary wording if any, human decision maker when known, intended host/coordinator, existing contracts, known constraints and revisions.
- **Alignment-only inputs (when opted in):** the exact **human-approved** IC-xx/D-xx design and identifiable approval/version, actual changed/current skill source and relevant config/code, and revision/diff where accessible. An incomplete or unavailable approval baseline cannot be silently inferred from proposed text.

Identify target/revision/source and **what is documented versus proposed**. If a Stage 2 report or a target source is missing, do a bounded read-only discovery of the accessible skills; mark unresolved ownership and evidence gaps **UNVERIFIED / NOT ASSESSED**. Do not fabricate `F-xx` IDs, approvals, interfaces, execution traces, or hidden code. If a critical owner/permission decision is unresolved, you **may still draft a conditional example**, but never finalize it.

Use the shared [Senior Engineer → Junior Developer Communication Guideline](../../docs/senior-engineer-mentoring-communication.md). Explain every material contract by **what it guarantees → why the consumer needs it → what can go wrong → the smallest design choice and trade-off**. Keep junior-friendly definitions brief and do not repeat a lesson for every routine field.

Read [contract-design-guide.md](references/contract-design-guide.md) for contract dimensions, evidence and decision rules. Read [report-template.md](references/report-template.md) for the exact seven-section layout. Read [contract-quality-review-questions.md](references/contract-quality-review-questions.md) **only when contract quality review is explicitly requested**. Read [review-lenses.md](references/review-lenses.md) **only when Stage 3 conference lenses are requested**. Read [industry-framework-review-lenses.md](references/industry-framework-review-lenses.md) **only when optional Stage 3 industry review is requested**. Read [implementation-alignment-review.md](references/implementation-alignment-review.md) **only when `implementation_alignment_review: on` is explicitly requested**, using its separate output format instead of the normal design template. References are not evidence of target behavior.

## Optional Contract Quality Review — CQ-01–CQ-06

**Default: off.** The normal four-step Stage 3 design still drafts proportional `IC-xx` contracts and `D-xx` human decisions without an extra review. Do not automatically load CQ questions.

- `quality_review: on` or `contract_quality_review: on` explicitly enables **all six Stage 3 contract-quality questions** from [contract-quality-review-questions.md](references/contract-quality-review-questions.md). These are **CQ-01–CQ-06**, not Stage 2's Q-01–Q-10.
- `quality_questions: CQ-03,CQ-06` (or an equivalent explicit subset) evaluates **only** those CQ IDs, in question order. Review the **proposed IC-xx cards**, not the target skills themselves.
- After contract drafting and material cross-cutting analysis, add **Contract Quality Review Coverage (optional)** inside **report Section 5 — Cross-Cutting Guarantees & Trade-offs**, immediately **before Section 6 — Human Decision Ledger**.
- Format as a compact Markdown comparison table: first column **Contract-quality question** with each selected CQ-xx ID, title and **full canonical question text**; remaining columns are the actual **IC-xx contract cards**, not skills. Compare one or two IC columns at once; group additional contracts and repeat selected CQ rows. Keep full arguments, revisions, and decisions in the existing vertical IC and D cards, **not** giant table cells.
- Each cell has a concise `CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE` **design assessment**, a source/design reason and actual `IC-xx`, `D-xx` and supplied Stage 2 `F-xx (Cx)` references when relevant. `CLEAR` means the proposal is clear, **not approved, implemented, enforced or tested**. A material issue should improve the existing IC wording or link to an actual D-xx choice; never invent a second findings-ID series.
- Do not require an unavailable Stage 2 report, fabricate source fields, make optional context mandatory, create one IC per CQ, prescribe the agent's internal reasoning, or force a coordinator. When no meaningful IC exists, explain and omit an empty coverage table. Human design approval remains separate.

## Optional Stage 3 conference Review Lenses

**Default off.** Read [review-lenses.md](references/review-lenses.md) only when `review_lenses: relevant` or an explicit named subset is requested. Review **proposed IC-xx contracts**, not target skills independently. A lens-only run never activates the CQ-01–CQ-06 checklist.

- `review_lenses: relevant`: select only applicable lenses based on inspected contract/target evidence, and explain briefly why. `review_lenses: [context-engineering, security-and-trust]` or another named list: use only the requested lenses, marking individual ICs NOT APPLICABLE with reason when needed. Supported lens names are `context-engineering`, `security-and-trust`, `reliability-and-workflow`, `evaluation-and-observability`, `lifecycle-and-portability`.
- In **report Section 5**, after normal cross-cutting discussion and after optional **Contract Quality Review Coverage** if CQ review is enabled, add **Review Lens Coverage (optional)**. Compare selected lenses against the real IC-xx cards in a compact Markdown table: first column **Review lens & diagnostic questions** (lens name, complete reference questions, mapped contract dimensions), then **one or two IC-xx contract columns**. For three or more contracts, group in pairs and repeat selected rows. Don't add an eighth numbered section.
- **Contract cells:** concise `CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE` design assessment, relevant inspected target source link or evidence limit, and real IC-xx/D-xx/Stage 2 F-xx (Cx) pointers only when material. Explain required changes in the existing IC card and human choices in the D ledger; do not create second findings IDs. With lens-only mode show contract-dimension mappings, **not unexplained CQ-xx references**.
- **Conference Sources & Further Reading (optional):** Immediately under the lens coverage, provide a compact Markdown table with **Lens / Topic | Session title & speaker | PDF | YouTube (when matched)**. Include actual direct links from [review-lenses.md](references/review-lenses.md) for the selected lenses (ideally 1–3 relevant sources per lens). These source links must appear in the **generated result**, not only in the skill reference file. No fabricated video links: where the saved matching index has no established recording, link the PDF and show `—` for video.
- **Evidence boundary:** Conference takeaways offer reading and design perspective, **not evidence the target skill implements a guarantee**, nor official AAIF/MCP requirements. Use inspected SKILL.md and actual supplied audits for factual claims. The saved conference YouTube/PDF map establishes video title/speaker matching; it does not prove the video was watched. Never treat CLEAR as approved, implemented or runtime-tested.
- **Minimality:** Preserve standalone skill paths and human approval gates; do not force coordinator dispatch, telemetry, schema fields or versioning machinery simply to satisfy a conference lens. If `relevant` selects none, say why and omit the empty lens/source tables.

## Optional Stage 3 Industry Framework Review

**Default off.** This is a third, independent review perspective for **proposed IC-xx integration contracts**, not another design step. Read [industry-framework-review-lenses.md](references/industry-framework-review-lenses.md) only when explicitly requested.

- `industry_framework_review: relevant` selects only frameworks justified by the current IC-xx proposals; explain applicability, and omit empty tables if none apply.
- `industry_framework_review: on` considers all five proportionately, marking truly inapplicable frameworks NOT APPLICABLE.
- `industry_frameworks: [aws-agentic-ai-lens, cmu-sei-atam]` considers **only named IDs**, even if `on` or `relevant` is also set. Other names: `iso-25010`, `nist-ai-rmf`, `owasp-agentic-top10-2026`.
- After contracts are drafted, append **Industry Framework Review Coverage (optional)** in report **Section 5**, after any requested CQ review and conference review with source readings. The first table column contains each selected framework's **full adapted Stage 3 questions and mapping to contract dimensions**; remaining columns assess real **IC-xx** cards, *not the target skills*. For three or more contracts, repeat selected questions in groups of at most two IC columns.
- Cells contain a concise `CLEAR / NEEDS CLARIFICATION / NEEDS HUMAN / NOT VERIFIED / NOT APPLICABLE` **design assessment**, inspected source/evidence limitation, and actual IC-xx, D-xx and supplied Stage 2 F-xx (Cx) references where material. Reuse the existing IC proposals and D human decisions for fixes; do not create another issue ID scheme or duplicate findings. CLEAR does not mean APPROVED, IMPLEMENTED, TESTED or compliant.
- Immediately after industry coverage, include **Official Industry Framework Sources & Further Reading (optional)** with `Framework / type | Topic or official section | Publisher & version | Official URL`, using direct links from the reference for only selected frameworks. Industry sources provide design perspectives, not evidence that the targets behave correctly.
- Treat the sources distinctly: ISO/IEC 25010 is an international product-quality standard; AWS Agentic AI Lens is vendor guidance; NIST AI RMF is voluntary AI-risk guidance; CMU SEI ATAM is an architecture-evaluation method; OWASP Agentic Top 10 is community security guidance. These are **adapted design questions**, not certification or a completed formal assessment.
- Industry-only mode does not enable CQ or conference reviews. Preserve order **core cross-cutting → CQ (if enabled) → conference lenses/sources (if enabled) → industry frameworks/official sources (if enabled)**, all in Section 5. Keep the four SDI steps, seven report sections and human decision gate. Never force a coordinator, mandatory cross-skill dependency, runtime controls, telemetry or elaborate schemas to satisfy a framework. Stage 4 implements; Stage 5 tests.

## Optional Implementation Alignment Review — after Stage 4

**Default: off.** The existing contract-design workflow stays unchanged. Explicitly set `implementation_alignment_review: on` to switch to a **read-only post-implementation comparison** against **approved** IC-xx and D-xx terms. This is still the Stage 3 *skill* assessing alignment to its design; it does not make implementation part of Stage 3 or replace Stage 5 runtime validation.

- **Load [implementation-alignment-review.md](references/implementation-alignment-review.md)** for the four-step source-comparison procedure, verdict definitions, five-section alignment report and example. **Do not rerun the default seven-section design report** in alignment mode or rewrite the approved baseline.
- **Mandatory approval baseline for authoritative verdicts:** Identify exact IC-xx/D-xx wording, explicit human approval of that version and scope, and the inspected current source/revision. If approval or exact wording cannot be established, output **APPROVED BASELINE NOT VERIFIED** and the missing input; an optional provisional comparison must never be reported as alignment to an approved design. Approval of one D-xx doesn't approve another.
- **Source comparison:** Read the changed/current `SKILL.md`, relevant references, configs or code and base/head diff **when available**, rather than relying on a claim that changes were implemented. Match each material approved guarantee to actual source links and assess **ALIGNED / PARTIALLY ALIGNED / MISMATCH / NOT VERIFIED**. With no diff, state that only current source content was assessed.
- **Evidence boundary:** `ALIGNED` means the specific approved guarantee is represented in inspected source at a disclosed evidence level; it does **not** prove runtime enforcement, actual automatic skill dispatch, successful evaluations, approval to merge or deployment readiness. Missing traces alone do not make a documented source-aligned clause a defect.
- **Stage routing:** If a source change is incomplete or contradicts an approved IC, recommend the **smallest Stage 4 correction** and rerun alignment against the same approved design. If the **design itself** needs revision, route to a separate Stage 3 IC/D revision and **new human approval** before Stage 4. If source aligns but runtime behavior remains unknown, propose proportionate **Stage 5 validation**, NOT EXECUTED.
- **Independent modes:** CQ, conference lenses and industry frameworks remain **design-mode-only** options. If supplied together with alignment mode, perform **alignment only** and note that the design-mode checks weren't run; use a separate invocation to redesign contracts. Don't create duplicate F/IC/D identifiers or add an eighth section to the default report.
- **No script or writes:** This is implemented as skill/reference **instructions**, not executable tooling. Never edit targets, run tests, invoke connected skills or claim behavioral PASS in this review.

## Four-step integration-design procedure (aligned with SDI)

### Step 1 — Scope, baseline and unresolved decisions

- Identify the user goal, which connection(s) matter, each skill's **standalone** entry and result, and existing vs desired links. Do not force every pair of skills into a contract.
- Bring forward **material Stage 2 findings by F-xx (Cx)** when supplied. Verify linked source evidence/revisions if accessible; record changed or inaccessible evidence honestly.
- Separate **DOCUMENTED** instructions, **OBSERVED** supplied runtime results, **PROPOSED** requirements and **APPROVED DESIGN** decisions. No approval follows from a recommendation or from a passing check.
- Identify essential human ownership/authority conflicts before claiming an integration path is settled. Preserve them as questions if not resolved.

### Step 2 — High-level interactions and responsibility boundaries

- Map each **actual intended producer → consumer** connection and any optional reverse feedback, plus each skill's standalone entry. Give a small ASCII/Markdown diagram only when it clarifies branching. **A local interaction map is not a replacement for an existing broader workflow architecture**; name its scope rather than inventing or showing every other skill.
- Assign each **decision/result a proposed owner**, identifying who produces, consumes, verifies and approves. Distinguish separate decisions from shared input context; legitimate overlap is not automatically a problem.
- If a material review finding may change an upstream artifact, map a **conditional feedback route**: what finding triggers the return, which authorized owner decides, what can be revised **only after approval**, and whether to revisit the affected skill or continue forward. **No issue or no authorized change → no mandatory return loop**. Never imply automatic reruns, approvals or dispatch.
- Explain briefly **why standalone skills matter** in the interaction map: they can start independently, use optional context when chosen, and revisit only the work that needs attention. This permits branching and iteration without forcing all skills through one rigid sequence. **Flexible routing still requires clear contracts** for required prerequisites, responsibilities, handoff evidence and human authority.
- Prefer a **manual or user-chosen optional handoff** over unnecessary coupled skill invocation. A producer's output being available does not make it a required prerequisite; never relax a genuinely required safety/data prerequisite.
- Evaluate a **separately invoked optional coordinator** only when routing/sequence/context-return complexity is evidenced or explicitly requested. Its contract covers routing and context passing, not component skills' substantive decisions. Do not assume a `SKILL.md` automatically dispatches another skill.

### Step 3 — Design the minimal applicable contracts

For each material connection, create a short **IC-01, IC-02, …** contract card following [report-template.md](references/report-template.md). For a standalone-only scope, draft that skill's **entry/exit contract** instead of inventing another skill.

Include only **applicable, decision-useful** guarantees:

- **Interface:** producer → consumer; optional/required trigger; required vs optional fields; what a successful output contains; source identity, revision and unresolved questions when needed.
- **Behavior:** preconditions (what must be true before use); postconditions (what the result guarantees if successful); invariants (what must stay true, such as original requirement and approval state). No field schema merely for completeness.
- **Trust and approval:** source provenance; who may propose, change, publish or approve; untrusted input; what requires actual host/tool enforcement rather than wording alone.
- **Failure and feedback:** unavailable/conflicting/malformed input; BLOCKED/NEEDS HUMAN vs safe standalone continuation; owner of returned questions and permission to resume; partial failure/fault isolation when applicable.
- **Observability and compatibility:** evidence/source links and minimal status/identity fields needed for later diagnosis; version/host assumptions and changes consumers can tolerate. Do not promise telemetry or runtime checks not present.

Mark **CURRENT DOCUMENTED** guarantees separately from **NEW PROPOSAL** and **UNVERIFIED ENFORCEMENT**. Do not write an exact implementation specification, dispatch algorithm, retries, security controls or additional artifacts unless the justified handoff requires it. **One meaningful contract per connection**, not one card for each generic quality category. If contract quality review is requested, assess the drafted cards with CQ-xx before presenting the human decisions, and put material clarifications/choices in the existing IC/D cards.

### Step 4 — Trade-offs, human decision gate and Stage 4 handoff

- Use `D-01, D-02, …` for material decisions (e.g., optional vs required handoff; who approves; coordinator vs simpler manual route); link each decision to `IC-xx` and original `F-xx (Cx)` if available.
- Explain your recommended minimum option, why it helps, alternative and practical downside. Give the user concrete choices: **APPROVE / REVISE / REJECT / DEFER**, with exact wording for proposed terms.
- Default all new contracts/decisions to **PROPOSED**. If a required owner/boundary is unresolved, mark dependent contracts **CONDITIONAL — NEEDS HUMAN**; do not present them as adopted.
- Only a human's **explicit approval of a specific, fully shown design version** can mark it **APPROVED — DESIGN ONLY**. Approval is not repository implementation, tool permission, management authorization or runtime verification. Changed boundaries reopen dependent contracts.
- In Section 7, list the *smallest* approved or still-conditional changes that Stage 4 could implement, affected skill-local files and a few relevant Stage 5 candidate checks (`V-xx`), clearly **NOT EXECUTED**. Never edit target files or claim a test ran here.

## Output contract — seven stable sections (default design mode only)

**Alignment-only exception:** `implementation_alignment_review: on` uses the **five-section implementation alignment report** in [implementation-alignment-review.md](references/implementation-alignment-review.md) instead of the seven design sections below. All existing design-mode headings remain stable.

Follow [report-template.md](references/report-template.md) with these headings, in order:

1. **Executive Summary** — goal, scope, key decision and evidence limits.
2. **Current Skill Boundaries & Stage 2 Evidence** — compact side-by-side source-backed inputs/responsibilities/outputs; `F-xx (Cx)` trace links only when real.
3. **Proposed Interaction & Ownership Map** — scoped connections, standalone paths, conditional feedback/owner-approved revision and selective re-entry where applicable; briefly explain flexibility without weakening contracts or human gates, and evaluate coordinator choice only when justified.
4. **Proposed Integration Contract Cards** — vertical `IC-xx` cards with evidence, minimal guarantees, failure/approval/feedback and status; only actual meaningful connections.
5. **Cross-Cutting Guarantees & Trade-offs** — consolidate material trust, reliability, observability and compatibility issues; when requested, append CQ coverage, conference Review Lens Coverage and sources, and Industry Framework Review Coverage and official sources, all within this section.
6. **Human Decision Ledger & Open Questions** — `D-xx` decisions, recommendation, trade-off, explicit status and question requiring human confirmation.
7. **Stage 4 Implementation Handoff & Stage 5 Candidates** — exact proposed changes/owners, dependencies and conditional validation ideas; no execution.

**Formatting:** A small side-by-side Section 2 table is appropriate for two or three skills; keep exact contract cards and decision rationale in **vertical Markdown bullets** with one field per line, never enormous cells or HTML breaks. The optional Section 5 CQ, conference lens and industry framework coverage tables compare **contracts**, not skills. When lenses are enabled, also list presentation topic, title, speaker and direct PDF/verified matched-video links. For larger workflows group comparisons; for one skill show a vertical profile. Use direct links to inspected source paths/lines when possible; never create an evidence-key table.

**IDs and statuses must not collide:** `C1–C6` are **Stage 2 considerations**, `F-xx` are **Stage 2 findings**, `IC-xx` are **Stage 3 contracts**, `D-xx` are **Stage 3 human design decisions**, and `V-xx` are **proposed Stage 5 checks**, and `CQ-xx` are **optional Stage 3 contract-quality questions**. Reference only IDs that exist in the report; do not infer that a contract is approved, implemented or tested.

**One-pass design default:** Present a complete, minimal proposal and all material options in the first design report, even if human decisions are missing. Ask for approval/revision **after** showing the proposal. Do not start modifying targets when a user approves the design; that is separate Stage 4 work.

## Completion boundary

**Design mode:** Deliver a traceable integration design, not a running integration. Stop with human decisions and a Stage 4 handoff. The human may approve, revise, reject or defer specific D-xx/IC-xx proposals.

**Implementation alignment mode:** Deliver a source-backed comparison against **specific approved IC-xx/D-xx terms** and route material differences to Stage 4 correction, separate Stage 3 redesign/approval, or Stage 5 verification. A missing approval baseline blocks an authoritative alignment verdict. Never modify files, execute the workflow or fabricate runtime evidence.
