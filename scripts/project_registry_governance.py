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
from datetime import date
from pathlib import Path
from typing import Any

LANES = ["Ideas", "Discovery", "Design", "In Sprint", "Review", "Released", "Archived"]
ID_RE = re.compile(r"^prj\d{7}$")


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _projects_path(root: Path) -> Path:
    return root / "data" / "projects.json"


def _kanban_path(root: Path) -> Path:
    return root / "docs" / "project" / "kanban.md"


def _read_projects(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_projects(path: Path, projects: list[dict[str, Any]]) -> None:
    path.write_text(json.dumps(projects, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _table_cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _lane_heading_index(lines: list[str], lane: str) -> int:
    heading = f"## {lane}"
    for idx, line in enumerate(lines):
        if line.strip() == heading:
            return idx
    raise ValueError(f"Missing lane heading: {heading}")


def _summary_heading_index(lines: list[str]) -> int:
    for idx, line in enumerate(lines):
        if line.strip() == "## Summary Metrics":
            return idx
    raise ValueError("Missing '## Summary Metrics' heading")


def _lane_region(lines: list[str], lane: str) -> tuple[int, int]:
    start = _lane_heading_index(lines, lane)
    candidate_ends = [len(lines)]
    for other in LANES:
        if other == lane:
            continue
        try:
            idx = _lane_heading_index(lines, other)
            if idx > start:
                candidate_ends.append(idx)
        except ValueError:
            pass
    try:
        sm = _summary_heading_index(lines)
        if sm > start:
            candidate_ends.append(sm)
    except ValueError:
        pass
    return start, min(candidate_ends)


def _find_lane_table(lines: list[str], lane: str) -> tuple[int, int, int, int]:
    start, end = _lane_region(lines, lane)
    header_idx = -1
    sep_idx = -1
    for i in range(start, end):
        if lines[i].lstrip().startswith("| ID "):
            header_idx = i
            if i + 1 < end and lines[i + 1].lstrip().startswith("|---"):
                sep_idx = i + 1
            break
    if header_idx < 0 or sep_idx < 0:
        raise ValueError(f"Missing table header in lane section: {lane}")

    row_start = sep_idx + 1
    row_end = row_start
    while row_end < end:
        cur = lines[row_end].strip()
        if cur.startswith("## ") or cur == "---":
            break
        row_end += 1
    return start, end, row_start, row_end


def _parse_lane_rows(lines: list[str], lane: str) -> dict[str, str]:
    _, _, row_start, row_end = _find_lane_table(lines, lane)
    rows: dict[str, str] = {}
    for i in range(row_start, row_end):
        line = lines[i].strip()
        if not line.startswith("| prj"):
            continue
        cells = _table_cells(line)
        if cells and ID_RE.match(cells[0]):
            rows[cells[0]] = line
    return rows


def _all_kanban_rows(lines: list[str]) -> dict[str, str]:
    merged: dict[str, str] = {}
    for lane in LANES:
        merged.update(_parse_lane_rows(lines, lane))
    return merged


def _format_pr(pr_value: Any) -> str:
    if pr_value is None:
        return "pending"
    text = str(pr_value).strip()
    if not text:
        return "pending"
    if "[" in text and "](" in text:
        return text
    refs = re.findall(r"#(\d+)", text)
    if not refs:
        return text
    return " ".join(f"[#{n}](https://github.com/UndiFineD/PyAgent/pull/{n})" for n in refs)


def _lane_row_from_project(lines: list[str], lane: str, project: dict[str, Any]) -> str:
    _, _, _, _ = _find_lane_table(lines, lane)
    # Find header columns
    start, end = _lane_region(lines, lane)
    header_line = next(line for line in lines[start:end] if line.lstrip().startswith("| ID "))
    columns = _table_cells(header_line)

    tags = project.get("tags") or []
    tags_text = ", ".join(tags) if isinstance(tags, list) else str(tags)

    value_map = {
        "id": project.get("id", "—"),
        "name": project.get("name", "—"),
        "summary": project.get("summary", "—"),
        "branch": project.get("branch") or "—",
        "pr": _format_pr(project.get("pr")),
        "priority": project.get("priority", "P3"),
        "budget": project.get("budget_tier", "unknown"),
        "budget tier": project.get("budget_tier", "unknown"),
        "tags": tags_text,
        "updated": project.get("updated") or date.today().isoformat(),
        "released": project.get("updated") or date.today().isoformat(),
        "reason": project.get("reason") or "—",
    }

    values: list[str] = []
    for col in columns:
        key = col.lower().strip()
        values.append(str(value_map.get(key, "—")))

    return "| " + " | ".join(values) + " |"


def _remove_project_row_everywhere(lines: list[str], project_id: str) -> list[str]:
    out: list[str] = []
    needle = f"| {project_id} "
    for line in lines:
        if line.strip().startswith(needle):
            continue
        out.append(line)
    return out


def _insert_row_in_lane(lines: list[str], lane: str, row: str) -> list[str]:
    _, _, row_start, row_end = _find_lane_table(lines, lane)
    insert_at = row_end
    return lines[:insert_at] + [row] + lines[insert_at:]


def _refresh_summary_metrics(lines: list[str], projects: list[dict[str, Any]]) -> list[str]:
    counts = {lane: 0 for lane in LANES}
    for p in projects:
        lane = p.get("lane")
        if lane in counts:
            counts[lane] += 1

    out = lines[:]
    try:
        sm_idx = _summary_heading_index(out)
    except ValueError:
        return out

    # Rewrite top status line if present.
    for i in range(min(6, len(out))):
        if out[i].strip().startswith("_Last updated:"):
            out[i] = (
                f"_Last updated: {date.today().isoformat()} | Total projects: {len(projects)} "
                f"| Auto-synced by project_registry_governance.py "
                f"(Discovery: {counts['Discovery']}, Review: {counts['Review']}, Released: {counts['Released']})_"
            )
            break

    # Find Summary Metrics table rows and replace lane count rows.
    table_header = -1
    for i in range(sm_idx, len(out)):
        if out[i].lstrip().startswith("| Lane "):
            table_header = i
            break
    if table_header < 0:
        return out

    row_idx = table_header + 2
    while row_idx < len(out):
        line = out[row_idx].strip()
        if not line.startswith("|"):
            break
        cells = _table_cells(line)
        if len(cells) >= 2:
            lane_name = cells[0]
            if lane_name in counts:
                out[row_idx] = f"| {lane_name} | {counts[lane_name]} |"
            elif lane_name == "**Total**":
                out[row_idx] = f"| **Total** | **{len(projects)}** |"
        row_idx += 1

    return out


def validate() -> int:
    root = _repo_root()
    projects = _read_projects(_projects_path(root))
    kanban_lines = _kanban_path(root).read_text(encoding="utf-8").splitlines()

    issues: list[str] = []

    # JSON basic checks
    ids = [p.get("id") for p in projects]
    if len(ids) != len(set(ids)):
        issues.append("Duplicate project IDs found in data/projects.json")

    project_ids = {i for i in ids if isinstance(i, str)}
    lane_by_id = {p.get("id"): p.get("lane") for p in projects if isinstance(p.get("id"), str)}

    kanban_rows_by_lane = {lane: _parse_lane_rows(kanban_lines, lane) for lane in LANES}
    kanban_ids = {pid for rows in kanban_rows_by_lane.values() for pid in rows.keys()}

    missing_in_kanban = sorted(project_ids - kanban_ids)
    missing_in_json = sorted(kanban_ids - project_ids)
    if missing_in_kanban:
        issues.append(f"Projects in JSON but not in kanban: {missing_in_kanban[:10]}")
    if missing_in_json:
        issues.append(f"Projects in kanban but not in JSON: {missing_in_json[:10]}")

    for lane, rows in kanban_rows_by_lane.items():
        for pid in rows:
            if lane_by_id.get(pid) != lane:
                issues.append(f"Lane mismatch for {pid}: json={lane_by_id.get(pid)!r}, kanban={lane!r}")

    if issues:
        print("VALIDATION_FAILED")
        for issue in issues:
            print(f"- {issue}")
        return 1

    print("VALIDATION_OK")
    print(f"projects={len(project_ids)} kanban_rows={len(kanban_ids)}")
    return 0


def set_lane(project_id: str, lane: str, branch: str | None, pr: str | None) -> int:
    if lane not in LANES:
        raise SystemExit(f"Invalid lane: {lane}. Expected one of: {', '.join(LANES)}")

    root = _repo_root()
    projects_path = _projects_path(root)
    kanban_path = _kanban_path(root)

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

    _write_projects(projects_path, projects)

    lines = kanban_path.read_text(encoding="utf-8").splitlines()
    lines = _remove_project_row_everywhere(lines, project_id)
    row = _lane_row_from_project(lines, lane, entry)
    lines = _insert_row_in_lane(lines, lane, row)
    lines = _refresh_summary_metrics(lines, projects)
    kanban_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    print(f"UPDATED {project_id} lane={lane}")
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Govern docs/project/kanban.md and data/projects.json updates.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("validate", help="Validate consistency between projects.json and kanban lanes.")

    set_lane_parser = sub.add_parser("set-lane", help="Update a project lane and sync both projects.json + kanban.")
    set_lane_parser.add_argument("--id", required=True, help="Project ID (e.g., prj0000100)")
    set_lane_parser.add_argument("--lane", required=True, choices=LANES)
    set_lane_parser.add_argument("--branch", required=False, default=None)
    set_lane_parser.add_argument("--pr", required=False, default=None)

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.cmd == "validate":
        return validate()

    if args.cmd == "set-lane":
        return set_lane(project_id=args.id, lane=args.lane, branch=args.branch, pr=args.pr)

    parser.error(f"Unknown command: {args.cmd}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
