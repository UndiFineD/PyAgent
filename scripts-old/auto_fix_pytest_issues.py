#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Conservative fixer for common pytest import/indentation issues.

Usage:
  python scripts/auto_fix_pytest_issues.py --dry-run
  python scripts/auto_fix_pytest_issues.py --apply

This script performs conservative, reversible edits only:
- normalize BOM / NBSP characters
- dedent mis-indented top-level import lines (heuristic)
- dedent imports that appear immediately after `except`/`finally`/`else`
- move inline `import traceback` out of exception blocks when safe
- wrap trailing `main()` call in `if __name__ == '__main__'` when safe

It prints unified diffs in dry-run mode and writes files only with --apply.
"""

from __future__ import annotations

import argparse
import difflib
import re
from pathlib import Path
from typing import Iterable


EXCLUDE_DIRS = {".venv", "venv", "dist", "build", "target", "__pycache__", ".git"}


def iter_py_files(root: Path) -> Iterable[Path]:
    """Recursively yield .py files under root, excluding certain directories."""
    for p in root.rglob("*.py"):
        parts = set(p.parts)
        if parts & EXCLUDE_DIRS:
            continue
        yield p


def normalize_text(text: str) -> str:
    """Normalize text by removing non-breaking spaces and BOM characters."""
    # remove non-breaking spaces that can cause odd parsing
    # (BOM is now handled by utf-8-sig encoding)
    text = text.replace("\u00A0", " ")
    return text


def safe_wrap_main(lines: list[str]) -> list[str]:
    """Wrap a trailing main() call in a guarded block if it appears to be a bare call."""
    # If file ends with a bare main() call and defines a main(), wrap it.
    if not lines:
        return lines

    # Find the last non-empty line
    last_idx = len(lines) - 1
    while last_idx >= 0 and not lines[last_idx].strip():
        last_idx -= 1

    if last_idx < 0:
        return lines

    tail = "".join(lines[max(0, last_idx - 8):])  # inspect last few lines
    if "if __name__" in tail:
        return lines

    if lines[last_idx].strip() == "main()":
        # check for a def main earlier
        joined = "".join(lines)
        if re.search(r"def\s+main\s*\(", joined):
            # replace the last occurrence with a guarded version
            new = lines[:last_idx]
            new.append("if __name__ == '__main__':\n")
            new.append("    main()\n")
            # Preserve any trailing newlines that were after main()
            new.extend(lines[last_idx + 1:])
            return new
    return lines


def dedent_imports(lines: list[str]) -> list[str]:
    """Dedent import lines that appear to be mis-indented at top-level or after control flow."""
    out: list[str] = []
    # helper to get previous non-empty non-comment line
    def prev_nonempty(idx: int) -> str | None:
        for j in range(idx - 1, -1, -1):
            raw = lines[j]
            if raw.strip():
                return raw
        return None

    for i, line in enumerate(lines):
        m = re.match(r"^(\s+)(from|import)\s+", line)
        if m:
            prev = prev_nonempty(i)
            prev_str = prev.strip() if prev is not None else None
            prev_lstr = prev.lstrip() if prev is not None else None
            # Conservative: only dedent when previous meaningful line clearly
            # indicates top-level or a continued import (closing paren, comma, \),
            # or when previous line is another import or comment. Do NOT dedent
            # imports that are inside explicit control-flow blocks like try/except/else/finally
            # because moving them can break block structure (e.g. a `try:` must be
            # followed by an indented block).
            is_safe_prev = (
                prev is None or
                (prev_str is not None and prev_str.endswith(")")) or
                (prev_str is not None and prev_str.endswith(",")) or
                (prev_str is not None and prev_str.endswith("\\")) or
                (prev_lstr is not None and prev_lstr.startswith("from ")) or
                (prev_lstr is not None and prev_lstr.startswith("import ")) or
                (prev_lstr is not None and prev_lstr.startswith("#"))
            )
            # If the previous meaningful line is indented, we're likely inside
            # a block (for example, a `try:` body's imports); in that case
            # do not dedent — leave indentation as-is.
            if is_safe_prev:
                if prev is not None and (prev.startswith(" ") or prev.startswith("\t")):
                    out.append(line)
                    continue
                new_line = line.lstrip()
                if new_line != line:
                    out.append(new_line)
                    continue
        out.append(line)
    return out


def indent_imports_after_try(lines: list[str]) -> list[str]:
    """Indent imports that immediately follow a `try:` but are not indented.

    Some files contain a `try:` followed by unindented imports (likely caused by
    prior dedent operations). This function conservatively indents those imports
    by one level (4 spaces) to restore valid block structure.
    """
    out: list[str] = list(lines)
    i = 0
    while i < len(out) - 1:
        line = out[i]
        m_try = re.match(r"^(\s*)try:\s*$", line)
        if m_try:
            try_indent = m_try.group(1)
            block_indent = try_indent + "    "
            j = i + 1
            # Indent any immediately following import/from lines that have no indent
            while j < len(out):
                nxt = out[j]
                if not nxt.strip():
                    # stop at blank line — imports should be immediate
                    break
                # match import lines possibly already indented
                m_imp = re.match(r"^(\s*)(from|import)\s+", nxt)
                if m_imp:
                    # If import is already indented to at least block indent, leave it
                    if len(m_imp.group(1)) >= len(block_indent):
                        j += 1
                        continue
                    # Otherwise, re-indent to block level and preserve the rest
                    out[j] = block_indent + nxt.lstrip()
                    j += 1
                    continue
                # stop if next line is not an import; leave structure alone
                break
        i += 1
    return out


def indent_imports_after_control(lines: list[str]) -> list[str]:
    """Indent imports that immediately follow control-flow headers (try/except/else/finally).

    This generalizes `indent_imports_after_try` to handle other control-flow headers
    which may have lost their indented blocks during prior transformations.  We
    also treat ``if TYPE_CHECKING:`` as a control header so that dedented
    imports can be pushed back inside the block.
    """
    out: list[str] = list(lines)
    i = 0
    control_kw = ("try", "except", "else", "finally")
    while i < len(out) - 1:
        line = out[i]
        m = re.match(r"^(\s*)(?:try|except|else|finally|if\s+TYPE_CHECKING)\s*:\s*$", line)
        if m:
            base = m.group(1)
            block_indent = base + "    "
            j = i + 1
            while j < len(out):
                nxt = out[j]
                if not nxt.strip():
                    break
                m_imp = re.match(r"^(\s*)(from|import)\s+", nxt)
                if m_imp:
                    if len(m_imp.group(1)) >= len(block_indent):
                        j += 1
                        continue
                    out[j] = block_indent + nxt.lstrip()
                    j += 1
                    continue
                break
        i += 1
    return out


def move_inline_traceback(lines: list[str]) -> list[str]:
    """Dedent `import traceback` when it's inside an except/finally block.

    We only un-indent the import to the same level as the `except` line
    (or top-level) to avoid changing module semantics too aggressively.
    """
    out: list[str] = []
    for i, line in enumerate(lines):
        m = re.match(r"^(\s+)(import\s+traceback\b)", line)
        if m:
            # find previous meaningful line
            prev = None
            for j in range(i - 1, -1, -1):
                s = lines[j].strip()
                if s:
                    prev = lines[j]
                    break
            if prev is not None and prev.lstrip().startswith(("except", "finally", "else")):
                # move import to same indent level as prev (dedent)
                match = re.match(r"^(\s*)", prev)
                indent = match.group(1) if match else ""
                out.append(indent + m.group(2) + "\n")
                continue
        out.append(line)
    return out



from auto_fix.rule_engine import RuleEngine

_engine = RuleEngine.load_from_dir("src/auto_fix/rules")


def analyze_and_fix_file(path: Path, root: Path, apply: bool) -> tuple[bool, str]:
    """Analyze a file for common pytest issues by delegating to the rule engine.

    Returns a tuple where the first element indicates whether a fix was
    proposed and the second element contains a unified diff describing the
    change.  The behaviour mirrors the previous implementation while
    consolidating all transformation logic inside ``src/auto_fix/rules``.
    """
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return False, ""

    fixes = _engine.evaluate(str(path), text)
    if not fixes:
        return False, ""

    # We conservatively apply only the first fix in this script; rules are
    # written in a way that a single fix encapsulates all necessary changes
    fix = fixes[0]
    new_text = fix.replacement

    try:
        rel_path = path.relative_to(root)
    except ValueError:
        rel_path = path

    diff = "\n".join(difflib.unified_diff(
        text.splitlines(),
        new_text.splitlines(),
        fromfile=str(rel_path),
        tofile=str(rel_path) + " (fixed)",
        lineterm=""
    ))
    if apply:
        try:
            bak = path.with_suffix(path.suffix + ".bak")
            if not bak.exists():
                bak.write_text(text, encoding="utf-8")
        except (OSError, IOError):
            pass
        path.write_text(new_text, encoding="utf-8")
    return True, diff


def main() -> None:
    """Main entry point for the script. Parses arguments and processes .py files under the specified root."""
    p = argparse.ArgumentParser()
    p.add_argument("--root", "-r", default=".", help="Repository root to scan")
    p.add_argument("--apply", action="store_true", help="Apply changes (default: dry-run)")
    p.add_argument("--limit", type=int, default=0, help="Limit number of files changed (0 => no limit)")
    p.add_argument("--quiet", "-q", action="store_true", help="Suppress diff output")
    args = p.parse_args()

    root = Path(args.root).resolve()
    apply = args.apply

    changed_files = 0
    for f in iter_py_files(root):
        ok, diff = analyze_and_fix_file(f, root, apply)
        if ok:
            changed_files += 1
            print(f"=== Proposed fix: {f.relative_to(root)}")
            if not args.quiet:
                print(diff or "(no textual diff available)")
            print()
            if args.limit and changed_files >= args.limit:
                break

    if changed_files == 0:
        print("No conservative fixes were needed.")
    else:
        print(f"Processed {changed_files} file(s). (apply={apply})")


if __name__ == "__main__":
    main()
