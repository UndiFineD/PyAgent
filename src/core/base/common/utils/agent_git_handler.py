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

"""
Manager for git operations.
(Facade for src.core.base.common.git_core)
"""

import logging
from pathlib import Path
from typing import Any

from src.core.base.common.shell_core import ShellCore


class AgentGitHandler:
    """Facade for Git operations with recording support."""

    def __init__(self, repo_root: Path, no_git: bool = False, recorder: Any = None) -> None:
        self.repo_root: Path = repo_root
        self.no_git: bool = no_git
        self.recorder: Any = recorder
        self.shell = ShellCore(repo_root=repo_root)

    def _record(self, action: str, result: str, meta: dict[str, Any] | None = None) -> None:
        """Internal helper to record git operations if recorder is available."""
        if self.recorder:
            self.recorder.record_interaction(provider="Git", model="cli", prompt=action, result=result, meta=meta)

    def commit_changes(self, message: str, files: list[str] | None = None) -> None:
        """Commit changes to the repository."""
        if self.no_git:
            logging.info(f"Skipping git commit: no_git=True. Message: {message}")
            return

        try:
            if files:
                for file in files:
                    self.shell.execute(["git", "add", file], check=True)
            else:
                self.shell.execute(["git", "add", "."], check=True)

            # Check if there are changes to commit
            res = self.shell.execute(["git", "status", "--porcelain"])
            status = res.stdout.strip()

            if not status:
                logging.info("No changes to commit.")
                return

            res = self.shell.execute(["git", "commit", "-m", message], check=True)
            logging.info("Successfully committed changes: %s", message)
            self._record(f"commit: {message}", "success", {"files": files})
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error("Error during git commit: %s", e)
            self._record(f"commit: {message}", f"error: {str(e)}")

    def create_branch(self, branch_name: str) -> bool:
        """Create and switch to a new branch."""
        if self.no_git:
            return False
        try:
            self.shell.execute(["git", "checkout", "-b", branch_name], check=True)
            logging.info(f"Created branch: {branch_name}")
            return True
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Failed to create branch {branch_name}: {e}")
            return False
