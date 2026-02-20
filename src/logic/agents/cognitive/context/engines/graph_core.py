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


# GraphCore logic for PyAgent.
# Pure logic for AST-based code relationship analysis and graph management.

"""Graph core: lightweight AST-based graph extraction.

This module provides a small, pure-Python fallback implementation
for tests and environments where the original implementation is
corrupted or a Rust acceleration layer isn't available.
"""

import ast
from typing import Any, Dict, List, Set, Tuple


class CodeGraphVisitor(ast.NodeVisitor):
    """AST visitor to collect imports, classes, bases and simple calls."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.imports: Set[str] = set()
        self.classes: List[str] = []
        self.calls: Set[str] = set()
        self.bases: Dict[str, List[str]] = {}

    def visit_Import(self, node: ast.Import) -> None:  # pylint: disable=invalid-name
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:  # pylint: disable=invalid-name
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:  # pylint: disable=invalid-name
        self.classes.append(node.name)
        bases: List[str] = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(base.attr)
        self.bases[node.name] = bases
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:  # pylint: disable=invalid-name
        if isinstance(node.func, ast.Name):
            self.calls.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.calls.add(node.func.attr)
        self.generic_visit(node)


class GraphCore:
    """Utility class exposing parsing and simple edge building."""

    @staticmethod
    def parse_python_content(rel_path: str, content: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(content)
            visitor = CodeGraphVisitor(rel_path)
            visitor.visit(tree)
            return {
                "rel_path": rel_path,
                "imports": list(visitor.imports),
                "classes": visitor.classes,
                "inherits": visitor.bases,
                "calls": list(visitor.calls),
            }
        except (SyntaxError, ValueError, AttributeError):
            return {"rel_path": rel_path, "imports": [], "classes": [], "inherits": {}, "calls": []}

    @staticmethod
    def build_edges(analysis: Dict[str, Any]) -> List[Tuple[str, str, str]]:
        """Build simple edges from analysis results.

        Returns list of tuples (source, target, relationship_type).
        """
        edges: List[Tuple[str, str, str]] = []
        rel_path = analysis.get("rel_path", "")
        for imp in analysis.get("imports", []):
            edges.append((rel_path, imp, "imports"))
        for cls, bases in analysis.get("inherits", {}).items():
            for base in bases:
                edges.append((f"{rel_path}::{cls}", base, "inherits"))
        return edges
