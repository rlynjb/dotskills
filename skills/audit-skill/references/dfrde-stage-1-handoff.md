# DFRDE Stage 1 — Discover: optional audit evidence handoff

This reference guides **evidence handoff**, not question creation. The [DFRDE Engineering Review Template](../../../docs/dfrde/engineering-review-template.md) is the **only source** of the Stage 1–3 review questions, their wording, and their IDs.

## When to use

- **Audit-only request:** Do **not** perform this handoff. Produce the read-only audit findings and evidence gaps, without a questionnaire.
- **Explicit DFRDE Stages 1–3 prefill request:** Read the current engineering review template and use the findings to answer **only its existing Discover question rows**. Do not maintain or invent another list. If the template is inaccessible, say so and provide the audit alone rather than guessing its questions.

## Evidence to supply for Discover

- **Purpose and current reality:** What the target skill is for, its intended users and triggers, sources/revisions inspected, documented workflow, and actual dependencies.
- **Requirements and constraints:** What applicable source files describe about inputs, outputs, standards, safety boundaries, permissions, and non-goals. Distinguish approved requirements from agent proposals.
- **Existing patterns:** Source-backed architecture, declared tools/agents, handoffs, existing safeguards/tests, and meaningful limits on reuse. Do not infer real runtime behavior from written instructions.
- **Known gaps:** Missing files, code access, runtime traces, or human decisions. State who would need to supply evidence, if known.

Cite **direct clickable links** to the inspected source file and relevant lines beside each claim. Use the inspected revision when available. Preserve distinctions between **documented instructions**, **implemented checks**, **observed authorized results**, **inference**, and **not verified**. If evidence is absent, do not invent a citation or claim a failure.

## Prefill boundaries

1. Use only the three **Discover question rows already in the template**; give each a short, source-backed answer or transparent unknown.
2. Treat the user problem, desired outcome, success measures, and owner as **proposed until confirmed** unless authoritative evidence establishes otherwise.
3. Do not answer future Design or Contract questions as if the team had already approved an architecture.
4. Keep the Stage 1 outcome **HUMAN REVIEW REQUIRED**. An audit is not approval, a runtime test, a Jira write, or permission to change code.
5. Do not create evaluation cases, a separate question map, an evidence-key lookup table, or a redundant source index.

Keep proprietary code, tickets, and sensitive evidence in approved locations. The Audit Skill itself remains read-only; writing a review document is a separate authorized action.
