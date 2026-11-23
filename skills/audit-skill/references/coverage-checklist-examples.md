# Audit Skill — Q-01–Q-10 explained for junior developers

This is a **learning reference**, not a completed audit and not a second questionnaire. The ten official questions live in [SKILL.md](../SKILL.md). The examples below are **ILLUSTRATIVE — NOT OBSERVED**: they show how a senior engineer could explain an issue to a junior engineer, but they do not describe a verified problem in a real repository.

## How to read a finding

Imagine a code review. A useful reviewer does not just write "wrong" or "fix it." They point to the relevant code, explain the consequence, and suggest a small, testable improvement.

For each Q:

- **What the question means** — the engineering concept in everyday words.
- **Why it matters** — what could go wrong if it is unclear.
- **Example finding** — what a source-backed audit might explain.
- **Example recommendation** — a practical next action and why it helps.

The real audit additionally shows its check/status and an **actual link to inspected source lines**. It distinguishes **DOCUMENTED INSTRUCTIONS** (written rules), **IMPLEMENTED CHECK** (real validator or guard), **OBSERVED RESULT** (actual authorized run) and **NOT VERIFIED** (missing evidence).

## Q-01 — Purpose & boundaries

**What it means:** What is this skill responsible for, when should someone use it, and what should it never do? Think of this as the skill's job description.

**Why it matters:** If its job is vague, it may act on a task that belongs to another skill or assume it can make a decision no one assigned to it.

**Example finding:** "The skill explains that it summarizes requirements. However, I could not find a rule stating whether it may approve requirements or only recommend changes. That distinction matters because an approval is a human decision, not just a summary."

**Example recommendation:** "Add an explicit 'does not approve requirements' rule and identify who is responsible for approval. This helps the next skill distinguish a suggestion from an authorized decision."

## Q-02 — Activation & discovery

**What it means:** How does an agent find this skill, and how does it know when to use it or not use it?

**Why it matters:** Even a well-written skill will not help if the agent invokes it at the wrong time or overlooks it when it is needed.

**Example finding:** "The file describes what the skill does but not which requests should trigger it. That makes incorrect activation harder to detect."

**Example recommendation:** "Add a short 'use when / do not use when' description and a concrete invocation example. Later, check in a separately authorized evaluation whether the intended requests select it."

## Q-03 — Structure, inputs & dependencies

**What it means:** Which files, facts, tools and configuration must be available before the skill can work? A *dependency* is something the skill relies on.

**Why it matters:** Missing a required input or resource can lead to incomplete answers, guessed details or unnecessary tool calls.

**Example finding:** "The skill refers to a guidance file, but the inspected source does not show what to do if it cannot be loaded. We therefore cannot tell whether the skill should stop or continue with limited information."

**Example recommendation:** "Name the required reference and define a safe missing-file response. Verify that the reference is packaged and accessible in the intended environment."

## Q-04 — Workflow & orchestration

**What it means:** In what order does the skill work, when does it make decisions, and when does it ask for help or pass work to an agent? *Orchestration* means coordinating the steps and participants.

**Why it matters:** If decision rules are unclear, work can be duplicated, a step can be skipped, or the wrong agent can take responsibility.

**Example finding:** "The skill documents the analysis steps, but it is unclear whether a delegated worker can decide that a result is final. This creates uncertainty about who has decision authority."

**Example recommendation:** "Specify which step proposes the result, which step checks it, and which decision needs a human. That makes the workflow easier to follow and review."

## Q-05 — Contracts & outputs

**What it means:** What must a skill receive, what does it promise to return, and what happens when it cannot? A *contract* is an agreement about expected behavior. An *invariant* is something that must stay true.

**Why it matters:** The receiving skill may assume it has complete information when the previous skill only supplied part of it.

**Example finding:** "The output fields are documented, but the instructions do not explain what happens if a required input is absent. The next skill could treat an incomplete result as usable."

**Example recommendation:** "Name the required fields and an explicit BLOCKED/NEEDS HUMAN result when one is missing. This lets a downstream skill stop safely instead of inventing information."

