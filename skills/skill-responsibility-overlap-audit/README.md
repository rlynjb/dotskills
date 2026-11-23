# Skill Responsibility & Overlap Audit

A focused, **read-only Stage 2 investigation skill** for clarifying responsibilities before writing integration contracts. Works with one skill or any set of skills in a repository-aware coding agent.

## What it produces

1. Individual reviews of the same **six considerations**: Inputs, Responsibilities, Outputs, Handoffs, Boundaries and Feedback. The first three receive deeper analysis; the last three identify future design questions.
2. **Side-by-side comparisons** for two or more skills, so ownership and differences are visible in the same rows. Large sets are split into groups with an overall synthesis.
3. **Optional connection documentation proposals, per affected skill** when Handoffs, Boundaries, or Feedback reveal a material issue. Keep each skill independently usable with complete inputs, workflow and outputs; suggest passing the other skill's result as optional context only, never as an automatic invocation.
4. Evidence-backed classification of legitimate shared behavior, complementary roles, duplication, conflicts and unclear ownership.
5. Missing responsibilities/gaps, High/Medium/Low recommendations, and questions for human review.

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

**Default: keep it in each affected `SKILL.md`.** The core rules belong there: standalone inputs and outputs, what each skill owns, a short optional-handoff condition, approval/permission limits, and feedback to the responsible human owner.

**Add an optional local reference only when warranted** by substantial mapping rules, examples, conditional handoffs or conflict-resolution guidance. A skill should point to **its own** reference, never require a shared file or another skill's installation to function. Prefer self-explanatory direction names:

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

This tree is **illustrative**, not a requirement to create files. For a short connection, the two `SKILL.md` files are enough. Use `handoff` for one transition or `handoffs` for multiple transitions within a single file; inspect existing references before suggesting duplicates. The audit recommends file placement and wording **per affected skill**, but does not edit target skills or create their handoff files.

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
