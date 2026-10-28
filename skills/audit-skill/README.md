# Audit Skill

**`audit-skill` is a read-only, overview-first way to understand a large agent skill before making changes.** Instead of manually reading a long `SKILL.md` and every supporting reference, have a coding agent extract the skill's contract, trace its workflow and evidence, identify overlap with other skills, and surface validation gaps for review.

**Output:** a concise, evidence-backed audit report, a prioritized gap list, and three *proposed* test cases. **It does not change skills, run those test cases, or claim that a static review proves runtime behavior.**

## The big picture

```text
Identify target skill(s)
       ↓
1. Extract a Skill Contract — what the skill promises
       ↓
2. Map workflow + source evidence — how decisions are described
       ↓
3. Compare responsibilities — what overlaps or conflicts
       ↓
4. Audit validation — what protects conclusions, and what is missing
       ↓
5. Draft three test cases — how to verify behavior later
       ↓
Human reviews the overview → selects a finding to investigate
```

The guiding idea is **understand first, verify claims, and only then consider improvements**. A validation layer should supplement work the skill already performs rather than repeating requirements analysis.

## When to use it

Use Audit Skill when an existing skill is too long to inspect line by line, its workflow or handoff is unclear, two skills appear to assess the same things, or you want to decide where an additional validation gate belongs.

The starter use case is the workplace **Sprint Assessment** skill compared with DotSkills' **Refine Requirements** skill. The possible distinction is *requirements refinement versus sprint-readiness assessment*, but that is a **hypothesis** until the actual skill instructions and evidence have been inspected. The prompt is reusable for other skills.

## What it needs

- The target skill's `SKILL.md` or an authorized repository path.
- Relevant `references/`, templates, scripts, tests/evals, and handoff artifacts when available.
- Optionally, a second skill to compare.
- Source branch or revision where available.

If a comparison skill or repository is inaccessible, the agent marks that portion **NOT ASSESSED / NOT VERIFIED** instead of making up findings. Keep proprietary workplace content in its approved environment; this public DotSkills repository contains only the generic audit methodology and the starter prompt, **not** a copy of Sprint Assessment.

## From overview to details

| Phase | Question answered | Deliverable |
| --- | --- | --- |
| **1. Inventory** | What is this skill for, when does it trigger, and what does it consume or produce? | **Skill Contract** |
| **2. Workflow** | What are the major steps, decisions, and handoffs, and which files support them? | **Workflow Map** and **Evidence & Pattern Map** |
| **3. Overlap** | Which responsibilities are shared, duplicated, distinct, or contradictory? | **Overlap Analysis** (when a comparison is available) |
| **4. Validation** | What checks already exist, and where might unsupported conclusions get through? | **Existing Safeguards**, ranked **Gaps & Risks**, and proposed **Validation Layer** |
| **5. Test design** | What representative inputs would demonstrate correct or incorrect behavior? | **Three test scenarios** with expected outcomes and pass/fail assertions, marked **NOT RUN** |

### 1. The Skill Contract

The compact contract covers eight dimensions: **Purpose** (the problem solved), **Trigger** (when to invoke), **Inputs** (required information), **Workflow** (major stages), **Decisions** (judgments and criteria), **Outputs** (artifacts), **Validation** (checking mechanisms), and **Handoff** (next action or consumer).

A contract is an *extract of documented instructions*, not proof that an agent consistently follows them.

### 2. Workflow and evidence

The auditor reads the entry point, then follows only pertinent references. It creates an evidence map of **stage / claim → file and line → instruction or check → verification status → gap**. It distinguishes a written instruction from a test or script that implements a check, and both from an observed result.

### 3. Skill overlap

For Sprint Assessment vs. Refine Requirements, review their requirements coverage, stakeholder questions, technical uncertainties, sizing, readiness decisions, and handoff. Some overlap is useful: a planning skill may need to read refined requirements. The audit flags **duplicate decisions and inconsistent conclusions**, not merely shared topics.

### 4. Validation gaps

Check completeness of functional and non-functional requirements, source traceability, unsupported assumptions, acceptance criteria, technical dependencies, sizing justification, and readiness criteria. **Identify existing safeguards first**, then rank missing or weak controls **High / Medium / Low**, citing evidence and confidence.

A possible added gate asks: *Does the sprint-readiness recommendation actually follow from the requirements and technical evidence?* Labels like **Ready / Needs Clarification / Blocked** are proposals unless the target skill already defines them.

### 5. Test scenarios — proposed, not executed

The starter prompt defines three representative cases: **well-defined and ready**, **ambiguous requirements**, and **unresolved technical dependencies**. For each, define inputs, expected output, and objective pass/fail assertions. The first audit **does not run** those tests or score model behavior.

## Initial report and review flow

The first response should be **skimmable**, in this order: Executive Summary; Skill Contract; Evidence & Pattern Map; Workflow Map; Overlap Analysis; Existing Validation; Validation Gaps & Risks; Proposed Validation Layer; Three Test Scenarios; **Questions Requiring Human Decisions**. The last section invites selection of one finding for a deep dive.

Only after review should the agent investigate a chosen finding in detail. It should not ask the user to review each requirement or question separately before showing the overall picture.

## How to invoke

Use with a coding agent that has authorized, read-only access to the target skill:

```text
Use audit-skill to analyze our Sprint Assessment skill.
Compare it with refine-requirements if accessible.

Read only. Start with the Skill Contract, Evidence & Pattern Map,
workflow, overlap, existing checks, validation gaps, and three
proposed test cases. Keep the first report overview-first,
include file and line evidence, and do not modify files,
execute tests, or begin implementation.

Wait for me to choose which finding to investigate.
```

To review a different skill, replace the two names in the example.

## Relationship to other DotSkills skills

| Skill | Responsibility |
| --- | --- |
| **Audit Skill** (this one) | **Read-only diagnosis** of skill instructions, overlap, and validation coverage; proposes test cases. |
| [Refine Skill](../refine-skill/SKILL.md) | Human-gated **behavioral evaluation and refinement** after scope, tool permissions, and safe evaluation conditions are established. |
| [Refine Requirements](../refine-requirements/SKILL.md) | **Requirements engineering** for a feature or ticket, including FR/NFRs, evidence, acceptance, and design inputs for Superpowers. |

This skill is the **first-pass inspection**, not a substitute for Refine Skill's paired runs, grading, and regression testing. It does not invoke Superpowers or decide actual sprint commitments.

## Files

- [`SKILL.md`](SKILL.md) — installable agent instructions and the generalized five-phase audit workflow.
- [Original Sprint Assessment audit prompt](references/sprint-assessment-audit.md) — the starter prompt from the initial discussion, preserved so it can be reused verbatim.

## Boundaries and current status

The audit is **read-only by default and throughout its first-pass workflow**. It makes no commits, stakeholder contact, skill edits, agent executions, or test runs. Inspecting instructions alone cannot establish real-world quality or safety; runtime evidence and authorized evaluations are separate steps.

**Status:** starter skill and documentation only. No Sprint Assessment source files have been inspected here, and no audit or behavioral tests have been executed.
