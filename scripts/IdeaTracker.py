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
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

IDEA_ID_RE = re.compile(r"(idea\d{6})", re.IGNORECASE)
PLANNED_MAPPING_RE = re.compile(r"^Planned project mapping:\s*(.+)$", re.IGNORECASE)
PROJECT_ID_RE = re.compile(r"prj\d{7}", re.IGNORECASE)


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

    return {
        "idea_id": idea_id,
        "title": _extract_title(lines),
        "slug": slug,
        "status": "archived" if archived else "active",
        "source_path": relative_path,
        "planned_project_ids": _extract_planned_mappings(lines),
        "source_references": _extract_source_references(lines),
        "sha256": _file_sha256(file_path),
        "updated": datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc).isoformat(),
    }


def build_tracker_payload(repo_root: Path) -> dict[str, Any]:
    """Build idea tracker payload for active and archived ideas."""
    ideas_root = repo_root / "docs" / "project" / "ideas"
    archive_root = ideas_root / "archive"

    active_files = sorted(path for path in ideas_root.glob("idea*.md") if path.is_file())
    archived_files = sorted(path for path in archive_root.glob("idea*.md") if path.is_file())

    records: list[dict[str, Any]] = []
    for file_path in active_files:
        records.append(_collect_idea_record(repo_root, file_path, archived=False))
    for file_path in archived_files:
        records.append(_collect_idea_record(repo_root, file_path, archived=True))

    records.sort(key=lambda item: (item.get("idea_id", ""), item.get("status", ""), item.get("source_path", "")))

    ids = [item["idea_id"] for item in records if item.get("idea_id")]
    duplicate_ids = sorted({idea_id for idea_id in ids if ids.count(idea_id) > 1})

    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "active_dir": "docs/project/ideas",
            "archive_dir": "docs/project/ideas/archive",
        },
        "summary": {
            "total": len(records),
            "active": len(active_files),
            "archived": len(archived_files),
            "unique_idea_ids": len(set(ids)),
            "duplicate_idea_ids": duplicate_ids,
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
    return parser


def main() -> int:
    """Entry point for the idea tracker generator."""
    parser = _build_parser()
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve() if args.repo_root else _repo_root()
    output_path = (repo_root / args.output).resolve()

    payload = build_tracker_payload(repo_root)
    write_tracker(output_path, payload)

    summary = payload["summary"]
    print(
        "IDEA_TRACKER_OK "
        f"total={summary['total']} active={summary['active']} archived={summary['archived']} "
        f"output={output_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
