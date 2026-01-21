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


"""Agent specializing in Python type hint enforcement and 'Any' type elimination."""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import ast
import logging
from pathlib import Path
from typing import Any
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import create_main_function

__version__ = VERSION


class TypeSafetyAgent(BaseAgent):
    """Identifies missing type annotations and 'Any' usage to improve codebase robustness."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Type Safety Agent. "
            "Your role is to enforce strict type hinting across the codebase. "
            "Scan for: Function parameters without types, missing return types, and 'Any' type usage. "
            "Provide specific suggestions to replace 'Any' with more descriptive types."
        )

    def _get_default_content(self) -> str:
        return "# Type Safety Audit\n\n## Summary\nWaiting for analysis...\n"

    def analyze_file(self, target_path: Path) -> list[dict[str, Any]]:
        """Analyzes a single Python file for type safety issues."""
        issues = []
        try:
            content = target_path.read_text(encoding="utf-8")
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # Check arguments
                    for arg in node.args.args:
                        if arg.annotation is None and arg.arg != "self":
                            issues.append(
                                {
                                    "line": node.lineno,
                                    "type": "Missing Param Type",
                                    "item": f"Parameter '{arg.arg}' in '{node.name}'",
                                    "severity": "MEDIUM",
                                }
                            )

                    # Check return type
                    if node.returns is None:
                        issues.append(
                            {
                                "line": node.lineno,
                                "type": "Missing Return Type",
                                "item": f"Function '{node.name}'",
                                "severity": "LOW",
                            }
                        )

                # Check for 'Any'
                elif isinstance(node, ast.Name) and node.id == "Any":
                    issues.append(
                        {
                            "line": node.lineno,
                            "type": "Usage of 'Any'",
                            "item": "Variable or annotation using 'Any'",
                            "severity": "HIGH",
                        }
                    )

        except Exception as e:
            logging.error(f"Failed to analyze {target_path}: {e}")

        return issues

    def run_audit(self, directory: str = "src") -> str:
        """Runs a full type safety audit on the directory."""
        root = Path(directory)
        all_issues = []

        for py_file in root.rglob("*.py"):
            if any(p in str(py_file) for p in ["__pycache__", "venv", ".git"]):
                continue

            file_issues = self.analyze_file(py_file)
            if file_issues:
                all_issues.append((py_file.name, file_issues))

        if not all_issues:
            return "✅ No type safety issues detected in the analyzed scope."

        report = ["## Type Safety Analysis Report\n"]
        for filename, issues in all_issues:
            report.append(f"### {filename}")
            for issue in issues:
                icon = "🚨" if issue["severity"] == "HIGH" else "⚠️"
                report.append(
                    f"- {icon} **{issue['type']}**: {issue['item']} (Line {issue['line']})"
                )

        return "\n".join(report)

    def improve_content(self, prompt: str) -> str:
        """Perform a type safety audit."""
        path = prompt if prompt else "src/classes"
        return self.run_audit(path)


if __name__ == "__main__":
    main = create_main_function(
        TypeSafetyAgent, "TypeSafety Agent", "Path to audit (e.g. 'src/classes')"
    )
    main()
