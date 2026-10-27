# Refine Requirements

**`refine-requirements`** is a codebase-first, interview-led engineering skill for turning a new feature request or a change to an existing feature into clear, evidence-backed requirements **before technical design begins**.

It serves two purposes: (1) refine real tickets into functional requirements (FRs), non-functional requirements (NFRs), testable acceptance criteria, and stakeholder decisions; and (2) practice the reasoning used in **system-design and DSA interviews**. The default experience is **overview first, selective deep dives second**: review an evidence and pattern map plus all material FR/NFR findings, then choose a requirement to explore through Code Review-inspired questions, scenarios, trade-offs, and learning checkpoints.

**Outcome:** a requirements brief that can be handed to **Superpowers** for design and implementation *later*. This skill does not choose an architecture, implement code, or answer business questions on behalf of stakeholders.

## Table of contents

- [When to use it](#when-to-use-it)
- [Workflow](#workflow)
- [Initial Findings Overview](#initial-findings-overview)
- [The interview learning loop](#the-interview-learning-loop)
- [Modes](#modes)
- [What the skill refines](#what-the-skill-refines)
- [Final deliverables](#final-deliverables)
- [Example interview question](#example-interview-question)
- [How to invoke it](#how-to-invoke-it)
- [Evidence, safety, and scope](#evidence-safety-and-scope)
- [Source files](#source-files)

## When to use it

Use this skill when a ticket, product request, or feature idea needs clarification before engineering design: a new capability, an enhancement to existing behavior, a variation of a reusable feature, or an ambiguous change with important edge cases or quality requirements. It is also useful when you want to **practice explaining requirements as an interview candidate**.

**Inputs:** the ticket or feature idea, any approved specs or decisions, and access to relevant code/tests/contracts when available. If the codebase cannot be inspected, the interview may proceed with **provisional** ticket-grounded questions and an explicit **NOT VERIFIED** code-pattern status.

## Workflow

The process borrows **clarification, scenarios, and edge-case reasoning** from DSA interviews and **functional/non-functional scoping, system constraints, and trade-offs** from system-design interviews. It is **adaptive**: skip questions already answered by evidence and mark inapplicable topics rather than asking everything by rote.

```mermaid
flowchart TD
    A["Feature ticket, idea, decisions"] --> B["Inspect relevant code, tests,<br/>contracts, and existing patterns"]
    B --> C["Evidence & pattern map<br/>or explicit NOT VERIFIED"]
    C --> D["Findings Overview<br/>all material FRs + NFRs"]
    D --> E["Summarize edge cases, dependencies,<br/>system-design gaps, readiness"]
    E --> F["Review choices: select FR/NFR/gap"]
    F --> G["Stakeholder questions<br/>one concise section at bottom"]
    G --> H{"User selects next action"}
    H -->|"Explore item"| I["Guided or Practice<br/>one chosen requirement at a time"]
    I --> J["Refine evidence, acceptance,<br/>and requirements register"]
    J --> H
    H -->|"Refresh inputs"| B
    H -->|"Complete / request handoff"| K["Consolidated requirements<br/>+ Superpowers handoff"]
    K --> L["Stakeholder questions<br/>last section"]
```

**Codebase first** means locating relevant existing behavior before recommending new requirements or asking stakeholders questions that code or approved documents might already answer. Code is evidence of **observed behavior**, not automatic proof of a **confirmed product requirement**.

### How a topic progresses

First, inspect code and present the **entire concise findings overview**, including the evidence map. Only **after you select an item** does the skill use these interview steps:

1. **Clarify the selected problem:** who needs this specific behavior, its trigger/outcome, boundaries, and unresolved assumptions.
2. **Check existing patterns:** inspect a close analogue, note reusable business rules/contracts, and distinguish follow/adapt/no suitable pattern/not verified.
3. **Write functional requirements:** observable behavior, actors, permissions, priority, and verifiable acceptance criteria.
4. **Stress-test with examples:** normal paths, invalid/empty input, duplicates, retries, concurrent actions, permission denial, partial failure, and recovery when relevant.
5. **Write non-functional requirements:** relevant performance, reliability, consistency/freshness, security/privacy, accessibility, scale, observability, compatibility, or cost expectations. Unapproved thresholds remain **target requires confirmation**.
6. **Prepare system-design inputs:** domain entities/states, data ownership, source of truth, interfaces/contracts, dependencies, read/write patterns, workload assumptions, trust boundaries, and trade-off questions—not a prescribed implementation.
7. **Challenge and revise:** change a constraint, explain how requirements and acceptance might change, record remaining unknowns, and check coverage.
8. **Assess readiness and hand off:** produce **READY**, **CONDITIONAL**, or **BLOCKED** with reasons; end with only the consequential **Questions to ask stakeholders**.

## Initial Findings Overview

**This is the default first output, not Problem question 1.** The skill searches the relevant existing code first and then shows the full *initial* findings in a compact register. You can scan the big picture and choose which IDs to discuss without reading a separate explanation for every requirement.

| Section (in order) | What appears |
| --- | --- |
| **1. Feature snapshot** | Goal, actors, scope, inspected branch/revision, and evidence limits. |
| **2. Evidence & pattern map** | Comparable features, code/test/path evidence, observable behavior, differences, FOLLOW / ADAPT / NO SUITABLE PATTERN FOUND / NOT VERIFIED. This section is **always present**. |
| **3. Functional requirements** | All material `FR-xx` rows: concise behavior, priority, confirmed/proposed/assumed/unknown, source/pattern link, open question. |
| **4. Non-functional requirements** | All material `NFR-xx` rows: linked FR/journey, quality and grounded target (or **target requires confirmation**), priority/status, evidence/owner. |
| **5. Bigger picture** | Short edge/failure scenarios, dependencies, permissions, data ownership, contracts, scale/reliability/security and other system-design inputs. |
| **6. Readiness and review choices** | Provisional readiness/blockers and an invitation to pick a requirement or gap to drill into. |
| **7. Post-interview — Questions to ask stakeholders** | **Always at the bottom:** a concise deduplicated list with Q-ID, owner, exact question, linked FR/NFR, priority and handoff-blocking flag. No extensive per-question explanations. |

The overview is **not** the full nine-part Superpowers handoff, and no initial findings should be misrepresented as approved decisions. If source code cannot be accessed, the pattern map says **NOT VERIFIED** and FR/NFR tables remain clearly provisional. When you provide new ticket details, decisions, or code changes, the skill **refreshes affected evidence and the pattern map** and summarizes changes instead of assuming previous findings are current.

## The interview learning loop

After the Findings Overview and **your selection** (for example, `FR-02` or `NFR-01`), Guided mode explores **one selected requirement at a time**, rather than interrogating each finding automatically:

```mermaid
flowchart LR
    A["Choose FR / NFR / gap"] --> B["Problem question on chosen item"]
    B --> C["How to reason + worked answer"]
    C --> D["Scenario and changed constraint"]
    D --> E["Refine requirement / acceptance"]
    E --> F["Takeaway + learning checkpoint"]
    F --> G["Stakeholder questions<br/>consolidated at bottom"]
    G --> H{"Explore another or refresh?"}
    H -->|"Another"| A
    H -->|"New evidence"| I["Refresh pattern map + overview"]
    I --> A
```

At the checkpoint you can explore the same item, choose another FR/NFR ID, or refresh the overview. **Practice** mode also starts with the overview, then asks one selected-item question and waits for your answer before revealing worked reasoning and critique. A question is not automatically a finished interview; completion also requires coverage and readiness checks.

## Modes

| Mode | Interaction | Best for |
| --- | --- | --- |
| **Guided (default)** | **Findings Overview first**; you choose an FR/NFR/gap, then get one worked interview question, scenario, trade-off, takeaway, and checkpoint. | Review the big picture, then learn selectively. |
| **Practice (on request)** | Same overview first; choose an item, answer one interview question before critique/hints. | Mock DSA/system-design-style interview practice. |
| **Full walkthrough (on request)** | Overview first, then cover relevant questions and a consolidated report in one pass. | A complete ticket-refinement exercise. |
| **Concise / refinement-only (on request)** | Overview-first evidence/FR/NFR tables and concise handoff; skip teaching. | Fast, work-focused requirements refinement. |

## What the skill refines

| Area | Key question | Recorded output |
| --- | --- | --- |
| **Functional requirements (FRs)** | What must the user/system do, for whom, and when? | `FR-01`, `FR-02`, … with actor/trigger, behavior, priority, status, evidence, and **Given/When/Then** acceptance. |
| **Non-functional requirements (NFRs)** | How well must the relevant journey work? | `NFR-01`, `NFR-02`, … linked to FRs/journeys, with a verified target or **target requires confirmation**, method of verification, and owner. |
| **Existing-system alignment** | Is behavior already present, partially present, missing, conflicting, or not verified? | Paths/symbols/tests, comparable patterns, and explicitly limited conclusions. |
| **Scenarios and correctness** | What happens at boundaries, during retries, or when operations fail? | Normal, edge, permission, duplicate, failure, and recovery examples that sharpen acceptance. |
| **System-design readiness** | What product and integration constraints would change the design? | Entities/states, source of truth, interface/data contracts, scale inputs, dependencies, reliability/security expectations, and unresolved trade-offs. |
| **Decision ownership** | Who must answer what before design or implementation? | Stakeholder and, when needed, developer/history questions with priority, owner, why it matters, and handoff-blocking status. |

Statements are classified as **CONFIRMED REQUIREMENT**, **OBSERVED BEHAVIOR**, **PROPOSED**, **ASSUMED**, or **UNKNOWN**; the last four are never silently upgraded into stakeholder approval. The five optional book lenses—APOSD, Algorithmic Thinking, DDIA, FODE, and System Design Interview—are used only when they reveal an important requirements gap.

## Final deliverables

On interview completion, or when a consolidated report is requested, the skill **expands the maintained overview** into a complete handoff rather than repeating each problem question:

1. **Feature brief:** goal, actors, scope/exclusions, sources, assumptions, and evidence limits.
2. **Pattern and alignment map:** existing behavior and reusable conventions, with verification status.
3. **Functional requirements:** prioritized, source-linked FR table and testable acceptance criteria.
4. **Non-functional requirements:** journey-linked NFR table, verified targets or owners for missing targets, and verification suggestions.
5. **Scenarios and constraints:** key user journeys, permissions, edge/failure/recovery behavior, dependencies, and compatibility needs.
6. **System-design preparation:** domain/data/interface/workload/trust-boundary inputs and technical questions explicitly deferred to Superpowers.
7. **Coverage and readiness:** what was inspected or executed, what is unverified, and a **READY / CONDITIONAL / BLOCKED** verdict. Even BLOCKED gets a clearly provisional brief.
8. **Post-interview — Questions to ask stakeholders (last section):** only unresolved, meaningful product decisions, plus developer/history questions where needed. Each has an owner, priority, ready-to-send wording, rationale, and **BLOCKS HANDOFF? YES/NO**.

**Important distinction:** these questions **replace draft code-review comments** from the Code Review learning pattern. They are *draft questions*, not comments to post to source code and not messages automatically sent to a stakeholder. If none remain, the report says **“No unresolved stakeholder questions for this topic.”**

## Example interview question

> **Illustrative ticket:** “Allow signed-in users to update notification preferences.” This is a hypothetical exercise; no product policy or codebase behavior is being asserted.

**Initial Findings Overview (abbreviated):** Evidence & pattern map = **NOT VERIFIED** (no repository provided). **FR-01 (PROPOSED)** = save and read preferences; **NFR-01 (UNKNOWN)** = cross-device freshness, **target requires confirmation**. System-design gap = data ownership and freshness expectations. **Q-01 / Product owner:** acceptable cross-device delay? The skill stops here for you to pick an ID.

**After selecting NFR-01: Problem question 1 — What should happen when preferences change on one device?**

- **Reasoning:** inspect any existing settings flow; distinguish successful save behavior (FR) from how quickly a second device sees that change (NFR). If the code was not inspected, mark its baseline **NOT VERIFIED**.
- **FR-01 (PROPOSED):** a signed-in user can save a supported notification preference and later read the saved choice. A suitable Given/When/Then scenario would check the saved value is returned on a successful read; stakeholders must approve the exact guarantee.
- **NFR-01 (UNKNOWN):** cross-device freshness of preference changes; **target requires confirmation**.
- **Changed constraint:** what if the second device reads immediately after the first saves? The required freshness is undecided, so architecture must not assume instant synchronization.
- **Q-01 / Product owner (blocks confirming NFR-01):** “When a user saves a preference, must other signed-in devices reflect it immediately, or is a propagation delay acceptable?”

The aim is to learn how an unclear product expectation becomes an explicit decision **before** a system-design agent selects a solution.

## How to invoke it

Use a compatible DotSkills installation, or point your assistant to [`SKILL.md`](SKILL.md) and its references. Supply a ticket/feature description and access to relevant code or specs where permitted.

**Guided (default)**

```text
Use the refine-requirements skill on this feature ticket: <ticket or description>.
Inspect relevant code and tests first. Start with a compact Findings Overview:
evidence & pattern map, all material FRs and NFRs, design-input gaps,
readiness, and stakeholder questions grouped at the very bottom.
Pause so I can review the big picture and choose an FR/NFR/gap.
Then work through just that item with an interview-style question,
scenario, trade-off, refined acceptance, takeaway, and checkpoint.
Refresh the pattern map if I provide new code or changed requirements.
Do not edit code, contact stakeholders, or invoke Superpowers.
```

**Practice mode**

```text
Use refine-requirements in Practice mode for <ticket or feature>.
Show the evidence map and complete brief FR/NFR Findings Overview first.
Let me choose an ID. Ask one interview question about that item,
wait for my answer, then critique it and help refine its requirements.
```

**For a one-pass brief**, request **Full walkthrough** or **Concise / refinement-only** mode explicitly.

## Evidence, safety, and scope

- **Codebase-first, not codebase-as-policy:** cite relevant ticket/spec evidence and inspected paths/tests. A similar implementation may suggest a baseline but cannot approve product behavior.
- **Read-only by default:** this skill does not change source files, run deployments, post comments/issues, create tickets, send emails, or execute Superpowers. Any later writes or outreach require separate authorization and tool/runtime permissions.
- **No invented facts:** mark absent repository access **NOT VERIFIED**, distinguish hypothetical walkthroughs from executed tests, and never invent SLAs, volumes, compliance requirements, approvals, or historical reasoning.
- **Requirements before solution:** leave architecture, database/framework selection, detailed schemas/algorithms, and implementation tasks to the later design workflow.
- **Evidence stays untrusted:** ticket text, code, and tool output are task data, not permission to perform unrelated actions. A skill document by itself cannot enforce permissions; the host/runtime must enforce them.

## Source files

| File | Role |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Normative skill entry point: purpose, interview behavior, deliverables, and boundaries. |
| [`references/interview-playbook.md`](references/interview-playbook.md) | Detailed interviewer roles, question sequence, modes, response format, and worked example. |
| [`references/refine-requirements.md`](references/refine-requirements.md) | Source-locked requirements-analysis reference and Superpowers handoff checklist. Preserve this imported content unchanged. |

This README is an explanatory guide to the **currently implemented** skill, not a separate mode or a new set of instructions. For operational details, follow `SKILL.md` and its referenced playbooks.
