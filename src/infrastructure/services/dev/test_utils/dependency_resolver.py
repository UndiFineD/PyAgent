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


"""Auto-extracted class from agent_test_utils.py
"""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class DependencyResolver:
    """Resolves dependencies between tests."""

    def __init__(self) -> None:
        """Initialize resolver."""
        self.dependencies: dict[str, list[str]] = {}

    def add_test(self, name: str, depends_on: list[str]) -> None:
        """Register a test and its dependencies (test compatibility API)."""
        self.dependencies[name] = list(depends_on)

    def add_dependency(self, test: str, depends_on: str) -> None:
        """Add dependency."""
        if test not in self.dependencies:
            self.dependencies[test] = []
        self.dependencies[test].append(depends_on)

    def resolve(self) -> list[str]:
        """Resolve execution order or raise on circular dependencies."""
        visiting: set[str] = set()
        visited: set[str] = set()
        order: list[str] = []

        def visit(node: str) -> None:
            if node in visited:
                return
            if node in visiting:
                raise ValueError("Circular dependency detected")
            visiting.add(node)
            for dep in self.dependencies.get(node, []):
                visit(dep)
            visiting.remove(node)
            visited.add(node)
            order.append(node)

        nodes: set[str] = set(self.dependencies.keys())
        for deps in self.dependencies.values():
            nodes.update(deps)
        for n in sorted(nodes):
            visit(n)
        return order

    def resolve_order(self) -> list[str]:
        """Resolve execution order (topological sort)."""
        visited: set[str] = set()
        order: list[str] = []

        def visit(node: str) -> None:
            if node in visited:
                return
            visited.add(node)
            for dep in self.dependencies.get(node, []):
                visit(dep)
            order.append(node)

        for test in self.dependencies:
            visit(test)
        return order

    def detect_cycle(self) -> bool:
        """Detect circular dependencies."""
        visited: set[str] = set()
        rec_stack: set[str] = set()

        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for dep in self.dependencies.get(node, []):
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    return True
            rec_stack.remove(node)
            return False

        for test in self.dependencies:
            if test not in visited:
                if has_cycle(test):
                    return True
        return False
