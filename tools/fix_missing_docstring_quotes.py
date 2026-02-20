#!/usr/bin/env python3
"""Fix missing docstring delimiters that follow copyright headers.

Usage:
    python tools/fix_missing_docstring_quotes.py [--apply] [--limit N] [--root DIR] [--verbose]

This script looks for Python modules where a copyright/header block
is present, followed by an unquoted module description line (likely a
docstring missing its opening delimiters). It inserts an opening
docstring delimiter (three double quotes) before the candidate line and
a closing delimiter after the paragraph (or before the next import/def/class).
By default the script performs a dry-run and only prints candidates; use
``--apply`` to write changes and create ``.manual_fix.bak`` backups.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List, Tuple


def find_py_files(root: Path) -> List[Path]:
    return [p for p in root.rglob('*.py') if not p.name.endswith('.manual_fix.bak')]


def has_header(lines: List[str]) -> Tuple[bool, int]:
    # Return (has_header, index_of_line_after_header)
    header_end = 0
    for i, ln in enumerate(lines[:40]):
        if 'Copyright' in ln or 'Licensed under' in ln:
            # advance to end of contiguous comment block
            j = i
            while j + 1 < len(lines) and lines[j + 1].lstrip().startswith('#'):
                j += 1
            header_end = j + 1
            return True, header_end
    return False, 0


def is_candidate_line(ln: str) -> bool:
    s = ln.strip()
    if not s:
        return False
    if s.startswith(('#', 'import ', 'from ', 'def ', 'class ', '@')):
        return False
    if s[0] in ('"', "'"):
        return False
    # Heuristic: has letters and a space (sentence-like) or a period
    return any(c.isalpha() for c in s) and ('.' in s or ' ' in s)


def find_paragraph_end(lines: List[str], start: int) -> int:
    # Return index of line where paragraph ends (exclusive)
    for i in range(start, min(len(lines), start + 50)):
        s = lines[i].strip()
        if s == '':
            return i
        if s.startswith(('import ', 'from ', 'def ', 'class ', '@')):
            return i
    return min(len(lines), start + 1)


def already_has_triple_in_region(lines: List[str], start: int, end: int) -> bool:
    region = '\n'.join(lines[start:end])
    return '"""' in region or "'''" in region


def process_file(path: Path, apply: bool = False, verbose: bool = False) -> Tuple[bool, str]:
    text = path.read_text(encoding='utf-8', errors='surrogateescape')
    lines = text.splitlines(True)
    has_h, after = has_header(lines)
    if not has_h:
        return False, ''

    # Scan from after header for first candidate line
    for i in range(after, min(len(lines), after + 40)):
        if is_candidate_line(lines[i]):
            # ensure region doesn't already contain triple quotes
            end = find_paragraph_end(lines, i)
            if already_has_triple_in_region(lines, i, end):
                return False, ''

            # Prepare edit: insert opening triple quotes before i and closing before end
            new_lines = lines[:i]
            new_lines.append('"""\n')
            new_lines.extend(lines[i:end])
            new_lines.append('\n"""\n')
            new_lines.extend(lines[end:])
            new_text = ''.join(new_lines)
            if apply:
                bak = path.with_suffix(path.suffix + '.manual_fix.bak')
                bak.write_bytes(path.read_bytes())
                path.write_text(new_text, encoding='utf-8')
            if verbose:
                print(f"{path}: inserted docstring delimiters at lines {i+1}-{end}")
            return True, f'lines {i+1}-{end}'

    return False, ''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--root', type=str, default='src')
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()

    root = Path(args.root)
    files = find_py_files(root)
    processed = 0
    modified = 0
    for p in files:
        if args.limit and processed >= args.limit:
            break
        processed += 1
        try:
            changed, info = process_file(p, apply=args.apply, verbose=args.verbose)
        except Exception as exc:
            if args.verbose:
                print(f"ERROR {p}: {exc}")
            continue
        if changed:
            modified += 1

    print(f"Processed: {processed}; Modified: {modified}; apply={args.apply}")


if __name__ == '__main__':
    main()
