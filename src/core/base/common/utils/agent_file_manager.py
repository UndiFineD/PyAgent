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
from src.core.base.lifecycle.version import VERSION
import os
import logging
import time
import hashlib
from pathlib import Path
from src.core.base.common.utils.core_utils import load_codeignore
from src.core.base.lifecycle.agent_core import BaseCore

__version__ = VERSION


class AgentFileManager:
    """Manages file discovery, filtering, and snapshots for the Agent."""

    SUPPORTED_EXTENSIONS = {".py", ".sh", ".js", ".ts", ".go", ".rb"}

    def __init__(
        self,
        repo_root: Path,
        agents_only: bool = False,
        ignored_patterns: set[str] | None = None,
    ) -> None:
        self.repo_root = repo_root
        self.agents_only = agents_only
        self.ignored_patterns = ignored_patterns or load_codeignore(repo_root)
        self.core = BaseCore(workspace_root=str(repo_root))

    def is_ignored(self, path: Path) -> bool:
        """Check if a path should be ignored based on .codeignore patterns."""
        return self.core.is_path_ignored(path, self.repo_root, self.ignored_patterns)

    def find_code_files(self, max_files: int | None = None) -> list[Path]:
        """Find code files in the repository, respecting filters and ignore patterns."""
        all_potential_files = []

        search_root = self.repo_root
        if self.agents_only:
            # Look for agent-specific directories
            for sub in ["scripts/agent", "src/agent", "src/agents"]:
                potential = self.repo_root / sub
                if potential.exists():
                    search_root = potential
                    break

        logging.info(f"Searching for code files in {search_root}")

        for root, _, files in os.walk(search_root):
            for file in files:
                all_potential_files.append(Path(root) / file)

        # Delegate filtering to core logic
        code_files = self.core.filter_code_files(
            all_potential_files,
            self.repo_root,
            self.ignored_patterns,
            self.SUPPORTED_EXTENSIONS,
        )

        # If agents_only is True and we're searching from the root,
        # further filter to only include files that appear to be part of the agent system
        if self.agents_only and search_root == self.repo_root:
            agent_keywords = {"agent", "coder", "optimizer", "handler", "collector", "engine", "benchmarking"}
            code_files = [
                f
                for f in code_files
                if f.parent != self.repo_root or any(kw in f.name.lower() for kw in agent_keywords)
            ]

        if max_files:
            return code_files[:max_files]

        return code_files

    def load_cascading_codeignore(self, directory: Path | None = None) -> set[str]:
        """Load .codeignore patterns with cascading support."""
        if directory is None:
            directory = self.repo_root

        all_patterns: set[str] = set()
        current_dir = directory.resolve()

        # Walk up to repo root, loading .codeignore files
        while current_dir >= self.repo_root:
            codeignore_file = current_dir / ".codeignore"
            if codeignore_file.exists():
                try:
                    patterns = load_codeignore(current_dir)
                    all_patterns.update(patterns)
                    logging.debug(
                        f"Loaded {len(patterns)} patterns from {codeignore_file}"
                    )
                except Exception as e:
                    logging.warning(f"Failed to load {codeignore_file}: {e}")

            # Stop at repo root
            if current_dir == self.repo_root:
                break

            current_dir = current_dir.parent

        logging.debug(f"Total cascading patterns from {directory}: {len(all_patterns)}")
        return all_patterns

    def create_file_snapshot(self, file_path: Path) -> str | None:
        """Create a snapshot of file content before modifications."""
        try:
            if not file_path.exists():
                logging.debug(f"Cannot snapshot non-existent file: {file_path}")
                return None

            # Create snapshots directory if needed
            snapshot_dir = self.repo_root / ".agent_snapshots"
            snapshot_dir.mkdir(exist_ok=True)

            # Generate snapshot ID based on timestamp
            content = file_path.read_text(encoding="utf-8", errors="replace")
            content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            snapshot_id = f"{time.time():.0f}_{content_hash}"

            # Save relative path and content
            rel_path = file_path.relative_to(self.repo_root)
            snapshot_file = snapshot_dir / f"{snapshot_id}_{rel_path.name}"
            snapshot_file.write_text(content, encoding="utf-8")

            logging.debug(f"Created snapshot {snapshot_id} for {rel_path}")
            return snapshot_id

        except Exception as e:
            logging.error(f"Failed to create snapshot for {file_path}: {e}")
            return None

    def restore_from_snapshot(self, file_path: Path, snapshot_id: str) -> bool:
        """Restore a file from a previously created snapshot."""
        try:
            snapshot_dir = self.repo_root / ".agent_snapshots"
            if not snapshot_dir.exists():
                logging.warning(f"Snapshot directory not found: {snapshot_dir}")
                return False

            # Find snapshot file matching pattern
            rel_path = file_path.relative_to(self.repo_root)
            pattern = f"{snapshot_id}_{rel_path.name}"

            snapshot_file = snapshot_dir / pattern
            if not snapshot_file.exists():
                logging.warning(f"Snapshot not found: {pattern}")
                return False

            # Restore content
            content = snapshot_file.read_text(encoding="utf-8")
            file_path.write_text(content, encoding="utf-8")

            logging.info(f"Restored {rel_path} from snapshot {snapshot_id}")
            return True

        except Exception as e:
            logging.error(f"Failed to restore snapshot for {file_path}: {e}")
            return False

    def cleanup_old_snapshots(
        self, max_age_days: int = 7, max_snapshots_per_file: int = 10
    ) -> int:
        """Clean up old file snapshots according to retention policy."""
        snapshot_dir = self.repo_root / ".agent_snapshots"
        if not snapshot_dir.exists():
            logging.debug("No snapshot directory found, nothing to clean")
            return 0

        try:
            current_time = time.time()
            max_age_seconds = max_age_days * 24 * 60 * 60

            snapshots_by_file = self._group_snapshots_by_filename(snapshot_dir)
            deleted_count = self._prune_snapshot_groups(
                snapshots_by_file, current_time, max_age_seconds, max_snapshots_per_file
            )

            logging.info(f"Cleaned up {deleted_count} old snapshots")
            return deleted_count

        except Exception as e:
            logging.error(f"Failed to cleanup snapshots: {e}")
            return 0

    def _group_snapshots_by_filename(self, snapshot_dir: Path) -> dict[str, list[Path]]:
        """Helper to group snapshot files by their original filename."""
        groups: dict[str, list[Path]] = {}
        for snapshot_file in snapshot_dir.glob("*"):
            if snapshot_file.is_file():
                parts = snapshot_file.name.split("_", 2)
                if len(parts) >= 3:
                    filename = parts[2]
                    if filename not in groups:
                        groups[filename] = []
                    groups[filename].append(snapshot_file)
        return groups

    def _prune_snapshot_groups(
        self,
        groups: dict[str, list[Path]],
        current_time: float,
        max_age_seconds: int,
        max_count: int,
    ) -> int:
        """Helper to prune snapshot files based on age and count limits."""
        deleted = 0
        for filename, snapshots in groups.items():
            # Sort by modification time (newest first)
            snapshots.sort(key=lambda x: x.stat().st_mtime, reverse=True)

            for i, snapshot in enumerate(snapshots):
                mtime = snapshot.stat().st_mtime
                if (current_time - mtime) > max_age_seconds or i >= max_count:
                    try:
                        snapshot.unlink()
                        deleted += 1
                        logging.debug(f"Deleted snapshot: {snapshot.name}")
                    except Exception:
                        pass
        return deleted
