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
"""Structural tests for docs/architecture/ naming convention.

prj0000074 — workspace-meta-improvements (AC-3).

Rules enforced:
- All top-level .md files in docs/architecture/ must match r'^\\d.*\\.md$'
- No file named todolist.md or matching *.generated.md may exist
- Total count of top-level .md files must be <= 8
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ARCH_DIR = REPO_ROOT / "docs" / "architecture"

_NUMBERED_RE = re.compile(r"^\d.*\.md$")


def _top_level_md_files() -> list[Path]:
    """Return all .md files directly in docs/architecture/ (non-recursive)."""
    return [p for p in ARCH_DIR.iterdir() if p.is_file() and p.suffix == ".md"]


def test_architecture_dir_exists() -> None:
    """docs/architecture/ directory must exist."""
    assert ARCH_DIR.is_dir(), f"Expected directory at {ARCH_DIR}"


def test_no_md_files_exceed_eight() -> None:
    """At most 8 top-level .md files are allowed in docs/architecture/."""
    files = _top_level_md_files()
    names = [f.name for f in files]
    assert len(files) <= 8, f"Expected ≤ 8 top-level .md files in docs/architecture/, found {len(files)}: {names}"


def test_all_md_files_have_numbered_names() -> None:
    """Every top-level .md file in docs/architecture/ must start with a digit."""
    bad = [f.name for f in _top_level_md_files() if not _NUMBERED_RE.match(f.name)]
    assert not bad, (
        f"The following docs/architecture/ files do not match the numbered naming convention (^\\d.*\\.md$): {bad}"
    )


def test_no_todolist_md() -> None:
    """todolist.md must not exist in docs/architecture/."""
    assert not (ARCH_DIR / "todolist.md").exists(), "docs/architecture/todolist.md must be removed (stale file)"


def test_no_generated_md() -> None:
    """No *.generated.md file may exist in docs/architecture/."""
    generated = [f.name for f in _top_level_md_files() if ".generated." in f.name]
    assert not generated, f"Generated artefacts must not be checked in: {generated}"


def test_0overview_exists() -> None:
    """docs/architecture/0overview.md must exist (top-level overview)."""
    assert (ARCH_DIR / "0overview.md").exists(), "docs/architecture/0overview.md is missing — run restructure"


def test_1agents_exists() -> None:
    """docs/architecture/1agents.md must exist (agent system reference)."""
    assert (ARCH_DIR / "1agents.md").exists(), "docs/architecture/1agents.md is missing — run restructure"
