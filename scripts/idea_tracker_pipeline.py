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

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from scripts.idea_tracker_artifacts import (
    artifact_paths,
    load_all_artifacts,
    project_output_dir,
    update_progress_artifact,
    write_json,
    write_mapping_rows,
    write_reference_rows,
    write_section_rows,
    write_similarity_rows,
    write_token_rows,
)
from scripts.idea_tracker_similarity import build_similarity_candidates

RecordCollector = Callable[[Path, Path, bool], dict[str, Any]]
Tokenize = Callable[[str], set[str]]
BlockingKeys = Callable[[dict[str, Any]], list[str]]


def _build_batch_rows(
    records: list[dict[str, Any]],
    batch_id: str,
    tokenize: Tokenize,
    blocking_keys: BlockingKeys,
) -> dict[str, list[dict[str, Any]]]:
    """Build persisted batch artifact rows from collected idea records.

    Args:
        records: Batch idea records.
        batch_id: Deterministic batch identifier.
        tokenize: Tokenization helper.
        blocking_keys: Blocking-key helper.

    Returns:
        Mapping of artifact row collections.

    """
    mapping_rows: list[dict[str, Any]] = []
    reference_rows: list[dict[str, Any]] = []
    section_rows: list[dict[str, Any]] = []
    token_rows: list[dict[str, Any]] = []
    for record in records:
        idea_id = record.get("idea_id", "")
        if not idea_id:
            continue
        mapping_rows.append(
            {
                "idea_id": idea_id,
                "title": record.get("title", ""),
                "slug": record.get("slug", ""),
                "source_path": record.get("source_path", ""),
                "status": record.get("status", ""),
                "planned_project_ids": list(record.get("planned_project_ids", [])),
                "readiness_status": record.get("readiness_status", ""),
                "sha256": record.get("sha256", ""),
                "updated": record.get("updated", ""),
                "template_completeness": record.get("template_completeness", 0.0),
                "intake_answer_coverage": record.get("intake_answer_coverage", 0.0),
                "scoring": dict(record.get("scoring", {})),
                "merged_from": list(record.get("merged_from", [])),
                "batch_id": batch_id,
            }
        )
        for reference in sorted(record.get("source_references", [])):
            reference_rows.append(
                {
                    "idea_id": idea_id,
                    "reference": reference,
                    "batch_id": batch_id,
                }
            )
        section_rows.append(
            {
                "idea_id": idea_id,
                "section_names": sorted(record.get("section_names", [])),
                "missing_required_sections": list(record.get("missing_required_sections", [])),
                "missing_critical_sections": list(record.get("missing_critical_sections", [])),
                "template_completeness": record.get("template_completeness", 0.0),
                "intake_answer_coverage": record.get("intake_answer_coverage", 0.0),
                "batch_id": batch_id,
            }
        )
        token_rows.append(
            {
                "idea_id": idea_id,
                "title_tokens": sorted(tokenize(record.get("title", ""))),
                "project_tokens": sorted(record.get("planned_project_ids", [])),
                "source_reference_tokens": sorted(
                    set().union(*(tokenize(reference) for reference in record.get("source_references", [])))
                ),
                "blocking_keys": blocking_keys(record),
                "batch_id": batch_id,
            }
        )
    return {
        "mapping": mapping_rows,
        "references": reference_rows,
        "section_names": section_rows,
        "tokens": token_rows,
    }


