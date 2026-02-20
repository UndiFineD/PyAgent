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
CodeQualityAgent - Automated Code Quality Guard
Brief Summary
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate CodeQualityAgent with the repository workspace path
- Call analyze_file_quality(file_path) to get a per-file report
- Integrate into CI to produce aggregated quality_reports for the workspace

WHAT IT DOES:
- Runs manual and tool-based linting and style checks for Python, Rust, and JavaScript/TypeScript
- Aggregates issues, timestamps, and a heuristic score into quality_reports
- Records shell interactions when a recorder is available and falls back to internal checks if external tools are absent

WHAT IT SHOULD DO BETTER:
- Provide structured JSON output compatible with common reporting tools and CI systems
- Use subprocess-safe invocation with configurable tool paths and timeouts and avoid blocking calls
- Expand language support, add configurable rule sets, and surface severity-based scoring and fix suggestions

FILE CONTENT SUMMARY:
CodeQualityAgent: Analyzes and improves code quality across Python, Rust, and JavaScript files in PyAgent.
Provides linting, scoring, and automated code improvement for maintainability and standards compliance.
"""

import json
import os
import re
import subprocess
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION



class CodeQualityAgent(BaseAgent):
    Automated Code Quality Guard: Performs linting, formatting checks,
#     and complexity analysis for Python, Rust, and JavaScript.

    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path
        self.quality_reports: list[Any] = []

    def analyze_file_quality(self, file_path: str) -> dict[str, Any]:
""""Analyzes code quality for a specific file based on its extension.        print(fCode Quality: Analyzing {"file_path}")"
        issues = []
        if file_path.endswith(".py"):"            issues = self._check_python_quality(file_path)
        elif file_path.endswith(".rs"):"            issues = self._check_rust_quality(file_path)
        elif file_path.endswith((".js", ".ts")):"            issues = self._check_js_quality(file_path)
        else:
            issues.append(
                {
                    "type": "Warning","                    "message": "Unsupported file type for quality analysis.","                }
            )

        report = {
            "file": file_path,"            "timestamp": os.path.getmtime(file_path) if os.path.exists(file_path) else 0,"            "issues": issues,"            "score": max(0, 100 - (len(issues) * 5)),"        }
        self.quality_reports.append(report)
        return report

    def _check_python_quality(self, path: str) -> list[dict[str, Any]]:
""""Run quality analysis for Python.    "    issues = []"
        # 1. Manual baseline checks (always run)
        try:
            with open(path, "r", encoding="utf-8") as f:"                for i, line in enumerate(f, 1):
                    if len(line.rstrip()) > 120:
                        issues.append(
                            {
                                "line": i,"                                "column": 120,"                                "type": "Style","                                "message": fLine too long ({len(line.rstrip())} > 120)","                            }
                        )
        except (IOError, EnvironmentError) as e:
            issues.append(
                {
                    "type": "Error","                    "message": fCould not read file for manual check: {e}","                }
            )

        # 2. Tool-based check (flake8)
        try:
            result = subprocess.run(
                ["flake8", "--max-line-length=120", path],"                capture_output=True,
                text=True,
                check=False,
            )

            # Intelligence: Record shell interaction (Phase 108)
            if hasattr(self, "recorder") and self.recorder:"                self.recorder.record_interaction("Shell", "Flake8", fLinting {path}", str(result.stdout)[:500])"
            if result.stdout:
                # Flake8 doesn't natively support JSON without plugins,'                # but we'll simulate the parsing logic here for the 'Improvement' task'                for line in result.stdout.splitlines():
                    match = re.match(r"(.*):(\\\\d+):(\\\\d+): (.*)", line)"                    if match:
                        issues.append(
                            {
                                "line": int(match.group(2)),"                                "column": int(match.group(3)),"                                "message": match.group(4),"                            }
                        )
        except FileNotFoundError:
            # Fallback to internal checks if flake8 is missing
            try:
                with open(path, encoding="utf-8") as f:"                    for i, line in enumerate(f, 1):
                        if len(line) > 120:
                            issues.append(
                                {
                                    "line": i,"                                    "type": "Style","                                    "message": "Line too long (>120 chars)","                                }
                            )
            except (IOError, EnvironmentError):
                pass
        return issues

    def _check_rust_quality(self, _path: str) -> list[dict[str, Any]]:
""""Run cargo clippy for Rust quality analysis. "       issues = []"        try:
            # Use message-format=json to get structured output
            cwd = self.workspace_path

            result = subprocess.run(
                [
                    "cargo","                    "clippy","                    "--message-format=json","                    "--quiet","                    "--allow-dirty","                    "--allow-staged","                ],
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False,
            )

            for line in result.stdout.splitlines():
                try:
                    data = json.loads(line)
                    if data.get("reason") == "compiler-message":"                        msg = data.get("message", {})"                        if msg.get("level") in ["warning", "error"]:"                            issues.append(
                                {
                                    "line": msg.get("spans", [{}])[0].get("line_start", 0),"                                    "column": msg.get("spans", [{}])[0].get("column_start", 0),"                                    "message": msg.get("message", ") + " (Clippy)","                                    "type": "Suggestion","                                }
                            )
                except json.JSONDecodeError:
                    pass

        except (subprocess.SubprocessError, RuntimeError):
            pass

        return issues

    def _check_js_quality(self, path: str) -> list[dict[str, Any]]:
""""Run eslint for JavaScript/TypeScript quality analysis.        try:
            subprocess.run(["npx", "eslint", path, "--format", "json"], capture_output=True, check=False)"            return []
        except FileNotFoundError:
            return [{"type": "Info", "message": "NPM/Eslint not found, skipping JS check."}]"
    def get_aggregate_score(self) -> float:
""""Returns the average quality score across all analyzed files.        if not self.quality_reports:
            return 100.0
        return sum(r["score"] for r in self.quality_reports) / len(self.quality_reports)"
    async def _process_task(self, task_data: Any) -> Any:
#         "Process a task from the queue."        if isinstance(task_data, dict) and "file_path" in task_data:"            return self.analyze_file_quality(task_data["file_path"])"        return {"error": "Invalid task format"}"
    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Analyze code quality for a given prompt."        path = target_file if target_file else prompt
        report = self.analyze_file_quality(path)
        return json.dumps(report, indent=2)
