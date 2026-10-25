#!/usr/bin/env python3
"""Prepare one manual review workspace without evaluator answers or other cases."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

SUITE = Path(__file__).resolve().parent
ROOT = SUITE.parents[2]
SKILL_PATH = "skills/code-review/"
REVISIONS = {
    "before": "c6565141c5a5923235f80dd16a7ac680d58a1968",
    "after": "14abcdb4afe95c53a26522ab043fe1c0fc507421",
}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], stderr=subprocess.PIPE)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=["case-01", "case-02"], required=True)
    parser.add_argument("--skill", choices=REVISIONS, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() or output.is_relative_to(ROOT):
        parser.error("--output must be a new directory outside the DotSkills checkout")

    revision = REVISIONS[args.skill]
    try:
        paths = git("ls-tree", "-r", "--name-only", revision, "--", SKILL_PATH).decode().splitlines()
        if SKILL_PATH + "SKILL.md" not in paths:
            parser.error("the selected revision does not contain the code-review skill")
        skill_files = {p.removeprefix(SKILL_PATH): git("show", revision + ":" + p) for p in paths}
        eval_commit = git("rev-parse", "HEAD").decode().strip()
        eval_dirty = bool(git("status", "--porcelain", "--", str(SUITE.relative_to(ROOT))))
    except (OSError, subprocess.CalledProcessError):
        parser.error("cannot read the pinned skill snapshot; use a full Git checkout and run git fetch origin")

    fixture = SUITE / "fixtures" / args.case
    fixture_files = sorted(fixture.iterdir())
    hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in fixture_files}
    fixture_digest = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()

    output.mkdir(parents=True)
    shutil.copytree(fixture, output / "project")
    for relative, data in skill_files.items():
        destination = output / "skill" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    prompt = (SUITE / "prompt.md").read_text(encoding="utf-8")
    (output / "task.md").write_text(prompt.replace("{{WORKSPACE}}", str(output)), encoding="utf-8")

    # Save this metadata with the evaluator's notes, outside the reviewer workspace.
    print(json.dumps({
        "case": args.case,
        "skill": args.skill,
        "skill_revision": revision,
        "eval_source_commit": eval_commit,
        "eval_source_has_uncommitted_changes": eval_dirty,
        "fixture_sha256": fixture_digest,
        "task_file": str(output / "task.md"),
    }, indent=2))


if __name__ == "__main__":
    main()
