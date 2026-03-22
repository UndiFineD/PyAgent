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
"""SwarmMemory — shared and local memory domains for the swarm (prj0000022)."""
from __future__ import annotations

import asyncio
from typing import Any


class SwarmMemory:
    """Dual-domain memory: shared (cluster-wide) and local (per-node).

    In this initial implementation, both domains are backed by in-process
    dicts.  A real deployment would replace the shared store with a
    Redis or CRDT-backed backend.
    """

    def __init__(self) -> None:
        self._shared: dict[str, Any] = {}
        self._local: dict[str, dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def shared_set(self, key: str, value: Any) -> None:
        """Write a value to the shared domain."""
        async with self._lock:
            self._shared[key] = value

    async def shared_get(self, key: str, default: Any = None) -> Any:
        """Read a value from the shared domain."""
        async with self._lock:
            return self._shared.get(key, default)

    async def local_set(self, node_id: str, key: str, value: Any) -> None:
        """Write a value to a node's local domain."""
        async with self._lock:
            self._local.setdefault(node_id, {})[key] = value

    async def local_get(self, node_id: str, key: str, default: Any = None) -> Any:
        """Read a value from a node's local domain."""
        async with self._lock:
            return self._local.get(node_id, {}).get(key, default)

    async def shared_keys(self) -> list[str]:
        """Return all keys in the shared domain."""
        async with self._lock:
            return list(self._shared.keys())

    def metrics(self) -> str:
        """Prometheus-style metrics string."""
        lines = [
            f"swarm_memory_shared_keys {len(self._shared)}",
            f"swarm_memory_local_nodes {len(self._local)}",
        ]
        return "\n".join(lines)
