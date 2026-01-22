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
Hierarchical KV-Cache Interface (V2) for Phase 53.
Manages multi-group block allocation and dynamic layer-aware caching.
"""

import logging
<<<<<<< HEAD
<<<<<<< HEAD
from typing import List, Optional

import torch

from src.infrastructure.engine.kv_cache.v2.block_table import BlockTableV2
=======
from typing import Dict, List, Optional, Any, Tuple
import torch
from .block_table import BlockTableV2
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
from typing import Dict, List, Optional, Any, Tuple
import torch
from .block_table import BlockTableV2
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)

try:
    import rust_core as rc
except ImportError:
    rc = None

logger = logging.getLogger(__name__)

<<<<<<< HEAD
<<<<<<< HEAD

=======
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
class KVCacheInterfaceV2:
    """
    High-level interface for managing hierarchical KV-Cache.
    Supports dynamic block allocation and multi-GPU synchronization.
    """
<<<<<<< HEAD
<<<<<<< HEAD

    def __init__(self, num_layers: int, num_heads: int, head_size: int, num_blocks: int, block_size: int = 16) -> None:
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
    
    def __init__(self, 
                 num_layers: int, 
                 num_heads: int, 
                 head_size: int, 
                 num_blocks: int, 
                 block_size: int = 16):
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.head_size = head_size
        self.block_size = block_size
<<<<<<< HEAD
<<<<<<< HEAD

        self.block_table = BlockTableV2(num_blocks, block_size)

        # Physical storage (placeholder for Torch tensors)
        self.k_cache: Optional[torch.Tensor] = None
        self.v_cache: Optional[torch.Tensor] = None

        logger.info(f"KVCacheInterfaceV2 created: {num_layers} layers, {num_heads} heads, {num_blocks} blocks")

    def initialize_storage(self, device: str = "cuda", dtype: torch.dtype = torch.float16) -> None:
=======
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        
        self.block_table = BlockTableV2(num_blocks, block_size)
        
        # Physical storage (placeholder for Torch tensors)
        self.k_cache: Optional[torch.Tensor] = None
        self.v_cache: Optional[torch.Tensor] = None
        
        logger.info(f"KVCacheInterfaceV2 created: {num_layers} layers, {num_heads} heads, {num_blocks} blocks")

    def initialize_storage(self, device: str = "cuda", dtype: torch.dtype = torch.float16):
<<<<<<< HEAD
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """Allocates the physical KV tensors on the specified device."""
        shape = (self.block_table.num_blocks, self.num_layers, self.num_heads, self.block_size, self.head_size)
        self.k_cache = torch.zeros(shape, device=device, dtype=dtype)
        self.v_cache = torch.zeros(shape, device=device, dtype=dtype)
        logger.info(f"Allocated KV-Cache storage on {device} (Shape: {shape})")

    def get_layer_blocks(self, seq_id: int) -> Optional[List[int]]:
        """Returns physical block indices for a sequence."""
        return self.block_table.get_block_table(seq_id)

    def allocate_for_sequence(self, seq_id: int, num_tokens: int) -> bool:
        """
        Allocates enough blocks to store the tokens for a sequence.
        """
        num_required = (num_tokens + self.block_size - 1) // self.block_size
        blocks = self.block_table.allocate(seq_id, num_required)
        return len(blocks) > 0

<<<<<<< HEAD
<<<<<<< HEAD
    def sync_multi_gpu(self, rank: int, world_size: int) -> None:
=======
    def sync_multi_gpu(self, rank: int, world_size: int):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    def sync_multi_gpu(self, rank: int, world_size: int):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """
        Synchronizes block tables across multiple GPUs for distributed inference.
        """
        if rc and hasattr(rc, "kv_cache_sync_rust"):
            rc.kv_cache_sync_rust(rank, world_size)
        else:
            logger.debug(f"Multi-GPU sync simulated for rank {rank}")

<<<<<<< HEAD
<<<<<<< HEAD
    def purge(self) -> None:
=======
    def purge(self):
>>>>>>> e0370a77d (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
=======
    def purge(self):
>>>>>>> 125558c4f (feat: implement Swarm Evolution Meta-Learning Phase 81-85)
        """Clears all cached data and resets metadata."""
        self.block_table.free_blocks = list(range(self.block_table.num_blocks))
        self.block_table.mapping.clear()
        self.block_table.ref_counts.fill(0)
        logger.info("KVCacheInterfaceV2 purged")
