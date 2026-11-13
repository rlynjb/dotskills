# Context quality and requirements

## Required context

Establish the **specific** repository and implementation, existing feature, change, or agent-produced diff to explain. Obtain readable code for the target and enough callers/contracts to trace at least one representative path. If the target is ambiguous or inaccessible, ask for the smallest missing input rather than inventing files, architecture, or decisions. Keep inspection bounded to this implementation, not an automatic whole-repository tour.

## Supporting evidence and provenance

Use the request/ticket, agent summary, implementation diff, tests, migrations, configuration, schemas, ADRs/design documents, and dependencies when available. Treat an agent summary or ticket's rationale as a claim until aligned with evidence. Record the inspected branch/revision, paths and symbols; identify conflicts among requirements, summary, code, tests, and notes. Distinguish `OBSERVED` implementation choices, `DOCUMENTED` rationale, `INFERRED` rationale, `UNKNOWN` decisions or requirements, and `HYPOTHETICAL` alternatives. A code pattern is not proof of the original author's intent. Missing tests, scale targets, or metrics are unknowns, not evidence of failure.

## First response and completion

**Default first response: complete, skimmable four-step Implementation Learning Overview**, not a menu-only screen. After bounded code inspection, give a snapshot and visible **Step 1 — Implemented problem/scope**, **Step 2 — Existing architecture and boxed ASCII flow**, **Step 3 — Code mechanism and relevant book chapters**, and **Step 4 — Trade-offs, conditional recommendations and learning takeaways**. Keep it retrospective: explain what code does today, not a design-first proposal. A verified before/after flow is optional when a real diff is available. Attach actual code pointers, rationale evidence status and verification limits. Finish with 3–6 high-value stable `Q-xx`/`D-xx` selections and an option for the full `T-01`–`T-11` learning index; do not require a selection merely to see the four steps.

**Presentation is strict across terminal widths:** one concise vertical labeled block per item, **no tables**; `---` horizontal rules **only between Step 2 area/decision entries**. Steps 1, 3 and 4, chapter suggestions and the checkpoint use headings and blank-line spacing, not per-item dividers. Keep Step 2's actual **boxed ASCII component diagram**, based only on verified code, when it clarifies a real multi-component flow.

Recommend **1–3 relevant, verified book chapters** from the six referenced books. Give title, edition, chapter number/title, code connection and why the concept is worth studying. Use the master's edition-aware chapter guide; **do not invent numbered chapters or apply an irrelevant book**. For trade-offs and performance opportunities explain the observed approach, conditional alternative, likely cost/benefit and evidence or measurement needed; never claim a speedup without a measured baseline.

After the user selects a question, code path or decision, follow **Alex Xu's four steps** in order: understand implemented behavior/scope → reconstruct existing high-level design → code-backed deep dive with relevant chapters/trade-offs → wrap up and learning checkpoint. Guided covers one item with worked reasoning per response; Practice waits for the learner at each step. Use the thirteen master sections as a **coverage guide**, marking irrelevant mechanisms not applicable and unsupported claims not verified. Preserve stable IDs and coverage across turns, rechecking affected evidence on code changes.

At completion or on request, explain one concrete flow, relevant guarantees and limits, key **observable** design decisions and alternative trade-offs, applicable abstractions/algorithms, the glossary and learning summary. Label partial coverage and needed evidence; distinguish tests inspected, executed under separate authorization, and proposed. Keep the work read-only and omit draft code-review comments.
