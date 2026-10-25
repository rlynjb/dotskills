#!/usr/bin/env python3
"""Record local source inspection and verification commands for a review."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    commands = parser.add_subparsers(dest="operation", required=True)
    listing = commands.add_parser("list")
    listing.add_argument("path", nargs="?", default=".")
    reading = commands.add_parser("read")
    reading.add_argument("path")
    reading.add_argument("--start", type=int, default=1)
    reading.add_argument("--end", type=int)
    searching = commands.add_parser("search")
    searching.add_argument("pattern")
    searching.add_argument("paths", nargs="*", default=["."])
    running = commands.add_parser("run")
    running.add_argument("--cwd", default=".")
    running.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    root = args.root.resolve()
    log = args.log.resolve()
    if log.is_relative_to(root):
        parser.error("the recording must be outside the review input directory")

    def scoped(value: str) -> Path:
        path = (root / value).resolve()
        if not path.is_relative_to(root):
            raise ValueError("path is outside the assigned review workspace")
        return path

    event = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "operation": args.operation,
        "request": {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()
                    if k not in {"log"}},
        "stdout": "", "stderr": "", "exit_code": 0,
    }
    started = time.monotonic()
    try:
        if args.operation == "list":
            folder = scoped(args.path)
            event["stdout"] = "\n".join(
                str(p.relative_to(root)) for p in sorted(folder.rglob("*"))
                if p.is_file() and p.resolve().is_relative_to(root)
            ) + "\n"
        elif args.operation == "read":
            path = scoped(args.path)
            data = path.read_bytes()
            lines = data.decode("utf-8").splitlines()
            start, end = max(1, args.start), args.end or len(lines)
            event["source_sha256"] = hashlib.sha256(data).hexdigest()
            event["returned_line_range"] = [start, min(end, len(lines))]
            event["stdout"] = str(path.relative_to(root)) + "\n" + "\n".join(
                f"{i}: {line}" for i, line in enumerate(lines, 1) if start <= i <= end
            ) + "\n"
        else:
            if args.operation == "search":
                paths = [str(scoped(p)) for p in args.paths]
                argv, cwd = ["rg", "-n", "--", args.pattern, *paths], root
            else:
                argv = args.command
                if argv and argv[0] == "--":
                    argv = argv[1:]
                if not argv:
                    raise ValueError("run requires a command after --")
                cwd = scoped(args.cwd)
            event["executed_argv"] = argv
            completed = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=45)
            event.update(stdout=completed.stdout, stderr=completed.stderr, exit_code=completed.returncode)
    except Exception as exc:
        event.update(stderr=f"{type(exc).__name__}: {exc}\n", exit_code=2)
    event["duration_seconds"] = round(time.monotonic() - started, 6)
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(event, ensure_ascii=False) + "\n")
    sys.stdout.write(event["stdout"])
    sys.stderr.write(event["stderr"])
    raise SystemExit(event["exit_code"])


if __name__ == "__main__":
    main()
