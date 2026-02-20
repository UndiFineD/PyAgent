#!/usr/bin/env python3
"""Normalize `from __future__ import annotations` placement.

This script finds Python files under a target directory (default: `src/`) where
`from __future__ import annotations` is either wrapped inside try/except or
not located at the module top (after optional shebang and module docstring).

Usage:
  python tools/fix_future_annotations.py --target src --dry-run
  python tools/fix_future_annotations.py --target src --apply --backup

Behavior:
- Detect and remove try/except wrappers around the future import.
- Remove duplicate/misplaced `from __future__ import annotations` lines.
- Insert a single `from __future__ import annotations` immediately after the
  module docstring (or after shebang/comments when no docstring exists).
- By default runs in dry-run mode and prints files that would change.
- Use `--apply` to overwrite files. Use `--backup` to write .bak backups.
"""

from __future__ import annotations

import argparse
import os
import re
from typing import List, Tuple

TRY_EXCEPT_PATTERN = re.compile(
    r"try:\s*\n"
    r"(?:[ \t]+)from __future__ import annotations\s*\n"
    r"(?:[ \t]+)except\s+ImportError:\s*\n"
    r"(?:[ \t]+)from __future__ import annotations\s*\n",
    re.M,
)

FUTURE_LINE_PATTERN = re.compile(r"^\s*from __future__ import annotations\s*$", re.M)

TRIPLE_QUOTE_START = re.compile(r"^\s*(?P<q>\'\'\'|\"\"\")")


def find_py_files(target: str) -> List[str]:
    files: List[str] = []
    for root, _, filenames in os.walk(target):
        for fn in filenames:
            if fn.endswith(".py"):
                files.append(os.path.join(root, fn))
    return files


def find_docstring_block(lines: List[str], start: int) -> Tuple[int, int]:
    """Return (doc_start_idx, doc_end_idx_exclusive). If no docstring, return (start,start).
    Handles single-line and multi-line triple-quoted docstrings."""
    if start >= len(lines):
        return start, start
    m = TRIPLE_QUOTE_START.match(lines[start])
    if not m:
        return start, start
    quote = m.group("q")
    # If closing on same line
    if lines[start].count(quote) >= 2:
        return start, start + 1
    # Search for closing line
    i = start + 1
    while i < len(lines):
        if quote in lines[i]:
            return start, i + 1
        i += 1
    # unterminated docstring: treat until EOF
    return start, len(lines)


def compute_insertion_index(lines: List[str]) -> int:
    """Determine index where future import should be inserted.
    After optional shebang (line 0) and after module docstring block.
    """
    idx = 0
    if lines and lines[0].startswith("#!"):
        idx = 1
    # skip leading comments and blank lines up to potential docstring
    j = idx
    while j < len(lines) and lines[j].strip().startswith("#"):
        j += 1
    # if docstring starts at j, place after docstring
    ds_start, ds_end = find_docstring_block(lines, j)
    if ds_end > ds_start:
        insertion = ds_end
    else:
        # otherwise place at j (after leading comments)
        insertion = j
    # ensure not inside indentation: move to first line break after insertion if insertion not at 0
    return insertion


def normalize_file_contents(text: str) -> Tuple[str, bool]:
    """Return (new_text, changed).
    Steps:
    - Remove try/except wrapper around future import.
    - Remove any remaining future import lines.
    - Insert a single future import at computed insertion point.
    """
    original = text
    # Normalize newlines to \n for processing, preserve later
    nl = "\n"
    text_n = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove try/except wrapper occurrences
    text_n = TRY_EXCEPT_PATTERN.sub("", text_n)

    # Remove any standalone future import lines
    text_n = FUTURE_LINE_PATTERN.sub("", text_n)

    # Split into lines to compute insertion position
    lines = text_n.split(nl)

    insertion = compute_insertion_index(lines)

    # Insert single future import if not already present at the insertion
    future_line = "from __future__ import annotations"
    # Avoid inserting if next non-blank line is already the future import (edge-case)
    k = insertion
    while k < len(lines) and lines[k].strip() == "":
        k += 1
    if k < len(lines) and lines[k].strip() == future_line:
        new_lines = lines
    else:
        # ensure a blank line after the import for readability
        new_lines = lines[:insertion] + [future_line, ""] + lines[insertion:]

    new_text = nl.join(new_lines)

    changed = new_text != original.replace("\r\n", "\n").replace("\r", "\n")
    # Restore original newline style if needed (we keep \n)
    return new_text, changed


def process_file(path: str, apply: bool = False, backup: bool = False) -> Tuple[bool, str]:
    """Return (changed, message)"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()
    except Exception as e:
        return False, f"ERROR reading: {e}"

    if "from __future__ import annotations" not in txt:
        return False, "no future import"

    new_txt, changed = normalize_file_contents(txt)
    if not changed:
        return False, "no change needed"

    if apply:
        if backup:
            bak = path + ".bak"
            try:
                with open(bak, "w", encoding="utf-8") as bf:
                    bf.write(txt)
            except Exception as e:
                return False, f"ERROR writing backup: {e}"
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_txt)
        except Exception as e:
            return False, f"ERROR writing file: {e}"
        return True, "applied"
    else:
        return True, "would apply"


def main() -> None:
    p = argparse.ArgumentParser(description="Normalize 'from __future__ import annotations' placement")
    p.add_argument("--target", default="src", help="Directory to target (default: src)")
    p.add_argument("--apply", action="store_true", help="Apply changes; default is dry-run")
    p.add_argument("--backup", action="store_true", help="Write .bak backups when applying")
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    args = p.parse_args()

    files = find_py_files(args.target)
    changed_files = []
    errors = []

    for fpath in sorted(files):
        changed, msg = process_file(fpath, apply=args.apply, backup=args.backup)
        if changed:
            changed_files.append((fpath, msg))
            if args.verbose:
                print(f"{fpath}: {msg}")
        else:
            if args.verbose:
                print(f"{fpath}: {msg}")
        if msg.startswith("ERROR"):
            errors.append((fpath, msg))

    print("\nSummary:")
    print(f"  scanned: {len(files)} files")
    print(f"  changed: {len(changed_files)} files")
    if errors:
        print(f"  errors: {len(errors)} files")
        for pth, em in errors:
            print(f"    {pth}: {em}")
    if changed_files and not args.apply:
        print("\nRun with --apply to write changes, and --backup to keep .bak copies.")


if __name__ == "__main__":
    main()
