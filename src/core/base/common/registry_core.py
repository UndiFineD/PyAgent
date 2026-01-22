<<<<<<< HEAD
<<<<<<< HEAD
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
from typing import Callable, Dict, Generic, List, Optional, Tuple, TypeVar

from .base_core import BaseCore

T = TypeVar("T")

try:
    import rust_core as rc  # pylint: disable=import-error
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified Registry core for all PyAgent components."""

import logging
from typing import Dict, Any, List, Optional, TypeVar, Generic, Callable, Tuple
from .base_core import BaseCore

T = TypeVar('T')

try:
    import rust_core as rc
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
except ImportError:
    rc = None

logger = logging.getLogger("pyagent.registry")

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class RegistryCore(BaseCore, Generic[T]):
    """
    Generic registry to handle Tools, Signals, Plugins, and Capabilities.
    Standardizes registration, lookup, and lifecycle management.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self, name: str = "generic") -> None:
        BaseCore.__init__(self, name=name)
        self._items: Dict[str, T] = {}
        self._hooks: Dict[str, List[Callable[[str, T], None]]] = {"on_register": [], "on_unregister": []}

    def detect_cycles(self, nodes: List[str], edges: List[Tuple[str, str]]) -> bool:
        """High-speed cycle detection for dependency graphs."""
        if rc and hasattr(rc, "detect_cycles_rust"):  # pylint: disable=no-member
            try:
                return rc.detect_cycles_rust(nodes, edges)  # type: ignore # pylint: disable=no-member
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
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
                return rc.detect_cycles_rust(nodes, edges) # type: ignore
            except Exception: # pylint: disable=broad-exception-caught
                pass
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Simple DFS fallback
        visited = set()
        path = set()
        adj = {n: [] for n in nodes}
        for u, v in edges:
<<<<<<< HEAD
<<<<<<< HEAD
            if u in adj:
                adj[u].append(v)

        def has_cycle(v) -> bool:
=======
            if u in adj: adj[u].append(v)
            
        def has_cycle(v):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
            if u in adj: adj[u].append(v)
            
        def has_cycle(v):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            visited.add(v)
            path.add(v)
            for neighbor in adj.get(v, []):
                if neighbor not in visited:
<<<<<<< HEAD
<<<<<<< HEAD
                    if has_cycle(neighbor):
                        return True
=======
                    if has_cycle(neighbor): return True
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
                    if has_cycle(neighbor): return True
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
                elif neighbor in path:
                    return True
            path.remove(v)
            return False
<<<<<<< HEAD
<<<<<<< HEAD

        for node in nodes:
            if node not in visited:
                if has_cycle(node):
                    return True
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
            
        for node in nodes:
            if node not in visited:
                if has_cycle(node): return True
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return False

    def topological_sort(self, nodes: List[str], edges: List[Tuple[str, str]]) -> List[str]:
        """Rust-accelerated topological sort for agent task ordering."""
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        if rc and hasattr(rc, "topological_sort_rust"):  # pylint: disable=no-member
            try:
                return rc.topological_sort_rust(nodes, edges)  # type: ignore # pylint: disable=no-member
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
 # pylint: disable=broad-exception-caught
                pass

=======
        if rc and hasattr(rc, "topological_sort_rust"):
            return rc.topological_sort_rust(nodes, edges)
=======
        if rc and hasattr(rc, "topological_sort_rust"): # pylint: disable=no-member
            try:
                return rc.topological_sort_rust(nodes, edges) # type: ignore
            except Exception: # pylint: disable=broad-exception-caught
                pass
>>>>>>> 8d4d334f2 (chore: stabilize rust_core and resolve pylint diagnostics in base common cores)
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        if rc and hasattr(rc, "topological_sort_rust"):
            return rc.topological_sort_rust(nodes, edges)
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        # Simple Kahn's algorithm fallback
        in_degree = {n: 0 for n in nodes}
        adj = {n: [] for n in nodes}
        for u, v in edges:
            if u in adj and v in in_degree:
                adj[u].append(v)
                in_degree[v] += 1
<<<<<<< HEAD
<<<<<<< HEAD

=======
        
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
        
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        queue = [n for n in nodes if in_degree[n] == 0]
        sorted_nodes = []
        while queue:
            u = queue.pop(0)
            sorted_nodes.append(u)
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)
<<<<<<< HEAD
<<<<<<< HEAD

        return sorted_nodes if len(sorted_nodes) == len(nodes) else []

    def register(self, key: str, item: Optional[T] = None) -> bool:
        """Register an item with a specific key. Supports single-argument item registration."""
        from typing import cast

        if item is None:
            # Fallback for single-argument registration where key acts as the item
            item = cast(T, key)
            if hasattr(item, "__name__"):
                key = getattr(item, "__name__")
            elif hasattr(item, "agent_name") and isinstance(getattr(item, "agent_name"), str):
                key = getattr(item, "agent_name")
            elif hasattr(item, "name") and isinstance(getattr(item, "name"), str):
                key = getattr(item, "name")
            else:
                key = str(item)

        if key in self._items:
            logger.warning("[%s] Overwriting existing registry item: %s", self.name, key)

        self._items[key] = item

        for hook in self._hooks["on_register"]:
            try:
                hook(key, item)
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logger.error("[%s] Registry hook 'on_register' failed for %s: %s", self.name, key, e)

=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        
        return sorted_nodes if len(sorted_nodes) == len(nodes) else []

    def register(self, key: str, item: T) -> bool:
        """Register an item with a specific key."""
        if key in self._items:
            logger.warning(f"[{self.name}] Overwriting existing registry item: {key}")
        
        self._items[key] = item
        
        for hook in self._hooks["on_register"]:
            try:
                hook(key, item)
            except Exception as e: # pylint: disable=broad-exception-caught
                logger.error(f"[{self.name}] Registry hook 'on_register' failed for {key}: {e}")
        
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        return True

    def unregister(self, key: str) -> Optional[T]:
        """Unregister an item and return it."""
        item = self._items.pop(key, None)
        if item:
            for hook in self._hooks["on_unregister"]:
                try:
                    hook(key, item)
<<<<<<< HEAD
<<<<<<< HEAD
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    logger.error("[%s] Registry hook 'on_unregister' failed for %s: %s", self.name, key, e)
=======
                except Exception as e:
                    logger.error(f"[{self.name}] Registry hook 'on_unregister' failed for {key}: {e}")
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
                except Exception as e:
                    logger.error(f"[{self.name}] Registry hook 'on_unregister' failed for {key}: {e}")
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
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
