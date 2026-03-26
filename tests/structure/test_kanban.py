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
"""Structural tests for data/projects.json and docs/project/kanban.md.

Validates prj0000052 project-management deliverables: the machine-readable
project registry (T1) and the 7-lane Kanban board (T2).

Tests are TDD-style (red phase): written before the files exist.
Content-dependent tests skip gracefully until the files are present and
contain the expected marker.  Only the two existence tests fail in the red
phase.  Acceptance criteria: AC-01 (projects.json) and AC-02 (kanban.md).
"""

import json
import re
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
_PROJECTS_PATH = REPO_ROOT / "data" / "projects.json"
_KANBAN_PATH = REPO_ROOT / "docs" / "project" / "kanban.md"

# ---------------------------------------------------------------------------
# Load files at module import time (same pattern as test_readme.py)
# ---------------------------------------------------------------------------

try:
    _projects_data = json.loads(_PROJECTS_PATH.read_text(encoding="utf-8"))
except (FileNotFoundError, json.JSONDecodeError):
    _projects_data = None

try:
    _kanban_content = _KANBAN_PATH.read_text(encoding="utf-8")
    _kanban_lines = _kanban_content.splitlines()
except FileNotFoundError:
    _kanban_content = ""
    _kanban_lines = []

# ---------------------------------------------------------------------------
# Sentinels
# _PROJECTS_MISSING — True while data/projects.json does not yet exist
# _KANBAN_MISSING   — True while kanban.md does not exist or lacks the
#                     canonical H1 "# PyAgent Project Kanban Board"
# ---------------------------------------------------------------------------

_PROJECTS_MISSING = not _PROJECTS_PATH.exists()

_KANBAN_MISSING = (
    not _KANBAN_PATH.exists()
    or not _kanban_lines
    or _kanban_lines[0].strip() != "# PyAgent Project Kanban Board"
)

_SKIP_PROJECTS = pytest.mark.skipif(
    _PROJECTS_MISSING,
    reason="data/projects.json not yet created (awaiting @6code)",
)
_SKIP_KANBAN = pytest.mark.skipif(
    _KANBAN_MISSING,
    reason="docs/project/kanban.md not yet created (awaiting @6code)",
)

# ---------------------------------------------------------------------------
# Domain constants
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = {
    "id", "name", "lane", "summary", "branch", "pr",
    "priority", "budget_tier", "tags", "created", "updated",
}

VALID_LANES = {
    "Ideas", "Discovery", "Design",
    "In Sprint", "Review", "Released", "Archived",
}

VALID_PRIORITIES = {"P1", "P2", "P3", "P4"}

VALID_BUDGET_TIERS = {"XS", "S", "M", "L", "XL", "unknown"}

# All 7 lane H2s plus Summary Metrics — parametrized in test_kanban_required_h2s
KANBAN_REQUIRED_H2S = [
    "## Ideas",
    "## Discovery",
    "## Design",
    "## In Sprint",
    "## Review",
    "## Released",
    "## Archived",
    "## Summary Metrics",
]


# ===========================================================================
# FILE 1:  data/projects.json
# ===========================================================================


def test_projects_json_exists() -> None:
    """data/projects.json must exist at the repo root.

    No skip guard — this test is the TDD red gate for T1 and intentionally
    fails until @6code creates the file.
    """
    assert _PROJECTS_PATH.exists(), (
        f"data/projects.json not found at {_PROJECTS_PATH}. "
        "Run @6code to implement T1."
    )


@_SKIP_PROJECTS
def test_projects_json_valid() -> None:
    """data/projects.json must parse as a valid JSON array without error."""
    assert _projects_data is not None, (
        "data/projects.json failed to parse as valid JSON"
    )
    assert isinstance(_projects_data, list), (
        f"Expected a JSON array at top level, got {type(_projects_data).__name__}"
    )


@_SKIP_PROJECTS
def test_projects_json_entry_count() -> None:
    """data/projects.json must contain exactly 88 entries.

    Breakdown: prj0000001–prj0000088 (88 unique entries; duplicates removed).
    """
    assert _projects_data is not None
    assert len(_projects_data) == 88, (
        f"Expected 88 project entries, got {len(_projects_data)}"
    )


@_SKIP_PROJECTS
def test_projects_json_required_fields() -> None:
    """Every entry in data/projects.json must have all 11 required fields.

    Required: id, name, lane, summary, branch, pr, priority, budget_tier,
              tags, created, updated.
    """
    assert _projects_data is not None
    failures: list[str] = []
    for entry in _projects_data:
        missing = REQUIRED_FIELDS - set(entry.keys())
        if missing:
            failures.append(
                f"  {entry.get('id', '<unknown>')!r}: missing {sorted(missing)}"
            )
    assert not failures, (
        f"{len(failures)} entries have missing required fields:\n"
        + "\n".join(failures)
    )


