# SPDX-License-Identifier: Apache-2.0
"""
PackKV: LLM-Aware Lossy Compression for KV Cache.
Ref: arXiv:2512.24449
"""

from typing import Dict, List, Optional, Any
from .managers import SingleTypeKVCacheManager
from .data_classes import KVCacheBlock, CacheGroupSpec
from .structural import BlockPool

class PackKVManager(SingleTypeKVCacheManager):
    """
    Manager for PackKV compressed cache blocks.
    Implements metadata tracking for quantization scales and permutations.
    """
    def __init__(self, spec: CacheGroupSpec, block_pool: BlockPool) -> None:
        super().__init__(spec, block_pool)
        self.bit_width = getattr(spec, "bit_width", 4)
        self.compression_metadata: Dict[int, Dict[str, Any]] = {}

    def get_num_blocks_needed(self, num_tokens: int) -> int:
        from math import ceil
        # PackKV typically uses 4-bit quantization, 
        # allowing 4x more tokens per physical block if stored densely.
        # But if physical blocks are fixed-size, we track compressed groups.
        return ceil(num_tokens / self.spec.block_size)

    def set_compression_metadata(self, block_id: int, scale: float, min_val: float, permutation: List[int]):
        """Store metadata required for register-level decompression."""
        self.compression_metadata[block_id] = {
            "scale": scale,
            "min": min_val,
            "permutation": permutation
        }

    def get_compression_metadata(self, block_id: int) -> Optional[Dict[str, Any]]:
        return self.compression_metadata.get(block_id)

    def free(self, request_id: str) -> None:
        blocks = self.request_blocks.get(request_id, [])
        for block in blocks:
            if block.block_id in self.compression_metadata:
                del self.compression_metadata[block.block_id]
        super().free(request_id)
