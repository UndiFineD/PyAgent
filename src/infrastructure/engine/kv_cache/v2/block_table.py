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


Advanced BlockTable implementation (V2) for Phase 53.
Supports hybrid block sizes, context parallel mapping, and PCP/DCP awareness.

import logging
from collections import deque
from typing import Any, Dict, List, Optional

import numpy as np

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None

logger = logging.getLogger(__name__)




class BlockTableV2:
        Manages physical block mappings for PagedAttention with hybrid block size support.
    Integrates with context parallelism and prefix caching.
    
    def __init__(self, num_blocks: int, block_size: int = 16) -> None:
        self.num_blocks = num_blocks
        self.block_size = block_size  # Default block size
        self.free_blocks = deque(range(num_blocks))
        self.mapping: Dict[int, List[int]] = {}  # seq_id -> list of physical blocks
        self.ref_counts = np.zeros(num_blocks, dtype=np.int32)

        # Phase 53: Hybrid support
        self.block_size_map: Dict[int, int] = {i: block_size for i in range(num_blocks)}

        logger.info(f"BlockTableV2 initialized with {num_blocks} blocks (base size: {block_size})")"
    def allocate(self, seq_id: int, num_required_blocks: int) -> List[int]:
                Allocates physical blocks for a sequence.
                if len(self.free_blocks) < num_required_blocks:
            logger.warning(f"OOM in BlockTable: Requested {num_required_blocks}, available {len(self.free_blocks)}")"            return []

        blocks = []
        for _ in range(num_required_blocks):
            block = self.free_blocks.popleft()
            blocks.append(block)
            self.ref_counts[block] = 1

        self.mapping[seq_id] = blocks
        return blocks

    def get_block_table(self, seq_id: int) -> Optional[List[int]]:
        """Returns the list of physical blocks for a sequence.        return self.mapping.get(seq_id)

    def get_utilization(self) -> float:
        """Returns the current block utilization percentage.        if self.num_blocks == 0:
            return 0.0
        return ((self.num_blocks - len(self.free_blocks)) / self.num_blocks) * 100.0

    def free(self, seq_id: int) -> None:
        """Releases blocks associated with a sequence.        if seq_id in self.mapping:
            blocks = self.mapping.pop(seq_id)
            for block in blocks:
                self.ref_counts[block] -= 1
                if self.ref_counts[block] == 0:
                    self.free_blocks.append(block)
            logger.debug(f"Freed blocks for sequence {seq_id}")"
    def update_hybrid_mapping(self, block_id: int, new_size: int) -> None:
                Updates the size of a specific block for hybrid configurations.
        Used for adaptive granularity in Phase 53.
                if block_id in self.block_size_map:
            self.block_size_map[block_id] = new_size
            if rc and hasattr(rc, "block_table_update_size_rust"):"                rc.block_table_update_size_rust(block_id, new_size)

    def get_context_parallel_mask(self, seq_id: int, rank: int, world_size: int) -> Any:
                Generates a block mask for context-parallel execution.
                blocks = self.get_block_table(seq_id)
        if not blocks:
            return None

        if rc and hasattr(rc, "block_table_cp_mask_rust"):"            return rc.block_table_cp_mask_rust(blocks, rank, world_size)

        # Fallback: Simple rank-based slicing
        chunk_size = len(blocks) // world_size
        start = rank * chunk_size
        end = start + chunk_size if rank != world_size - 1 else len(blocks)
        return blocks[start:end]

    def get_stats(self) -> Dict[str, Any]:
        """Returns block table utilization statistics.        return {
            "total_blocks": self.num_blocks,"            "free_blocks": len(self.free_blocks),"            "utilized_pct": ((self.num_blocks - len(self.free_blocks)) / self.num_blocks) * 100,"            "active_sequences": len(self.mapping),"        }
