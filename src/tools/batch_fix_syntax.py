#!/usr/bin/env python3
"""Batch-fix common Python syntax corruption heuristics across a tree.

Creates a `.auto_fix.bak` backup for each modified file and logs actions.

Heuristics applied:
- Move `from __future__ import ...` lines to module top (after shebang/comment/docstring).
- Insert newline after a closing triple-quote when it is immediately followed by code 
  (for example, a closing triple-quote followed directly by an `if` token).
- Remove emoji / symbol characters that commonly break parsing.
- If a file has an odd number of triple-quotes, append a closing triple-quote.

Use with caution; each changed file is backed up before writing.
"""
from __future__ import annotations

import argparse
import io
import os
import re
import sys
import unicodedata
from typing import List


LOG_PATH = os.path.join(os.path.dirname(__file__), "batch_fix_syntax.log")


def is_emoji_or_symbol(ch: str) -> bool:
    # Remove characters categorized as 'Symbol, other' (So) or surrogates (Cs)
    cat = unicodedata.category(ch)
    return cat.startswith("So") or cat == "Cs"


def remove_emojis(text: str) -> str:
    if not text:
        return text
    return "".join(ch for ch in text if not is_emoji_or_symbol(ch))


def extract_future_imports(text: str) -> (List[str], str):
    pattern = re.compile(r"^from\s+__future__\s+import\s+.+$", flags=re.MULTILINE)
    found = pattern.findall(text)
    new_text = pattern.sub("", text)
    return found, new_text


def insert_future_imports_at_top(lines: List[str], future_lines: List[str]) -> List[str]:
    if not future_lines:
        return lines

    idx = 0
    n = len(lines)
    # Skip shebang
    if idx < n and lines[idx].startswith("#!"):
        idx += 1

    # Skip initial block of comment lines and blank lines
    while idx < n and (lines[idx].strip() == "" or lines[idx].lstrip().startswith("#")):
        idx += 1

    # If there's a module docstring, skip it
    if idx < n and (lines[idx].lstrip().startswith('"""') or lines[idx].lstrip().startswith("'''")):
        quote = lines[idx].lstrip()[:3]
        # find closing
        idx += 1
        while idx < n and quote not in lines[idx]:
            idx += 1
        if idx < n:
            idx += 1

    insert_at = idx
    for i, fl in enumerate(future_lines):
        lines.insert(insert_at + i, fl.rstrip() + "\n")
    return lines


def fix_triple_quote_followed_by_code(text: str) -> str:
    # Insert a newline after a closing triple-quote if immediate code token follows
    pattern = re.compile(r'"""(?=(if|for|return|def|class|import|from|\(|\[|\{|@))')
    text = pattern.sub('"""\n', text)
    pattern2 = re.compile(r"'''(?=(if|for|return|def|class|import|from|\(|\[|\{|@))")
    text = pattern2.sub("'''\n", text)
    return text


def ensure_even_triple_quotes(text: str) -> str:
    # If odd count of triple quotes, append a closing triple-quote at EOF
    for q in ('"""', "'''"):
        if text.count(q) % 2 == 1:
            text = text + "\n" + q + "\n"
    return text


def process_file(path: str, dry_run: bool = False) -> bool:
    """Process a single Python file. Returns True if modified."""
    try:
        with io.open(path, 'r', encoding='utf-8') as f:
            orig = f.read()
    except Exception:
        return False

    text = orig

    # 1) Extract and remove future imports
    future_lines, text = extract_future_imports(text)

    # 2) Remove emoji/symbol characters that often break parsing
    text = remove_emojis(text)

    # 3) Fix triple-quote followed immediately by code
    text = fix_triple_quote_followed_by_code(text)

    # 4) Ensure even triple-quote counts
    text = ensure_even_triple_quotes(text)

    # 5) If we removed future imports, re-insert them near top
    if future_lines:
        lines = text.splitlines(True)
        lines = insert_future_imports_at_top(lines, future_lines)
        text = ''.join(lines)

    if text != orig:
        if dry_run:
            return True

        bak = path + '.auto_fix.bak'
        if not os.path.exists(bak):
            try:
                with io.open(bak, 'w', encoding='utf-8') as bf:
                    bf.write(orig)
            except Exception:
                pass

        try:
            with io.open(path, 'w', encoding='utf-8') as f:
                f.write(text)
        except Exception:
            return False

        with io.open(LOG_PATH, 'a', encoding='utf-8') as log:
            log.write(f'MODIFIED: {path}\n')
        return True

    return False


def walk_and_fix(root: str, dry_run: bool = False) -> int:
    modified = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # skip common virtualenv and cache dirs
        if any(part in ('.venv', 'venv', '__pycache__', '.git') for part in dirpath.split(os.sep)):
            continue
        for fn in filenames:
            if not fn.endswith('.py'):
                continue
            path = os.path.join(dirpath, fn)
            try:
                if process_file(path, dry_run=dry_run):
                    modified += 1
            except Exception:
                with io.open(LOG_PATH, 'a', encoding='utf-8') as log:
                    log.write(f'ERROR processing {path}\n')
    return modified


def main() -> int:
    parser = argparse.ArgumentParser(description='Batch-fix common Python syntax corruption heuristics')
    parser.add_argument('root', nargs='?', default='src', help='Root path to scan (default: src)')
    parser.add_argument('--dry-run', action='store_true', help='Report files that would be changed without writing')
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    if not os.path.exists(root):
        print(f'Root not found: {root}', file=sys.stderr)
        return 2

    if args.dry_run:
        print('Dry run: reporting files that would be modified...')

    modified = walk_and_fix(root, dry_run=args.dry_run)
    if args.dry_run:
        print(f'Files that would be modified: {modified}')
    else:
        print(f'Files modified: {modified}. Backups saved with `.auto_fix.bak` suffix.')
        print(f'Log: {LOG_PATH}')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
