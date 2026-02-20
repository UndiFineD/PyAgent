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
Encrypted Memory Store shim for tests.

"""
Provides a thin wrapper delegating to the backend store without
performing real encryption. This keeps imports and API compatibility
for unit tests while avoiding dependency on the full crypto stack.
"""
try:
    from typing import Any, Dict, List, Optional, Tuple
except ImportError:
    from typing import Any, Dict, List, Optional, Tuple


try:
    from ..memory_core import MemoryNode, MemoryStore
except ImportError:
    from ..memory_core import MemoryNode, MemoryStore

try:
    from .e2e_encryption_core import E2EEncryptionCore
except ImportError:
    from .e2e_encryption_core import E2EEncryptionCore





class EncryptedMemoryStore:
    def __init__(self, backend_store: MemoryStore, e2e_core: E2EEncryptionCore):
        self.backend = backend_store
        self.e2e_core = e2e_core

        async def store_memory(self, user_id: str, node: MemoryNode) -> str:
        return await self.backend.store_memory(node)

        async def get_memory(self, user_id: str, memory_id: str) -> Optional[MemoryNode]:
        return await self.backend.get_memory(memory_id)

        async def search_similar(self, user_id: str, query_embedding: List[float], limit: int = 10, threshold: float = 0.7) -> List[Tuple[MemoryNode, float]]:
        return await self.backend.search_similar(query_embedding, limit, threshold)

        async def update_memory(self, user_id: str, memory_id: str, updates: Dict[str, Any]) -> bool:
        return await self.backend.update_memory(user_id, memory_id, updates)

        async def delete_memory(self, user_id: str, memory_id: str) -> bool:
        return await self.backend.delete_memory(memory_id)
