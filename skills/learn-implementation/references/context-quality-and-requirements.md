# Context quality and requirements

## Required context

Establish the target repository and implementation, feature, diff, or revision to explain. Obtain readable code for the target and enough adjacent callers or contracts to trace at least one representative flow. If the target is ambiguous or inaccessible, ask for the smallest missing input rather than inventing an implementation.

## Supporting evidence

Use the request or ticket, agent summary, tests, migrations, configuration, schema, and relevant dependencies when available. Treat summaries as claims to check against code. Record the revision when available; identify conflicts between requirements, summaries, and implementation explicitly. Missing tests or scale targets are unknowns, not proof of failure.

## Scope and completion

Keep the exercise read-only. Follow all thirteen master sections, marking irrelevant mechanisms not applicable and unsupported claims unverified. Cite inspected files and symbols; use verified line numbers only. Explain one concrete flow, the relevant guarantees and limits, design and algorithmic trade-offs, relevant abstraction and interface complexity, and the final learning summary. Label a partial explanation as partial and identify evidence needed to complete it.
