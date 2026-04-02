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
import json
from pathlib import Path

from pytest import CaptureFixture


def _load_idea_tracker_module():
    """Load scripts/IdeaTracker.py as module for direct function testing."""
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "IdeaTracker.py"
    spec = importlib.util.spec_from_file_location("IdeaTracker", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _artifact_path(tmp_path: Path, file_name: str) -> Path:
    """Return the canonical artifact path under the temporary repo root.

    Args:
        tmp_path: Temporary repository root.
        file_name: Artifact file name.

    Returns:
        Absolute artifact path.

    """
    return tmp_path / "docs" / "project" / file_name


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


# ---------------------------------------------------------------------------
# Blocking-similarity and verbosity tests (prj0000114)
# ---------------------------------------------------------------------------

_FULL_SECTIONS = [
    "## Idea summary",
    "Quick summary.",
    "## Problem statement",
    "Performance bottleneck.",
    "## Why this matters now",
    "Impacts production.",
    "## Detailed proposal",
    "Refactor the pipeline.",
    "## Scope suggestion",
    "Core only.",
    "## Requirements",
    "Latency under threshold.",
    "## Dependencies and constraints",
    "None.",
    "## Success metrics",
    "50% reduction.",
    "## Validation commands",
    "- pytest -q",
    "## Risks and mitigations",
    "- Risk: regression",
    "## Failure handling and rollback",
    "- Rollback: revert",
    "## Source references",
    "- docs/ref.md",
]


def test_similarity_blocking_finds_shared_project_duplicates(tmp_path: Path) -> None:
    """Blocking similarity must detect duplicates for ideas sharing a planned project ID."""
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    (ideas_dir / "idea000401-async-pipeline-gateway.md").write_text(
        "\n".join(
            [
                "# idea-401 - async pipeline gateway",
                "",
                "Planned project mapping: prj0000401",
                "",
            ]
            + _FULL_SECTIONS
        ),
        encoding="utf-8",
    )
    (ideas_dir / "idea000402-async-pipeline-triage.md").write_text(
        "\n".join(
            [
                "# idea-402 - async pipeline triage",
                "",
                "Planned project mapping: prj0000401",
                "",
            ]
            + _FULL_SECTIONS
        ),
        encoding="utf-8",
    )
    # Third idea in a completely different project — must NOT appear as candidate with 401/402.
    (ideas_dir / "idea000403-unrelated-topic.md").write_text(
        "\n".join(
            [
                "# idea-403 - unrelated topic",
                "",
                "Planned project mapping: prj0000999",
                "",
            ]
            + _FULL_SECTIONS
        ),
        encoding="utf-8",
    )

    module = _load_idea_tracker_module()
    payload = module.build_tracker_payload(tmp_path)

    all_candidates = (
        payload["duplicate_candidates"]["merge_candidates"]
        + payload["duplicate_candidates"]["review_candidates"]
    )
    candidate_pairs = {tuple(sorted(item["idea_ids"])) for item in all_candidates}

    assert ("idea000401", "idea000402") in candidate_pairs, (
        "Ideas sharing a project ID must be reported as duplicate candidates"
    )
    # Cross-project pairs must be absent (no shared project or title prefix).
    assert ("idea000401", "idea000403") not in candidate_pairs
    assert ("idea000402", "idea000403") not in candidate_pairs


def test_similarity_blocking_ignores_cross_project_pairs(tmp_path: Path) -> None:
    """Blocking strategy must not compare ideas from disjoint project groups."""
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    # 3 ideas in project A, 2 ideas in project B — disjoint titles.
    project_a_sections = [
        "## Problem statement", "Alpha problem.",
        "## Success metrics", "Alpha metric.",
        "## Validation commands", "- pytest -q",
        "## Risks and mitigations", "- Risk.",
        "## Failure handling and rollback", "- Rollback.",
        "## Source references", "- docs/alpha.md",
    ]
    project_b_sections = [
        "## Problem statement", "Beta problem.",
        "## Success metrics", "Beta metric.",
        "## Validation commands", "- pytest -q",
        "## Risks and mitigations", "- Risk.",
        "## Failure handling and rollback", "- Rollback.",
        "## Source references", "- docs/beta.md",
    ]

    for idx in range(1, 4):
        (ideas_dir / f"idea00050{idx}-alpha-idea-{idx}.md").write_text(
            "\n".join(
                [f"# idea-50{idx} - alpha idea {idx}", "", "Planned project mapping: prj0000501", ""]
                + project_a_sections
            ),
            encoding="utf-8",
        )
    for idx in range(4, 6):
        (ideas_dir / f"idea00050{idx}-beta-idea-{idx}.md").write_text(
            "\n".join(
                [f"# idea-50{idx} - beta idea {idx}", "", "Planned project mapping: prj0000502", ""]
                + project_b_sections
            ),
            encoding="utf-8",
        )

    module = _load_idea_tracker_module()
    payload = module.build_tracker_payload(tmp_path)

    all_candidates = (
        payload["duplicate_candidates"]["merge_candidates"]
        + payload["duplicate_candidates"]["review_candidates"]
    )
    candidate_pair_set = {tuple(sorted(c["idea_ids"])) for c in all_candidates}

    # No cross-project pair should appear.
    cross_project = [
        ("idea000501", "idea000504"),
        ("idea000501", "idea000505"),
        ("idea000502", "idea000504"),
        ("idea000502", "idea000505"),
        ("idea000503", "idea000504"),
        ("idea000503", "idea000505"),
    ]
    for pair in cross_project:
        assert pair not in candidate_pair_set, f"Cross-project pair {pair} should not be a candidate"


def test_similarity_blocking_title_fallback_finds_similar_ungrouped_ideas(tmp_path: Path) -> None:
    """Ideas with no project mapping but a shared title prefix must be compared via title-fallback blocking.

    This validates that the fallback blocking key (first significant title token) is generated
    and that pairs in the same title block are evaluated and reported when their
    combined similarity score exceeds the review threshold (0.6).

    Design note: both ideas carry identical H1 titles and the same source reference
    so their Jaccard scores are title_sim=1.0, source_sim=1.0, mapping_sim=0.0,
    yielding a combined score of 0.70 which clears the default review threshold.
    """
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    shared_title = "# async pipeline optimizer"  # first token "async" → blocking key title:async
    sections = [
        "## Problem statement", "Pipeline slow.",
        "## Success metrics", "2x faster.",
        "## Validation commands", "- pytest -q",
        "## Risks and mitigations", "- Risk.",
        "## Failure handling and rollback", "- Rollback.",
        "## Source references", "- docs/ref.md",
    ]

    # Both ideas: no planned project mapping, identical title → title-fallback blocking applies.
    (ideas_dir / "idea000601-pipeline-alpha.md").write_text(
        "\n".join(
            [shared_title, "", "Planned project mapping: none yet", ""] + sections
        ),
        encoding="utf-8",
    )
    (ideas_dir / "idea000602-pipeline-beta.md").write_text(
        "\n".join(
            [shared_title, "", "Planned project mapping: none yet", ""] + sections
        ),
        encoding="utf-8",
    )

    module = _load_idea_tracker_module()
    payload = module.build_tracker_payload(tmp_path)

    all_candidates = (
        payload["duplicate_candidates"]["merge_candidates"]
        + payload["duplicate_candidates"]["review_candidates"]
    )
    candidate_pairs = {tuple(sorted(item["idea_ids"])) for item in all_candidates}

    assert ("idea000601", "idea000602") in candidate_pairs, (
        "Ideas with no project mapping but shared title token must be compared via title-fallback blocking"
    )


def test_build_tracker_payload_verbose_logs_to_stderr(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    """Verbose mode must emit progress lines to stderr and leave stdout clean."""
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    for idx in range(1, 4):
        (ideas_dir / f"idea00070{idx}-verbose-test-{idx}.md").write_text(
            "\n".join(
                [f"# idea-70{idx} - verbose test {idx}", "", "## Source references", "- docs/v.md"]
            ),
            encoding="utf-8",
        )

    module = _load_idea_tracker_module()
    module.build_tracker_payload(tmp_path, verbose=True, batch_size=1)

    captured = capsys.readouterr()
    assert "[IdeaTracker]" in captured.err, "Verbose mode must write [IdeaTracker] progress to stderr"
    assert captured.out == "", "Verbose progress must not contaminate stdout"


def test_build_tracker_payload_batch_size_default_no_stderr(tmp_path: Path, capsys: CaptureFixture[str]) -> None:
    """Without --verbose, no progress output must reach stderr."""
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    (ideas_dir / "idea000801-quiet-test.md").write_text(
        "# idea-801 - quiet test\n\n## Source references\n- docs/q.md\n",
        encoding="utf-8",
    )

    module = _load_idea_tracker_module()
    module.build_tracker_payload(tmp_path, verbose=False)

    captured = capsys.readouterr()
    assert captured.err == "", "Non-verbose mode must produce no stderr output"


def test_similarity_verbose_heartbeat_not_tied_to_large_batch_size(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    """Similarity stage should keep emitting heartbeats even with huge batch_size values."""
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    sections = [
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

    # Two groups so the similarity stage has meaningful block processing.
    for idx in range(1, 21):
        (ideas_dir / f"idea0012{idx:02d}-alpha-{idx}.md").write_text(
            "\n".join(
                [
                    f"# async alpha tracker {idx}",
                    "",
                    "Planned project mapping: prj0012001",
                    "",
                ]
                + sections
            ),
            encoding="utf-8",
        )
    for idx in range(21, 41):
        (ideas_dir / f"idea0012{idx:02d}-beta-{idx}.md").write_text(
            "\n".join(
                [
                    f"# async beta tracker {idx}",
                    "",
                    "Planned project mapping: prj0012002",
                    "",
                ]
                + sections
            ),
            encoding="utf-8",
        )

    module = _load_idea_tracker_module()
    module.build_tracker_payload(tmp_path, verbose=True, batch_size=10000)

    captured = capsys.readouterr()
    progress_lines = [
        line for line in captured.err.splitlines() if "Similarity stage: processed blocks" in line
    ]
    assert len(progress_lines) >= 2, "Expected recurring similarity heartbeats with very large batch_size"


def test_build_tracker_payload_writes_checkpoint_each_batch(tmp_path: Path) -> None:
    """Progress checkpoints should be written at each batch interval when configured."""
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    for idx in range(1, 6):
        (ideas_dir / f"idea00090{idx}-checkpoint-{idx}.md").write_text(
            "\n".join(
                [
                    f"# idea-90{idx} - checkpoint {idx}",
                    "",
                    "Planned project mapping: none yet",
                    "",
                    "## Source references",
                    "- docs/c.md",
                ]
            ),
            encoding="utf-8",
        )

    module = _load_idea_tracker_module()
    checkpoint_path = tmp_path / "docs" / "project" / "ideatracker.json"
    module.build_tracker_payload(
        tmp_path,
        batch_size=2,
        verbose=False,
        checkpoint_output_path=checkpoint_path,
    )

    checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    assert checkpoint.get("in_progress") is True
    assert checkpoint.get("progress", {}).get("stage") in {"collecting", "similarity"}
    assert checkpoint["source"]["processed_total"] >= 4


def test_build_tracker_payload_persists_incremental_artifacts(tmp_path: Path) -> None:
    """Incremental runs must persist the full artifact set under docs/project."""
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    for idx in range(1, 4):
        (ideas_dir / f"idea00130{idx}-artifact-{idx}.md").write_text(
            "\n".join(
                [
                    f"# idea-130{idx} - artifact {idx}",
                    "",
                    "Planned project mapping: prj0013001",
                    "",
                    "## Problem statement",
                    "Artifact persistence problem.",
                    "## Success metrics",
                    "Artifacts written.",
                    "## Validation commands",
                    "- pytest -q",
                    "## Risks and mitigations",
                    "- Schema drift.",
                    "## Failure handling and rollback",
                    "- Re-run batch.",
                    "## Source references",
                    f"- docs/ref-{idx}.md",
                ]
            ),
            encoding="utf-8",
        )

    module = _load_idea_tracker_module()
    payload = module.build_tracker_payload(tmp_path, batch_size=2, limit=3, verbose=False)

    progress_path = _artifact_path(tmp_path, "ideatracker.progress.json")
    mapping_path = _artifact_path(tmp_path, "ideatracker.mapping.json")
    references_path = _artifact_path(tmp_path, "ideatracker.references.json")
    section_names_path = _artifact_path(tmp_path, "ideatracker.section_names.json")
    tokens_path = _artifact_path(tmp_path, "ideatracker.tokens.json")
    similarities_path = _artifact_path(tmp_path, "ideatracker.similarities.json")

    for path in [
        progress_path,
        mapping_path,
        references_path,
        section_names_path,
        tokens_path,
        similarities_path,
    ]:
        assert path.exists(), f"Expected artifact file {path.name} to be written"

    progress_payload = json.loads(progress_path.read_text(encoding="utf-8"))
    mapping_payload = json.loads(mapping_path.read_text(encoding="utf-8"))
    references_payload = json.loads(references_path.read_text(encoding="utf-8"))
    section_names_payload = json.loads(section_names_path.read_text(encoding="utf-8"))
    tokens_payload = json.loads(tokens_path.read_text(encoding="utf-8"))
    similarities_payload = json.loads(similarities_path.read_text(encoding="utf-8"))

    assert progress_payload["next_offset"] == 3
    assert len(progress_payload["completed_batches"]) == 2
    assert len(mapping_payload["mappings"]) == payload["summary"]["total"] == 3
    assert len(section_names_payload["sections"]) == 3
    assert len(tokens_payload["token_rows"]) == 3
    assert len(references_payload["references"]) == 3
    assert isinstance(references_payload["reference_index"], list)
    assert isinstance(section_names_payload["section_frequency"], list)
    assert similarities_payload["thresholds"]["merge"] == 0.8
    assert similarities_payload["thresholds"]["review"] == 0.6


def test_build_tracker_payload_rewrites_existing_batch_rows_without_duplicates(tmp_path: Path) -> None:
    """Re-running the same window must replace persisted rows instead of duplicating them."""
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    idea_path = ideas_dir / "idea001401-rewrite-target.md"
    idea_path.write_text(
        "\n".join(
            [
                "# initial rewrite title",
                "",
                "Planned project mapping: none yet",
                "",
                "## Problem statement",
                "Initial state.",
                "## Success metrics",
                "Initial metric.",
                "## Validation commands",
                "- pytest -q",
                "## Risks and mitigations",
                "- Initial risk.",
                "## Failure handling and rollback",
                "- Initial rollback.",
                "## Source references",
                "- docs/initial.md",
            ]
        ),
        encoding="utf-8",
    )
    (ideas_dir / "idea001402-second-target.md").write_text(
        "\n".join(
            [
                "# second stable title",
                "",
                "Planned project mapping: none yet",
                "",
                "## Problem statement",
                "Second state.",
                "## Success metrics",
                "Second metric.",
                "## Validation commands",
                "- pytest -q",
                "## Risks and mitigations",
                "- Second risk.",
                "## Failure handling and rollback",
                "- Second rollback.",
                "## Source references",
                "- docs/second.md",
            ]
        ),
        encoding="utf-8",
    )

    module = _load_idea_tracker_module()
    module.build_tracker_payload(tmp_path, batch_size=1, limit=2, verbose=False)

    idea_path.write_text(
        idea_path.read_text(encoding="utf-8").replace(
            "# initial rewrite title",
            "# rewritten artifact title",
        ),
        encoding="utf-8",
    )
    module.build_tracker_payload(tmp_path, batch_size=1, limit=2, verbose=False)

    mapping_payload = json.loads(_artifact_path(tmp_path, "ideatracker.mapping.json").read_text(encoding="utf-8"))
    token_payload = json.loads(_artifact_path(tmp_path, "ideatracker.tokens.json").read_text(encoding="utf-8"))
    progress_payload = json.loads(_artifact_path(tmp_path, "ideatracker.progress.json").read_text(encoding="utf-8"))

    assert len(mapping_payload["mappings"]) == 2
    assert len(token_payload["token_rows"]) == 2
    assert len(progress_payload["completed_batches"]) == 2

    mapping_by_id = {row["idea_id"]: row for row in mapping_payload["mappings"]}
    tokens_by_id = {row["idea_id"]: row for row in token_payload["token_rows"]}
    assert mapping_by_id["idea001401"]["title"] == "rewritten artifact title"
    assert "rewritten" in tokens_by_id["idea001401"]["title_tokens"]
    assert "initial" not in tokens_by_id["idea001401"]["title_tokens"]


def test_write_split_tracker_chunks_creates_expected_files(tmp_path: Path) -> None:
    """Split output should emit one chunk file per batch using NNNNNN suffix."""
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    archive_dir.mkdir(parents=True)

    for idx in range(1, 6):
        (ideas_dir / f"idea00110{idx}-split-test-{idx}.md").write_text(
            "\n".join(
                [
                    f"# idea-110{idx} - split test {idx}",
                    "",
                    "Planned project mapping: none yet",
                    "",
                    "## Source references",
                    "- docs/split.md",
                ]
            ),
            encoding="utf-8",
        )

    module = _load_idea_tracker_module()
    output_path = tmp_path / "docs" / "project" / "ideatracker.json"
    payload = module.build_tracker_payload(tmp_path, batch_size=2, verbose=False)
    module.write_tracker(output_path, payload)
    written = module.write_split_tracker_chunks(output_path, payload, chunk_size=2)

    assert written == 3
    assert (output_path.parent / "ideatracker-000001.json").exists()
    assert (output_path.parent / "ideatracker-000003.json").exists()
    assert (output_path.parent / "ideatracker-000005.json").exists()
