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
Core logic for Python Linting analysis.
Integrates ruff, flake8, and pylint for comprehensive code quality checks.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
from typing import Optional, TypedDict

from src.core.base.common.base_interfaces import ContextRecorderInterface


class LintIssue(TypedDict):
    """Represents a single issue found by a linter."""

    file: str
    line: int
    column: int
    code: str
    message: str
    linter: str  # 'ruff', 'flake8', 'pylint'
    type: str    # 'error', 'warning', 'convention', 'refactor'


class LintResult(TypedDict):
    """Result of a linting session."""

    valid: bool
    issues: list[LintIssue]
    error: Optional[str]


class LinterCore:
    """Core logic for Python Linter analysis."""

    def __init__(self, recorder: Optional[ContextRecorderInterface] = None) -> None:
        self.logger: logging.Logger = logging.getLogger(__name__)
        self.recorder = recorder

    def run_ruff(self, file_path: str) -> list[LintIssue]:
        """Runs ruff and returns issues."""
        issues: list[LintIssue] = []
        try:
            # --output-format json
            command = ["ruff", "check", "--output-format=json", file_path]
            process: subprocess.CompletedProcess[str] = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

            output = process.stdout or process.stderr
            if self.recorder:
                self.recorder.record_interaction(
                    provider="python",
                    model="ruff",
                    prompt=" ".join(command),
                    result=output[:2000],
                )

            if process.stdout:
                try:
                    ruff_json = json.loads(process.stdout)
                    for item in ruff_json:
                        issues.append({
                            "file": item.get("filename", file_path),
                            "line": item.get("location", {}).get("row", 0),
                            "column": item.get("location", {}).get("column", 0),
                            "code": item.get("code", "UNKNOWN"),
                            "message": item.get("message", ""),
                            "linter": "ruff",
                            "type": "warning" # ruff doesn't explicitly categorize in simple json
                        })
                except json.JSONDecodeError:
                    self.logger.warning("Failed to parse ruff output")
        except FileNotFoundError:
            self.logger.warning("ruff executable not found")
        except (subprocess.SubprocessError, OSError, ValueError) as e:
            self.logger.error(f"Error running ruff: {e}")

        return issues

    def run_pylint(self, file_path: str) -> list[LintIssue]:
        """Runs pylint and returns issues."""
        issues: list[LintIssue] = []
        try:
            # -f json
            command = ["pylint", "-f", "json", file_path]
            process: subprocess.CompletedProcess[str] = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

            output = process.stdout or process.stderr
            if self.recorder:
                self.recorder.record_interaction(
                    provider="python",
                    model="pylint",
                    prompt=" ".join(command),
                    result=output[:2000],
                )

            if process.stdout:
                try:
                    pylint_json = json.loads(process.stdout)
                    for item in pylint_json:
                        issues.append({
                            "file": item.get("path", file_path),
                            "line": item.get("line", 0),
                            "column": item.get("column", 0),
                            "code": item.get("symbol", item.get("message-id", "UNKNOWN")),
                            "message": item.get("message", ""),
                            "linter": "pylint",
                            "type": item.get("type", "warning")
                        })
                except json.JSONDecodeError:
                    self.logger.warning("Failed to parse pylint output")
        except FileNotFoundError:
            self.logger.warning("pylint executable not found")
        except (subprocess.SubprocessError, OSError, ValueError) as e:
            self.logger.error(f"Error running pylint: {e}")

        return issues

    def run_flake8(self, file_path: str) -> list[LintIssue]:
        """Runs flake8 and returns issues."""
        issues: list[LintIssue] = []
        try:
            # flake8 default output: file:line:col: code message
            command = ["flake8", "--format=default", file_path]
            process: subprocess.CompletedProcess[str] = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

            output = process.stdout or process.stderr
            if self.recorder:
                self.recorder.record_interaction(
                    provider="python",
                    model="flake8",
                    prompt=" ".join(command),
                    result=output[:2000],
                )

            if process.stdout:
                for line in process.stdout.splitlines():
                    parts = line.split(":", 3)
                    if len(parts) >= 4:
                        try:
                            # filename = parts[0]
                            lineno = int(parts[1])
                            col = int(parts[2])
                            rest: str = parts[3].strip()
                            code_msg: list[str] = rest.split(" ", 1)
                            code: str = code_msg[0]
                            msg: str = code_msg[1] if len(code_msg) > 1 else ""

                            issues.append({
                                "file": file_path,
                                "line": lineno,
                                "column": col,
                                "code": code,
                                "message": msg,
                                "linter": "flake8",
                                "type": "warning"
                            })
                        except ValueError:
                            pass

        except FileNotFoundError:
            self.logger.warning("flake8 executable not found")
        except (subprocess.SubprocessError, OSError, ValueError) as e:
            self.logger.error(f"Error running flake8: {e}")

        return issues

    def lint_file(self, file_path: str, tools: list[str] | None = None) -> LintResult:
        """
        Runs specified linters on a python file.
        Default includes 'ruff', 'pylint', 'flake8'.
        """
        if not os.path.exists(file_path):
            return {
                "valid": False,
                "issues": [],
                "error": "File not found",
            }

        if tools is None:
            tools = ["ruff", "pylint", "flake8"]

        all_issues: list[LintIssue] = []

        if "ruff" in tools and file_path.endswith(".py"):
            all_issues.extend(self.run_ruff(file_path))

        if "pylint" in tools and file_path.endswith(".py"):
            all_issues.extend(self.run_pylint(file_path))

        if "flake8" in tools and file_path.endswith(".py"):
            all_issues.extend(self.run_flake8(file_path))

        # Sort by line number
        all_issues.sort(key=lambda x: x["line"])

        return {
            "valid": len(all_issues) == 0,
            "issues": all_issues,
            "error": None
        }
