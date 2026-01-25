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
Tech debt agent.py module.
"""


from __future__ import annotations

import ast
import os
from typing import Any

from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class TechDebtAgent(BaseAgent):  # pylint: disable=too-many-ancestors
    """
    Analyzes the codebase for technical debt including high cyclomatic complexity,
    missing docstrings, and large files.
    """

    def __init__(self, workspace_path: str) -> None:
        super().__init__(workspace_path)
        self.workspace_path = workspace_path

    def analyze_file(self, file_path: str) -> dict[str, Any]:
        """Analyzes a single Python file for technical debt."""
        if not file_path.endswith(".py"):
            return {"file": file_path, "issues": []}

        issues = []
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content, filename=file_path)

            # Check for missing docstrings
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    if not ast.get_docstring(node):
                        issues.append(
                            {
                                "type": "Missing Docstring",
                                "name": getattr(node, "name", "Module"),
                                "severity": "Low",
                            }
                        )

            # Check for high complexity (simple heuristic: depth of nesting/number of nodes)
            node_count = sum(1 for _ in ast.walk(tree))
            if node_count > 1000:
                issues.append(
                    {
                        "type": "High Complexity",
                        "detail": f"File contains {node_count} AST nodes.",
                        "severity": "Medium",
                    }
                )

        except (SyntaxError, EnvironmentError) as e:
            issues.append({"type": "Error", "detail": str(e), "severity": "Medium"})

        return {"file": file_path, "issues": issues, "issue_count": len(issues)}

    def analyze_workspace(self) -> dict[str, Any]:
        """Runs technical debt analysis on the entire workspace."""
        total_issues = 0
        file_reports = []

        for root, dirs, files in os.walk(self.workspace_path):
            dirs[:] = [
                d for d in dirs if not d.startswith(".") and d not in ["node_modules", "__pycache__", ".venv", "venv"]
            ]
            for file in files:
                if file.endswith(".py"):
                    path = os.path.join(root, file)
                    report = self.analyze_file(path)
                    if report["issue_count"] > 0:
                        file_reports.append(report)
                        total_issues += report["issue_count"]

        return {
            "total_issues": total_issues,
            "hotspots": sorted(file_reports, key=lambda x: x["issue_count"], reverse=True)[:5],
        }

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
        """Perform a tech debt analysis."""
        if target_file:
            report = self.analyze_file(target_file)
            import json

            return json.dumps(report, indent=2)

        workspace_report = self.analyze_workspace()
        report_lines = ["## Tech Debt Analysis Report"]
        report_lines.append(f"**Total Issues**: {workspace_report['total_issues']}")
        report_lines.append("\n### Hotspots")
        for hotspot in workspace_report["hotspots"]:
            report_lines.append(f"- `{hotspot['file']}`: {hotspot['issue_count']} issues")

        return "\n".join(report_lines)


if __name__ == "__main__":
    from src.core.base.common.base_utilities import create_main_function

    main = create_main_function(TechDebtAgent, "TechDebt Agent", "Workspace path")
    main()
