# New Feature Discovery & Requirements Prompt Library

A reusable, **pre-design feature discovery** prompt for any AI coding agent. Use it when you have an idea or user problem but **no established codebase, ticket, design spec, implementation plan, or architecture decision**. It guides you from user needs and realistic scenarios to functional requirements, non-functional requirements, constraints, options, trade-offs, and questions worth answering before building.

**Core question:** What must this feature enable users to do, under what conditions, with what guarantees, and what viable approaches should we evaluate?

This complements [Existing Feature Investigation](investigate-existing-feature.md), which reconstructs how an already-built feature works and where its resources came from. For reviewing implemented changes, see [Code Review](code-review.md).

**Scope:** Discovery and requirements analysis, not a proposal to start coding. The feature can be a new product, a greenfield feature, or an enhancement where repository context is unavailable. If code or documentation exists, it may inform the investigation, but it is **not a prerequisite**.

---

## Index

| # | Prompt or reference | Reach for it when |
| --- | --- | --- |
| ★ | [Compact daily discovery](#compact-daily-discovery-prompt) | You have a rough feature idea and need a fast, structured first pass |
| 0 | [Master new-feature discovery](#0-master-new-feature-discovery-prompt) | You need thorough requirements, edge cases, and grounded options before design |
| 1 | [Discover user journeys and hidden scenarios](#1-discover-user-journeys-and-hidden-scenarios) | You can describe the happy path but suspect important user conditions are missing |
| 2 | [Separate functional requirements, NFRs, and hard constraints](#2-separate-functional-requirements-nfrs-and-hard-constraints) | Terms like offline, secure, fast, or scalable are underspecified |
| 3 | [Explore possible approaches and trade-offs](#3-explore-possible-approaches-and-trade-offs) | You want 2–3 ways to satisfy requirements without jumping to a tech stack |
| 4 | [Turn requirements into testable scenarios](#4-turn-requirements-into-testable-scenarios) | You need clear acceptance criteria before writing a spec |
| — | [Five book lenses](#five-book-lenses-for-new-feature-discovery) | Understand the problem through the books you are studying |
| — | [Worked example: offline data access](#worked-example-offline-data-access) | See how an everyday scenario becomes several distinct requirements |
| — | [How this fits the other prompts](#how-this-fits-the-other-prompts) | Choose the correct stage of your workflow |

---

## Five book lenses for new-feature discovery

These are the same five reading lenses used by [Code Review](code-review.md), but here they help **ask better questions before an implementation exists**. They do **not** imply that a specific architecture, algorithm, database, or external service is required.

| Lens | Full book title | Discovery questions |
| --- | --- | --- |
| **APOSD** | *A Philosophy of Software Design* | What concepts and responsibilities does the feature introduce? What complexity should the eventual interface hide? What decisions can remain flexible without leaking into user workflows? |
| **AT** | *Algorithmic Thinking* | What actual computation might be necessary (search, sorting, routing, geometry, conflict resolution)? What are the inputs, outputs, correctness conditions, and plausible workload sizes? Don't invent algorithms when none are indicated. |
| **DDIA** | *Designing Data-Intensive Applications* | What must remain correct when data is stale, duplicated, edited concurrently, lost, retried, or synchronized? Which data is authoritative? What durability, consistency, and recovery behaviors do users expect? |
| **FODE** | *Fundamentals of Data Engineering* | Where will data come from, who owns it, how will it be collected/validated/transformed, and when must it reach consumers? What quality, freshness, lineage, retention, and governance requirements matter? |
| **SDI** | *System Design Interview* | Who are the users, what are the functional and non-functional requirements, what are the constraints and scale assumptions, and which broad system choices merit comparison? What trade-offs shape feasibility? |

**Lens policy:** First establish the user problem and evidence. Apply a lens only when it clarifies a real requirement or trade-off. Mark irrelevant lenses **not applicable** and explain briefly. Keep factual requirements separate from book-inspired questions or recommended options. Never manufacture book quotations, page numbers, or claims about what a stakeholder wants.

---

## 0. Master new-feature discovery prompt

**What it does:** Helps a junior engineer discover the problem, elicit requirements, challenge assumptions, compare approaches, and build an evidence-based handoff into a future design spec—without assuming any codebase or existing plan.

**How to use:** Paste the prompt below into a coding or general AI agent. Provide an idea, intended users, and any context you have. If you only have one sentence, that is enough for a first pass; unresolved issues must stay explicitly unresolved.

~~~text
# New Feature Discovery and Requirements Investigator

Act as a patient senior software engineer and product-thinking mentor
helping a junior developer reason through a feature BEFORE designing
or implementing it.

We may have no existing code, repository, ticket, design document,
implementation plan, technology stack, or established architecture.

Your job is to discover WHAT problem we're solving, WHO needs it,
HOW and WHEN the feature will be used, WHAT must be true for it to
work well, and WHICH feasible approaches are worth considering.

This is requirements discovery, not a code review, an architecture
specification, or an implementation plan.

## My feature idea

Feature or product idea:
<DESCRIBE THE FEATURE IN NATURAL LANGUAGE>

Users or stakeholders (if known):
<WHO WILL USE IT OR BE AFFECTED; OTHERWISE UNKNOWN>

Situation or example use case:
<WHAT THE USER IS TRYING TO DO, WHERE, AND WHY>

Context, constraints, or links (optional):
<DOMAIN, PLATFORMS, BUDGET, DEADLINE, BUSINESS RULES,
POLICIES, DEVICES, THIRD-PARTY SYSTEMS, DOCUMENTS, ETC.>

My current uncertainties:
<WHAT I DON'T KNOW; CAN BE BLANK>

## Working principles

- Start from user outcomes, not frameworks or solutions.
- The feature idea is NOT automatically a confirmed requirement.
- Do not assume there is an existing codebase or a design to inspect.
  If reference materials are supplied and accessible, use them as
  evidence; otherwise perform conceptual discovery and label it so.
- Never invent stakeholder decisions, quantitative targets, traffic,
  architecture, integrations, business rules, compliance obligations,
  or historical facts.
- Label significant statements as:
    CONFIRMED — provided by the user or supported by a source.
    PROPOSED — candidate requirement or recommendation to validate.
    ASSUMED — temporary hypothesis used to explore a scenario.
    UNKNOWN — cannot be determined yet.
  Do not label a proposed requirement as confirmed.
- Distinguish REQUIREMENT (needed behavior or quality) from
  SOLUTION (one possible way to meet it).
- Do not turn all good practices into hard requirements.
- If an important decision hinges on missing information, ask
  focused, high-value questions one at a time or in a small batch.
  Still provide a useful provisional analysis from what is known.
- Teach me the engineering reasoning in plain language:
  define unfamiliar terms briefly, explain why each scenario
  matters, and compare trade-offs without talking down to me.
- Work read-only. Do not generate application code, modify files,
  create an implementation plan, choose a final technology stack,
  or claim product decisions have been approved.
- When useful, provide 2–3 genuinely different options with
  prerequisites, trade-offs, and conditions that favor each.
- Only mention external tools, vendors, or services as confirmed
  dependencies when the context establishes them; otherwise present
  them as possible options, not required integrations.
- Do not introduce sensitive details, actual credentials, or
  private data in examples.

## 1. Define the real user problem

Before listing features, answer:
- Who are the users? Which roles have different goals or permissions?
- What job are they trying to accomplish?
- Why is the current situation difficult or insufficient?
- What is the desired outcome, independent of a particular UI?
- How will we recognize that the user succeeded?
- Who else is affected (support, administrators, operations, others)?
- What is explicitly NOT in scope, if known?

Write a short problem statement and outcome statement.

Separate user needs from a proposed solution. For example,
"staff need to view facility data without a connection" is a
potential need; "build a native mobile app" is only one option.

## 2. Discover realistic user journeys

Explore at least:
- Happy path: ordinary user achieves the intended outcome.
- First use / onboarding: no prior account, data, or cached state.
- Returning use: previously stored state or partial work.
- Wrong or missing input: empty data, invalid identifier, no access.
- Unavailable dependency: no network, slow service, vendor outage.
- Interrupted workflow: refresh, app restart, device restart,
  expired session, backgrounding, or an operation halfway done.
- Stale or conflicting information: updates by another user,
  delayed synchronization, mismatched versions.
- Permission and privacy boundaries: who can see or change what?
- Recovery: what should happen after failure, reconnection,
  retry, cancellation, or duplicate action?
- Accessibility and device/context constraints where relevant.

Not all scenarios apply to every feature. Explain why you selected
them and flag plausible missing scenarios for validation.

For each meaningful scenario give:
USER / CONTEXT / TRIGGER / ACTION / EXPECTED OUTCOME /
WHAT COULD GO WRONG / QUESTION TO VALIDATE.

Distinguish a real stakeholder use case from an illustrative
scenario that you invented to explore risks.

## 3. Extract functional requirements

Functional requirements describe what the system MUST DO.

Derive candidate functional requirements from the user journeys:
- View, search, create, edit, delete, import, export, or share.
- Authorize actions and enforce visibility/ownership.
- Validate inputs, show status, and handle errors.
- Work under relevant environmental conditions, e.g. offline.
- Preserve user intent through failures and retries, if needed.
- Reconcile or review conflicts when multiple actors edit data.

For each requirement include:
ID (FR-01 ...):
Statement ("The user/system must be able to ..."):
User journey / outcome it supports:
Trigger and expected behavior:
Acceptance example (Given / When / Then):
Priority: Must / Should / Could / Out of scope:
Status: CONFIRMED / PROPOSED / ASSUMED / UNKNOWN:
Open question, if any:

Don't invent a requirement to fill a category.

## 4. Identify non-functional requirements

Non-functional requirements (NFRs) describe HOW WELL the system
must perform or what guarantees/constraints shape its behavior.

Check relevance of:
- Performance and response times (including offline behavior).
- Availability, reliability, and graceful degradation.
- Durability, data loss tolerance, and recovery.
- Synchronization, freshness, consistency, and conflict handling.
- Security, privacy, authorization, and local device protection.
- Accessibility and supported devices/browsers.
- Scalability: expected users, data volume, peak demand.
- Usability, observability, maintainability, and operability.
- Portability, storage limits, cost, and vendor dependencies.
- Compliance or retention obligations only if evidenced.

For each applicable candidate NFR include:
ID (NFR-01 ...):
Quality attribute:
User/business impact and linked FR or scenario:
Proposed measurable acceptance method or threshold:
Who must confirm the target:
Priority:
Status:
Trade-off or dependency:

If a target is unknown, write "target requires confirmation";
offer an illustrative range only if clearly labeled as an example.
Never make up an SLA, p95 latency, RPO, RTO, retention period, or
traffic estimate and present it as a fact.

IMPORTANT: A requirement can involve multiple layers.
"Users can OPEN previously downloaded data without Wi-Fi" is a
functional capability. "That data survives app restart" is a
durability expectation. "Updates synchronize correctly after
reconnection" adds behavior and consistency guarantees.
Classify each separately rather than treating "offline" as one
vague non-functional checkbox.

## 5. Separate hard constraints from preferences

A hard constraint is a boundary a valid solution cannot violate.
Examples may involve policy, regulatory obligations, required
platforms, existing vendor commitments, a verified deadline, an
approved budget cap, offline field conditions, or data ownership.

Record each candidate constraint:
ID (C-01 ...):
Constraint:
Source / evidence:
Hard, flexible, or still unconfirmed:
Why it matters:
What design options it rules out:
Who can validate or change it:

Keep constraint hardness separate from prioritization:
a high-priority feature is not necessarily an immutable constraint.
Do not assume a platform, vendor, framework, or deployment model
is mandatory merely because it is familiar.

## 6. Discover data, resource, and external prerequisites

Without assuming a codebase, determine:
- What information the user needs and when.
- Where that information would come from.
- What is authoritative, derived, cached, or user-generated.
- Whether data, files, maps, floor plans, reference records, or
  other assets must be supplied by a person or external provider.
- Required formats, validation, permissions, freshness, ownership,
  retention, and updates (as far as requirements establish).
- Whether third-party services, external access, or offline
  preparation might be needed.

Trace a CONCEPTUAL journey:
source/owner -> acquisition/validation -> storage or local copy ->
user action -> output -> any later update/sync.

This is a requirements-level flow, NOT an invented architecture.

For each prerequisite, say:
CONFIRMED / PROPOSED / ASSUMED / UNKNOWN;
who or what might supply it; why it's needed; what to verify.

## 7. Explore alternative approaches BEFORE choosing a design

Identify up to three substantially different approaches that
could satisfy the highest-priority user scenarios.

Describe at the level of product/system strategy, not a final
component diagram or stack selection.

For each option:
- Short name and plain-English behavior.
- Which functional requirements and scenarios it supports.
- Which NFRs or hard constraints it may or may not meet.
- Dependencies, data/assets, and external prerequisites.
- Benefits, drawbacks, failure modes, operational effort,
  and maintenance complexity.
- What we'd need to learn or test to judge feasibility.
- When to prefer it; when to avoid it.

Compare the options against the SAME criteria in a matrix.
Separate facts and constraints from engineering estimates.

Do not present an option as the only valid solution without
evidence. Explicitly identify requirements that force or
differentiate a choice, and choices that remain reversible.

## 8. Use the five books as learning lenses

Use the five lenses from my Code Review Prompt Library.
They are ways to THINK, not mandatory design patterns.

For each relevant lens, provide one to three grounded insights
or questions, tied to a real scenario, requirement, or trade-off.

- APOSD — A Philosophy of Software Design:
  What domain concepts, interface boundaries, responsibilities,
  and likely change points exist? What complexity should be
  hidden from the user or isolated from other modules?
  Do not draft specific modules without sufficient requirements.

- AT — Algorithmic Thinking:
  Is there an actual computational problem (search, ordering,
  routing, geometry, conflict detection)? What inputs/outputs,
  invariants, corner cases, and workload assumptions matter?
  If no special algorithm is evident, mark NOT APPLICABLE.

- DDIA — Designing Data-Intensive Applications:
  What are the requirements for correctness, local or durable
  state, concurrent edits, duplicates, idempotence, versioning,
  stale reads, reconnection, consistency, and recovery?
  Distinguish potential guarantees from established needs.

- FODE — Fundamentals of Data Engineering:
  Where does source data or an asset originate, how fresh must
  it be, who owns it, and how is its quality verified? What
  acquisition, transformation, distribution, or governance
  handoffs might be required?

- SDI — System Design Interview:
  Clarify users, scope, functional/NFR priorities, hard
  constraints, scale assumptions, interfaces between external
  parties or systems, and system-level trade-offs.

Mark NOT APPLICABLE lenses briefly and do not force all five
to generate equal-length output. Summarize overlapping insights
once rather than repeating them five times.

Never claim these books prescribe one specific solution, or
fabricate quotations/page numbers.

## 9. Identify uncertainty, decision gates, and smallest validations

Separate:
- Unknown requirements that could change the user experience.
- Unknown constraints that could eliminate an option.
- Technical assumptions that need a prototype or experiment.
- Organizational/resource questions needing a stakeholder.
- Nice-to-know questions that can wait.

For each high-impact unknown:
Question:
Why it matters:
Impact if answer A versus B:
Who could answer or how to test it:
Blocks requirements / blocks architecture choice / can wait:

Recommend minimal LOW-COST validation, such as a scenario
walkthrough, stakeholder interview, sample data check,
paper prototype, or time-boxed feasibility spike.
Do not execute a spike or build a prototype unless asked.

## 10. Define a smallest useful scope

Recommend a provisional MVP based on the user outcome, and
say which requirements are Must / Should / Could / Won't-for-now.

Include:
- Which user scenario the MVP must successfully handle.
- Which failure/edge scenarios cannot safely be deferred.
- Which enhancements can wait.
- What would invalidate the current MVP recommendation.
- What is explicitly NOT decided or approved yet.

Prioritize by consequence and evidence, not by how easy a
technology seems or how impressive a feature sounds.

## 11. Required final output

Use the following structure, concise but sufficiently concrete:

1. **Problem and desired user outcome** — stakeholders, context,
   success criteria, and what remains assumed.
2. **User journey map** — normal, edge, failure, and recovery cases;
   each with why the case matters.
3. **Functional requirements** — FR IDs, priority, status,
   acceptance examples, linked user scenarios.
4. **Non-functional requirements** — NFR IDs, measurable
   verification proposal, linked user impact, unknown targets.
5. **Hard constraints vs preferences** — C IDs and evidence.
6. **Data, assets, and external prerequisites** — conceptual
   source-to-user flow and unknown ownership.
7. **Two or three viable options** — common trade-off matrix,
   dependencies, failure cases, and decision criteria.
8. **Five-book lens synthesis** — APOSD, AT, DDIA, FODE, SDI,
   marked applicable/not applicable as appropriate.
9. **Top uncertainties and validation questions** — rank by
   what most changes the requirements or approach.
10. **Provisional MVP and acceptance checklist** — explicit
    assumptions and deferred ideas.
11. **Readiness / handoff** — discovery sufficient to design,
    discovery sufficient with assumptions, or blocked by
    critical requirement gaps. List decisions the design-spec
    prompt can consume, but do NOT write the design spec yet.

Finish by asking me ONE high-impact question that helps advance
our understanding. Explain briefly how its answer could change
the recommendation.

If there is almost no initial context, make a helpful
illustrative scenario map, clearly mark it PROPOSED, and avoid
pretending it is a stakeholder-approved requirements document.
~~~

---

## Compact daily discovery prompt

**What it does:** A first pass from a rough idea to the key scenarios, requirements, unknowns, and options, without requiring an existing implementation.

~~~text
Help me investigate a NEW feature before a design or implementation plan.

Idea: <FEATURE OR USER PROBLEM>
Intended users and context: <IF KNOWN>
Known hard requirements: <IF ANY>
Important uncertainties: <IF ANY>

Act as a senior engineer mentoring a junior developer. Do not
assume a codebase, existing architecture, technology stack, or
confirmed requirements.

1. Define the problem and the outcome users need.
2. Explore happy path, first use, edge cases, failures, and recovery.
3. Extract candidate functional requirements (what it must DO).
4. Extract candidate non-functional requirements (how WELL,
   safely, reliably, or under what quality constraints it works).
5. Separate hard constraints from preferences and guesses.
6. Identify data, assets, third-party dependencies, and who
   might have to provide them.
7. Compare 2–3 genuinely different possible approaches,
   with trade-offs, prerequisites, and what would choose between them.
8. Apply relevant five-book lenses:
   APOSD — module boundaries / hidden complexity;
   AT — correctness and real algorithms (if applicable);
   DDIA — data guarantees, failures, consistency;
   FODE — data sources, lifecycle, quality, ownership;
   SDI — use cases, requirements, boundaries, scale, trade-offs.
9. Identify the most important unanswered questions and a
   sensible provisional MVP.

Use CONFIRMED, PROPOSED, ASSUMED, and UNKNOWN labels.
Show FR/NFR IDs, brief Given/When/Then acceptance examples,
and a simple option comparison. Do not invent numeric targets.
Explain unfamiliar concepts and why each scenario matters.
Don't write code, choose a final architecture, or produce a spec.
Ask me one high-impact follow-up question at the end.
~~~

---

## 1. Discover user journeys and hidden scenarios

**Use when:** You're describing a feature by its happy path but don't know how it should behave under less ideal conditions.

~~~text
Act as a product-minded senior engineer helping a junior developer
discover real use cases for: <FEATURE IDEA>.

Start with users, contexts, and outcomes. Create a scenario matrix
covering first use, normal use, unusual inputs, weak/no network,
session expiration, unauthorized access, service failure,
concurrent use, stale data, and recovery AS RELEVANT.

For each scenario:
- User, context, trigger, action, expected outcome.
- What could fail or become ambiguous.
- Candidate functional requirement and likely quality needs.
- Whether it is confirmed or merely a proposed example.
- One question or observation that would validate the scenario.

Use APOSD, AT, DDIA, FODE, and SDI selectively to reveal
missing boundaries, computations, data guarantees, sources,
or system constraints. Avoid making architecture decisions.

Finish by ranking the three scenarios most likely to change
the scope or solution. Ask one relevant clarification.
~~~

---

## 2. Separate functional requirements, NFRs, and hard constraints

**Use when:** A statement such as "the app works offline," "must be secure," or "should be fast" sounds important but is not yet actionable.

~~~text
Take these rough needs or statements:
<PASTE USER STORIES OR REQUIREMENTS>

Rewrite them as distinct:
- Functional requirements: observable capabilities and behavior.
- Non-functional requirements: required qualities/guarantees,
  with ways to validate them.
- Hard constraints: boundaries that viable solutions cannot violate.
- Preferences: desirable but negotiable choices.
- Assumptions and unknowns: items requiring stakeholder confirmation.

Make a traceability table:
ID -> scenario -> precise statement -> status -> priority ->
how to verify -> missing decision.

Use examples to explain why one sentence may need multiple
requirements. Never invent numeric targets or silently
treat a proposed SLA/platform/vendor as a hard constraint.

Use five relevant book lenses to inspect blind spots, especially
DDIA (correctness/recovery), FODE (data origin and freshness),
and SDI (scope and quality requirements). APOSD and AT are
optional if boundaries or computation matter.

Do not design or implement the system.
~~~

---

## 3. Explore possible approaches and trade-offs

**Use when:** You know the outcome but don't know the right level of solution.

~~~text
Given this new feature and candidate requirements:
<FEATURE + USERS + REQUIREMENTS / CONSTRAINTS>

Propose up to three substantially different product/system
approaches without committing to a technology stack.

For every option:
- User experience and supported scenarios.
- Which FRs, NFRs, and hard constraints it meets or fails.
- Data, assets, and external-resource prerequisites.
- Failure/recovery implications, possible operational overhead.
- Complexity, likely cost drivers, reversibility, and risks.
- What fact or small experiment would make this option preferable.

Compare against the same criteria, not three promotional blurbs.
Use all five book lenses where relevant:
APOSD for interfaces and complexity, AT for actual computation,
DDIA for guarantees and failure modes, FODE for data/source
workflow, SDI for architecture-level trade-offs and constraints.

Finish with a conditional recommendation:
"If X is a hard requirement, prefer A; if Y is flexible,
B may be simpler." Mark assumptions. No code or implementation plan.
~~~

---

## 4. Turn requirements into testable scenarios

**Use when:** You have candidate requirements and need to make them observable before handing them to a designer or engineer.

~~~text
Turn these candidate feature requirements into clear acceptance
scenarios: <REQUIREMENTS>.

For each FR, write Given / When / Then behavior with normal,
boundary, failure, and recovery cases where relevant.
For each NFR, identify a measurable verification method,
but leave unknown targets as questions instead of inventing them.

Link: user outcome -> scenario -> FR/NFR -> acceptance check.
Surface conflicts and missing data or external resources.

Use DDIA for consistency and recovery tests, FODE for data quality
and freshness, AT for algorithm correctness where applicable,
SDI for requirements coverage, and APOSD for boundaries that
could otherwise complicate changes. Mark inapplicable lenses.

Do not write production code, tests, a design spec, or a plan.
~~~

---

## Worked example: offline data access

**Idea:** "Field staff need to access facility information even when they have no Wi-Fi or cellular connection."

This is a **starting use case**, not a complete set of requirements. The following are illustrative **PROPOSED** questions and requirements, not decisions already made.

### Possible user scenarios

| Scenario | Question that changes the scope |
| --- | --- |
| Staff opened a facility while connected, then lost connectivity | Does read-only access to previously loaded information satisfy the need? |
| Staff opens a facility for the first time while disconnected | Must the data have been explicitly downloaded beforehand? Is first-time offline access mandatory? |
| Staff edits a room's status offline | Are offline edits required, or is viewing sufficient? |
| Two staff members edit the same record on separate devices | Who decides which update is authoritative after reconnection? |
| A device is shared, lost, or left unlocked | May sensitive facility information remain stored locally, and for how long? |
| Floor-plan asset loads but room labels are missing | Must images and their associated metadata be downloaded together and checked for compatibility? |

### Separating requirements

| Kind | Candidate statement | Status |
| --- | --- | --- |
| **Functional (FR)** | Users can view previously downloaded facility information without an internet connection. | PROPOSED |
| **Functional (FR)** | Users can see whether they are viewing offline or potentially outdated information. | PROPOSED |
| **Functional (FR)** | Users can record changes offline and synchronize on reconnection. | PROPOSED — confirm whether edits are necessary |
| **Non-functional (NFR)** | Required offline data remains readable after closing and reopening the app. | PROPOSED — durability requirement |
| **Non-functional (NFR)** | Offline information satisfies an agreed freshness policy after reconnection. | PROPOSED — policy/target unknown |
| **Non-functional (NFR)** | Local sensitive data follows an approved storage and access-protection policy. | PROPOSED — determine applicable policy |
| **Constraint** | Field staff regularly work without reliable network service. | Only CONFIRMED if a stakeholder or source verifies it |

### Possible approaches (not a final architecture)

| Approach | Supports | Limitations / questions |
| --- | --- | --- |
| **Online-first with cached read-only data** | Previously viewed information when offline | What must be preloaded? Are offline edits out of scope? |
| **Explicit download for offline use** | Chosen facilities/assets prepared in advance | Who manages downloads, storage limits, updates, and expiry? |
| **Offline-first with local edits and later sync** | Viewing and editing while disconnected | Requires harder decisions about conflict resolution, synchronization, security, and recovery |

These are strategic options. Technologies such as browser storage, service workers, local databases, or synchronization services should be considered **after** deciding what users actually need.

### Five-book connection

- **SDI:** Define what "offline access" means for the user journey, and whether read-only or editing is a hard requirement.
- **FODE:** Determine the facility information's source, what must be packaged locally, who owns updates, and how stale data is identified.
- **DDIA:** Investigate data durability, authoritative versions, consistency after reconnection, duplicate updates, and conflicts.
- **AT:** If the feature includes conflict detection or geometry processing, investigate their correctness conditions. Otherwise this lens may be inapplicable.
- **APOSD:** Identify which complicated offline/sync details the eventual feature should hide from users and other parts of the application, without committing to modules yet.

**First high-impact question:** *Do users only need to **view** facility data offline, or do they also need to **change** it offline?* The answer may rule out the simplest approach and materially change the requirements.

---

## How this fits the other prompts

| Stage | Prompt | What it establishes |
| --- | --- | --- |
| **New idea with no code or spec** | **New Feature Discovery** (this file) | User scenarios, FRs, NFRs, constraints, options, unknowns, provisional MVP |
| Existing feature or a working example | [Existing Feature Investigation](investigate-existing-feature.md) | Runtime behavior, provenance, original assets/tools, external setup |
| **After investigation / before Superpowers** | [Refine Feature Requirements](refine-feature-requirements.md) | Confirm FRs/NFRs, identify stakeholder questions, make the design-readiness decision |
| Deeper understanding of an implementation | [System Learning Implementation](system-learning-implementation.md) | Execution flow, mechanisms, data changes, and design reasoning |
| Onboarding to an unfamiliar codebase | [System Learning Repo](system-learning-repo.md) | Whole-repository structure, responsibilities, and representative data flows |
| Implemented changes to assess | [Code Review](code-review.md) | Correctness, maintainability, and engineering trade-offs |

**Suggested workflow:** Idea -> discover real user journeys -> distinguish FRs / NFRs / constraints -> compare options -> validate consequential unknowns -> only then design, plan, implement, and review.

Do not run the complete master prompt for every tiny decision. The compact prompt and focused modules are enough for many day-to-day questions.
