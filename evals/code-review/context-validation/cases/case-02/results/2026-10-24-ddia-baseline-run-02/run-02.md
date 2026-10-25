## Review result

**One actionable finding: a confirmed, blocking violation of the input-validation contract.**

### Invalid input is appended instead of rejected

**Classification:** Confirmed defect

**Severity:** Blocking

**Location:** `project/create-user.cjs:3–4`, through `project/save-user.cjs:1–4`

**Requirement:** `project/requirements.md:6–11`

`createUser` passes its input directly to `saveUser`. The helper constructs `{ name: user.name }` and immediately appends it, without checking the input’s shape, the name’s type, or whether the name contains a non-whitespace character.

Consequently, reachable invalid JSON inputs mutate the application’s authoritative `users` array and return successfully. For example:

| Input | Observed behavior | Required behavior |
|---|---|---|
| `{}` | Appends `{ name: undefined }` | Throw `TypeError` without appending |
| `[]` | Appends `{ name: undefined }` | Throw `TypeError` without appending |
| `{ "name": 0 }` | Appends `{ name: 0 }` | Throw `TypeError` without appending |
| `{ "name": "   " }` | Appends the whitespace-only name | Throw `TypeError` without appending |

This requires no concurrency, retry, or storage failure: one ordinary call with invalid decoded JSON violates the contract. `null` happens to throw a `TypeError` when the helper accesses `user.name`, but that does not protect the other invalid inputs.

**Smallest recommended correction:** Validate at the sole external entry point, before calling `saveUser`:

```js
if (
  input === null ||
  typeof input !== 'object' ||
  Array.isArray(input) ||
  typeof input.name !== 'string' ||
  input.name.trim().length === 0
) {
  throw new TypeError('Expected an object with a non-blank string name');
}
```

Continue passing the original input to the helper after validation so the stored name retains its supplied whitespace. This establishes the required validation-before-write boundary without adding duplicate validation to the internal helper.

## Verification performed

I inspected the requirements and both application source files, covering the complete declared path from `createUser` to `saveUser`. I then ran a non-mutating, in-memory Node.js harness against the supplied implementation using **Node v24.22.1**. Every tested input was passed through JSON encoding and decoding.

- **Five valid cases passed.** Checks covered exactly one appended record, the returned record’s identity, preservation of the supplied name and whitespace, omission of extra input fields, and preservation of an existing array element.
- **Nineteen invalid cases were checked.** Only `null` satisfied the required `TypeError` and unchanged-array behavior. The other **18 cases appended one record without throwing**, covering primitive inputs, arrays, missing names, non-string names, empty names, and whitespace-only names.

## Review boundary and limitations

This was a review of the complete supplied application snapshot, not a before/after diff. No test suite was supplied; the results above come from the local verification harness. Its finite input matrix supports the reproduced defect, while the source inspection establishes the missing validation across the declared call path.

The writable `users` array is the only storage in this scope. No additional entry points, middleware, durable storage, or asynchronous execution were assumed. No other actionable issues were identified in the inspected scope, and no supplied files were modified.
