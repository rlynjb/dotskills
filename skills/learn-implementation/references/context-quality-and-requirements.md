# Context quality and requirements

## Required context

Establish the **specific** repository and implementation, existing feature, change, or agent-produced diff to explain. Obtain readable code for the target and enough callers/contracts to trace at least one representative path. If the target is ambiguous or inaccessible, ask for the smallest missing input rather than inventing files, architecture, or decisions. Keep inspection bounded to this implementation, not an automatic whole-repository tour.

## Supporting evidence and provenance

Use the request/ticket, agent summary, implementation diff, tests, migrations, configuration, schemas, ADRs/design documents, and dependencies when available. Treat an agent summary or ticket's rationale as a claim until aligned with evidence. Record the inspected branch/revision, paths and symbols; identify conflicts among requirements, summary, code, tests, and notes. Distinguish `OBSERVED` implementation choices, `DOCUMENTED` rationale, `INFERRED` rationale, `UNKNOWN` decisions or requirements, and `HYPOTHETICAL` alternatives. A code pattern is not proof of the original author's intent. Missing tests, scale targets, or metrics are unknowns, not evidence of failure.

## First response and completion

Before teaching, give the master's complete **Implementation Learning Menu**: snapshot, evidence/mechanism map, stable `D-xx` design-decision index, all applicable `Q-xx` questions grouped by `T-xx` topics across three stages, evidence gaps, and a choice. Do not start the first lesson without a selected item, unless a complete tutorial was explicitly requested. Preserve IDs and coverage across turns, rechecking affected evidence on change.

For a selected question or decision, follow **Alex Xu's four steps** in order: understand problem/scope → reconstruct existing high-level design → code-backed deep dive with decision trade-offs → wrap up and learning checkpoint. Guided covers one item with worked reasoning per response; Practice waits for the learner at each step. Use all thirteen master sections as a **coverage guide**, marking irrelevant mechanisms not applicable and unsupported claims not verified. Apply only relevant FODE, DDIA, SDI, Algorithmic Thinking, and APOSD lenses.

At completion or on request, explain one concrete flow, relevant guarantees and limits, key **observable** design decisions and alternative trade-offs, applicable abstractions/algorithms, the glossary and learning summary. Label partial coverage and needed evidence; distinguish tests inspected, executed under separate authorization, and proposed. Keep the work read-only and omit draft code-review comments.
