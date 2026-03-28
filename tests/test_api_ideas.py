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
"""RED tests for ideas API ingestion, filtering, sorting, and resilience.

prj0000093 - projectmanager-ideas-autosync.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app import app

_CLIENT = TestClient(app, raise_server_exceptions=False)
_ROOT = Path(__file__).resolve().parents[1]
_IDEAS_DIR = _ROOT / "docs" / "project" / "ideas"
_PROJECTS_PATH = _ROOT / "data" / "projects.json"
_PLANNED_MAPPING_PATTERN = re.compile(r"^Planned project mapping:\s*(.+)$", re.IGNORECASE)
_PROJECT_ID_PATTERN = re.compile(r"prj\d{7}", re.IGNORECASE)
_IDEA_ID_PATTERN = re.compile(r"(idea\d{6})", re.IGNORECASE)


def _idea_files() -> list[Path]:
    """Return the repository idea markdown corpus in deterministic order.

    Returns:
        list[Path]: Sorted markdown files from docs/project/ideas.

    """
    return sorted(_IDEAS_DIR.glob("idea*.md"))


def _extract_idea_id(idea_file: Path) -> str:
    """Extract the canonical idea ID from an idea markdown filename.

    Args:
        idea_file: Markdown file path in docs/project/ideas.

    Returns:
        str: Canonical lower-case idea ID, e.g. ``idea000123``.

    Raises:
        AssertionError: If the file stem does not contain a valid idea ID.

    """
    match = _IDEA_ID_PATTERN.search(idea_file.stem)
    assert match is not None, f"Idea filename must include ideaNNNNNN: {idea_file.name}"
    return match.group(1).lower()


def _mapped_project_ids(idea_file: Path) -> list[str]:
    """Extract mapped project IDs from an idea file.

    Args:
        idea_file: Markdown file path.

    Returns:
        list[str]: Unique project IDs in first-seen order.

    """
    text = idea_file.read_text(encoding="utf-8")
    mapping_line = ""
    for raw_line in text.splitlines():
        match = _PLANNED_MAPPING_PATTERN.match(raw_line.strip())
        if match is not None:
            mapping_line = match.group(1).strip()
            break
    if not mapping_line or mapping_line.lower() == "none yet":
        return []

    seen: set[str] = set()
    unique: list[str] = []
    for token in _PROJECT_ID_PATTERN.findall(mapping_line):
        project_id = token.lower()
        if project_id not in seen:
            seen.add(project_id)
            unique.append(project_id)
    return unique


def _project_lane_map() -> dict[str, str]:
    """Load project lanes keyed by lower-case project ID.

    Returns:
        dict[str, str]: Mapping of project ID to lane value.

    """
    projects = json.loads(_PROJECTS_PATH.read_text(encoding="utf-8"))
    return {
        str(item.get("id", "")).lower(): str(item.get("lane", ""))
        for item in projects
        if item.get("id")
    }


def _expected_ids_for_implemented_exclude(mode: str) -> set[str]:
    """Compute expected IDs for ``implemented=exclude`` semantics.

    Args:
        mode: Implemented mode value.

    Returns:
        set[str]: Expected idea IDs that should remain visible.

    """
    lane_map = _project_lane_map()
    if mode == "released_only":
        implemented_lanes = {"released"}
    else:
        implemented_lanes = {"discovery", "design", "in sprint", "review", "released"}

    visible_ids: set[str] = set()
    for idea_file in _idea_files():
        mapped = _mapped_project_ids(idea_file)
        implemented = any(lane_map.get(project_id, "").lower() in implemented_lanes for project_id in mapped)
        if not implemented:
            visible_ids.add(_extract_idea_id(idea_file))
    return visible_ids


def test_api_ideas_returns_ideas_loaded_from_docs_project_ideas() -> None:
    """Return all repository idea files when ``implemented=include`` is used.

    This verifies endpoint ingestion uses docs/project/ideas as source of truth.
    """
    response = _CLIENT.get("/api/ideas", params={"implemented": "include"})

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)

    expected_ids = {_extract_idea_id(path) for path in _idea_files()}
    returned_ids = {str(item["idea_id"]).lower() for item in payload}
    assert returned_ids == expected_ids
    assert all(str(item["source_path"]).replace("\\", "/").startswith("docs/project/ideas/") for item in payload)


def test_implemented_false_excludes_ideas_mapped_to_active_or_released_lanes() -> None:
    """Exclude implemented ideas for default active-or-released semantics."""
    response = _CLIENT.get(
        "/api/ideas",
        params={
            "implemented": "exclude",
            "implemented_mode": "active_or_released",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)

    expected_ids = _expected_ids_for_implemented_exclude(mode="active_or_released")
    returned_ids = {str(item["idea_id"]).lower() for item in payload}
    assert returned_ids == expected_ids


def test_implemented_mode_released_only_excludes_released_lanes_only() -> None:
    """Exclude only released-lane mapped ideas when mode is ``released_only``."""
    response = _CLIENT.get(
        "/api/ideas",
        params={
            "implemented": "exclude",
            "implemented_mode": "released_only",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)

    expected_ids = _expected_ids_for_implemented_exclude(mode="released_only")
    returned_ids = {str(item["idea_id"]).lower() for item in payload}
    assert returned_ids == expected_ids


def test_rank_sort_is_stable_with_idea_id_tie_break() -> None:
    """Sort by rank and apply deterministic tie-break using idea_id.

    The endpoint contract is expected to support sort=rank and stable sorting.
    """
    response = _CLIENT.get(
        "/api/ideas",
        params={
            "implemented": "include",
            "sort": "rank",
            "order": "asc",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)

    sort_keys: list[tuple[int, str]] = []
    for item in payload:
        rank_value = item.get("rank")
        rank = int(rank_value) if rank_value is not None else 10_000_000
        sort_keys.append((rank, str(item["idea_id"]).lower()))

    assert sort_keys == sorted(sort_keys)


def test_malformed_idea_file_does_not_crash_endpoint() -> None:
    """Skip malformed idea files instead of failing the entire endpoint response."""
    malformed_path = _IDEAS_DIR / "idea999998-malformed-red-test.md"
    malformed_path.write_bytes(b"\x80\x81\x82\xff")
    try:
        response = _CLIENT.get("/api/ideas", params={"implemented": "include"})
    finally:
        malformed_path.unlink(missing_ok=True)

    assert response.status_code == 200
    payload = response.json()
    assert isinstance(payload, list)
    returned_ids = {str(item["idea_id"]).lower() for item in payload}
    assert "idea999998" not in returned_ids


def test_patch_idea_updates_title_summary_and_mapping() -> None:
    """PATCH /api/ideas/{idea_id} updates markdown-backed fields."""
    temp_idea = _IDEAS_DIR / "idea999997-patch-red-test.md"
    temp_idea.write_text(
        "\n".join(
            [
                "# Temporary patch idea",
                "",
                "## Idea Summary",
                "Initial summary.",
                "",
                "Planned project mapping: none yet",
                "",
            ]
        ),
        encoding="utf-8",
    )

    try:
        response = _CLIENT.patch(
            "/api/ideas/idea999997",
            json={
                "title": "Updated patch idea title",
                "summary": "Updated summary line",
                "mapped_project_ids": ["prj0000094"],
            },
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["idea_id"] == "idea999997"
        assert payload["title"] == "Updated patch idea title"
        assert payload["summary"] == "Updated summary line"
        assert payload["mapped_project_ids"] == ["prj0000094"]

        updated_text = temp_idea.read_text(encoding="utf-8")
        assert "# Updated patch idea title" in updated_text
        assert "## Idea Summary" in updated_text
        assert "Updated summary line" in updated_text
        assert "Planned project mapping: prj0000094" in updated_text
    finally:
        temp_idea.unlink(missing_ok=True)
