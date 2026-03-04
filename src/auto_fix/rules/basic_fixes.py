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

"""Conservative file transformations that address common pytest import and
indentation problems as well as other syntactic nuisances.

This rule mirrors the behavior of ``scripts/auto_fix_pytest_issues.py`` but
is expressed as an engine rule so that the CLI and other consumers can
reuse it programmatically.

The check function accepts the file content as a single string and returns
an empty list if no changes are required or a single-fix list containing the
updated text.
"""

 from __future__ import annotations

import re
from typing import List

 from auto_fix.rule_engine import Fix


# --- helper functions copied/adapted from the older script ------------------

def normalize_text(text: str) -> str:
    """Remove a couple of characters that often trip the parser."""
    return text.replace("\u00A0", " ")


def safe_wrap_main(lines: List[str]) -> List[str]:
    """If the file ends with an unguarded call to main(), wrap it in a guard."""
    if not lines:
        return lines

    last_idx = len(lines) - 1
    while last_idx >= 0 and not lines[last_idx].strip():
        last_idx -= 1

    if last_idx < 0:
        return lines

    tail = "".join(lines[max(0, last_idx - 8) :])
    if "if __name__" in tail:
        return lines

    if lines[last_idx].strip() == "main()":
        joined = "".join(lines)
        if re.search(r"def\s+main\s*\(", joined):
            new = lines[:last_idx]
            new.append("if __name__ == '__main__':\n")
            new.append("    main()\n")
            new.extend(lines[last_idx + 1 :])
            return new
    return lines


def dedent_imports(lines: List[str]) -> List[str]:
    """Dedent any import statements that are indented but not actually part of a block."""
    out: List[str] = []

    def prev_nonempty(idx: int) -> str | None:
        # look in the already-processed output first so that we respect
        # earlier dedents within the same pass
        for raw in reversed(out):
            if raw.strip():
                return raw
        # fall back to the original lines if nothing in out
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
            # never dedent when the previous statement is a TYPE_CHECKING block
            if prev_lstr is not None and prev_lstr.strip().startswith("if TYPE_CHECKING"):
                is_safe_prev = False
            else:
                is_safe_prev = (
                    prev is None
                    or (prev_str is not None and prev_str.endswith(")"))
                    or (prev_str is not None and prev_str.endswith(","))
                    or (prev_str is not None and prev_str.endswith("\\"))
                    or (prev_lstr is not None and prev_lstr.startswith("from "))
                    or (prev_lstr is not None and prev_lstr.startswith("import "))
                    or (prev_lstr is not None and prev_lstr.startswith("#"))
                )
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


def indent_imports_after_control(lines: List[str]) -> List[str]:
    """Indent imports that appear inside or immediately after a control block.

    The previous implementation only handled imports directly following a
    control statement.  In practice we often have a comment or even
    semantically-meaningful code before the stray ``import``; the fix should
    still apply as long as the import is logically part of the last control
    block.  We now treat ``if TYPE_CHECKING:`` as another control header so
    that any imports (or other lines) that were accidentally dedented are
    shoved back inside the block.
    """
    out: List[str] = list(lines)

    for i, line in enumerate(lines):
        m = re.match(r"^(\s*)(?:try|except|else|finally|if\s+TYPE_CHECKING)\s*:\s*$", line)
        if not m:
            continue

        control_indent = len(m.group(1))
        j = i + 1
        left_block = False

        while j < len(lines):
            nxt = lines[j]
            stripped = nxt.strip()
            nxt_indent = len(nxt) - len(nxt.lstrip())

            # skip blank/comment lines but keep left_block state
            if not stripped or stripped.startswith("#"):
                # if we've dedented already, don't clear left_block
                if nxt_indent <= control_indent:
                    left_block = True
                j += 1
                continue

            # detect leaving block when we encounter a line with indent <=
            # control level (i.e. dedent to top level).
            if nxt_indent <= control_indent:
                left_block = True

            # if we see an import and we're either still in the block or have
            # just left it, indent it to the block's body indentation
            if re.match(r"^(from|import)\s+", stripped):
                desired = control_indent + 4
                if nxt_indent < desired:
                    out[j] = " " * desired + stripped + ("\n" if nxt.endswith("\n") else "")
                j += 1
                continue

            # any other real code after we've left the block means we're done
            if left_block:
                break

            j += 1
    return out



