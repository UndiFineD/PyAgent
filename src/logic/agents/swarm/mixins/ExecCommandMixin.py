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

"""Command and git execution logic for OrchestratorAgent."""

from __future__ import annotations
import logging
import subprocess
import sys
from pathlib import Path
from contextlib import contextmanager

class ExecCommandMixin:
    """Mixin for fundamental command execution and git operations."""

    def _run_command(
        self, cmd: list[str], timeout: int = 120, max_retries: int = 1
    ) -> subprocess.CompletedProcess[str]:
        """Run a command with timeout, error handling, retry logic, and logging."""
        return getattr(self, "command_handler").run_command(cmd, timeout, max_retries)

    @contextmanager
    def _with_agent_env(self, agent_name: str):
        """Temporarily set environment variables for a specific agent."""
        with getattr(self, "command_handler").with_agent_env(agent_name):
            yield

    def run_stats_update(self, files: list[Path]) -> None:
        """Run stats update."""
        file_paths = [str(f) for f in files]
        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent.parent / "agent_stats.py"),
            "--files",
        ] + file_paths
        self._run_command(cmd)

    def run_tests(self, code_file: Path) -> None:
        """Run tests for the code file."""
        test_name = f"test_{code_file.stem}.py"
        tests_file = code_file.parent / test_name
        if tests_file.exists():
            logging.info(f"Running tests for {code_file.name}...")
            cmd = [sys.executable, "-m", "pytest", str(tests_file), "-v"]
            result = self._run_command(cmd)
            if result.returncode != 0:
                logging.warning(f"Tests failed for {code_file.name}:")
                logging.warning(result.stdout)
                logging.warning(result.stderr)
            else:
                logging.info(f"Tests passed for {code_file.name}")
        else:
            logging.debug(f"No tests file found for {code_file.name}")

    def _commit_and_push(self, code_file: Path) -> None:
        """Commit and push changes for the code file."""
        if getattr(self, "no_git", False):
            logging.info(f"Skipping git operations for {code_file.name} (--no-git)")
            return

        logging.info(f"Committing changes for {code_file.name}")
        try:
            self._run_command(["git", "add", "-A"])
            commit_msg = f"Agent improvements for {code_file.name}"
            result = self._run_command(["git", "commit", "-m", commit_msg])
            if result.returncode == 0:
                logging.info(f"Committed changes for {code_file.name}")
                push_result = self._run_command(["git", "push"])
                if push_result.returncode == 0:
                    logging.info(f"Pushed changes for {code_file.name}")
                else:
                    logging.error(f"Failed to push changes: {push_result.stderr}")
            else:
                logging.info(f"No changes to commit for {code_file.name}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Git operation failed for {code_file.name}: {e}")
        except FileNotFoundError:
            logging.error(f"Git not available for {code_file.name}")
