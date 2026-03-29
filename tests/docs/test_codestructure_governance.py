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

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CODESTRUCTURE_PATH = REPO_ROOT / ".github" / "agents" / "data" / "codestructure.md"


def _read_codestructure_text() -> str:
    """Read canonical code structure index text.

    Returns:
        The UTF-8 decoded contents of the codestructure index file.

    """
    return CODESTRUCTURE_PATH.read_text(encoding="utf-8")


def _data_rows(text: str) -> list[tuple[str, str, str]]:
    """Parse markdown table rows from the canonical index table.

    Args:
        text: Full markdown contents of the codestructure index file.

    Returns:
        A list of tuples in the order (file, line, code).

    """
    rows: list[tuple[str, str, str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        if line == "| file | line | code |" or line.startswith("|---"):
            continue

        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 3:
            continue
        rows.append((parts[0], parts[1], parts[2]))
    return rows


def test_codestructure_file_exists_at_canonical_path() -> None:
    """Require codestructure index at the canonical governance location."""
    assert CODESTRUCTURE_PATH.exists()


def test_codestructure_has_required_table_schema_and_integer_line_values() -> None:
    """Require table schema header and integer line values for all index rows."""
    text = _read_codestructure_text()
    assert "| file | line | code |" in text

    rows = _data_rows(text)
    assert rows, "codestructure index must contain at least one data row"
    for file_path, line_value, code_text in rows:
        assert file_path
        assert line_value.isdigit()
        assert code_text
