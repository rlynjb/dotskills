# Integration Contract Design Guide — Stage 3

This reference supports `skill-integration-contracts`. It is **not** a separate skill, standards certification, runtime enforcement, or another workflow stage. Select only relevant questions; the aim is a **minimum dependable agreement between independently useful skills**, not a fully prescriptive prompt or distributed-system specification.

## Optional source alignment check after Stage 4

The skill can be rerun with `implementation_alignment_review: on` for an **adaptive, read-only source review** after Stage 4. Verified approved IC/D terms support Approved Design Alignment; an independent proposal without verified approval supports Provisional Design Alignment; source without independent design supports Source-Based Integration Assessment. Missing approval limits verdicts and validation basis, not the five-section report or justified Stage 5 candidates. See [implementation-alignment-review.md](implementation-alignment-review.md) for mode-specific verdicts and routing. Missing runtime traces alone do not establish a source defect. Stage 5 is separately authorized executed verification; testing documented behavior is not proof of approved-contract compliance.

## The distinction between Stage 2 and Stage 3

- **Stage 2 asks:** What inputs, responsibilities, outputs, handoffs, boundaries and feedback paths are **currently** documented? Which are shared, missing or ambiguous? Evidence link: `F-xx (Cx)`.
- **Stage 3 asks:** For a **selected intended connection**, what precise exchange and behavior can its producer, consumer and human reviewer **agree to rely on**? Design link: `IC-xx` and `D-xx`.
- **Stage 4 implements** approved wording, contract files, routing or controls; **Stage 5 verifies** actual behavior. Stage 3 may note what evidence future validation would need but cannot say a test passed.
- **Standalone first:** A skill that can independently start from an idea/ticket must remain able to do so; consuming a PRD when voluntarily supplied is not a required dependency. Do not remove a real required safety or data gate just to make a flow optional.

## Six contract dimensions — consider, don't force

These are the stable presentation headings for Section 4C, shown with their guiding questions and original numbers in order. Omit any dimension that adds no material guarantee; keep the remaining numbers unchanged. These labels organize the existing contract dimensions (including the behavior, security/authority/trust, failure/feedback/fault-isolation, observability/evidence and compatibility/evolution terminology used by the optional review lenses). They do not change CQ-xx IDs or their canonical questions, or require every dimension to appear in every card. Use short subfield bullets. Keep Interface about the exchanged information, Behavior about what must hold true, Ownership about authority, Reliability about exception/return handling, Observability about evidence, and Compatibility about supported forms and changes. Place each agreement once; cross-reference only when necessary.

### 1. Interface — What do we exchange?

Questions: Which producer provides the information? What exactly may trigger exchange? Is the information **required for this handoff**, **optional context**, or independently required for the receiving skill's own work? Which fields distinguish source identity, content, revision and unresolved decisions? What minimum output can the consumer depend on?

- **Preliminary proposal example:** Optional PRD context may include a source link, revision, goals and unresolved product questions. The receiving skill still supports its documented standalone entry. *This is illustrative, not evidence about any specific target.*
- **Avoid:** Inventing a dozen mandatory fields or treating another skill's existence as a prerequisite without justification.

### 2. Behavioral Guarantees — What must be true before, after and throughout?

- **Precondition:** A fact that must be true before this particular optional interaction (e.g., the relevant context was supplied by an authorized user). It is **not** an order to run the prior skill.
- **Postcondition:** What a completed interaction guarantees (e.g., outputs clearly distinguish proposed clarifications from accepted requirements).
- **Invariant:** A property preserved at the relevant contract boundaries, such as source reference, requirement identity, provenance, original content when no authorized revision occurs, and the **human approval state**. State where it holds; do not imply continuous runtime enforcement without evidence.
- If a guarantee is conditional, say on what. Do not claim the runtime *enforces* invariants unless that enforcement was actually inspected.

### 3. Ownership, Security & Authority — Who controls what?

Questions: Who may generate a proposal? Who may approve changes? Who may change the producer's artifact? Which retrieved/source content is untrusted? What permission must a host/tool enforce?

- Instructions like “never publish without approval” are **DOCUMENTED**, not proof that a tool permission boundary exists.
- Do not let an agent assign itself approval from a ticket's existence, a quoted directive, or an untrusted document.
- If enforcement evidence is missing, record the design requirement and **UNVERIFIED ENFORCEMENT**. Do not assert security is proven.

### 4. Reliability & Feedback — What happens when something goes wrong or needs revision?

