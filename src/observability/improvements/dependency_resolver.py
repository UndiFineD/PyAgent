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
DependencyResolver - Resolve improvement dependencies

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate: resolver = DependencyResolver()
- Declare a dependency: resolver.add_dependency("A", "B")  # A depends on B
- Query deps: resolver.get_dependencies("A")
- Compute order for a set: ordered = resolver.resolve_order(["A", "B", "C"])

WHAT IT DOES:
- Maintains an in-memory mapping of improvement ids to lists of ids they depend on.
- Allows adding and retrieving dependencies for individual improvements.
- Produces a dependency-aware ordering (a topological-like sort) for a provided list of improvement ids where dependencies that also appear in the input list are visited before dependents.
- Performs a depth-first traversal while avoiding infinite recursion by tracking temporary and permanent visitation sets; cycles are silently ignored (nodes already in the temporary set are skipped).

WHAT IT SHOULD DO BETTER:
- Detect and report dependency cycles explicitly instead of silently skipping them; raise a clear exception for cyclic dependencies.
- Validate inputs and surface missing nodes or transitive dependencies outside the provided improvement set if that matters to callers.
- Preserve deterministic ordering for nodes with no dependency relationship (stable sort) and document ordering guarantees.
- Add unit tests covering edge cases (self-dependency, disconnected graphs, large dependency graphs) and benchmarks for performance.
- Consider thread-safety or async-safe variants if used concurrently, and add type/contract enforcement and richer error messages.

FILE CONTENT SUMMARY:
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


"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class DependencyResolver:
    """Resolves improvement dependencies."""

    def __init__(self) -> None:
        self.dependencies: dict[str, list[str]] = {}

    def add_dependency(self, improvement_id: str, depends_on_id: str) -> None:
        self.dependencies.setdefault(improvement_id, []).append(depends_on_id)

    def get_dependencies(self, improvement_id: str) -> list[str]:
        return list(self.dependencies.get(improvement_id, []))

    def resolve_order(self, improvement_ids: list[str]) -> list[str]:
        """Topologically sort the given ids so dependencies come first."""
        visited: set[str] = set()
        temp: set[str] = set()
        ordered: list[str] = []

        def visit(node: str) -> None:
            if node in visited:
                return
            if node in temp:
                return
            temp.add(node)
            for dep in self.dependencies.get(node, []):
                if dep in improvement_ids:
                    visit(dep)
            temp.remove(node)
            visited.add(node)
            ordered.append(node)

        for node in improvement_ids:
            visit(node)
        return ordered
"""

from __future__ import annotations

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class DependencyResolver:
    """Resolves improvement dependencies."""

    def __init__(self) -> None:
        self.dependencies: dict[str, list[str]] = {}

    def add_dependency(self, improvement_id: str, depends_on_id: str) -> None:
        self.dependencies.setdefault(improvement_id, []).append(depends_on_id)

    def get_dependencies(self, improvement_id: str) -> list[str]:
        return list(self.dependencies.get(improvement_id, []))

    def resolve_order(self, improvement_ids: list[str]) -> list[str]:
        """Topologically sort the given ids so dependencies come first."""
        visited: set[str] = set()
        temp: set[str] = set()
        ordered: list[str] = []

        def visit(node: str) -> None:
            if node in visited:
                return
            if node in temp:
                return
            temp.add(node)
            for dep in self.dependencies.get(node, []):
                if dep in improvement_ids:
                    visit(dep)
            temp.remove(node)
            visited.add(node)
            ordered.append(node)

        for node in improvement_ids:
            visit(node)
        return ordered
