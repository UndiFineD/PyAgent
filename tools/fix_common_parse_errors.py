#!/usr/bin/env python3
"""Conservative fixer for common parse-time corruption patterns.

Usage:
  python tools/fix_common_parse_errors.py [--apply] [--limit N] [--verbose]

This script performs non-destructive, minimal edits aimed at restoring
Python parseability for files that suffer from common issues found in
the project: misplaced `from __future__` imports, missing newlines after
closed triple-quotes, stray trailing quotes, and unbalanced triple-quotes.

It creates a backup next to each modified file with the suffix
`.manual_fix.bak`. By default the script runs in dry-run mode and only
prints planned changes; pass `--apply` to write changes.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Tuple


def find_py_files(root: Path):
    return [p for p in root.rglob("*.py") if not p.name.endswith('.manual_fix.bak')]


def move_future_imports(text: str) -> Tuple[str, bool]:
    futures = re.findall(r"^\s*from __future__ import [^\n]+", text, flags=re.M)
    if not futures:
        return text, False

    # Remove all occurrences
    new_text = re.sub(r"^\s*from __future__ import [^\n]+\n?", "", text, flags=re.M)

    # Build insertion point: after shebang and module docstring (if present)
    lines = new_text.splitlines(True)
    i = 0
    if lines and lines[0].startswith("#!"):
        i = 1

    # detect module docstring start
    if i < len(lines) and re.match(r"^\s*(?:[rubfRUBF]?)?([\'\"]{3})", lines[i]):
        delim = re.match(r"^\s*(?:[rubfRUBF]?)?([\'\"]{3})", lines[i]).group(1)
        # find closing delim
        for j in range(i + 1, len(lines)):
            if delim in lines[j]:
                i = j + 1
                break

    insert_text = "\n".join(dict.fromkeys(futures)) + "\n"
    lines.insert(i, insert_text)
    return "".join(lines), True


def fix_triple_quote_adjacent(text: str) -> Tuple[str, bool]:
    # Insert newline after closing triple-quote when followed immediately by an identifier
    new, n = re.subn(r"([\'\"]{3})(\s*)(?=[A-Za-z_])", r"\1\n", text)
    return new, n > 0


def remove_unmatched_trailing_quote(text: str) -> Tuple[str, bool]:
    changed = False
    out_lines = []
    for ln in text.splitlines(True):
        s = ln.rstrip('\n')
        # If line ends with a single or double quote and the count of that quote in the line is odd,
        # remove the trailing quote to avoid unterminated string literal on that line.
        if s.endswith('"') and s.count('"') % 2 == 1:
            s = s[:-1]
            changed = True
        elif s.endswith("'") and s.count("'") % 2 == 1:
            s = s[:-1]
            changed = True
        out_lines.append(s + ("\n" if ln.endswith('\n') else ""))
    return "".join(out_lines), changed


def remove_trailing_quote_after_paren(text: str) -> Tuple[str, bool]:
    # Fix patterns like TypeVar(... )'  -> remove stray trailing quote after closing paren
    new, n = re.subn(r"(\)\s*)'[ \t]*(?=\n|$)", r"\1", text)
    return new, n > 0


def balance_triple_quotes(text: str) -> Tuple[str, bool]:
    changed = False
    for q in ('"""', "'''"):
        cnt = text.count(q)
        if cnt % 2 == 1:
            text = text + "\n" + q + "\n"
            changed = True
    return text, changed


def fix_double_quote_docstring_pairs(text: str) -> Tuple[str, bool]:
    """Convert pairs of lines that contain only two double quotes into triple-quoted blocks.

    Detect a pattern where a line contains exactly two double-quote characters
    on its own, followed later by another such line. The region between them is
    treated as a docstring paragraph and the pair is replaced with proper
    triple-quote delimiters (three double-quote characters) surrounding that
    paragraph. The docstring here avoids embedding literal triple-quote
    examples to remain parser-safe.
    """
    lines = text.splitlines(True)
    changed = False
    i = 0
    out = []
    n = len(lines)
    while i < n:
        ln = lines[i]
        if ln.strip() == '""':
            # look ahead for a closing pair within a reasonable window
            j = i + 1
            while j < n and j <= i + 300:
                if lines[j].strip() == '""':
                    # replace opening and closing with triple quotes
                    out.append('"""' + ("\n" if not ln.endswith('\n') else "\n"))
                    # copy middle lines
                    out.extend(lines[i+1:j])
                    # closing
                    out.append('"""' + ("\n" if not lines[j].endswith('\n') else "\n"))
                    i = j + 1
                    changed = True
                    break
                j += 1
            else:
                # no closing found; keep the line as-is
                out.append(ln)
                i += 1
        else:
            out.append(ln)
            i += 1
    return ''.join(out), changed


def apply_heuristics(path: Path, text: str) -> Tuple[str, list[str]]:
    changes = []
    t, ok = move_future_imports(text)
    if ok:
        changes.append('move_future_imports')
        text = t

    t, ok = fix_triple_quote_adjacent(text)
    if ok:
        changes.append('fix_triple_quote_adjacent')
        text = t

    t, ok = remove_unmatched_trailing_quote(text)
    if ok:
        changes.append('remove_unmatched_trailing_quote')
        text = t

    t, ok = remove_trailing_quote_after_paren(text)
    if ok:
        changes.append('remove_trailing_quote_after_paren')
        text = t

    t, ok = balance_triple_quotes(text)
    if ok:
        changes.append('balance_triple_quotes')
        text = t

    t, ok = fix_double_quote_docstring_pairs(text)
    if ok:
        changes.append('fix_double_quote_docstring_pairs')
        text = t

    return text, changes


def process_file(path: Path, apply: bool = False, verbose: bool = False) -> Tuple[bool, list[str]]:
    text = path.read_text(encoding='utf-8', errors='surrogateescape')
    new_text, changes = apply_heuristics(path, text)
    if not changes:
        return False, []

    if apply:
        bak = path.with_suffix(path.suffix + '.manual_fix.bak')
        bak.write_bytes(path.read_bytes())
        path.write_text(new_text, encoding='utf-8')

    if verbose:
        print(f"{path}: {', '.join(changes)}")
    return True, changes


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='Write changes (default: dry-run)')
    parser.add_argument('--limit', type=int, default=0, help='Limit number of files processed (0=all)')
    parser.add_argument('--root', type=str, default='src', help='Root directory to scan')
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
            changed, changes = process_file(p, apply=args.apply, verbose=args.verbose)
        except Exception as exc:
            if args.verbose:
                print(f"ERROR processing {p}: {exc}")
            continue
        if changed:
            modified += 1

    print(f"Processed: {processed} files; Modified: {modified} files; apply={args.apply}")


if __name__ == '__main__':
    main()
