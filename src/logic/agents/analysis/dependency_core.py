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
DependencyCore logic for PyAgent.
Pure logic for AST-based dependency analysis.
No I/O or side effects.
"""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import ast
from src.core.base.common.types.dependency_type import DependencyType
from src.core.base.common.types.dependency_node import DependencyNode

__version__ = VERSION


class DependencyCore:
    """Pure logic core for dependency analysis."""

    @staticmethod
    def parse_dependencies(
        content: str, file_path: str = ""
    ) -> dict[str, DependencyNode]:
        """Parses imports and class inheritance from code content."""
        nodes: dict[str, DependencyNode] = {}

        try:
            tree = ast.parse(content)
        except SyntaxError:
            return nodes

        # Analyze imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    DependencyCore._add_to_nodes(
                        nodes, alias.name, DependencyType.IMPORT, file_path
                    )
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                DependencyCore._add_to_nodes(
                    nodes, module, DependencyType.IMPORT, file_path
                )
            elif isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        DependencyCore._add_to_nodes(
                            nodes, base.id, DependencyType.CLASS_INHERITANCE, file_path
                        )

        return nodes

    @staticmethod
    def _add_to_nodes(
        nodes: dict[str, DependencyNode],
        name: str,
        dep_type: DependencyType,
        file_path: str,
    ) -> None:
        if name not in nodes:
            nodes[name] = DependencyNode(name=name, type=dep_type, file_path=file_path)
        else:
            if file_path not in nodes[name].depended_by:
                nodes[name].depended_by.append(file_path)

    @staticmethod
    def filter_external_deps(
        nodes: dict[str, DependencyNode], stdlib_list: set[str]
    ) -> list[str]:
        """Filters nodes to return only non-standard library dependencies."""
        return [name for name in nodes if name not in stdlib_list]
