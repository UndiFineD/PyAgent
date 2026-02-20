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


def collapse_duplicate_triple_lines(text: str) -> Tuple[str, bool]:
    """Collapse consecutive identical triple-quote-only lines.

    Handles corruption patterns where multiple triple-quote delimiters
    appear consecutively (e.g. four triple-quote lines surrounding a
    docstring), by collapsing runs of identical standalone triple-quote
    lines into a single delimiter. This preserves intended docstrings
    while removing redundant empty delimiters that break parsing.
    """
    lines = text.splitlines(True)
    out = []
    changed = False
    prev_strip = None
    for ln in lines:
        s = ln.strip()
        if s in ('"""', "'''") and prev_strip == s:
            # skip this duplicate triple-quote-only line
            changed = True
            continue
        out.append(ln)
        prev_strip = s if s in ('"""', "'''") else None
    return ''.join(out), changed


def normalize_docstring_blocks(text: str) -> Tuple[str, bool]:
    """Normalize docstring blocks: ensure a single opening and closing delimiter
    and clean stray quote characters around the content.

    This scans for standalone triple-quote delimiters and the matching
    closing delimiter, extracts the content, strips accidental leading/trailing
    quote characters, and rewrites the block as a clean multi-line docstring.
    """
    lines = text.splitlines(True)
    n = len(lines)
    i = 0
    out = []
    changed = False
    while i < n:
        ln = lines[i]
        stripped = ln.strip()
        if stripped in ('"""', "'''"):
            delim = stripped
            # find closing
            j = i + 1
            while j < n and delim not in lines[j]:
                j += 1
            if j >= n:
                # no closing found; leave as-is
                out.append(ln)
                i += 1
                continue
            # If the closing delimiter is immediately adjacent (empty block),
            # it's possible the file has duplicated triple-quote lines before
            # the real docstring content/closing. Look further ahead for a
            # non-empty content region followed by a closing delimiter and
            # prefer that as the closing boundary.
            if j == i + 1:
                k = j + 1
                while k < min(n, j + 200):
                    if delim in lines[k]:
                        # ensure there's non-empty content between j and k
                        mid_content = ''.join(lines[j+1:k]).strip()
                        if mid_content:
                            j = k
                            break
                    k += 1
            # Extract and clean content between i and j
            content = ''.join(lines[i+1:j])
            cleaned = content.strip()
            # Remove accidental leading/trailing quote characters
            cleaned = re.sub(r'^[\'\"]+', '', cleaned)
            cleaned = re.sub(r'[\'\"]+$', '', cleaned)
            # Reconstruct a clean docstring block
            out.append(delim + "\n")
            if cleaned:
                for cl in cleaned.splitlines():
                    out.append(cl.rstrip() + "\n")
            out.append(delim + "\n")
            changed = True
            i = j + 1
            continue
        out.append(ln)
        i += 1
    return ''.join(out), changed


def fix_method_indentation(text: str) -> Tuple[str, bool]:
    """Normalize indentation for method blocks inside classes.

    Conservative heuristic: when a `def` line appears indented (i.e. inside a
    class) but the following lines (docstring and body) are not indented to the
    expected method indent level, this function will indent those lines to be
    four spaces deeper than the `def` line. It stops at the next top-level
    `def`/`class` or an unindented line that signals the method block end.
    """
    lines = text.splitlines(True)
    n = len(lines)
    i = 0
    changed = False
    out = []
    while i < n:
        ln = lines[i]
        m = re.match(r"^(\s+)(def\s+[A-Za-z_][A-Za-z0-9_]*\s*\(.*\)\s*:\s*)$", ln)
        if m:
            base_indent = m.group(1)
            req = base_indent + " " * 4
            out.append(ln)
            i += 1
            # adjust subsequent lines until we hit a line that is at or
            # left of base_indent and looks like a new def/class or file-level
            # boundary.
            while i < n:
                nxt = lines[i]
                # if next line is blank, keep it (but indent if needed)
                if nxt.strip() == "":
                    out.append(nxt)
                    i += 1
                    continue
                # detect new block at same or lesser indent that looks like def/class
                leading = re.match(r"^(\s*)", nxt).group(1)
                if len(leading) <= len(base_indent) and re.match(r"^\s*(def |class )", nxt):
                    break
                # make sure the line is indented at least to req
                content = nxt.lstrip()
                new_ln = req + content
                if new_ln != nxt:
                    changed = True
                out.append(new_ln)
                i += 1
            continue
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

    t, ok = normalize_docstring_blocks(text)
    if ok:
        changes.append('normalize_docstring_blocks')
        text = t

    t, ok = collapse_duplicate_triple_lines(text)
    if ok:
        changes.append('collapse_duplicate_triple_lines')
        text = t

    t, ok = fix_method_indentation(text)
    if ok:
        changes.append('fix_method_indentation')
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
