#!/usr/bin/env python3
"""Speculative fixer for string and simple syntax corruption.

This script is more aggressive than the conservative or previous aggressive fixer.
It will attempt several higher-risk heuristics (remove isolated quote chars, close
odd quote counts, join likely split string lines, and remove stray unmatched
characters). It always verifies via `compile()` before applying and creates a
`.speculative_fix.bak.TIMESTAMP` backup when writing.

USE WITH CAUTION: run with `--backup --apply` to modify files, and review backups.
"""
from __future__ import annotations

import argparse
import os
import re
import time
from pathlib import Path


def compile_ok(src: str, filename: str = "<string>") -> bool:
    try:
        compile(src, filename, "exec")
        return True
    except Exception:
        return False


def heuristics(text: str) -> list[str]:
    """Generate candidate fixes (highest-to-lowest confidence).
    Return list of candidate texts to try (first that compiles will be chosen).
    """
    candidates: list[str] = []

    # Candidate A: Close odd triple-quotes
    if text.count('"""') % 2 == 1:
        candidates.append(text + "\n\n\"\"\"\n")
    if text.count("'''") % 2 == 1:
        candidates.append(text + "\n\n'''\n")

    # Candidate B: Append a simple quote at EOF
    candidates.extend([text + q + "\n" for q in ('"', "'")])

    # Candidate C: Strip isolated quote characters that are alone on a line
    lines = text.splitlines()
    stripped = []
    changed = False
    for ln in lines:
        if ln.strip() in ('"', "'"):
            changed = True
            continue
        stripped.append(ln)
    if changed:
        candidates.append("\n".join(stripped) + "\n")

    # Candidate D: Remove stray quotes at end of lines after code/comments
    new_lines = []
    changed = False
    for ln in lines:
        if re.search(r"[^\\]\"$", ln) or re.search(r"[^\\]'$", ln):
            new_lines.append(ln[:-1])
            changed = True
        else:
            new_lines.append(ln)
    if changed:
        candidates.append("\n".join(new_lines) + "\n")

    # Candidate E: Join lines where a string literal seems split (heuristic):
    # find lines ending with an opening quote but not closing
    joined = []
    i = 0
    L = len(lines)
    while i < L:
        ln = lines[i]
        if (ln.count('"') % 2 == 1 or ln.count("'") % 2 == 1) and i + 1 < L and len(lines[i + 1].strip()) < 200:
            # join with next line
            joined.append(ln + ' ' + lines[i + 1])
            i += 2
        else:
            joined.append(ln)
            i += 1
    candidate_joined = "\n".join(joined) + "\n"
    if candidate_joined != text:
        candidates.append(candidate_joined)

    # Candidate F: as last resort, remove any unescaped stray quote characters
    cand = re.sub(r"(?m)(^|\s)(['\"])\s*(?=\n|$)", "", text)
    if cand != text:
        candidates.append(cand)

    return candidates


def process_file(path: Path, apply: bool, backup: bool, verbose: bool) -> tuple[bool, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"read_error: {e}"

    if compile_ok(text, str(path)):
        return False, "ok"

    for candidate in heuristics(text):
        if compile_ok(candidate, str(path)):
            if not apply:
                return True, "would_fix"
            try:
                if backup:
                    bak = path.with_suffix(path.suffix + f".speculative_fix.bak.{int(time.time())}")
                    bak.write_text(text, encoding="utf-8")
                    if verbose:
                        print(f"  backup -> {bak}")
                path.write_text(candidate, encoding="utf-8")
                return True, "patched"
            except Exception as e:
                return False, f"write_error: {e}"

    return False, "no_safe_fix"


def iter_target(root: Path, apply: bool, backup: bool, verbose: bool) -> dict:
    results = {"checked": 0, "ok": 0, "would_fix": 0, "patched": 0, "no_safe_fix": 0, "errors": 0}
    for dirpath, dirnames, filenames in os.walk(root):
        if any(p in dirpath for p in (".venv", "venv", "site-packages", "__pycache__", ".git")):
            continue
        for fn in filenames:
            if not fn.endswith('.py'):
                continue
            p = Path(dirpath) / fn
            results['checked'] += 1
            ok, msg = process_file(p, apply, backup, verbose)
            if msg == 'ok':
                results['ok'] += 1
            elif msg == 'would_fix':
                results['would_fix'] += 1
                if verbose:
                    print(f"WILL FIX: {p}")
            elif msg == 'patched':
                results['patched'] += 1
                print(f"PATCHED: {p}")
            elif msg == 'no_safe_fix':
                results['no_safe_fix'] += 1
            else:
                results['errors'] += 1
                print(f"ERROR {p}: {msg}")
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', required=True)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--backup', action='store_true')
    ap.add_argument('--verbose', action='store_true')
    args = ap.parse_args()

    root = Path(args.target)
    if not root.exists():
        print(f"Target not found: {root}")
        return 2

    print(f"Speculative scan {root} (apply={args.apply}, backup={args.backup})")
    res = iter_target(root, args.apply, args.backup, args.verbose)
    print('Summary:', res)
    return 0 if res['errors'] == 0 else 1


if __name__ == '__main__':
    raise SystemExit(main())
