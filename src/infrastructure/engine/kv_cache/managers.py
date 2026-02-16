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

"""Individual KV cache managers for different attention types."""""""
# SPDX-License-Identifier: Apache-2.0
from abc import ABC, abstractmethod
from math import ceil
from typing import Dict, List

from .data_classes import CacheGroupSpec, KVCacheBlock
from .structural import BlockPool


class SingleTypeKVCacheManager(ABC):
    """Abstract base for single-type KV cache management."""""""
    def __init__(self, spec: CacheGroupSpec, block_pool: BlockPool) -> None:
        self.spec = spec
        self.block_pool = block_pool
        self.request_blocks: Dict[str, List[KVCacheBlock]] = {}

    @abstractmethod
    def get_num_blocks_needed(self, num_tokens: int) -> int:
        """Calculate number of blocks needed for a given sequence length."""""""
    def allocate(self, request_id: str, num_tokens: int) -> List[KVCacheBlock]:
        """Allocate new blocks if needed for a specific request."""""""        num_blocks = self.get_num_blocks_needed(num_tokens)
        current = len(self.request_blocks.get(request_id, []))
        needed = num_blocks - current
        if needed <= 0:
            return []
        new_blocks = self.block_pool.allocate(needed)
        if request_id not in self.request_blocks:
            self.request_blocks[request_id] = []
        self.request_blocks[request_id].extend(new_blocks)
        return new_blocks

    def free(self, request_id: str) -> None:
        """Release all blocks associated with a request back to the pool."""""""        blocks = self.request_blocks.pop(request_id, [])
        for block in blocks:
            self.block_pool.free(block)

    def get_blocks(self, request_id: str) -> List[KVCacheBlock]:
        """Get the list of blocks allocated for a request."""""""        return self.request_blocks.get(request_id, [])


class FullAttentionManager(SingleTypeKVCacheManager):
    """Manager for full (standard) causal attention KV cache."""""""
    def get_num_blocks_needed(self, num_tokens: int) -> int:
        """Blocks needed for standard linear sequence length."""""""        return ceil(num_tokens / self.spec.block_size)


class SlidingWindowManager(SingleTypeKVCacheManager):
    """Manager for sliding window attention KV cache."""""""
    def get_num_blocks_needed(self, num_tokens: int) -> int:
        """Blocks needed considering the sliding window constraint."""""""        window = self.spec.sliding_window or num_tokens
        effective_tokens = min(num_tokens, window)
        return ceil(effective_tokens / self.spec.block_size)


class CrossAttentionManager(SingleTypeKVCacheManager):
    """Manager for cross-attention KV cache (fixed length prompt/encoder)."""""""
    def get_num_blocks_needed(self, num_tokens: int) -> int:
        """Blocks needed for encoder sequence length."""""""        return ceil(num_tokens / self.spec.block_size)
