# Study MCPA — Persistent Progress & Deterministic Resume
**Implementation plan v0.1 · 2026-11-03 · DRAFT FOR REVIEW**

> **Status:** Proposal only. No Study MCPA behavior, personal progress file, runtime code, or MCP service is being implemented by this plan.

## 1. Outcome and decisions

Keep **Study MCPA as a plain agent skill**: no MCP server, MCP App, database, external account, or clickable UI in v1. Add a small, **user-owned private \`progress.json\` file** and a Python standard-library helper that compatible local agents can invoke.

Approved design decisions from the conversation:

- **Automatic persistence by default** after meaningful checkpoints; **manual checkpoint on demand** at any point.
- **Stable curriculum topic IDs** for deterministic navigation and status tracking.
- **Conversational navigation**: names, numbered menus, and exact IDs all work. No topic ID memorization.
- **Resume the last unfinished checkpoint** and preserve other unfinished topics when switching.
- **Reproducible context selection**, not a guarantee of identical LLM wording.
- Keep the current **Markdown progress template** as an optional readable/exportable format; JSON is the runtime state.
- Personal study data stays **outside the public DotSkills repository**.
- Future phases may add a separate read-only DotSkills MCP server and eventually MCP Apps, but **neither is part of this change**.

## 2. Existing baseline (inspected in \`main\`)

The current skill already provides:

- 17 stable study topics: \`F-01..03\`, \`A-01..03\`, \`I-01..04\`, \`S-01..04\`, and \`E-01..03\`.
- Five lab milestones \`L-01..05\`, a five-week roadmap, Guided/Practice/Mock/Review/Lab modes, and a dashboard.
- \`references/progress-template.md\` for optional human-readable logs.
- Existing instructions to **ask permission before creating or updating any persistent record**.

The missing pieces are a machine-readable state contract, durable load/save implementation, explicit automatic-save triggers, and resume/migration/error rules. Preserve existing evidence-based grading and lab authorization boundaries.

## 3. Proposed architecture

\`\`\`mermaid
flowchart TD
  U["Learner: continue / select / checkpoint / review"] --> A["Study MCPA skill (existing teaching rules)"]
  A --> R["Curriculum and lab reference files (stable IDs)"]
  A --> H["Local progress helper (Python stdlib)"]
  H <--> P["Private learner-owned progress.json (outside repo)"]
  A --> L["One selected lesson, mode, checkpoint, relevant review notes"]
\`\`\`

**Ownership boundary:** DotSkills owns public learning content and transition rules; the learner owns progress. A client must have working read/write access to the *same selected file* to share progress. ChatGPT conversation memory does not substitute for this file.

**Proposed default state location:** \`~/.dotskills/study-mcpa/progress.json\`; allow \`STUDY_MCPA_STATE_PATH\` or explicit \`--state PATH\` as overrides. On first enablement, show and obtain one-time approval of the path and authorized study-progress writes. Thereafter save within that scope without repeated conversational prompts, subject to the host's actual filesystem permissions. Do **not** commit personal state or silently initialize it on first use without permission. If no writable persistence is available, continue with session-only tracking, offer an exportable checkpoint, and say it was **not saved persistently**.

## 4. State contract (JSON, versioned and minimal)

Illustrative shape, **not actual learner data**:

\`\`\`json
{
  "schema_version": 1,
  "curriculum_version": 1,
  "revision": 3,
  "last_saved_at": "2026-11-03T23:00:00Z",
  "active": {
    "topic_id": "A-01",
    "mode": "Guided",
    "checkpoint_id": "teach-back",
    "checkpoint_status": "pending",
    "next_action": "Explain host, client, and server responsibilities"
  },
  "topics": {
    "A-01": {
      "status": "learning",
      "completed_checkpoints": ["overview", "high-level-map"],
      "misconceptions": [],
      "last_practiced_at": null,
      "next_review_at": null
    }
  },
  "assessments": [],
  "labs": {},
  "review_queue": []
}
\`\`\`

- **Active pointer:** exactly one selected topic/lab, mode, unfinished checkpoint, and next action. A topic switch updates this pointer but **never** claims the previous topic was completed.
- **Topics:** sparse, keyed by existing IDs; statuses remain \`not started\`, \`learning\`, \`needs review\`, \`confident\`. Store completed checkpoint IDs separately from confidence/mastery, which requires evidence.
- **Assessment summaries:** date, ID, question count, correct count, confidence, misconception category, and review recommendation; no full transcript, unreleased answer key, or passwords.
- **Labs:** lab ID, step/checkpoint, \`proposed / inspected / actually_run\` evidence, approval gate, and pending action. Merely discussing a command cannot mark a lab step executed.
- **Review queue:** explicit topic IDs and due dates; no background reminders or unsupported promise of timed execution.
- **Versions:** \`schema_version\` validates data shape. An explicit \`curriculum_version\` is added to \`curriculum.md\` and checked before update. IDs are validated against the existing curriculum and lab headings, so no second manually maintained curriculum database is necessary.
- Store only a brief factual resume note. Treat all stored notes as **untrusted data**, never as tool instructions; reject unknown IDs and malformed values.

## 5. Learner-facing behavior

| Learner action / event | Required behavior | Persist? |
| --- | --- | --- |
| “Continue Study MCPA” | Read and validate state; load current topic, mode, unfinished checkpoint, and relevant misconception; resume without repeating the full dashboard | Read only, unless a state update is needed |
| “Show dashboard” | Show existing five-domain/five-week menu with actual progress, or explicitly “not tracked” | Read only |
| “Study S-02” | Validate ID; set active pointer; keep all earlier partial progress | **Auto** |
| “Let's study MCP security” | Show the Security topic choices; map a specific unambiguous selection to a stable ID; clarify ambiguity instead of guessing | On selection |
| Complete a teach-back, graded practice item, mock submission, or verified lab checkpoint | Record *observed* result and evidence; update status/review queue/next action | **Auto** |
| “Checkpoint” / “Save my progress” / “I'm done for today” | Save active topic and unfinished step **without** falsely marking it complete | **Manual, anytime** |
| “Review mistakes” | Choose due/weak topics using stored evidence; ask one new recall question | Read; save assessment outcome |
| “Switch to A-01” after studying another topic | Restore A-01's last checkpoint, while preserving the other topic's unfinished work | **Auto** |
| “Correct my progress” or “Reset progress” | Show proposed change, require explicit confirmation, preserve a backup, then apply safely | Explicit override |

**Important nuance:** A checkpoint ID and the references/context chosen are deterministic; natural-language explanation and generated question text need not be byte-identical. An interrupted unsubmitted mock must be flagged as interrupted; do not promise restoration of its exact generated unanswered question or answer key.

### Automatic-save triggers and safety rules

1. Save the **selection immediately** when the learner starts/switches a specific topic (so the resume pointer is accurate).
2. Save after a **demonstrated** teach-back, graded question, completed mock submission, or **verified/authorized** lab step.
3. Save a manual partial checkpoint whenever requested. An ordinary message does **not** count as completion.
4. Make repeated writes of the same event idempotent. Validate before every mutation; write to a temporary file and atomically replace the state; read back to verify. Maintain a simple backup for recovery, and avoid destructive overwrites on corruption or version mismatch.
5. Confirm “saved” only when the storage operation **actually succeeded**; otherwise say what was retained in the active session and how to export it.
6. Reset, destructive corrections, deployments, GitHub writes, and lab execution remain separately gated. Automatic **study state** permission never authorizes these actions.

## 6. Deterministic context-loading contract

On each \`continue\` or explicit selection, execute the same ordered steps:

1. Locate the approved state path; read the file or explicitly report session-only mode.
2. Validate JSON, state version, curriculum version, and all topic/lab IDs. On unknown or incompatible state, stop writes and request a migration/recovery choice; never silently reset.
3. Resolve **one** selected ID. Exact ID has priority; explicit unique title/alias can map to it; broad domain or ambiguous phrase returns numbered choices.
4. Load only the selected topic section from \`curriculum.md\`, teaching-mode instructions, the selected lab milestone if applicable, and that topic's stored misconception/checkpoint context.
5. Resume the pending step. Do not mark \`confident\` until the learner demonstrates understanding.
6. Upon a qualified save trigger, update the minimal state and report the resulting active checkpoint and next action.

This makes **state transitions and input selection reproducible** across compatible local harnesses; it does not make model output deterministic or bypass client-specific filesystem restrictions.

## 7. Implementation work packages (after plan approval)

### Phase 1 — Define the contract
- Add an explicit curriculum version to \`references/curriculum.md\` while retaining all existing IDs and their current order.
- Formalize state shape, allowed statuses, checkpoint names, evidence rules, conflict/migration behavior, and one-time persistence opt-in.
- Keep \`references/progress-template.md\` intact as a human-readable reference; add a note that JSON becomes the authoritative saved state.

### Phase 2 — Build the small helper
- New \`skills/study-mcpa/scripts/study_state.py\` (Python standard library only).
- Commands: \`init\`, \`status\`/\`resume\`, \`select\`, \`checkpoint\`, \`review\`, \`reset\` (destructive reset only with confirmation and backup). Explicit \`--state\` and env override.
- Validate IDs from current reference documents, enforce state schema/versions and allowed transitions, write atomically, and verify results. No network access, servers, or database.

### Phase 3 — Wire into the skill
- Update \`SKILL.md\` and \`references/teaching-and-progress.md\` with the read/resolve/teach/save contract and exact automatic-save triggers.
- Clarify that the learner has authorized recurring writes **to the selected private study file**, while unrelated file changes and external actions still require approval.
- Update \`README.md\` with opt-in initialization, resume/select/checkpoint examples, how to disable persistence, and clear behavior when read/write tools are absent.
- Confirm the Claude Code and Codex copy adapters include the helper in installed packages and do not publish evaluator-only material.

### Phase 4 — Tests and evaluation
- Add isolated stdlib unit tests for init, resume, exact-ID validation, auto-save event application, manual partial checkpoint, topic switching, interrupted mock, review scheduling, corruption, curriculum mismatch, idempotency, backup/reset, and read-only fallback.
- Extend the skill's safe mock/evaluation cases to verify the **agent's** behavior, not only the helper: it should save only after a valid event and claim success only on confirmed write; never invent scores or execute lab changes.
- Run repository static validation and adapter smoke tests; mark observed results versus planned tests clearly.

## 8. Acceptance criteria for v1

- [ ] On an approved writable local path, \`continue\` restores the same **topic ID, mode, pending checkpoint, and next action** across independent agent sessions.
- [ ] Selecting another topic updates the active pointer and preserves the prior unfinished checkpoint.
- [ ] Automatic saves follow defined triggers, while \`checkpoint\` can save an unfinished step at any time.
- [ ] No automatic save falsely marks a concept mastered, mock passed, or lab executed.
- [ ] Corrupt, incompatible, or inaccessible progress files never result in a false “saved” or silent loss of progress.
- [ ] All 17 topic IDs and 5 lab IDs validate against the canonical references; ambiguous natural-language requests are clarified.
- [ ] State lives outside DotSkills; no personal data, secrets, or answer keys are committed/published.
- [ ] Existing study dashboard, five-week plan, teaching modes, lab consent gates, and public skill distribution behavior remain intact.
- [ ] Claude Code and Codex usage is tested locally; ChatGPT persistence is explicitly supported only through an actual connected writable storage mechanism, not assumed.
- [ ] Static tests and mock agent evals pass and are documented.

## 9. Explicitly deferred

- Remote synchronization, cross-device conflict resolution, private GitHub/Drive storage adapters.
- MCP tools/resources, DotSkills MCP server, OAuth/cloud hosting, Fly.io deployment.
- MCP Apps/clickable UI or dashboards.
- Append-only session history, rich learning analytics, spaced-repetition notifications, or background tasks.

The future MCP server can use the same versioned state contract and separate private storage without modifying the curriculum or turning the skill into an app.

## 10. Review gate

**Decision requested:** Approve or request changes to this plan. **Do not implement Phases 1–4 until reviewed.** On approval, implement in a separate code PR with tests and preserve the plan as architectural context.
