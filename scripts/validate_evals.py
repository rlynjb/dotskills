#!/usr/bin/env python3
"""Validate optional skill-local Agent Skills evaluation definitions.

Conventions: https://agentskills.io/skill-creation/evaluating-skills

Usage:
    python3 scripts/validate_evals.py --all
    python3 scripts/validate_evals.py skills/refine-skill/evals/evals.json

This checks JSON structure and referenced input files only. It does not run
models, grade output quality, enforce isolation, or certify safety.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def validate_suite(filename: Path) -> list[str]:
    """Return actionable validation errors for one skill-local evals.json."""
    errors: list[str] = []
    filename = filename.resolve()
    skill_dir = filename.parent.parent
    label = str(filename)

    if filename.name != "evals.json" or filename.parent.name != "evals":
        return [f"{label}: expected <skill>/evals/evals.json"]
    if not (skill_dir / "SKILL.md").is_file():
        errors.append(f"{label}: missing sibling skill SKILL.md")

    try:
        data = json.loads(filename.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return errors + [f"{label}: {exc}"]
    if not isinstance(data, dict):
        return errors + [f"{label}: top-level JSON must be an object"]
    if data.get("skill_name") != skill_dir.name:
        errors.append(
            f"{label}: skill_name must match package directory {skill_dir.name!r}"
        )
    cases = data.get("evals")
    if not isinstance(cases, list) or not cases:
        return errors + [f"{label}: evals must be a nonempty list"]

    seen: set[int] = set()
    for index, case in enumerate(cases, 1):
        prefix = f"{label}: evals[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{prefix}: case must be an object")
            continue
        case_id = case.get("id")
        if isinstance(case_id, bool) or not isinstance(case_id, int) or case_id < 1:
            errors.append(f"{prefix}: id must be a positive integer")
        elif case_id in seen:
            errors.append(f"{prefix}: duplicate id {case_id}")
        else:
            seen.add(case_id)
        for key in ("prompt", "expected_output"):
            value = case.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{prefix}: {key} must be a nonempty string")

        for key in ("files", "assertions"):
            if key not in case:
                continue
            value = case[key]
            if not isinstance(value, list):
                errors.append(f"{prefix}: {key} must be a list")
                continue
            for i, item in enumerate(value):
                if not isinstance(item, str) or not item.strip():
                    errors.append(f"{prefix}: {key}[{i}] must be a nonempty string")
                    continue
                if key != "files":
                    continue
                fixture = Path(item)
                if fixture.is_absolute() or ".." in fixture.parts:
                    errors.append(f"{prefix}: unsafe fixture path {item!r}")
                    continue
                resolved = (skill_dir / fixture).resolve()
                if not resolved.is_relative_to(skill_dir.resolve()):
                    errors.append(f"{prefix}: fixture escapes skill package: {item!r}")
                elif not resolved.is_file() or (skill_dir / fixture).is_symlink():
                    errors.append(f"{prefix}: missing or symlinked fixture: {item!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Skill-local evals.json files")
    parser.add_argument(
        "--all", action="store_true", help="Validate every skills/*/evals/evals.json"
    )
    args = parser.parse_args()
    if args.all and args.paths:
        parser.error("Choose --all or explicit file paths, not both")
    if not args.all and not args.paths:
        parser.error("Specify --all or one or more file paths")
    paths = sorted(SKILLS.glob("*/evals/evals.json")) if args.all else args.paths
    if not paths:
        print("PASS: no optional skill-local eval suites found")
        return 0
    issues = [err for path in paths for err in validate_suite(path)]
    if issues:
        for err in issues:
            print("ERROR:", err, file=sys.stderr)
        return 1
    print(f"PASS: {len(paths)} Agent Skills eval suite(s) structurally valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
