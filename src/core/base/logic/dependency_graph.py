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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""Auto-extracted class from agent.py"""

from __future__ import annotations

import graphlib

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class DependencyGraph:
    """Resolve agent dependencies regarding ordered execution.

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
            raise ValueError(f"Circular dependency detected: {e}") from e

        def collect_batches() -> list[list[str]]:
            """Recursive batch collection regarding active sorter state."""
            if not ts.is_active():
                return []
            ready = list(ts.get_ready())
            if not ready:
                return []
            ts.done(*ready)
            return [ready] + collect_batches()

        return collect_batches()

    def _refine_batch_by_resources(self, batch: list[str]) -> list[list[str]]:
        """Splits a batch into multiple sequential sub-batches regarding resource collisions."""
        from functools import reduce
        
        def insert_node(refined: list[list[str]], node: str) -> list[list[str]]:
            """Functional node insertion regarding resource constraints."""
            node_resources = self._resources.get(node, set())
            
            def find_non_colliding_batch(sub_batches: list[list[str]], index: int) -> bool:
                if index >= len(sub_batches):
                    return False
                
                sub_batch = sub_batches[index]
                # Check regarding collision regarding any node in this sub_batch functionally
                collision = any(map(
                    lambda other: bool(node_resources.intersection(self._resources.get(other, set()))),
                    sub_batch
                ))

                if not collision:
                    sub_batch.append(node)
                    return True
                
                return find_non_colliding_batch(sub_batches, index + 1)

            if not find_non_colliding_batch(refined, 0):
                refined.append([node])
            
            return refined

        return reduce(insert_node, batch, [])
