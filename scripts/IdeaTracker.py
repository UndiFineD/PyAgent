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

import argparse
import hashlib
import itertools
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IDEA_ID_RE = re.compile(r"(idea\d{6})", re.IGNORECASE)
PLANNED_MAPPING_RE = re.compile(r"^Planned project mapping:\s*(.+)$", re.IGNORECASE)
PROJECT_ID_RE = re.compile(r"prj\d{7}", re.IGNORECASE)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
TOKEN_RE = re.compile(r"[a-z0-9]+")
READINESS_VALUE_RE = re.compile(r"readiness[_\s-]*status\s*:\s*([a-z\-]+)", re.IGNORECASE)

REQUIRED_SECTIONS = [
    "idea summary",
    "problem statement",
    "why this matters now",
    "detailed proposal",
    "scope suggestion",
    "requirements",
    "dependencies and constraints",
    "success metrics",
    "validation commands",
    "risks and mitigations",
    "failure handling and rollback",
    "source references",
]

INTAKE_SIGNALS = [
    "problem statement",
    "success metrics",
    "why this matters now",
    "scope suggestion",
    "dependencies and constraints",
    "risks and mitigations",
    "candidate implementation paths",
    "validation commands",
    "failure handling and rollback",
]

CRITICAL_SECTIONS = [
    "problem statement",
    "success metrics",
    "validation commands",
    "risks and mitigations",
    "failure handling and rollback",
]


def _repo_root() -> Path:
    """Return repository root path."""
    return Path(__file__).resolve().parents[1]


def _extract_idea_id(file_path: Path) -> str:
    """Extract idea ID from filename."""
    match = IDEA_ID_RE.search(file_path.stem)
    if match is None:
        return ""
    return match.group(1).lower()


def _extract_title(lines: list[str]) -> str:
    """Extract first markdown H1 title from content."""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def _extract_planned_mappings(lines: list[str]) -> list[str]:
    """Extract mapped project IDs from planned project mapping line."""
    mapping_line = ""
    for line in lines:
        match = PLANNED_MAPPING_RE.match(line.strip())
        if match is not None:
            mapping_line = match.group(1).strip()
            break

    if not mapping_line or mapping_line.lower() == "none yet":
        return []

    seen: set[str] = set()
    mapped: list[str] = []
    for project_id in PROJECT_ID_RE.findall(mapping_line):
        normalized = project_id.lower()
        if normalized not in seen:
            seen.add(normalized)
            mapped.append(normalized)
    return mapped


def _extract_source_references(lines: list[str]) -> list[str]:
    """Extract bullet entries under the 'Source references' section."""
    start = -1
    for idx, line in enumerate(lines):
        if line.strip().lower() == "## source references":
            start = idx + 1
            break

    if start < 0:
        return []

    refs: list[str] = []
    for idx in range(start, len(lines)):
        stripped = lines[idx].strip()
        if stripped.startswith("## "):
            break
        if stripped.startswith("- "):
            refs.append(stripped[2:].strip())
        elif stripped.startswith("* "):
            refs.append(stripped[2:].strip())
    return refs


def _extract_section_names(lines: list[str]) -> set[str]:
    """Return normalized section heading names (## only)."""
    sections: set[str] = set()
    for line in lines:
        match = HEADING_RE.match(line.strip())
        if match is None:
            continue
        sections.add(match.group(1).strip().lower())
    return sections


def _extract_section_bullets(lines: list[str], heading: str) -> list[str]:
    """Extract bullet values from a section heading."""
    heading_key = heading.strip().lower()
    start = -1
    for idx, line in enumerate(lines):
        match = HEADING_RE.match(line.strip())
        if match and match.group(1).strip().lower() == heading_key:
            start = idx + 1
            break
    if start < 0:
        return []

    values: list[str] = []
    for idx in range(start, len(lines)):
        stripped = lines[idx].strip()
        if stripped.startswith("## "):
            break
        if stripped.startswith("- "):
            values.append(stripped[2:].strip())
        elif stripped.startswith("* "):
            values.append(stripped[2:].strip())
    return values


