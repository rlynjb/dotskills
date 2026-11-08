# Audit Skill

**`audit-skill` is one read-only, overview-first workflow for reviewing one or more agent skills.** It automatically adjusts its scope from independent single-skill analysis to multi-skill responsibility and handoff analysis. There is **no Explore/Audit/Compare mode selection**.

The first result is a compact, complete review of what each skill does, how it works, what evidence exists, what is unverified, and what the team should discuss. It also **prefills DFRDE Stage 1 — Discover** with sourced answers and targeted human-confirmation questions, without editing documents or approving decisions. Choose any finding or topic afterward for a deeper explanation.

## Table of contents

- [How it works](#how-it-works)
- [What the first report contains](#what-the-first-report-contains)
- [DFRDE Stage 1 — Discover prefill](#dfrde-stage-1--discover-prefill)
- [Quality and standards checks](#quality-and-standards-checks)
- [Cross-platform compatibility](#cross-platform-compatibility)
- [How to invoke](#how-to-invoke)
- [Evidence and safety rules](#evidence-and-safety-rules)
- [Relationship to other DotSkills skills](#relationship-to-other-dotskills-skills)

## How it works

```text
                 One or more target skills
                           |
             Read-only source inspection
                           |
              Audit Skill — At a Glance
              /                       \
       For every skill          Only with 2+ skills
       - Contract/profile       - Responsibility matrix
       - Standards review       - Shared/unique decisions
       - Current-state flow     - Conflicts/duplication
       - Quality & evidence     - Handoff/integration options
       - Runtime parity                |
              \                       /
               Findings + NOT RUN eval proposals
                           |
                 Human selects topic/finding
                           |
               Cited, focused deep dive
                           |
              Human decides next workflow
```

1. **Find and inspect** each available skill, references, agents, manifests, tests and relevant history, with source revision and line evidence.
2. **Apply the same review criteria to every skill**, whether one or several were supplied.
3. **Add relationships automatically** only when there are two or more accessible skills. Otherwise mark inter-skill comparison NOT APPLICABLE.
4. **Report all criteria at a glance** with existing safeguards before risks, source limitations and proposed tests that have **not** run.
5. **Wait for a requested deep dive.** Never silently change the skill or run a behavioral evaluation.

If a named target cannot be accessed, label it NOT ASSESSED and avoid constructing a fictitious comparison.

## What the first report contains

The report begins **Audit Skill — At a Glance** (not a mode guide or a long question menu):

| Output | What it communicates |
| --- | --- |
| **Target/source boundary** | Which skills and revisions were inspected; what was inaccessible; no tests or target skill execution |
| **Skill profile(s)** | Purpose, activation, inputs, dependencies, steps/decisions, agents and tools, outputs, permissions, failures and handoffs |
| **Quality dashboard** | Q-01–Q-10 verdicts for each skill, supporting paths/lines, and key unknowns |
| **Agent Skills specification matrix** | Required format vs recommended/optional structure; normative claims tied to the published specification |
| **Mermaid current-state diagram(s)** | One flowchart per target, including decisions, delegation, stop conditions and unverified edges |
| **Relationship analysis (2+ only)** | Shared/unique responsibility matrix, conflicts, duplicate decisions, and proposed handoff/compose/merge alternatives |
| **Cross-runtime matrix** | Explicit host-by-capability compatibility evidence and adapter needs |
| **Evidence and risk map** | Existing safeguards first; source-backed F-xx findings, impact/confidence, and unanswered questions |
| **Evaluation recommendations** | At least three realistic synthetic cases and pass/fail criteria, all **NOT RUN**, plus smallest next step |
| **DFRDE Stage 1 Discover handoff** | Draft answers to S1-Q01–S1-Q10, problem hypothesis, known constraints, unresolved evidence, priority team questions and pending review gate |

The main report remains concise. A selected `F-xx`, `Q-xx`, `S1-Qxx`, diagram, workflow stage or contract receives an evidence-backed deep dive without switching modes. Never present a hypothetical path as a tested run.

### Mermaid example (illustrative only)

```mermaid
flowchart TD
    A["Skill receives task"] --> B{"Required evidence available?"}
    B -->|Yes| C["Documented evaluation steps"]
    B -->|No| D["Clarify or stop as unresolved"]
    C --> E["Evidence-backed result"]
    D --> E
```

A real diagram must come from the target files and label which edges are inferred or unverified. For two skills, keep **as-is** diagrams distinct from any **PROPOSED** integration diagram.

## DFRDE Stage 1 — Discover prefill

The Audit Skill **automatically produces a read-only Stage 1 Discovery draft** after inspecting one or more agent skills. Its purpose is to **answer the questions that repository evidence can answer before a team review** and surface only the remaining human or runtime questions.

Use [the generic DFRDE engineering review template](../../docs/dfrde/engineering-review-template.md#1-discover--what-problem-and-existing-reality-are-we-working-with) as the destination for an approved copy. The [discovery handoff contract](references/dfrde-stage-1-handoff.md) defines what to prefill.

| Question status | What to do |
| --- | --- |
| **ANSWERED BY EVIDENCE** | Give the concise answer, inspected version and exact path:line; distinguish documented intent from observed behavior |
| **NEEDS CONFIRMATION** | Ask a stakeholder to confirm business purpose, user intent, ownership or proposed success metrics |
| **OPEN DECISION** | Carry architecture/ownership alternatives into Stage 2 rather than letting the agent choose |
| **NOT VERIFIED** | Identify missing source or runtime evidence and how to obtain it safely |

Stage 1 outputs include a **PROPOSED problem statement**, known/unknown requirements and constraints, a current-state inventory, evidence backlog and **priority teammate questions**—not a transcript of every question already settled by the code. No team approval, live execution or file modification is implied.

### Audit-assisted invocation example

```text
Use audit-skill on the existing skill(s). Give the full At a Glance
review and prefill all DFRDE Stage 1 Discover questions (S1-Q01–S1-Q10).
Cite inspected files/lines and versions. Mark business goals and desired
success metrics PROPOSED until confirmed. Separate answered facts from
needs-confirmation, open design decisions and not-verified runtime
questions. Present a meeting-ready shortlist. Do not run tests, edit
the engineering record or advance to Stage 2.
```

## Quality and standards checks

The [Agent Skills specification](https://agentskills.io/specification) is the standards baseline for `SKILL.md`, naming/frontmatter and supporting resources. Its actual requirements are distinct from the team-defined engineering quality expectations below.

| ID | Requirement | What a reviewer should find |
| --- | --- | --- |
| Q-01 | Purpose and boundaries | Intended job, who uses it, when it should not activate |
| Q-02 | Activation and discovery | Invocation, triggers, incorrect-trigger behavior |
| Q-03 | Structure, inputs and dependencies | Source files, context, tools/MCP, credentials and environment assumptions |
| Q-04 | Workflow and orchestration | Steps, decisions, dynamic vs named agents, delegation, approvals and result aggregation |
| Q-05 | Contracts and outputs | Explicit inputs, outputs, guarantees, invariants, ownership and failed handoffs |
| Q-06 | Context and trust | Provenance, freshness, conflicting or untrusted information and evidence |
| Q-07 | Permissions and side effects | Enforced authorization, least privilege, scoped writes and human approval |
| Q-08 | Failure and stop behavior | Unavailable tools, ambiguous inputs, partial batches, retries, stop conditions |
| Q-09 | Evals and observability | Existing tests, CI, scenarios, execution traces, expected and observed outcomes |
| Q-10 | Lifecycle and portability | Owners, versioning, review/rollback, compatible hosts, adapters and regressions |

For each applicable item show **PASS (static)**, **GAP**, **UNVERIFIED**, or **NOT APPLICABLE**, with a reason and evidence. A written instruction to check something does not prove the check actually ran.

The separate **standards compliance matrix** distinguishes required specification elements, recommendations and experimental/host-specific behavior. It should not imply full standards conformance if the published specification was not consulted or a validator was not run.

## Cross-platform compatibility

An Agent Skills-compatible Markdown directory does **not** guarantee that a multi-agent workflow behaves the same in every harness. The review explicitly covers:

1. Skill packaging and installation.
2. Discovery, triggers and invocation.
3. Context loading and configuration inheritance.
4. Tools, shell names, MCP integrations and local paths.
5. Agent delegation, concurrency and worker result aggregation.
6. User identity, permission and approval enforcement.
7. Output schemas, error handling, timeouts and partial failures.
8. Eval evidence, adapter ownership and supported versions.

Use a runtime × capability matrix with **SUPPORTED (evidenced)**, **ADAPTER REQUIRED**, **NOT SUPPORTED (evidenced)** and **NOT VERIFIED**. When runtimes are unspecified, say so. Do not assume Claude Code and Codex have interchangeable tool names or delegation APIs.

## How to invoke

**One skill — no mode to select:**

```text
Use audit-skill on Sprint Assessment in this repository.
Start with a complete at-a-glance report including the skill contract,
Mermaid current-state flow, Agent Skills compliance matrix, ten quality
requirements, cross-platform compatibility, risks and NOT RUN eval cases.
Cite file/line evidence. Do not execute the skill or edit anything.
```

**Two skills — comparison happens automatically:**

```text
Use audit-skill on Sprint Assessment and Refine Requirements.
Inspect each independently, then include the ownership/overlap matrix,
conflicting decisions, missing handoffs and PROPOSED integration choices.
Include standards, quality, runtime-compatibility and evidence checks.
Read-only; no execution or edits. Pause for my review.
```

**Focused follow-up:**

```text
Deep dive F-02. Show the exact source evidence, implementation status,
risk, trade-offs and the smallest useful validation step.
```

The [generic Stage 1 handoff contract](references/dfrde-stage-1-handoff.md) defines the reusable Discovery output. The optional [Sprint Assessment example](references/sprint-assessment-audit.md) provides task-specific prompts, not an alternative workflow.

## Evidence and safety rules

- **DOCUMENTED INSTRUCTIONS** = written guidance; **IMPLEMENTED CHECK** = code/config check found; **OBSERVED RESULT** = actual authorized trace; **NOT VERIFIED** = not established.
- Cite relevant file paths and lines; distinguish a referenced file from an actually loaded file.
- Report existing safeguards **before** gaps. Missing evidence must not become a fabricated failure or a passing test.
- The audit is **read-only** and never executes target agents, scripts, evals, live Jira/Confluence actions or repo mutations. Approved read-only file/repository sources may be inspected.
- Prompt text cannot enforce permissions. Only host/tool/server controls can enforce read-only authority.
- Preserve approved workplace data boundaries; do not paste confidential sources into a public repository.

## Relationship to other DotSkills skills

| Skill | Responsibility |
| --- | --- |
| **Audit Skill** (this skill) | Single workflow for independent and multi-skill source audits, compliance, contracts, trust, diagrams and portability, plus evidence-prefilled DFRDE Stage 1 questions; **no execution or edits** |
| [Evaluate Skill](../evaluate-skill/SKILL.md) | Separately authorized behavioral evaluation, diagnosis, human-approved changes and regression review; runtime safety gates still apply |
| [Integrate Skills](../integrate-skills/SKILL.md) | Draft collaboration/architecture walkthrough for connecting independently reviewed skills; not an implementation runner |
| [Learn Repo](../learn-repo/SKILL.md) | Guided learning of an entire codebase rather than skill-specific audit |

**Recommended path:** Audit as-is → discuss contracts/decisions with humans → separately authorize evaluation or implementation when warranted.

**Status:** This revision defines a single review procedure, not a proven new agent runtime or eval engine. Static documentation checks alone do not establish behavioral reliability.
