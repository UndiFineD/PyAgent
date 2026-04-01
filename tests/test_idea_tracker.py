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

from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_idea_tracker_module():
    """Load scripts/IdeaTracker.py as module for direct function testing."""
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "IdeaTracker.py"
    spec = importlib.util.spec_from_file_location("IdeaTracker", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_build_tracker_payload_includes_active_and_archived_ideas(tmp_path: Path) -> None:
    """Tracker payload must index both active and archived idea directories."""
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    (ideas_dir / "idea000111-active-sample.md").write_text(
        "\n".join(
            [
                "# idea-111 - active sample",
                "",
                "Planned project mapping: prj0000111",
                "",
                "## Source references",
                "- docs/sample.md",
            ]
        ),
        encoding="utf-8",
    )

    (archive_dir / "idea000112-archived-sample.md").write_text(
        "\n".join(
            [
                "# idea-112 - archived sample",
                "",
                "Planned project mapping: none yet",
                "",
                "## Source references",
                "- docs/archive-sample.md",
            ]
        ),
        encoding="utf-8",
    )

    module = _load_idea_tracker_module()
    payload = module.build_tracker_payload(tmp_path)

    assert payload["summary"]["total"] == 2
    assert payload["summary"]["active"] == 1
    assert payload["summary"]["archived"] == 1

    by_id = {record["idea_id"]: record for record in payload["ideas"]}
    assert by_id["idea000111"]["status"] == "active"
    assert by_id["idea000112"]["status"] == "archived"
    assert by_id["idea000111"]["planned_project_ids"] == ["prj0000111"]