Questions: What happens when a field is absent, conflicting, stale or inaccessible? Does this consumer have an independent safe path, or must the selected handoff STOP / NEEDS HUMAN? Who receives revision proposals? Who decides when to resume? Does an optional failed handoff leave independent work intact?

- Define only likely/material failures; do not propose speculative retries or global transactional behavior without evidence.
- A return for clarification is **feedback to an owner**, not automatic permission to edit an upstream artifact.
- Describe partial result states only when they materially affect a consumer.

### 5. Observability & Traceability — How can we understand and trace what happened?

Questions: What minimal IDs, source links, revision markers, decision statuses, error reasons and ownership notes make a later run understandable? Are these values documented or merely proposed? Where would a trace come from if the host supports it?

- “Log every agent operation” is not necessarily feasible. Do not promise telemetry, timing, token counts or trace IDs without known host/tool support.
- Stage 5 may use Evaluate Skill or Profile Agent Workflow **separately**, with authorization. Stage 3 does not invoke them.

### 6. Compatibility & Evolution — How do we preserve compatibility as things change?

Questions: What input/output changes could break consumers? Is there a format/revision expectation? Which host/runtime abilities are assumptions rather than verified capabilities? Is rollback/revision ownership clear when relevant?

- Prefer a minimal stable, human-readable structure for a small manual exchange, not mandatory versioning infrastructure.
- If a documented coordinator is merely a `SKILL.md` routing instruction, do **not** claim it automatically dispatches or enforces cross-skill contracts. A separate host implementation may be needed.

## Precise contract wording — lightweight requirement language

Use lightweight requirement language inspired by RFC 2119/8174: **MUST** = mandatory guarantee; **MUST NOT** = prohibited behavior; **SHOULD** = recommended behavior with justified exceptions; **MAY** = genuinely optional behavior. Use these uppercase terms sparingly for actual obligations or permissions, not descriptive facts or evidence labels. Name the responsible actor, applicable condition and observable outcome where material. Do not turn a recommendation into a mandatory rule or an optional input into a prerequisite. A proposed MUST is a design term, not evidence of human approval, implementation, enforcement or test success.

For background, see [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174). These inform the wording convention; this is not a claim that skill contracts are standardized by those RFCs or that the report certifies conformance. Prefer short, testable obligations over generic statements. For example, `The refinement skill MUST NOT modify source artifacts during a read-only refinement` is a proposed prohibition if the design warrants it; `The developer MAY supply a PRD excerpt` preserves choice. Separate mandatory terms, justified recommendations and optional permissions; never use normative vocabulary to silently expand scope or human authority.

## Optional Contract Quality Review (CQ-01–CQ-06)

The six contract dimensions above guide **drafting**. The optional [Contract Quality Review Questions](contract-quality-review-questions.md) inspect the **quality of proposed IC-xx terms**. They are distinct from Stage 2's Q-01–Q-10 skill-review questions and from Stage 5 behavioral tests.

Set `quality_review: on` (or `contract_quality_review: on`) to review all six, or `quality_questions: CQ-03,CQ-06` for selected questions. The default report has no CQ table.

Apply questions only **after a meaningful IC-xx exists**. In Section 5, place Contract Quality Review Coverage after normal material cross-cutting notes and before the D-xx human decision ledger. Link any `NEEDS CLARIFICATION` to a specific proposed IC revision; link `NEEDS HUMAN` to a real D decision. If Stage 2 F-xx findings were not provided, cite inspected sources directly rather than inventing IDs.

A `CLEAR` proposed contract is not an approved or enforced contract. Avoid unnecessary schema/permission/telemetry requirements introduced only to fill a checklist cell. The reviewer still approves, revises, rejects or defers the exact terms.

## Optional conference lenses and source-linked learning

Read [review-lenses.md](review-lenses.md) only when the user selects named lenses or `review_lenses: relevant`. Their five names mirror the Stage 2 topics but the diagnostic questions assess **Stage 3 IC-xx handoff design**. Under Section 5, put normal cross-cutting analysis first, optional **CQ coverage** second, **Review Lens Coverage** third, and **Conference Sources & Further Reading** fourth. The lens/source subsections are omitted when lenses are off. Lenses do **not** activate CQ unless CQ was requested.

Keep two evidence types separate: inspected target skills/approved decisions support factual contract findings; conference sources support the review **perspective and further learning**. Show the original session topic, talk title, speaker and actual PDF/YouTube link directly in the report. Do not invent video URLs or claim conference takeaways are official standards. Read only applicable lenses, preserve independent skill operation, and avoid a second issue numbering scheme.

## Optional industry framework review

