#!/usr/bin/env python3
"""Check DotSkills package structure and imported-reference consistency.

Run from the repository root:
    python3 scripts/validate_skills.py

Uses only the Python standard library and locates the repository relative to
this script. The same command can run locally or in GitHub Actions.

Checks:
- Each skill folder has SKILL.md with name and description frontmatter.
- Skill names match their folders and satisfy naming/length rules.
- Catalog entries match the skill folders, without duplicate names.
- references/ links in SKILL.md point to existing files inside that skill.
- Source-lock entries have a recorded source commit and unique destinations
  pointing to existing files within skills/.
- Imported file contents match the Git blob hashes recorded in source-lock.json.
- Catalog reference counts match the locked imports for each skill.

Reports detected problems as ERROR lines and exits with status 1. On success,
prints PASS with package/reference counts and exits with status 0.

Limits:
This is a structural and consistency check, not a prompt-injection or malware
scanner. It does not execute skills, run behavioral evals, judge instruction
quality, or enforce runtime permissions. Hash matches establish agreement with
the local lock file; they do not prove that the source is safe or independently
verify its contents against the upstream commit.

See docs/security.md (relative to the repository root) for security guidance,
planned review and evaluation improvements, and runtime safeguards.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES: list[str] = []


def fail(message: str) -> None:
    FAILURES.append(message)


def read_json(filename: str) -> dict:
    try:
        obj = json.loads((ROOT / filename).read_text(encoding="utf-8"))
        if not isinstance(obj, dict):
            raise ValueError("top-level JSON must be an object")
        return obj
    except (OSError, ValueError) as exc:
        fail(f"{filename}: {exc}")
        return {}


catalog = read_json("catalog.json")
lock = read_json("source-lock.json")
skills_root = ROOT / "skills"
skill_dirs = sorted(p for p in skills_root.iterdir() if p.is_dir()) if skills_root.is_dir() else []
if not skill_dirs:
    fail("skills/: no skill directories found")

catalog_names: set[str] = set()
for item in catalog.get("skills", []):
    name = item.get("name", "")
    path = item.get("path", "")
    if name in catalog_names:
        fail(f"catalog.json: duplicate name {name}")
    catalog_names.add(name)
    if path != f"skills/{name}" or not (ROOT / path / "SKILL.md").is_file():
        fail(f"catalog.json: invalid or missing entrypoint for {name}: {path}")

names: set[str] = set()
name_pattern = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
for folder in skill_dirs:
    names.add(folder.name)
    skill_file = folder / "SKILL.md"
    if not skill_file.is_file():
        fail(f"{folder.relative_to(ROOT)}: SKILL.md missing")
        continue
    content = skill_file.read_text(encoding="utf-8")
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(f"{skill_file.relative_to(ROOT)}: frontmatter missing")
        continue
    try:
        closing = lines.index("---", 1)
    except ValueError:
        fail(f"{skill_file.relative_to(ROOT)}: frontmatter not terminated")
        continue
    metadata = "\n".join(lines[1:closing])
    scalars = dict(re.findall(r"^(name|description):[ \t]*(.+)$", metadata, re.MULTILINE))
    name = scalars.get("name", "").strip().strip("'\"")
    desc = scalars.get("description", "").strip().strip("'\"")
    if len(name) > 64 or not name_pattern.fullmatch(name) or name != folder.name:
        fail(f"{skill_file.relative_to(ROOT)}: invalid or mismatched name: {name!r}")
    if not desc or len(desc) > 1024:
        fail(f"{skill_file.relative_to(ROOT)}: description must be 1–1024 characters")
    for relative in re.findall(r"\]\((references/[^)\s#]+)", content):
        target = (folder / relative).resolve()
        if not target.is_relative_to(folder.resolve()) or not target.is_file():
            fail(f"{skill_file.relative_to(ROOT)}: invalid or missing reference: {relative}")

if catalog_names != names:
    fail(f"Catalog/skill mismatch: not listed={sorted(names-catalog_names)}, stale={sorted(catalog_names-names)}")

locked_paths: set[str] = set()
imports_per_skill = {name: 0 for name in names}
for entry in lock.get("files", []):
    dst = entry.get("destination", "")
    source = entry.get("source", "")
    if dst in locked_paths:
        fail(f"source-lock.json: duplicate destination {dst}")
    locked_paths.add(dst)
    origin = lock.get("sources", {}).get(source)
    if not origin or not origin.get("commit"):
        fail(f"source-lock.json: source missing immutable commit: {dst}")
    resolved = (ROOT / dst).resolve()
    if not resolved.is_relative_to(skills_root.resolve()) or not resolved.is_file():
        fail(f"source-lock.json: missing or unsafe reference {dst}")
        continue
    data = resolved.read_bytes()
    calculated = hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()
    if calculated != entry.get("blob_sha"):
        fail(f"{dst}: source Git blob SHA mismatch")
    pieces = Path(dst).parts
    if len(pieces) >= 4 and pieces[0] == "skills" and pieces[2] == "references" and pieces[1] in imports_per_skill:
        imports_per_skill[pieces[1]] += 1

for item in catalog.get("skills", []):
    name = item.get("name", "")
    if item.get("reference_count") != imports_per_skill.get(name):
        fail(f"catalog.json: reference_count differs from locked imports for {name}")

if FAILURES:
    for issue in FAILURES:
        print("ERROR:", issue, file=sys.stderr)
    sys.exit(1)
print(f"PASS: {len(names)} skill packages and {len(locked_paths)} immutable source references verified")
