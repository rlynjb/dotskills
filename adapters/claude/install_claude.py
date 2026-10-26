#!/usr/bin/env python3
"""Copy whole canonical skill packages into a project's .claude/skills directory."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from common import add_selection, check_existing, remove_existing, safe_destination, select


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, default=Path.cwd(), help='Existing project directory.')
    add_selection(parser)
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing.')
    parser.add_argument('--force', action='store_true', help='Replace selected installed directories.')
    args = parser.parse_args()
    try:
        target = args.target.expanduser().absolute()
        if not target.is_dir():
            raise ValueError(f'Target project does not exist: {target}')
        selected = select(args)
        # Preflight every destination before changing any installed package.
        plan = [(source, safe_destination(target / '.claude' / 'skills' / name))
                for name, source in selected]
        for _, destination in plan:
            check_existing(destination, args.force)
        for source, destination in plan:
            print(f'{"DRY RUN: " if args.dry_run else ""}Copy {source} -> {destination}')
            if not args.dry_run:
                destination.parent.mkdir(parents=True, exist_ok=True)
                remove_existing(destination)
                shutil.copytree(source, destination)
        print(f'{"Would install" if args.dry_run else "Installed"} {len(plan)} skill(s).')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
