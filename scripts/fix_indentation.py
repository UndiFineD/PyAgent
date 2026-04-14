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

"""fix_indentation.py - Smart, multi-pass indentation fixer for PyAgent src.

USAGE
    python scripts/fix_indentation.py [--path PATH] [--dry-run] [--verbose] [--max-passes N]

PURPOSE
    Fixes mis-indented Python source files that result from a known code-generation
    defect where certain lines lose their leading whitespace.  Three primary defect
    patterns are targeted:

    Pattern A  -  An `import` / `from ... import` line inside a method body that
                  appears at column 0 (or wrong indent) while the surrounding lines
                  are properly indented.

        def method(self):
            body = 1
from functools import reduce   # should be 8 spaces
            return reduce(...)

    Pattern B  -  One or more consecutive non-import lines inside a method body
                  that also appear at the wrong indent level, immediately adjacent
                  to a pattern-A line or another pattern-B line.

        def method(self):
            body = 1
from functools import reduce
        result = reduce(f, x, [])      # both lines should be at 8 spaces
            return result

    Pattern C  -  A `def` line (or the lines of a whole method) inside a class body
                  whose indent is less than expected, so they appear at or near
                  module scope instead of inside the class.

        class Foo:
            def good(self): ...

        def bad(self): ...                # missing 4 spaces

ALGORITHM
    Phase 1 - Survey:
        Attempt to compile every .py file.  Collect the set of files that raise
        SyntaxError / IndentationError, recording the error line number.

    Phase 2 - Repair (repeated until stable, up to MAX_PASSES):
        For each broken file in each pass:
          1. Walk every line and compute a "context indent" from the N=15 nearest
             non-blank non-comment lines before and after it.
          2. If the line is at an unexpectedly low indent and the context strongly
             suggests a higher indent (≥ 4 spaces), add the inferred indent.
          3. Additionally, run a targeted "class-body method repair" pass that
             detects `def NAME(self` lines outside the expected class body indent
             and shifts them (and their body) to the right by the needed amount.
          4. A new post-processing step fixes lines immediately following an
             `except` clause that were accidentally dedented.  This ensures any
             non-blank content in the except block is indented one level.

    Phase 3 - Verify:
        Re-compile every file that was modified and report pass/fail.

Notes
-----
    - Only lines whose stripped content does NOT start with `class ` at a higher
      nesting are touched, to avoid moving genuinely module-level code.
    - The script is idempotent: re-running is safe.
    - `--dry-run` prints what would change without writing.

"""

from __future__ import annotations

import argparse

# import ast
import re
import sys
import time
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
CONTEXT_WINDOW = 20  # lines to scan before/after for indent inference
MIN_INDENT_STEP = 4  # smallest natural indent step in Python
MAX_PASSES = 20  # safety cap on repair passes per file

# Patterns that represent lines which cannot live at column 0 inside a class body.
_IMPORT_RE = re.compile(r"^(from\s+\S|\bimport\s+\S)")
_DEF_RE = re.compile(r"^def\s+\w+\s*\(")
_ASYNC_DEF_RE = re.compile(r"^async\s+def\s+\w+\s*\(")

# Lines that open a new indented block
_BLOCK_OPENER_RE = re.compile(r":\s*(?:#.*)?$")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _indent(line: str) -> int:
    """Return the indentation width (spaces only; tabs count as 1)."""
    return len(line) - len(line.lstrip(" \t"))


def _is_blank_or_comment(line: str) -> bool:
    """Return True if the line is blank or a comment (ignoring leading whitespace)."""
    s = line.strip()
    return not s or s.startswith("#")


def _compile_check(path: Path) -> Optional[SyntaxError]:
    """Return the SyntaxError if the file is broken, else None."""
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        compile(source, str(path), "exec")
        return None
    except SyntaxError as e:
        return e


