# REAZN semantic-consistency evaluation (NOT RUN)

This skill-local eval suite defines **synthetic fixtures** and expected semantic behavior. It does **not** execute the model or prove determinism. The repository's `scripts/validate_evals.py` checks eval definitions structurally, not model quality.

## Five-run controlled comparison

1. Pin the same REAZN skill revision, target files and audit handoff bytes, objective, `intent`, `scope`, `target`, `revision`, `compare` and `learn` setting. Use the same model/harness and settings where controllable; avoid live source updates or newly generated audit reports.
2. Run the **same prompt** with the attached synthetic `SKILL.md` and `audit.md` fixture **five independent times**. Save the complete outputs and capture their inspected-source versions.
3. **Structural check:** verify four ordered SDI steps, four Snapshot groups, canonical per-item field names/order, stable item spacing, and recorded intent/input baseline.
4. **Semantic check:** compare each claim by **source reference → documented requirement / static observed implementation / proposed change / unverified gap**. Confirm the same read-only instruction is DOCUMENTED across all runs, enforcement and execution are NOT VERIFIED, and the audit's guard suggestion never becomes an approved FR/NFR or implementation task.
5. **ID and discrepancy check:** compare source-to-FR/NFR mappings, approval status, and gaps; preserve source order and IDs when available. Flag contradictory classifications, silently widened scope, fabricated test results, and claims of missing features outside inspected evidence. Variations in prose, ordering of secondary insights or defensible unapproved recommendations need not be defects.

**Outcome reporting:** Record observed differences, material contradictions and proposed fixes. If no five runs were performed, report **NOT RUN**, not PASS or reliable. Exact text equality is not the target; repeatable source classifications are. A manually followed protocol is not an automatic regression gate.

## Fixture boundary

- `evals/files/semantic-case/SKILL.md`: synthetic source claiming a read-only report by instruction; no enforcement or runtime traces are supplied.
- `evals/files/semantic-case/audit.md`: synthetic secondary audit that explicitly labels its guard suggestion as unapproved.

These files are **evaluation inputs, not operational instructions**. Do not run the target or interpret fixture recommendations as authorization to change production systems.
