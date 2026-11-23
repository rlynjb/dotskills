# Skill Responsibility & Overlap Audit

A focused, **read-only Stage 2 investigation skill** for clarifying responsibilities before writing integration contracts. Works with one skill or any set of skills in a repository-aware coding agent.

## Communication style

Use [Senior Engineer → Junior Developer Communication Guideline](../../docs/senior-engineer-mentoring-communication.md) for clear, evidence-based explanation of significant findings. The audit's `SKILL.md` simply references this guideline and retains only the task-specific formatting and evidence boundaries. The referenced file must be accessible to the agent. This is a communication approach, not a separate teaching skill or extra audit step.

## What it produces

1. Individual reviews of the same **six considerations**: Inputs, Responsibilities, Outputs, Handoffs, Boundaries and Feedback. The first three receive deeper analysis; the last three identify future design questions.
2. **Side-by-side comparisons with matching layouts for Primary C1–C3 and Supporting C4–C6.** Both tables must have `Consideration` as the first column and the **same skills as columns**; C1–C6 are row labels, never column headings. Material findings retain F-xx IDs and concise Finding / Evidence / Assessment / Why / Recommendation in the relevant skill cell. Exact long wording may use an adjacent row **in the same table**, without HTML or detached findings.
3. **Optional connection documentation proposals, per affected skill** when Handoffs, Boundaries, or Feedback reveal a material issue. Keep each skill independently usable with complete inputs, workflow and outputs; suggest passing the other skill's result as optional context only, never as an automatic invocation.
4. Evidence-backed classification of legitimate shared behavior, complementary roles, duplication, conflicts and unclear ownership.
5. **Optional coordinator assessment** when multiple skills have a material combined-workflow routing, sequencing, context or feedback problem. Explain why a separate coordinator is needed—or why optional handoff docs and copyable prompts are enough.
6. Missing responsibilities/gaps, High/Medium/Low recommendations, and questions for human review.

Assessment labels describe preliminary engineering judgment, not evidence certainty, High/Medium/Low priority or approval. **KEEP** is a useful no-change result; **VERIFY** means collect evidence before proposing a fix. The final recommendations reference the F-xx identifiers inside the consideration rows without repeating every explanation.

When a meaningful issue comes from ambiguous instructions, the matching C1–C6 row may also contain **Current wording → Concern → Recommended wording — PROPOSED**. For long exact quotes, put that detail in an **immediately adjacent table row** using the same F-xx ID. This is optional, not a seventh consideration, a new findings section, or a reason to rewrite well-written instructions. **No HTML tags are used.**

It does **not** decide the future architecture, draft contracts, execute skills, make repository edits, or mark recommendations as approved.

## Example invocation

```text
Use skill-responsibility-overlap-audit on:
- skills/first-skill
- skills/second-skill
- skills/third-skill

Goal: identify responsibilities, overlaps, and missing ownership
before integration design.

Use direct file/line evidence and show comparisons side by side.
Do not make edits or draft integration contracts.
```

An optional workflow description or harness name helps explain which handoffs matter, but neither is required. Supply commit/branch revisions when reproducibility matters.

## How to interpret overlap

- **Shared input:** two skills read the same requirements for different reasons. Often healthy.
- **Duplicated decision:** both independently claim the final authority on the same requirement. May create conflicting results.
- **Handoff gap:** a skill expects information no preceding skill promises to produce.
- **Unverified:** the evidence does not establish a capability or missing capability. A documented promise alone is not runtime proof.

## Optional connections preserve standalone skills

Suppose one skill produces a product brief and another refines requirements. **Illustrative only:** either skill may be run on its own from its supported inputs. If a brief already exists, a human may pass it to refinement as useful context. Refinement can suggest changes to the brief, but does not silently revise it; the brief's owner reviews any proposed updates. Neither skill must invoke or automatically run the other.

When the audit finds handoff, boundary, or feedback issues, it may recommend **wording for each affected skill** under five labels: *Standalone use*, *Optional handoff*, *Responsibilities*, *Boundaries*, and *Feedback*. These are **proposals for human review**, not edits to the audited skills or formal contracts.