def _parse_error_log(log_path: Path, project_root: Path) -> dict[Path, set[int]]:
    """Parse a pytest-style error log and return mapping of files to offending line numbers.

    The log is scanned for lines like::

        File "c:/dev/PyAgent/src/foo/bar.py", line 123

    Paths are resolved against the project root so relative paths still work.
    The returned dict maps absolute Path -> set of 1-based line numbers.
    """
    entries: dict[Path, set[int]] = {}
    regex = re.compile(r'File "([^"]+)", line (\d+)')
    try:
        text = log_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return entries
    for line in text.splitlines():
        m = regex.search(line)
        if not m:
            continue
        raw = m.group(1)
        try:
            p = Path(raw)
            if not p.is_absolute():
                p = project_root / p
            p = p.resolve()
        except Exception:  # noqa: S112
            continue
        lineno = int(m.group(2))
        entries.setdefault(p, set()).add(lineno)
    return entries


def _context_indent(lines: list[str], idx: int, window: int = CONTEXT_WINDOW) -> int:
    """Infer the expected indentation for lines[idx] by looking at the
    surrounding `window` non-blank non-comment lines.

    Returns the most common indent value >= MIN_INDENT_STEP found in the
    window, or 0 if the context is predominantly module-level.
    """
    candidates: list[int] = []

    # Scan backward
    count = 0
    for i in range(idx - 1, max(-1, idx - window - 1), -1):
        if _is_blank_or_comment(lines[i]):
            continue
        ind = _indent(lines[i])
        if ind > 0:
            candidates.append(ind)
        count += 1
        if count >= window:
            break

    # Scan forward
    count = 0
    for i in range(idx + 1, min(len(lines), idx + window + 1)):
        if _is_blank_or_comment(lines[i]):
            continue
        ind = _indent(lines[i])
        if ind > 0:
            candidates.append(ind)
        count += 1
        if count >= window:
            break

    if not candidates:
        return 0

    from collections import Counter

    freq = Counter(candidates)

    # Prioritize indents that appear multiple times
    multi_freq_indents = [k for k, v in freq.items() if v >= 2]
    if multi_freq_indents:
        # Return the smallest of the most frequent indents
        return min(multi_freq_indents)

    # If no indent appears multiple times, return the most common single indent.
    # This will be the only one if all appear once, or one of the equally most common.
    # This makes _context_indent less conservative.
    most_common_indent = freq.most_common(1)[0][0]
    return most_common_indent


def _prev_nonblank_index(lines: list[str], idx: int) -> int:
    """Return index of previous non-blank, non-comment line before idx, or -1."""
    for j in range(idx - 1, -1, -1):
        if not _is_blank_or_comment(lines[j]):
            return j
    return -1


def _preceding_block_indent(lines: list[str], idx: int) -> int:
    """Walk backward from idx to find the nearest line that ends with ':'
    (opens a block).  Return THAT line's indent + MIN_INDENT_STEP so we
    know what the first line of the block should look like.
    Returns -1 if not found.
    """
    for i in range(idx - 1, -1, -1):
        line = lines[i]
        if _is_blank_or_comment(line):
            continue
        stripped = line.rstrip()
        if stripped.endswith(":"):
            # The body of this block should be indented by MIN_INDENT_STEP more
            return _indent(line) + MIN_INDENT_STEP
        # If we hit a non-colon line that's at or more indented than us, keep going
        # but stop at a clearly module-level line that doesn't open a block.
        if _indent(line) == 0 and not stripped.endswith(":"):
            return -1
    return -1


# ---------------------------------------------------------------------------
# Pass 1: Fix zero/low-indent lines that are surrounded by body code
# ---------------------------------------------------------------------------
def _is_import_or_simple_stmt(stripped: str) -> bool:
    """Return True for lines that are commonly found as in-method imports."""
    return bool(_IMPORT_RE.match(stripped))


