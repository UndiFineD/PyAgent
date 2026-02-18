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


"""
DependencyResolver - Resolve improvement dependencies

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate: resolver = DependencyResolver()
- Declare a dependency: resolver.add_dependency("A", "B")  # A depends on B"- Query deps: resolver.get_dependencies("A")"# [AUTO-FIXED F821] # [AUTO-FIXED F821] - Compute order for a set: ordered = resolver.resolve_order(["A", "B", "C"])"
WHAT IT DOES:
- Maintains an in-memory mapping of improvement ids to lists of ids they depend on.
- Allows adding and retrieving dependencies for individual improvements.
# [AUTO-FIXED F821] # [AUTO-FIXED F821] - Produces a dependency-aware ordering (a topological-like sort) for a provided list of improvement ids where dependencies that also appear in the input list are visited before dependents.
- Performs a depth-first traversal while avoiding infinite recursion by tracking temporary and permanent visitation sets; cycles are silently ignored (nodes already in the temporary set are skipped).

WHAT IT SHOULD DO BETTER:
- Detect and report dependency cycles explicitly instead of silently skipping them; raise a clear exception for cyclic dependencies.
- Validate inputs and surface missing nodes or transitive dependencies outside the provided improvement set if that matters to callers.
- Preserve deterministic ordering for nodes with no dependency relationship (stable sort) and document ordering guarantees.
# [AUTO-FIXED F821] - Add unit tests covering edge cases (self-dependency, disconnected graphs, large dependency graphs) and benchmarks for performance.
- Consider thread-safety or async-safe variants if used concurrently, and add type/contract enforcement and richer error messages.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py

from __future__ import annotations


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION



class DependencyResolver:
    """Resolves improvement dependencies.
# [AUTO-FIXED F821]     def __init__(self) -> None:
# [AUTO-FIXED F821]         self.dependencies: dict[str, list[str]] = {}

# [AUTO-FIXED F821]     def add_dependency(self, improvement_id: str, depends_on_id: str) -> None:
# [AUTO-FIXED F821]         self.dependencies.setdefault(improvement_id, []).append(depends_on_id)

# [AUTO-FIXED F821]     def get_dependencies(self, improvement_id: str) -> list[str]:
# [AUTO-FIXED F821]         return list(self.dependencies.get(improvement_id, []))

# [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821]     def resolve_order(self, improvement_ids: list[str]) -> list[str]:
        """Topologically sort the given ids so dependencies come first.# [AUTO-FIXED F821] # [AUTO-FIXED F821]         visited: set[str] = set()
# [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821]         temp: set[str] = set()
# [AUTO-FIXED F821] # [AUTO-FIXED F821]         ordered: list[str] = []

# [AUTO-FIXED F821] # [AUTO-FIXED F821]     def visit(node: str) -> None:
# [AUTO-FIXED F821] # [AUTO-FIXED F821]         if node in visited:
            return
# [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821]         if node in temp:
            return
# [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821]         temp.add(node)
# [AUTO-FIXED F821]         for dep in self.dependencies.get(node, []):
# [AUTO-FIXED F821] # [AUTO-FIXED F821]             if dep in improvement_ids:
# [AUTO-FIXED F821] # [AUTO-FIXED F821]                 visit(dep)
# [AUTO-FIXED F821] # [AUTO-FIXED F821] # [AUTO-FIXED F821]         temp.remove(node)
# [AUTO-FIXED F821] # [AUTO-FIXED F821]         visited.add(node)
# [AUTO-FIXED F821] # [AUTO-FIXED F821]         ordered.append(node)
# [AUTO-FIXED F821] # [AUTO-FIXED F821]         for node in improvement_ids:
# [AUTO-FIXED F821] # [AUTO-FIXED F821]             visit(node)
# [AUTO-FIXED F821] # [AUTO-FIXED F821]         return ordered
