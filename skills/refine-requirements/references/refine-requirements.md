# Feature Requirements Refinement & Superpowers Handoff

A **standalone, pre-design feature investigation and requirements-refinement prompt** for both **new features** and **changes to existing features**. Start with an assigned ticket, product request, or feature idea; **review the relevant codebase first** to find existing features, reusable patterns, and established behavior; check how that evidence aligns with the request; **only then** refine functional requirements, non-functional requirements, and unanswered questions **before** Superpowers designs and plans the implementation.

You do **not** need to run a separate "investigate new feature" or "investigate existing feature" prompt first.

**Core questions:** What comparable features or established patterns already exist in this codebase? Can the requested behavior follow them, or are there requirements that genuinely differ? Where do the ticket and existing behavior agree or conflict? Only after checking those facts, which functional/non-functional requirements and stakeholder/developer questions remain?

**Workflow:** Ticket / idea → **review relevant code and find similar patterns** → compare ticket against existing behavior → **refine FRs, NFRs, and acceptance criteria** → ask only the remaining stakeholder/developer questions → hand off requirements and reusable-pattern evidence to **Superpowers** for design, planning, and execution → [Code Review](code-review.md).

**Boundary:** Investigate **just enough existing behavior, nearby patterns, and history to validate requirements**. Prefer alignment with proven local conventions over inventing a new approach, **when those conventions satisfy the confirmed requirements**; Superpowers makes the actual technical reuse/design decision. This is not a deep technical walkthrough, code review, architecture design, technology selection, or implementation plan.

---

## Index

