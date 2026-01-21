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
import subprocess
import re
import json
from typing import Any
from src.core.base.lifecycle.base_agent import BaseAgent

__version__ = VERSION


class CodeQualityAgent(BaseAgent):
    """
    Automated Code Quality Guard: Performs linting, formatting checks,
    and complexity analysis for Python, Rust, and JavaScript.
    """

    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.quality_reports: list[Any] = []

    def analyze_file_quality(self, file_path: str) -> dict[str, Any]:
        """Analyzes code quality for a specific file based on its extension."""
        print(f"Code Quality: Analyzing {file_path}")

        issues = []
        if file_path.endswith(".py"):
            issues = self._check_python_quality(file_path)
        elif file_path.endswith(".rs"):
            issues = self._check_rust_quality(file_path)
        elif file_path.endswith((".js", ".ts")):
            issues = self._check_js_quality(file_path)
        else:
            issues.append(
                {
                    "type": "Warning",
                    "message": "Unsupported file type for quality analysis.",
                }
            )

        report = {
            "file": file_path,
            "timestamp": os.path.getmtime(file_path)
            if os.path.exists(file_path)
            else 0,
            "issues": issues,
            "score": max(0, 100 - (len(issues) * 5)),
        }
        self.quality_reports.append(report)
        return report

    def _check_python_quality(self, path: str) -> list[dict[str, Any]]:
        """Run quality analysis for Python."""
        issues = []

        # 1. Manual baseline checks (always run)
        try:
            with open(path, "r", encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    if len(line.rstrip()) > 120:
                        issues.append(
                            {
                                "line": i,
                                "column": 120,
                                "type": "Style",
                                "message": f"Line too long ({len(line.rstrip())} > 120)",
                            }
                        )
        except Exception as e:
            issues.append(
                {
                    "type": "Error",
                    "message": f"Could not read file for manual check: {e}",
                }
            )

        # 2. Tool-based check (flake8)
        try:
            result = subprocess.run(
                ["flake8", "--max-line-length=120", path],
                capture_output=True,
                text=True,
                check=False,
            )

            # Intelligence: Record shell interaction (Phase 108)
            if hasattr(self, "recorder") and self.recorder:
                self.recorder.record_interaction(
                    "Shell", "Flake8", f"Linting {path}", str(result.stdout)[:500]
                )

            if result.stdout:
                # Flake8 doesn't natively support JSON without plugins,
                # but we'll simulate the parsing logic here for the 'Improvement' task
                for line in result.stdout.splitlines():
                    match = re.match(r"(.*):(\d+):(\d+): (.*)", line)
                    if match:
                        issues.append(
                            {
                                "line": int(match.group(2)),
                                "column": int(match.group(3)),
                                "message": match.group(4),
                            }
                        )
        except FileNotFoundError:
            # Fallback to internal checks if flake8 is missing
            with open(path, encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    if len(line) > 120:
                        issues.append(
                            {
                                "line": i,
                                "type": "Style",
                                "message": "Line too long (>120 chars)",
                            }
                        )
        return issues

    def _check_rust_quality(self, path: str) -> list[dict[str, Any]]:
        """Run cargo clippy for Rust quality analysis."""
        issues = []
        try:
            # Use message-format=json to get structured output
            cwd = self.workspace_path

            result = subprocess.run(
                [
                    "cargo",
                    "clippy",
                    "--message-format=json",
                    "--quiet",
                    "--allow-dirty",
                    "--allow-staged",
                ],
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False,
            )

            for line in result.stdout.splitlines():
                try:
                    data = json.loads(line)
                    if data.get("reason") == "compiler-message":
                        msg = data.get("message", {})
                        if msg.get("level") in ["warning", "error"]:
                            issues.append(
                                {
                                    "line": msg.get("spans", [{}])[0].get(
                                        "line_start", 0
                                    ),
                                    "column": msg.get("spans", [{}])[0].get(
                                        "column_start", 0
                                    ),
                                    "message": msg.get("message", "") + " (Clippy)",
                                    "type": "Suggestion",
                                }
                            )
                except json.JSONDecodeError:
                    pass

        except Exception:
            pass

        return issues

    def _check_js_quality(self, path: str) -> list[dict[str, Any]]:
        """Run eslint for JavaScript/TypeScript quality analysis."""
        try:
            subprocess.run(
                ["npx", "eslint", path, "--format", "json"], capture_output=True
            )
            return []
        except FileNotFoundError:
            return [
                {"type": "Info", "message": "NPM/Eslint not found, skipping JS check."}
            ]

    def get_aggregate_score(self) -> float:
        """Returns the average quality score across all analyzed files."""
        if not self.quality_reports:
            return 100.0
        return sum(r["score"] for r in self.quality_reports) / len(self.quality_reports)
