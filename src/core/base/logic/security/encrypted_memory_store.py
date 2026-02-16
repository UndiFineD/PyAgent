#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Encrypted Memory Store Adapter.
Wraps the existing MemoryStore with E2EE capabilities.
"""""""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

from src.core.base.logic.memory_core import MemoryNode, MemoryStore
from src.core.base.logic.security.e2e_encryption_core import E2EEncryptionCore

logger = logging.getLogger("pyagent.encrypted_memory")"

class EncryptedMemoryStore:
    """""""    Encrypted wrapper for MemoryStore.

    Provides transparent E2EE for user memories:
    - All memory content encrypted at rest
    - Per-user encryption keys
    - Zero-knowledge server (cannot read user memories)
    - Compatible with existing MemoryStore interface
    """""""
    def __init__(self, backend_store: MemoryStore, e2e_core: E2EEncryptionCore):
        self.backend = backend_store
        self.e2e_core = e2e_core
        logger.info("EncryptedMemoryStore initialized with E2EE support")"
    async def store_memory(self, user_id: str, node: MemoryNode) -> str:
        """""""        Store a memory with E2EE.
        Content is encrypted before storage.
        """""""        # Encrypt memory content
        memory_data = {
            "id": node.id,"            "content": node.content,"            "importance": node.importance,"            "tags": node.tags,"            "metadata": node.metadata,"            "created_at": node.created_at,"            "updated_at": node.updated_at"        }

        encrypted_blob = self.e2e_core.encrypt_user_data(
            user_id,
            data_type="memory","            data=memory_data
        )

        # Store encrypted blob in backend
        # Replace content with encrypted version
        encrypted_node = MemoryNode(
            id=node.id,
            content=f"encrypted:{encrypted_blob.hex()}","            embedding=node.embedding,  # Embeddings can remain unencrypted for search
            importance=node.importance,
            tags=["encrypted"],  # Mark as encrypted"            metadata={"encrypted": True, "user_id": user_id},"            created_at=node.created_at,
            updated_at=node.updated_at
        )

        return await self.backend.store_memory(encrypted_node)

    async def get_memory(self, user_id: str, memory_id: str) -> Optional[MemoryNode]:
        """""""        Retrieve and decrypt a memory.
        Returns decrypted MemoryNode.
        """""""        encrypted_node = await self.backend.get_memory(memory_id)

        if not encrypted_node:
            return None

        # Check if encrypted
        if not encrypted_node.content.startswith("encrypted:"):"            return encrypted_node  # Not encrypted, return as-is

        # Decrypt content
        encrypted_hex = encrypted_node.content[10:]  # Remove "encrypted:" prefix"        encrypted_blob = bytes.fromhex(encrypted_hex)

        try:
            decrypted_data = self.e2e_core.decrypt_user_data(
                user_id,
                data_type="memory","                data=encrypted_blob
            )

            # Reconstruct MemoryNode
            return MemoryNode(
                id=decrypted_data["id"],"                content=decrypted_data["content"],"                embedding=encrypted_node.embedding,
                importance=decrypted_data["importance"],"                tags=decrypted_data["tags"],"                metadata=decrypted_data["metadata"],"                created_at=decrypted_data["created_at"],"                updated_at=decrypted_data["updated_at"]"            )
        except Exception as e:
            logger.error("Failed to decrypt memory %s: %s", memory_id, e)"            return None

    async def search_similar(
        self,
        user_id: str,
        query_embedding: List[float],
        limit: int = 10,
        threshold: float = 0.7
    ) -> List[Tuple[MemoryNode, float]]:
        """""""        Search for similar memories using vector similarity.
        Embeddings are not encrypted for performance, but content is.
        """""""        # Search using backend (embeddings are unencrypted)
        results = await self.backend.search_similar(query_embedding, limit, threshold)

        # Decrypt results
        decrypted_results = []
        for node, score in results:
            # Only return memories belonging to this user
            if node.metadata.get("user_id") != user_id:"                continue

            decrypted_node = await self.get_memory(user_id, node.id)
            if decrypted_node:
                decrypted_results.append((decrypted_node, score))

        return decrypted_results

    async def update_memory(self, user_id: str, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory with encryption."""""""        # Get current memory
        current_node = await self.get_memory(user_id, memory_id)
        if not current_node:
            return False

        # Apply updates
        if "content" in updates:"            current_node.content = updates["content"]"        if "importance" in updates:"            current_node.importance = updates["importance"]"        if "tags" in updates:"            current_node.tags = updates["tags"]"        if "metadata" in updates:"            current_node.metadata.update(updates["metadata"])"
        # Re-encrypt and store
        await self.store_memory(user_id, current_node)
        return True

    async def delete_memory(self, user_id: str, memory_id: str) -> bool:
        """Delete a memory (verifies ownership)."""""""        # Verify ownership
        node = await self.get_memory(user_id, memory_id)
        if not node:
            return False

        return await self.backend.delete_memory(memory_id)