def pass_fix_orphan_imports(
    lines: list[str],
    verbose: bool = False,
    focus_lines: set[int] | None = None,
) -> tuple[list[str], int]:
    """Fix lines at column 0 (or unexpectedly low indent) that are preceded and
    followed by higher-indented code.  Changes are applied conservatively.

    If ``focus_lines`` is provided the pass will only touch lines that are
    within two lines of any number in the set.  This allows surgical fixes
    based on an external error log.

    Returns (new_lines, number_of_changes).
    """
    result = list(lines)
    changes = 0

    for i, line in enumerate(result):
        if _is_blank_or_comment(line):
            continue

        # skip lines not near any focus if we have one
        if focus_lines is not None:
            lineno = i + 1
            if not any(abs(lineno - f) <= 2 for f in focus_lines):
                continue

        stripped = line.lstrip()
        current_indent = _indent(line)

        # Only attempt to fix lines at exactly 0 or 4 that look like they
        # belong inside a method (we avoid mangling genuinely module-level code).
        if current_indent > MIN_INDENT_STEP:
            continue

        # We only fix import statements here (the safest targeted fix).
        if not _is_import_or_simple_stmt(stripped.rstrip()):
            continue

        # Infer expected indent from context.
        expected = _context_indent(result, i)
        if expected <= current_indent:
            # Context says the current indent is fine (or we can't tell).
            if verbose:
                msg = (
                    f"        line {i + 1:5d}: SKIP (context_indent={expected}, "
                    f"current={current_indent})  {stripped[:70].rstrip()!a}"
                )
                print(msg)
            continue

        # Never move __future__ imports or dunder module-level assignments.
        if stripped.startswith("from __future__") or stripped.startswith("__"):
            if verbose:
                print(f"        line {i + 1:5d}: SKIP (future/dunder import)")
            continue

        # Double-check: look for the enclosing block opener.
        block_start = _preceding_block_indent(result, i)

        # If there is no enclosing block opener preceding this line and there
        # are no prior indented lines in the file, this is almost certainly a
        # module-level import and should not be shifted.
        has_prior_indented = any(
            _indent(existing_line) > 0 for existing_line in result[:i] if not _is_blank_or_comment(existing_line)
        )
        if block_start == -1 and not has_prior_indented:
            if verbose:
                print(f"        line {i + 1:5d}: SKIP (no enclosing block and no prior indents)")
            continue

        if block_start > 0:
            # Use the block-determined indent unless context suggests something bigger.
            best = max(block_start, expected) if expected > 0 else block_start
        else:
            best = expected

        if best != current_indent:
            if verbose:
                print(
                    f"        line {i + 1:5d}: indent {current_indent}->{best}  "
                    f"(block_start={block_start}, context={expected})"
                )
                print(f"               BEFORE: {line.rstrip()!a}")
                print(f"               AFTER:  {(' ' * best + stripped.rstrip())!a}")
            result[i] = " " * best + stripped.rstrip("\n") + "\n"
            changes += 1

    return result, changes


def pass_indent_after_except(
    lines: list[str],
    verbose: bool = False,
    focus_lines: set[int] | None = None,
) -> tuple[list[str], int]:
    """Ensure the first non-blank line after any `except ...:` is indented
    one step deeper than the except line itself.  This handles a common
    code-gen defect where the block header is present but the body loses
    its leading whitespace.

    If ``focus_lines`` is provided we only examine areas near the reported
    line numbers (within two lines), keeping the pass efficient for
    targeting known failures.
    """
    result = list(lines)
    changes = 0

    for i, line in enumerate(lines[:-1]):
        if _is_blank_or_comment(line):
            continue

        # optional focus filtering
        if focus_lines is not None:
            lineno = i + 1
            if not any(abs(lineno - f) <= 2 for f in focus_lines):
                continue

        stripped = line.lstrip()
        if stripped.startswith("except") and stripped.rstrip().endswith(":"):
            next_line = result[i + 1]
            if _is_blank_or_comment(next_line):
                continue
            expected_indent = _indent(line) + MIN_INDENT_STEP
            if _indent(next_line) < expected_indent:
                result[i + 1] = " " * expected_indent + next_line.lstrip()
                changes += 1
                if verbose:
                    print(f"        indent-after-except: line {i + 2} -> {expected_indent} spaces")
    return result, changes