def indent_after_type_checking(lines: List[str]) -> List[str]:
    """Ensure lines belonging under an ``if TYPE_CHECKING:`` header are indented.

    Only a narrow subset of statements are expected in these blocks (imports,
    type aliases, comments).  When the block has been accidentally flattened
    by previous transformations we conservatively indent those lines by one
    level.  Execution stops as soon as we see a line that looks like normal
    runtime code, to avoid pushing unrelated statements.
    """
    out: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if re.match(r"^\s*if\s+TYPE_CHECKING\s*:\s*$", line):
            base_indent = len(line) - len(line.lstrip())
            j = i + 1
            while j < len(lines):
                nxt = lines[j]
                stripped = nxt.strip()
                if not stripped:
                    out.append(nxt)
                    j += 1
                    continue
                # only indent lines that clearly belong in the TYPE_CHECKING
                # block: imports, simple assignments (aliases), or comments
                is_import = re.match(r"^(from|import)\s+", stripped)
                is_assignment = re.match(r"^[A-Za-z_]\w*\s*=", stripped)
                is_comment = stripped.startswith("#")
                if is_import or is_assignment or is_comment:
                    nxt_indent = len(nxt) - len(nxt.lstrip())
                    desired = base_indent + 4
                    if nxt_indent < desired:
                        out.append(" " * desired + stripped + ("\n" if nxt.endswith("\n") else ""))
                    else:
                        out.append(nxt)
                    j += 1
                    continue
                # anything else likely exits the TYPE_CHECKING block
                break
            i = j
            continue
        i += 1
    return out


def indent_after_header(lines: List[str]) -> List[str]:
    """Indent the first real statement following any block header.

    This catch-all rule helps repair files where a control or definition
    header (``def``, ``class``, ``if``, ``for``, etc.) is immediately
    followed by a non-indented line.  Pytest and the compiler often
    complain with ``IndentationError: expected an indented block`` in
    these situations.  We only adjust the *next non-blank, non-comment*
    line and leave existing indentation alone if it already exceeds the
    header level.  This keeps us conservative while fixing the common
    pattern discovered during the syntax audit.
    """
    out = list(lines)
    header_re = re.compile(r"^\s*(?:if|for|while|with|def|class|elif|else|try|except|finally)\b.*:\s*$")
    i = 0
    while i < len(lines):
        line = lines[i]
        if header_re.match(line):
            base_indent = len(line) - len(line.lstrip())
            # find next non-blank, non-comment line
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                nxt = lines[j]
                stripped = nxt.strip()
                if not stripped.startswith("#"):
                    nxt_indent = len(nxt) - len(nxt.lstrip())
                    # if it's dedented or at same level, indent it
                    if nxt_indent <= base_indent:
                        desired = base_indent + 4
                        out[j] = " " * desired + stripped + ("\n" if nxt.endswith("\n") else "")
            i = j
        else:
            i += 1
    return out

# ---------------------------------------------------------------------------

def check(content: str) -> list[dict]:
    """Apply basic syntactic cleanups to the file content, returning a single fix if any changes were made."""
    orig = content
    text = normalize_text(orig)
    lines = text.splitlines(keepends=True)

    # conservative top-of-file dedent for any imports within the first 50 lines
    # (but avoid touching imports that are clearly inside a conditional such as
    # ``if TYPE_CHECKING`` or other control-flow blocks).
    def prev_nonempty_before(idx: int) -> str | None:
        for j in range(idx - 1, -1, -1):
            raw = lines[j]
            if raw.strip():
                return raw
        return None

    for idx, line in enumerate(lines[:50]):
        if re.match(r"^\s+(from|import)\s+", line):
            prev = prev_nonempty_before(idx)
            if prev is not None and prev.strip().startswith("if TYPE_CHECKING"):
                continue
            # also avoid dedenting if prev line is indented (inside block)
            if prev is not None and (prev.startswith(" ") or prev.startswith("\t")):
                continue
            lines[idx] = line.lstrip()

    # apply transformations
    lines = dedent_imports(lines)
    lines = indent_imports_after_control(lines)
    lines = indent_after_type_checking(lines)
    lines = indent_after_header(lines)
    lines = safe_wrap_main(lines)

    new_text = "".join(lines)
    if new_text != orig:
        return [
            {
                "path": "",  # engine fills in
                "original": orig,
                "replacement": new_text,
                "description": "basic syntactic cleanups",
            }
        ]
    return []
