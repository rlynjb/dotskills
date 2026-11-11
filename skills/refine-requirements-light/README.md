# Refine Requirements Light

**A noninteractive, verification-first SDI assessment for workplace Jira tickets in an existing application codebase.**

This skill investigates the relevant **actual code** before recommending how a feature should fit. It produces one concise engineering overview: requirements, existing pattern or subsystem evidence, a minimal high-level proposal, relevant full-stack data flow, and practical trade-offs.

It complements [Refine Requirements](../refine-requirements/README.md), which guides you through a longer collaborative design process with interactive exploration and explicit decision approvals.

## How it works

| SDI step | What it does | Result |
| --- | --- | --- |
| **1. Understand the problem and scope** | Read the assigned ticket, FRs/NFRs, acceptance criteria, constraints and unknowns | Short ticket and scope summary |
| **2. Verify existing code, then propose high-level design** | Find possible components/subsystems in the application, inspect their real behavior, identify compatible patterns, and only then recommend reuse, adaptation or a justified addition | Evidence-backed reuse map and current → proposed flow |
| **3. Targeted deep dive** | Check relevant code paths, contracts, data ownership and, when applicable, full-stack read/write flows | Focused implementation/data-flow assessment |
| **4. Wrap up** | Compare worthwhile options, assess risks, validation needs and implementation footprint | Recommendation, trade-offs, blockers and readiness |

### Verify before recommending

An existing application may already contain a reusable feature, subsystem, API or pattern—but that is a **hypothesis until inspected**. Step 2 must distinguish:

- **FOLLOW:** verified pattern already fits.
- **ADAPT:** verified pattern fits with a scoped change.
- **NEW REQUIRED:** inspection and requirements justify adding something new.
- **NO SUITABLE PATTERN FOUND IN INSPECTED SCOPE:** relevant search was performed, but absence across the entire application is **not proven**.
- **NOT VERIFIED:** code access or evidence is insufficient.

For each finding, record **where it was found** (path, symbol, contract or test), **what it currently does**, **how it relates to the ticket**, and any unresolved uncertainty. The recommendation follows the evidence, not an assumed architecture.

**Prefer the smallest coherent extension to verified application patterns** over parallel abstractions, duplicate logic, or a wholesale redesign. Respect actual team conventions and application constraints; do not force reuse if the contracts or behavior do not fit.

## Engineering considerations

The four-step **SDI framework** organizes the analysis. Within each step, examine only the engineering concerns that matter to the ticket and verified implementation:

- **Data behavior:** models, queries, transactions, consistency, freshness, concurrency, indexing, caching and recovery.
- **Data movement:** origin, validation, transformations, source of truth, read/write paths, consumers, contracts and data quality.
- **Code structure:** module responsibilities, interfaces, coupling, duplication, maintainability and compatibility.
- **Correctness and reliability:** edge cases, computational cost, authorization, dependency failures, observability and focused verification.

These are **situational engineering checks**, not a required checklist or a reason to override company conventions. Explain applicable trade-offs in plain engineering terms and support claims with code or ticket evidence.

## Example of an output (hypothetical)

For an audit-records filtering ticket, the report would:

1. Clarify which users can filter, supported fields and acceptance cases.
2. **Search for and verify** the actual audit UI, endpoint, service and query mechanism. If a shared filter pattern exists and fits, recommend adapting it with code evidence; if it is unverified, say so.
3. Trace the confirmed and proposed **UI → API → service → data store → response** paths, separating read/write behavior and identifying any data consistency/query issues.
4. Summarize the minimum expected code changes, risks, tests and ticket questions.

It does **not** claim these specific components exist without examining the repository.

## Invocation

```text
Run refine-requirements-light for Jira ticket <KEY> in this application.
First inspect and verify relevant existing code paths, subsystems,
patterns, contracts, tests and documented team conventions.
Then give me one concise four-step SDI overview:
1. Requirements and scope
2. Verified existing patterns and high-level design recommendation
3. Relevant implementation/data flow (when applicable)
4. Trade-offs, risks, validation and readiness
Prefer the smallest compatible change. Label unverified findings.
No interview, learning menu, source edits, Jira updates or implementation.
```

## Boundaries

- **One-pass output:** No interactive questions, lessons, checkpoints or decision-approval flow. Unknowns become a short questions/blockers section at the end.
- **Read-only analysis:** No code modification, Jira mutation, deployment, or invoking a coding agent. The report is a proposal, **not implementation authorization**.
- **Evidence over assumptions:** Existing code proves observed behavior, not approved product intent. Missing access, unverified design paths, measurements and tests must be clearly labeled.
- **Workplace data:** Respect access controls and do not move proprietary content into public sources.

The operational contract is [`SKILL.md`](SKILL.md). The full skill's interactive procedures are **not inherited**.
