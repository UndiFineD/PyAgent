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
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast

from scripts.idea_tracker_artifacts import write_json
from scripts.idea_tracker_pipeline import run_incremental_tracker, write_split_tracker_chunks

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

# Stop-words excluded from title-based blocking keys.
_STOP_WORDS: frozenset[str] = frozenset(
    {"a", "an", "the", "of", "in", "for", "and", "or", "to", "with", "at", "by", "from"}
)


def _log(msg: str) -> None:
    """Write a progress message to stderr, flushing immediately.

    Args:
        msg: The progress message to emit.

    """
    print(msg, file=sys.stderr, flush=True)


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
        "section_names": sorted(section_names),
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


def _blocking_keys(record: dict[str, Any]) -> list[str]:
    """Return blocking keys for a record used in scalable candidate narrowing.

    Two records are only compared if they share at least one blocking key.
    Primary keys are derived from shared ``planned_project_ids``.  When a
    record has no project mapping the fallback is the first significant
    (non-stop-word) title token.

    Args:
        record: Idea record dict as produced by ``_collect_idea_record``.

    Returns:
        Non-empty list of string blocking keys.

    """
    keys: list[str] = []
    planned_project_ids = cast(list[str], record.get("planned_project_ids") or [])
    for pid in planned_project_ids:
        normalized_pid = pid.lower()
        keys.append(f"proj:{normalized_pid}")
    if not keys:
        tokens = [t for t in _tokenize(record.get("title", "")) if t not in _STOP_WORDS]
        keys.append(f"title:{tokens[0]}" if tokens else "title:_ungrouped_")
    return keys


def build_tracker_payload(
    repo_root: Path,
    offset: int = 0,
    limit: int | None = None,
    merge_threshold: float = 0.8,
    review_threshold: float = 0.6,
    batch_size: int = 1000,
    verbose: bool = False,
    checkpoint_output_path: Path | None = None,
) -> dict[str, Any]:
    """Build idea tracker payload for active and archived ideas.

    Args:
        repo_root: Repository root path.
        offset: Start index into the combined sorted file list.
        limit: Maximum number of files to process; None means all.
        merge_threshold: Similarity score at or above which a pair is a merge candidate.
        review_threshold: Minimum similarity score for a review candidate.
        batch_size: Emit a stderr progress line every this many files when *verbose*.
        verbose: When True, log collection and similarity progress to stderr.
        checkpoint_output_path: Optional output file path to write progress checkpoints.

    Returns:
        Tracker payload dict with schema_version 2.

    """
    return run_incremental_tracker(
        repo_root,
        offset=offset,
        limit=limit,
        merge_threshold=merge_threshold,
        review_threshold=review_threshold,
        batch_size=batch_size,
        verbose=verbose,
        output_path=checkpoint_output_path,
        collect_record=_collect_idea_record,
        tokenize=_tokenize,
        blocking_keys=_blocking_keys,
        log=_log,
    )


def write_tracker(output_path: Path, payload: dict[str, Any]) -> None:
    """Write tracker JSON to disk.

    Args:
        output_path: Output file path.
        payload: JSON payload to write.

    """
    write_json(output_path, payload)


def _write_split_tracker_chunks(output_path: Path, payload: dict[str, Any], chunk_size: int) -> int:
    """Write split tracker chunk files named ``<stem>-NNNNNN.json``.

    Args:
        output_path: Main tracker output file path.
        payload: Final tracker payload.
        chunk_size: Number of idea records per split file.

    Returns:
        Number of chunk files written.

    """
    return write_split_tracker_chunks(output_path, payload, chunk_size)


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
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        dest="batch_size",
        help="Log progress every N files during collection (default: 1000).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Emit progress messages to stderr during long runs.",
    )
    parser.add_argument(
        "--split-output",
        action="store_true",
        default=True,
        help="Also write split chunk files as <output-stem>-NNNNNN.json using --batch-size.",
    )
    parser.add_argument(
        "--no-split-output",
        action="store_false",
        dest="split_output",
        help="Disable split chunk output files.",
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
        batch_size=args.batch_size,
        verbose=args.verbose,
        checkpoint_output_path=output_path,
    )
    write_tracker(output_path, payload)
    split_count = 0
    if args.split_output:
        split_count = _write_split_tracker_chunks(output_path, payload, args.batch_size)

    summary = payload["summary"]
    print(
        "IDEA_TRACKER_OK "
        f"total={summary['total']} active={summary['active']} archived={summary['archived']} "
        f"ready={summary['readiness']['ready']} needs_discovery={summary['readiness']['needs-discovery']} "
        f"blocked={summary['readiness']['blocked']} merge_candidates={summary['merge_candidates']} "
        f"review_candidates={summary['review_candidates']} output={output_path} split_files={split_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