| Prompt | Use it when |
| --- | --- |
| [Master feature requirements investigation](#0-master-feature-requirements-investigation-prompt) | You have an assigned ticket or idea and want to review similar code patterns first, then refine requirements and identify unanswered questions |
| [Compact ticket readiness check](#compact-ticket-readiness-check) | You need a fast requirements check before invoking Superpowers |
| [Five-book lens guide](#five-book-lens-guide) | You want the books to reveal requirement gaps without turning this into technical design |

---

## Five-book lens guide

Use the lenses **lightly** to identify missing business rules, observable behavior, or quality expectations. They are question generators, not mandatory technical analyses.

| Lens | Requirements-focused question (not a design task) |
| --- | --- |
| **APOSD — A Philosophy of Software Design** | Are user-visible concepts, responsibilities, boundaries, and rules clear? Is an important variation or exception missing from the ticket? |
| **AT — Algorithmic Thinking** | If the feature involves searching, ranking, matching, sorting, calculating, or reconciling, what observable output is correct? What ties, input limits, edge cases, or business rules need clarification? |
| **DDIA — Designing Data-Intensive Applications, 2nd edition** | What must users expect when data changes, is duplicated, stale, unavailable, edited concurrently, or recovered? Which information is authoritative, and what cannot be lost? |
| **FODE — Fundamentals of Data Engineering** | Where does required business data or an asset originate? Who owns its meaning and quality? How fresh must it be, and who consumes it? |
| **SDI — System Design Interview** | Who uses this feature? What functional and non-functional expectations, dependencies, scale assumptions, and product-level trade-offs matter? |

Mark irrelevant lenses **not applicable**. Combine overlapping insights; do not generate five separate technical reports or imply a book mandates any particular technology or architecture.

---

## 0. Master feature requirements investigation prompt

**What it does:** Starts from a **ticket or feature idea**, checks relevant code and similar feature patterns **before** drafting requirements or questions, then identifies what can be reused, what differs, which decisions require stakeholder/developer input, and what Superpowers should receive. If no codebase is available, it explicitly marks the pattern check unverified.

~~~text
Act as a feature requirements investigator and refinement partner.
Prepare the assigned ticket or feature idea for the Superpowers
design and implementation-planning workflow.

This is a STANDALONE prompt. Do not require a prior new-feature
or existing-feature investigation report. Use one if I supply it,
but begin from the ticket and available evidence otherwise.

SEQUENCE IS IMPORTANT: First read the ticket just to locate the
feature and its context; then inspect the relevant codebase for
similar features and reusable conventions. Only AFTER reporting
that evidence should you refine functional/non-functional
requirements or draft questions for stakeholders or developers.

INPUTS (use what is available; missing inputs are not blockers by
themselves)
- Feature / assigned ticket / product idea: [PASTE TEXT OR LINK]
- Repository / codebase / branch: [IF AVAILABLE]
- Product specs, designs, related tickets, previous implementations:
  [IF AVAILABLE]
- Known stakeholder decisions, constraints, and answered questions:
  [IF AVAILABLE]
- Specific uncertainty or concern: [OPTIONAL]

FIRST: LOCATE THE FEATURE AND REVIEW RELEVANT CODE
- Read the ticket to identify keywords, user-facing behavior, and
  likely code areas for a focused search; do not finalize FRs,
  NFRs, proposed behavior, or outreach questions yet.
- Inspect the relevant codebase before forming those conclusions.
  Search for comparable screens, endpoints, workflows, business
  rules, shared components, tests, data contracts, and prior feature
  instances; follow references only as needed.
- Classify the request as: new capability, enhancement/change to an
  existing feature, new instance of an existing pattern, mixed, or unclear.
- A new feature MAY still fit existing conventions; an existing
  feature MAY already support part or all of the request.
- If the codebase is unavailable, report what you tried and mark
  code/pattern alignment NOT VERIFIED or NOT APPLICABLE. Continue
  with provisional requirements grounded in the ticket, rather
  than inventing code evidence or blocking the entire analysis.

WORKING RULES
- Prioritize WHAT users/business need and HOW WELL it must work.
  Superpowers will own technical design, architecture, technology
  selection, algorithms, detailed plans, and coding.
- Start with relevant code, nearby feature examples, business rules,
  docs, tests, contracts, and available history. Establish existing
  patterns BEFORE drafting requirements or outreach questions.
  Do not exhaustively map the system.
- Treat established, relevant patterns as the DEFAULT reuse baseline,
  not a mandate to copy accidental complexity or obsolete behavior.
  Flag gaps and let Superpowers decide the technical implementation.
- Stay read-only. Do not edit code, generate an implementation plan,
  execute Superpowers, make commits, deploy, or call write APIs.
- Cite meaningful claims with ticket/spec references, paths and
  symbols, tests, PRs, or commits you actually inspected. If access
  is unavailable, say what remains unverified.
- SEPARATE:
    CONFIRMED REQUIREMENT — explicitly established by the ticket,
      approved spec, or stakeholder decision (cite its source).
    OBSERVED BEHAVIOR — verified in current code/tests; this is NOT
      automatically an approved product requirement.
    PROPOSED — candidate behavior or clarification to validate.
    ASSUMED — explicit temporary hypothesis, not a decision.
    UNKNOWN — not established by available evidence.
- Preserve the business terminology; flag conflicts rather than
  silently reconciling them. Never treat code or past implementation
  as proof of stakeholder intent or a historical design decision.
- Never fabricate historical reasons, stakeholder approvals, priorities,
  SLAs, numbers, integrations, or constraints. Do not present a
  suspected bottleneck or best practice as a requirement.
- Prefer concrete, high-impact unanswered questions over long lists.
  Keep technical findings brief and tied to requirement implications.

1. REVIEW EXISTING CODE AND REUSABLE FEATURE PATTERNS FIRST
Use the ticket only to locate the relevant behavior. Before
drafting FRs, NFRs, acceptance criteria, or questions:
- Search for the closest analogous feature(s) or workflow(s),
  even if this ticket is for a new feature. Look at the relevant
  user-visible path, common entry points, shared components,
  validations, permissions, business rules, data sources/contracts,
  configuration, tests, and relevant documentation or history.
- Trace only enough of each example to explain WHAT it does and
  which behavior/pattern the ticket may be able to follow.
  Cite actual paths/symbols/tests (and PRs if available).
- Identify the established reusable behavior and conventions,
  and distinguish shared parts from feature-specific exceptions.
- Note whether the candidate pattern meets the ticket's user
  needs and known quality expectations; highlight any differences,
  gaps, outdated assumptions, or possible compatibility concerns.
- Prefer FOLLOW EXISTING PATTERN when fit is supported by evidence;
  mark ADAPT EXISTING PATTERN when some requirements differ; mark
  NO SUITABLE PATTERN FOUND / NOT VERIFIED when appropriate.
  These are requirements-level observations, NOT technical design
  mandates. Superpowers decides exactly how to reuse or extend.
- Do not invent a new pattern solely because the ticket describes
  something new. Do not insist on reuse if it conflicts with a
  verified requirement. When search coverage is incomplete, say so.

Summarize this evidence FIRST in a compact pattern map:
  Similar feature / file or test evidence / observable behavior /
  reusable rule or contract / relevant difference / suitability:
  FOLLOW / ADAPT / NO SUITABLE PATTERN FOUND / NOT VERIFIED.

2. CLARIFY THE TICKET AND ALIGN IT WITH EXISTING BEHAVIOR
Only now, using the code/pattern findings AND ticket/spec evidence:
- Explain who needs the feature, which problem it solves, and what
  observable outcome counts as success.
- Distinguish what already exists from what must be added, changed,
  preserved, reused, or removed; do not assume existing behavior
  is an approved new requirement.
- State in-scope work, exclusions, dependencies, and undecided scope.
- Produce a concise alignment table for significant behavior:
    Ticket requirement or acceptance expectation / source
    Existing behavior or similar-pattern evidence
    Status: ALREADY PRESENT / PARTIAL / MISSING / CONFLICT /
            NOT VERIFIED / NOT APPLICABLE
    Reuse fit and requirements implication / open decision
- Only label behavior MISSING when the inspected evidence supports
  the finding; otherwise say NOT VERIFIED.
- For legacy patterns, identify undocumented assumptions or past
  decisions a developer may need to confirm. Don't invent history.
- Avoid deep call graphs, refactoring plans, query tuning, and
  detailed technical solutions; those belong with Superpowers.

3. REFINE THE USER JOURNEYS
- State the normal user journey: actor -> trigger -> expected action ->
  observable outcome.
- Add only material alternative, permission, empty-data, invalid-input,
  repeated-action, failure, and recovery cases.
- Use the existing pattern examples to spot missing scenarios or
  behavior differences; ask for confirmation rather than copying
  business rules without evidence.
- Show where the ticket is ambiguous and different interpretations
  would change user behavior or acceptance.
- For existing features, explicitly distinguish current user behavior
  from requested user behavior.

4. REFINE FUNCTIONAL REQUIREMENTS (FR)
For each material requirement include:
- FR-ID, observable user/system behavior, actor/trigger, expected result.
- Must / Should / Could / Out of scope (mark proposed priorities).
- CONFIRMED REQUIREMENT / PROPOSED / ASSUMED / UNKNOWN.
- Source/ticket reference, relevant existing-pattern or observed
  code evidence (if any), reuse/variation implication, and linked
  open question.
- A short Given / When / Then acceptance example for the important
  happy path, business rules, and error cases.

Flag duplicate, conflicting, vague, missing, or untestable statements.
Do not promote what exists in code into a new requirement without
ticket or stakeholder support.

5. REFINE NON-FUNCTIONAL REQUIREMENTS (NFR)
For each relevant expectation include:
- NFR-ID, user/business impact, linked journey or FR, desired quality,
  proposed verification/acceptance method, priority and status.
- If no target is provided, write "target requires confirmation".
- Consider relevant latency/performance, reliability/availability,
  consistency/freshness, durability/recovery, security/privacy,
  accessibility, supported clients, scale, usability, operating
  constraints, and costs. Skip irrelevant categories.
- Compare verified qualities/constraints from similar features or
  contracts against the ticket; identify NFRs the existing pattern
  appears to cover and any newly required or unverified targets.
- Identify product-level choices (e.g., can users tolerate stale
  information?) without designing the system to satisfy them.
- Never invent specific thresholds, compliance duties, or SLAs.

6. CHECK CONSTRAINTS, DEPENDENCIES, AND ACCEPTANCE
- Separate hard constraints, preferences, unverified assumptions,
  and freedom intentionally left to Superpowers.
- Identify any prerequisite business data, assets, team decisions,
  access/approval, external system, or previous behavior that must
  remain compatible, if evidence supports it.
- Confirm each Must requirement has an observable acceptance condition.
- Identify conflicts between FRs, NFRs, ticket wording, current
  behavior, and candidate reuse patterns without making a product
  decision on anyone's behalf.

7. FIVE-BOOK REQUIREMENTS CHECK (LIGHTWEIGHT)
Apply APOSD, AT, DDIA (2nd edition), FODE, and System Design
Interview (SDI) only when they expose a material missing business
rule, acceptance condition, constraint, or quality expectation.
For each applicable lens give at most 1-2 useful questions linked
to an FR, NFR, scenario, or scope decision. Mark irrelevant lenses
NOT APPLICABLE. Consolidate overlap.

Do not produce system diagrams, technical design alternatives,
schema proposals, algorithm analysis, or performance optimization.

8. ROUTE ONLY REMAINING QUESTIONS TO THE RIGHT PEOPLE
AFTER the code/pattern review and the FR/NFR refinement, check
whether existing code, tests, docs, or verified decisions already
answer each candidate question. Drop answered or redundant questions.
Prioritize only unresolved questions in these groups:

A. STAKEHOLDERS / PRODUCT OWNER — business intent, scope,
   expected user behavior, acceptance criteria, priorities, quality
   targets, policy, or externally owned input. Blocking when the
   answer changes material requirements or design assumptions.

B. DEVELOPERS / FEATURE HISTORY — whether a similar feature
   was intended as the reusable pattern; which shared conventions,
   contracts, exceptions, tests, previous tickets/PRs, or legacy
   constraints matter; or why an earlier behavior was introduced
   (ask; don't invent the historical answer). Only block handoff
   when that fact is necessary to define valid requirements or
   avoid a material compatibility error.

C. SUPERPOWERS DESIGN QUESTIONS — architecture, libraries,
   module organization, query/index design, implementation tasks,
   engineering trade-offs. Preserve these for Superpowers rather
   than presenting them as stakeholder blockers.

D. DEFER / NICE TO KNOW — questions unlikely to alter scope or
   meaningful acceptance behavior. Avoid distracting outreach.

For each outreach question (A or B), provide:
- ID (Q-01 ...), priority, owner/role (or owner to identify).
- Exact concise question ready to send.
- Why it matters; linked FR, NFR, journey, or code/ticket conflict.
- Answer options and consequences only when useful; do not imply
  an option has been approved.
- Evidence or source of uncertainty.
- BLOCKS HANDOFF? YES / NO, with a short reason.

Separate product decisions from factual questions about existing
behavior. Developers may explain history, but cannot approve
product scope just because they know the code.
Provide TWO short ready-to-send messages only when needed:
one for stakeholders, one for involved developers. Include the
highest-impact unanswered questions; omit resolved questions.

9. CREATE A SUPERPOWERS REQUIREMENTS HANDOFF
Produce a concise requirements brief containing:
- Feature context (new / change / reuse), product problem, user,
  expected outcome, and in-scope/out-of-scope boundaries.
- Confirmed FRs, relevant NFRs, and observable acceptance criteria.
- Existing feature/pattern references (files/symbols/tests) and
  reusable behavior or contracts to preserve. State where the
  ticket fits the pattern, where it needs variation, and what
  remains unverified; do not dictate technical design.
- Required compatibility with existing behavior or contracts,
  supported by evidence; distinguish unknown compatibility risks.
- Hard constraints, prerequisites, dependencies, and verified targets.
- Approved decisions and named provisional assumptions, with sources.
- Remaining stakeholder/developer questions and their owners.
- Engineering topics deliberately handed to Superpowers, without
  attempting to solve them here.

Give one readiness verdict:
- READY — material requirements/acceptance are sufficiently clear;
  no blocking product or historical/compatibility decisions remain.
- CONDITIONAL — named non-blocking assumptions remain, with owners
  and explicit conditions that would require revisiting the brief.
- BLOCKED — a critical product decision or necessary existing-system
  fact remains unknown; identify the MINIMUM answers required.

If blocked, still produce a useful provisional handoff but do NOT
present it as agreed or implementation-ready. Do not let Superpowers
invent business answers. Mark open questions that require approval
before execution even if design exploration can start.

REQUIRED OUTPUT (keep concise; omit inapplicable detail)
1. Codebase-first review: comparable existing features, pattern map,
   file/test evidence, and FOLLOW / ADAPT / NO SUITABLE PATTERN /
   NOT VERIFIED assessment (or explain why no code is accessible).
2. Ticket outcome, scope, and ticket-to-codebase alignment table.
3. User journeys and key acceptance scenarios, grounded in patterns
   where relevant.
4. Refined functional requirements (FR table), with reuse links.
5. Refined non-functional requirements (NFR table), with pattern
   baseline vs new expectations.
6. Constraints, dependencies, and compatibility concerns.
7. Material five-book requirement questions (if applicable).
8. Remaining questions BY OWNER, plus stakeholder/developer
   ready-to-send messages where useful.
9. Superpowers handoff brief with existing-pattern references
   and READY / CONDITIONAL / BLOCKED verdict.

Do not repeat the full ticket, existing code, or history. Finish
with the most consequential unanswered question, if one exists.
~~~

---

## Compact ticket readiness check

**Use when:** An assigned ticket looks small or straightforward and you want to validate requirements and fit against the relevant existing code before Superpowers takes over.

~~~text
Review this ticket or feature idea and relevant codebase as a
STANDALONE requirements check before I use Superpowers for design
and implementation planning.

Input: [TICKET / FEATURE REQUEST, REPOSITORY IF AVAILABLE, KNOWN
DECISIONS, LINKS OR REFERENCE FILES]

This may be a NEW feature or a CHANGE to an existing one. FIRST
inspect the relevant code/docs/tests for similar feature patterns,
observable behavior, and constraints. Use the ticket only to target
the search at this stage. Do not require an earlier investigation,
or perform deep technical analysis. If no code is accessible, mark
pattern alignment NOT VERIFIED and continue provisionally.

Only AFTER the code review, give me:
1. Comparable features, relevant paths/tests, established reusable
   patterns and fit: FOLLOW / ADAPT / NO SUITABLE PATTERN FOUND /
   NOT VERIFIED.
2. Product goal, scope, and ticket-to-code alignment with evidence.
3. Refined functional requirements and acceptance examples,
   referencing existing behavior where relevant.
4. Non-functional requirements: existing quality expectations,
   gaps, and targets needing approval.
5. Material assumptions, dependencies, and compatibility risks.
6. Only remaining questions after checking code and docs:
   (a) stakeholder/product decisions, (b) involved developers
   about history, conventions, or pattern applicability. Include
   decision owner, blockers, and ready-to-send wording.
7. APOSD, AT, DDIA (2nd edition), FODE, and SDI questions ONLY
   where these uncover a material requirements gap.
8. A product-focused Superpowers handoff citing relevant
   reusable patterns, plus READY / CONDITIONAL / BLOCKED verdict.

Distinguish CONFIRMED REQUIREMENTS from OBSERVED CODE BEHAVIOR,
proposals, assumptions, and unknowns. Cite what you inspect.
Leave technical architecture and implementation planning to
Superpowers. Work read-only.
~~~

---

## How this fits the engineering workflow

| Stage | Responsibility |
| --- | --- |
| Assigned ticket / new idea / change to existing feature | Input to this prompt, with whatever source material exists |
| **Requirements investigation and refinement (this file)** | **First inspect code and similar features**; identify reusable conventions; then compare ticket, refine FRs/NFRs, and ask only unresolved stakeholder/developer questions |
| Confirm unanswered product and history questions | Obtain decisions or factual context from the appropriate people; update the requirements brief |
| Design, implementation plan, execution | **Superpowers**, using confirmed requirements and explicitly noted assumptions |
| Review implemented changes | [Code Review](code-review.md) |

**Use this file directly for both new and existing features.** No separate investigation prompt is required. Use the compact check for small tickets, the master for ambiguous or consequential work. The goal is to establish *what the codebase already supports, what to build, what established pattern fits, and what still needs to be asked*, then hand the technical choices to Superpowers.
