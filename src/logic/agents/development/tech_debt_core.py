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
from src.core.base.version import VERSION
import ast
from typing import Any

try:
    import rust_core as rc
    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION


class TechDebtCore:
    """
    Pure logic for analyzing technical debt from AST.
    Ready for Rust conversion.
    """

    @staticmethod
    def analyze_ast_debt(tree: ast.AST) -> list[dict[str, Any]]:
        """
        Analyzes an AST tree for technical debt markers.

        Args:
            tree: The pre-parsed AST tree.

        Returns:
            A list of identified issues.
        """
        # Count missing docstrings
        missing_docstrings = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                if not ast.get_docstring(node):
                    missing_docstrings += 1

        # Count AST nodes (complexity proxy)
        node_count = sum(1 for _ in ast.walk(tree))

        # Use Rust for issue analysis if available
        if HAS_RUST:
            # Rust function: analyze_tech_debt_rust(node_count, missing_docstrings, todo_count)
            return rc.analyze_tech_debt_rust(node_count, missing_docstrings, 0)

        # Python fallback
        issues = []
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

        if node_count > 1000:
            issues.append(
                {
                    "type": "High Complexity",
                    "detail": f"Structure contains {node_count} AST nodes.",
                    "severity": "Medium",
                }
            )

        return issues

    @staticmethod
    def identify_hotspots(
        reports: list[dict[str, Any]], limit: int = 5
    ) -> list[dict[str, Any]]:
        """Sorts and returns major technical debt hotspots."""
        return sorted(reports, key=lambda x: x.get("issue_count", 0), reverse=True)[
            :limit
        ]
