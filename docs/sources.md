# Provenance and upstream ownership

The retained references use these pinned source commits:

| Source | Commit | Imported material |
| --- | --- | --- |
| [rlynjb/dotfiles](https://github.com/rlynjb/dotfiles/tree/master/reference) | `5a0e147ac81db92c1082dfb8ed4a6b629845b742` | 8 Markdown prompt/reference files |
| [rlynjb/buffr](https://github.com/rlynjb/buffr/tree/main) | `d7031090cc001632fd7d649076a2de5bc995b82c` | 10 versioned module documents plus M0–M7 runtime prompt snapshots |

For every imported Markdown file, `source-lock.json` records the source, source path, destination, and original Git blob hash. The validator checks byte-for-byte identity of each imported reference to the recorded source object.

## Canonical ownership

- **DotSkills is canonical for packaging/distribution.** The original material under `dotfiles/reference` remains source-attributed and may continue evolving independently until you adopt a sync or migration process.
- **Buffr remains canonical for execution.** Its TypeScript `src/agents/`, `src/contracts/`, and `src/workflow/` own the behavior. A copied prompt has no engine, data validation, tools, durable state, or approval gates.
- **Versioned Buffr prompt documents are design history.** They may differ from the runtime prompt snapshots, which may themselves be outdated relative to subsequent commits in Buffr.
- **No automatic sync is configured.** To update a reference, inspect upstream changes, update the file and locked hash deliberately, run checks and evals, and review the release.

Upstream text was preserved verbatim; some relative links within source documents may refer to adjacent files that are now packaged under another skill. Navigate via `catalog.json` or the upstream source repository rather than assuming those cross-skill links resolve in an isolated installation.

Upstream links to the combined `code-review.md` describe source material that
is no longer packaged here. Use [the code-review entrypoint](../skills/code-review/SKILL.md)
to select an individual book lens in DotSkills.

Upstream links to System Learning Implementation refer to the original prompt
library, which is no longer packaged here. Use [Learn Implementation](../skills/learn-implementation/SKILL.md)
for its extracted master prompt. The original source remains available in
[the pinned upstream file](https://github.com/rlynjb/dotfiles/blob/5a0e147ac81db92c1082dfb8ed4a6b629845b742/reference/system-learning-implementation.md).

Upstream links to System Learning Repo refer to the original onboarding library,
which is no longer packaged here. Use [Learn Repo](../skills/learn-repo/SKILL.md)
for the adapted master onboarding tutorial. The original source remains available
in [the pinned upstream file](https://github.com/rlynjb/dotfiles/blob/5a0e147ac81db92c1082dfb8ed4a6b629845b742/reference/system-learning-repo.md).
