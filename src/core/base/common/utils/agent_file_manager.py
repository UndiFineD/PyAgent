#!/usr/bin/env python3
from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Manager for agent files and discovery.
"""

"""
import fnmatch
import hashlib
import logging
import time
from pathlib import Path
from typing import List, Optional, Set

from .core_utils import load_codeignore

logger = logging.getLogger("pyagent.file_manager")


class AgentFileManager:
"""
Manages file discovery, filtering, and snapshots for the Agent.""
SUPPORTED_EXTENSIONS = {".py", ".sh", ".js", ".ts", ".go", ".rb"}

    def __init__(
        self,
        repo_root: Path,
        agents_only: bool = False,
        ignored_patterns: Set[str] | None = None,
    ) -> None:
        self.repo_root = Path(repo_root)
        self.agents_only = agents_only
        self.ignored_patterns = ignored_patterns or load_codeignore(self.repo_root)


    def find_code_files(self, max_files: Optional[int] = None) -> List[Path]:
"""
Finds all code files relevant to the current agent context.""
found: List[Path] = []

        if not self.repo_root.exists():
            return []

        for path in self.repo_root.rglob("*"):
            if path.is_dir():
                continue

            if path.suffix not in self.SUPPORTED_EXTENSIONS:
                continue

            try:
                rel_path = path.relative_to(self.repo_root)
            except ValueError:
                rel_path = path

            rel_str = str(rel_path).replace("\\", "/")
            should_ignore = False
            for pat in self.ignored_patterns:
                if fnmatch.fnmatch(rel_str, pat) or fnmatch.fnmatch(path.name, pat) or any(
                    fnmatch.fnmatch(str(p).replace("\\", "/"), pat) for p in rel_path.parents
                ):
                    should_ignore = True
                    break

            if should_ignore:
                continue

            if self.agents_only:
                if path.name.startswith("test_") and "agent" not in path.name.lower():
                    continue
                if "random_helper" in path.name:
                    continue

            found.append(path)

        found.sort()

        if max_files:
            found = found[:max_files]

        return found


    def create_snapshot(self, file_path: Path) -> Optional[str]:
"""
Creates a timestamped snapshot of a file.

        Returns a snapshot id string, or None on failure.
"""
try:
            if not file_path.exists():
                return None
            snapshot_dir = self.repo_root / ".agent_snapshots"
            snapshot_dir.mkdir(exist_ok=True)
            content = file_path.read_text(encoding="utf-8", errors="replace")
            content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
            snapshot_id = f"{int(time.time())}_{content_hash}"
            snapshot_file = snapshot_dir / f"{snapshot_id}_{file_path.name}"
            snapshot_file.write_text(content, encoding="utf-8")
            return snapshot_id
        except Exception as e:
            logger.error("Snapshot failed: %s", e)
            return None


    def restore_from_snapshot(self, file_path: Path, snapshot_id: str) -> bool:
"""
Restores a file from a snapshot.

        Returns True on success, False otherwise.
"""
try:
            snapshot_dir = self.repo_root / ".agent_snapshots"
            matches = list(snapshot_dir.glob(f"{snapshot_id}_{file_path.name}"))
            if not matches:
                return False
            content = matches[0].read_text(encoding="utf-8")
            file_path.write_text(content, encoding="utf-8")
            return True
        except Exception as e:
            logger.error("Restore failed: %s", e)
            return False