# ---------------------------------------------------------------------------
# Pass 2: Fix streams of consecutive wrong-indent lines (not just imports)
# ---------------------------------------------------------------------------
def pass_fix_misindented_blocks(
    lines: list[str],
    verbose: bool = False,
    focus_lines: set[int] | None = None,
) -> tuple[list[str], int]:
    """Detects runs of consecutive lines at an unexpectedly low indent that are
    sandwiched between higher-indented code.  Shifts the whole run upward.

    If ``focus_lines`` is provided the run will only be adjusted when it
    intersects (±2 lines) with any of the focus line numbers.

    Handles patterns like::

        def method(self):
            a = 1
        from functools import reduce      # <-- wrong
        result = reduce(...)                # <-- wrong
            return result

    Both lines in the run are shifted to match their neighbours.
    """
    result = list(lines)
    changes = 0

    # Find runs of consecutive "wrong" lines (lines at 0 indent between
    # higher-indented neighbours).
    i = 0
    while i < len(result):
        line = result[i]
        if _is_blank_or_comment(line):
            i += 1
            continue

        current = _indent(line)
        if current > MIN_INDENT_STEP:
            i += 1
            continue

        # Collect a run of consecutive lines at ≤ MIN_INDENT_STEP
        run_start = i
        run_end = i
        while run_end < len(result):
            run_line = result[run_end]
            if _is_blank_or_comment(run_line):
                run_end += 1
                continue
            if _indent(run_line) > MIN_INDENT_STEP:
                break
            # Stop the run if we hit a class or top-level def WITHOUT self
            s = run_line.strip()
            if s.startswith("class ") or (_DEF_RE.match(s) and "self" not in run_line and "cls" not in run_line):
                break
            run_end += 1

        # Guard: inner loop broke immediately (e.g. class at col 0) – skip.
        if run_end == run_start:
            i += 1
            continue

        # If we are focusing, verify the run overlaps a focus line nearby.
        if focus_lines is not None:
            run_line_nums = set(range(run_start + 1, run_end + 1))
            if not any(abs(r - f) <= 2 for r in run_line_nums for f in focus_lines):
                i = run_end
                continue

        run_lines = result[run_start:run_end]
        has_import = any(
            _is_import_or_simple_stmt(run_line.strip()) for run_line in run_lines if not _is_blank_or_comment(run_line)
        )
        # Apply a context or block-based indent lookup if there's no import.
        if not has_import:
            # Check if this block should be indented because it follows a try/except/def/etc.
            block_start = _preceding_block_indent(result, run_start)
            context_indent = _context_indent(result, run_start)
            expected = max(block_start, context_indent) if block_start > 0 else context_indent

            # Additional heuristic: If it starts with 'except' or 'finally', it must match the try block level,
            # which is block_start - MIN_INDENT_STEP if block_start is valid.
            stripped_first = run_lines[0].lstrip() if run_lines else ""
            if stripped_first.startswith(("except ", "except:", "finally:")):
                # Usually follows a try block, so indent should be same as the try.
                # Just use context which is hopefully right, or look specifically for `try:`.
                expected = max(MIN_INDENT_STEP, expected)
            elif expected <= current:
                i = run_end
                continue
        else:
            expected = _context_indent(result, run_start)

        if expected <= current:
            if verbose:
                real_run = [j for j in range(run_start, run_end) if not _is_blank_or_comment(result[j])]
                print(
                    f"        lines {run_start + 1}-{run_end}: SKIP block "
                    f"(context_indent={expected} <= current={current}, {len(real_run)} line(s))"
                )
            i = run_end
            continue

        if verbose:
            real_run = [j for j in range(run_start, run_end) if not _is_blank_or_comment(result[j])]
            num_lines = len(real_run)
            print(
                f"        lines {run_start + 1}-{run_end}: block of {num_lines} line(s), "
                f"shift indent {current}->{expected}"
            )

        # Apply the same indent to every non-blank non-comment line in the run.
        for j in range(run_start, run_end):
            run_line = result[j]
            if _is_blank_or_comment(run_line):
                continue
            l_stripped = run_line.lstrip()
            existing = _indent(run_line)
            delta = expected - current
            new_indent = max(0, existing + delta)
            if verbose:
                print(f"          line {j + 1:5d}: indent {existing}->{new_indent}  {l_stripped[:60].rstrip()!a}")
            result[j] = " " * new_indent + l_stripped.rstrip("\n") + "\n"
            changes += 1

        i = run_end

    return result, changes


