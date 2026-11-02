# Provider-native proof artifacts

This directory documents the v0.2 proof boundary. It intentionally contains
no provider output, authentication material, fixture content, or claimed live
result.

Offline orchestration can create a unique run directory with independent
`with-skill` and `without-skill` workspaces, equivalent fixture digests, and a
plan-bound `proof-manifest.json`. Evaluator-only answer keys, prior results,
grader files, symlinks, and `evals.json` are rejected from agent fixtures.
The orchestration contract keeps provider authentication in the trusted
driver boundary; its offline helper creates a scrubbed agent environment and
supplies secret values to evidence redaction only in memory. The live boundary
still has to prove that the provider runtime honors this separation.

A provider result is not a completed proof without a matching
`EvidenceBundle`. Each arm retains separate execution, quality, and safety
statuses. The pair is complete only when both arms are complete; no synthetic
cross-provider or cross-dimension score is produced.

## Current status

**BLOCKED — NOT RUN.** The offline coordinator and tests exist, but no real
Claude or Codex proof has been authorized or executed. The committed
capability inventory still marks native runtime confinement as unverified,
and this repository does not yet provide an independently operated native
boundary launcher, provider-auth gateway, or trusted action-trace collector.

Before a real proof, the human gate must identify and approve all of the
following for each provider separately:

- exact synthetic case, fixture digest, skill/rubric revisions, provider,
  model snapshot, adapter, and installed tool versions;
- maximum turns, duration, output size, and cost;
- provider-auth location and proof that credentials are unavailable inside
  both evaluated arms and their traces;
- exact filesystem/tool/network/effect surfaces and all required negative
  probes in the effective runtime;
- external data disclosure and the provider policy that permits it;
- protected/disposable snapshot roots, action-trace destination, native
  result path, cleanup evidence, and retention decision.

If any scoped approval, installed-version match, runtime control, probe,
trace, state comparison, or cleanup guarantee is missing, retain
`BLOCKED — NOT RUN`. Do not update a capability to `verified` from offline
tests, a prepared config, a provider setting, or a self-authored receipt.