def _extract_readiness_status(lines: list[str]) -> str:
    """Extract readiness status from explicit marker or section content."""
    text = "\n".join(lines)
    match = READINESS_VALUE_RE.search(text)
    if match is not None:
        value = match.group(1).strip().lower()
        if value in {"ready", "needs-discovery", "blocked"}:
            return value

    section_values = _extract_section_bullets(lines, "readiness status")
    for value in section_values:
        normalized = value.lower()
        for candidate in ("ready", "needs-discovery", "blocked"):
            if candidate in normalized:
                return candidate

    section_text = _extract_section_body(lines, "readiness status").lower()
    for candidate in ("ready", "needs-discovery", "blocked"):
        if candidate in section_text:
            return candidate

    return ""


def _extract_section_body(lines: list[str], heading: str) -> str:
    """Extract plain text body of a section heading."""
    heading_key = heading.strip().lower()
    start = -1
    for idx, line in enumerate(lines):
        match = HEADING_RE.match(line.strip())
        if match and match.group(1).strip().lower() == heading_key:
            start = idx + 1
            break
    if start < 0:
        return ""

    body_lines: list[str] = []
    for idx in range(start, len(lines)):
        stripped = lines[idx].strip()
        if stripped.startswith("## "):
            break
        if stripped:
            body_lines.append(stripped)
    return "\n".join(body_lines)


def _clamp_score(value: int) -> int:
    """Clamp score to [0, 5]."""
    return max(0, min(5, value))


def _compute_scores(
    section_names: set[str],
    source_references: list[str],
    planned_project_ids: list[str],
    readiness_status: str,
    completeness: float,
) -> dict[str, int]:
    """Compute deterministic triage scores from idea structure."""
    impact = 2
    impact += int("problem statement" in section_names)
    impact += int("why this matters now" in section_names)
    impact += int("success metrics" in section_names)

    confidence = 1
    confidence += int(len(source_references) > 0)
    confidence += int(completeness >= 0.75)
    confidence += int(readiness_status == "ready")
    confidence += int("validation commands" in section_names)

    effort = 3
    effort += int("candidate implementation paths" not in section_names)
    effort -= int("scope suggestion" in section_names)

    risk = 3
    risk += int("risks and mitigations" not in section_names)
    risk += int("failure handling and rollback" not in section_names)
    risk -= int(readiness_status == "blocked")

    alignment = 1
    alignment += min(2, len(planned_project_ids))
    alignment += int("requirements" in section_names)
    alignment += int("dependencies and constraints" in section_names)

    return {
        "impact_score": _clamp_score(impact),
        "confidence_score": _clamp_score(confidence),
        "effort_score": _clamp_score(effort),
        "risk_score": _clamp_score(risk),
        "alignment_score": _clamp_score(alignment),
    }


def _infer_readiness_status(explicit_status: str, missing_critical: list[str], completeness: float) -> str:
    """Infer readiness status when explicit status is unavailable."""
    if explicit_status in {"ready", "needs-discovery", "blocked"}:
        return explicit_status
    if len(missing_critical) >= 2:
        return "blocked"
    if completeness < 0.55 or len(missing_critical) == 1:
        return "needs-discovery"
    return "ready"


def _tokenize(text: str) -> set[str]:
    """Tokenize to lowercase alphanumeric words."""
    return {token for token in TOKEN_RE.findall(text.lower()) if token}


