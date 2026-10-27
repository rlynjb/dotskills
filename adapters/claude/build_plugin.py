#!/usr/bin/env python3
"""Build a Claude Code skills-only plugin; canonical instructions stay unchanged."""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from common import ROOT, add_selection, check_existing, ignore_evaluator_material, remove_existing, safe_destination, select


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    add_selection(parser)
    parser.add_argument('--name', default='dotskills-methodology')
    parser.add_argument('--version', default='0.1.0')
    parser.add_argument('--description', default='Reusable skills from the canonical DotSkills library.')
    parser.add_argument('--output', type=Path, help='Default: dist/claude/<name>.')
    parser.add_argument('--zip', action='store_true', help='Also create a ZIP beside the directory.')
    parser.add_argument('--force', action='store_true', help='Replace existing output and requested ZIP.')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.name):
            raise ValueError('Plugin name must use lowercase letters, digits, and hyphens')
        if not re.fullmatch(r'\d+\.\d+\.\d+', args.version):
            raise ValueError('Version must be MAJOR.MINOR.PATCH')
        selected = select(args)
        output = safe_destination(args.output or ROOT / 'dist' / 'claude' / args.name)
        check_existing(output, args.force)
        archive = safe_destination(output.with_name(output.name + '.zip'))
        if args.zip and archive.exists() and (not args.force or not archive.is_file()):
            raise ValueError(f'Archive exists (use --force for a regular file): {archive}')
        if args.dry_run:
            print(f'Would build {output} with: {", ".join(name for name, _ in selected)}')
            return 0
        output.parent.mkdir(parents=True, exist_ok=True)
        # Stage the full package before replacing a previous build.
        with tempfile.TemporaryDirectory(dir=output.parent, prefix='.dotskills-build-') as temp:
            staged = Path(temp) / 'plugin'
            (staged / '.claude-plugin').mkdir(parents=True)
            for name, source in selected:
                shutil.copytree(source, staged / 'skills' / name,
                                ignore=ignore_evaluator_material(source))
            manifest = {'name': args.name, 'version': args.version,
                        'description': args.description,
                        'repository': 'https://github.com/rlynjb/dotskills'}
            (staged / '.claude-plugin' / 'plugin.json').write_text(
                json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
            if args.zip:
                staged_zip = Path(temp) / 'plugin.zip'
                with zipfile.ZipFile(staged_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for file in sorted(staged.rglob('*')):
                        if file.is_file():
                            zf.write(file, file.relative_to(staged))
            remove_existing(output)
            staged.rename(output)
            if args.zip:
                staged_zip.replace(archive)
        print(f'Built {output} with {len(selected)} skill(s).')
        if args.zip:
            print(f'Created {archive}')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
