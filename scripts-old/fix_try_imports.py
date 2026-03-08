#!/usr/bin/env python3
"""Fix files where `try:` is immediately followed by an unindented import.

This is a quick, conservative fixer used after the auto-fixer made some
imports dedented accidentally. It adds four-space indentation to imports
that directly follow a `try:` line and are at the same indentation level.

Usage:
  python scripts/fix_try_imports.py --root . --apply
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

EXCLUDE_DIRS = {".venv", "venv", "dist", "build", "target", "__pycache__", ".git"}


def iter_py_files(root: Path):
    """Recursively yield .py files under root, excluding certain directories."""
    for p in root.rglob("*.py"):
        parts = set(p.parts)
        if parts & EXCLUDE_DIRS:
            continue
        yield p


def fix_text(text: str) -> tuple[bool, str]:
    """Add indentation to imports that directly follow a try: line."""
    # Match a line that contains only optional indentation + try:
    # followed by a newline and then a line that starts with optional indentation
    # and 'from' or 'import' but that indentation is not greater than the try line.
    changed = False

    def repl(m: re.Match) -> str:
        """Repl function for re.sub. Checks if the import line is at the same or less indent than the try line."""
        nonlocal changed
        prefix = m.group(1) or ""
        try_indent = m.group(2) or ""
        imp_line = m.group(3)
        # If import is already indented more than try, leave alone
        if imp_line.startswith(try_indent + "    "):
            return m.group(0)
        changed = True
        return f"{prefix}{try_indent}try:\n{try_indent}    {imp_line}"

    pattern = re.compile(r"(^|\n)([ \t]*)try:\n([ \t]*(?:from\s+|import\s+).*)", flags=re.M)
    new_text = pattern.sub(repl, text)
    return changed, new_text


def main() -> None:
    """Main entry point for the script. Parses arguments and processes files.
    """
    p = argparse.ArgumentParser()
    p.add_argument("--root", "-r", default=".", help="Repository root")
    p.add_argument("--apply", action="store_true", help="Write changes")
    args = p.parse_args()

    root = Path(args.root).resolve()
    total = 0
    changed_files = 0
    for f in iter_py_files(root):
        txt = f.read_text(encoding="utf-8-sig")
        total += 1
        ok, new = fix_text(txt)
        if ok:
            changed_files += 1
            print(f"Fixing: {f.relative_to(root)}")
            if args.apply:
                bak = f.with_suffix(f.suffix + ".bak")
                if not bak.exists():
                    bak.write_text(txt, encoding="utf-8")
                f.write_text(new, encoding="utf-8")
    print(f"Scanned {total} files, modified {changed_files} files (apply={args.apply})")


if __name__ == '__main__':
    main()
