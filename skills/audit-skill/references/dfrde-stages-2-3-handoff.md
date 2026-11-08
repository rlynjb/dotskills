# DFRDE Stages 2–3 — audit-assisted design and contract prefill

This is the **read-only output contract** for `audit-skill` when pre-populating DFRDE **Stage 2 — Design** and **Stage 3 — Contract** from the existing source evidence. It extends [the Stage 1 handoff](dfrde-stage-1-handoff.md); it is **not a separate mode**, a confirmed architecture, an implementation tool or an evaluation runner.

**Canonical generic template when accessible:** `docs/dfrde/engineering-review-template.md`, sections **2. Design** and **3. Contract**. If inaccessible, provide equivalent **inline Markdown drafts**, not imaginary edits to that file.

## Distinguish discovered reality from proposed engineering choices

- **AS-IS / DOCUMENTED:** What actually appears in inspected files, configurations and references, with path:line and source revision. A documented workflow or permission is not automatically observed runtime behavior.
- **OBSERVED RESULT:** Only a provided or separately authorized real trace/test demonstrates the behavior. An agent's assertion of success is not independent evidence.
- **INFERRED:** Plausible interpretation with supporting evidence and uncertainty.
- **PROPOSED OPTION / PROPOSED CONTRACT:** A suggestion derived from the current evidence; **never** describe it as accepted, implemented, enforced, tested or team-approved.
- **OPEN DECISION:** Team ownership or architecture choice not yet resolved.
- **NOT VERIFIED:** Evidence unavailable, source incomplete, runtime effect not observed or context omitted.

**Dependency rule:** Do not treat the draft Stage 1 problem statement as an approved requirement. If business scope, success criteria or design direction is unconfirmed, prefill Stages 2–3 as **conditional proposals based on stated assumptions**. The Audit Skill may provide alternatives and candidate contracts for discussion, but **cannot choose the design, finalize the contract, advance stage gates or edit the review record**.

When a skill has one accessible target, consider its internal interfaces and architecture; mark inter-skill integration NOT APPLICABLE. When multiple accessible skills are present, ground each independently before proposing integration. Missing targets remain NOT ASSESSED, and speculative handoffs are NOT VERIFIED or PROPOSED—not existing contracts.

## Stage 2 — Design: questions to prefill

Produce **S2-Q01–S2-Q05** with short evidence-backed answers or explicit unknowns. For each include source/version, evidence type, question status and recommended next owner action. Add a **compact options/trade-off matrix** and an **as-is diagram reference**. Create a **clearly PROPOSED to-be Mermaid diagram** only when the available evidence is sufficient to sketch plausible boundaries; do not draw unsupported implementation as-if real.

| ID | Question | Prefill from inspection | Human boundary |
| --- | --- | --- | --- |
| **S2-Q01** | Which realistic approaches could solve the *proposed* problem, including keep-as-is or the smallest adequate change? | Existing workflow boundaries, duplicate work and candidate composition/merge/handoff options, when relevant | Options are **PROPOSED** until the Stage 1 problem and design are confirmed |
| **S2-Q02** | Which existing patterns, subsystems, tool configurations and supported runtime assumptions should we preserve? | Actual source-backed architecture, interfaces and versions | Uninspected subsystems and claimed portability are NOT VERIFIED |
| **S2-Q03** | Where should coordination, ownership and decision-making live? | Present skill/agent responsibilities, triggers, result aggregation and handoffs | Assigning new responsibilities or selecting central vs delegated orchestration is an **OPEN DECISION** |
| **S2-Q04** | What are the important trade-offs, bottlenecks, failure cases, permission changes, complexity and costs? | Source-grounded risks; clearly labeled hypothetical trade-offs | Do not invent measured latency, cost, accuracy or operational behavior |
| **S2-Q05** | Which approach is approved, by whom and with what reasoning? | Existing decision record or approval **only if explicitly available** | Otherwise **NEEDS CONFIRMATION / OPEN DECISION**, approval NOT GRANTED |

**Stage 2 design options matrix**

| Option | What changes | Benefit / trade-off | Evidence and assumptions | Status |
| --- | --- | --- | --- | --- |
| **A. Keep existing behavior / minimal validation** | [Source-supported] | [Hypothesis] | [Path:line or UNVERIFIED] | PROPOSED |
| **B. Alternative architecture** | [Source-supported boundaries only] | [Hypothesis] | [Path:line or UNVERIFIED] | PROPOSED |
| **C. Optional other meaningful choice** | [If warranted] | [Hypothesis] | [Path:line or UNVERIFIED] | PROPOSED |

**Stage 2 output:** What is known as-is; alternative(s) and trade-offs; priority questions for teammates (confirmation/decision/runtime evidence only); draft architecture as **PROPOSED**; reviewed design selection **OPEN**, pending **HUMAN REVIEW REQUIRED — Design**.

## Stage 3 — Contract: questions to prefill

Propose a **conditional contract draft** informed by the as-is interfaces and each proposed design option; where options require different interfaces, label **Option A contract / Option B contract** rather than silently choosing one. No agreement exists until the accountable team reviews it.

