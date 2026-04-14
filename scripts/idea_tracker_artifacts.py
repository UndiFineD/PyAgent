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

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 3
PROGRESS_FILE_NAME = "ideatracker.progress.json"
MAPPING_FILE_NAME = "ideatracker.mapping.json"
REFERENCES_FILE_NAME = "ideatracker.references.json"
SECTION_NAMES_FILE_NAME = "ideatracker.section_names.json"
TOKENS_FILE_NAME = "ideatracker.tokens.json"
SIMILARITIES_FILE_NAME = "ideatracker.similarities.json"


def _timestamp() -> str:
    """Return the current UTC timestamp in ISO-8601 format.

    Returns:
        Current UTC timestamp string.

    """
    return datetime.now(timezone.utc).isoformat()


def project_output_dir(repo_root: Path) -> Path:
    """Return the canonical IdeaTracker artifact directory.

    Args:
        repo_root: Repository root path.

    Returns:
        The docs/project directory path.

    """
    return repo_root / "docs" / "project"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write a JSON payload with deterministic formatting.

    Args:
        path: Output file path.
        payload: JSON-serializable payload.

    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    """Read JSON or return a default payload when the file is absent.

    Args:
        path: Input file path.
        default: Default payload to return when the file does not exist.

    Returns:
        Loaded JSON payload or a shallow copy of the default payload.

    """
    if not path.exists():
        return dict(default)
    return json.loads(path.read_text(encoding="utf-8"))


def artifact_paths(project_dir: Path) -> dict[str, Path]:
    """Return the canonical set of artifact file paths.

    Args:
        project_dir: Docs/project directory path.

    Returns:
        Mapping of artifact labels to absolute file paths.

    """
    return {
        "progress": project_dir / PROGRESS_FILE_NAME,
        "mapping": project_dir / MAPPING_FILE_NAME,
        "references": project_dir / REFERENCES_FILE_NAME,
        "section_names": project_dir / SECTION_NAMES_FILE_NAME,
        "tokens": project_dir / TOKENS_FILE_NAME,
        "similarities": project_dir / SIMILARITIES_FILE_NAME,
    }


def default_progress_payload(run_args: dict[str, Any], available_total: int) -> dict[str, Any]:
    """Build the default progress artifact payload.

    Args:
        run_args: CLI/runtime arguments captured for the run.
        available_total: Total number of available idea files.

    Returns:
        Default progress payload.

    """
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _timestamp(),
        "run_args": run_args,
        "next_offset": run_args.get("offset", 0),
        "available_total": available_total,
        "completed_batches": [],
    }


def default_mapping_payload() -> dict[str, Any]:
    """Return the default mapping artifact payload.

    Returns:
        Empty mapping artifact payload.

    """
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _timestamp(),
        "source": {
            "active_dir": "docs/project/ideas",
            "archive_dir": "docs/project/ideas/archive",
        },
        "mappings": [],
    }


def default_references_payload() -> dict[str, Any]:
    """Return the default references artifact payload.

    Returns:
        Empty references artifact payload.

    """
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _timestamp(),
        "references": [],
        "reference_index": [],
    }


def default_section_names_payload() -> dict[str, Any]:
    """Return the default section artifact payload.

    Returns:
        Empty section-names artifact payload.

    """
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _timestamp(),
        "sections": [],
        "section_frequency": [],
    }


def default_tokens_payload() -> dict[str, Any]:
    """Return the default token artifact payload.

    Returns:
        Empty token artifact payload.

    """
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _timestamp(),
        "token_rows": [],
    }


def default_similarities_payload(merge_threshold: float, review_threshold: float) -> dict[str, Any]:
    """Return the default similarity artifact payload.

    Args:
        merge_threshold: Merge-candidate threshold.
        review_threshold: Review-candidate threshold.

    Returns:
        Empty similarities artifact payload.

    """
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": _timestamp(),
        "thresholds": {
            "merge": merge_threshold,
            "review": review_threshold,
        },
        "candidate_pairs": [],
    }