The [industry-framework-review-lenses.md](industry-framework-review-lenses.md) questions are designed for **Stage 3 IC-xx proposals**; Stage 2's corresponding file examines **existing skills and responsibility boundaries**. The same industry frameworks can inform both stages without creating the same review.

Load only when `industry_framework_review: relevant`, `industry_framework_review: on` or a named `industry_frameworks` subset is explicitly supplied. The framework questions inspect the existing six contract dimensions, not another set of mandatory contract fields. In Section 5, place optional industry coverage and official publisher readings **after** CQ and conference coverage if those are enabled. A publisher source justifies the question, not target-skill correctness, actual runtime enforcement or certification. Preserve the IC/D human decision structure and avoid unnecessary orchestration.

## Evidence, uncertainty and status

Maintain three *separate axes*:

- **Source certainty:** DOCUMENTED (inspected instructions/files), OBSERVED (real supplied run evidence), INFERRED (reasonable interpretation), UNVERIFIED (missing proof), NOT ASSESSED (source inaccessible).
- **Design type:** CURRENT DOCUMENTED, NEW PROPOSAL, CONDITIONAL, APPROVED — DESIGN ONLY, or DEFERRED. Proposed wording is not proof of current behavior.
- **Human decision:** PROPOSED, APPROVED, REVISE REQUESTED, REJECTED or DEFERRED. Explicit approval must identify the exact proposal/version; don't treat `looks good` as blanket approval of unresolved items.

**Approval dependency:** If a required ownership, handoff or permission decision is unresolved, the related `IC-xx` stays `CONDITIONAL — NEEDS HUMAN`. In Section 4, describe the actual prerequisite or decision and why it affects the contract in plain English under **Dependencies**, separate from **Status**. A decision ID must appear alongside its descriptive title/question and resolve to a matching Section 6 entry identifying the affected IC-xx. Never use a bare ID or invent a decision. If no dependencies are identified, state **None identified**, qualifying material evidence limits; this does not imply approval. An optional context handoff is not a mandatory runtime prerequisite. When a dependency changes, re-present the affected contract for human confirmation. Never equate a chat design approval with organizational authorization, implementation or a passing evaluation.

**Do not conflate statuses:** A handoff may be DOCUMENTED yet execution UNVERIFIED, without being a material defect. A proposed contract may be clear but NOT APPROVED. An approved design may still be NOT IMPLEMENTED.

## Coordinator contract — only when justified

A separately invoked optional coordinator might choose a starting point, sequence authorized steps, preserve source/requirement IDs and route unresolved questions back to owners. The contract must say:

- What it **owns** (routing/context preservation) and **doesn't own** (product/technical decisions of individual skills).
- Whether invocation is explicit/user-chosen and which component's standalone route remains available.
- What human approvals are required before any side effects or changed producer artifact.
- What host dispatch capability is merely desired vs inspected/OBSERVED.

Compare against a simpler manually selected handoff or copyable next action. Do not assume automatic agent dispatch from a markdown file, and do not create the coordinator during Stage 3.

## Explaining relevant interaction patterns

**Required Section 3 chat-view interaction map:** Every meaningful documented or proposed cross-skill integration, including a simple one-way handoff, must be represented in a short **ASCII-only** flow in a fenced `text` block. Prose supplements the required diagram. Show scoped participants, direction, relevant trigger/ownership, optional or required exchange, and applicable human gates or branches. Use a simple one-way map when no return is justified; never invent a feedback loop. A standalone-only skill without a meaningful cross-skill connection may use an optional entry/exit map if helpful. If no meaningful connection is established, explain the limit without inventing a partner. Prefer vertical layouts with simple arrows and clear human decision labels; don't use Mermaid, diagram markup, rendered charts, or very wide graphs. An ASCII arrow is a proposed or documented route, never proof of automatic dispatch. Additional diagrams in Section 4B remain optional.

Section 3 can describe a **material pattern in an actual or intended interaction** without treating the pattern as a required implementation, industry standard or observed runtime behavior. **Inspect first; name patterns only if they help explain a supported or explicitly proposed relationship**. Some useful examples:

