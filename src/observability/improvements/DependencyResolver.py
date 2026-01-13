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

"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from typing import Dict, List

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