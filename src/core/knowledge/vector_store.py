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
from .storage_base import KnowledgeStore
from typing import Any
import logging

__version__ = VERSION


class VectorKnowledgeStore(KnowledgeStore):
    """
    Handles vector-based knowledge storage using ChromaDB.
    Isolated per agent.
    """

    def __init__(self, agent_id: str, storage_path: Any) -> None:
        super().__init__(agent_id, storage_path)
        try:
            import chromadb

            self.client = chromadb.PersistentClient(path=str(self.storage_path))
            self.collection = self.client.get_or_create_collection(
                name=f"{agent_id}_knowledge"
            )
        except (ImportError, AttributeError):
            self.client = None
            logging.warning(
                "ChromaDB not installed or incompatible, VectorKnowledgeStore will be disabled."
            )

    def store(
        self, key: str, value: str, metadata: dict[str, Any] | None = None
    ) -> bool:
        if not self.client:
            return False
        self.collection.add(
            documents=[value], metadatas=[metadata] if metadata else [{}], ids=[key]
        )
        return True

    def retrieve(self, query: str, limit: int = 5) -> list[Any]:
        if not self.client:
            return []
        results = self.collection.query(query_texts=[query], n_results=limit)
        return results.get("documents", [[]])[0]

    def delete(self, key: str) -> bool:
        if not self.client:
            return False
        self.collection.delete(ids=[key])
        return True
