#!/usr/bin/env python3
"""Build a skills-only OpenAI portable plugin from canonical DotSkills packages.

Run from anywhere:
    python3 adapters/openai/build_plugin.py

By default this packages the `methodology` category. Use --skill repeatedly,
--category, or --all to choose a different set.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "catalog.json"
DEFAULT_OUTPUT = ROOT / "dist" / "openai" / "dotskills-methodology"


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
        selected = catalog
    elif names:
        by_name = {item.get("name"): item for item in catalog}
        missing = [name for name in names if name not in by_name]
        if missing:
            raise ValueError(f"Unknown skill(s): {', '.join(missing)}")
        selected = [by_name[name] for name in names]
    else:
        wanted = category or "methodology"
        selected = [item for item in catalog if item.get("category") == wanted]
        if not selected:
            raise ValueError(f"No skills found in category {wanted!r}")
    return selected


def copy_skill(item: dict, destination: Path) -> str:
    name = item.get("name")
    source_rel = item.get("path")
    if not isinstance(name, str) or not isinstance(source_rel, str):
        raise ValueError(f"Invalid catalog entry: {item!r}")
    source = (ROOT / source_rel).resolve()
    expected_root = (ROOT / "skills").resolve()
    if not source.is_relative_to(expected_root) or not (source / "SKILL.md").is_file():
        raise ValueError(f"Unsafe or invalid skill path for {name}: {source_rel}")
    shutil.copytree(source, destination / name)
    return name


def build_manifest(name: str, version: str, description: str) -> dict:
    display_name = "DotSkills Methodology" if name == "dotskills-methodology" else name
    return {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": name,
        "version": version,
        "description": description,
        "repository": "https://github.com/rlynjb/dotskills",
        "keywords": ["agent-skills", "evals", "methodology"],
        "extensions": {
            "com.openai": {
                "interface": {
                    "displayName": display_name,
                    "shortDescription": "Human-gated, evidence-driven skill refinement workflows.",
                    "longDescription": (
                        "Reusable DotSkills methodology for evaluating, diagnosing, "
                        "improving, and regression-testing agent skills."
                    ),
                    "developerName": "DotSkills",
                    "category": "Productivity",
                    "defaultPrompt": [
                        "Use refine-skill to improve this skill.",
                        "Start at the first human gate and use guided learning.",
                    ],
                }
            }
        },
    }


def zip_directory(source: Path) -> Path:
    archive = source.with_suffix(".zip")
    if archive.exists():
        archive.unlink()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(source))
    return archive


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build an OpenAI portable plugin from canonical DotSkills skill folders."
    )
    selector = parser.add_mutually_exclusive_group()
    selector.add_argument(
        "--category",
        default=None,
        help="Package all skills in this catalog category (default: methodology).",
    )
    selector.add_argument(
        "--all",
        action="store_true",
        help="Package every catalog skill.",
    )
    parser.add_argument(
        "--skill",
        action="append",
        default=[],
        help="Package a named skill. Repeat for multiple skills.",
    )
    parser.add_argument("--name", default="dotskills-methodology", help="Plugin package name.")
    parser.add_argument("--version", default="0.1.0", help="Plugin version.")
    parser.add_argument(
        "--description",
        default="Human-gated methodology and skill refinement tools from DotSkills.",
        help="Portable plugin description.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output directory (default: dist/openai/dotskills-methodology).",
    )
    parser.add_argument(
        "--zip",
        action="store_true",
        help="Also create a ZIP beside the output directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.skill and (args.category is not None or args.all):
        print("ERROR: use --skill by itself, or choose --category/--all", file=sys.stderr)
        return 2

    try:
        catalog = load_catalog()
        selected = select_skills(
            catalog,
            names=args.skill,
            category=args.category,
            all_skills=args.all,
        )

        output = args.output.expanduser().resolve()
        if output == ROOT.resolve() or ROOT.resolve().is_relative_to(output):
            raise ValueError(f"Refusing unsafe output path: {output}")
        if output.exists():
            shutil.rmtree(output)
        skills_out = output / "skills"
        skills_out.mkdir(parents=True)

        copied = [copy_skill(item, skills_out) for item in selected]
        manifest = build_manifest(args.name, args.version, args.description)
        (output / "plugin.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )

        print(f"Built OpenAI plugin: {output}")
        print(f"Packaged {len(copied)} skill(s): {', '.join(copied)}")
        if args.zip:
            archive = zip_directory(output)
            print(f"Created ZIP: {archive}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