| ID | Question | Prefill from inspection | Human boundary |
| --- | --- | --- | --- |
| **S3-Q01** | Who produces and consumes each input/output, owns the guarantee, and maintains the contract/version? | Documented inputs/outputs, declared agents, consumers, version references | New producer/consumer responsibility and contract owner remain PROPOSED |
| **S3-Q02** | What are the functional/nonfunctional guarantees, valid states, pre/postconditions, and invariants? | Explicit documented rules/validators and expected outputs; assumptions clearly flagged | New required fields, success thresholds and guarantees are proposed, not existing facts |
| **S3-Q03** | Which identities, trust boundaries, permissions, human approvals and forbidden side effects apply? | Declared tool allowlists, tool/MCP dependencies, policy references and *verified* runtime controls if available | A prompt saying read-only does **not** enforce authorization; unverified enforcement stays NOT VERIFIED |
| **S3-Q04** | What should happen on missing evidence, failed tools, timeouts, retries, duplicated requests, conflicts, partial results and blocked status? | Documented error/stop behavior, existing checks and handoff results | Do not silently invent recovery or resolve conflicts by guessing |
| **S3-Q05** | How will the guarantees be checked and what existing baseline/tests are available? | Present tests/CI/traces and intended outcomes; draft normal/negative/misuse cases | Proposed tests are **NOT RUN**. Quality/security thresholds need approval |
| **S3-Q06** | Where does the contract live and who approves changes and compatibility? | Existing `SKILL.md`, reference docs, schemas, manifests and review controls | New contract file location, versioning and sign-off **OPEN DECISION** |

Use a compact **contract proposal table**:

| Producer → consumer | Inputs / outputs | Required guarantees / invariants | Permission and failure handling | Evidence / status |
| --- | --- | --- | --- | --- |
| [Documented or PROPOSED] | [Known vs new fields] | [Existing vs PROPOSED] | [Enforced / prompt-only / NOT VERIFIED] | [Source:line; OPEN] |

For domain-specific contracts, only propose relevant schemas. **An interface contract is not a universal JSON/YAML format**, and an invariant is a rule that must hold across applicable states, including failure paths. Distinguish the **contract** from the actual implementation and enforcement.

**Stage 3 output:** Candidate inputs/outputs, roles, invariants, trust/permissions and failure semantics; proposed acceptance and regression cases; outstanding agreement questions; contract selection **NOT APPROVED** until Stage 2 design and Stage 3 contract owners agree. **HUMAN REVIEW REQUIRED — Contract** remains pending.

## Output format and meeting preparation

After **Audit Skill — At a Glance** and the Stage 1 draft, provide two concise sections, not additional long independent audits:

```markdown
## DFRDE Stage 2 — Design (audit-prefilled, PROPOSED)
**Prerequisite:** Stage 1 problem/scope [APPROVED or UNCONFIRMED].
**As-is evidence:** [links to audit source map/current-state diagrams].
| S2 question | Draft answer/option | Evidence | Status | Teammate confirmation/decision |
| ... S2-Q01 through S2-Q05 ... |
**Options/trade-offs:** [2+ real choices only when warranted].
**Proposed architecture:** [clearly PROPOSED Mermaid or deferred for missing evidence].
**Gate:** HUMAN REVIEW REQUIRED — design choice NOT APPROVED.

## DFRDE Stage 3 — Contract (conditional draft, NOT APPROVED)
**Dependency:** [which Stage 2 option this draft assumes; or alternatives].
| S3 question | Candidate guarantee / unknown | Evidence | Status | Approval/verification needed |
| ... S3-Q01 through S3-Q06 ... |
**Contract outline:** [producer/consumer, invariants, trust, errors, versions].
**Evaluation suggestions:** [cases expected/negative; NOT RUN].
**Gate:** HUMAN REVIEW REQUIRED — contract NOT APPROVED.

## Team discussion shortlist
[Only confirmations, design decisions, contract ownership and evidence checks
not already resolved by source inspection. Identify owner and next step.]
```

Use `ANSWERED BY EVIDENCE`, `NEEDS CONFIRMATION`, `OPEN DECISION`, `NOT VERIFIED` for questions, even if the **draft option or contract** is PROPOSED. Existing facts can answer a question without approving the proposed response to those facts. Link a question to an existing `F-xx` or `Q-xx` when relevant. Provide full detail on a requested deep dive rather than overwhelming the initial overview.

## Boundaries

- The Audit Skill **does not change** target skills, DFRDE templates or project records. User approval to save the resulting draft belongs to a separate authorized writing workflow.
- Never call a draft an approved architecture/contract, mistake a code comment for effective permission, invent baseline evidence, or assume different agent harnesses have equivalent delegation.
- Never execute target skills, tools, agents, evaluations, tests, write-capable business integrations or deployment as part of a prefill.
- Sensitive workplace code, Jira tickets, transcripts and other non-public material must stay in an approved environment; do not copy them to public DotSkills.
