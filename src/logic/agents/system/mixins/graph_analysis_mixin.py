
"""
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
    """Mixin for graph analysis and impact assessment in TopologicalNavigator."""

    @as_tool
    def find_impact_zone(self: TopologicalNavigator, entity_id: str, depth: int = 2) -> dict[str, Any]:
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
            "total_affected": len(affected),
        }

    def _build_reverse_graph(self: TopologicalNavigator) -> None:
        """Constructs the reverse dependency graph (A depends on B -> B is used by A)."""
        self.reverse_graph = {}
        for source, dependencies in self.graph.items():
            for dep in dependencies:
                if dep not in self.reverse_graph:
                    self.reverse_graph[dep] = set()
                self.reverse_graph[dep].add(source)

    @as_tool
    def get_topological_order(self: TopologicalNavigator) -> list[str]:
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
