## Review conclusion

**One confirmed blocking defect: invalid input is written to `users` instead of being rejected.** This violates the explicit input-validation contract. The valid-input cases exercised behaved correctly.

### [Blocking] Validate input before invoking storage

**Classification:** Confirmed defect

**Lenses:** AT correctness and invariants; APOSD validation ownership

**Location:** `project/create-user.cjs:4`, with the write at `project/save-user.cjs:3`

**Contract:** `project/requirements.md:7`, `:8`, and `:11`

`createUser` forwards every input directly to `saveUser`. The helper reads `user.name`, builds a record, and appends it without validation. Nothing on this complete call path checks that input is a non-null, non-array object or that its name is a string containing a non-whitespace character.

For example:

```js
const users = [];
createUser({ name: "   " }, users);
```

**Expected:** Throw `TypeError`, leaving `users` empty.

**Actual:** Return `{ name: "   " }` and append that record.

This also affects numbers, booleans, strings, arrays, objects without `name`, and objects whose name is null or another non-string value. For example, `{}` appends a record whose `name` is `undefined`. `null` happens to throw `TypeError` when the helper accesses `user.name`; that incidental failure does not cover the other invalid input classes.

**Smallest reasonable correction:** Add a guard before the call to `saveUser` that rejects input when any of these conditions holds:

```js
input === null ||
typeof input !== "object" ||
Array.isArray(input) ||
typeof input.name !== "string" ||
input.name.trim().length === 0
```

Throw `TypeError` when the guard fails. Use trimming only to determine validity; continue storing the original name so leading and trailing whitespace remain intact. The requirements identify `saveUser` as an internal helper with no other callers, so duplicate validation in both functions is unnecessary.

**Targeted verification:** Rerun the invalid-input cases and assert both the exception type and the absence of an append. Retain valid-name checks for whitespace preservation, record shape, exactly one append, and identity between the returned and appended record.

## Evidence and checks executed

I inspected the complete application snapshot:

- `project/requirements.md`
- `project/create-user.cjs`
- `project/save-user.cjs`

The execution path is `createUser` → `saveUser` → construct `{ name: user.name }` → append → return. No validation precedes the write.

I executed one non-mutating Node.js assertion harness through the supplied command interface, using **Node v24.22.1** and **22 JSON-decoded input cases**. Each case started with an existing record in `users`.

| Cases | Result |
|---|---|
| Four valid inputs: ordinary name, surrounding whitespace, extra properties, and a Unicode name | All passed. Each appended exactly one record containing only `name`, preserved the supplied name and existing record, and returned the appended object. |
| `null` | Passed: threw `TypeError` without appending. |
| Seventeen other invalid inputs: booleans, numbers, strings, arrays, missing name, non-string names, empty name, and whitespace-only names | All failed the contract. Each appended one record and threw no exception. |

Overall: **5 passed; 17 failed**. These failures share one root cause and are reported as one finding.

## Review method and limitations

I read `skill/SKILL.md` and `skill/references/code-review.md`. I used the **Compact daily code-review prompt**, together with its **Evidence and severity calibration**, **Understand and trace the change**, **AT — algorithms and invariants**, **Finding and verification format**, and review-workflow guidance.

Correctness and validation ownership apply directly. DDIA and SDI considerations are limited to the synchronous in-memory write path; the snapshot provides no distributed storage or service architecture. FODE is not applicable. No specialized supporting guides were needed.

This was a review of the supplied snapshot, not a before/after diff. No test suite was supplied; the executed checks were an inline assertion harness. The cases are representative rather than exhaustive over all JSON values. I did not assess malformed `users` dependencies, other callers, middleware, or external storage because the requirements explicitly exclude them. No supplied files were modified.

**The missing validation must be addressed to satisfy the stated contract. No additional actionable defects were found in the inspected scope.**
