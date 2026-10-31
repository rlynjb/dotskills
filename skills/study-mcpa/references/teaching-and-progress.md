# Teaching, practice, mock exams, and learning progress

## Session pacing and modes

Each session is learner-driven. Keep the big picture accessible but teach **one selected concept, question, or lab step**. Use an overview-first dashboard, stable IDs from the curriculum, and checkpoints rather than a long uninterrupted lecture.

### Guided (default after selection)

Start with the chosen question and its relation to the official domain. Explain in clear, beginner-friendly terms through the four steps from SKILL.md:
1. **Problem and scope:** what the mechanism is for, actors, and assumptions.
2. **High-level map:** a diagram or short text path of key actors.
3. **Concrete deep dive:** a small, correct 2026-07-28 JSON-RPC/message, TypeScript SDK excerpt, or hypothetical failure trace, plus one meaningful trade-off. Mark illustrative messages clearly and avoid inventing mandatory protocol fields.
4. **Wrap-up:** 1–2 takeaways, one teach-back question that asks the learner to reason, and a checkpoint. Wait for their response.

When a learner answers the teach-back, respond to their reasoning, correct gaps with source links, suggest a memory cue, and invite a new ID. If the learner wants a complete walkthrough, provide it in a single response; do not accidentally convert the whole curriculum into a wall of text.

### Practice

- For each question, announce domain/ID and difficulty (foundation/applied), ask a single original multiple-choice scenario (prefer four plausible choices), and **wait for the learner's answer**.
- Do not display correct answers, hints, scoring explanations or answer-marking formatting before the attempt. If asked for a hint, offer a conceptual clue without giving the letter.
- Once answered, mark correct/incorrect, explain the causal reasoning, differentiate every distractor concisely, link to authoritative documentation, and ask the learner to explain the principle in their own words if misunderstood.
- Encourage a confidence value: low / medium / high. A confident wrong answer is a priority for later review.
- Do not claim generated questions are released exam questions, official practice exams, or exam-style equivalents validated by Linux Foundation.

### Mock

- Offer 10-, 20-, or 40-question original mixed-domain mocks; use roughly the official domain distribution and avoid repeats from the immediately preceding session. Score the submitted answers and report per-domain coverage.
- Do not reveal correctness until the mock is submitted, ended, or the learner explicitly exits mock mode. If output limits require batching, preserve state and do not leak the answer key between batches.
- Time is **self-managed by the learner** unless a real timing tool exists. Do not claim the mock was timed by the model, or that the model measured elapsed time.
- Recommend (not assert as an official pass score) aiming for about **85% on two fresh mocks**, with **80% or better per domain**. These are suggested study readiness heuristics only.

### Review

- First revisit low-confidence/wrong concepts and practice with a *new* scenario rather than repeating the same answer key.
- Use spaced review where a persistent record exists: next study session, about 3 days later, about 7 days later; adjust for the learner's calendar. Without background automation, suggest review dates but do not promise reminders.
- Have the learner explain the correct mental model and a counterexample. Mark mastery from repeated demonstrations, not just a self-declared status.

## Progress model

Track (only as supported by available conversation evidence or a user-owned progress file):
- `study_started`, last study date, exam revision verified date.
- Topic ID and domain; status `not started` / `learning` / `needs review` / `confident`; evidence and confidence; last attempt and recommended next review.
- Questions attempted, correct, type, error pattern (concept misconception, protocol-version confusion, distractor, or careless read).
- Lab ID, current step, whether checks were proposed/inspected/executed, proof and safety gates.
- Mocks: question count, domain breakdown, genuine answers, accuracy, notes, and self-timing (if provided).

For an optional lasting record, use [progress template](progress-template.md) in a *learner-owned* path such as `notes/study-mcpa-progress.md` or ChatGPT Library. **Ask before creating/updating it**; never store personal scores in the canonical public DotSkills skill package or evaluator-only suite. If storage is unavailable, offer a compact copy/paste study log and state that future retrieval is not guaranteed.

## Lesson output shape

`Selected: <ID> | Domain | Mode | Reference revision`

- **What and why** (brief)
- **Four-step explanation** (Guided) or **one unanswered question** (Practice) or **one lab checkpoint** (Lab)
- **What evidence supports it** (links or inspected file paths; clearly label hypothetical vs actually run)
- **Takeaway / feedback**
- **Progress** (only what has been observed)
- **Learning checkpoint:** deeper / next / practice / dashboard

Ask one clear question at the end, not a stack of subquestions. If the user needs more technical depth, expand only the selected mechanism.

## Accuracy rules

- Never grade from an uncertain source without checking the source or clearly labeling the uncertainty; prefer to correct a flawed question over penalizing the learner.
- If a source edition changed, tell the learner which revision a question assumes and avoid mixing older and newer protocol behavior.
- Do not infer exam readiness from finishing a deployment or checking off a topic.
- Do not claim an actual exam-style item, Linux Foundation pass rate, official mock score, successful test, or cloud connection unless independently established.
