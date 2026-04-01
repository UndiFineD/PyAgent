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
"""Structural tests for docs/project/kanban.json.

Validates prj0000052 project-management deliverables in the machine-readable
project registry in kanban.json.

Acceptance criteria: AC-01 (kanban.json projects).
"""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
_PROJECTS_PATH = REPO_ROOT / "docs" / "project" / "kanban.json"
_NEXTPROJECT_PATH = REPO_ROOT / "data" / "nextproject.md"

# ---------------------------------------------------------------------------
# Load files at module import time (same pattern as test_readme.py)
# ---------------------------------------------------------------------------

try:
    _projects_raw = json.loads(_PROJECTS_PATH.read_text(encoding="utf-8"))
    if isinstance(_projects_raw, list):
        _projects_data = _projects_raw
    elif isinstance(_projects_raw, dict) and isinstance(_projects_raw.get("projects"), list):
        _projects_data = _projects_raw["projects"]
    else:
        _projects_data = None
except (FileNotFoundError, json.JSONDecodeError):
    _projects_data = None

try:
    _nextproject_raw = _NEXTPROJECT_PATH.read_text(encoding="utf-8").strip()
except FileNotFoundError:
    _nextproject_raw = ""


def _expected_project_count() -> int | None:
    """Return expected project count inferred from data/nextproject.md.

    If nextproject marker is `prj0000092`, expected count is 91.
    Returns None when the marker is missing or malformed.
    """
    match = re.fullmatch(r"prj(\d{7})", _nextproject_raw)
    if not match:
        return None
    return int(match.group(1)) - 1


# ---------------------------------------------------------------------------
# Sentinels
# _PROJECTS_MISSING — True while docs/project/kanban.json does not yet exist
# ---------------------------------------------------------------------------

_PROJECTS_MISSING = not _PROJECTS_PATH.exists()

# ---------------------------------------------------------------------------
# Domain constants
# ---------------------------------------------------------------------------

REQUIRED_FIELDS = {
    "id",
    "name",
    "lane",
    "summary",
    "branch",
    "pr",
    "priority",
    "budget_tier",
    "tags",
    "created",
    "updated",
}

VALID_LANES = {
    "Ideas",
    "Discovery",
    "Design",
    "In Sprint",
    "Review",
    "Released",
    "Archived",
}

VALID_PRIORITIES = {"P1", "P2", "P3", "P4"}

VALID_BUDGET_TIERS = {"XS", "S", "M", "L", "XL", "unknown"}

# ===========================================================================
# FILE: docs/project/kanban.json (projects array)
# ===========================================================================


def test_projects_json_exists() -> None:
    """docs/project/kanban.json must exist at the repo root.

    No skip guard — this test is the TDD red gate for T1 and intentionally
    fails until @6code creates the file.
    """
    assert _PROJECTS_PATH.exists(), (
        f"docs/project/kanban.json not found at {_PROJECTS_PATH}. Run @6code to implement T1."
    )


def test_projects_json_valid() -> None:
    """kanban.json must expose a valid project list (array or envelope.projects)."""
    assert _projects_data is not None, "docs/project/kanban.json failed to expose a valid projects list"
    assert isinstance(_projects_data, list), f"Expected a JSON array at top level, got {type(_projects_data).__name__}"


def test_projects_json_entry_count() -> None:
    """kanban.json project entry count must align with nextproject marker.

    Expected count is derived from data/nextproject.md as marker_id - 1.
    """
    assert _projects_data is not None
    expected = _expected_project_count()
    assert expected is not None, "Could not derive expected project count from data/nextproject.md"
    assert len(_projects_data) == expected, f"Expected {expected} project entries, got {len(_projects_data)}"


def test_projects_json_required_fields() -> None:
    """Every project entry in kanban.json must have all 11 required fields.

    Required: id, name, lane, summary, branch, pr, priority, budget_tier,
              tags, created, updated.
    """
    assert _projects_data is not None
    failures: list[str] = []
    for entry in _projects_data:
        missing = REQUIRED_FIELDS - set(entry.keys())
        if missing:
            failures.append(f"  {entry.get('id', '<unknown>')!r}: missing {sorted(missing)}")
    assert not failures, f"{len(failures)} entries have missing required fields:\n" + "\n".join(failures)


def test_projects_json_lane_values() -> None:
    """All 'lane' values in kanban.json projects must be one of the 7 valid lanes."""
    assert _projects_data is not None
    invalid: list[str] = []
    for entry in _projects_data:
        lane = entry.get("lane")
        if lane not in VALID_LANES:
            invalid.append(f"  {entry.get('id', '<unknown>')!r}: lane={lane!r}")
    assert not invalid, (
        f"{len(invalid)} entries have invalid lane values (valid: {sorted(VALID_LANES)}):\n" + "\n".join(invalid)
    )


def test_projects_json_priority_values() -> None:
    """All 'priority' values in kanban.json projects must be P1, P2, P3, or P4."""
    assert _projects_data is not None
    invalid: list[str] = []
    for entry in _projects_data:
        priority = entry.get("priority")
        if priority not in VALID_PRIORITIES:
            invalid.append(f"  {entry.get('id', '<unknown>')!r}: priority={priority!r}")
    assert not invalid, (
        f"{len(invalid)} entries have invalid priority values "
        f"(valid: {sorted(VALID_PRIORITIES)}):\n" + "\n".join(invalid)
    )


def test_projects_json_budget_tier_values() -> None:
    """All 'budget_tier' values must be one of XS, S, M, L, XL, unknown."""
    assert _projects_data is not None
    invalid: list[str] = []
    for entry in _projects_data:
        budget_tier = entry.get("budget_tier")
        if budget_tier not in VALID_BUDGET_TIERS:
            invalid.append(f"  {entry.get('id', '<unknown>')!r}: budget_tier={budget_tier!r}")
    assert not invalid, (
        f"{len(invalid)} entries have invalid budget_tier values "
        f"(valid: {sorted(VALID_BUDGET_TIERS)}):\n" + "\n".join(invalid)
    )


def test_projects_json_prj0000052_present() -> None:
    """kanban.json projects must contain an entry with id == 'prj0000052'."""
    assert _projects_data is not None
    ids = {entry.get("id") for entry in _projects_data}
    assert "prj0000052" in ids, (
        "No entry with id 'prj0000052' found in docs/project/kanban.json projects. "
        "This project (project-management) must register itself."
    )
