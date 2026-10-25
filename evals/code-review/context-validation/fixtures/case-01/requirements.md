# User creation

Review this self-contained, synchronous application snapshot.

- `createUser(input, users)` is the application's only external entry point.
- `input` may be any value produced by decoding JSON.
- A valid input is a non-null, non-array object whose `name` is a string
  containing at least one non-whitespace character.
- For valid input, append exactly one record containing only `name` to `users`
  and return that record. Preserve the supplied name, including whitespace.
- For invalid input, throw a `TypeError` before appending any record.
- The application supplies `users` as a writable array; evaluating that
  internal dependency's type is outside the input-validation requirement.
- `saveUser` is an internal storage helper. No other application entry points,
  callers, storage constraints, or middleware exist in this snapshot.

The scope is the input-validation and write behavior of this complete path.
No before/after diff or test suite is supplied.
