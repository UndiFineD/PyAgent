#!/usr/bin/env python3
"""Fix import lines that were accidentally moved to column 0 but belong inside an indented block.

This is conservative: it only indents a top-level import line when the previous
non-empty non-comment line is indented (>=4 spaces) and the import is at column 0.
"""
from pathlib import Path
import re
import argparse

EXCLUDE_DIRS = {".venv", "venv", "dist", "build", "target", "__pycache__", ".git"}


def iter_py_files(root: Path):
    for p in root.rglob('*.py'):
        parts = set(p.parts)
        if parts & EXCLUDE_DIRS:
            continue
        yield p


def fix_file(path: Path, apply: bool) -> bool:
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return False
    lines = text.splitlines(keepends=True)
    changed = False
    for i, line in enumerate(lines):
        if re.match(r'^(from|import)\b', line):
            # find previous non-empty non-comment line
            prev = None
            for j in range(i-1, -1, -1):
                if lines[j].strip() and not lines[j].lstrip().startswith('#'):
                    prev = lines[j]
                    break
            if prev is None:
                continue
            prev_indent = len(prev) - len(prev.lstrip(' '))
            cur_indent = len(line) - len(line.lstrip(' '))
            if prev_indent >= 4 and cur_indent == 0:
                lines[i] = ' ' * prev_indent + line
                changed = True
    if changed and apply:
        bak = path.with_suffix(path.suffix + '.bak')
        if not bak.exists():
            bak.write_text(text, encoding='utf-8')
        path.write_text(''.join(lines), encoding='utf-8')
    return changed


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', '-r', default='.', help='root')
    p.add_argument('--apply', action='store_true')
    args = p.parse_args()
    root = Path(args.root)
    changed = 0
    for f in iter_py_files(root):
        ok = fix_file(f, args.apply)
        if ok:
            print('Fixed:', f)
            changed += 1
    print('Processed', changed, 'files')


if __name__ == '__main__':
    main()
