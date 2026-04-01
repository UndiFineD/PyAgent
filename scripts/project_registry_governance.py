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
import json
import re
import shutil
from datetime import date
from pathlib import Path
from typing import Any

LANES = ["Ideas", "Discovery", "Design", "In Sprint", "Review", "Released", "Archived"]
ID_RE = re.compile(r"^prj\d{7}$")


def _repo_root() -> Path:
    """Get the root path of the repository."""
    return Path(__file__).resolve().parents[1]


def _projects_path(root: Path) -> Path:
    """Get the path to the projects JSON file."""
    return root / "docs" / "project" / "kanban.json"


def _ideas_path(root: Path) -> Path:
    """Get the path to the ideas directory."""
    return root / "docs" / "project" / "ideas"


def _ideas_archive_path(root: Path) -> Path:
    """Get the path to the archive directory for ideas."""
    return _ideas_path(root) / "archive"


def _idea_tags(project: dict[str, Any]) -> list[str]:
    """Extract idea tags from a project dictionary."""
    tags = project.get("tags")
    if not isinstance(tags, list):
        return []
    return [str(tag) for tag in tags if isinstance(tag, str) and re.fullmatch(r"idea\d{6}", tag)]


def _archive_idea_files_for_project(root: Path, project: dict[str, Any]) -> list[str]:
    """Archive idea files for a specific project by moving them to the archive directory."""
    ideas_dir = _ideas_path(root)
    archive_dir = _ideas_archive_path(root)
    archive_dir.mkdir(parents=True, exist_ok=True)

    moved: list[str] = []
    for idea_tag in _idea_tags(project):
        for source in sorted(ideas_dir.glob(f"{idea_tag}-*.md")):
            target = archive_dir / source.name
            if target.exists():
                target.unlink()
            shutil.move(str(source), str(target))
            moved.append(source.name)
    return moved


def sync_idea_archive() -> int:
    """Sync the idea archive by moving released project ideas to the archive directory."""
    root = _repo_root()
    projects = _read_projects(_projects_path(root))

    moved_all: list[str] = []
    for project in projects:
        if project.get("lane") == "Released":
            moved_all.extend(_archive_idea_files_for_project(root, project))

    print(f"SYNC_IDEA_ARCHIVE moved={len(moved_all)}")
    if moved_all:
        for file_name in moved_all:
            print(f"- {file_name}")
    return 0


def _read_projects(path: Path) -> list[dict[str, Any]]:
    """Read the project data from the specified path."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        return [item for item in raw if isinstance(item, dict)]
    if isinstance(raw, dict):
        projects = raw.get("projects", [])
        if isinstance(projects, list):
            return [item for item in projects if isinstance(item, dict)]
    return []


def _write_projects(path: Path, projects: list[dict[str, Any]]) -> None:
    """Write the project data to the specified path, preserving existing structure if possible."""
    existing_raw: Any
    try:
        existing_raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        existing_raw = {}

    if isinstance(existing_raw, dict):
        payload: Any = {**existing_raw, "projects": projects}
    else:
        payload = projects

    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def validate() -> int:
    """Validate the JSON project registry and released-idea archival consistency."""
    root = _repo_root()
    projects = _read_projects(_projects_path(root))

    issues: list[str] = []

    # JSON basic checks
    ids = [p.get("id") for p in projects]
    if len(ids) != len(set(ids)):
        issues.append("Duplicate project IDs found in docs/project/kanban.json projects list")

    project_ids = {i for i in ids if isinstance(i, str)}

    # Released idea-backed projects must have their idea files archived.
    for project in projects:
        if project.get("lane") != "Released":
            continue
        for idea_tag in _idea_tags(project):
            in_ideas = list((_ideas_path(root)).glob(f"{idea_tag}-*.md"))
            in_archive = list((_ideas_archive_path(root)).glob(f"{idea_tag}-*.md"))
            if in_ideas:
                message = (
                    f"Released project {project.get('id')} has unarchived idea file(s) "
                    f"in docs/project/ideas for {idea_tag}"
                )
                issues.append(message)
            if not in_archive:
                message = (
                    f"Released project {project.get('id')} is missing archived idea file "
                    f"in docs/project/ideas/archive for {idea_tag}"
                )
                issues.append(message)

    if issues:
        print("VALIDATION_FAILED")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("VALIDATION_OK")
    print(f"projects={len(project_ids)}")
    return 0


def set_lane(project_id: str, lane: str, branch: str | None, pr: str | None) -> int:
    """Update a project's lane in the JSON registry."""
    if lane not in LANES:
        raise SystemExit(f"Invalid lane: {lane}. Expected one of: {', '.join(LANES)}")

    root = _repo_root()
    projects_path = _projects_path(root)
    projects = _read_projects(projects_path)
    entry = next((p for p in projects if p.get("id") == project_id), None)
    if entry is None:
        raise SystemExit(f"Unknown project id: {project_id}")

    entry["lane"] = lane
    entry["updated"] = date.today().isoformat()
    if branch is not None:
        entry["branch"] = branch
    if pr is not None:
        entry["pr"] = pr

    moved: list[str] = []
    if lane == "Released":
        moved = _archive_idea_files_for_project(root, entry)

    _write_projects(projects_path, projects)

    print(f"UPDATED {project_id} lane={lane}")
    if moved:
        print(f"ARCHIVED_IDEA_FILES {len(moved)}")
        for file_name in moved:
            print(f"- {file_name}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the project registry governance script."""
    parser = argparse.ArgumentParser(description="Govern docs/project/kanban.json project registry updates.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate", help="Validate project registry and released-idea archive consistency.")
    sub.add_parser("sync-idea-archive", help="Archive released project idea files under docs/project/ideas/archive.")

    set_lane_parser = sub.add_parser("set-lane", help="Update a project lane in docs/project/kanban.json.")
    set_lane_parser.add_argument("--id", required=True, help="Project ID (e.g., prj0000100)")
    set_lane_parser.add_argument("--lane", required=True, choices=LANES)
    set_lane_parser.add_argument("--branch", required=False, default=None)
    set_lane_parser.add_argument("--pr", required=False, default=None)

    return parser


def main() -> int:
    """Entry point for the project registry governance script."""
    parser = _build_parser()
    args = parser.parse_args()

    if args.cmd == "validate":
        return validate()

    if args.cmd == "set-lane":
        return set_lane(project_id=args.id, lane=args.lane, branch=args.branch, pr=args.pr)

    if args.cmd == "sync-idea-archive":
        return sync_idea_archive()

    parser.error(f"Unknown command: {args.cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
