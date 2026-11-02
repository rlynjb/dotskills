# Evaluate Skill proof artifacts

This directory documents historical native evidence and the active Docker-only
v0.4 proof boundary. It intentionally contains
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

**DOCKER_DESIGN_PENDING / BLOCKED — NOT RUN.** The v0.4 implementation is
present and covered by offline tests, including contracts, immutable image and
runtime identity, the shell-free workload, credential gateway, hardened
topology, nine no-model probes, host observer, signed evidence, cleanup, and
the active [`eval_runner.py`](../eval_runner.py) command surface. No real
Docker client/daemon, image, or container has been approved or used by this
workflow, so `real_docker_probes_passed` remains false and the production
capability inventory stays unverified. No Claude or Codex model ran.

The 2026-11-02 local run executed all six probes without Promptfoo or a model.
Five passed; `secondary-tool-route` failed because the sandbox allowed the
host-owned inert executable canary. The status is therefore `FAIL`, not a
partial pass. This is historical evidence only. Native live dispatch is
retired with no fallback. The Docker implementation has not yet been
provisioned or exercised against a real daemon.

The next gate is a separate human decision covering Docker provisioning,
reviewed image build or download, and the real no-model probe command. Only a
complete `READY_NOT_RUN` artifact containing all nine accepted v0.4 probes may
replace `DOCKER_DESIGN_PENDING`. Provider execution requires another fresh,
separate live authorization after that review.

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