def _sort_rows(rows: list[dict[str, Any]], sort_fields: tuple[str, ...]) -> list[dict[str, Any]]:
    """Return rows sorted deterministically by the requested fields.

    Args:
        rows: Rows to sort.
        sort_fields: Field names used for ordering.

    Returns:
        Sorted row list.

    """
    return sorted(rows, key=lambda item: tuple(item.get(field, "") for field in sort_fields))


def _upsert_rows(
    existing_rows: list[dict[str, Any]],
    new_rows: list[dict[str, Any]],
    key_fields: tuple[str, ...],
    sort_fields: tuple[str, ...],
) -> list[dict[str, Any]]:
    """Upsert rows by entity key, replacing prior versions deterministically.

    Args:
        existing_rows: Current persisted rows.
        new_rows: Replacement rows.
        key_fields: Fields that uniquely identify an entity row.
        sort_fields: Fields used to sort the final row list.

    Returns:
        Updated and sorted row list.

    """
    new_key_set = {tuple(row.get(field, "") for field in key_fields) for row in new_rows}
    retained_rows = [
        row for row in existing_rows if tuple(row.get(field, "") for field in key_fields) not in new_key_set
    ]
    return _sort_rows(retained_rows + new_rows, sort_fields)


def update_progress_artifact(
    path: Path,
    run_args: dict[str, Any],
    available_total: int,
    next_offset: int,
    batch_row: dict[str, Any],
) -> dict[str, Any]:
    """Persist the progress artifact with an upserted batch ledger row.

    Args:
        path: Progress artifact path.
        run_args: CLI/runtime arguments.
        available_total: Total number of available idea files.
        next_offset: Next global offset after the completed batch.
        batch_row: Completed batch ledger row.

    Returns:
        Updated progress payload.

    """
    payload = read_json(path, default_progress_payload(run_args, available_total))
    batch_rows = payload.get("completed_batches", [])
    batch_key = batch_row.get("batch_id", "")
    batch_rows = [row for row in batch_rows if row.get("batch_id", "") != batch_key]
    batch_rows.append(batch_row)
    payload["schema_version"] = SCHEMA_VERSION
    payload["generated_at"] = _timestamp()
    payload["run_args"] = run_args
    payload["next_offset"] = next_offset
    payload["available_total"] = available_total
    payload["completed_batches"] = _sort_rows(batch_rows, ("offset", "batch_id"))
    write_json(path, payload)
    return payload