@_SKIP_PROJECTS
def test_projects_json_lane_values() -> None:
    """All 'lane' values in data/projects.json must be one of the 7 valid lanes."""
    assert _projects_data is not None
    invalid: list[str] = []
    for entry in _projects_data:
        lane = entry.get("lane")
        if lane not in VALID_LANES:
            invalid.append(
                f"  {entry.get('id', '<unknown>')!r}: lane={lane!r}"
            )
    assert not invalid, (
        f"{len(invalid)} entries have invalid lane values "
        f"(valid: {sorted(VALID_LANES)}):\n" + "\n".join(invalid)
    )


@_SKIP_PROJECTS
def test_projects_json_priority_values() -> None:
    """All 'priority' values in data/projects.json must be P1, P2, P3, or P4."""
    assert _projects_data is not None
    invalid: list[str] = []
    for entry in _projects_data:
        priority = entry.get("priority")
        if priority not in VALID_PRIORITIES:
            invalid.append(
                f"  {entry.get('id', '<unknown>')!r}: priority={priority!r}"
            )
    assert not invalid, (
        f"{len(invalid)} entries have invalid priority values "
        f"(valid: {sorted(VALID_PRIORITIES)}):\n" + "\n".join(invalid)
    )


@_SKIP_PROJECTS
def test_projects_json_budget_tier_values() -> None:
    """All 'budget_tier' values must be one of XS, S, M, L, XL, unknown."""
    assert _projects_data is not None
    invalid: list[str] = []
    for entry in _projects_data:
        budget_tier = entry.get("budget_tier")
        if budget_tier not in VALID_BUDGET_TIERS:
            invalid.append(
                f"  {entry.get('id', '<unknown>')!r}: budget_tier={budget_tier!r}"
            )
    assert not invalid, (
        f"{len(invalid)} entries have invalid budget_tier values "
        f"(valid: {sorted(VALID_BUDGET_TIERS)}):\n" + "\n".join(invalid)
    )


@_SKIP_PROJECTS
def test_projects_json_prj0000052_present() -> None:
    """data/projects.json must contain an entry with id == 'prj0000052'."""
    assert _projects_data is not None
    ids = {entry.get("id") for entry in _projects_data}
    assert "prj0000052" in ids, (
        "No entry with id 'prj0000052' found in data/projects.json. "
        "This project (project-management) must register itself."
    )


# ===========================================================================
# FILE 2:  docs/project/kanban.md
# ===========================================================================


def test_kanban_exists() -> None:
    """kanban.md must exist and open with '# PyAgent Project Kanban Board'.

    No skip guard — this test is the TDD red gate for T2 and intentionally
    fails until @6code creates the file.
    """
    assert _KANBAN_PATH.exists(), (
        f"docs/project/kanban.md not found at {_KANBAN_PATH}. "
        "Run @6code to implement T2."
    )
    assert _kanban_lines, "docs/project/kanban.md is empty"
    assert _kanban_lines[0].strip() == "# PyAgent Project Kanban Board", (
        f"Expected first line '# PyAgent Project Kanban Board', "
        f"got: {_kanban_lines[0]!r}"
    )


@_SKIP_KANBAN
@pytest.mark.parametrize("heading", KANBAN_REQUIRED_H2S)
def test_kanban_required_h2s(heading: str) -> None:
    """kanban.md must contain all 7 lane H2 headings and ## Summary Metrics."""
    headings_in_file = {line.strip() for line in _kanban_lines if line.startswith("## ")}
    assert heading in headings_in_file, (
        f"Required heading {heading!r} not found in kanban.md. "
        f"Present H2s: {sorted(headings_in_file)}"
    )


@_SKIP_KANBAN
def test_kanban_total_rows() -> None:
    r"""kanban.md must contain exactly 88 project data rows.

    A data row is any line matching r'^\|\s*prj\d{7}'.
    """
    pattern = re.compile(r"^\|\s*prj\d{7}")
    data_rows = [line for line in _kanban_lines if pattern.match(line)]
    assert len(data_rows) == 88, (
        f"Expected 88 project rows in kanban.md, found {len(data_rows)}"
    )


@_SKIP_KANBAN
def test_kanban_prj0000052_present() -> None:
    """'prj0000052' must appear somewhere in the kanban.md content."""
    assert "prj0000052" in _kanban_content, (
        "Project ID 'prj0000052' not found in docs/project/kanban.md"
    )


@_SKIP_KANBAN
def test_kanban_no_todo_fixme() -> None:
    """kanban.md must contain no TODO, FIXME, or TBD placeholder strings."""
    markers = ("TODO", "FIXME", "TBD")
    for i, line in enumerate(_kanban_lines, start=1):
        upper = line.upper()
        for marker in markers:
            assert marker not in upper, (
                f"Forbidden placeholder {marker!r} found in kanban.md "
                f"at line {i}: {line!r}"
            )
