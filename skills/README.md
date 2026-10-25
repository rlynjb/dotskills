# DotSkills skill families

DotSkills keeps every installable skill as a first-level package under `skills/<name>/`.
The conceptual hierarchy is expressed through `catalog.json` categories rather than
nested skill directories, so each skill remains independently discoverable and portable.

## Methodology skills

Use these to develop, diagnose, and improve other skills.

| Skill | Role |
| --- | --- |
| `eval-driven-skill-development` | Entry point. Defines the improvement loop and routes failures to the relevant specialist methodology. |
| `context-engineering` | Context selection, progressive retrieval, provenance, freshness, conflict handling, and stopping conditions. |
| `correctness-and-verification` | Requirements, invariants, evidence, deterministic checks, and uncertainty. |
| `skill-lifecycle-and-release` | Versioning, paired evals, regression coverage, portability checks, and release decisions. |
| `agent-observability-and-feedback` | Agent-journey traces, outcome/process signals, diagnostics, and production-feedback loops. |
| `agent-trust-and-governance` | Authority, provenance, permissions, approvals, guardrails, and risk controls. |

Start with `eval-driven-skill-development`. Invoke a specialist methodology only
when the observed evidence points to that failure class. A failed eval does not
automatically mean the target skill should be edited.

## Task skills

Task skills perform the user's actual work, for example code review, investigation,
requirements refinement, learning, and decision support. They are targets that the
methodology skills can evaluate and improve; they are not children of the methodology
packages in the filesystem.
