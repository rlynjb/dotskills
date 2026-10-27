# Claude Code adapter

Use canonical DotSkills packages in the **Claude Code CLI** through project-local
installation or a skills-only plugin. Python 3.10+ is required for the adapter;
Claude Code must be installed and signed in to use the resulting skills.
No compilation or rewriting of `SKILL.md` is involved.

## Table of contents

- [Install into a project](#install-into-a-project)
- [Build and load a plugin](#build-and-load-a-plugin)
- [Selection and updates](#selection-and-updates)
- [Validation and boundaries](#validation-and-boundaries)

## Install into a project

From the DotSkills repository, preview and then install into an existing project:

```bash
python3 adapters/claude/install_claude.py --target ../my-project --dry-run
python3 adapters/claude/install_claude.py --target ../my-project
```

This copies the six methodology skills, including `refine-skill`, into
`../my-project/.claude/skills/<name>/`, with their complete supporting files.
Start `claude` from that project and invoke `/refine-skill`. Confirm that the
skill appears in the command menu; managed policies can restrict loading.

The default target is the current directory. Copy mode preserves source bytes;
it does not keep copies synchronized automatically. To update, rerun with
`--force`, which replaces only the selected skill directories. Other installed
skills and Claude settings are left alone. Remove an installed skill by deleting
its copied directory under the target project's `.claude/skills/`.

## Build and load a plugin

```bash
python3 adapters/claude/build_plugin.py --zip
claude plugin validate ./dist/claude/dotskills-methodology
claude --plugin-dir ./dist/claude/dotskills-methodology
```

The generated folder contains `.claude-plugin/plugin.json` and
`skills/<name>/SKILL.md` with each skill's full directory. An optional ZIP is
written beside it, with the manifest and skills at the archive root.
In that Claude session, invoke `/dotskills-methodology:refine-skill`.
`--plugin-dir` loads the plugin for that session; it is not a marketplace install.
Use an absolute plugin path when launching Claude from another project.
Choose one installation path to avoid loading duplicate copies of these skills.

The build defaults to `dist/claude/<name>/`. Customize it with `--name`,
`--version MAJOR.MINOR.PATCH`, `--description`, and `--output`. Existing output
requires `--force`; review the output path because its directory is replaced.
`--dry-run` previews without writing.

## Selection and updates

Both commands support the same mutually exclusive selectors:

```bash
# One or more skills (repeat --skill)
python3 adapters/claude/install_claude.py --target ../my-project --skill refine-feature-requirements

# A category
python3 adapters/claude/build_plugin.py --category engineering --name dotskills-engineering

# All exposed skills
python3 adapters/claude/build_plugin.py --all --name dotskills-all
```

Without a selector, the `methodology` category is used. Catalog entries marked
`exposed: false` are excluded from categories and `--all`; explicitly selecting
one fails. Selection does not infer dependencies: install the methodology family
when you need Refine Skill's specialist routing. Unknown names and empty
categories fail before files are written. Symlinked package contents and output
paths are rejected to avoid copying or replacing unexpected locations.

Change behavior in canonical `skills/`, validate/evaluate it, then reinstall or
rebuild. Generated `dist/` output is ignored by Git. No skill source, catalog
entry, OpenAI adapter, or imported source hash is modified by this adapter.

## Validation and boundaries

```bash
python3 scripts/validate_skill_repository_integrity.py
python3 -m unittest discover -s adapters/claude -p 'test_*.py' -v
```

Automated tests exercise copying, selection, hidden-skill exclusion, conflicts,
path protection, plugin layout, and ZIP contents. They do not establish model
behavior or that Claude follows approval gates. Run the native validation and a
representative skill task in your installed Claude Code version before relying
on it. The implementation environment did not have the Claude CLI, so native
plugin validation and live behavioral evaluation were not run there.

This adapter does not install Claude Code, change permissions, configure MCP
servers, publish a marketplace, or install into claude.ai/Cowork. Permissions and
runtime enforcement remain with the host. Project skill copies are not a sandbox.

Official format references (checked 2026-10-26):

- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Create and test plugins](https://code.claude.com/docs/en/plugins/create)
- [Plugin manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference)
