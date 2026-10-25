# TODO: Skill name — task guide

Authoring note: rename this file to match its subject (for example,
`review-change.md`) and update the link in the package's `SKILL.md`.
Replace the placeholders and remove these authoring notes and the illustrative
example before using the skill, unless the example is relevant to its task.

This is supporting guidance, not a second skill entry point. The package-root
`SKILL.md` holds the name/description frontmatter and explains when to read this
file. Supporting reference filenames are descriptive; they need no frontmatter.

## Minimal task-guide template

### Purpose

TODO: State the specific task and useful outcome in one sentence.

### Required context

Apply [context quality and requirements](context-quality-and-requirements.md).
TODO: Identify the particular inputs this procedure uses without duplicating
the full input and evidence rules from that file.

### Procedure

1. Confirm the requested outcome, scope, and permitted actions.
2. TODO: Inspect the relevant inputs and identify the evidence needed.
3. TODO: Apply one concrete task-specific rule or decision.
4. Check the result against the requirements; state missing evidence.
5. Return the requested output with sources and material uncertainty.

### Decision rules

- TODO: If a stated condition is supported by evidence, take the specified action.
- TODO: If decisive evidence is missing or conflicting, explain the limitation
  and identify the next check rather than inventing a conclusion.

### Output

TODO: Define the response format, required evidence, and completion criteria.
Report only checks actually performed.

## Filled-in example: review a small code change

Illustrative authoring example; adapt or remove it when creating your skill.

### Purpose

Review a code change against its stated requirement and report supported defects.

### Required context

The requested behavior, the diff, relevant callers, and available tests.
Apply the companion context-quality rules before relying on those inputs.

### Procedure

1. Identify what behavior the change is supposed to provide.
2. Read the changed code and relevant callers or guards.
3. Trace one concrete input through the affected behavior.
4. Compare the observed behavior with the stated requirement.
5. Report a defect only when the evidence supports it; otherwise explain the
   unresolved question or report no supported finding within the inspected scope.

### Decision rules

- If a caller rejects invalid input before a write, account for that protection.
- If the caller is unavailable, do not claim that validation is absent everywhere.
- Distinguish reading a test from executing it.

### Output

For each supported finding: location, triggering condition, observed behavior,
violated requirement, and supporting evidence. End with checks performed and
remaining limitations. Do not manufacture a finding to fill the format.

Keep private evaluator answer keys and recorded eval results under `evals/`,
outside the agent-facing skill package.
