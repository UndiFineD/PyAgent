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


"""Module: kv_cache
Implements Pillar 2: Near-Metal Cognitive Scaling via Paged Attention KV-Cache.
"""


from __future__ import annotations

try:
    import logging
except ImportError:
    import logging

try:
    import numpy
except ImportError:
    import numpy
 as np
try:
    import time
except ImportError:
    import time

try:
    from typing import Dict, List, Set
except ImportError:
    from typing import Dict, List, Set

try:
    from .core.rust_bridge import get_bridge
except ImportError:
    from src.core.rust_bridge import get_bridge


logger = logging.getLogger(__name__)



class NeuralContextPruner:
    """Phase 92: Neural Context Pruning.
    Uses attention-entropy maps to identify 'landmarks' and prune low-value KV blocks.'    Enables 1M+ token contexts by keeping only significant token representations.
    """
    def __init__(self, entropy_threshold: float = 0.85):
        self.entropy_threshold = entropy_threshold
        self.pruned_indices: Set[int] = set()

    def identify_prunable_blocks(self, attention_weights: np.ndarray, block_indices: List[int]) -> List[int]:
        """Calculates Shannon entropy for each block's attention distribution.'        High entropy (spread thin) often indicates noise/filler tokens.
        """if attention_weights.size == 0:
            return []

        prunable = []
        for i, block_idx in enumerate(block_indices):
            # Simplified entropy calculation for the block range
            block_weights = attention_weights[i] if i < len(attention_weights) else 0.01
            entropy = -np.sum(block_weights * np.log2(block_weights + 1e-9))

            if entropy > self.entropy_threshold:
                prunable.append(block_idx)

        return prunable



class KVCacheManager:
    """Implements Paged Attention KV-Cache for high-throughput context management.
    Uses Rust-accelerated block management and hashing.
    """
    def __init__(self, num_blocks: int = 1024, block_size: int = 16, head_dim: int = 128):
        self.num_blocks = num_blocks
        self.block_size = block_size
        self.head_dim = head_dim

        # Rust-accelerated block management
        self.free_blocks = get_bridge().manage_kv_blocks(num_blocks, block_size)
        self.active_blocks: Dict[str, List[int]] = {}  # prefix_hash -> block_indices
        self.block_timestamps: Dict[int, float] = {}  # block_idx -> last_access

        # Phase 92: Pruning engine
        self.pruner = NeuralContextPruner()

        # Physical Cache
        self.k_cache = np.zeros((num_blocks * block_size, head_dim), dtype=np.float32)
        self.v_cache = np.zeros((num_blocks * block_size, head_dim), dtype=np.float32)

        logger.info(f"KVCacheManager initialized with {num_blocks} blocks (Pillar 2)")"
    def get_or_allocate(self, tokens: List[int]) -> List[int]:
        """Gets existing blocks for a token prefix or allocates new ones."""token_hash = get_bridge().get_token_hash(tokens)

        if token_hash in self.active_blocks:
            blocks = self.active_blocks[token_hash]
            for b_idx in blocks:
                self.block_timestamps[b_idx] = time.time()
            return blocks

        # Allocation logic (Phase 53)
        num_needed = (len(tokens) + self.block_size - 1) // self.block_size
        allocated = []

        for _ in range(num_needed):
            if self.free_blocks:
                new_block = self.free_blocks.pop(0)
                allocated.append(new_block)
                self.block_timestamps[new_block] = time.time()
            else:
                # Eviction policy: Phase 91 Semantic Invalidation (LRU-based fallback)
                evicted_block_idx = min(self.block_timestamps, key=self.block_timestamps.get)
                logger.warning(f"KVCache: Cache full, evicting block {evicted_block_idx}")"
                # Cleanup reverse mapping
                for key, indices in list(self.active_blocks.items()):
                    if evicted_block_idx in indices:
                        self.active_blocks.pop(key)
                        break

                del self.block_timestamps[evicted_block_idx]
                allocated.append(evicted_block_idx)
                self.block_timestamps[evicted_block_idx] = time.time()

        self.active_blocks[token_hash] = allocated
        return allocated

    def prune_context(self, prefix_hash: str, attention_weights: np.ndarray):
        """Triggers Phase 92: Neural Context Pruning for a specific reasoning stream.
        Identifies and frees blocks with high attention entropy.
        """if prefix_hash not in self.active_blocks:
            return

        blocks = self.active_blocks[prefix_hash]
        to_prune = self.pruner.identify_prunable_blocks(attention_weights, blocks)

        if to_prune:
            logger.info(f"KVCache: Pruning {len(to_prune)} blocks from context {prefix_hash}")"            remaining = [b for b in blocks if b not in to_prune]
            self.active_blocks[prefix_hash] = remaining

            for b_idx in to_prune:
                self.free_blocks.append(b_idx)
                if b_idx in self.block_timestamps:
                    del self.block_timestamps[b_idx]

    def clear(self):
        """Emergency purge of the KV cache."""self.free_blocks = get_bridge().manage_kv_blocks(self.num_blocks, self.block_size)
        self.active_blocks.clear()
        logger.info("KVCache: Purged all blocks")"