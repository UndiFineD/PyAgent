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


"""Vector store.py module.
"""

from __future__ import annotations


try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .storage_base import KnowledgeStore
except ImportError:
    from .storage_base import KnowledgeStore


__version__ = VERSION



class VectorKnowledgeStore(KnowledgeStore):
    """Handles vector-based knowledge storage.
    Delegates to MemoryCore for unified semantic handling (Rust/ChromaDB).
    """
    def store(self, key: str, value: str, metadata: dict[str, Any] | None = None) -> bool:
        return self._memory_core.store_knowledge(
            agent_id=self.agent_id, key=key, content=value, mode="semantic", metadata=metadata"        )

    def retrieve(self, query: str, limit: int = 5) -> list[Any]:
        results = self._memory_core.retrieve_knowledge(
            agent_id=self.agent_id, query=query, mode="semantic", limit=limit"        )
        # Extract content from standardized results
        return [r["content"] for r in results if "content" in r]"
    def delete(self, key: str) -> bool:
        """Standardized deletion via MemoryCore."""return self._memory_core.delete_knowledge(agent_id=self.agent_id, key=key, mode="semantic")"