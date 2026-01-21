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
from typing import Any
from pathlib import Path
from .btree_store import BTreeKnowledgeStore
from .vector_store import VectorKnowledgeStore
from .graph_store import GraphKnowledgeStore
from .knowledge_pruning_engine import KnowledgePruningEngine

__version__ = VERSION


class KnowledgeEngine:
    """
    Central engine for managing multi-modal knowledge storage.
    Automatically routes data to B-Tree, Vector, or Graph stores.
    Supports recursive compression of 'cold' memory blocks (Phase 128).
    """

    def __init__(self, agent_id: str, base_path: Path) -> None:
        self.agent_id = agent_id
        self.base_path = base_path / agent_id

        self.btree = BTreeKnowledgeStore(agent_id, self.base_path / "structured")
        self.vector = VectorKnowledgeStore(agent_id, self.base_path / "semantic")
        self.graph = GraphKnowledgeStore(agent_id, self.base_path / "relational")
        self.pruning = KnowledgePruningEngine(self)
        self._compressor = None

    def _get_compressor(self) -> bool:
        """Lazy loading of CompressionAgent to avoid circular imports."""
        if self._compressor is None:
            try:
                from src.logic.agents.system.compression_agent import CompressionAgent

                self._compressor = CompressionAgent(
                    str(self.base_path / "compression_config.json")
                )
            except ImportError as e:
                import logging

                logging.error(f"KnowledgeEngine: Failed to load CompressionAgent: {e}")
        return self._compressor

    def compress_memory(self, key: str) -> bool:
        """
        Retrieves content for a key, compresses it via CompressionAgent,
        and replaces the original content with the dense summary.
        """
        compressor = self._get_compressor()
        if not compressor:
            return False

        # Get content from either BTree or Vector (prefer BTree for density)
        content = self.btree.retrieve(key, limit=1)
        if not content:
            content = self.vector.retrieve(key, limit=1)

        if not content:
            return False

        # Compress
        summary = compressor.extract_gist(str(content))

        # update metadata or content to indicate compression
        metadata = {"compressed": True, "original_len": len(str(content))}
        self.store(summary, mode="btree", key=key, metadata=metadata)
        return True

    def store(self, content: Any, mode: str = "vector", **kwargs) -> bool:
        """
        Store knowledge in the specified mode.
        modes: 'vector', 'btree', 'graph'
        """
        key = kwargs.get("key", str(hash(content)))
        self.pruning.log_access(key)  # Mark as vital on store

        if mode == "vector":
            return self.vector.store(key, content, kwargs.get("metadata"))
        elif mode == "btree":
            return self.btree.store(key, content, kwargs.get("metadata"))
        elif mode == "graph":
            return self.graph.store(
                content, kwargs.get("target"), kwargs.get("relationship", "related_to")
            )
        return False

    def query(self, query: Any, mode: str = "vector", limit: int = 5) -> list[Any]:
        self.pruning.log_access(str(query))
        if mode == "vector":
            return self.vector.retrieve(query, limit)
        elif mode == "btree":
            return self.btree.retrieve(query, limit)
        elif mode == "graph":
            return self.graph.retrieve(query, limit)
        return []
