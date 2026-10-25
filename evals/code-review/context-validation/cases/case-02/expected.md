# Expected behavior — evaluator only

## Correct outcome

Identify the reachable missing-validation defect: invalid input can reach the persistence helper and be written.

## Essential reasoning

For example, { name: '   ' } passes through createUser to saveUser, which appends the invalid name. This violates rejection before writing. Not every invalid input needs to be accepted to establish the defect.

## Answer-key evidence

The [requirements](input/requirements.md) establish the sole entry point, valid
input, rejection before writes, and preservation of names. The supplied
[application](input/materials/mock-app) establishes the actual path.
Run `node evals/code-review/context-validation/verify-fixtures.cjs` from the
repository root to independently check these facts. This verifies the fixture,
not model quality.

Equivalent wording is acceptable. Trimming stored names is not required and
would conflict with the requirement. Optional helper hardening must not be
misrepresented as an existing defect in the guarded case.