If inspection shows a skill actually requires a partner's output, the report must **not** pretend it already supports standalone use. Changing a documented required dependency would be a separate design decision. Security or authorization rules may also require enforcement beyond documentation.

### Where to document an optional handoff

**During Stage 2, recommend a *planned* `Optional Handoffs` note in each affected `SKILL.md`.** The core rules belong there: standalone inputs and outputs, what each skill owns, the possible future handoff direction, approval/permission limits, and feedback to the responsible human owner. Explicitly mark the connection **PLANNED / PROPOSED — NOT IMPLEMENTED**. The purpose is to communicate the integration *plan* to a future reviewer, not to assert that the skills have been integrated.

**Recommend an optional local reference as a potential Stage 3 artifact only when warranted** by substantial mapping rules, examples, conditional handoffs or conflict-resolution guidance. If it does not exist, label its path **PLANNED — NOT CREATED**. A skill may later point to **its own** reference, never require a shared file or another skill's installation to function. Prefer self-explanatory direction names:

```text
skills/
├── prd-development/
│   ├── SKILL.md
│   └── references/
│       └── prd-to-refinement-handoff.md     # Only if detailed
└── refine-requirements/
    ├── SKILL.md
    └── references/
        └── refinement-to-prd-handoff.md     # Only if detailed
```

This tree is **illustrative**, not a requirement to create files. No target skill files or handoff references are created by this audit. For a short connection, the two *proposed* `SKILL.md` notes are enough. Stage 3 will decide the actual integration contract and whether any proposed reference file is needed. Use `handoff` for one transition or `handoffs` for multiple transitions within a single file; inspect existing references before suggesting duplicates. The audit recommends file placement and wording **per affected skill**, but does not edit target skills or create their handoff files.

### When to recommend an optional coordinator skill

The audit now checks **whether multiple skills need more than an optional handoff**. A missing field or unclear ownership by itself doesn't justify a new coordinator.

- **NOT NEEDED:** Each skill's own handoff instructions plus copyable next-step prompts are enough.
- **OPTIONAL COORDINATOR RECOMMENDED:** A requested combined workflow repeatedly needs to select a starting skill, sequence stages, retain source/requirement IDs and revisions, manage human-reviewed returns, or report the end-to-end result. Explain why that work should be owned in one optional entry-point skill rather than spread across the individual skills.
- **DEFER / UNVERIFIED:** The coordination need, supporting source evidence or host execution capability is unclear.

When warranted, the audit may propose a separate `skills/<workflow-goal>-workflow/SKILL.md` with a **router + short sequential workflow** concept. It would own only coordination: where to start, what context to carry, how to present the next action and who reviews proposed updates. It **must not** take over the individual skills' decisions or remove their standalone invocation. The audit compares this with the simpler manual/copyable-prompt route, and **does not create the coordinator** or claim Markdown alone guarantees runtime dispatch.

## How this differs from other DotSkills skills

- **This skill:** investigates current responsibilities and gaps only; stops before integration design.
- **[Audit Skill](../audit-skill/SKILL.md):** broader Q-01–Q-10 quality review, proposed boundaries and conditional contracts, human-review workflow, and validation preparation.
- **[Evaluate Skill](../evaluate-skill/SKILL.md):** guided evaluations and evidence-based skill improvements, where an authorized runner exists.
- **[Profile Agent Workflow](../profile-agent-workflow/SKILL.md):** read-only analysis of dispatch and resource traces against approved routing rules.

The smaller scope is deliberate: first investigate **who owns what**, then address **how skills communicate and what they guarantee** in a separate design stage.

## Files

- [SKILL.md](SKILL.md) — installable skill instructions.
- [Report template](references/report-template.md) — aligned comparison layout.
- [Evaluation cases](evals/evals.json) — static expected-behavior cases; not evidence of an evaluation run.
- [Copyable original prompt](../../docs/skill-responsibility-overlap-audit-prompt.md) — standalone non-installable prompt.

DotSkills catalog registration makes the skill discoverable; it is not automatically installed in Codex, ChatGPT, or another harness. Check that environment's packaging and available tools.
