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
"""Regenerate dynamic README statistics from the project registry.

This script keeps high-churn numeric references in README.md in sync with
`docs/project/kanban.json` while preserving all other manual README content.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def _load_project_counts(projects_path: Path) -> tuple[int, int]:
    """Load project counts from the project registry JSON.

    Args:
       projects_path: Path to the project registry JSON file.

    Returns:
       A tuple containing the total number of projects and the number of
       released projects.

    """
    raw = json.loads(projects_path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        projects = [item for item in raw if isinstance(item, dict)]
    elif isinstance(raw, dict) and isinstance(raw.get("projects"), list):
        projects = [item for item in raw["projects"] if isinstance(item, dict)]
    else:
        projects = []
    total = len(projects)
    released = sum(1 for item in projects if str(item.get("lane", "")).lower() == "released")
    return total, released


def _update_readme_counts(content: str, total_projects: int, released_projects: int) -> str:
    """Update dynamic project counters in README content.

    Args:
       content: Original README content.
       total_projects: Total number of projects.
       released_projects: Number of released projects.

    Returns:
       Updated README content with dynamic project counters.

    """
    updated = re.sub(
        r"covering the \d+ projects that have been delivered",
        f"covering the {released_projects} projects that have been delivered",
        content,
    )
    updated = re.sub(
        r"through \d+ focused projects",
        f"through {total_projects} focused projects",
        updated,
    )
    return updated


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the README update script."""
    parser = argparse.ArgumentParser(
        description="Update dynamic project counters in README.md from docs/project/kanban.json.",
    )
    parser.add_argument(
        "--readme",
        type=Path,
        default=Path("README.md"),
        help="Path to README markdown file (default: README.md).",
    )
    parser.add_argument(
        "--projects",
        type=Path,
        default=Path("docs/project/kanban.json"),
        help="Path to project registry JSON (default: docs/project/kanban.json).",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with status 1 if README would change.",
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point for the README update script."""
    args = _parse_args()
    readme_path = args.readme.resolve()
    projects_path = args.projects.resolve()

    if not readme_path.exists():
        raise FileNotFoundError(f"README not found: {readme_path}")
    if not projects_path.exists():
        raise FileNotFoundError(f"Project registry not found: {projects_path}")

    total_projects, released_projects = _load_project_counts(projects_path)
    original = readme_path.read_text(encoding="utf-8")
    updated = _update_readme_counts(original, total_projects=total_projects, released_projects=released_projects)

    if original == updated:
        print("README already up to date.")
        return 0

    if args.check:
        print("README is out of date. Run scripts/write_readme.py to update it.")
        return 1

    readme_path.write_text(updated, encoding="utf-8")
    print(
        f"Updated {readme_path} using {projects_path} "
        f"(total_projects={total_projects}, released_projects={released_projects})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
