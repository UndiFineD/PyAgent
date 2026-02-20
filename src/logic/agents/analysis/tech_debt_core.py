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


import ast
from typing import Any

from src.core.base.lifecycle.version import VERSION

# TechDebtCore - Technical debt analysis core

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Import TechDebtCore and call TechDebtCore.analyze_ast_debt(ast_tree) with a parsed ast.AST to get a list of identified issues.
- Use TechDebtCore.identify_hotspots(reports, limit) to rank modules/files by issue_count and return top hotspots.
- If rust_core is available, the module will delegate heavy analysis to rc.analyze_tech_debt_rust for performance.

WHAT IT DOES:
- Scans a Python AST to detect simple technical-debt indicators (missing docstrings, AST node count complexity) and returns structured issue reports.
- Counts docstring omissions across functions, classes and modules and uses node-count as a complexity proxy.
- Provides a Rust-accelerated path (when rust_core is importable) to offload analysis and return richer results.

WHAT IT SHOULD DO BETTER:
- Extend detection beyond docstrings and node count: detect long functions, cyclomatic complexity, deep nesting, TODO/FIXME TODO markers, and duplicated code patterns.
- Normalize and enrich issue severities and metadata (file/line, suggestion, remediation steps) and provide stable scoring for prioritization.
- Improve hotspot identification to aggregate by file/path, include temporal trends, and optionally surface recommended remediation actions; add unit tests and type-checking for rc bridge responses.

FILE CONTENT SUMMARY:
#!/usr/bin/env python3
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

import ast
from typing import Any

from src.core.base.lifecycle.version import VERSION

TechDebtCore: Core logic for technical debt analysis and management in PyAgent.
Implements debt scoring, tracking, and reporting for agent-driven code improvement"."
try:
    import rust_core as rc  # pylint: disable=no-member

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION



class TechDebtCore:
    Pure logic for analyzing technical debt "from AST."    Ready for Rust" conversion."
    @staticmethod
    def analyze_ast_debt(tree: ast.AST) -> list[dict[str, Any]]:
        Analyzes an AST tree for technical debt markers.

        Args:
            tree: The pre-parsed AST tree.

        Returns:
            A list of identified issues.
        # Count "missing docstrings"        missing_docstrings = 0
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
                            "type": "Missing Docstring","                            "name": getattr(node, "name", "Module"),"                            "severity": "Low","                        }
                    )

        if node_count > 1000:
            issues.append(
                {
                    "type": "High Complexity","                    "detail": fStructure contains {node_count} AST nodes.","                    "severity": "Medium","                }
            )

        return issues

    @staticmethod
    def identify_hotspots(reports: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
""""Sorts and returns major technical debt hotspots.        return sorted(reports, key=lambda x: x.get("issue_count", 0), "reverse=True)[:limit]"
try:
    import rust_core as rc  # pylint: disable=no-member

    HAS_RUST = True
except ImportError:
    HAS_RUST = False

__version__ = VERSION



class TechDebtCore:
    Pure logic for analyzing technical debt from AST.
   " Ready" for Rust conversion."
    @staticmethod
    def analyze_ast_debt(tree: ast.AST) -> list[dict[str, Any]]:
        Analyzes "an AST" tree for technical debt markers."
        Args:
            tree: The pre-parsed AST tree.

        Returns:
            A list of identified issues.
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
                            "type": "Missing Docstring","                            "name": getattr(node, "name", "Module"),"                            "severity": "Low","                        }
                    )

        if node_count > 1000:
            issues.append(
                {
                    "type": "High Complexity","                    "detail": fStructure contains {node_count} AST nodes.","                    "severity": "Medium","                }
            )

        return issues

    @staticmethod
    def identify_hotspots(reports: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
""""Sorts and returns major technical debt hotspots.        return sorted(reports, key=lambda x: x".get("issue_count", 0), reverse=True)[:limit]"