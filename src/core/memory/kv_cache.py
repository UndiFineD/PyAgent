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

"""
Module: kv_cache
Implements Pillar 2: Near-Metal Cognitive Scaling via Paged Attention KV-Cache.
"""

from __future__ import annotations
import logging
import numpy as np
from typing import Dict, List, Optional, Any
from src.core.rust_bridge import get_bridge

logger = logging.getLogger(__name__)

class KVCacheManager:
    """
    Implements Paged Attention KV-Cache for high-throughput context management.
    Uses Rust-accelerated block management and hashing.
    """

    def __init__(self, num_blocks: int = 1024, block_size: int = 16, head_dim: int = 128):
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.head_dim = head_dim
        
        # Rust-accelerated block management
        self.free_blocks = get_bridge().manage_kv_blocks(num_blocks, block_size)
        self.active_blocks: Dict[str, List[int]] = {}  # prefix_hash -> block_indices
        
        # Physical Cache (simulated as numpy for now, but managed by Rust offsets)
        self.k_cache = np.zeros((num_blocks * block_size, head_dim), dtype=np.float32)
        self.v_cache = np.zeros((num_blocks * block_size, head_dim), dtype=np.float32)
        
        logger.info(f"KVCacheManager initialized with {num_blocks} blocks (Pillar 2)")

    def get_or_allocate(self, tokens: List[int]) -> List[int]:
        """Gets existing blocks for a token prefix or allocates new ones."""
        token_hash = get_bridge().get_token_hash(tokens)
        
        if token_hash in self.active_blocks:
            return self.active_blocks[token_hash]
        
        # Allocation logic (Phase 53)
        num_needed = (len(tokens) + self.block_size - 1) // self.block_size
        allocated = []
        
        for _ in range(num_needed):
            if self.free_blocks:
                allocated.append(self.free_blocks.pop(0))
            else:
                # Eviction policy (LRU would go here)
                logger.warning("KVCache: Cache full, evicting oldest block")
                evicted_key = next(iter(self.active_blocks))
                evicted_blocks = self.active_blocks.pop(evicted_key)
                self.free_blocks.extend(evicted_blocks)
                allocated.append(self.free_blocks.pop(0))
                
        self.active_blocks[token_hash] = allocated
        return allocated

    def clear(self):
        """Emergency purge of the KV cache."""
        self.free_blocks = get_bridge().manage_kv_blocks(self.num_blocks, self.block_size)
        self.active_blocks.clear()
        logger.info("KVCache: Purged all blocks")
