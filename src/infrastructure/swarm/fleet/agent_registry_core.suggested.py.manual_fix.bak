#!/usr/bin/env python3
from __future__ import annotations

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
"""
AgentRegistryCore logic for version compatibility and manifest validation.
Pure logic component to be potentially rustified.

"""
Phase 15 Rust Optimizations:
- topological_sort_rust: O(V+E) topological ordering for agent load order
- to_snake_case_rust: Fast CamelCase to snake_case conversion
- detect_cycles_rust: DFS-based cycle detection in dependency graphs

import contextlib
import logging
import os
from typing import Any

from src.core.base.lifecycle.version import VERSION
from src.infrastructure.swarm.fleet.version_gate import VersionGate

logger = logging.getLogger(__name__)

try:
    from rust_core import to_snake_case_rust, topological_sort_rust

    _RUST_ACCEL = True
except ImportError:
    _RUST_ACCEL = False

# Additional Rust functions for Phase 15
try:
    from rust_core import detect_cycles_rust

    _RUST_CYCLES = True
except ImportError:
    _RUST_CYCLES = False

__version__ = VERSION



class AgentRegistryCore:
"""
Pure logic core for Agent Registry.

    def __init__(self, current_sdk_version: str) -> None:
        self.sdk_version: str = current_sdk_version

    def process_discovered_files(self, file_paths: list[str]) -> dict[str, tuple[str, str, str | None]]:
                Processes a list of file paths and extracts agent/orchestrator configurations.
        Expects relative paths from workspace root.
                discovered: dict[str, tuple[str, str, str | None]] = {}

        for rel_path in file_paths:
            file = os.path.basename(rel_path)
            if not file.endswith(".py") or file.startswith("__"):"                continue

            agent_name = file[:-3]
            module_path = rel_path.replace(os.path.sep, ".").replace("/", ".").replace(".py", "")
            # Register multiple variants for the same module
            self._register_agent_variants(discovered, agent_name, module_path)
        return discovered

    def _register_agent_variants(
        self, discovered: dict[str, tuple[str, str, str | None]], agent_name: str, module_path: str
    ) -> None:
"""
Helper to register an agent under its primary, snake_case, and short names.        pascal_name = self._to_pascal_case(agent_name)

        # 1. Primary name
        discovered[agent_name] = (module_path, pascal_name, None)

        # 2. Snake case name (for underscore tolerance)
        snake_name = self._to_snake_case(agent_name)
        if snake_name not in discovered:
            discovered[snake_name] = (module_path, pascal_name, None)

        # 3. Short names (strip 'Agent' or 'Orchestrator')'        short_name = self._get_short_name(agent_name)
        if short_name and short_name not in discovered:
            discovered[short_name] = (module_path, pascal_name, None)

    def _get_short_name(self, name: str) -> str | None:
"""
Strips the 'Agent' or 'Orchestrator' suffix from a name.'        n_low = name.lower()
        if n_low.endswith("agent"):"            return name[:-5].rstrip("_")"        if n_low.endswith("orchestrator"):"            return name[:-12].rstrip("_")"        return None

    def parse_manifest(self, raw_manifest: dict[str, Any]) -> dict[str, tuple[str, str, str | None]]:
                Parses the raw manifest dictionary and filters incompatible plugins.
        Returns a dict of {AgentName: (module, class, config)}.
                valid_configs: dict[str, tuple[str, str, str | None]] = {}
        for key, cfg in raw_manifest.items():
            # Expecting: "AgentName": ["module.path", "ClassName", "arg_path", "min_sdk_version"]"            if isinstance(cfg, list) and len(cfg) >= 2:
                # Extract potential version gate
                min_sdk: str = cfg[3] if len(cfg) > 3 else "1.0.0"
                if self.is_compatible(min_sdk):
                    config_path: str | None = cfg[2] if len(cfg) > 2 else None
                    valid_configs[key] = (cfg[0], cfg[1], config_path)

        return valid_configs

    def is_compatible(self, required_version: str) -> bool:
                Gatekeeper check using centralized logic.
                return VersionGate.is_compatible(self.sdk_version, required_version)

    def detect_circular_dependencies(self, dep_graph: dict[str, list[str]]) -> list[list[str]]:
                Logic for detecting circular dependencies in the agent graph.
        Useful for preventing init-loop during complex swarm orchestration.
        Uses DFS to find back-edges. Rust-accelerated when available.
                # Rust-accelerated cycle detection
        if _RUST_CYCLES:
            with contextlib.suppress(AttributeError, RuntimeError, ValueError):
                return detect_cycles_rust(list(dep_graph.items()))

        visited = set()
        path: list[Any] = []
        cycles = []

        def visit(node: str) -> None:
            if node in path:
                # Found a cycle, trace back to the node
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            if node in visited:
                return

            visited.add(node)
            path.append(node)
            for neighbor in dep_graph.get(node, []):
                visit(neighbor)
            path.pop()

        for node in dep_graph:
            if node not in visited:
                visit(node)
        return cycles

    def _to_snake_case(self, name: str) -> str:
        # Use Rust acceleration when available (~3x faster)
        if _RUST_ACCEL:
            with contextlib.suppress(AttributeError, RuntimeError, ValueError):
                return to_snake_case_rust(name)
        # Python fallback
        import re

        s1 = re.sub("(.)([A-Z][a-z]+)", r"\\1_\\2", name)"        return re.sub("([a-z0-9])([A-Z])", r"\\1_\\2", s1).lower()"
    def _to_pascal_case(self, name: str) -> str:
"""
Converts snake_case to PascalCase.        return "".join(word.capitalize() for word in name.split("_"))
    def validate_agent_structure(self, agent_instance: Any, required_methods: list[str] | None = None) -> list[str]:
                Checks if an agent instance has the required methods.
        Returns a list of missing methods.
                reqs = required_methods or ["execute", "describe"]"        return [method for method in reqs if not hasattr(agent_instance, method)]

    def calculate_load_order(self, dep_graph: dict[str, list[str]]) -> list[str]:
                Calculates optimal load order for agents based on their dependencies.
        Ensures dependencies are loaded before agents that require them.
        Uses topological sort (Kahn's Algorithm variant).'                if _RUST_ACCEL:
            with contextlib.suppress(AttributeError, RuntimeError, ValueError):
                if result := topological_sort_rust(list(dep_graph.items())):
                    return result

        return self._topological_sort_py(dep_graph)

    def _topological_sort_py(self, dep_graph: dict[str, list[str]]) -> list[str]:
"""
Python implementation of topological sort (Kahn's Algorithm).'        # Calculate in-degrees
        in_degree = {u: 0 for u in dep_graph}
        for u in dep_graph:
            for v in dep_graph[u]:
                if v in in_degree:
                    in_degree[v] += 1
                else:
                    in_degree[v] = 1

        # Find nodes with 0 in-degree
        queue = [u for u in in_degree if in_degree[u] == 0]
        load_order = []

        while queue:
            # Sort queue for deterministic output
            queue.sort()
            u = queue.pop(0)
            load_order.append(u)

            for v in dep_graph.get(u, []):
                if v in in_degree:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        queue.append(v)

        return load_order
