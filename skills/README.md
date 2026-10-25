# DotSkills skill families

DotSkills keeps every installable skill as a first-level package under `skills/<name>/`.
The conceptual hierarchy is expressed through `catalog.json` categories rather than
nested skill directories, so each skill remains independently discoverable and portable.

## Methodology skills

Use these to develop, diagnose, and improve other skills.

| Skill | Role |
| --- | --- |
| `eval-driven-skill-development` | Entry point. Defines the human-gated improvement loop, teaches relevant methodology concepts, and routes confirmed failures to the relevant specialist methodology. |
| `context-engineering` | Context selection, progressive retrieval, provenance, freshness, conflict handling, and stopping conditions. |
| `correctness-and-verification` | Requirements, invariants, evidence, deterministic checks, and uncertainty. |
| `skill-lifecycle-and-release` | Versioning, paired evals, regression coverage, portability checks, and release decisions. |
| `agent-observability-and-feedback` | Agent-journey traces, outcome/process signals, diagnostics, and production-feedback loops. |
| `agent-trust-and-governance` | Authority, provenance, permissions, approvals, guardrails, and risk controls. |

Start with `eval-driven-skill-development`. Invoke a specialist methodology only
when the observed evidence points to that failure class. A failed eval does not
automatically mean the target skill should be edited.

### Default interaction

`eval-driven-skill-development` is human-gated by default. It should make a
recommendation, explain why, show materially different alternatives when useful, and
give the human an open path to contribute their own solution, constraints, concerns, or
opinion.

Human feedback is not implicit approval. If the human revises a proposal or contributes
an alternative, the methodology should respond to that input and present the gate again
before taking the gated action.

Guided learning is also the default. At meaningful gates, the methodology briefly
explains the concept currently in use, how it applies to the concrete case, what evidence
to notice, and why the recommendation follows. Learning content stays outside the
evaluated target skill's task context.

Typical harness invocation:

```text
Use eval-driven-skill-development to improve <target-skill>.

Work in the default human-gated, guided-learning mode.
Walk me through the methodology one gate at a time.
Do not invoke a specialist, edit the target skill, run a gated comparison,
or accept regression coverage without my explicit approval.
At each gate, make a recommendation, show useful alternatives,
and let me contribute my own solution or feedback.
```

The same entry point can be used for either refining an existing skill or developing a
new one. For a new skill, define the intended capability and eval behavior before drafting
the implementation.

## Task skills

Task skills perform the user's actual work, for example code review, investigation,
requirements refinement, learning, and decision support. They are targets that the
methodology skills can evaluate and improve; they are not children of the methodology
packages in the filesystem.
