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


"""Auto-extracted class from agent.py"""

# pylint: disable=too-many-ancestors

from __future__ import annotations

import fnmatch
import logging
import subprocess
from pathlib import Path
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class GitBranchProcessor:
    """Process files changed in a specific git branch.

    Example:
        processor=GitBranchProcessor(repo_root)
        changed_files=processor.get_changed_files("feature-branch")
        for file in changed_files:
            process(file)
    """

    def __init__(self, repo_root: Path, recorder: Any = None) -> None:
        """Initialize processor.

        Args:
            repo_root: Repository root directory.
            recorder: Optional LocalContextRecorder.
        """
        self.repo_root = repo_root
        self.recorder = recorder

    def _record(self, action: str, result: str) -> None:
        """Record git operations if recorder is available."""
        if self.recorder:
            self.recorder.record_interaction(provider="Git", model="cli", prompt=action, result=result)

    def get_changed_files(
        self,
        branch: str,
        base_branch: str = "main",
        extensions: list[str] | None = None,
    ) -> list[Path]:
        """Get files changed in branch compared to base.

        Args:
            branch: Branch to check.
            base_branch: Base branch for comparison.
            extensions: File extensions to include (e.g., [".py", ".md"]).

        Returns:
            List of changed file paths.
        """
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", f"{base_branch}...{branch}"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            if result.returncode != 0:
                logging.warning(f"Git diff failed: {result.stderr}")
                self._record(f"git diff {base_branch}...{branch}", f"Failed: {result.stderr}")
                return []

            self._record(
                f"git diff {base_branch}...{branch}",
                f"Success: {len(result.stdout.strip().splitlines())} files",
            )
            files: list[Path] = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                file_path = self.repo_root / line
                if extensions:
                    if file_path.suffix in extensions:
                        files.append(file_path)
                else:
                    files.append(file_path)

            return files

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Error getting branch changes: {e}")
            return []

    def get_current_branch(self) -> str | None:
        """Get current git branch name."""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception:  # pylint: disable=broad-exception-caught
            return None

    def list_branches(self, pattern: str | None = None) -> list[str]:
        """List branches, optionally filtered by pattern.

        Args:
            pattern: Glob pattern to match branch names.

        Returns:
            List of branch names.
        """
        try:
            result = subprocess.run(
                ["git", "branch", "--list", "--format=%(refname:short)"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            if result.returncode != 0:
                return []

            branches = result.stdout.strip().split("\n")
            if pattern:
                branches = [b for b in branches if fnmatch.fnmatch(b, pattern)]

            return branches

        except Exception:  # pylint: disable=broad-exception-caught
            return []
