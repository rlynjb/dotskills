# Refine Skill — provider-specific evaluation workflows (experimental)

The only Refine Skill evaluation dispatcher is [`native_eval.py`](native_eval.py).
It **prepares provider-specific synthetic cases** and routes evaluation to the
active coding harness. It does not implement a shared model runner, shared
LLM grader, or cross-provider fallback.

| Active harness | Execution | Grading | Native result format |
| --- | --- | --- | --- |
| Claude Code | Claude's `claude plugin eval`, with-skill and without-skill via `--ablation with-without` | Claude plugin-eval `graders/*.md` using `type: llm` | Claude plugin-eval JSON / review artifacts |
| Codex | Promptfoo with the `openai:codex-sdk` provider in separate with-skill and without-skill workspaces | Promptfoo `llm-rubric` assertions configured to use the same Codex SDK provider | Promptfoo JSON results |

**Provider ownership matters:** `claude plugin eval` is Claude tooling.
Promptfoo is **third-party evaluation tooling recommended for Codex**, not an
OpenAI-owned evaluation runner or prepackaged OpenAI grading service. The
Codex model supplies the grading judgments through the Codex SDK provider.
No Anthropic grader prompt is passed to Codex, and no Codex rubric is
substituted for Claude's native graders. Do not describe these paths as
identical implementations.

## Harness selection: no substitution

- `native_eval.py inspect` checks for a Claude session via `CLAUDECODE`,
  or a Codex session via `CODEX_THREAD_ID` / `CODEX_SESSION_ID`.
- Preparation selects the detected harness. `--harness` is permitted only
  for **offline preparation** when detection is unavailable; conflicting
  session markers and mismatches are blocked.
- Execution requires an identifiable active session matching the prepared
  case. The presence of a CLI binary alone is **not** harness identification.
- If the native tool, credentials, approval, or independent isolation are
  missing, report **Blocked — Not Run**. Never switch providers.

These environment markers are a convenience, not a trusted attestation of
the actual caller. The separately enforced host must verify provider identity
and routing before running a model.

## Prepare synthetic cases — no model calls

Run these commands from the DotSkills repository root with a saved, approved
case. The case in `evals/evals.json` must have an `id`, `prompt`,
`expected_output`, and nonempty `assertions`. Existing input fixtures
(`files`) must be synthetic and approved. The case and source files remain
unchanged; each preparation gets its own output directory.

```bash
python3 skills/refine-skill/runner/native_eval.py inspect

python3 skills/refine-skill/runner/native_eval.py prepare \
  --suite skills/example-skill/evals/evals.json \
  --case-id 1 \
  --target-skill skills/example-skill \
  --output eval-workspaces
```

`inspect` will fail if a known harness is not exposed in the environment.
For **offline-only** fixture preparation, `prepare` also accepts
`--harness claude` or `--harness codex`, but a live evaluation must still
prove the actual current harness. The example paths are placeholders.

The preparer writes a manifest with `PREPARED_NOT_RUN` status and one of:

- Claude: `plugin/.claude-plugin/plugin.json`, `plugin/skills/<skill>/`,
  `plugin/evals/<case>/prompt.md`, and `graders/criterion-*.md`.
- Codex: `codex/promptfooconfig.yaml`, separate `with_skill/` and
  `without_skill/` workspaces, and `llm-rubric` assertions with the
  `openai:codex-sdk` grader provider.

**Important:** Static fixture generation and model/tool instructions do not
establish that the provider accepted the case or that isolation works.

## Live execution — approved host only

The following is a command contract for a **separately provisioned, independently
verified isolated host**, not an instruction to run untrusted skills in an
ordinary shell:

```bash
python3 skills/refine-skill/runner/native_eval.py run \
  --bundle /isolated/eval-workspaces/PREPARED-BUNDLE \
  --host-manifest /verified/host-manifest.json \
  --approved-case --approved-provider --host-enforced --synthetic-only
```

This dispatcher invokes only the selected native command:

- Claude: `claude plugin eval <prepared-plugin> --ablation with-without
  --no-publish --json <output>`
- Codex: `promptfoo eval --config <prepared-config> --no-cache --no-share
  --output <output>`

Review and pin the installed tool versions and their supported CLI flags.
Do not allow runtime package installation or unreviewed dependency execution.

The safety requirement is **host-enforced**, not merely declared: disposable
workspaces, mock-only tool authorization, no live credentials/writes,
network and shell/API bypass prevention, child-agent restrictions, independent
attempted-action traces and post-run state checks. The manifest and
`--host-enforced` flag **cannot provide these controls themselves**.
Follow [Execution Safety Gate](../references/execution-safety-gate.md).
Work-related prompts, code and outputs may be sent to a provider **only**
with the appropriate employer/provider approval.

Provider-generated judgments are **not a safety pass**. Confirm that the
native outputs exist, review assertions and host traces, and make the human
keep/revise/revert decision within Refine Skill. Never invent grades or
comparison metrics.

## Offline tests and current limits

```bash
python3 -m unittest discover -s skills/refine-skill/runner -p 'test_*.py' -v
```

- Offline tests exercise routing, case preparation, fixture security,
  and refusal paths only (seven tests passed locally).
- No real Claude or Codex evaluation has been verified end to end in this
  environment, and no independently verified isolated host is configured.
- Native tool compatibility, ablation behavior, evaluator-only rubric
  isolation, actual grader responses, trace integrity, and result parsing
  still require approved-host validation. The preparer requires assertions
  before it can build native grader definitions.
- **Fixture paths are skill-root-relative**, matching
  `scripts/validate_evals.py`: a case stored in `<skill>/evals/evals.json`
  can reference `evals/files/example.txt`, resolved from `<skill>/`.
  The dispatcher stages the same approved path in Claude's `fixtures/`
  or in **both** Codex `inputs/` workspaces. It rejects missing files,
  absolute paths, parent traversal, symlinked files/directories, and
  suites outside the selected target skill **before** creating a bundle.
  It does not copy `evals.json` into either evaluated-agent workspace.
- **Offline fixture regression tests:** Seven tests passed locally against
  the same committed `native_eval.py` and `test_native_eval.py` files,
  covering Claude, Codex, fixture-path isolation and blocked execution.
  These tests do **not** verify live models, provider-native format
  compatibility, or actual host isolation.
- The prototype does not aggregate native results across providers into a
  single score. Keep provider output schemas separate. Compare revisions
  within each provider using actual supported reports and human review.