## Q-06 — Context & trust

**What it means:** Where did the information come from, is it trustworthy and current, and what should happen if sources disagree? *Provenance* simply means the origin of the information.

**Why it matters:** Without clear source rules, a skill could treat a quoted example, an old document or untrusted text as the final authority.

**Example finding:** "The skill asks for evidence links, but does not describe what to do when a newer source contradicts an older summary. The agent could silently choose the wrong version."

**Example recommendation:** "Add a rule to show both sources and flag the conflict for the appropriate owner. This prevents the skill from turning uncertainty into an unsupported conclusion."

## Q-07 — Permissions & effects

**What it means:** What may the skill read, change or send, and which host/tool/server restrictions actually enforce that permission? A *side effect* is a real action such as changing a file or posting a ticket.

**Why it matters:** Writing 'read-only' in a prompt does not technically remove a tool's ability to write.

**Example finding:** "The skill instructions say not to edit files, which is a helpful written safeguard. I did not inspect a host permission policy that enforces it, so actual write prevention remains unverified."

**Example recommendation:** "Check the approved host/tool permissions and confirm the skill receives only necessary capabilities. Run enforcement checks only in an authorized environment; do not treat the written promise as proof."

## Q-08 — Failure & stop behavior

**What it means:** What does the skill do when a tool fails, evidence is missing or only some items finish? Does it stop, retry, report partial success or ask a human?

**Why it matters:** Silent partial failures can make the whole workflow appear successful when important items were never completed.

**Example finding:** "The skill explains the happy path but has no clear response for an unavailable downstream tool. The next stage may not realize its input is missing."

**Example recommendation:** "Define a visible BLOCKED or PARTIAL result with the cause and affected item. This preserves completed work while making failures clear to the user."

## Q-09 — Evals & observability

**What it means:** How do we check the skill's behavior, and do we have records of real runs? An *eval* is an evaluation case; a *trace* records what happened during execution.

**Why it matters:** A list of test scenarios is not evidence that the skill passed them. Without traces, a claim about reliability is difficult to verify.

**Example finding:** "The repository contains evaluation cases, which is a useful starting point. However, no actual run results or traces were supplied, so the skill's runtime behavior is still not verified."

**Example recommendation:** "Choose one meaningful scenario and define the exact output that would count as passing. Execute it separately with approved tools and retain its result or trace for review."

## Q-10 — Lifecycle & portability

**What it means:** Who maintains this skill, how do changes get reviewed or rolled back, and which agent environments actually support it? *Portability* means being able to use the same skill across environments with appropriate adaptations.

**Why it matters:** A skill may look portable in Markdown while relying on host-specific agent or tool behavior. Changes can also break existing use cases.

**Example finding:** "The instructions mention more than one coding agent, but no cross-host execution evidence is available. We can confirm the declared intent, not equivalent runtime behavior."

**Example recommendation:** "State supported hosts and owners, record meaningful versions, and compare a representative case on each authorized runtime. Keep a rollback path for regressions."

## Interpreting the result without overclaiming

- **PRESENT** means the applicable part is sufficiently supported by the inspected type of evidence. It does not mean a human approved the design or that a live run passed.
- **PARTIAL** means some important parts are described but other parts still need definition or evidence.
- **MISSING** means the needed definition was not found in a sufficiently inspected source.
- **NOT VERIFIED** means there is not enough source/runtime information to know.
- **NOT APPLICABLE** means a whole question genuinely does not apply, not merely that the evidence is missing.

Do not give every criterion a problem to fix. If the source supports a sound safeguard and no meaningful gap was found, explain what works and state: *Recommendation: None justified from inspected evidence.*

### How this fits the whole Audit Skill

The **same senior-to-junior teaching style** applies outside Q-01–Q-10: to the Step 1 responsibility picture, Step 2 boundary decisions, Step 3 contract cards, consolidated human review, and Step 4 validation preparation. For the full workflow tutorial, return to the [Audit Skill README](../README.md).
