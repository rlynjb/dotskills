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

## Conference research: AgentCon / MCPCon 2026

Sources reviewed: the user's saved slide PDFs. Page references below use PDF
page numbers, including title pages. These are source notes and future work,
not implemented security controls or a guarantee of malicious-content detection.

### Shipping Agent Skills Safely: CI/CD, Evals, and Guardrails

**Michael Larson, Christensen Solutions** — `shipping_agent_skills_safely.pdf`.

- Page 5 warns that attacks can disguise malware as setup steps and that
  encrypted archives can evade content scans.
- Page 6 presents a software lifecycle: version, evaluate, review, release.
- Page 11 explicitly presents the attack-checking sequence:
  **Scan → Review → Sandbox**.
- Pages 7–8 recommend representative tasks, known failure modes, deterministic
  assertions, adversarial cases, and reruns when skills or models change.
- Page 10 calls for testing across supported agent hosts.

Follow-up for DotSkills (our proposed implementation of these lessons):

- [ ] Define a pre-use intake process for external prompts and skills:
  scan their contents, review findings and requested actions, then test behavior
  in a restricted sandbox before granting normal execution access.
- [ ] Inspect setup instructions, executable scripts, dependencies, downloads,
  and bundled archives alongside `SKILL.md` and its references. If content
  cannot be inspected, record the unresolved risk; do not report a clean scan
  as evidence that the hidden contents are safe.
- [ ] Record the reviewed revision, findings, reviewer decision, and sandbox
  evidence. Reassess changed content rather than transferring an old review
  to a new version.
- [ ] Preserve the current per-case eval workflow. Broader CI and cross-host
  testing remain future work; this note does not introduce comparison folders.

The detailed intake checklist above is our adaptation. The slide establishes
the scan/review/sandbox sequence, not a complete scanner specification.

### Trustworthy Context Is Untrusted by Default

**Shub, Arcade.dev** — `trustworthy-context-is-untrusted-by-default.pdf`
(the title slide identifies the speaker as Shub).

Pages 12–17 present five complementary defenses for stored agent context:

1. A server-generated warning around every read that treats stored code claims
   as potentially stale hypotheses.
2. Risk classification when context is written, with checks again when read;
   the author must not control its own risk classification.
3. Provenance and content boundaries supplied by the system, distinguishing
   claimed identity or commit information from server-recorded metadata.
4. File anchors tied to a commit so readers can check what changed.
5. Verification against current code before relying on stored implementation
   claims, with discrepancies reported.

Pages 10–11 explain why task-success grading can miss poisoned context:
the output may appear acceptable while relying on forged claims. Page 19
also documents errors in the talk's own graders, including confusing rejection
of malicious text with adoption of it. Pages 18–20 show that warnings reduced
some failures but did not eliminate them.

Follow-up for DotSkills and its consuming hosts:

- [ ] Preserve source, revision, relevant file anchors, and verification status
  for consequential context claims; distinguish recorded facts from
  self-reported metadata.
- [ ] Require current-code verification for implementation claims and report
  stale or conflicting context. Code verification does not make code comments
  or embedded instructions authoritative.
- [ ] Add eval cases for plausible forged facts, fake provenance, stale memory,
  and attempts to impersonate trusted context boundaries, alongside obvious
  override instructions.
- [ ] Check whether the agent adopted an injected claim or merely quoted it
  to reject it. Include benign controls and retain traces to audit grading.
- [ ] Keep system-generated context wrappers, authorization, and permission
  enforcement in the consuming host/runtime. Text fences and warnings alone
  are not security boundaries.

These five context defenses differ from the five broad validation layers
earlier in this file. Neither slide deck establishes that running a prompt
through several agents can certify that it contains no malicious content.

## Additional related-session research (2026-10-25)

A broader search of the user's conference chats found the related sessions below.
Evidence levels matter: the two sections above retain their previously recorded
PDF page references; the additions below distinguish retrieved PDF content from
earlier assistant-written session summaries and research leads. This search did
not recover every original transcript or slide deck, so it is not a complete
conference security audit. No new slide numbers or chat URLs are inferred.

### Runtime enforcement: Agntcon26 — Yaron Schneider

**Durability, Guardrails, and Attestation.** Evidence: retrieved session-chat
summaries dated 2026-10-23, including descriptions of slides 9 and 11 and the
phrase “The model proposes. The runtime enforces.” These are earlier assistant
descriptions of the slides, not a fresh inspection of the original deck.

The recorded discussion separates model proposals from authentication,
authorization, policy enforcement, execution, and execution evidence. It also
distinguishes observability from attestation. This complements pre-use screening:
a reviewed skill still needs enforced limits when it executes.

