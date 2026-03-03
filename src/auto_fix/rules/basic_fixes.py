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
    out: List[str] = []

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
    out: List[str] = list(lines)
    i = 0
    while i < len(out) - 1:
        line = out[i]
        m = re.match(r"^(\s*)(try|except|else|finally)\s*:\s*$", line)
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


# ---------------------------------------------------------------------------

def check(content: str) -> list[dict]:
    orig = content
    text = normalize_text(orig)
    lines = text.splitlines(keepends=True)

    # conservative top-of-file dedent for any imports within the first 50 lines
    for idx, line in enumerate(lines[:50]):
        if re.match(r"^\s+(from|import)\s+", line):
            lines[idx] = line.lstrip()

    # apply transformations
    lines = dedent_imports(lines)
    lines = indent_imports_after_control(lines)
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