def _jaccard_similarity(left: set[str], right: set[str]) -> float:
    """Return Jaccard similarity of two token sets."""
    if not left and not right:
        return 0.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _idea_similarity(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    """Compute weighted similarity and component signals between two idea records."""
    title_sim = _jaccard_similarity(_tokenize(left.get("title", "")), _tokenize(right.get("title", "")))
    mapping_sim = _jaccard_similarity(
        set(left.get("planned_project_ids", [])),
        set(right.get("planned_project_ids", [])),
    )
    source_sim = _jaccard_similarity(
        set(left.get("source_references", [])),
        set(right.get("source_references", [])),
    )

    score = (0.5 * title_sim) + (0.3 * mapping_sim) + (0.2 * source_sim)
    return {
        "score": round(score, 4),
        "title_similarity": round(title_sim, 4),
        "mapping_similarity": round(mapping_sim, 4),
        "source_similarity": round(source_sim, 4),
    }


def _file_sha256(file_path: Path) -> str:
    """Return SHA-256 for deterministic change tracking."""
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        digest.update(handle.read())
    return digest.hexdigest()


def _collect_idea_record(repo_root: Path, file_path: Path, archived: bool) -> dict[str, Any]:
    """Build one idea record from markdown file."""
    text = file_path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    idea_id = _extract_idea_id(file_path)
    relative_path = file_path.relative_to(repo_root).as_posix()
    slug = file_path.stem
    if idea_id and slug.lower().startswith(f"{idea_id}-"):
        slug = slug[len(idea_id) + 1 :]

    section_names = _extract_section_names(lines)
    missing_sections = [name for name in REQUIRED_SECTIONS if name not in section_names]
    missing_critical = [name for name in CRITICAL_SECTIONS if name not in section_names]

    completeness = round((len(REQUIRED_SECTIONS) - len(missing_sections)) / len(REQUIRED_SECTIONS), 4)
    intake_answers = sum(1 for signal in INTAKE_SIGNALS if signal in section_names)
    intake_coverage = round(intake_answers / len(INTAKE_SIGNALS), 4)

    explicit_readiness = _extract_readiness_status(lines)
    source_refs = _extract_source_references(lines)
    planned_ids = _extract_planned_mappings(lines)
    readiness_status = _infer_readiness_status(explicit_readiness, missing_critical, completeness)
    scores = _compute_scores(section_names, source_refs, planned_ids, readiness_status, completeness)

    priority_score = (
        scores["impact_score"]
        + scores["confidence_score"]
        + scores["alignment_score"]
        - scores["effort_score"]
        - scores["risk_score"]
    )

    return {
        "idea_id": idea_id,
        "title": _extract_title(lines),
        "slug": slug,
        "status": "archived" if archived else "active",
        "source_path": relative_path,
        "planned_project_ids": planned_ids,
        "source_references": source_refs,
        "template_completeness": completeness,
        "missing_required_sections": missing_sections,
        "missing_critical_sections": missing_critical,
        "intake_answer_coverage": intake_coverage,
        "readiness_status": readiness_status,
        "scoring": {
            **scores,
            "priority_score": priority_score,
        },
        "merged_from": _extract_section_bullets(lines, "Merged from"),
        "sha256": _file_sha256(file_path),
        "updated": datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc).isoformat(),
    }


def _build_similarity_clusters(
    records: list[dict[str, Any]],
    merge_threshold: float,
    review_threshold: float,
) -> list[dict[str, Any]]:
    """Build pairwise duplicate candidates for merge/review queues."""
    active_records = [record for record in records if record.get("status") == "active" and record.get("idea_id")]
    clusters: list[dict[str, Any]] = []

    for left, right in itertools.combinations(active_records, 2):
        signals = _idea_similarity(left, right)
        score = signals["score"]
        if score < review_threshold:
            continue

        candidate_type = "merge_candidate" if score >= merge_threshold else "review_candidate"
        clusters.append(
            {
                "type": candidate_type,
                "score": score,
                "idea_ids": [left["idea_id"], right["idea_id"]],
                "paths": [left["source_path"], right["source_path"]],
                "signals": signals,
            }
        )

    clusters.sort(key=lambda item: (item["score"], item["idea_ids"][0], item["idea_ids"][1]), reverse=True)
    return clusters