# ---------------------------------------------------------------------------
# Pass 3: Fix method definitions that escaped their class body
# ---------------------------------------------------------------------------
def pass_fix_escaped_methods(
    lines: list[str],
    verbose: bool = False,
    focus_lines: set[int] | None = None,
) -> tuple[list[str], int]:
    """Detects `def NAME(self, ...` and `async def NAME(self, ...` lines at column 0
    (or lower than expected) that follow a class body.  Shifts the entire
    method (def + body) by the missing indentation.

    When ``focus_lines`` is given the repair will only trigger if the method
    signature or some line in its body falls within two lines of a focus
    line number.

    Only acts when a class definition appears earlier in the file and the
    adjacent methods in the class body are properly indented.
    """
    result = list(lines)
    changes = 0

    # First, collect all class definitions and their expected body indent.
    # class_regions: list of (class_start_idx, expected_method_indent)
    class_stack: list[tuple[int, int]] = []  # (class_line_idx, body_indent)
    for i, line in enumerate(result):
        if _is_blank_or_comment(line):
            continue
        s = line.strip()
        if re.match(r"^class\s+\w+", s):
            expected_body = _indent(line) + MIN_INDENT_STEP
            class_stack.append((i, expected_body))

    if not class_stack:
        return result, changes

    # For each class, look for `def ... (self` / `async def ... (self` at
    # column 0 that appear AFTER the class definition, suggesting they slipped.
    last_class_idx = class_stack[-1][0]
    # last_class_body_indent = class_stack[-1][1]

    i = 0
    while i < len(result):
        line = result[i]
        if _is_blank_or_comment(line):
            i += 1
            continue

        s = line.strip()
        ind = _indent(line)

        # Candidate: def/async def with self at unexpectedly low indent (< 4)
        is_method_def = (_DEF_RE.match(s) or _ASYNC_DEF_RE.match(s)) and ("self" in s or "cls" in s)
        if not is_method_def or ind >= MIN_INDENT_STEP:
            i += 1
            continue

        # if we have focus rules, make sure this definition or nearby lines
        # intersect them; otherwise skip quickly.
        if focus_lines is not None:
            lineno = i + 1
            if not any(abs(lineno - f) <= 2 for f in focus_lines):
                # check body extent before skipping entirely
                block_end = _find_block_end(result, i, ind)
                run_line_nums = set(range(i + 1, block_end + 1))
                if not any(abs(r - f) <= 2 for r in run_line_nums for f in focus_lines):
                    i += 1
                    continue

        # Check if we are after a class definition
        if i <= last_class_idx:
            i += 1
            continue

        # Find the correct indent for this method by looking at other
        # well-indented methods in the file.
        expected_method_indent = _infer_method_indent(result, i)
        if expected_method_indent <= ind:
            i += 1
            continue

        # Collect the entire method body (until next same-or-lower indent
        # non-blank line or end of file).
        block_end = _find_block_end(result, i, ind)
        delta = expected_method_indent - ind

        if verbose:
            method_sig = result[i].strip()[:70]
            print(f"        line {i + 1:5d}: escaped method - shift +{delta} spaces  {method_sig!a}")
            print(f"                        -> body lines {i + 1}-{block_end}")

        for j in range(i, block_end):
            block_line = result[j]
            if not block_line.strip():  # keep blank lines blank
                continue
            existing_indent = _indent(block_line)
            new_indent = existing_indent + delta
            if verbose:
                print(
                    f"          line {j + 1:5d}: indent {existing_indent}->{new_indent}  "
                    f"{block_line.lstrip()[:55].rstrip()!a}"
                )
            result[j] = " " * new_indent + block_line.lstrip()
            changes += 1

        i = block_end

    return result, changes


