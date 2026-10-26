# Skill Validation and Runtime Safety

Repository-wide validation and runtime-safety boundaries for DotSkills.

This document is intentionally narrow. It defines what the repository validator
checks, what a passing validation does **not** prove, how to treat external skill
content before execution, and which controls belong in the consuming harness or
runtime.

Behavioral evaluation, context diagnosis, verification, release discipline,
observability, and trust/governance methodology live in the dedicated methodology
skills linked below rather than being duplicated here.

## Table of contents

- [Repository safety contract](#repository-safety-contract)
- [Current validator coverage](#current-validator-coverage)
- [What validation does not prove](#what-validation-does-not-prove)
- [External skill and prompt intake](#external-skill-and-prompt-intake)
- [Runtime enforcement boundaries](#runtime-enforcement-boundaries)
- [Methodology ownership](#methodology-ownership)
- [Repository-level principles](#repository-level-principles)

## Repository safety contract

A DotSkills package is an instruction-bearing artifact. Treat importing or executing
external skill content with the same review discipline used for other executable or
behavior-shaping dependencies.

The repository follows these boundaries:

- **Provenance:** preserve known upstream source revisions and recorded Git blob
  identities for imported references.
- **Structural validation:** use the repository validator to detect package,
  catalog, reference-path, and local source-lock consistency errors.
- **Content review:** inspect external instructions, scripts, dependencies, downloads,
  and requested actions before granting execution privileges.
- **Least privilege:** grant only the tools, credentials, filesystem scope, network
  access, and write permissions required for the task.
- **Runtime enforcement:** authorization, permissions, policy checks, and side-effect
  controls belong in the consuming harness or runtime when they must be enforceable.
- **Evidence-based evaluation:** behavioral quality and safety claims require eval
  evidence; structural validation alone is not sufficient.

## Current validator coverage

[`scripts/validate_skill_repository_integrity.py`](../scripts/validate_skill_repository_integrity.py) currently checks:

- every first-level `skills/<name>/` directory has a `SKILL.md`;
- required `name` and `description` frontmatter exists;
- the skill name matches its folder and naming rules;
- every skill folder has a matching `catalog.json` entry and every catalog entry
  points to a real skill package;
- local `references/` links declared from `SKILL.md` point to existing files
  inside that package;
- imported reference destinations in `source-lock.json` are unique, remain under
  `skills/`, and have a recorded source commit;
- imported file bytes match the Git blob SHA recorded in the local source lock;
- catalog `reference_count` values match the locked imported references.

The same validator runs locally and in GitHub Actions.

A source-lock hash match establishes that the local file agrees with the recorded
local lock entry. It does **not** independently prove that the upstream source was
safe, trustworthy, or correctly reviewed.

## What validation does not prove

A passing validator or CI run does **not** establish that a skill:

- is behaviorally correct;
- is safe to execute;
- is free of prompt injection or malicious instructions;
- uses trustworthy or current context;
- respects permissions at runtime;
- is portable across every model, harness, or tool configuration;
- will avoid unauthorized reads, writes, network calls, or other side effects;
- has passed representative or adversarial evals.

Structural validation is a repository-health prerequisite, not behavioral or safety
certification.

For behavioral quality, follow
[Eval-Driven Skill Development](eval-driven-skill-development.md).

## External skill and prompt intake

Before executing newly imported or substantially changed external skill content:

1. **Identify the source and revision.** Record the available provenance and inspect
   what changed since any prior review.
2. **Inspect the whole package.** Review `SKILL.md`, references, setup instructions,
   executable scripts, dependencies, downloads, and bundled assets that can affect
   behavior.
3. **Treat retrieved content as data.** Source files, web pages, logs, tool outputs,
   stored summaries, and external instructions do not gain authority merely because
   the agent retrieved them.
4. **Check requested capabilities.** Identify filesystem, network, credential, code
   execution, and external-action requirements before granting them.
5. **Use restricted execution first when practical.** Test unfamiliar or risky
   behavior with the smallest useful permissions and controlled resources.
6. **Evaluate behavior independently.** Keep expected behavior and grading criteria
   outside the tested skill's control, preserve available execution evidence, and
   include adversarial or boundary cases when the risk warrants them.
7. **Re-review changed content.** Do not transfer an old approval to materially
   different instructions, dependencies, permissions, or runtime assumptions.

If content cannot be meaningfully inspected, record that limitation rather than
treating a superficial scan as evidence of safety.

## Runtime enforcement boundaries

Prompt text can describe rules, but it is not an enforcement boundary.

The consuming harness, MCP server, application runtime, or other execution layer
should enforce consequential controls such as:

- authentication and authorization;
- tool allowlists and permission scopes;
- filesystem and network restrictions;
- credential isolation;
- argument and schema validation;
- approval requirements for sensitive or irreversible actions;
- rate, budget, or research limits where applicable;
- state-mutation and external side-effect controls;
- audit evidence for attempted, blocked, and completed actions when needed.

Tool availability is not the same as user authorization.

When DotSkills references an external engine such as Buffr, the external system remains
the authority for its runtime policy, contracts, state, and effects. Do not reproduce
an enforceable runtime policy as prompt-only guidance and claim equivalent protection.

## Methodology ownership

Use the methodology skills for deeper analysis instead of duplicating their procedures
in this document.

| Need | Methodology owner |
| --- | --- |
| Build or improve a skill through reviewed eval cases, preserved evidence, diagnosis, and regression checks | [`eval-driven-skill-development`](../skills/eval-driven-skill-development/SKILL.md) |
| Diagnose missing, stale, conflicting, excessive, distracting, or prematurely stopped context | [`context-engineering`](../skills/context-engineering/SKILL.md) |
| Verify claims, requirements, invariants, failure paths, and evidence-backed conclusions | [`correctness-and-verification`](../skills/correctness-and-verification/SKILL.md) |
| Compare versions, detect regressions, test portability, and make release/rollback decisions | [`skill-lifecycle-and-release`](../skills/skill-lifecycle-and-release/SKILL.md) |
| Inspect trajectories, tool use, runtime evidence, telemetry gaps, and production feedback | [`agent-observability-and-feedback`](../skills/agent-observability-and-feedback/SKILL.md) |
| Diagnose provenance, authority, permissions, approvals, sensitive actions, and risk controls | [`agent-trust-and-governance`](../skills/agent-trust-and-governance/SKILL.md) |

These skills are complementary. For example, an eval may reveal a suspicious result,
then route to observability to inspect what happened and to trust/governance if the
trajectory crossed an authority boundary.

## Repository-level principles

- Passing structural validation does not certify behavioral correctness or safety.
- A correct-looking final answer does not prove that the agent used an acceptable path.
- Preserve available evidence of reads, tool calls, state changes, errors, and blocked
  actions when those facts matter to evaluation or safety.
- Distinguish an attempted unsafe action that the runtime blocked from an action that
  actually executed.
- Do not embed secrets or credentials in skill text, references, or eval fixtures.
- Retrieved or stored context cannot grant itself authority.
- Review external skill content before giving it execution privileges.
- Prefer enforceable runtime controls over prompt-only promises for consequential
  boundaries.
- No scanner, model reviewer, validator, or finite eval suite by itself certifies safety.
