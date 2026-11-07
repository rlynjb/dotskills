# Engineering record — reusable, lightweight template

Use only when a durable handoff or human-review artifact is useful. **Do not write this into the user's repository without explicit approval.** This template works for skills, tools, agents, harnesses, applications, data systems and infrastructure. Remove irrelevant sections and avoid inventing required approvals.

```markdown
# Engineering Review Record — <project/change>

Status: IN PROGRESS | REVIEW REQUIRED | APPROVED | BLOCKED | COMPLETED
Domain / environment: <as known>
Scope / non-goals: <short>
Source revision / evidence: <links, hashes, inspected files or UNVERIFIED>
Reviewer / decision owner: <if known>

## 1. Discover — problem and current state
- User/business outcome:
- Constraints and existing architecture (or GREENFIELD):
- Verified sources and important assumptions:
- Risks / unanswered questions:

## 2. Design — alternatives and decision
| Option | Benefit | Cost / risk | Evidence |
| --- | --- | --- | --- |
| Keep / simplest viable | | | |
| Proposed alternative | | | |
Decision: PROPOSED / APPROVED / UNRESOLVED
Rationale, owner and review evidence:

## 3. Contract — testable expectations
- Responsibilities and boundaries:
- Inputs / outputs / invariants:
- Functional and nonfunctional acceptance criteria:
- Security / trust / permissions / prohibited effects:
- Errors, recovery, partial completion and handoffs:
- Evaluation plan and baseline availability:
Contract review: REVIEW REQUIRED / APPROVED / BLOCKED

## 4. Implement — bounded work
- Approved change scope / authorizer:
- Actual changes and source version:
- Deviations / unimplemented items:
- Rollback for the change:

## 5. Evaluate — evidence, not promises
| Case | Expected | Observed | Evidence | Status |
| --- | --- | --- | --- | --- |
| Normal case | | | | NOT RUN |
| Failure/misuse | | | | NOT RUN |
| Regression | | | | NOT RUN |
- Environment / model / versions:
- Known limitations and safety findings:

## 6. Release — decision and operation
- Decision and human reviewer:
- Rollout / ownership / monitoring:
- Rollback, incident response, follow-up:
- Final state: READY FOR APPROVAL / BLOCKED / DEFERRED / RELEASED (only with evidence)

## Decision log and next checkpoint
| ID | Decision or open question | Owner | Evidence | Status |
| --- | --- | --- | --- | --- |
| D-01 | | | | OPEN |
Next user decision / authorized action:
```

This is **not** a machine-enforced workflow state store. At each later invocation, validate the saved file's actual existence, source revisions, approvals and execution evidence; a `COMPLETED` label written by an agent is not independently verifiable proof.