def _build_idea_records_from_artifacts(
    artifacts: dict[str, dict[str, Any]],
    scope_idea_ids: set[str],
) -> list[dict[str, Any]]:
    """Rebuild final idea records from persisted artifacts.

    Args:
        artifacts: Loaded artifact payloads.
        scope_idea_ids: Idea IDs included in the current output scope.

    Returns:
        Reconstructed idea records.

    """
    mapping_rows = artifacts["mapping"].get("mappings", [])
    section_rows = artifacts["section_names"].get("sections", [])
    reference_rows = artifacts["references"].get("references", [])
    section_index = {row.get("idea_id", ""): row for row in section_rows if row.get("idea_id") in scope_idea_ids}
    reference_index: dict[str, list[str]] = {}
    for row in reference_rows:
        idea_id = row.get("idea_id", "")
        if idea_id not in scope_idea_ids:
            continue
        reference = row.get("reference", "")
        if reference:
            reference_index.setdefault(idea_id, []).append(reference)
    records: list[dict[str, Any]] = []
    for row in mapping_rows:
        idea_id = row.get("idea_id", "")
        if idea_id not in scope_idea_ids:
            continue
        section_row = section_index.get(idea_id, {})
        records.append(
            {
                "idea_id": idea_id,
                "title": row.get("title", ""),
                "slug": row.get("slug", ""),
                "status": row.get("status", ""),
                "source_path": row.get("source_path", ""),
                "planned_project_ids": list(row.get("planned_project_ids", [])),
                "source_references": sorted(reference_index.get(idea_id, [])),
                "template_completeness": section_row.get(
                    "template_completeness",
                    row.get("template_completeness", 0.0),
                ),
                "missing_required_sections": list(section_row.get("missing_required_sections", [])),
                "missing_critical_sections": list(section_row.get("missing_critical_sections", [])),
                "intake_answer_coverage": section_row.get(
                    "intake_answer_coverage",
                    row.get("intake_answer_coverage", 0.0),
                ),
                "readiness_status": row.get("readiness_status", ""),
                "scoring": dict(row.get("scoring", {})),
                "merged_from": list(row.get("merged_from", [])),
                "sha256": row.get("sha256", ""),
                "updated": row.get("updated", ""),
                "section_names": sorted(section_row.get("section_names", [])),
            }
        )
    return sorted(
        records,
        key=lambda item: (
            item.get("idea_id", ""),
            item.get("status", ""),
            item.get("source_path", ""),
        ),
    )


