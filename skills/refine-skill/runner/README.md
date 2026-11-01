# Refine Skill — Claude + Codex evaluation adapter (experimental)

This **skill-local**, standard-library Python adapter connects the existing
Refine Skill stages to native model/harness CLIs. It has no project-wide
package dependency and does **not** vendor Anthropic or OpenAI code.

- **Stage 3:** Paired execution with the current skill and without it.
  Claude uses its noninteractive CLI; Codex uses codex exec with JSONL events.
  Only the selected case and synthetic fixture go to agent workspaces;
  evaluator-only expected outputs, assertions, and earlier runs stay outside.
- **Stage 4:** Semantic assertion grading via a Claude or Codex model. Claude
  requires a locally reviewed, **SHA-256 pinned** copy of Anthropic Skill
  Creator's official agents/grader.md. Codex can use its own model with a
  structured JSON output schema; the same pinned grader guide is optional.
  Deterministic and human review remain part of Refine Skill.
- **Stage 10:** The compare action creates comparison.json containing both
  arms' pass rates and their difference in **percentage points**. It is
  descriptive/provisional, not proof of safety, significance, or generality.

## Security contract — read before running

**This adapter is NOT an isolated host, security proxy, or complete agent
eval framework.** Claude's plan mode, Codex's read-only sandbox, and a JSON
manifest are defense-in-depth, **not** independent isolation. The command-line
flags requiring approvals are operator declarations, not enforceable human
approvals or proof that your OS/network/tool permissions are restricted.

**Do not execute run-pair or grade-pair** unless a separately configured and
independently verified host enforces all of the following: disposable isolated
workspace, approved provider/data routing, no accessible production secrets,
no live write paths, no unrestricted shell/API/network bypass, child-agent
restrictions, complete host-generated attempted-action traces, and post-run
state verification. Apply [Execution Safety Gate](../references/execution-safety-gate.md).
The host MUST enforce per-tool authorization; this runner cannot guarantee it.

For workplace use, obtain employer authorization before any proprietary
code, prompts, logs, or outputs are sent to external providers. **V1 is
synthetic-only** and deliberately refuses model execution without the
separate case/provider approval flags, synthetic-only declaration, and
host-enforcement declaration. Those flags alone are not sufficient safety
evidence. Do not treat a manifest validator as a sandbox.

**No executable safe host was provided or verified in this change.**
Therefore the real Claude/Codex evaluations remain **Blocked — Not Run**
until the host and provider access are configured and approved. Your
existing Stage 2 cases and fixtures remain intact.

## Offline validation

From the DotSkills root:

    python3 -m unittest discover -s skills/refine-skill/runner -p 'test_*.py' -v

A safe static preflight (never calls a model):

    python3 skills/refine-skill/runner/runner.py preflight \
        --suite skills/learn-repo/evals/evals.json --case-id 1

The Stage 2 case must actually exist in that workspace; the example
path will be absent if the fixture is local/uncommitted.

## Host-only execution flow (reference; DO NOT run in ordinary shell)

After separate human/provider approval **and independent host verification**:

    python3 skills/refine-skill/runner/runner.py run-pair \
        --suite skills/learn-repo/evals/evals.json --case-id 1 \
        --harness claude --host-manifest /verified/host-manifest.json \
        --approved-case --approved-provider --host-enforced --synthetic-only \
        --output /isolated/eval-workspaces

Use --harness codex when executing under the approved Codex host. Both
arms use the same case and fixture, in separate fresh workspaces, and
receive **different skill access**. Each run writes to a unique directory;
nothing replaces existing saved fixtures or previous runs.

After the first observed outputs, define evidence-based assertions in
the approved case and freeze them symmetrically for both arms. For
Claude, install/review the upstream [Skill Creator grader](https://github.com/anthropics/skills/blob/main/skills/skill-creator/agents/grader.md)
on the approved host and calculate its SHA-256:

    shasum -a 256 /reviewed/skill-creator/agents/grader.md

Then run **only inside the approved grading host**:

    python3 skills/refine-skill/runner/runner.py grade-pair \
        --suite skills/learn-repo/evals/evals.json --case-id 1 \
        --harness claude --run-dir /isolated/eval-workspaces/RUN-ID \
        --host-manifest /verified/host-manifest.json \
        --approved-provider --host-enforced \
        --grader-instructions /reviewed/skill-creator/agents/grader.md \
        --grader-instructions-sha256 EXPECTED_DIGEST

Codex uses --harness codex, with its own Codex model as judge, and
passes a restrictive output schema to codex exec. The same reviewed
grader.md can optionally inform the Codex grading rubric.

After grading, compare the **same case revision** with:

    python3 skills/refine-skill/runner/runner.py compare \
        --suite skills/learn-repo/evals/evals.json --case-id 1 \
        --harness claude --run-dir /isolated/eval-workspaces/RUN-ID

This produces output.txt, trace.txt, grading.json and comparison.json.
**The CLI's trace is not a trusted host action/state trace**; a separate
host audit must evaluate attempted tool effects before security can be
graded. A failed or missing host audit must remain Unknown/Blocked, never
a fabricated Pass. Human approval still controls all skill edits.

## Native tooling limitations

Anthropic's Skill Creator handles behavioral cases through independent
subagents. Its scripts/run_eval.py only tests whether a description
**triggers** the skill; it is not a behavioral runner. Here we use
approved noninteractive Claude CLI execution and the official pinned
grader instructions, not a vendored or automatically installed Anthropic
subagent runtime.

OpenAI documents codex exec --json for structured execution traces and
--output-schema for model-assisted grading. This adapter uses those CLI
capabilities but does not install Codex, provision authentication,
manage model costs, or enforce the host sandbox.

The host may need controlled, approved model API access while agent tool
egress remains blocked; that enforcement is infrastructure outside this
skill. No code here proves that boundary exists.

## Known limits

- No actual Claude Code or Codex CLI/model run has been verified in this
  repository change. Offline tests exercise file staging, argument
  construction, grading validation, and denial paths only.
- Input staging copies SKILL.md and references/, not arbitrary executable
  scripts/assets. Skills requiring such resources need a reviewed extension.
- The provisional compare action aggregates assertion pass rates but does
  not implement the optional blind comparator agent or viewer yet.
- Missing/unsafe host configuration stops the workflow at Stage 3;
  no automatic jump to Stage 4–11, simulated grades, or performance claims.