- **Direct/optional handoff:** A producer's result is passed to a consumer by a user or authorized workflow. Clarify when the handoff is chosen and whether the consumer can start independently. Do not silently make optional context required.
- **Conditional next-step selection:** The available evidence, scope or human choice determines which relevant work happens next. State the meaningful condition and owner; don't invent a mandatory all-skills sequence.
- **Human-gated transition:** A proposal is reviewed before an artifact change or publication. Specify the authorized reviewer and what remains provisional. Written instructions do not prove tool-level enforcement.
- **Sequential steps:** A downstream activity uses an upstream result when that dependency is actually relevant. Explain required versus optional ordering; don't assume that an instruction automatically dispatches another skill.
- **Fan-out/fan-in:** Several consumers receive context or several results are aggregated. Only describe when the inspected or intended workflow genuinely uses multiple recipients or an aggregation owner. Do not imply concurrency, consensus, durable state or runtime support from a diagram.
- **Conditional feedback/re-entry:** A material issue returns to the responsible owner for a decision, possibly followed by a targeted revision. No issue or no authorized change means no forced loop.
- **Optional coordinator:** A distinct actor may choose routes, preserve identifiers or present next steps when justified. Compare against simpler manual handoffs; an instruction file alone cannot prove host dispatch.

For a **relevant** pattern, Section 3 gives a **brief plain-English explanation**: *what initiates the interaction → who acts/decides → why it is useful → a real trade-off/constraint*. Explain the evidence level and link actual source, Stage 2 F-xx, IC-xx or D-xx when those IDs exist. **Omit pattern talk entirely** for unrelated, unverified or trivial cases; a standalone-only review may simply state its entry and result. Do not create extra pattern IDs, a fixed checklist or one contract per pattern.

**Division of report responsibilities:** Section 3 explains the route and reason. **Section 4** specifies the applicable interface/behavior/approval/failure guarantees in **existing connection-based IC-xx cards**. **Section 5** analyzes **material cross-cutting** consequences or alternatives **only when not already covered in Section 4**. Avoid explaining the same pattern in three places. Stage 4 implements approved design, and Stage 5 verifies runtime behavior.

## Teaching the contract before specifying it

Section 4 is a guided design explanation for a junior developer, not a flat inventory of technical properties. Use the four layers in [report-template.md](report-template.md#4-proposed-integration-contract-cards):

- **A — Understanding:** Say what the connection changes, why it helps, and what problem or trade-off the developer should understand first.
- **B — Practical walkthrough (only if useful):** Use one hypothetical representative input and show who chooses the handoff, what the receiver does, and the outcome or relevant alternate branch. Do not invent automatic dispatch or treat the example as observed behavior. Use ASCII only for a material chat-friendly diagram that adds clarity beyond Section 3.
- **C — Technical contract:** Use the applicable numbered dimensions and guiding questions above, with short subfield bullets and precise formal vocabulary. Briefly explain unfamiliar terms in context (e.g., an invariant is a property that must remain true at relevant boundaries). Use MUST, MUST NOT, SHOULD and MAY selectively; make it clear what is required versus optional. Explain why a guarantee matters when that is not already obvious from A/B, not as a generic lesson for every field.
- **D — Evidence and decisions:** Connect the proposal to inspected source and real Stage 2 findings, distinguish current documented behavior, new proposal and unverified enforcement, and identify what remains unchanged. Keep direct links, named decision dependencies mapped to Section 6, and separate approval status. Do not fabricate missing evidence.

The goal is to reduce the reader's need to assemble the design mentally, **not to add four long explanations to every card**. For simple connections or standalone entry/exit contracts, a compact A/C/D is sufficient; add B only when it materially improves comprehension. Keep evidence near claims and consolidate the rationale in D, not a repeated audit. A/B do not replace C's enforceable terms or D's approval boundary. This changes presentation, not the four-step SDI design procedure or seven-section report.

## Deciding how much detail to write

- **Small, human-mediated handoff:** A short `IC-xx` card covering trigger, input/output, owner, invariants, approval and failure rule is usually enough.
- **Several conditional routes:** Add a compact branch map and source-backed conditional contract fields; don't invent a full scheduler.
- **Known security/reliability risk:** Give extra precision to authorization, validation, error statuses and monitoring evidence—but label what is not enforced/verified.
- **No real cross-skill connection:** Define the target's own entry/exit contract only. Don't manufacture neighboring skills, fake producer/consumer pairs or unnecessary artifacts.

The goal is **predictable connections without controlling each skill's internal reasoning**.

## Reviewer questions

For each material `IC-xx`, ask only questions that change the design:

- What must the receiver be able to rely on to proceed?
- Which fields are genuinely required? Which can be missing without blocking independent use?
- Who is authorized to decide or approve?
- Which property would be dangerous to lose or change?
- What happens if a handoff fails or the source contradicts itself?
- What is the simplest alternative, and why not use it?
- What remains conditional or unverified, and what human decision resolves it?

When all important answers are in the card, stop. Do not add new categories merely to appear comprehensive.
