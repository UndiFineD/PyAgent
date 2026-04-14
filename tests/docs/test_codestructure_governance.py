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

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CODESTRUCTURE_PATH = REPO_ROOT / ".github" / "agents" / "data" / "codestructure.md"
CODESTRUCTURE_DATA_DIR = REPO_ROOT / ".github" / "agents" / "data"
REQUIRED_SPLIT_FILES = (
    "backend.codestructure.md",
    "rust_core.codestructure.md",
    "scripts.codestructure.md",
    "src.codestructure.md",
    "tests.codestructure.md",
    "web.codestructure.md",
    "other.codestructure.md",
)
ROW_PATTERN = re.compile(r"^-\s*(\d+)\s*:\s*(.+)\s*$")


def _read_codestructure_text() -> str:
    """Read canonical code structure index text.

    Returns:
        The UTF-8 decoded contents of the codestructure index file.

    """
    return CODESTRUCTURE_PATH.read_text(encoding="utf-8")


def _parse_data_rows(text: str) -> list[tuple[str, int, str]]:
    """Parse grouped markdown rows from a code-structure markdown file.

    Args:
        text: Full markdown contents of a code-structure index file.

    Returns:
        A list of tuples in the order (file, line, code).

    """
    rows: list[tuple[str, int, str]] = []
    current_file = ""
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            heading = line[3:].strip()
            current_file = "" if heading.lower() in {"split domain files", "other"} else heading
            continue

        if line.startswith("### "):
            current_file = line[4:].strip()
            continue

        if not line.startswith("- "):
            continue

        match = ROW_PATTERN.match(line)
        if not match or not current_file:
            continue
        rows.append((current_file, int(match.group(1)), match.group(2).strip()))
    return rows


def _all_codestructure_paths() -> list[Path]:
    """Return canonical and required split code-structure file paths.

    Returns:
        A list containing the canonical manifest path followed by split index paths.

    """
    return [CODESTRUCTURE_PATH, *[CODESTRUCTURE_DATA_DIR / name for name in REQUIRED_SPLIT_FILES]]


def test_codestructure_file_exists_at_canonical_path() -> None:
    """Require codestructure index at the canonical governance location."""
    assert CODESTRUCTURE_PATH.exists()


def test_required_codestructure_split_files_exist() -> None:
    """Require all mandated split code-structure files at canonical data location."""
    for split_name in REQUIRED_SPLIT_FILES:
        assert (CODESTRUCTURE_DATA_DIR / split_name).exists(), split_name


def test_codestructure_rows_across_manifest_and_splits_are_valid() -> None:
    """Require non-empty, well-formed grouped rows across all code-structure files."""
    rows: list[tuple[str, int, str]] = []
    for path in _all_codestructure_paths():
        rows.extend(_parse_data_rows(path.read_text(encoding="utf-8")))

    assert rows, "code-structure index files must contain at least one data row"
    for file_path, line_value, code_text in rows:
        assert file_path
        assert isinstance(line_value, int)
        assert line_value > 0
        assert code_text