def _build_reference_index(reference_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build an aggregated reference index from normalized reference rows.

    Args:
        reference_rows: Flat reference rows.

    Returns:
        Aggregated reference index rows.

    """
    reference_map: dict[str, set[str]] = {}
    for row in reference_rows:
        reference = row.get("reference", "")
        idea_id = row.get("idea_id", "")
        if not reference or not idea_id:
            continue
        reference_map.setdefault(reference, set()).add(idea_id)
    return [
        {
            "reference": reference,
            "idea_ids": sorted(idea_ids),
            "count": len(idea_ids),
        }
        for reference, idea_ids in sorted(reference_map.items())
    ]


def _build_section_frequency(section_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build aggregated section-frequency counts.

    Args:
        section_rows: Section metadata rows.

    Returns:
        Aggregated section frequency rows.

    """
    frequency: dict[str, int] = {}
    for row in section_rows:
        for section_name in row.get("section_names", []):
            frequency[section_name] = frequency.get(section_name, 0) + 1
    return [{"section_name": section_name, "count": count} for section_name, count in sorted(frequency.items())]


def write_mapping_rows(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Persist mapping rows with deterministic upsert semantics.

    Args:
        path: Mapping artifact path.
        rows: Mapping rows for the current batch.

    Returns:
        Updated mapping artifact payload.

    """
    payload = read_json(path, default_mapping_payload())
    payload["schema_version"] = SCHEMA_VERSION
    payload["generated_at"] = _timestamp()
    payload["mappings"] = _upsert_rows(
        payload.get("mappings", []),
        rows,
        ("idea_id",),
        ("idea_id", "status", "source_path"),
    )
    write_json(path, payload)
    return payload


def write_reference_rows(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Persist reference rows with deterministic upsert semantics.

    Args:
        path: References artifact path.
        rows: Reference rows for the current batch.

    Returns:
        Updated references artifact payload.

    """
    payload = read_json(path, default_references_payload())
    updated_rows = _upsert_rows(
        payload.get("references", []),
        rows,
        ("idea_id", "reference"),
        ("reference", "idea_id"),
    )
    payload["schema_version"] = SCHEMA_VERSION
    payload["generated_at"] = _timestamp()
    payload["references"] = updated_rows
    payload["reference_index"] = _build_reference_index(updated_rows)
    write_json(path, payload)
    return payload


def write_section_rows(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Persist section rows with deterministic upsert semantics.

    Args:
        path: Section artifact path.
        rows: Section rows for the current batch.

    Returns:
        Updated section artifact payload.

    """
    payload = read_json(path, default_section_names_payload())
    updated_rows = _upsert_rows(
        payload.get("sections", []),
        rows,
        ("idea_id",),
        ("idea_id",),
    )
    payload["schema_version"] = SCHEMA_VERSION
    payload["generated_at"] = _timestamp()
    payload["sections"] = updated_rows
    payload["section_frequency"] = _build_section_frequency(updated_rows)
    write_json(path, payload)
    return payload


def write_token_rows(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Persist token rows with deterministic upsert semantics.

    Args:
        path: Token artifact path.
        rows: Token rows for the current batch.

    Returns:
        Updated token artifact payload.

    """
    payload = read_json(path, default_tokens_payload())
    payload["schema_version"] = SCHEMA_VERSION
    payload["generated_at"] = _timestamp()
    payload["token_rows"] = _upsert_rows(
        payload.get("token_rows", []),
        rows,
        ("idea_id",),
        ("idea_id",),
    )
    write_json(path, payload)
    return payload


def write_similarity_rows(
    path: Path,
    rows: list[dict[str, Any]],
    merge_threshold: float,
    review_threshold: float,
) -> dict[str, Any]:
    """Persist similarity candidate rows with deterministic upsert semantics.

    Args:
        path: Similarity artifact path.
        rows: Similarity candidate rows.
        merge_threshold: Merge-candidate threshold.
        review_threshold: Review-candidate threshold.

    Returns:
        Updated similarities artifact payload.

    """
    payload = read_json(path, default_similarities_payload(merge_threshold, review_threshold))
    payload["schema_version"] = SCHEMA_VERSION
    payload["generated_at"] = _timestamp()
    payload["thresholds"] = {
        "merge": merge_threshold,
        "review": review_threshold,
    }
    payload["candidate_pairs"] = _upsert_rows(
        payload.get("candidate_pairs", []),
        rows,
        ("left_idea_id", "right_idea_id"),
        ("left_idea_id", "right_idea_id"),
    )
    write_json(path, payload)
    return payload


def load_all_artifacts(
    project_dir: Path,
    merge_threshold: float,
    review_threshold: float,
) -> dict[str, dict[str, Any]]:
    """Load all IdeaTracker artifacts from disk.

    Args:
        project_dir: Docs/project directory path.
        merge_threshold: Merge-candidate threshold.
        review_threshold: Review-candidate threshold.

    Returns:
        Mapping of artifact names to loaded payloads.

    """
    paths = artifact_paths(project_dir)
    return {
        "progress": read_json(paths["progress"], default_progress_payload({}, 0)),
        "mapping": read_json(paths["mapping"], default_mapping_payload()),
        "references": read_json(paths["references"], default_references_payload()),
        "section_names": read_json(paths["section_names"], default_section_names_payload()),
        "tokens": read_json(paths["tokens"], default_tokens_payload()),
        "similarities": read_json(
            paths["similarities"],
            default_similarities_payload(merge_threshold, review_threshold),
        ),
    }
