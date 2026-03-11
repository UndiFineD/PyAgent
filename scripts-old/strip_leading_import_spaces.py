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

"""Strip stray single-space indents before import statements.

A recurring formatting bug left a leading space before some module-level
imports.  Python treats these as an unexpected indent when the file is
compiled at module scope, causing pytest collection errors.

This script scans all .py files under the given path (default "src/") and
removes a single leading space on lines where the stripped text begins with
"import " or "from ".  Only lines with exactly one leading space are
modified, avoiding disruption of intentionally indented nested imports
inside functions/methods.

Usage::

    python scripts/strip_leading_import_spaces.py [--path PATH] [--dry-run]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

IMPORT_RE = re.compile(r"^( )(?:(from\s+\S)|(import\s+\S))")


def fix_file(path: Path, dry_run: bool = False, verbose: bool = False) -> bool:
    """Return True if file was modified."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    changed = False
    out_lines: list[str] = []
    for line in lines:
        m = IMPORT_RE.match(line)
        if m:
            # Only remove single space; preserve additional indentation
            new_line = line[1:]
            if verbose:
                print(f"Fixing leading space in {path}:{len(out_lines)+1}")
            out_lines.append(new_line)
            changed = True
        else:
            out_lines.append(line)
    if changed and not dry_run:
        path.write_text("".join(out_lines), encoding="utf-8")
    return changed


def main() -> None:
    """Scan .py files and fix leading spaces before imports."""
    p = argparse.ArgumentParser(description="Strip stray leading spaces before imports")
    p.add_argument("--path", "-p", default="src", help="root directory to scan")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()
    root = Path(args.path)
    files = list(root.rglob("*.py"))
    modified = 0
    for f in files:
        if fix_file(f, dry_run=args.dry_run, verbose=args.verbose):
            modified += 1
    print(f"Processed {len(files)} files; modified {modified}.")


if __name__ == "__main__":
    main()
