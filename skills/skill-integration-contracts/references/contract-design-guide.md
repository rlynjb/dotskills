# Integration Contract Design Guide — Stage 3

This reference supports `skill-integration-contracts`. It is **not** a separate skill, standards certification, runtime enforcement, or another workflow stage. Select only relevant questions; the aim is a **minimum dependable agreement between independently useful skills**, not a fully prescriptive prompt or distributed-system specification.

## The distinction between Stage 2 and Stage 3

- **Stage 2 asks:** What inputs, responsibilities, outputs, handoffs, boundaries and feedback paths are **currently** documented? Which are shared, missing or ambiguous? Evidence link: `F-xx (Cx)`.
- **Stage 3 asks:** For a **selected intended connection**, what precise exchange and behavior can its producer, consumer and human reviewer **agree to rely on**? Design link: `IC-xx` and `D-xx`.
- **Stage 4 implements** approved wording, contract files, routing or controls; **Stage 5 verifies** actual behavior. Stage 3 may note what evidence future validation would need but cannot say a test passed.
- **Standalone first:** A skill that can independently start from an idea/ticket must remain able to do so; consuming a PRD when voluntarily supplied is not a required dependency. Do not remove a real required safety or data gate just to make a flow optional.

## Six contract dimensions — consider, don't force

### 1. Interface: What crosses the boundary?

Questions: Which producer provides the information? What exactly may trigger exchange? Is the information **required for this handoff**, **optional context**, or independently required for the receiving skill's own work? Which fields distinguish source identity, content, revision and unresolved decisions? What minimum output can the consumer depend on?

- **Preliminary proposal example:** Optional PRD context may include a source link, revision, goals and unresolved product questions. The receiving skill still supports its documented standalone entry. *This is illustrative, not evidence about any specific target.*
- **Avoid:** Inventing a dozen mandatory fields or treating another skill's existence as a prerequisite without justification.

### 2. Behavior: What must happen or remain unchanged?

- **Precondition:** A fact that must be true before this particular optional interaction (e.g., the relevant context was supplied by an authorized user). It is **not** an order to run the prior skill.
- **Postcondition:** What a completed interaction guarantees (e.g., outputs clearly distinguish proposed clarifications from accepted requirements).
- **Invariant:** What stays true throughout, such as source reference, requirement identity, provenance, original content when no authorized revision occurs, and the **human approval state**.
- If a guarantee is conditional, say on what. Do not claim the runtime *enforces* invariants unless that enforcement was actually inspected.

### 3. Security, authority and trust

Questions: Who may generate a proposal? Who may approve changes? Who may change the producer's artifact? Which retrieved/source content is untrusted? What permission must a host/tool enforce?

- Instructions like “never publish without approval” are **DOCUMENTED**, not proof that a tool permission boundary exists.
- Do not let an agent assign itself approval from a ticket's existence, a quoted directive, or an untrusted document.
- If enforcement evidence is missing, record the design requirement and **UNVERIFIED ENFORCEMENT**. Do not assert security is proven.

### 4. Failure, feedback and fault isolation

Questions: What happens when a field is absent, conflicting, stale or inaccessible? Does this consumer have an independent safe path, or must the selected handoff STOP / NEEDS HUMAN? Who receives revision proposals? Who decides when to resume? Does an optional failed handoff leave independent work intact?

- Define only likely/material failures; do not propose speculative retries or global transactional behavior without evidence.
- A return for clarification is **feedback to an owner**, not automatic permission to edit an upstream artifact.
- Describe partial result states only when they materially affect a consumer.

### 5. Observability and evidence

Questions: What minimal IDs, source links, revision markers, decision statuses, error reasons and ownership notes make a later run understandable? Are these values documented or merely proposed? Where would a trace come from if the host supports it?

- “Log every agent operation” is not necessarily feasible. Do not promise telemetry, timing, token counts or trace IDs without known host/tool support.
- Stage 5 may use Evaluate Skill or Profile Agent Workflow **separately**, with authorization. Stage 3 does not invoke them.

### 6. Compatibility and evolution

Questions: What input/output changes could break consumers? Is there a format/revision expectation? Which host/runtime abilities are assumptions rather than verified capabilities? Is rollback/revision ownership clear when relevant?

