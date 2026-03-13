#!/usr/bin/env python3
"""Fix unterminated triple-quoted strings in a Python codebase.

This script is intended to help with legacy code (e.g., src-old/) that has
been auto-generated or bulk-edited in a way that left docstrings with an odd
number of triple-quote delimiters. Python will raise "unterminated triple-quoted
string literal" syntax errors in those files.

This tool attempts the following fixes:
  - Normalize any line that is *only* `r\"\"\"` or `r\'\'\'` to `\"\"\"` / `\'\'\'`.
  - If a file has an odd number of `\"\"\"` or `\'\'\'` occurrences, append a
    matching closing delimiter at the end of the file.
  - Remove duplicate consecutive closing delimiters at the end of a file.

Usage:
  python scripts/fix_triple_quotes.py [--root src-old] [--dry-run]

The script prints a summary of files updated.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

TRIPLE_QUOTE_PATTERNS = [r'"""', r"'''"]


def normalize_raw_docstring_markers(text: str) -> str:
    """Normalize malformed raw docstring markers like `r\"\"\"` to `\"\"\"`."""
    # Only fix lines that consist solely of an r""" or r''' marker, possibly
    # preceded by whitespace.
    # We capture the delimiter (""" or '''), and replace the whole line with it.
    text = re.sub(r'(?m)^[ \t]*r(?P<q>"""|\'\'\')\s*$', r"\g<q>", text)
    return text


def ensure_balanced_triple_quotes(text: str) -> tuple[str, int]:
    """Ensure the file has balanced triple-quote delimiters.

    Returns:
        (fixed_text, num_fixes)
    """

    fixed = 0

    # Normalize raw markers first.
    new_text = normalize_raw_docstring_markers(text)
    if new_text != text:
        fixed += 1
        text = new_text

    # Convert module-level docstrings that contain backslash escape sequences into raw
    # docstrings to prevent unicodeescape and invalid escape errors.
    def rawify_if_escapes(txt: str) -> tuple[str, int]:
        changes = 0
        for delim in ('"""', "'''"):
            # Find the first occurrence of an unraw docstring opening delimiter.
            m = re.search(rf'(?m)(?<![rR]){re.escape(delim)}', txt)
            if not m:
                continue
            start = m.end()
            end = txt.find(delim, start)
            if end == -1:
                continue
            inner = txt[start:end]
            if '\\' in inner:
                txt = txt[:m.start()] + 'r' + txt[m.start():]
                changes += 1
        return txt, changes

    new_text, rawify_changes = rawify_if_escapes(text)
    if rawify_changes:
        fixed += rawify_changes
        text = new_text

    # Strip trailing whitespace lines, keep a snapshot for later comparison.
    lines = text.splitlines()
    while lines and lines[-1].strip() == "":
        lines.pop()

    # Collapse repeated closing delimiters at end of file.
    while len(lines) >= 2 and lines[-1].strip() in ('"""', "'''") and lines[-2].strip() == lines[-1].strip():
        lines.pop()
        fixed += 1

    # Add closing delimiter when counts are odd.
    for delim in ('"""', "'''"):
        count = '\n'.join(lines).count(delim)
        if count % 2 != 0:
            # Append at end using the indentation of the last non-empty line
            indent = ''
            if lines:
                last = lines[-1]
                indent = last[: len(last) - len(last.lstrip(' \t'))]
            lines.append(f"{indent}{delim}")
            fixed += 1

    fixed_text = "\n".join(lines) + "\n"
    return fixed_text, fixed


def process_file(path: pathlib.Path, dry_run: bool) -> int:
    """Process a single Python file and fix triple-quote issues.

    Returns the number of edits applied.
    """

    text = path.read_text(encoding='utf-8', errors='ignore')
    fixed_text, fixes = ensure_balanced_triple_quotes(text)
    if fixes and not dry_run:
        path.write_text(fixed_text, encoding='utf-8')
    return fixes


def main(argv: list[str] | None = None) -> int:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Fix unterminated triple-quoted strings in Python source files."
    )
    parser.add_argument(
        "--root",
        default="src-old",
        help="Root directory to scan (default: src-old).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be changed without writing files.",
    )
    args = parser.parse_args(argv)

    root = pathlib.Path(args.root)
    if not root.exists():
        print(f"Error: root path does not exist: {root}", file=sys.stderr)
        return 2

    total_files = 0
    total_fixes = 0
    updated_files: list[tuple[pathlib.Path, int]] = []

    for path in sorted(root.rglob("*.py")):
        total_files += 1
        fixes = process_file(path, dry_run=args.dry_run)
        if fixes:
            updated_files.append((path, fixes))
            total_fixes += fixes

    print(f"Scanned {total_files} Python files under {root}")
    print(f"Applied {total_fixes} fixes across {len(updated_files)} files")
    if args.dry_run and updated_files:
        print("Files that would be modified:")
        for path, fixes in updated_files[:50]:
            print(f"  {path} (fixes: {fixes})")
        if len(updated_files) > 50:
            print(f"  ...and {len(updated_files)-50} more")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
