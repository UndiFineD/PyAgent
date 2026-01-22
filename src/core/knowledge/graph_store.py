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
from src.core.base.lifecycle.version import VERSION
import hashlib
from .storage_base import KnowledgeStore
from typing import Any
from pathlib import Path

__version__ = VERSION


class GraphKnowledgeStore(KnowledgeStore):
    """
    Sharded Graph storage for relational and ontological knowledge.
    Scales to trillions of triples by sharding nodes across the filesystem.
    Utilization of MemoryCore for standardized backend.
    """

    def _hash_node(self, node_id: str) -> str:
        return hashlib.md5(node_id.encode()).hexdigest()

    def _get_node_path(self, node_id: str) -> Path:
        """Hierarchical Sharding for Graph Nodes (Phase 130)."""
        hash_val = self._hash_node(node_id)
        tier1 = hash_val[:2]
        tier2 = hash_val[2:4]

        # Use MemoryCore via base class to ensure path alignment
        shard_dir = self.storage_path / tier1 / tier2
        shard_dir.mkdir(exist_ok=True, parents=True)
        return shard_dir / f"{node_id}.json"

    def store(self, node: str, target: Any, relationship: str = "related_to") -> bool:
        path = self._get_node_path(node)

        # Use memory_core.retrieve_knowledge logic or standardized load_json
        data = self._memory_core._storage.load_json(path)
        if not data:
            data = {"id": node, "edges": []}

        data["edges"].append({"to": target, "type": relationship})

        # Atomic write via storage core
        self._memory_core._storage.save_json(path, data)
        return True

    def retrieve(self, node: str, limit: int = 5) -> list[Any]:
        path = self._get_node_path(node)
        data = self._memory_core._storage.load_json(path)
        if data:
            return data.get("edges", [])[:limit]
        return []

    def delete(self, node: str) -> bool:
        path = self._get_node_path(node)
        if path.exists():
            path.unlink()
            return True
        return False
