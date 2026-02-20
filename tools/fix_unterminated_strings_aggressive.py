#!/usr/bin/env python3
"""Aggressive, heuristic fixer for unterminated/imbalanced string literals.

Usage: python tools/fix_unterminated_strings_aggressive.py --target src [--apply] [--backup] [--verbose]

This is a risky script: it attempts simple heuristics (close unbalanced triple-quotes,
append single/double quote at EOF, strip trailing stray quotes) and verifies with
`compile()` before writing changes. Always run with `--backup` and review diffs.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path


def compile_ok(src: str, filename: str = "<string>") -> bool:
    try:
        compile(src, filename, "exec")
        return True
    except Exception:
        return False


def try_fixes(text: str) -> tuple[bool, str]:
    # Try a sequence of heuristic fixes. Return (fixed, new_text).
    orig = text

    # 1) Balance triple double quotes
    if text.count('"""') % 2 == 1:
        candidate = text + "\n\n\"\"\"\n"
        if compile_ok(candidate):
            return True, candidate

    # 2) Balance triple single quotes
    if text.count("'''") % 2 == 1:
        candidate = text + "\n\n'''\n"
        if compile_ok(candidate):
            return True, candidate

    # 3) Try appending a single or double quote at EOF
    for q in ['"', "'"]:
        candidate = text + q + "\n"
        if compile_ok(candidate):
            return True, candidate

    # 4) Remove trailing stray quote characters at ends of lines
    lines = text.splitlines()
    modified = False
    new_lines = []
    for ln in lines:
        if ln.rstrip().endswith(('"', "'")) and len(ln.strip()) > 1:
            new_lines.append(ln.rstrip()[:-1])
            modified = True
        else:
            new_lines.append(ln)
    if modified:
        candidate = "\n".join(new_lines) + "\n"
        if compile_ok(candidate):
            return True, candidate

    # 5) As a last-ditch: append both triple-quotes and a single quote, in case of nested mess
    candidate = text + "\n\n\"\"\"\n'\n"
    if compile_ok(candidate):
        return True, candidate

    return False, orig


def process_file(path: Path, apply: bool, backup: bool, verbose: bool) -> tuple[bool, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"read_error: {e}"

    if compile_ok(text, str(path)):
        return False, "ok"

    fixed, new_text = try_fixes(text)
    if not fixed:
        return False, "no_safe_fix"

    if not apply:
        return True, "would_fix"

    # apply with backup
    try:
        if backup:
            bak = path.with_suffix(path.suffix + f".aggressive_fix.bak.{int(time.time())}")
            bak.write_text(text, encoding="utf-8")
            if verbose:
                print(f"  backup -> {bak}")
        path.write_text(new_text, encoding="utf-8")
        return True, "patched"
    except Exception as e:
        return False, f"write_error: {e}"


def iter_target(root: Path, apply: bool, backup: bool, verbose: bool) -> dict:
    results = {"checked": 0, "ok": 0, "would_fix": 0, "patched": 0, "no_safe_fix": 0, "errors": 0}
    for dirpath, dirnames, filenames in os.walk(root):
        # skip virtualenvs, .git, __pycache__, and other large irrelevant dirs
        if any(p in dirpath for p in (".venv", "venv", "site-packages", "__pycache__", ".git")):
            continue
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            p = Path(dirpath) / fn
            results["checked"] += 1
            ok, msg = process_file(p, apply, backup, verbose)
            if msg == "ok":
                results["ok"] += 1
                if verbose:
                    print(f"OK: {p}")
            elif msg == "would_fix":
                results["would_fix"] += 1
                print(f"WILL FIX: {p}")
            elif msg == "patched":
                results["patched"] += 1
                print(f"PATCHED: {p}")
            elif msg == "no_safe_fix":
                results["no_safe_fix"] += 1
                if verbose:
                    print(f"NO SAFE FIX: {p}")
            else:
                results["errors"] += 1
                print(f"ERROR {p}: {msg}")
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, help="Target dir to scan")
    ap.add_argument("--apply", action="store_true", help="Write fixes instead of dry-run")
    ap.add_argument("--backup", action="store_true", help="Create .aggressive_fix.bak.* backups before writing")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    root = Path(args.target)
    if not root.exists():
        print(f"Target not found: {root}")
        return 2

    print(f"Scanning {root} (apply={args.apply}, backup={args.backup})")
    res = iter_target(root, args.apply, args.backup, args.verbose)
    print("Summary:", res)
    # exit code: 0 if no errors and nothing dangerous; 1 if some files couldn't be fixed
    if res["errors"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
