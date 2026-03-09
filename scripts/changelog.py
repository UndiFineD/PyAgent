#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import subprocess
from pathlib import Path


def generate_entry() -> str:
    """Produce a changelog entry from git history since last tag."""
    lines = subprocess.check_output([
        "git",
        "log",
        "--oneline",
        "--no-merges",
        r"--grep=^feat\|^fix",
    ], encoding="utf-8").splitlines()

    if not lines:
        return ""  # nothing to add

    added = []
    changed = []
    fixed = []
    for line in lines:
        if line.startswith("feat"):
            added.append("- " + line)
        elif line.startswith("fix"):
            fixed.append("- " + line)
        else:
            changed.append("- " + line)

    parts = []
    if added:
        parts.append("### Added\n" + "\n".join(added))
    if changed:
        parts.append("### Changed\n" + "\n".join(changed))
    if fixed:
        parts.append("### Fixed\n" + "\n".join(fixed))

    return "\n".join(parts)


def main() -> None:
    entry = generate_entry()
    if not entry:
        print("No changes detected.")
        return
    path = Path("docs/release_notes_template.md")
    text = path.read_text(encoding="utf-8")
    new_text = text.replace("## [Unreleased]", "## [Unreleased]\n\n" + entry)
    path.write_text(new_text, encoding="utf-8")
    print("Changelog updated.")


if __name__ == "__main__":
    main()
