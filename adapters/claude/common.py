"""Shared selection and filesystem checks for the Claude Code adapter."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def add_selection(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--skill', action='append', default=[], help='Named skill; repeat for multiple.')
    group.add_argument('--category', help='Catalog category (default: methodology).')
    group.add_argument('--all', action='store_true', help='All exposed catalog skills.')


def select(args):
    catalog = json.loads((ROOT / 'catalog.json').read_text(encoding='utf-8'))['skills']
    by_name = {item['name']: item for item in catalog}
    if args.skill:
        unknown = set(args.skill) - by_name.keys()
        if unknown:
            raise ValueError(f'Unknown skills: {sorted(unknown)}')
        items = [by_name[name] for name in dict.fromkeys(args.skill)]
        hidden = [item['name'] for item in items if item.get('exposed') is False]
        if hidden:
            raise ValueError(f'Skills marked exposed=false cannot be packaged: {hidden}')
    else:
        items = [item for item in catalog if item.get('exposed') is not False
                 and (args.all or item.get('category') == (args.category or 'methodology'))]
    if not items:
        raise ValueError('No exposed skills match the selection')
    result = []
    for item in items:
        name = item['name']
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or name in {'synced', 'anthropic-skills'}:
            raise ValueError(f'Invalid or reserved skill name: {name}')
        source = ROOT / 'skills' / name
        if item['path'] != f'skills/{name}' or source.is_symlink() or not (source / 'SKILL.md').is_file():
            raise ValueError(f'Invalid skill source: {name}')
        # Reject links rather than accidentally distributing files outside a package.
        if any(p.is_symlink() for p in source.rglob('*')):
            raise ValueError(f'Skill contains symlinks; review before packaging: {name}')
        result.append((name, source))
    return result


def safe_destination(path):
    """Do not follow links or let an output overwrite canonical repository files."""
    path = path.expanduser().absolute()
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError(f'Destination contains a symlink: {path}')
    path = path.resolve()
    root = ROOT.resolve()
    allowed = (root / 'dist', root / '.claude' / 'skills')
    if path == root or root.is_relative_to(path):
        raise ValueError(f'Destination overlaps repository: {path}')
    if path.is_relative_to(root) and not any(path.is_relative_to(p) and path != p for p in allowed):
        raise ValueError(f'Use dist/ or .claude/skills/ for outputs inside DotSkills: {path}')
    return path


def check_existing(path, force):
    if path.exists() and not force:
        raise ValueError(f'{path} exists; use --force to replace it')
    if path.exists() and not path.is_dir():
        raise ValueError(f'Expected a directory: {path}')


def remove_existing(path):
    if path.exists():
        shutil.rmtree(path)