def _infer_method_indent(lines: list[str], idx: int) -> int:
    """Look backward and forward for other `def ... (self` lines whose indent > 0,
    return the most common such indent value.
    """
    indents: list[int] = []
    for i, line in enumerate(lines):
        if i == idx:
            continue
        s = line.strip()
        ind = _indent(line)
        if (_DEF_RE.match(s) or _ASYNC_DEF_RE.match(s)) and ("self" in s or "cls" in s) and ind > 0:
            indents.append(ind)

    if not indents:
        return MIN_INDENT_STEP

    from collections import Counter

    return Counter(indents).most_common(1)[0][0]


def _find_block_end(lines: list[str], start: int, base_indent: int) -> int:
    """Return the index of the first line after the block beginning at `start`
    that is at or below `base_indent` (exclusive), or end-of-file.
    """
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if not line.strip():
            continue
        if _indent(line) <= base_indent:
            return i
    return len(lines)


# ---------------------------------------------------------------------------
# Pass 4: Ensure `load` alias is not accidentally introduced (idempotency fix)
# ---------------------------------------------------------------------------
def pass_dedup_method_aliases(lines: list[str]) -> tuple[list[str], int]:
    """Removes accidental duplicate `load = load_config` or `load = load` style
    alias lines introduced during earlier passes.  Very targeted.
    """
    # Not needed for the indentation fixer; placeholder for future use.
    return lines, 0


# ---------------------------------------------------------------------------
# Core repair loop for a single file
# ---------------------------------------------------------------------------
def repair_file(
    path: Path,
    max_passes: int = MAX_PASSES,
    verbose: bool = False,
    focus_lines: set[int] | None = None,
) -> tuple[int, bool, list[str]]:
    """Repair a single file. Returns (total_changes, now_valid, new_lines)."""
    try:
        original = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0, False, []

    lines = original.splitlines(keepends=True)
    # Ensure every line ends with a newline for consistency.
    lines = [line_text if line_text.endswith("\n") else line_text + "\n" for line_text in lines]

    total_changes = 0
    pass_stats: list[tuple[int, int, int, int]] = []  # (pass_num, c1, c2, c3)

    for pass_num in range(1, max_passes + 1):
        # Check if already valid
        err = _compile_check_lines(lines)
        if err is None:
            if verbose and pass_num > 1:
                print(f"      [OK] file compiles cleanly after pass {pass_num - 1}")
            break

        if verbose:
            print(f"    -- pass {pass_num} --  error at line {err.lineno}: {err.msg}")

        prev_lines = list(lines)

        # Apply all three passes in order
        if verbose:
            print(f"      [pass {pass_num}/A] orphan imports")
        lines, c1 = pass_fix_orphan_imports(lines, verbose=verbose, focus_lines=focus_lines)

        if verbose:
            print(f"      [pass {pass_num}/B] misindented blocks")
        lines, c2 = pass_fix_misindented_blocks(lines, verbose=verbose, focus_lines=focus_lines)

        if verbose:
            print(f"      [pass {pass_num}/C] escaped methods")
        lines, c3 = pass_fix_escaped_methods(lines, verbose=verbose, focus_lines=focus_lines)

        # new pass to fix dedented content after except:
        if verbose:
            print(f"      [pass {pass_num}/D] indent-after-except")
        lines, c4 = pass_indent_after_except(lines, verbose=verbose, focus_lines=focus_lines)

        pass_stats.append((pass_num, c1, c2, c3, c4))
        pass_total = c1 + c2 + c3 + c4
        total_changes += pass_total

        if verbose:
            print(f"      pass {pass_num} result: {pass_total} change(s)  [A={c1} B={c2} C={c3} D={c4}]")

        if lines == prev_lines:
            if verbose:
                print(f"      no progress in pass {pass_num} - stopping early")
            # No progress - stop to avoid infinite loop
            break

    if verbose and pass_stats:
        print(f"    total passes run: {len(pass_stats)}, total line changes: {total_changes}")
        print(
            "    per-pass summary: "
            + ", ".join(f"pass{p}={c1 + c2 + c3 + c4}(A={c1},B={c2},C={c3},D={c4})" for p, c1, c2, c3, c4 in pass_stats)
        )

    return total_changes, _compile_check_lines(lines) is None, lines


