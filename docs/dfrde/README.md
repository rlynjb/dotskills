# DFRDE engineering reviews

**Design-First, Review-Driven Engineering (DFRDE)** is a reusable process for discovering, designing, contracting, implementing, evaluating and releasing technical changes with human review. It is domain-agnostic: use the same sequence for skills, tools, agents, harnesses, applications and infrastructure while adapting the checks to the domain.

## Choose the right file

| Document | When to use it |
| --- | --- |
| **[Engineering review template](engineering-review-template.md)** | **Start here for any new project**. Copy into the approved workspace, rename it, and fill it progressively. Stage 1 can be prefilled from source evidence and team confirmations. |
| [Sprint Assessment + Refine Requirements integration review](sprint-assessment-refine-requirements-integration-review.md) | Existing **project-specific example and working record**. Preserve its actual findings, choices and questions; don't copy its Agent Arcade assumptions into unrelated work. |
| [Apply DFRDE skill](../../skills/apply-dfrde/SKILL.md) | Guided six-stage method and human approval gates. |
| [Audit Skill](../../skills/audit-skill/SKILL.md) | For existing agent skills: source-backed audit plus **DFRDE Stage 1 Discover prefill** (no execution or edits). |
| [Lightweight record](../../skills/apply-dfrde/references/engineering-record.md) | Short alternative when the full six-stage discussion template would add unnecessary overhead. |

## Recommended routine

1. Copy the [engineering review template](engineering-review-template.md) into the project-approved repository or internal documentation system. Keep this reusable source file unchanged.
2. For an existing **agent skill**, request an **Audit Skill Stage 1 handoff** for one or multiple skills. For other domains, use the appropriate read-only architecture inspection instead.
3. Ask AI to prefill questions that can be answered from source evidence and mark **ANSWERED BY EVIDENCE**, **NEEDS CONFIRMATION**, **OPEN DECISION**, or **NOT VERIFIED**.
4. Review the problem statement and only unanswered questions with collaborators. Recording/transcription requires appropriate participant consent and approved handling of organizational data.
5. Let AI propose edits to the working record from meeting notes; **a responsible human confirms decisions and approves file writes**.
6. Continue DFRDE stages 2–6, preserving decision rationale, approvals, observable eval evidence and rollback plans.

The public DotSkills repository should hold **only generic templates and approved/redacted examples**. Do not copy workplace-only code, Jira content, credentials, recordings or sensitive analysis into public documents.
