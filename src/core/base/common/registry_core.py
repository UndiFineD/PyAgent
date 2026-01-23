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

"""Unified Registry core for all PyAgent components."""

import logging
from typing import Dict, List, Optional, TypeVar, Generic, Callable, Tuple
from .base_core import BaseCore

T = TypeVar('T')

try:
    import rust_core as rc # pylint: disable=import-error
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.registry")


class RegistryCore(BaseCore, Generic[T]):
    """
    Generic registry to handle Tools, Signals, Plugins, and Capabilities.
    Standardizes registration, lookup, and lifecycle management.
    """
    def __init__(self, name: str):
        BaseCore.__init__(self, name=name)
        self._items: Dict[str, T] = {}
        self._hooks: Dict[str, List[Callable[[str, T], None]]] = {
            "on_register": [],
            "on_unregister": []
        }

    def detect_cycles(self, nodes: List[str], edges: List[Tuple[str, str]]) -> bool:
        """High-speed cycle detection for dependency graphs."""
        if rc and hasattr(rc, "detect_cycles_rust"): # pylint: disable=no-member
            try:
                return rc.detect_cycles_rust(nodes, edges) # type: ignore # pylint: disable=no-member
            except Exception: # pylint: disable=broad-exception-caught
                pass

        # Simple DFS fallback
        visited = set()
        path = set()
        adj = {n: [] for n in nodes}
        for u, v in edges:
            if u in adj:
                adj[u].append(v)

        def has_cycle(v):
            visited.add(v)
            path.add(v)
            for neighbor in adj.get(v, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in path:
                    return True
            path.remove(v)
            return False

        for node in nodes:
            if node not in visited:
                if has_cycle(node):
                    return True
        return False

    def topological_sort(self, nodes: List[str], edges: List[Tuple[str, str]]) -> List[str]:
        """Rust-accelerated topological sort for agent task ordering."""
        if rc and hasattr(rc, "topological_sort_rust"): # pylint: disable=no-member
            try:
                return rc.topological_sort_rust(nodes, edges) # type: ignore # pylint: disable=no-member
            except Exception: # pylint: disable=broad-exception-caught
                pass

        # Simple Kahn's algorithm fallback
        in_degree = {n: 0 for n in nodes}
        adj = {n: [] for n in nodes}
        for u, v in edges:
            if u in adj and v in in_degree:
                adj[u].append(v)
                in_degree[v] += 1

        queue = [n for n in nodes if in_degree[n] == 0]
        sorted_nodes = []
        while queue:
            u = queue.pop(0)
            sorted_nodes.append(u)
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        return sorted_nodes if len(sorted_nodes) == len(nodes) else []

    def register(self, key: str, item: T) -> bool:
        """Register an item with a specific key."""
        if key in self._items:
            logger.warning("[%s] Overwriting existing registry item: %s", self.name, key)

        self._items[key] = item

        for hook in self._hooks["on_register"]:
            try:
                hook(key, item)
            except Exception as e: # pylint: disable=broad-exception-caught
                logger.error("[%s] Registry hook 'on_register' failed for %s: %s", self.name, key, e)

        return True

    def unregister(self, key: str) -> Optional[T]:
        """Unregister an item and return it."""
        item = self._items.pop(key, None)
        if item:
            for hook in self._hooks["on_unregister"]:
                try:
                    hook(key, item)
                except Exception as e: # pylint: disable=broad-exception-caught
                    logger.error("[%s] Registry hook 'on_unregister' failed for %s: %s", self.name, key, e)
        return item

    def get(self, key: str) -> Optional[T]:
        """Retrieve an item by key."""
        return self._items.get(key)

    def list_keys(self) -> List[str]:
        """List all registered keys."""
        return list(self._items.keys())

    def list_items(self) -> List[T]:
        """List all registered items."""
        return list(self._items.values())

    def clear(self) -> None:
        """Clear the registry."""
        self._items.clear()

    def add_hook(self, event: str, callback: Callable[[str, T], None]) -> None:
        """Add a lifecycle hook."""
        if event in self._hooks:
            self._hooks[event].append(callback)
        else:
            raise ValueError(f"Unsupported registry event: {event}")
