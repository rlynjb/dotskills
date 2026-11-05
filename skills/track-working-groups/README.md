# Track Working Groups

**Track Working Groups** is a reusable DotSkills skill with a real, standard-library Python CLI for keeping up with working-group activity. It maintains a user-editable group registry, checks public GitHub updates **and AAIF's public working-group calendar**, remembers previously seen items, and saves source-backed briefings.

## Quick start

From the DotSkills repository (macOS/Linux, Python 3.11+, no pip install needed):

~~~bash
python3 skills/track-working-groups/scripts/wg.py init
python3 skills/track-working-groups/scripts/wg.py list
python3 skills/track-working-groups/scripts/wg.py
~~~

The third command checks all active groups **and automatically retrieves upcoming meetings** from the public AAIF calendar, prints a fixed six-section briefing, and saves it. The first successful run looks back 30 days. Later runs overlap their last successful source checkpoint by one day. An explicit --since may expand, never narrow, the lookback. A source error is not treated as no activity.

An optional executable wrapper, scripts/wg, lets you invoke the CLI as wg if **you add that wrapper to your PATH** (for example via a personal ~/.local/bin symlink). The portable agent skill can be invoked as track-working-groups in a compatible harness; installing it does not automatically register a global shell alias.

## Commands

| Command | Behavior |
| --- | --- |
| wg or wg update | Refresh active groups and save a briefing |
| wg update identity-trust --since 30d | Check one group over a wider GitHub activity window, plus its meetings |
| wg meetings | Fetch public AAIF meeting times without checking GitHub |
| wg meetings identity-trust --days 30 | Show this group's public meetings up to 30 days ahead |
| wg update --days 30 | Normal refresh with 30-day meeting lookahead (default 14, maximum 90) |
| wg update --no-calendar | Explicitly skip public calendar checks |
| wg list | Show every group, including paused and archived |
| wg status | Show last successful checks and failed sources |
| wg links [GROUP] | List GitHub and calendar links |
| wg add --name "New Group" --github https://github.com/org/repo | Add group with next WG ID |
| wg edit WG-0002 --priority low --membership observer | Change metadata, preserve IDs |
| wg pause WG-0005 / wg resume WG-0005 | Pause or resume tracking |
| wg remove WG-0005 --yes | Archive group, never delete notes |
| wg reset WG-0002 --yes | Reset that group's checkpoints only |
| wg prep WG-0001 | Recent activity, meeting notes, three learning questions |
| wg notes WG-0001 --file notes.md --key meeting-2026-11-04 | Import a named note with stable DOC ID |
| wg meeting add WG-0001 --when 2026-11-10T09:00:00-08:00 --title "WG meeting" | Save verified upcoming meeting |
| wg meeting list | List saved meetings; removal requires --yes |
| wg validate | Validate local registry and state |

To set storage, use WG_DATA_DIR or put --data-dir /private/folder *before* the subcommand. Importing a different document under an existing note key requires --replace.

## Private persistence

The first invocation automatically creates user-owned files **outside** the canonical DotSkills repository:

~~~text
~/.dotskills/working-groups/
  groups.json
  state.json
  notes/
    WG-0001/DOC-<stable-hash>.md
  reports/
    latest.md
    latest.json
    <timestamp>.md
    <timestamp>.json
~~~

The included five AAIF GitHub repositories are a **starter tracking set, not proof of personal membership**. All start with membership_status = unconfirmed. To record actual membership, edit the group to observer, member, contributor, or left.

This is intentionally file-based: the data persists across CLI runs on the same device, but does not automatically sync across computers, Claude, Codex, or ChatGPT. Cross-harness identical state requires a common user-authorized shared directory. Do not commit private notes or checkpoints to the public DotSkills repository.

## What is checked

**The public AAIF calendar is now automatically ingested.** During `wg`, `wg update`, or `wg meetings`, the CLI fetches the [AAIF Working Groups calendar](https://aaif.io/working-groups/calendar) once and extracts event titles, identifiers, start/end times, group association, and canonical AAIF links from its public page data. Times display in Pacific time with daylight-saving handling. Meeting records get stable `MTG-` IDs as long as the source event identity remains the same. The lookahead is 14 days by default (1–90 days configurable). Meetings for groups you don't track, such as Governance, Risk & Regulatory Alignment, are displayed separately as **Other AAIF meetings**—never silently added to your group registry.

The CLI uses public GitHub GET requests to read issue, pull-request and commit metadata, including canonical URLs, title, status and timestamps. A changed item preserves its UPD ID, while its changed fingerprint causes it to reappear. A closed issue or merged PR is **not proof of a confirmed working-group governance decision**.

The AAIF page includes public meeting metadata, but can also include Zoom/LFX join credentials and recording details. **Only safe event fields are retained; no join tokens, recordings, transcripts, or raw HTML are written to state or reports.** Private LFX meeting materials and personal ICS feeds are not fetched. Verified meetings may still be added manually, and user-provided Markdown/plaintext notes imported. `wg prep GROUP` uses the last saved source-verified meeting dates, labeled by the calendar's check time. Meeting preparation asks:

1. What problem are they solving?
2. What are they producing?
3. How do they reach decisions?

There is no continuous background monitoring, authenticated LFX integration, private transcript access, or cloud synchronization in v1.1. Those are separate, permissioned extensions.

## Reliability and safety

- No third-party Python dependencies; registry, note, and unit-test operations need no network.
- GITHUB_TOKEN is optional for GitHub API rate limits; it is read from environment, never written to files or errors.
- GitHub checkpoints advance only after fetching complete issue, PR and commit collections. AAIF calendar checks have an independent source checkpoint. Failures, incomplete data and pagination overflow are reported as **unavailable**, rather than as "no meetings" or "no activity".
- Private local files use POSIX locks and atomic writes. Each report is persisted before checkpoints, reducing lost updates on failures.
- GitHub titles, public calendar data and imported notes are untrusted data, never instructions. The calendar parser reads page-data JSON without executing JavaScript, strips sensitive join metadata, and never writes the raw page to disk. No GitHub writes or downloaded-code execution.
- Offline unit tests use synthetic AAIF event payloads and mock GitHub calls. The public calendar adapter was also smoke-tested against the live AAIF site on November 5, 2026, including the three meetings in Identity & Trust, Governance and Observability. Website changes and LLM-summary quality still require separate verification.

See [Deterministic Execution Contract v1](references/deterministic-execution-contract-v1.md), [starter groups](config/starter-groups.json), and the [official AAIF calendar](https://aaif.io/working-groups/calendar).

## Tests

~~~bash
python3 -m unittest discover -s skills/track-working-groups/evals -p "test_*.py" -v
python3 scripts/validate_skill_repository_integrity.py
python3 scripts/validate_evals.py --all
~~~

Evaluator-only test files are not distributed by normal DotSkills adapters.
