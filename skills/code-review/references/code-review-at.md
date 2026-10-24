# Algorithmic Thinking Code-Review Prompt Library

Quick-reference for reviewing a change with an AI coding agent, using principles from *Algorithmic Thinking* by Daniel Zingaro to judge whether the problem is understood correctly, the algorithm fits the constraints, the implementation is correct, and the complexity is justified.

A normal review asks:

```text
Does this code work?
Are there bugs?
Are there tests?
```

An Algorithmic Thinking review also asks:

```text
What problem is this code actually solving?
What are the constraints?
What information matters?
Which algorithmic pattern fits the problem?
Is the chosen data structure appropriate?
Why is the algorithm correct?
What happens at the boundaries?
How do runtime and memory grow with input size?
```

Algorithmic Thinking should **complement, not replace** reviews for ordinary correctness, software design, security, maintainability, and system architecture.

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
|---|---|---|---|
| ★ | [**Compact daily**](#compact-daily-code-review-prompt) | 10-point algorithmic review in one pass | Default for algorithmic changes |
| 0 | [**Master**](#0-master-algorithmic-thinking-code-review-prompt) | Full problem → algorithm → correctness → complexity review | Bigger or higher-risk logic |
| 1 | [**Understand the problem**](#1-understand-the-problem-first) | Reconstructs inputs, outputs, constraints, and requirements | First — before judging the solution |
| 2 | [**Correctness**](#2-review-algorithmic-correctness) | Finds bugs using concrete counterexamples | Always |
| 3 | [**Algorithm choice**](#3-review-the-algorithm-choice) | Checks whether the strategy fits the problem | Multiple approaches are possible |
| 4 | [**Data structures**](#4-review-data-structure-choice) | Matches structures to required operations | Collections or representation matter |
| 5 | [**Complexity**](#5-review-time-and-space-complexity) | Analyzes runtime and memory growth | Performance-sensitive logic |
| 6 | [**Invariants**](#6-review-the-algorithms-invariants) | Explains why the algorithm remains correct | Loops, traversal, DP, windows, heaps |
| 7 | [**Edge cases**](#7-review-edge-cases-and-boundaries) | Generates adversarial boundary inputs | Before accepting correctness |
| 8 | [**Pattern recognition**](#8-identify-the-problem-solving-pattern) | Extracts reusable DSA clues and patterns | Learning from a solved problem |
| 9 | [**Tests**](#9-review-tests-as-algorithmic-evidence) | Checks whether tests actually support correctness | Reviewing test coverage |
| A | [**AI-generated solution**](#a-reviewing-an-ai-generated-algorithmic-solution) | Skeptical pass for plausible-looking AI mistakes | Code came from an agent |

---

## Compact daily code-review prompt

**What it does:** Runs the most useful Algorithmic Thinking checks in one pass. Use this as the default prompt for normal DSA or algorithm-heavy code.

```text
Review this diff using principles from Algorithmic Thinking.

Focus on:

1. What problem the code is actually solving
2. Inputs, outputs, assumptions, and constraints
3. Behavioral and algorithmic correctness
4. Algorithm choice
5. Data-structure choice
6. Important invariants
7. Boundary and edge cases
8. Time complexity
9. Space complexity
10. Test quality

For every finding, provide:

- Evidence from the code
- Concrete consequence
- Severity
- A specific input or scenario demonstrating the issue
- Smallest reasonable improvement

Separate findings into:

- Correctness issues
- Performance issues
- Maintainability issues
- Optional improvements

Do not recommend a more complicated algorithm unless the input constraints,
performance requirements, or correctness requirements justify it.

Do not claim an optimization is necessary without explaining the workload at
which the current approach becomes a problem.

Calibrate every claim: distinguish CONFIRMED DEFECT, PLAUSIBLE RISK,
VERIFICATION GAP, and OPTIONAL IMPROVEMENT. Provide the evidence and
conditions for each; severity must match demonstrated impact, not a
hypothetical worst case. State what was inspected or actually tested,
and what was not. Zero findings is a valid result.
```

---

## 0. Master Algorithmic Thinking code-review prompt

**What it does:** Performs the full review from problem definition through correctness, representation, complexity, and testing.

```text
Review this change using principles from Algorithmic Thinking.

First understand the problem before criticizing the implementation.

Evaluate:

1. What problem is being solved.
2. What the expected inputs and outputs are.
3. What assumptions are made about the input.
4. What constraints affect the solution.
5. What the simplest correct solution would look like.
6. What algorithmic approach the implementation uses.
7. Why that algorithm should produce the correct result.
8. What data structures are used and why.
9. Whether those data structures fit the operations performed.
10. What invariants must remain true during execution.
11. What boundary cases or unusual inputs could break the implementation.
12. What the time complexity is.
13. What the space complexity is.
14. Where repeated or unnecessary work occurs.
15. Whether tests verify the important input classes and invariants.

Separate findings into:

- Problem-understanding issues
- Correctness issues
- Algorithm and data-structure issues
- Complexity issues
- Testing gaps
- Optional improvements

For every finding:

- Cite the file and symbol
- Explain the concrete consequence
- Give a specific input or execution that demonstrates the issue
- Explain expected versus actual behavior
- Suggest the smallest reasonable improvement
- Mark it as blocking, important, or optional

Clearly separate:

- Behavior proven by the implementation
- Assumptions
- Complexity analysis
- Potential optimizations

Prefer the simplest solution that satisfies the actual constraints.

Do not optimize merely because a theoretically faster algorithm exists.

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

## 1. Understand the problem first

**What it does:** Forces the agent to reconstruct the actual problem before pattern-matching to an algorithm.

```text
Before reviewing the implementation, reconstruct the problem it is trying to
solve.

Identify:

- Inputs
- Outputs
- Input constraints
- Valid and invalid input
- Required behavior
- Important edge cases
- Performance requirements
- Ordering requirements
- Duplicate handling
- Empty-input behavior
- Expected data size
- Important invariants

Summarize the problem in plain English.

Then identify:

- What information from the input actually matters
- What information can be ignored
- Which operations dominate the problem
- Which constraints are likely to influence algorithm choice

Separate what is confirmed by the code, tests, or requirements from what you
inferred.

Do not evaluate algorithm choice until the problem and constraints are clear.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 2. Review algorithmic correctness

**What it does:** Searches for concrete counterexamples instead of simply declaring that the algorithm looks correct.

```text
Review this implementation for algorithmic correctness.

Look for:

- Incorrect assumptions
- Missing cases
- Off-by-one errors
- Incorrect loop boundaries
- Incorrect termination conditions
- Incorrect state updates
- Incorrect comparisons
- Duplicate-handling errors
- Incorrect ordering assumptions
- Empty collections
- Single-element inputs
- Minimum and maximum values
- Cycles where relevant
- Repeated values
- Negative values where relevant
- Overflow or precision problems
- Mutation that affects later computation
- Incorrect recursion base cases
- Incorrect memoization or cache keys

For each issue, give the smallest concrete input that demonstrates the failure.

Use this format:

Input:
Expected result:
Actual or likely result:
Why it fails:
Smallest fix:

Do not report a correctness issue without a concrete failing scenario.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 3. Review the algorithm choice

**What it does:** Identifies the underlying strategy and checks whether it is appropriate for the actual constraints.

```text
Identify the algorithmic strategy used by this implementation.

Possible patterns may include:

- Brute force
- Sorting
- Hashing
- Two pointers
- Sliding window
- Binary search
- Recursion
- Divide and conquer
- Greedy
- Dynamic programming
- BFS
- DFS
- Graph traversal
- Heap / priority queue
- Prefix sums
- Interval processing

Then evaluate:

- Why this approach fits the problem
- Which constraints make it valid
- Whether a simpler approach would work
- Whether the implementation matches the intended pattern correctly
- Whether another approach would meaningfully improve correctness,
  readability, or performance

When comparing alternatives, provide:

Current approach:
Current time complexity:
Current space complexity:

Alternative:
Alternative time complexity:
Alternative space complexity:

Trade-off:
When the difference actually matters:

Do not recommend cleverness for its own sake.

Prefer a simple correct algorithm when it satisfies the real constraints.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 4. Review data-structure choice

**What it does:** Checks whether the representation matches the operations the algorithm needs to perform.

```text
Review the important data structures used by this implementation.

For each one identify:

- What information it represents
- Operations performed on it
- Lookup frequency
- Insert frequency
- Delete frequency
- Ordering requirements
- Duplicate requirements
- Memory cost

Evaluate whether the structure fits those operations.

Consider where relevant:

- Array / list
- Set
- Hash map
- Stack
- Queue
- Deque
- Heap
- Tree
- Graph
- Linked structure

Look for cases where the implementation repeatedly performs an expensive
operation that a different representation could make cheaper or clearer.

For every suggested replacement explain:

- Current operation cost
- Proposed operation cost
- Additional complexity introduced
- Why the trade-off is worthwhile

Do not replace a simple structure unless there is a meaningful correctness,
clarity, or performance benefit.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 5. Review time and space complexity

**What it does:** Goes beyond simply printing Big-O and identifies what actually dominates runtime and memory.

```text
Analyze the important execution paths in this implementation.

For each one provide:

- Time complexity
- Space complexity
- Dominant operation
- Relevant input variable
- Best case if meaningful
- Worst case if meaningful

Look for:

- Nested loops
- Repeated scans
- Repeated sorting
- Repeated allocation
- Hidden library-operation complexity
- Recursive depth
- Expensive work inside loops
- Duplicate computation
- Repeated conversions or copying

Then evaluate:

- What happens at 10× input size?
- What happens at 100× input size?
- What resource becomes the bottleneck first?
- Is the concern theoretical or realistically important?

If you recommend an optimization, explain the input size or workload at which
the current implementation becomes a meaningful problem.

Do not treat a better Big-O value as automatically better engineering.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 6. Review the algorithm's invariants

**What it does:** Makes the reasoning behind correctness explicit.

```text
Identify the important invariants maintained by this algorithm.

Examples include:

- Everything before index i has already been processed
- The queue contains discovered but unvisited nodes
- The current window satisfies a defined constraint
- The heap contains the best k candidates seen so far
- dp[i] represents the answer to a defined subproblem
- The left and right partitions satisfy a particular ordering property

For every important invariant:

1. State it clearly.
2. Show where it is established.
3. Show how each iteration or recursive step preserves it.
4. Show how it contributes to termination.
5. Show how it leads to the final result.

Flag any execution path that can violate the invariant.

If the algorithm is correct but the invariant is difficult to understand from
the implementation, suggest the smallest change that would make the reasoning
more obvious.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 7. Review edge cases and boundaries

**What it does:** Generates targeted adversarial inputs based on the actual algorithm.

```text
Generate edge cases and adversarial inputs for this implementation.

Consider where relevant:

- Empty input
- One element
- Two elements
- All values equal
- Already sorted input
- Reverse-sorted input
- Maximum-size input
- Minimum values
- Maximum values
- Duplicate values
- Missing values
- Negative values
- Zero values
- Cyclic input
- Disconnected structures
- Deep recursion
- Highly skewed input
- Multiple equally valid answers

For every meaningful case provide:

Input:
What behavior it exercises:
Expected result:
Whether the implementation handles it correctly:

Prioritize cases that:

- Exercise a different branch
- Challenge an assumption
- Test an invariant
- Hit a boundary
- Distinguish two competing algorithmic approaches

Do not produce edge cases that are irrelevant to this problem.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 8. Identify the problem-solving pattern

**What it does:** Turns a code review into a reusable learning exercise for future DSA problems.

```text
Analyze this code as a problem-solving exercise.

Identify:

Problem type:
Important clues:
Relevant constraints:
Algorithmic pattern:
Data structure:
Key invariant:
Time complexity:
Space complexity:

Then explain:

1. Which clues should make me consider this pattern in a future problem?
2. What question should I ask myself when I encounter a similar problem?
3. Which data or constraint made this pattern useful?
4. What similar-looking problem would require a different pattern?
5. What common wrong approach might someone try first?
6. How can I recognize that the wrong approach will not scale or will fail?

End with:

Recognition rule:
"When I see ______ and the constraint is ______, consider ______."

Keep the explanation focused on reasoning and recognition rather than
memorizing a list of algorithms.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## 9. Review tests as algorithmic evidence

**What it does:** Checks whether the test suite actually supports the correctness claim.

```text
Review the tests for this algorithm.

Determine whether they cover:

- Normal input
- Empty input
- Smallest valid input
- Boundary conditions
- Duplicate values
- Ordering differences
- Maximum or large input
- Important algorithm branches
- Previously failing cases
- Important invariants
- Performance-sensitive input

Then identify:

- Important equivalence classes that are missing
- Cases where tests pass but the algorithm could still be incorrect
- Cases where one test could cover several redundant tests
- Property-based tests that would be useful
- Complexity or performance behavior worth testing

Recommend the smallest set of additional tests that would meaningfully increase
confidence in correctness.

For each suggested test explain what specific bug or invariant it protects.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```

---

## A. Reviewing an AI-generated algorithmic solution

**What it does:** Applies extra skepticism to AI-generated solutions that may look convincing without actually being correct.

```text
Review this AI-generated algorithmic solution skeptically.

Do not assume that plausible-looking code is correct.

Check specifically for:

- Pattern matching to the wrong algorithm
- Unstated assumptions
- Invented constraints
- Incorrect complexity claims
- Off-by-one errors
- Missing edge cases
- Incorrect mutation
- Incorrect recursion base cases
- Incorrect memoization
- Data structures chosen because they are common rather than necessary
- Premature optimization
- Overcomplicated solutions
- Tests that only reproduce examples from the prompt

Before accepting the solution:

1. Restate the problem and constraints.
2. Identify the algorithmic pattern.
3. State the core invariant.
4. Explain why the algorithm should be correct.
5. Search for the smallest counterexample.
6. Verify time and space complexity.
7. Compare it with the simplest reasonable alternative.

Clearly separate:

- What the code proves
- What the agent assumed
- What still requires verification

If the current simple solution already satisfies the constraints, do not
recommend a more complicated one.

Calibrate conclusions: cite inspected evidence and concrete conditions.
Separate confirmed defects, plausible risks, verification gaps, and
optional improvements. Do not inflate severity or imply unverified
production impact; zero actionable findings is a valid outcome.
```