- Prefer a minimal stable, human-readable structure for a small manual exchange, not mandatory versioning infrastructure.
- If a documented coordinator is merely a `SKILL.md` routing instruction, do **not** claim it automatically dispatches or enforces cross-skill contracts. A separate host implementation may be needed.

## Optional Contract Quality Review (CQ-01–CQ-06)

The six contract dimensions above guide **drafting**. The optional [Contract Quality Review Questions](contract-quality-review-questions.md) inspect the **quality of proposed IC-xx terms**. They are distinct from Stage 2's Q-01–Q-10 skill-review questions and from Stage 5 behavioral tests.

Set `quality_review: on` (or `contract_quality_review: on`) to review all six, or `quality_questions: CQ-03,CQ-06` for selected questions. The default report has no CQ table.

Apply questions only **after a meaningful IC-xx exists**. In Section 5, place Contract Quality Review Coverage after normal material cross-cutting notes and before the D-xx human decision ledger. Link any `NEEDS CLARIFICATION` to a specific proposed IC revision; link `NEEDS HUMAN` to a real D decision. If Stage 2 F-xx findings were not provided, cite inspected sources directly rather than inventing IDs.

A `CLEAR` proposed contract is not an approved or enforced contract. Avoid unnecessary schema/permission/telemetry requirements introduced only to fill a checklist cell. The reviewer still approves, revises, rejects or defers the exact terms.

## Optional conference lenses and source-linked learning

Read [review-lenses.md](review-lenses.md) only when the user selects named lenses or `review_lenses: relevant`. Their five names mirror the Stage 2 topics but the diagnostic questions assess **Stage 3 IC-xx handoff design**. Under Section 5, put normal cross-cutting analysis first, optional **CQ coverage** second, **Review Lens Coverage** third, and **Conference Sources & Further Reading** fourth. The lens/source subsections are omitted when lenses are off. Lenses do **not** activate CQ unless CQ was requested.

Keep two evidence types separate: inspected target skills/approved decisions support factual contract findings; conference sources support the review **perspective and further learning**. Show the original session topic, talk title, speaker and actual PDF/YouTube link directly in the report. Do not invent video URLs or claim conference takeaways are official standards. Read only applicable lenses, preserve independent skill operation, and avoid a second issue numbering scheme.

## Evidence, uncertainty and status

Maintain three *separate axes*:

- **Source certainty:** DOCUMENTED (inspected instructions/files), OBSERVED (real supplied run evidence), INFERRED (reasonable interpretation), UNVERIFIED (missing proof), NOT ASSESSED (source inaccessible).
- **Design type:** CURRENT DOCUMENTED, NEW PROPOSAL, CONDITIONAL, APPROVED — DESIGN ONLY, or DEFERRED. Proposed wording is not proof of current behavior.
- **Human decision:** PROPOSED, APPROVED, REVISE REQUESTED, REJECTED or DEFERRED. Explicit approval must identify the exact proposal/version; don't treat `looks good` as blanket approval of unresolved items.

**Approval dependency:** If an upstream ownership/permission `D-xx` is unresolved, related `IC-xx` stays `CONDITIONAL — NEEDS HUMAN`. When the dependency changes, re-present the affected contract for human confirmation. Never equate a chat design approval with organizational authorization, implementation or a passing evaluation.

**Do not conflate statuses:** A handoff may be DOCUMENTED yet execution UNVERIFIED, without being a material defect. A proposed contract may be clear but NOT APPROVED. An approved design may still be NOT IMPLEMENTED.

## Coordinator contract — only when justified

A separately invoked optional coordinator might choose a starting point, sequence authorized steps, preserve source/requirement IDs and route unresolved questions back to owners. The contract must say:

- What it **owns** (routing/context preservation) and **doesn't own** (product/technical decisions of individual skills).
- Whether invocation is explicit/user-chosen and which component's standalone route remains available.
- What human approvals are required before any side effects or changed producer artifact.
- What host dispatch capability is merely desired vs inspected/OBSERVED.

Compare against a simpler manually selected handoff or copyable next action. Do not assume automatic agent dispatch from a markdown file, and do not create the coordinator during Stage 3.

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
