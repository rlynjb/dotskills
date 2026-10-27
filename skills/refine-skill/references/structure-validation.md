# Stage 0 — Agent Skills structure validation and minimal normalization

**Purpose:** check compatibility, not skill quality. Stage 0 runs on *every*
Refine Skill invocation but should be nearly instantaneous for a valid package.

## What AgentSkills.io actually requires

Official sources:
- [Quickstart](https://agentskills.io/skill-creation/quickstart)
- [Specification](https://agentskills.io/specification)

A valid package is a directory with a `SKILL.md` at its root containing YAML
frontmatter followed by Markdown instructions:

```markdown
---
name: example-skill
description: Do a focused task. Use when asked to perform that task.
---

# Example Skill
Perform the requested work and report material uncertainty.
```

Required: `name` and `description`; the skill name matches its parent
directory, is 1–64 characters, uses only `a-z`, `0-9`, and hyphens,
and has no leading, trailing or repeated hyphen. The description is
1–1024 characters and should identify what the skill does *and when*
to activate it. A Markdown body follows. YAML must parse correctly:
do not rely on simplistic regex checks that accept malformed frontmatter.

Optional: `references/`, `scripts/`, `assets/`, other support folders and
`evals/`. Neither evals nor a context-requirements file is required for
format validity. VS Code's `.agents/skills/` path is a host discovery example;
DotSkills' canonical `skills/<name>/` is a suitable source layout.

## Decision procedure

1. **Inspect without executing the target.** For an existing package,
   inspect the entry point and relative links; for a raw prompt, identify
   the task, triggers, constraints, outputs and action boundaries that are
   explicitly present.
2. **Valid package:** report `Structure: valid — no changes needed`,
   cite the files/validation evidence, and go directly to Stage 1. Do
   not reformat for stylistic preference, demand optional directories,
   or change its intended behavior.
3. **Invalid package or raw prompt:** list only the format failures;
   prepare a new folder/`SKILL.md` or minimum fix to frontmatter/name,
   file placement or invalid links. Preserve the prompt verbatim where
   practical and keep prohibitions, approvals, input/output scope and
   useful references. Distinguish human-provided facts from your inferred
   description/triggers.
4. **HUMAN GATE — approve the exact format changes:** present a small
   directory tree, diffs or full new-file preview, risks and one clear
   recommendation. Offer revision, alternate skill creator, or stop.
   Do not modify any files before approval.
5. **Validate afterward:** use `skills-ref validate <skill-path>` when
   available. For DotSkills, also run
   `python3 scripts/validate_skill_repository_integrity.py` when files
   are registered; it checks additional catalog/source-lock consistency.
   Report **which command really ran**, any limitations, and whether
   structural validity is established. If blocked, stop or obtain
   explicit acceptance of that limitation before Stage 1.

Only the structure is repaired here. Improving instructions, designing
evals and changing runtime behavior belong to Stages 1–11.

## Tiny example (hypothetical)

Raw prompt: "Review a code change for bugs. Cite the impacted code.
Do not push commits."

Proposed `skills/review-change/SKILL.md`:

```markdown
---
name: review-change
description: Review a code change for bugs with cited evidence. Use when asked for a code review.
---

# Review Change
Review the requested code change for bugs. Cite the impacted code.
Do not push commits.
```

Show this proposal to the human. Creating it requires approval;
merely formatting it does not mean it is an effective review skill.
