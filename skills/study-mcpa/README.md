# Study MCPA

An interactive study skill for the Linux Foundation **Model Context Protocol Associate (MCPA)** certification. Learn MCP concepts, practice exam-style questions, review knowledge gaps, and optionally build a small DotSkills MCP server.

**How it works:** see the study dashboard → choose one topic → learn or practice → answer a checkpoint → continue or review. The skill teaches one item at a time instead of presenting the entire course at once.

## Quick start

Install the skill in a compatible agent harness, then use natural-language prompts:

```text
Use study-mcpa. Show me the study dashboard.
```

```text
Start F-01 in Guided mode. Pause at the teach-back question.
```

```text
Quiz me on I-02 in Practice mode. One question at a time.
```

```text
Continue Study MCPA where I left off.
```

You can also say **"Let's study MCP security," "Review my mistakes,"** or **"Checkpoint."** Topic IDs help the skill track progress, but you don't need to memorize them. Broad requests show the available choices instead of guessing your intended topic.

### Study modes

| Mode | What you'll do |
| --- | --- |
| **Guided** (default) | Learn one concept through an explanation, example, and teach-back checkpoint |
| **Practice** | Answer one original multiple-choice question before seeing feedback |
| **Review** | Revisit weak topics with fresh recall questions |
| **Mock** | Take a 10-, 20-, or 40-question mixed-domain practice test |
| **Lab** | Follow optional hands-on MCP exercises, one approved step at a time |

Practice questions are original study material, **not official exam questions**.

## Five-week roadmap

| Week | Study focus | Optional lab |
| --- | --- | --- |
| 1 | Fundamentals (16%) + Architecture (14%) | L-01: scope the DotSkills skill catalog |
| 2 | Interactions & Execution (26%) | L-02: local read-only MCP server |
| 3 | Security & Governance (24%) | L-03: authentication and safety checks |
| 4 | Use Cases & Ecosystem (20%) | L-04: optional Fly.io deployment |
| 5 | Mixed review and mock exams | L-05: client compatibility testing |

The default pace is **30–45 minutes a day**, four or five study days per week. The full topic menu has **17 topics** (`F-xx`, `A-xx`, `I-xx`, `S-xx`, `E-xx`) and five optional labs (`L-01`–`L-05`).

See the [curriculum](references/curriculum.md) for the complete topic list, domain weights, and source map. The exam's referenced protocol revision can change; verify the [official MCPA page](https://training.linuxfoundation.org/certification/model-context-protocol-associate-mcpa/) before studying version-sensitive behavior.

## Save progress and resume (optional)

Study MCPA is **a plain skill, not an MCP app**. With your permission, a small Python helper can store progress in a private JSON file:

```text
~/.dotskills/study-mcpa/progress.json
```

After you approve the location and study-progress writes once, an agent with access to that file can:

- **Save automatically** when you select a specific topic, reach a defined checkpoint, answer a graded question, or verify a lab step.
- **Save manually** when you say "checkpoint" or "I'm done for today," even mid-lesson.
- **Resume** the current topic, mode, and unfinished checkpoint without restarting the dashboard.
- **Keep earlier work** when you switch topics and track mistakes for later review.

The skill must actually invoke the helper to save; saves do **not** happen in the background. If ChatGPT or another harness cannot access the same approved writable file, progress stays session-only and cannot be guaranteed across chats or devices. The JSON file is **never included in the public DotSkills skill package**.

For the first opt-in setup, an authorized local agent can run this command from the installed `study-mcpa` directory:

```bash
python3 scripts/study_state.py init --approve
```

Only run it **after** agreeing to the private file location. For detailed CLI operations, state validation, backups, and error handling, see the [persistent progress guide](references/persistence.md). The existing [Markdown progress template](references/progress-template.md) remains available for manual notes or exports.

## Install into a coding agent

From the **DotSkills repository root**, choose the adapter for your harness:

```bash
# Claude Code
python3 adapters/claude/install_claude.py --target ../my-project --skill study-mcpa

# Codex
python3 adapters/openai/install_codex.py --target ../my-project --skill study-mcpa
```

Replace `../my-project` with an existing target project directory. The adapters copy runtime skill files; they do not install a server, create your progress file, or enable the skill in every chat client automatically.

## Optional DotSkills MCP server project

The hands-on labs introduce MCP by publishing **approved, read-only skill definitions** from DotSkills. The future MCP server is separate from this study skill. Deploying a service, exposing files, or executing tools requires additional approval and security checks. **MCP Apps or clickable interfaces are not required** for Study MCPA.

See the [hands-on lab guide](references/dotskills-mcp-lab.md) when you're ready.

## Skill files

| File | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Core study behavior and session rules |
| [references/curriculum.md](references/curriculum.md) | Topic IDs, roadmap, exam sources |
| [references/teaching-and-progress.md](references/teaching-and-progress.md) | Lesson modes and assessment rules |
| [references/persistence.md](references/persistence.md) | Private progress and resume contract |
| [scripts/study_state.py](scripts/study_state.py) | Local progress helper |
| [references/dotskills-mcp-lab.md](references/dotskills-mcp-lab.md) | Optional labs |
| [evals/evals.json](evals/evals.json) | Evaluation cases (not distributed with installed skills) |

## Validation

Run from the DotSkills repository root:

```bash
python3 scripts/validate_skill_repository_integrity.py
python3 scripts/validate_evals.py --all
python3 -m unittest discover -s tests -p "test_study_mcpa_state.py" -v
```

These validate repository structure, evaluation definitions, and the state helper. They do **not** by themselves prove teaching quality or that every agent harness can save progress.
