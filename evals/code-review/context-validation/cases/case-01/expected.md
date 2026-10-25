# Expected behavior — evaluator only

## Correct outcome

Recognize that the sole public entry point validates before the helper writes. Do not report a missing-validation defect on this path.

## Essential reasoning

The guard in create-user.cjs throws TypeError before saveUser for invalid input. The helper is internal; direct external calls are outside the supplied contract.

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
