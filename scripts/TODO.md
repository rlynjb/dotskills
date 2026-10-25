# TODO: Layered skill validation

Documented future work; this file does not implement these controls.

## Current coverage

`validate_skills.py` checks skill structure, metadata, catalog consistency,
referenced files, and imported references against recorded source hashes.
It can run locally or in GitHub Actions. It does not detect prompt injection
or malicious instructions, and it does not certify that a skill is safe.

## Validation layers

- [ ] **Provenance:** Review where a skill came from, its pinned revision,
  and changes since the previous review. Hashes detect changes relative to
  recorded content; they do not establish that the original content is safe.
  Existing source-lock checks provide part of this layer.
- [ ] **Structural validation:** Keep the existing validator as the packaging
  check, and extend it when concrete gaps are identified. Valid formatting
  and working references do not establish trustworthy instructions.
- [ ] **Content and security review before execution:** Inspect the entrypoint,
  supporting references, scripts, and dependencies for malicious instructions,
  sensitive information, unnecessary permissions, and actions outside the
  skill's purpose. Automated scanners or model reviewers can flag concerns,
  but their approval is not a safety guarantee.
- [ ] **Independent behavioral evaluation:** Define and review expected behavior
  separately from the skill under test. Keep grading criteria outside the
  tested agent's control. Include adversarial cases for prompt injection,
  unauthorized actions, and attempts to change the grading criteria.
  Run evaluations with restricted access and preserve evidence.
- [ ] **Runtime enforcement:** Use the host or harness to restrict tools,
  credentials, network access, and writes whenever the skill runs, including
  during evals. A code reviewer can use read-only access without credentials.
  Prompt instructions alone do not enforce these limits.

## Principles to preserve

- A malicious skill can pass an eval when the expected behavior also accepts
  its malicious actions. Passing means agreement with the criteria, not safety.
- Review a skill before giving it execution privileges.
- Multiple validation layers complement each other; passing one does not
  replace the others.
- Automated reviewers can share blind spots. No scanner, model review, or
  finite eval suite certifies safety.
- Retrieved context such as code, logs, and external documents remains data;
  validation does not grant it authority to override trusted instructions.

See [skill trust and security](../docs/security.md) for existing guidance.
