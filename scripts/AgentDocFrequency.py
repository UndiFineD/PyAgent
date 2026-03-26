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
"""AgentDocFrequency — analyse how often agent memory docs are updated.

Scans ``docs/agents/*.memory.md`` files, queries git log for each, and
reports update frequency, last-update date, and a staleness score.

Usage::

    python scripts/AgentDocFrequency.py [--docs-dir <path>] [--days-stale <n>]

Staleness score: days since last commit / ``--days-stale`` threshold (capped at 1.0).
A score of 1.0 means the file is at or beyond the staleness threshold.
"""
from __future__ import annotations

import argparse
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass
class DocStats:
    """Statistics for a single agent memory doc."""

    name: str
    path: Path
    commit_count: int = 0
    last_updated: datetime | None = None
    staleness: float = 1.0  # 0.0 = fresh, 1.0 = stale / never committed


def _git_log_count(path: Path, repo_root: Path) -> int:
    """Return the number of commits that touched *path*."""
    try:
        result = subprocess.run(  # noqa: S603
            ["git", "log", "--oneline", "--follow", "--", str(path.relative_to(repo_root))],  # noqa: S607
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=10,
        )
        lines = [l for l in result.stdout.splitlines() if l.strip()]
        return len(lines)
    except Exception:
        return 0


def _git_last_modified(path: Path, repo_root: Path) -> datetime | None:
    """Return the UTC datetime of the most recent commit that touched *path*."""
    try:
        result = subprocess.run(  # noqa: S603
            ["git", "log", "-1", "--format=%cI", "--follow", "--", str(path.relative_to(repo_root))],  # noqa: S607
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=10,
        )
        ts = result.stdout.strip()
        if not ts:
            return None
        return datetime.fromisoformat(ts)
    except Exception:
        return None


def analyse_docs(
    docs_dir: Path,
    repo_root: Path | None = None,
    days_stale: int = 30,
) -> list[DocStats]:
    """Analyse all ``*.memory.md`` files under *docs_dir*.

    Args:
        docs_dir: Directory containing agent memory files.
        repo_root: Git repository root.  Defaults to the parent of ``docs_dir``.
        days_stale: Age in days at which a file is considered fully stale.

    Returns:
        List of :class:`DocStats`, sorted by staleness (highest first).
    """
    if repo_root is None:
        repo_root = docs_dir.parent

    now = datetime.now(timezone.utc)
    results: list[DocStats] = []

    for md_file in sorted(docs_dir.glob("*.memory.md")):
        stats = DocStats(name=md_file.name, path=md_file)
        stats.commit_count = _git_log_count(md_file, repo_root)
        stats.last_updated = _git_last_modified(md_file, repo_root)

        if stats.last_updated is None:
            stats.staleness = 1.0
        else:
            last = stats.last_updated
            if last.tzinfo is None:
                last = last.replace(tzinfo=timezone.utc)
            age_days = (now - last).total_seconds() / 86400
            stats.staleness = min(1.0, age_days / days_stale)

        results.append(stats)

    results.sort(key=lambda s: s.staleness, reverse=True)
    return results


def format_table(stats: list[DocStats]) -> str:
    """Render *stats* as a Markdown pipe table."""
    header = "| File | Commits | Last Updated | Staleness |"
    sep = "|------|---------|--------------|-----------|"
    rows = [header, sep]
    for s in stats:
        last = s.last_updated.strftime("%Y-%m-%d") if s.last_updated else "never"
        stale = f"{s.staleness:.2f}"
        rows.append(f"| {s.name} | {s.commit_count} | {last} | {stale} |")
    return "\n".join(rows)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Analyse agent doc update frequency.")
    parser.add_argument(
        "--docs-dir",
        default=".github/agents/data",
        help="Path to the agent docs directory (default: .github/agents/data).",
    )
    parser.add_argument(
        "--days-stale",
        type=int,
        default=30,
        help="Days threshold for full staleness (default: 30).",
    )
    args = parser.parse_args()

    docs_dir = Path(args.docs_dir)
    if not docs_dir.exists():
        print(f"ERROR: docs dir not found: {docs_dir}")
        raise SystemExit(1)

    stats = analyse_docs(docs_dir, days_stale=args.days_stale)
    print(format_table(stats))
    print(f"\nTotal docs analysed: {len(stats)}")
    stale_count = sum(1 for s in stats if s.staleness >= 1.0)
    print(f"Stale (score 1.0): {stale_count}")


if __name__ == "__main__":
    main()
