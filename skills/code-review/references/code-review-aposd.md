# APOSD Code-Review Prompt Library

Quick-reference for reviewing a change with an AI coding agent, using *A Philosophy of Software Design* to judge whether the change makes the system easier or harder to understand and modify.

A normal review asks:

```text
Does this code work?
Are there bugs?
Are there tests?
```

An APOSD review also asks:

```text
Where did the complexity go?
Is the complexity hidden inside a module, or pushed onto callers?
Did this change duplicate design knowledge?
Will the next change require editing many places?
```

APOSD should **complement, not replace** reviews for correctness, security, performance, accessibility, and testing.

---

## Evidence and severity calibration (applies to every review prompt)

**Use this rule for master, compact, and focused prompts.** Each copyable
prompt below also includes a concise reminder, so standalone prompts still
calibrate claims. The goal is accuracy, not a long list of possible problems.

- **Ground findings in inspected evidence:** cite actual code, relevant call
  paths, tests, contracts, config, or results. Check existing guards,
  validations, and surrounding behavior before claiming something is missing.
- **Label the claim, not just its severity:**
  - **Confirmed defect:** a contradiction of a supported requirement or a
    reproducible error/failure, with the relevant conditions established.
  - **Plausible risk:** a code-supported failure scenario whose likelihood,
    reachability, or real-world impact still needs verification; state the
    preconditions and uncertainty.
  - **Verification gap:** needed evidence is inaccessible or checks were not
    performed; this is not automatically a bug.
  - **Optional improvement:** a design/performance alternative with a
    justified trade-off, not a defect by default.
- **Calibrate severity separately:** use **blocking** only for an evidenced
  release-stopping correctness, security, data-loss, or agreed-contract issue;
  **important** for consequential supported concerns; **optional** for
  nonurgent improvements. Unknown impact is not automatically high severity.
- **Do not overclaim:** a hypothetical failure is not an observed incident;
  a theoretical complexity concern is not measured slowness; absent tests
  are not proof the code is wrong; code inspection is not proof of production
  behavior, load, cost, or deployment configuration.
- **Report the review boundary:** say whether this is a diff, feature path,
  representative sample, or broader repository inspection. List meaningful
  gaps in files, environments, tests, or tools. Never claim the entire repo
  is safe or free of issues when only part was inspected.
- **State verification honestly:** distinguish tests/benchmarks actually run
  and their outcomes from tests merely read or recommended. Don't invent
  outputs, metrics, exploitability, root causes, or stakeholder intent.
- **Prefer precision over volume:** deduplicate shared root causes and permit
  **zero actionable findings**. If none are supported, say "No actionable
  issues found in the inspected scope," with limitations, not "bug-free."

## Index