def _compile_check_lines(lines: list[str]) -> Optional[SyntaxError]:
    source = "".join(lines)
    try:
        compile(source, "<string>", "exec")
        return None
    except SyntaxError as e:
        return e


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    """Process command-line arguments and repair indentation errors in Python files.

    Scans target directory for syntax errors, applies multi-pass indentation fixes,
    and reports results. Returns 0 on success or 1 if files remain broken.
    """
    parser = argparse.ArgumentParser(description="Smart indentation fixer for PyAgent src/ files.")
    parser.add_argument(
        "--path",
        default=None,
        help="Root directory to scan (default: src/ relative to project root).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report what would be changed without writing files.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print per-file repair progress.",
    )
    parser.add_argument(
        "--max-passes",
        type=int,
        default=MAX_PASSES,
        help=f"Maximum repair passes per file (default: {MAX_PASSES}).",
    )
    parser.add_argument(
        "--file",
        default=None,
        help="Fix a single specific file instead of scanning a directory.",
    )
    parser.add_argument(
        "--error-log",
        default=None,
        help="Path to pytest error output; only files/lines mentioned will be repaired.",
    )
    args = parser.parse_args()

    # Resolve root
    project_root = Path(__file__).resolve().parent.parent
    # determine set of files to inspect
    error_map: dict[Path, set[int]] | None = None
    if args.error_log:
        log_path = Path(args.error_log)
        error_map = _parse_error_log(log_path, project_root)
        # if the log contained our own survey output rather than pytest format,
        # try a secondary pass that understands the "BROKEN line X" lines.
        if not error_map:
            # read and scan for the survey style "BROKEN" messages
            try:
                text = log_path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                text = ""
            # pattern: BROKEN  line   20: ...\n *src\path\file.py
            fallback: dict[Path, set[int]] = {}
            pattern = re.compile(r"BROKEN\s+line\s+(\d+):")
            lines = text.splitlines()
            i = 0
            while i < len(lines):
                m = pattern.search(lines[i])
                if m:
                    lineno = int(m.group(1))
                    # next nonblank line is path
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines):
                        raw = lines[j].strip()
                        try:
                            p = Path(raw)
                            if not p.is_absolute():
                                p = project_root / p
                            p = p.resolve()
                        except (OSError, RuntimeError):
                            i = j + 1
                            continue
                        fallback.setdefault(p, set()).add(lineno)
                        i = j + 1
                        continue
                i += 1
            if fallback:
                error_map = fallback
            else:
                print(f"Warning: --error-log provided but no entries parsed from {log_path}")

    if args.file:
        target_files = [Path(args.file).resolve()]
    else:
        if error_map is not None:
            # restrict to files found in the log
            target_files = list(error_map.keys())
        else:
            scan_root = Path(args.path).resolve() if args.path else project_root / "src"
            target_files = list(scan_root.rglob("*.py"))

    wall_start = time.perf_counter()

    # -- Phase 1: Survey -----------------------------------------------------
    total_files = len(target_files)
    print(f"\n{'=' * 64}")
    if error_map is not None:
        logged_files = len(error_map)
        logged_lines = sum(len(s) for s in error_map.values())
        print(f"  Phase 1 - Survey: restricting to {logged_files} file(s) from error log ({logged_lines} lines) ")
    else:
        print(f"  Phase 1 - Survey: {total_files} Python file(s) in scope")
    print(f"{'=' * 64}")

    broken: list[tuple[Path, SyntaxError]] = []
    for idx, p in enumerate(target_files, 1):
        err = _compile_check(p)
        if err is not None:
            broken.append((p, err))
            if args.verbose:
                rel = p.relative_to(project_root)
                print(f"  [{idx:5d}/{total_files}] BROKEN  line {err.lineno:4d}: {err.msg}")
                print(f"             {rel}")
        elif args.verbose and total_files <= 200:
            # Only show OK lines when the set is small enough to be readable.
            rel = p.relative_to(project_root)
            print(f"  [{idx:5d}/{total_files}] ok      {rel}")
        elif idx % 500 == 0 or idx == total_files:
            pct = idx / total_files * 100
            print(f"  scanned {idx}/{total_files} ({pct:.0f}%)  -  {len(broken)} broken so far ...")

    scan_elapsed = time.perf_counter() - wall_start
    print(f"\n  Scan complete in {scan_elapsed:.2f}s - {len(broken)}/{total_files} file(s) broken.")

    if not broken:
        print("\n  Nothing to fix. [OK]")
        return 0

    # -- Phase 2: Repair ------------------------------------------------------
    print(f"\n{'=' * 64}")
    print(f"  Phase 2 - Repair: {len(broken)} broken file(s)")
    print(f"{'=' * 64}")

    fixed_count = 0
    still_broken: list[Path] = []
    total_line_changes = 0
    partial_count = 0

    for file_idx, (path, original_err) in enumerate(broken, 1):
        focus_lines_for_file: set[int] | None = None
        if error_map is not None:
            focus_lines_for_file = error_map.get(path.resolve())
        rel = path.relative_to(project_root)
        file_start = time.perf_counter()

        print(f"\n  [{file_idx:3d}/{len(broken)}] {rel}")
        print(f"         original error: line {original_err.lineno} - {original_err.msg}")
        if focus_lines_for_file:
            fl = sorted(focus_lines_for_file)
            print(f"         focus lines from log: {fl}")

        if args.verbose:
            print(f"         max passes: {args.max_passes}")

        result = repair_file(
            path,
            max_passes=args.max_passes,
            verbose=args.verbose,
            focus_lines=focus_lines_for_file,
        )
        changes, is_valid, new_lines = result
        file_elapsed = time.perf_counter() - file_start

        total_line_changes += changes

        if is_valid:
            fixed_count += 1
            if not args.dry_run:
                new_source = "".join(new_lines)
                # Preserve original EOL style
                original_source = path.read_text(encoding="utf-8", errors="replace")
                if "\r\n" in original_source and "\r\n" not in new_source:
                    new_source = new_source.replace("\n", "\r\n")
                path.write_text(new_source, encoding="utf-8")
            status = "FIXED" if not args.dry_run else "WOULD FIX"
            print(f"         [{status}]  {changes} line(s) adjusted  ({file_elapsed * 1000:.0f} ms)")
        else:
            still_broken.append(path)
            # Re-read the file for updated error position (dry-run: use in-memory lines).
            if args.dry_run:
                remaining_err = _compile_check_lines(new_lines)
            else:
                remaining_err = _compile_check(path)
            line_info = f"line {remaining_err.lineno}" if remaining_err else "?"
            err_msg = remaining_err.msg if remaining_err else "unknown"
            if changes > 0:
                partial_count += 1
                status = "PARTIAL"
            else:
                status = "UNCHANGED"
            print(
                f"         [{status}]  {changes} line(s) adjusted  "
                f"still broken at {line_info}: {err_msg}  ({file_elapsed * 1000:.0f} ms)"
            )

    # -- Phase 3: Summary -----------------------------------------------------
    total_elapsed = time.perf_counter() - wall_start
    print(f"\n{'=' * 64}")
    print("  Phase 3 - Summary")
    print(f"{'=' * 64}")
    print(f"  Files scanned:       {total_files}")
    print(f"  Files with errors:   {len(broken)}")
    print(f"  Files fully fixed:   {fixed_count}")
    print(f"  Files partially fixed: {partial_count}")
    print(f"  Files still broken:  {len(still_broken)}")
    print(f"  Lines adjusted:      {total_line_changes}")
    print(f"  Mode:                {'DRY RUN (no writes)' if args.dry_run else 'LIVE (files updated)'}")
    print(f"  Total time:          {total_elapsed:.2f}s")
    if still_broken:
        print(f"\n  Remaining failures ({len(still_broken)}):")
        for p in still_broken:
            err = _compile_check(p)
            loc = f"  line {err.lineno}: {err.msg}" if err else ""
            print(f"    {p.relative_to(project_root)}{loc}")
    print(f"{'=' * 64}\n")
    return 0 if not still_broken else 1


if __name__ == "__main__":
    sys.exit(main())