def build_tracker_payload_from_artifacts(
    project_dir: Path,
    scope_idea_ids: set[str],
    source: dict[str, Any],
    merge_threshold: float,
    review_threshold: float,
    in_progress: bool = False,
    progress: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble a tracker payload from the persisted artifact set.

    Args:
        project_dir: Docs/project artifact directory.
        scope_idea_ids: Idea IDs included in the current output scope.
        source: Source metadata for the current output.
        merge_threshold: Merge-candidate threshold.
        review_threshold: Review-candidate threshold.
        in_progress: Whether the output is an in-progress checkpoint payload.
        progress: Optional progress metadata block.

    Returns:
        Final or in-progress tracker payload.

    """
    artifacts = load_all_artifacts(project_dir, merge_threshold, review_threshold)
    idea_records = _build_idea_records_from_artifacts(artifacts, scope_idea_ids)
    ids = [item.get("idea_id", "") for item in idea_records if item.get("idea_id")]
    id_counts = Counter(ids)
    duplicate_ids = sorted([idea_id for idea_id, count in id_counts.items() if count > 1])
    readiness_counts = {
        "ready": sum(1 for item in idea_records if item.get("readiness_status") == "ready"),
        "needs-discovery": sum(1 for item in idea_records if item.get("readiness_status") == "needs-discovery"),
        "blocked": sum(1 for item in idea_records if item.get("readiness_status") == "blocked"),
    }
    candidate_rows = [
        row
        for row in artifacts["similarities"].get("candidate_pairs", [])
        if row.get("left_idea_id") in scope_idea_ids and row.get("right_idea_id") in scope_idea_ids
    ]
    merge_candidates = [
        {
            "type": row.get("type", ""),
            "score": row.get("score", 0.0),
            "idea_ids": [row.get("left_idea_id", ""), row.get("right_idea_id", "")],
            "paths": list(row.get("paths", [])),
            "signals": dict(row.get("signals", {})),
        }
        for row in candidate_rows
        if row.get("type") == "merge_candidate"
    ]
    review_candidates = [
        {
            "type": row.get("type", ""),
            "score": row.get("score", 0.0),
            "idea_ids": [row.get("left_idea_id", ""), row.get("right_idea_id", "")],
            "paths": list(row.get("paths", [])),
            "signals": dict(row.get("signals", {})),
        }
        for row in candidate_rows
        if row.get("type") == "review_candidate"
    ]
    payload = {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "summary": {
            "total": len(idea_records),
            "active": sum(1 for item in idea_records if item.get("status") == "active"),
            "archived": sum(1 for item in idea_records if item.get("status") == "archived"),
            "unique_idea_ids": len(set(ids)),
            "duplicate_idea_ids": duplicate_ids,
            "readiness": readiness_counts,
            "merge_candidates": len(merge_candidates),
            "review_candidates": len(review_candidates),
        },
        "queues": {
            "ready": [item.get("idea_id", "") for item in idea_records if item.get("readiness_status") == "ready"],
            "needs-discovery": [
                item.get("idea_id", "") for item in idea_records if item.get("readiness_status") == "needs-discovery"
            ],
            "blocked": [item.get("idea_id", "") for item in idea_records if item.get("readiness_status") == "blocked"],
        },
        "duplicate_candidates": {
            "merge_candidates": merge_candidates,
            "review_candidates": review_candidates,
        },
        "ideas": idea_records,
    }
    if in_progress:
        payload["in_progress"] = True
        payload["progress"] = progress or {}
    return payload


def write_split_tracker_chunks(output_path: Path, payload: dict[str, Any], chunk_size: int) -> int:
    """Write split tracker chunk files named ``<stem>-NNNNNN.json``.

    Args:
        output_path: Main tracker output file path.
        payload: Final tracker payload.
        chunk_size: Number of idea records per split file.

    Returns:
        Number of chunk files written.

    """
    if chunk_size <= 0:
        return 0
    ideas = payload.get("ideas") or []
    if not isinstance(ideas, list) or not ideas:
        return 0
    source = payload.get("source", {})
    duplicate_candidates = payload.get("duplicate_candidates", {"merge_candidates": [], "review_candidates": []})
    generated_at = payload.get("generated_at", datetime.now(timezone.utc).isoformat())
    chunk_count = 0
    for start in range(0, len(ideas), chunk_size):
        chunk_ideas = ideas[start : start + chunk_size]
        chunk_start_index = start + 1
        chunk_path = output_path.with_name(f"{output_path.stem}-{chunk_start_index:06d}.json")
        ids = [item.get("idea_id", "") for item in chunk_ideas if isinstance(item, dict)]
        duplicate_ids = sorted({idea_id for idea_id in ids if idea_id and ids.count(idea_id) > 1})
        readiness_counts = {
            "ready": sum(1 for item in chunk_ideas if item.get("readiness_status") == "ready"),
            "needs-discovery": sum(1 for item in chunk_ideas if item.get("readiness_status") == "needs-discovery"),
            "blocked": sum(1 for item in chunk_ideas if item.get("readiness_status") == "blocked"),
        }
        chunk_payload = {
            "schema_version": payload.get("schema_version", 2),
            "generated_at": generated_at,
            "source": {
                "active_dir": source.get("active_dir", "docs/project/ideas"),
                "archive_dir": source.get("archive_dir", "docs/project/ideas/archive"),
                "offset": (source.get("offset") or 0) + start,
                "limit": len(chunk_ideas),
                "available_total": source.get("available_total", len(ideas)),
                "processed_total": len(chunk_ideas),
            },
            "summary": {
                "total": len(chunk_ideas),
                "active": sum(1 for item in chunk_ideas if item.get("status") == "active"),
                "archived": sum(1 for item in chunk_ideas if item.get("status") == "archived"),
                "unique_idea_ids": len(set(ids)),
                "duplicate_idea_ids": duplicate_ids,
                "readiness": readiness_counts,
                "merge_candidates": 0,
                "review_candidates": 0,
            },
            "queues": {
                "ready": [item.get("idea_id", "") for item in chunk_ideas if item.get("readiness_status") == "ready"],
                "needs-discovery": [
                    item.get("idea_id", "") for item in chunk_ideas if item.get("readiness_status") == "needs-discovery"
                ],
                "blocked": [
                    item.get("idea_id", "") for item in chunk_ideas if item.get("readiness_status") == "blocked"
                ],
            },
            "duplicate_candidates": duplicate_candidates,
            "ideas": chunk_ideas,
        }
        write_json(chunk_path, chunk_payload)
        chunk_count += 1
    return chunk_count


def run_incremental_tracker(
    repo_root: Path,
    offset: int,
    limit: int | None,
    merge_threshold: float,
    review_threshold: float,
    batch_size: int,
    verbose: bool,
    output_path: Path | None,
    collect_record: RecordCollector,
    tokenize: Tokenize,
    blocking_keys: BlockingKeys,
    log: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    """Run the persisted incremental IdeaTracker pipeline.

    Args:
        repo_root: Repository root path.
        offset: Start index into the combined idea file list.
        limit: Optional processing limit.
        merge_threshold: Merge-candidate threshold.
        review_threshold: Review-candidate threshold.
        batch_size: Collection batch size.
        verbose: Whether to emit progress logs.
        output_path: Optional main output path used for per-batch checkpoints.
        collect_record: Record collector callable.
        tokenize: Tokenization helper.
        blocking_keys: Blocking-key helper.
        log: Optional progress logger.

    Returns:
        Final tracker payload.

    """
    ideas_root = repo_root / "docs" / "project" / "ideas"
    archive_root = ideas_root / "archive"
    active_files_all = sorted(path for path in ideas_root.glob("idea*.md") if path.is_file())
    archived_files_all = sorted(path for path in archive_root.glob("idea*.md") if path.is_file())
    all_files_with_status: list[tuple[Path, bool]] = [(path, False) for path in active_files_all]
    all_files_with_status += [(path, True) for path in archived_files_all]
    scoped_start = max(offset, 0)
    scoped_end = None if limit is None else scoped_start + max(limit, 0)
    scoped_files = all_files_with_status[scoped_start:scoped_end]
    effective_batch_size = max(1, batch_size)
    if verbose and log is not None:
        log(f"[IdeaTracker] Collecting {len(scoped_files)} idea files (batch_size={effective_batch_size})")

    project_dir = project_output_dir(repo_root)
    paths = artifact_paths(project_dir)
    run_args = {
        "offset": offset,
        "limit": limit,
        "batch_size": batch_size,
        "verbose": verbose,
        "output": str(output_path) if output_path is not None else "",
    }
    run_scope_idea_ids: set[str] = set()
    processed_total = 0

    for batch_offset in range(0, len(scoped_files), effective_batch_size):
        batch_slice = scoped_files[batch_offset : batch_offset + effective_batch_size]
        batch_records = [collect_record(repo_root, file_path, archived=archived) for file_path, archived in batch_slice]
        batch_id = f"batch-{scoped_start + batch_offset:06d}"
        batch_rows = _build_batch_rows(batch_records, batch_id, tokenize, blocking_keys)
        write_mapping_rows(paths["mapping"], batch_rows["mapping"])
        write_reference_rows(paths["references"], batch_rows["references"])
        write_section_rows(paths["section_names"], batch_rows["section_names"])
        write_token_rows(paths["tokens"], batch_rows["tokens"])

        batch_idea_ids = {record.get("idea_id", "") for record in batch_records if record.get("idea_id")}
        run_scope_idea_ids.update(batch_idea_ids)
        processed_total += len(batch_records)
        next_offset = scoped_start + processed_total
        batch_row = {
            "batch_id": batch_id,
            "offset": scoped_start + batch_offset,
            "limit": len(batch_records),
            "processed_total": len(batch_records),
            "stage": "collected",
            "status": "completed",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "completed_at": datetime.now(timezone.utc).isoformat(),
            "files_written": [
                paths["mapping"].name,
                paths["references"].name,
                paths["section_names"].name,
                paths["tokens"].name,
            ],
        }
        update_progress_artifact(paths["progress"], run_args, len(all_files_with_status), next_offset, batch_row)
        if verbose and log is not None:
            log(f"[IdeaTracker] Processed {processed_total}/{len(scoped_files)} files...")

        if output_path is not None:
            partial_payload = build_tracker_payload_from_artifacts(
                project_dir,
                run_scope_idea_ids,
                {
                    "active_dir": "docs/project/ideas",
                    "archive_dir": "docs/project/ideas/archive",
                    "offset": scoped_start,
                    "limit": limit,
                    "available_total": len(all_files_with_status),
                    "processed_total": processed_total,
                },
                merge_threshold,
                review_threshold,
                in_progress=True,
                progress={
                    "stage": "collecting",
                    "processed": processed_total,
                    "batch_size": effective_batch_size,
                },
            )
            write_json(output_path, partial_payload)

    if verbose and scoped_files and log is not None:
        log(f"[IdeaTracker] Collection complete: {len(scoped_files)}/{len(scoped_files)} files processed")
        log("[IdeaTracker] Building summary indexes...")
        log("[IdeaTracker] Starting similarity analysis...")
        log("[IdeaTracker] Similarity analysis in progress...")

    artifacts = load_all_artifacts(project_dir, merge_threshold, review_threshold)
    similarity_batch_id = f"similarity-{scoped_start:06d}-{len(scoped_files):06d}"
    similarity_rows = build_similarity_candidates(
        artifacts["mapping"].get("mappings", []),
        artifacts["tokens"].get("token_rows", []),
        merge_threshold,
        review_threshold,
        scope_idea_ids=run_scope_idea_ids if run_scope_idea_ids else None,
        log=log if verbose else None,
        progress_every=effective_batch_size,
        similarity_batch_id=similarity_batch_id,
    )
    write_similarity_rows(paths["similarities"], similarity_rows, merge_threshold, review_threshold)
    final_source = {
        "active_dir": "docs/project/ideas",
        "archive_dir": "docs/project/ideas/archive",
        "offset": scoped_start,
        "limit": limit,
        "available_total": len(all_files_with_status),
        "processed_total": len(run_scope_idea_ids),
    }
    final_payload = build_tracker_payload_from_artifacts(
        project_dir,
        run_scope_idea_ids,
        final_source,
        merge_threshold,
        review_threshold,
    )
    return final_payload