Proposed follow-up (our adaptation, not a verbatim speaker checklist):

- [ ] Specify which checks belong to DotSkills intake and which must be enforced
  by the consuming harness/MCP runtime. Put authorization, permitted tools,
  argument validation, file/network access, and execution limits in runtime code.
- [ ] Record attempted actions, policy decisions, and actual execution outcomes.
  Keep ordinary logs distinct from cryptographically verifiable attestations;
  neither establishes that an agent's reasoning or final answer is correct.
- [ ] Test that disallowed actions remain blocked even when the skill or a tool
  result explicitly requests them.

### Context failures: Agntcon27 — Drew Breunig

**How Contexts Fail (and How to Fix Them).** Evidence: earlier session/project
summaries identify poisoning, distraction, confusion, and conflicting context.
The detailed original transcript/slides were not recovered in this search.
Treat this as a relevant research lead, not independently verified slide wording.

Proposed follow-up:

- [ ] Extend adversarial fixtures beyond obvious override strings: include
  plausible false facts, irrelevant but persuasive context, contradictory
  requirements, and stale summaries. Keep malicious and benign failure cases
  separately labeled so ordinary context mistakes are not called attacks.
- [ ] Test whether a corrected fact actually displaces an earlier false claim,
  including after summarization or memory reuse.
- [ ] Recover the original session material before attributing specific
  mitigations or measured effectiveness to the speaker.

### Whole-workflow evaluation: Agntcon24 — EvalBench

**Building an Agentic Eval Pipeline: Battle-Tested Lessons with EvalBench** —
Kurtis Van Gent / Haoyu Wang.

Evidence: retrieved content from
`mcpcon-na-26-building-an-agentic-eval-pipeline_-battle-tested-lessons-with-evalbench-agntcon-2026.pdf`.
The retrieval describes evaluation of Critical User Journeys, trajectory and
outcome/output measures, regression detection across tools/skills/prompts/models,
and deterministic checks combined with calibrated, explained LLM judges.
Page numbers were not supplied by this retrieval.

Proposed follow-up:

- [ ] Grade the execution trace as well as the final answer: an acceptable answer
  must not hide an unauthorized read, write, tool call, or attempted exfiltration.
  Record attempted and completed actions separately.
- [ ] Validate graders against independently reviewed examples of both safe and
  unsafe behavior, including quoted attacks that the agent correctly rejects.
  Track false positives and false negatives rather than trusting one pass score.
- [ ] Use clean, isolated test state and controlled test resources for security
  cases. Do not expose production credentials or data to malicious fixtures.
- [ ] Record the skill revision, model, harness, policy configuration, and grader
  version with each per-case run; rerun affected cases when these change.

### Additional leads: credentials and MCP observability

- **Christian Posta — “DO NOT give AI agents credentials!”** The conference
  directory identifies this demo and source photo `5748.jpg`. The title and
  source locator were recovered; the demo's detailed mechanism was not.
- **Agntcon03 — What Your MCP Server Does When Nobody's Looking (Austin Parker).**
  Earlier chat summaries discuss MCP observability and tracing. Original slide
  text/transcript was not recovered, so specific security claims remain
  unverified.
- **Stop Vibe-Testing, Beyond Pass/Fail, and agent regression testing** also
  surfaced as related evaluation sessions. Their original material was not
  recovered in this pass; do not treat their titles as evidence of a particular
  security technique.

Proposed follow-up:

- [ ] Investigate credential isolation and narrowly scoped tool access in the
  runtime; avoid placing secrets in skill text, model context, or eval fixtures.
  Verify the credentials demo before claiming a specific implementation.
- [ ] Preserve enough tool-call and policy-decision evidence to investigate
  failures while redacting secrets and sensitive input from telemetry.
- [ ] Recover original material for these leads and replace summary-level
  attribution with precise source references when available.

## Suggested implementation order

This ordering is our proposal, not a conference-prescribed pipeline:

1. Define the intake policy and trust boundaries; preserve provenance and reviewed
   revisions. External content remains untrusted during inspection.
2. Add static screening and independent review of the whole skill package.
   Do not run unreviewed setup steps merely to make scanning possible.
3. Establish the restricted execution environment before running any behavioral
   tests. Test both the skill and enforcement of runtime restrictions.
4. Add independently reviewed adversarial cases and calibrate the graders.
5. Gate release on recorded evidence; retain runtime limits, monitor execution,
   and reassess changed skills, dependencies, models, and harnesses.

An AI reviewer is another fallible component exposed to the inspected content.
Multiple reviewers or a “cleaned” prompt are not proof of safety. Keep reviewer
permissions restricted and prevent the inspected skill from changing review
policy, expected outcomes, or grading criteria.