def build_tracker_payload(
    repo_root: Path,
    offset: int = 0,
    limit: int | None = None,
    merge_threshold: float = 0.8,
    review_threshold: float = 0.6,
) -> dict[str, Any]:
    """Build idea tracker payload for active and archived ideas."""
    ideas_root = repo_root / "docs" / "project" / "ideas"
    archive_root = ideas_root / "archive"

    active_files_all = sorted(path for path in ideas_root.glob("idea*.md") if path.is_file())
    archived_files_all = sorted(path for path in archive_root.glob("idea*.md") if path.is_file())

    all_files_with_status: list[tuple[Path, bool]] = [(path, False) for path in active_files_all]
    all_files_with_status += [(path, True) for path in archived_files_all]

    scoped_start = max(offset, 0)
    scoped_end = None if limit is None else scoped_start + max(limit, 0)
    scoped = all_files_with_status[scoped_start:scoped_end]

    records: list[dict[str, Any]] = []
    for file_path, archived in scoped:
        records.append(_collect_idea_record(repo_root, file_path, archived=archived))

    records.sort(key=lambda item: (item.get("idea_id", ""), item.get("status", ""), item.get("source_path", "")))

    ids = [item["idea_id"] for item in records if item.get("idea_id")]
    duplicate_ids = sorted({idea_id for idea_id in ids if ids.count(idea_id) > 1})

    readiness_counts = {
        "ready": sum(1 for item in records if item.get("readiness_status") == "ready"),
        "needs-discovery": sum(1 for item in records if item.get("readiness_status") == "needs-discovery"),
        "blocked": sum(1 for item in records if item.get("readiness_status") == "blocked"),
    }

    similarity_clusters = _build_similarity_clusters(records, merge_threshold, review_threshold)
    merge_candidates = [item for item in similarity_clusters if item["type"] == "merge_candidate"]
    review_candidates = [item for item in similarity_clusters if item["type"] == "review_candidate"]

    active_count = sum(1 for item in records if item.get("status") == "active")
    archived_count = sum(1 for item in records if item.get("status") == "archived")

    return {
        "schema_version": 2,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "active_dir": "docs/project/ideas",
            "archive_dir": "docs/project/ideas/archive",
            "offset": scoped_start,
            "limit": limit,
            "available_total": len(all_files_with_status),
            "processed_total": len(records),
        },
        "summary": {
            "total": len(records),
            "active": active_count,
            "archived": archived_count,
            "unique_idea_ids": len(set(ids)),
            "duplicate_idea_ids": duplicate_ids,
            "readiness": readiness_counts,
            "merge_candidates": len(merge_candidates),
            "review_candidates": len(review_candidates),
        },
        "queues": {
            "ready": [item["idea_id"] for item in records if item.get("readiness_status") == "ready"],
            "needs-discovery": [
                item["idea_id"]
                for item in records
                if item.get("readiness_status") == "needs-discovery"
            ],
            "blocked": [item["idea_id"] for item in records if item.get("readiness_status") == "blocked"],
        },
        "duplicate_candidates": {
            "merge_candidates": merge_candidates,
            "review_candidates": review_candidates,
        },
        "ideas": records,
    }


def write_tracker(output_path: Path, payload: dict[str, Any]) -> None:
    """Write tracker JSON to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    """Build CLI parser."""
    parser = argparse.ArgumentParser(description="Track active and archived idea files in JSON format.")
    parser.add_argument(
        "--output",
        default="docs/project/ideatracker.json",
        help="Output JSON path relative to repo root (default: docs/project/ideatracker.json)",
    )
    parser.add_argument(
        "--repo-root",
        default=None,
        help="Optional repository root override.",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Start index for batch processing (default: 0).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional max number of ideas to process in this run.",
    )
    parser.add_argument(
        "--merge-threshold",
        type=float,
        default=0.8,
        help="Similarity threshold for merge candidates (default: 0.8).",
    )
    parser.add_argument(
        "--review-threshold",
        type=float,
        default=0.6,
        help="Similarity threshold for review candidates (default: 0.6).",
    )
    return parser


def main() -> int:
    """Entry point for the idea tracker generator."""
    parser = _build_parser()
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else _repo_root()
    output_path = (repo_root / args.output).resolve()

    payload = build_tracker_payload(
        repo_root,
        offset=args.offset,
        limit=args.limit,
        merge_threshold=args.merge_threshold,
        review_threshold=args.review_threshold,
    )
    write_tracker(output_path, payload)

    summary = payload["summary"]
    print(
        "IDEA_TRACKER_OK "
        f"total={summary['total']} active={summary['active']} archived={summary['archived']} "
        f"ready={summary['readiness']['ready']} needs_discovery={summary['readiness']['needs-discovery']} "
        f"blocked={summary['readiness']['blocked']} merge_candidates={summary['merge_candidates']} "
        f"review_candidates={summary['review_candidates']} output={output_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
