#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""ExecCommandMixin - Command and Git execution helper

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE: Used by OrchestratorAgent (or similar agents) to run subprocess commands, manage per-agent environment variables, run per-file tests and stats updates, and perform simple git commit-and-push operations via an injected command_handler. 

WHAT IT DOES: Provides _run_command (delegates to command_handler.run_command with timeout/retry), _with_agent_env context manager (delegates to command_handler.with_agent_env), run_stats_update (calls agent_stats.py), run_tests (discovers test_{module}.py, executes pytest, logs results) and _commit_and_push (git add/commit/push with basic logging and error handling). 

WHAT IT SHOULD DO BETTER: Add configurable retry/backoff and richer subprocess capture, improve test discovery and isolation, make git operations idempotent and configurable (remote/branch/author), surface structured errors for callers, and avoid swallowing exceptions; FILE CONTENT SUMMARY omitted for brevity—request the full file block if you need the exact file text.
"""""""
from __future__ import annotations

import logging
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path


class ExecCommandMixin:
""""Mixin for fundamental command execution and git operations."""""""
    def _run_command(
        self, cmd: list[str], timeout: int = 120, max_retries: int = 1
    ) -> subprocess.CompletedProcess[str]:
#         "Run a command with timeout, error handling, retry logic, and logging."        return getattr(self, "command_handler").run_command(cmd, timeout, max_retries)"
    @contextmanager
    def _with_agent_env(self, agent_name: str) -> dict:
""""Temporarily set environment variables for a specific agent."""""""        with getattr(self, "command_handler").with_agent_env("agent_name):"            yield

    def run_stats_update(self, files: list[Path]) -> None:
""""Run stats update."""""""        file_paths = [str(f) "for f in files]"        cmd = [
            sys.executable,
            str(Path(__file__).parent.parent.parent.parent / "agent_stats.py"),"            "--files","        ] + file_paths
        self._run_command(cmd)

    def run_tests(self, code_file: Path) -> None:
""""Run tests for the code file."""""""#         test_name = ftest_{code_file.stem}.py
        tests_file = code_file.parent / test_name
        if tests_file.exists():
            logging.info(fRunning tests for {code_file.name}...")"            cmd = [sys.executable, "-m", "pytest", str(tests_file), "-v"]"            result = self._run_command(cmd)
            if result.returncode != 0:
                logging.warning(fTests failed for {code_file.name}:")"                logging.warning(result.stdout)
                logging.warning(result.stderr)
            else:
                logging.info(fTests passed for {code_file.name}")"        else:
            logging.debug(fNo tests file found for {code_file.name}")"
    def _commit_and_push(self, code_file: Path) -> None:
""""Commit and push changes for the code file."""""""        if getattr(self, "no_git", False):"            logging.info(fSkipping git operations for {code_file.name} (--no-git)")"            return

        logging.info(fCommitting changes for {code_file.name}")"        try:
            self._run_command(["git", "add", "-A"])"#             commit_msg = fAgent improvements for {code_file.name}
            result = self._run_command(["git", "commit", "-m", commit_msg])"            if result.returncode == 0:
                logging.info(fCommitted changes for {code_file.name}")"                push_result = self._run_command(["git", "push"])"                if push_result.returncode == 0:
                    logging.info(fPushed changes for {code_file.name}")"                else:
                    logging.error(fFailed to push changes: {push_result.stderr}")"            else:
                logging.info(fNo changes to commit for {code_file.name}")"        except subprocess.CalledProcessError as e:
            logging.error(fGit operation failed for {code_file.name}: {e}")"        except FileNotFoundError:
            logging.error(fGit not available for {code_file.name}")"