| # | Prompt | What it does | Reach for it when |
|---|--------|--------------|-------------------|
| ★ | [**Compact daily**](#compact-daily-code-review-prompt) | 11-point pass in one shot, blocking vs optional | Default. Most diffs. |
| 0 | [**Master**](#0-master-aposd-code-review-prompt) | Full 15-point review → 5 finding buckets | Bigger or higher-stakes change |
| 1 | [**Understand the change**](#1-understand-the-change-first) | Explains intent before critiquing | First — don't review what you don't understand |
| 2 | [**Correctness**](#2-review-correctness) | Bugs, branches, races, boundaries + repro | Always, before design (comes first) |
| 3 | [**Module depth**](#3-review-module-depth) | Deep vs shallow classification per module | New/changed modules |
| 4 | [**Shallow abstractions**](#4-detect-shallow-abstractions) | Flags forwarders, renamers, one-use wrappers | Diff added lots of hooks/services/files |
| 5 | [**Information hiding**](#5-review-information-hiding) | What each module owns vs leaks | Boundaries look thin |
| 6 | [**Duplicated design knowledge**](#6-find-duplicated-design-knowledge) | Same *decision* encoded in many places | High-value check — always worth it |
| 7 | [**Responsibility ownership**](#7-review-responsibility-ownership) | Who is authoritative for each decision | Logic feels scattered |
| 8 | [**State ownership**](#8-review-state-ownership) | Source of truth, readers, writers, staleness | React/stores/caches/optimistic updates |
| 9 | [**Temporal coupling**](#9-review-temporal-coupling) | Required call ordering the interface doesn't enforce | init/configure/load-style APIs |
| 10 | [**Interface complexity**](#10-review-interface-complexity) | Params, flags, ordering, error surface | Public interface changed |
| 11 | [**General vs special-purpose**](#11-review-general-purpose-versus-special-purpose-design) | Catches both over-specific and over-generic | Suspect hard-coding or framework-building |
| 12 | [**Error abstraction**](#12-review-error-abstraction) | Whether errors match each boundary's level | Low-level failures reach UI/callers |
| 13 | [**Code obviousness**](#13-review-code-obviousness) | Names, side effects, hidden behavior, comments | Change is hard to read quickly |
| 14 | [**Change amplification**](#14-review-change-amplification) | Probes future changes for change locality | Testing the design, not just cleanliness |
| 15 | [**Tests as design evidence**](#15-review-tests-as-design-evidence) | Behavior/invariants vs implementation-coupled | Reviewing the test changes |
| A | [**AI-generated change**](#a-reviewing-an-ai-generated-change) | Skeptical pass for common AI design smells | The diff came from an agent |
| B | [**Single function**](#b-review-a-single-function) | One function's responsibility + knowledge | Zooming in on one function |
| C | [**New abstraction**](#c-review-a-new-abstraction) | Whether the abstraction earns its existence | A new layer/interface was introduced |
| D | [**Refactor**](#d-review-a-refactor) | Behavior-preserved + complexity reduced not moved | PR labeled "refactor / no behavior change" |
| E | [**Review comments**](#e-producing-useful-review-comments) | Forces concrete, actionable, severity-tagged output | Turning findings into PR comments |

Reference (not prompts): [Review workflow](#recommended-review-workflow) · [Manual-review questions](#questions-to-remember-during-manual-review) · [The four reviews](#the-overall-model)

---

## Compact daily code-review prompt

**What it does:** Runs the whole APOSD review as a single 11-point pass and splits blocking from optional. Your everyday driver for a normal diff.

```text
Review this diff using APOSD principles.

Focus on:

1. Correctness and violated invariants
2. Module depth
3. Information hiding
4. Duplicated design knowledge
5. Responsibility and state ownership
6. Interface complexity
7. Temporal coupling
8. Change amplification
9. Error abstraction
10. Code obviousness
11. Test quality

For every finding, provide:

- Evidence
- Concrete consequence
- Severity
- Smallest recommended improvement

Separate blocking issues from optional design improvements.
Do not recommend additional abstractions unless they hide meaningful complexity.

Calibrate every claim: distinguish CONFIRMED DEFECT, PLAUSIBLE RISK,
VERIFICATION GAP, and OPTIONAL IMPROVEMENT. Provide the evidence and
conditions for each; severity must match demonstrated impact, not a
hypothetical worst case. State what was inspected or actually tested,
and what was not. Zero findings is a valid result.
```

---

## 0. Master APOSD code-review prompt

**What it does:** The full 15-point review producing five finding buckets, each finding tagged blocking/important/optional with a realistic scenario. Use for bigger or higher-stakes changes.

```text
Review this change using principles from A Philosophy of Software Design.

Do not focus only on style or formatting.

Evaluate:

1. What behavior the change introduces or modifies.
2. Whether the implementation matches the intended behavior.
3. Which modules and interfaces are affected.
4. Where the new complexity is located.
5. Whether modules hide meaningful complexity from callers.
6. Whether any interface became more complicated.
7. Whether implementation details leak across module boundaries.
8. Whether design knowledge is duplicated.
9. Whether responsibilities and state ownership are clear.
10. Whether the change introduces temporal coupling or required call ordering.
11. Whether the change increases change amplification.
12. Whether names and control flow make the code obvious.
13. Whether errors are handled at the correct abstraction level.
14. Whether the tests verify behavior and important invariants.
15. Whether a smaller or more localized design would be clearer.

Separate findings into:

- Correctness issues
- Design and complexity issues
- Maintainability risks
- Testing gaps
- Optional improvements

For every finding:

- Cite the file and symbol
- Explain the concrete consequence
- Give a realistic scenario where it matters
- Suggest the smallest reasonable improvement
- Mark it as blocking, important, or optional

Do not recommend abstraction merely to reduce line count.
Do not reward additional layers unless they hide meaningful complexity.

Evidence calibration: check the relevant surrounding code, tests,
contracts, and configuration before declaring a defect. Distinguish
confirmed defects, plausible code-backed risks, verification gaps,
and optional improvements; attach preconditions to uncertain claims.
Severity must follow supported impact; do not label speculative future
scale, unmeasured latency, or unknown deployment behavior as a blocker.
Report the reviewed scope and which tests or checks were actually run.
If no actionable issues are supported, report zero findings with limits
rather than implying the entire repository is defect-free.
```

---

## 1. Understand the change first

**What it does:** Forces the agent to explain intent, entry points, and invariants before critiquing — separating diff-confirmed facts from inference. Prevents criticism of code it hasn't understood.

```text
Explain this change before reviewing it.

Identify:

- The user or system behavior being changed
- The entry points affected
- The major execution path
- State read or written
- External systems involved
- Existing behavior being replaced
- Important invariants
- Assumptions made by the implementation

Separate what is directly confirmed by the diff from what you inferred.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 2. Review correctness

**What it does:** Standard correctness pass — bad assumptions, missing branches, races, boundaries — each issue backed by a concrete input or event sequence. Since APOSD is a design philosophy, this pass should still come first.

```text
Review this change for behavioral correctness.

Look for:

- Incorrect assumptions
- Missing branches
- Null or undefined values
- Invalid state transitions
- Boundary conditions
- Race conditions
- Partial failures
- Retry behavior
- Duplicate operations
- Stale data
- Backward compatibility problems
- Differences between runtime values and static types

For each issue, provide a concrete input or event sequence that demonstrates
the failure.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 3. Review module depth

**What it does:** Classifies every new/changed module deep → shallow → pass-through, contrasting hidden vs exposed complexity. The key question: *is the interface considerably simpler than the implementation behind it?*

```text
Evaluate the depth of every module introduced or substantially changed.

For each module, identify:

- Functionality provided
- Public interface
- Configuration required
- Knowledge required by callers
- Complexity hidden internally
- Complexity exposed externally

Classify it as:

- Deep
- Moderately deep
- Shallow
- Pass-through
- Unclear

Explain whether the module makes the system easier to use or merely moves code
into another file.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 4. Detect shallow abstractions

**What it does:** Finds abstractions the change introduced that add navigation cost without hiding complexity — forwarders, renamers, single-use wrappers. Especially useful on AI-generated code.

```text
Look for shallow abstractions introduced by this change.

Find modules or functions that:

- Only forward arguments
- Rename another API
- Contain almost no policy or behavior
- Expose nearly every implementation option
- Require callers to understand the wrapped implementation
- Are used only once without creating a meaningful boundary
- Split a simple operation across many files

For each candidate, determine whether it is:

- A useful adapter
- A stable architectural boundary
- A test seam
- A shallow abstraction
- An unnecessary pass-through

Do not assume that more modules mean better modularity.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 5. Review information hiding

**What it does:** Per changed module, contrasts what callers need to know vs what's exposed through params, returns, config, errors, or ordering — and judges whether the change improves or weakens hiding.

```text
For each changed module, identify:

- What design decisions it owns
- What implementation details it hides
- What callers currently need to know
- What callers should not need to know
- Which internal details are exposed through parameters, return values,
  configuration, errors, or required operation ordering

Determine whether the change improves or weakens information hiding.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

*Examples of details that may be leaking:*

```text
Database column names
HTTP response shapes
Cache-key formats
Retry rules
Storage representation
Vendor-specific error codes
Graph traversal implementation
Serialization format
Internal status values
```

---

## 6. Find duplicated design knowledge

**What it does:** One of the most valuable APOSD review checks — hunts for the same *decision* encoded in multiple places (not just repeated syntax), showing how the copies could diverge and who should own the rule.

```text
Search the change and surrounding code for duplicated design knowledge.

Look for rules such as:

- Validation requirements
- Status transitions
- Field mappings
- Permission decisions
- Default values
- Error-code interpretations
- Cache-key construction
- Serialization formats
- Database constraints
- Business calculations

For each duplicated rule:

1. Show all locations that know the rule.
2. Explain how those locations could diverge.
3. Identify which module should own the rule.
4. Determine whether this change increases or reduces duplication.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 7. Review responsibility ownership

**What it does:** Assigns an owner to each responsibility the change introduces and flags scattering, mixed ownership, and callers doing callee work. The test: *who is authoritative for this decision?*

```text
For each responsibility introduced by this change, identify its owner.

Responsibilities may include:

- Validation
- Authorization
- Transformation
- Persistence
- Caching
- Retry behavior
- State transitions
- Error translation
- UI formatting
- Domain calculations

Check whether:

- One responsibility is scattered across several modules
- One module owns unrelated responsibilities
- Callers perform work that should belong inside the callee
- Ownership is ambiguous
- Multiple modules can independently make the same decision

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 8. Review state ownership

**What it does:** Maps each added/modified state value — source of truth, readers, writers, staleness — and flags multiple sources of truth or manual synchronization. Especially useful for React, stores, caches, and optimistic updates.

```text
Map every state value added or modified by this change.

For each value, identify:

- Source of truth
- Owner
- Readers
- Writers
- Lifetime
- Persistence mechanism
- Derived values
- Synchronization behavior
- Invariants
- Staleness risks

Look for:

- Multiple sources of truth
- Duplicated derived state
- Ambiguous ownership
- State copied unnecessarily
- State that can become temporarily inconsistent
- Callers that must manually keep values synchronized

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 9. Review temporal coupling

**What it does:** Finds operations that must run in a particular order, and asks whether the interface enforces it or leaves every caller to remember it — and whether the module could absorb the ordering.

```text
Find operations that must occur in a particular order.

Examples:

- Initialize before reading
- Validate before transforming
- Save before publishing
- Refresh after mutation
- Register before dispatching
- Load configuration before constructing a service

For each sequence, determine:

- Whether the required order is obvious
- Whether the interface enforces it
- How many callers must remember it
- What happens when the order is violated
- Whether the module could absorb or eliminate the ordering requirement

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

*Fragile (ordering pushed onto callers):*

```ts
const client = createClient();
client.configure(config);
client.initialize();
client.load();
```

*Deeper (ordering hidden):*

```ts
const client = await createReadyClient(config);
```

---

## 10. Review interface complexity

**What it does:** Scores each changed public interface on params, flags, ordering, and error surface, and flags parameters that expose implementation decisions. Watch boolean flags — `loadGraph(true, false, true)` often signals hidden modes.

```text
Review each public interface changed by this patch.

Evaluate:

- Number of parameters
- Boolean flags
- Configuration options
- Required call ordering
- Return-value complexity
- Error surface
- Special cases
- Naming clarity
- Default behavior
- Knowledge required by callers

Ask whether the interface became simpler or more complex than before.

Identify parameters that expose implementation decisions rather than genuine
caller requirements.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 11. Review general-purpose versus special-purpose design

**What it does:** Checks for both opposite failures — over-specific hard-coding scattered through shared modules, and over-generic framework-building with no real users — and recommends the simplest design for known requirements.

```text
Determine whether this implementation is appropriately general.

Check for two opposite problems:

1. Overly special-purpose code
   - Hard-coded behavior
   - One-off branches
   - Feature-specific logic scattered through shared modules

2. Overly generic code
   - Excessive configuration
   - Abstract factories with one implementation
   - Generic types that obscure the domain
   - Extension points without realistic future users
   - Framework-building instead of solving the current problem

Recommend the simplest design that supports the known requirements without
creating unnecessary special cases.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 12. Review error abstraction

**What it does:** Traces where errors originate, get caught, and get translated, and checks each module exposes errors appropriate to its abstraction level.

```text
Review how errors cross module boundaries.

Identify:

- Where errors originate
- Where they are caught
- Where they are translated
- Where context is added or lost
- Which errors reach callers
- Which errors reach users
- Whether callers must understand infrastructure-specific failures

Check whether each module exposes errors appropriate to its abstraction level.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

*Example:*

```text
Poor boundary:
UI handles PostgreSQL constraint code 23505.

Better boundary:
Repository translates it into DuplicateProjectNameError.
```

---

## 13. Review code obviousness

**What it does:** Looks for anything that slows correct understanding — misleading names, hidden side effects, behavior buried in generic helpers, comments that repeat code instead of explaining design reasoning.

```text
Review this change for code obviousness.

Look for:

- Misleading names
- Important behavior hidden in generic helpers
- Side effects not reflected in names
- Control flow spread across many small functions
- Clever expressions
- Implicit conventions
- Unexpected mutation
- Nonlocal dependencies
- Comments that repeat code
- Missing comments about design reasoning
- Names that require knowledge of implementation details

Identify the smallest changes that would reduce the time needed to understand
the code correctly.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

*Comment quality:*

```text
Bad comment:
Increment index by one.

Useful comment:
Skip the synthetic root node because it is not persisted.
```

---

## 14. Review change amplification

**What it does:** Uses hypothetical future changes as probes to judge change locality — which modules contain a change vs let it spread. Often more informative than asking whether the code "looks clean."

```text
Use hypothetical future changes to evaluate this design.

Consider:

1. A small behavior modification
2. A new data field or state
3. A replacement of an external dependency
4. A new caller
5. A new error case

For each scenario, identify:

- Files likely to change
- Interfaces likely to change
- Rules duplicated across locations
- Modules that successfully contain the change
- Changes that would spread through unrelated layers

Determine whether this patch improves or worsens change locality.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 15. Review tests as design evidence

**What it does:** Judges whether tests verify behavior/invariants/contracts vs coupling to private methods, call order, and mock interactions. Tests that must know every internal call often reveal weak module boundaries.

```text
Review the tests for this change.

Determine whether they verify:

- User-visible behavior
- Important domain invariants
- Public module contracts
- Error behavior
- Boundary conditions
- State transitions
- Regression scenarios
- Concurrency or timing behavior when relevant

Look for tests that are overly coupled to:

- Private methods
- Internal call order
- Specific implementation details
- Mock interactions rather than outcomes
- Exact internal data representations

Explain what the tests reveal about the quality of the module interfaces.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## A. Reviewing an AI-generated change

**What it does:** A skeptical pass targeting design problems agents commonly produce — unnecessary layers, one-impl interfaces, silent fallbacks, type assertions hiding invalid states, partial migrations leaving two competing patterns.

```text
Review this AI-generated implementation skeptically.

Look specifically for common AI-generated design problems:

- Unnecessary files or layers
- Shallow wrapper functions
- Interfaces with only one implementation
- Premature factories or dependency injection
- Duplicate validation
- Excessive configuration
- Generic utility modules containing domain logic
- Broad exception handling
- Silent fallback behavior
- Type assertions hiding invalid states
- Comments that claim behavior not guaranteed by code
- Tests that merely reproduce the implementation
- New abstractions that are not used consistently
- Partial migration leaving two competing patterns

Determine which abstractions hide meaningful complexity and which merely add
navigation cost.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## B. Review a single function

**What it does:** Zooms in on one function's real responsibility, embedded design knowledge, and whether it should stay, merge, or move. Won't recommend extraction just because a function is long — a coherent long function can beat ten tiny ones.

```text
Review this function using APOSD principles.

Determine:

- Its actual responsibility
- Whether it performs more than one conceptual task
- What assumptions it makes
- What design knowledge it contains
- Whether that knowledge appears elsewhere
- Whether its inputs expose implementation details
- Whether its output creates work for callers
- Whether its name accurately communicates behavior
- Whether the function should remain separate, be merged, or belong in another
  module

Do not recommend extraction merely because the function is long.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## C. Review a new abstraction

**What it does:** Interrogates whether a newly introduced abstraction earns its keep — what it hides, how many real callers need it, what's lost if removed — and ends with a keep/simplify/merge/move/remove verdict.

```text
Evaluate whether this new abstraction earns its existence.

Ask:

- What complexity does it hide?
- What decision does it centralize?
- How much simpler is its interface than its implementation?
- How many realistic callers need it?
- Could callers use the underlying implementation just as easily?
- Does it create a stable boundary?
- Does it reduce change amplification?
- Does it eliminate duplicated knowledge?
- Does it introduce terminology developers must learn?
- What would be lost if the abstraction were removed?

Conclude with:

- Keep as-is
- Simplify
- Merge with another module
- Move responsibility
- Remove abstraction

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## D. Review a refactor

**What it does:** Verifies a "structural only" change actually preserves behavior and reduces complexity rather than relocating it — and flags any part that quietly changes behavior.

```text
Review this refactor separately from behavioral changes.

Verify:

- Whether behavior is genuinely preserved
- Whether complexity was reduced rather than relocated
- Whether module interfaces became simpler
- Whether information hiding improved
- Whether duplicated knowledge was removed
- Whether dependencies became more localized
- Whether the new structure requires more navigation
- Whether tests are less coupled to implementation
- Whether temporary compatibility layers remain

Identify any part of the refactor that changes behavior despite being presented
as structural only.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## E. Producing useful review comments

**What it does:** Makes the agent write concrete, actionable, severity-tagged comments instead of vague opinions ("this could be cleaner", "consider refactoring"). Every comment carries a consequence and a scenario.

```text
Write code-review comments that are concrete and actionable.

Each comment must include:

1. Location
2. Observed issue
3. Concrete consequence
4. Scenario where it matters
5. Smallest suggested improvement
6. Severity

Avoid comments such as:

- This could be cleaner.
- Consider refactoring.
- This feels complex.
- Use better separation of concerns.

Only report issues that have a plausible maintenance, correctness, or usability
consequence.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

*Example of a good comment:*

> **Important:** `ProductCard` now interprets the raw API status values `"active"` and `"archived"`. The same mapping exists in `productMapper.ts`. If the backend adds another status, both locations must change together. Consider returning a domain-level `ProductState` from the mapper so UI components do not depend on the transport representation.

---

## Recommended review workflow

Use several passes rather than reviewing everything simultaneously:

```text
Pass 1: Understand the intended behavior
Pass 2: Review correctness and failure cases
Pass 3: Review module boundaries and information hiding
Pass 4: Review state, dependencies, and errors
Pass 5: Review tests and change impact
Pass 6: Summarize only actionable findings
```

---

## Questions to remember during manual review

```text
What complexity does this change introduce?

Where is that complexity contained?

Does the caller need to know this detail?

Who owns this decision?

Is the same rule represented anywhere else?

Can invalid state cross this boundary?

Does the interface make the common case simple?

Must callers remember a particular operation order?

Would a likely future change remain localized?

Is this abstraction deeper than its interface?

Does this code make the system more obvious?

Does the test verify behavior or merely mirror the implementation?
```

---

## The overall model

```text
Correctness review:
Does the change work?

APOSD review:
Does the design contain its complexity?

Change-impact review:
Will the next modification remain localized?

Testing review:
Can we prove the behavior without depending on implementation details?
```

The strongest code review combines all four.
