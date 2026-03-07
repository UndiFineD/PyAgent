#!/usr/bin/env python3

"""Fix lines that start with a single leading space or tab before 'from' or 'import'.
This is a conservative fixer: it only removes a single leading space or tab when the line
starts with exactly that and then 'from ' or 'import '. It writes files in-place.
"""
import pathlib

root = pathlib.Path(__file__).parent.parent
COUNT = 0
for p in root.rglob('src/**/*.py'):
    try:
        text = p.read_text(encoding='utf-8')
    except Exception:
        continue
    HAS_CHANGED = False
    lines = text.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if line.startswith(' from ') or line.startswith('\tfrom '):
            lines[i] = line[1:]
            HAS_CHANGED = True
        elif line.startswith(' import ') or line.startswith('\timport '):
            lines[i] = line[1:]
            HAS_CHANGED = True
    if HAS_CHANGED:
        p.write_text(''.join(lines), encoding='utf-8')
        COUNT += 1
print(f"Fixed leading-import lines in {COUNT} files.")
