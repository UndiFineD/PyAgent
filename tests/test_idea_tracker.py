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


def test_build_tracker_payload_adds_readiness_and_duplicate_candidates(tmp_path: Path) -> None:
    """Tracker payload should include readiness queues and duplicate candidate clustering."""
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    (ideas_dir / "idea000201-async-pipeline-gateway.md").write_text(
        "\n".join(
            [
                "# idea-201 - async pipeline gateway",
                "",
                "Planned project mapping: prj0000201",
                "",
                "## Idea summary",
                "Coordinate queue-first async execution.",
                "## Problem statement",
                "Current intake does not scale for high volume.",
                "## Why this matters now",
                "Idea volume is increasing sharply.",
                "## Detailed proposal",
                "Introduce a structured triage pipeline.",
                "## Scope suggestion",
                "Intake and triage only.",
                "## Requirements",
                "Deterministic scoring.",
                "## Dependencies and constraints",
                "Existing docs/project conventions.",
                "## Success metrics",
                "95% ideas with readiness score.",
                "## Validation commands",
                "- python scripts/IdeaTracker.py --output docs/project/ideatracker.json",
                "## Risks and mitigations",
                "- Misclassification risk.",
                "## Failure handling and rollback",
                "- Re-run with stricter thresholds.",
                "## Source references",
                "- docs/prompt/roadmap.txt",
            ]
        ),
        encoding="utf-8",
    )

    (ideas_dir / "idea000202-async-pipeline-triage.md").write_text(
        "\n".join(
            [
                "# idea-202 - async pipeline triage",
                "",
                "Planned project mapping: prj0000201",
                "",
                "## Idea summary",
                "Queue-based intake triage.",
                "## Problem statement",
                "Large batches need deterministic prioritization.",
                "## Why this matters now",
                "Manual triage cannot keep pace.",
                "## Detailed proposal",
                "Weighted scoring with readiness queues.",
                "## Scope suggestion",
                "Tracker and template upgrades.",
                "## Requirements",
                "Stable scoring and duplicate detection.",
                "## Dependencies and constraints",
                "Reuse existing project governance.",
                "## Success metrics",
                "<5% duplicate survivors in active queue.",
                "## Validation commands",
                "- python scripts/IdeaTracker.py --output docs/project/ideatracker.json",
                "## Risks and mitigations",
                "- False-positive duplicate detection.",
                "## Failure handling and rollback",
                "- Keep originals archived with lineage.",
                "## Source references",
                "- docs/prompt/roadmap.txt",
            ]
        ),
        encoding="utf-8",
    )

    module = _load_idea_tracker_module()
    payload = module.build_tracker_payload(tmp_path)

    assert payload["schema_version"] == 2
    assert payload["summary"]["readiness"]["ready"] >= 2
    assert "ready" in payload["queues"]

    by_id = {record["idea_id"]: record for record in payload["ideas"]}
    assert by_id["idea000201"]["template_completeness"] > 0.9
    assert by_id["idea000201"]["readiness_status"] == "ready"
    assert "priority_score" in by_id["idea000201"]["scoring"]

    merge_candidates = payload["duplicate_candidates"]["merge_candidates"]
    review_candidates = payload["duplicate_candidates"]["review_candidates"]
    candidate_pairs = {tuple(item["idea_ids"]) for item in merge_candidates + review_candidates}
    assert ("idea000202", "idea000201") in candidate_pairs or ("idea000201", "idea000202") in candidate_pairs


def test_build_tracker_payload_batch_window(tmp_path: Path) -> None:
    """Tracker should support offset/limit for high-volume batch processing."""
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    for idx in range(1, 6):
        (ideas_dir / f"idea00030{idx}-sample-{idx}.md").write_text(
            "\n".join(
                [
                    f"# idea-{300 + idx} - sample {idx}",
                    "",
                    "Planned project mapping: none yet",
                    "",
                    "## Problem statement",
                    "Sample problem.",
                    "## Success metrics",
                    "Sample metric.",
                    "## Validation commands",
                    "- pytest -q",
                    "## Risks and mitigations",
                    "- Sample risk",
                    "## Failure handling and rollback",
                    "- Sample rollback",
                    "## Source references",
                    "- docs/sample.md",
                ]
            ),
            encoding="utf-8",
        )

    module = _load_idea_tracker_module()
    payload = module.build_tracker_payload(tmp_path, offset=1, limit=2)

    assert payload["source"]["offset"] == 1
    assert payload["source"]["limit"] == 2
    assert payload["source"]["processed_total"] == 2
    assert payload["summary"]["total"] == 2
