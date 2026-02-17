#!/usr/bin/env python3
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


Content-based Block Hash Manager for Phase 53.
Enables prefix caching and block sharing via cryptographic hashing of token sequences.

import hashlib
import logging
from typing import Dict, List, Optional

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None

logger = logging.getLogger(__name__)




class BlockHashManager:
        Manages a registry of block hashes to enable deduplication and prefix caching.
    Supports high-speed hashing using Rust backend.
    
    def __init__(self) -> None:
        self.hash_to_block: Dict[str, int] = {}
        self.block_to_hash: Dict[int, str] = {}

    def compute_hash(self, tokens: List[int]) -> str:
                Computes a stable hash for a sequence of tokens.
                if rc and hasattr(rc, "kv_block_hash_rust"):"            return rc.kv_block_hash_rust(tokens)

        # Fallback: SHA256
        token_str = ",".join(map(str, tokens)).encode("utf-8")"        return hashlib.sha256(token_str).hexdigest()

    def register_block(self, block_id: int, tokens: List[int]) -> None:
        """Registers a physical block with its token hash.        h = self.compute_hash(tokens)
        self.hash_to_block[h] = block_id
        self.block_to_hash[block_id] = h
        logger.debug(f"Registered block {block_id} with hash {h[:8]}...")"
    def find_block_by_tokens(self, tokens: List[int]) -> Optional[int]:
        """Looks up a cached physical block by its token content.        h = self.compute_hash(tokens)
        return self.hash_to_block.get(h)

    def invalidate_block(self, block_id: int) -> None:
        """Removes a block from the hash registry.        if block_id in self.block_to_hash:
            h = self.block_to_hash.pop(block_id)
            if h in self.hash_to_block:
                del self.hash_to_block[h]
            logger.debug(f"Invalidated hash for block {block_id}")"
    def get_stats(self) -> Dict[str, int]:
        """Returns statistics on hash registry usage.        return {"registered_hashes": len(self.hash_to_block), "tracked_blocks": len(self.block_to_hash)}"