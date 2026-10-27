#!/usr/bin/env python3
"""Install canonical DotSkills packages into a Codex-compatible repo-local path.

Example:
    python3 adapters/openai/install_codex.py --target ../my-project
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from runtime_copy import ignore_evaluator_material

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.json"


def load_catalog() -> list[dict]:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    skills = data.get("skills")
    if not isinstance(skills, list):
        raise ValueError("catalog.json: skills must be a list")
    return skills


def select_skills(
    catalog: list[dict], *, names: list[str], category: str | None, all_skills: bool
) -> list[dict]:
    if all_skills:
        return catalog
    if names:
        by_name = {item.get("name"): item for item in catalog}
        missing = [name for name in names if name not in by_name]
        if missing:
            raise ValueError(f"Unknown skill(s): {', '.join(missing)}")
        return [by_name[name] for name in names]
    wanted = category or "methodology"
    selected = [item for item in catalog if item.get("category") == wanted]
    if not selected:
        raise ValueError(f"No skills found in category {wanted!r}")
    return selected


def source_for(item: dict) -> Path:
    name = item.get("name")
    source_rel = item.get("path")
    if not isinstance(name, str) or not isinstance(source_rel, str):
        raise ValueError(f"Invalid catalog entry: {item!r}")
    source = (ROOT / source_rel).resolve()
    skills_root = (ROOT / "skills").resolve()
    if not source.is_relative_to(skills_root) or not (source / "SKILL.md").is_file():
        raise ValueError(f"Unsafe or invalid skill path for {name}: {source_rel}")
    return source


def install_one(
    source: Path,
    destination: Path,
    *,
    force: bool,
    link: bool,
    dry_run: bool,
) -> None:
    if destination.exists() or destination.is_symlink():
        if not force:
            raise ValueError(
                f"{destination} already exists; rerun with --force to replace it"
            )
        if not dry_run:
            if destination.is_dir() and not destination.is_symlink():
                shutil.rmtree(destination)
            else:
                destination.unlink()

    if link and (source / 'evals').exists():
        raise ValueError('Refusing --link: source contains evaluator-only evals/; use copy mode')

    if dry_run:
        action = "link" if link else "copy"
        print(f"DRY RUN: {action} {source} -> {destination}")
        return

    destination.parent.mkdir(parents=True, exist_ok=True)
    if link:
        destination.symlink_to(source, target_is_directory=True)
    else:
        shutil.copytree(source, destination,
                        ignore=ignore_evaluator_material(source))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install DotSkills into <target>/.agents/skills for Codex discovery."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="Target repository root (default: current directory).",
    )
    parser.add_argument(
        "--category",
        default=None,
        help="Install all skills in this catalog category (default: methodology).",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Install a named skill. Repeat for multiple skills.",
    )
    parser.add_argument("--all", action="store_true", help="Install every catalog skill.")
    parser.add_argument(
        "--link",
        action="store_true",
        help="Create symlinks to canonical skill folders instead of copying them.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing installed skill directories.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be installed without changing files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    selectors = int(bool(args.skill)) + int(args.category is not None) + int(args.all)
    if selectors > 1:
        print("ERROR: choose only one of --skill, --category, or --all", file=sys.stderr)
        return 2

    try:
        target = args.target.expanduser().resolve()
        if not target.exists() or not target.is_dir():
            raise ValueError(f"Target repository does not exist: {target}")

        catalog = load_catalog()
        selected = select_skills(
            catalog,
            names=args.skill,
            category=args.category,
            all_skills=args.all,
        )
        destination_root = target / ".agents" / "skills"

        installed: list[str] = []
        for item in selected:
            name = item["name"]
            source = source_for(item)
            install_one(
                source,
                destination_root / name,
                force=args.force,
                link=args.link,
                dry_run=args.dry_run,
            )
            installed.append(name)

        verb = "Would install" if args.dry_run else "Installed"
        print(f"{verb} {len(installed)} skill(s) into {destination_root}")
        print(", ".join(installed))
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
