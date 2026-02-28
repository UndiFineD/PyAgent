#!/usr/bin/env python3
"""Repo cleanup helper

Removes empty `try:\nexcept ImportError:` blocks and moves
`from __future__ import annotations` to the module top (after shebang
and module docstring). Use with --dry-run, --apply, --backup, --verbose.
"""
import argparse
import os
import re
import shutil
from pathlib import Path


def find_insert_index(lines):
    # Return index where future import should be inserted:
    # after shebang (line 0) and after closing module docstring if present
    i = 0
    if lines and lines[0].startswith("#!"):
        i = 1
    # skip initial blank lines
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    # if next token is a triple-quoted string, find its end
    if i < len(lines) and (lines[i].lstrip().startswith('"""') or lines[i].lstrip().startswith("'''")):
        quote = '"""' if lines[i].lstrip().startswith('"""') else "'''"
        # if the opening and closing are on same line, move past it
        if lines[i].strip().count(quote) >= 2:
            return i + 1
        j = i + 1
        while j < len(lines):
            if quote in lines[j]:
                return j + 1
            j += 1
        return i + 1
    return i


def file_process(path: Path, apply: bool, backup: bool, verbose: bool):
    text = path.read_text(encoding='utf-8')
    orig = text
    changed = False
    lines = text.splitlines(keepends=True)

    # 1) Move future import if present but not at top location
    fut = 'from __future__ import annotations'
    if fut in text:
        # find if it's already correctly placed: after shebang and/or docstring
        idx = find_insert_index(lines)
        # check if any occurrence exists before or at idx+2 lines
        prefix_text = ''.join(lines[: idx + 2])
        if fut not in prefix_text:
            # remove all occurrences
            text = text.replace(fut + '\n', '')
            lines = text.splitlines(keepends=True)
            insert_at = find_insert_index(lines)
            lines.insert(insert_at, fut + '\n')
            text = ''.join(lines)
            changed = True
            if verbose:
                print(f"Will move future-import in: {path}")

    # 2) Remove empty try/except ImportError blocks where try has no body
    # We'll scan lines for a 'try:' line followed shortly by 'except ImportError:'
    lines = text.splitlines(keepends=True)
    i = 0
    removals = 0
    while i < len(lines) - 1:
        if lines[i].strip().startswith('try:'):
            # find next non-empty line index
            j = i + 1
            # collect intervening lines
            intervening = []
            while j < len(lines) and lines[j].strip() == '':
                intervening.append(lines[j])
                j += 1
            if j < len(lines) and lines[j].strip().startswith('except ImportError'):
                # there was no indented block between try: and except -> remove both lines
                if verbose:
                    print(f"Removing empty try/except in {path} at lines {i+1}-{j+1}")
                # remove try line, intervening blanks, and except line
                del lines[i : j + 1]
                changed = True
                removals += 1
                # continue without increment (we removed current i)
                continue
        i += 1

    if removals and verbose:
        print(f"Removed {removals} empty try/except blocks from {path}")

    new_text = ''.join(lines)

    if new_text != orig:
        if apply:
            if backup:
                bkp = path.with_suffix(path.suffix + '.bak')
                shutil.copy2(path, bkp)
            path.write_text(new_text, encoding='utf-8')
            return 'applied'
        return 'would apply'
    return 'no change'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', default='src', help='Target directory')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--backup', action='store_true')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    root = Path(args.target)
    if not root.exists():
        print('Target not found:', root)
        return

    results = { 'applied': [], 'would apply': [], 'no change': [], 'errors': [] }
    for p in root.rglob('*.py'):
        # skip __pycache__ and hidden
        if any(part.startswith('.') for part in p.parts):
            continue
        try:
            res = file_process(p, args.apply, args.backup, args.verbose)
            results[res].append(str(p))
        except Exception as e:
            results['errors'].append((str(p), str(e)))
            if args.verbose:
                print('Error processing', p, e)

    print('\nSummary:')
    print('Applied:', len(results['applied']))
    print('Would apply:', len(results['would apply']))
    print('No change:', len(results['no change']))
    print('Errors:', len(results['errors']))
    if args.verbose and results['errors']:
        for e in results['errors']:
            print('ERR', e)

if __name__ == '__main__':
    main()
