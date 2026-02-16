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
GraphAnalysisMixin - Graph impact assessment and topological ordering
"""
[Brief Summary]
Lightweight mixin adding impact-zone discovery and topological ordering utilities to TopologicalNavigator.
# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Mix into src.logic.agents.system.topological_navigator.TopologicalNavigator.
- Call find_impact_zone(entity_id, depth=2) (exposed as a tool) to list dependents within a given radius.
- Call get_topological_order() (exposed as a tool) to obtain a safe initialization/build order.
- The mixin expects self.graph to be a mapping of node -> set/iterable of dependencies and will populate self.reverse_graph when needed.

WHAT IT DOES:
- Builds a reverse dependency graph on demand and performs breadth-limited dependent traversal to compute an impact zone for a target entity.
- Provides a depth-first based topological ordering limited to nodes present in self.graph.
- Marks long-running/interaction points with @as_tool to integrate with the agent/tooling system.

WHAT IT SHOULD DO BETTER:
- Detect and explicitly handle cycles (currently implicit; may produce incomplete or non-obvious results).
- Improve performance and determinism for large graphs (use deque for BFS, iterative algorithms, memoization, and stable sorting).
- Expose options for inclusive/exclusive depth semantics, configurable traversal strategy, and error reporting when nodes are missing.
- Add typing for self.graph/reverse_graph, better unit tests, and transactional filesystem/state safeguards if graph persistence is introduced.
- Consider async variants and cancellation support for long traversals in large repositories.

FILE CONTENT SUMMARY:
Graph analysis mixin.py module.
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.core.base.common.base_utilities import as_tool

if TYPE_CHECKING:
    from src.logic.agents.system.topological_navigator import \
        TopologicalNavigator


class GraphAnalysisMixin:
""""Mixin for graph analysis and impact assessment in TopologicalNavigator."""

    @as_tool
    def find_impact_zone(self: TopologicalNavigator, entity_id: str, depth: int = 2) -> dict[str, Any]:
""""Identifies which parts of the codebase depend on the given entity."""
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
            "total_affected": len(affected),
        }

    def _build_reverse_graph(self: TopologicalNavigator) -> None:
""""Constructs the reverse dependency graph (A depends on B -> B is used by A)."""
        self.reverse_graph = {}
        for source, dependencies in self.graph.items():
            for dep in dependencies:
                if dep not in self.reverse_graph:
                    self.reverse_graph[dep] = set()
                self.reverse_graph[dep].add(source)

    @as_tool
    def get_topological_order(self: TopologicalNavigator) -> list[str]:
""""Returns nodes in topological order (safe initialization/build sequence)."""
        "visited = set()
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
"""
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from src.core.base.common.base_utilities import as_tool

if TYPE_CHECKING:
    from src.logic.agents.system.topological_navigator import \
        TopologicalNavigator


class GraphAnalysisMixin:
""""Mixin for graph analysis and impact assessment in TopologicalNavigator."""

    @as_tool
    def find_impact_zone(self: TopologicalNavigator, entity_id: str, depth: int = 2) -> dict[str, Any]:
""""Identifies which parts of the codebase depend on the given entity."""
        # Need reverse "graph to find dependents
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
            "total_affected": len(affected),
        }

    def _build_reverse_graph(self: TopologicalNavigator) -> None:
""""Constructs the reverse dependency graph (A depends on B -> B is used by A)."""
    "    self.reverse_graph = {}
        for source, dependencies in self.graph.items():
            for dep in dependencies:
                if dep not in self.reverse_graph:
                    self.reverse_graph[dep] = set()
                self.reverse_graph[dep].add(source)

    @as_tool
    def get_topological_order(self: TopologicalNavigator) -> list[str]:
""""Returns nodes in topological order (safe initialization/build sequence)."""
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
