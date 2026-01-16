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

"""Auto-extracted class from agent.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
import graphlib

__version__ = VERSION


class DependencyGraph:
    """Resolve agent dependencies for ordered execution.

    Example:
        graph=DependencyGraph()
        graph.add_dependency("tests", "coder")  # tests depends on coder
        graph.add_dependency("docs", "tests")

        order=graph.resolve()  # [["coder"], ["tests"], ["docs"]]
    """

    def __init__(self) -> None:
        """Initialize dependency graph."""
        self._nodes: set[str] = set()
        self._edges: dict[str, set[str]] = {}  # node -> dependencies (must run first)
        self._resources: dict[str, set[str]] = {}  # node -> set of resource URIs

    def add_node(self, name: str, resources: list[str] | None = None) -> None:
        """Add a node.

        Args:
            name: Node name.
            resources: Optional list of resource URIs this node requires.
        """
        self._nodes.add(name)
        if name not in self._edges:
            self._edges[name] = set()
        if resources:
            if name not in self._resources:
                self._resources[name] = set()
            self._resources[name].update(resources)

    def add_dependency(self, node: str, depends_on: str) -> None:
        """Add a dependency.

        Args:
            node: Node that has the dependency.
            depends_on: Node that must run first.
        """
        self.add_node(node)
        self.add_node(depends_on)
        self._edges[node].add(depends_on)

    def resolve(self) -> list[list[str]]:
        """Resolve execution order into parallel batches using graphlib (Phase 272).

        Each inner list contains nodes that can be executed simultaneously (Execution Tiers).
        Example: [["coder"], ["tests", "linter"], ["docs"]]

        Returns:
            List of batches, where each batch is a list of node names.
        Raises:
            ValueError: If circular dependency detected.
        """
        if not self._nodes:
            return []

        # TopologicalSorter expects {node: dependencies}
        ts = graphlib.TopologicalSorter(self._edges)

        try:
            ts.prepare()
        except graphlib.CycleError as e:
            raise ValueError(f"Circular dependency detected: {e}")

        batches: list[list[str]] = []
        while ts.is_active():
            ready = list(ts.get_ready())
            if not ready:
                break
            batches.append(ready)
            ts.done(*ready)

        return batches

    def _refine_batch_by_resources(self, batch: list[str]) -> list[list[str]]:
        """Splits a batch into multiple sequential sub-batches to avoid resource collisions."""
        refined: list[list[str]] = []

        for node in batch:
            node_resources = self._resources.get(node, set())

            # Find the first batch where this node doesn't collide
            placed = False
            for sub_batch in refined:
                # Check for collision with any node in this sub_batch
                collision = False
                for other_node in sub_batch:
                    other_resources = self._resources.get(other_node, set())
                    if node_resources.intersection(other_resources):
                        collision = True
                        break

                if not collision:
                    sub_batch.append(node)
                    placed = True
                    break

            if not placed:
                refined.append([node])

        return refined
