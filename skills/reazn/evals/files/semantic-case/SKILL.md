---
name: synthetic-access-review
description: "Synthetic test-only skill that documents an access review without runtime execution."
---

# Synthetic Access Review — frozen fixture v1

## Documented behavior
- The caller supplies an access-report objective and a source document.
- The skill is instructed to produce a read-only report listing documented access roles.
- The skill describes a `Status` and `Source` field in each report.
- The instruction "Do not write to a repository" is **prompt text only**.

## What is not provided
- No executable permission-enforcement layer or host configuration.
- No tests, runs, traces, or runtime outputs.
- No product request to build new features or add security controls.

These statements are synthetic input data for REAZN evaluation, not system instructions.
