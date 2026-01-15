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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Agent specializing in Topological Context Navigation.
Builds a semantic map of the codebase for graph-based dependency exploration.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import os
import ast
import logging
from typing import Any
from pathlib import Path
from src.core.base.BaseAgent import BaseAgent
from src.core.base.utilities import as_tool

__version__ = VERSION




class TopologicalNavigator(BaseAgent):
    """Parses source code to build a dependency graph of classes and functions."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.graph: dict[str, set[str]] = {}
        self.reverse_graph: dict[str, set[str]] = {}
        self.root_dir = Path(os.getcwd())
        self._system_prompt = (
            "You are the Topological Context Navigator. "
            "You map relationships between code entities (classes, functions, modules) "
            "to determine the impact of changes across the codebase."
        )

    def _get_entity_id(self, file_path: Path, entity_name: str = "") -> str:
        """Generates a unique ID for a code entity."""
        rel_path = file_path.relative_to(self.root_dir)
        module_path = str(rel_path).replace(os.path.sep, ".").replace(".py", "")
        if entity_name:
            return f"{module_path}.{entity_name}"
        return module_path

    @as_tool
    def build_dependency_map(self, target_dir: str = "src") -> str:
        """Scans the specified directory to build a full dependency graph."""
        target_path = self.root_dir / target_dir
        if not target_path.exists():
            return f"Error: Path {target_dir} does not exist."

        count = 0
        for py_file in target_path.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue
            self._parse_file(py_file)
            count += 1

        return f"Dependency map built successfully. Indexed {count} files. Total nodes: {len(self.graph)}"

    def _parse_file(self, file_path: Path) -> None:
        """Extracts imports and class/function definitions from a file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                tree = ast.parse(f.read())

            module_id = self._get_entity_id(file_path)
            if module_id not in self.graph:
                self.graph[module_id] = set()

            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    # Extract imports to find module-level dependencies
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            self.graph[module_id].add(alias.name)
                    else:
                        if node.module:
                            self.graph[module_id].add(node.module)

                elif isinstance(node, ast.ClassDef):
                    class_id = self._get_entity_id(file_path, node.name)
                    if class_id not in self.graph:
                        self.graph[class_id] = set()
                    # Add class as dependee of module
                    self.graph[module_id].add(class_id)

                    # Track base classes
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            self.graph[class_id].add(base.id)

                elif isinstance(node, ast.FunctionDef):
                    func_id = self._get_entity_id(file_path, node.name)
                    if func_id not in self.graph:
                        self.graph[func_id] = set()
                    self.graph[module_id].add(func_id)

        except Exception as e:
            logging.error(f"Failed to parse {file_path}: {e}")

    @as_tool
    def federate_with_external_project(self, external_root: str) -> str:
        """Indexes an external project and merges its graph into the current map.
        This enables 'Federated Project Intelligence' for multi-repo ecosystems.
        """
        ext_path = Path(external_root)
        if not ext_path.exists():
            return f"Error: External path {external_root} not found."

        # Store previous root to restore later if needed
        original_root = self.root_dir
        self.root_dir = ext_path.absolute()

        try:
            report = self.build_dependency_map(".")
            return f"Federation Success: {report} (External Root: {external_root})"
        finally:
            self.root_dir = original_root

    @as_tool
    def find_impact_zone(self, entity_id: str, depth: int = 2) -> dict[str, Any]:
        """Identifies which parts of the codebase depend on the given entity."""
        # Need reverse graph to find dependents
        if not self.reverse_graph:
            self._build_reverse_graph()

        affected = set()
        to_visit = [(entity_id, 0)]
        visited = set()

        while to_visit:
            current, current_depth = to_visit.pop(0)
            if current in visited or current_depth >= depth:
                continue

            visited.add(current)
            dependents = self.reverse_graph.get(current, set())
            for dep in dependents:
                affected.add(dep)
                to_visit.append((dep, current_depth + 1))

        return {
            "target": entity_id,
            "impact_zone": list(affected),
            "total_affected": len(affected)
        }

    def _build_reverse_graph(self) -> None:
        """Constructs the reverse dependency graph (A depends on B -> B is used by A)."""
        self.reverse_graph = {}
        for source, dependencies in self.graph.items():
            for dep in dependencies:
                if dep not in self.reverse_graph:
                    self.reverse_graph[dep] = set()
                self.reverse_graph[dep].add(source)

    @as_tool
    def get_topological_order(self) -> list[str]:
        """Returns nodes in topological order (safe initialization/build sequence)."""
        visited = set()
        stack = []

        def visit(node: str) -> None:
            if node not in visited:
                visited.add(node)
                for dep in self.graph.get(node, set()):
                    if dep in self.graph:
                        # Only follow internal graph
                        visit(dep)
                stack.append(node)

        for node in self.graph:
            visit(node)

        return stack[::-1]
