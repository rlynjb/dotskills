# Skill trust and security

Skill packages are instruction-bearing artifacts. Importing external skills and prompts requires the same review discipline as importing dependencies.

- **Provenance:** keep upstream source revisions and blob SHA fingerprints; review imported changes before release.
- **Prompt injection:** treat source files, search results, web pages, logs, and tool outputs as untrusted data, never as higher-priority system or user instructions.
- **Least privilege:** require user authorization and harness permissions for writes, network calls, code execution, or external actions. Read-only investigation skills must remain read-only.
- **Secrets and personal data:** do not embed tokens or credentials in skills. Review skill references for personal information before broad distribution or installation into shared machines.
- **Runtime policy:** Buffr's checks, schema validation, research limits, and human approval controls live in Buffr. Do not simulate those controls with a prompt.
- **Validation:** a passing CI check proves only repository structure and source identity. It does not prove that a skill is correct, safe, injection-resistant, or compatible with all harnesses.

Before publishing new imports, inspect the content and any executable scripts, create adversarial examples, evaluate side effects, and require explicit review approval.
