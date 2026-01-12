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

from __future__ import annotations

from src.core.base.version import VERSION
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""
AgentRegistryCore logic for version compatibility and manifest validation.
Pure logic component to be potentially rustified.
"""




import os
from typing import Dict, List, Any, Optional, Tuple
from .VersionGate import VersionGate

class AgentRegistryCore:
    """Pure logic core for Agent Registry."""

    def __init__(self, current_sdk_version: str) -> None:
        self.sdk_version: str = current_sdk_version

    def process_discovered_files(self, file_paths: List[str]) -> Dict[str, Tuple[str, str, Optional[str]]]:
        """
        Processes a list of file paths and extracts agent/orchestrator configurations.
        Expects relative paths from workspace root.
        """
        discovered: Dict[str, Tuple[str, str, Optional[str]]] = {}
        
        for rel_path in file_paths:
            file = os.path.basename(rel_path)
            if file.endswith(".py") and not file.startswith("__"):
                agent_name: str = file[:-3]
                module_path: str = rel_path.replace(os.path.sep, ".").replace("/", ".").replace(".py", "")
                
                # Phase 105: Discovered agents should not default to their own file path as arg
                discovered[agent_name] = (module_path, agent_name, None)
                
                # Add snake_case name for tolerance
                snake_name = self._to_snake_case(agent_name)
                if snake_name not in discovered:
                    discovered[snake_name] = (module_path, agent_name, None)

                # Add short name
                if agent_name.endswith("Agent"):
                    short_name: str = agent_name[:-5]
                    if short_name and short_name not in discovered:
                        discovered[short_name] = (module_path, agent_name, None)
                elif agent_name.endswith("Orchestrator"):
                    short_name: str = agent_name[:-12]
                    if short_name and short_name not in discovered:
                        discovered[short_name] = (module_path, agent_name, None)
        return discovered

    def parse_manifest(self, raw_manifest: Dict[str, Any]) -> Dict[str, Tuple[str, str, Optional[str]]]:
        """
        Parses the raw manifest dictionary and filters incompatible plugins.
        Returns a dict of {AgentName: (module, class, config)}.
        """
        valid_configs: Dict[str, Tuple[str, str, Optional[str]]] = {}
        for key, cfg in raw_manifest.items():
            # Expecting: "AgentName": ["module.path", "ClassName", "arg_path", "min_sdk_version"]
            if isinstance(cfg, list) and len(cfg) >= 2:
                # Extract potential version gate
                min_sdk: str = cfg[3] if len(cfg) > 3 else "1.0.0"
                
                if self.is_compatible(min_sdk):
                    config_path: Optional[str] = cfg[2] if len(cfg) > 2 else None
                    valid_configs[key] = (cfg[0], cfg[1], config_path)
                
        return valid_configs

    def is_compatible(self, required_version: str) -> bool:
        """
        Gatekeeper check using centralized logic.
        """
        return VersionGate.is_compatible(self.sdk_version, required_version)

    def detect_circular_dependencies(self, dep_graph: Dict[str, List[str]]) -> List[List[str]]:
        """
        Logic for detecting circular dependencies in the agent graph.
        Useful for preventing init-loop during complex swarm orchestration.
        Uses DFS to find back-edges.
        """
        visited = set()
        path = []
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
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def validate_agent_structure(self, agent_instance: Any, required_methods: List[str] = None) -> List[str]:
        """
        Checks if an agent instance has the required methods.
        Returns a list of missing methods.
        """
        missing = []
        reqs = required_methods or ["execute", "describe"]
        for method in reqs:
            if not hasattr(agent_instance, method):
                missing.append(method)
        return missing

    def calculate_load_order(self, dep_graph: Dict[str, List[str]]) -> List[str]:
        """
        Calculates optimal load order for agents based on their dependencies.
        Ensures dependencies are loaded before agents that require them.
        Uses topological sort (Kahn's Algorithm variant).
        """
        # Calculate in-degrees
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
