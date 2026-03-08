#!/usr/bin/env python3
"""Fix imports that were dedented out of indented blocks like try/except.

Usage:
  python scripts/fix_unindented_block_imports.py --apply

This is conservative: it only indents import/from lines that immediately follow
an indented control-flow line (try/except/else/finally) and whose current
indentation is less than the control-flow indent.
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
    i = 0
    while i < len(lines) - 1:
        m = re.match(r'^(\s*)(try:|except\b.*:|finally:|else:)\s*$', lines[i])
        if m:
            block_indent = m.group(1) + '    '
            j = i + 1
            # allow intervening comment or pylint directive lines
            while j < len(lines):
                if not lines[j].strip():
                    # blank line — stop (imports should be immediate)
                    break
                if lines[j].lstrip().startswith('#'):
                    j += 1
                    continue
                # if it's an import or from line
                m_imp = re.match(r"^(\s*)(from|import)\b", lines[j])
                if m_imp:
                    cur_indent = m_imp.group(1)
                    if len(cur_indent) < len(block_indent):
                        # re-indent this line and any subsequent continuation lines
                        # (lines that end with backslash or are indented as continuation)
                        k = j
                        while k < len(lines):
                            # continuation lines: those that start with whitespace and
                            # are part of the import block (we stop at blank/comment/non-indented)
                            if k == j:
                                # first line
                                rest = lines[k].lstrip()
                                lines[k] = block_indent + rest
                            else:
                                # continuation line: ensure it's indented at least one level more than block
                                if lines[k].strip() == '':
                                    break
                                if lines[k].lstrip().startswith('#'):
                                    lines[k] = block_indent + '    ' + lines[k].lstrip()
                                    k += 1
                                    continue
                                # if it looks like a continuation (starts with whitespace)
                                if re.match(r'^\s+', lines[k]):
                                    lines[k] = block_indent + '    ' + lines[k].lstrip()
                                    k += 1
                                    # continue if previous line ended with backslash
                                    if not lines[k-1].rstrip().endswith('\\'):
                                        break
                                    continue
                                break
                            k += 1
                        changed = True
                    break
                break
        i += 1
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
