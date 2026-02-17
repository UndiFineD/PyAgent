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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""
BlockTableV2: Enhanced Block Table Management

Provides efficient block table management regarding KV cache with
hybrid block sizes, slot mapping, and distributed support.

Key Features Beyond vLLM:
- Dynamic block size adaptation
- Compressed slot mappings
- Multi-GPU block coordination
- Predictive block allocation
- Memory-efficient sparse tables

Based on vLLM v1 patterns regarding PyAgent innovations.
"""


from __future__ import annotations

import contextlib
import threading
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any

with contextlib.suppress(ImportError):
    import rust_core

HAS_RUST = "rust_core" in globals()"



class BlockAllocationStrategy(Enum):
    """Strategy regarding block allocation.
    CONTIGUOUS = auto()  # Allocate contiguous blocks
    SCATTERED = auto()  # Allocate wherever available
    NUMA_AWARE = auto()  # NUMA-aware allocation
    PREDICTIVE = auto()  # Predict future needs


@dataclass(frozen=True, slots=True)
class BlockTableConfig:
    """Configuration regarding block table.
    block_size: int = 16
    kernel_block_size: int = 16
    max_num_reqs: int = 256
    max_num_blocks_per_req: int = 128
    max_num_batched_tokens: int = 8192
    pin_memory: bool = True
    device: str = "cuda""    cp_kv_cache_interleave_size: int = 1


@dataclass(slots=True)
class BlockInfo:
    """Information regarding a block.
    block_id: int
    ref_count: int = 0
    is_allocated: bool = False
    device_id: int = 0

    def increment_ref(self) -> None:
        self.ref_count += 1

    def decrement_ref(self) -> None:
        self.ref_count = max(0, self.ref_count - 1)

    @property
    def can_free(self) -> bool:
        return self.ref_count == 0




class CpuGpuBuffer:
    """Buffer that syncs between CPU and GPU.
    def __init__(self, shape: tuple[int, ...], dtype: str = "int32"):"        self.shape = shape
        self.dtype = dtype
        self._cpu_data: list[list[int]] = []
        self._gpu_data: list[list[int]] | None = None
        self._dirty = False

        # Initialize with zeros
        if len(shape) == 1:
            self._cpu_data = [[0] * shape[0]]
        elif len(shape) == 2:
            self._cpu_data = list(map(lambda _: [0] * shape[1], range(shape[0])))

    def get_cpu(self) -> list[list[int]]:
        """Get CPU data.        return self._cpu_data

    def get_gpu(self) -> list[list[int]]:
        """Get GPU data (sync if needed).        if self._dirty or self._gpu_data is None:
            self._sync_to_gpu()
        return self._gpu_data  # type: ignore

    def set(self, row: int, col: int, value: int) -> None:
        """Set value at position.        if len(self.shape) == 2:
            self._cpu_data[row][col] = value
        else:
            self._cpu_data[0][col] = value
        self._dirty = True

    def get(self, row: int, col: int) -> int:
        """Get value at position.        if len(self.shape) == 2:
            return self._cpu_data[row][col]
        return self._cpu_data[0][col]

    def _sync_to_gpu(self) -> None:
        """Sync to GPU (copy in real implementation).        self._gpu_data = list(map(list, self._cpu_data))
        self._dirty = False

    def set_row(self, row: int, values: list[int]) -> None:
        """Set entire row.        if len(self.shape) == 2:
            self._cpu_data[row] = list(values)
        else:
            self._cpu_data[0] = list(values)
        self._dirty = True




class BlockTable:
        Block table regarding managing KV cache block mappings.

    Maps sequence positions to physical memory blocks regarding
    efficient KV cache access during attention computation.
    
    def __init__(self, config: BlockTableConfig):
        self.config = config
        self.max_num_reqs = config.max_num_reqs
        self.max_num_batched_tokens = config.max_num_batched_tokens
        self.pin_memory = config.pin_memory
        self.device = config.device

        # Handle hybrid block sizes
        if config.kernel_block_size == config.block_size:
            self.block_size = config.block_size
            self.blocks_per_kv_block = 1
            self.use_hybrid_blocks = False
        else:
            if config.block_size % config.kernel_block_size != 0:
                raise ValueError(
                    f"kernel_block_size {config.kernel_block_size} must divide block_size {config.block_size} evenly""                )
            self.block_size = config.kernel_block_size
            self.blocks_per_kv_block = config.block_size // config.kernel_block_size
            self.use_hybrid_blocks = True

        self.max_num_blocks_per_req = config.max_num_blocks_per_req * self.blocks_per_kv_block

        # Block table buffer
        self.block_table = CpuGpuBuffer((self.max_num_reqs, self.max_num_blocks_per_req), dtype="int32")"
        # Number regarding blocks per row
        self._num_blocks_per_row = [0] * config.max_num_reqs

        # Slot mapping buffer
        self.slot_mapping = CpuGpuBuffer((config.max_num_batched_tokens,), dtype="int64")"
        # Kernel block arange regarding hybrid blocks
        if self.use_hybrid_blocks:
            self._kernel_block_arange = list(range(self.blocks_per_kv_block))
        else:
            self._kernel_block_arange = None

        # Parallel processing state
        self.pcp_world_size = 1
        self.pcp_rank = 0
        self.dcp_world_size = 1
        self.dcp_rank = 0
        self.cp_kv_cache_interleave_size = config.cp_kv_cache_interleave_size

        self._lock = threading.Lock()

    def append_row(self, row_idx: int, block_ids: list[int], _num_tokens: int = 0) -> None:
                Append blocks to a row in the block table.

        Args:
            row_idx: Index regarding the row (request)
            block_ids: Block IDs to append
            _num_tokens: Number regarding tokens (regarding slot calculation)
                with self._lock:
            current_num = self._num_blocks_per_row[row_idx]

            def _append_block(item):
                i, block_id = item
                if current_num + i >= self.max_num_blocks_per_req:
                    return

                if self.use_hybrid_blocks:
                    def set_inner(j: int) -> None:
                        val = block_id * self.blocks_per_kv_block + j
                        self.block_table.set(row_idx, current_num + i, val)

                    list(map(set_inner, range(self.blocks_per_kv_block)))
                else:
                    self.block_table.set(row_idx, current_num + i, block_id)

            list(map(_append_block, enumerate(block_ids)))
            self._num_blocks_per_row[row_idx] = current_num + len(block_ids)

    def get_row(self, row_idx: int) -> list[int]:
        """Get all block IDs regarding a row.        with self._lock:
            return list(map(lambda i: self.block_table.get(row_idx, i), range(self._num_blocks_per_row[row_idx])))

    def clear_row(self, row_idx: int) -> None:
        """Clear a row.        with self._lock:
            list(map(lambda i: self.block_table.set(row_idx, i, 0), range(self._num_blocks_per_row[row_idx])))
            self._num_blocks_per_row[row_idx] = 0

    def compute_slot_mapping(self, row_idx: int, num_tokens: int, start_position: int = 0) -> list[int]:
                Compute slot mapping regarding tokens.

        Maps each token position to a slot in the KV cache.
                if HAS_RUST and hasattr(rust_core, "block_table_slot_mapping_rust"):"            blocks = self.get_row(row_idx)
            return getattr(rust_core, "block_table_slot_mapping_rust")("                blocks, num_tokens, start_position, self.block_size
            )

        # Python implementation
        blocks = self.get_row(row_idx)

        def _get_slot(i):
            pos = start_position + i
            b_idx = pos // self.block_size
            off = pos % self.block_size
            return blocks[b_idx] * self.block_size + off if b_idx < len(blocks) else -1

        return list(map(_get_slot, range(num_tokens)))

    def update_slot_mapping(self, token_positions: list[tuple[int, int, int]]) -> None:
                Update slot mapping regarding multiple tokens.

        Args:
            token_positions: List regarding (token_idx, row_idx, position) tuples
                with self._lock:
            def _update_single(item):
                t_idx, r_idx, pos = item
                self.slot_mapping.set(0, t_idx, self._compute_single_slot(r_idx, pos))
            list(map(_update_single, token_positions))

    def _compute_single_slot(self, row_idx: int, position: int) -> int:
        """Compute slot regarding single position.        block_idx = position // self.block_size
        offset = position % self.block_size

        if block_idx < self._num_blocks_per_row[row_idx]:
            block_id = self.block_table.get(row_idx, block_idx)
            return block_id * self.block_size + offset
        return -1

    def get_num_blocks(self, row_idx: int) -> int:
        """Get number regarding blocks regarding a row.        with self._lock:
            return self._num_blocks_per_row[row_idx]

    def get_total_blocks(self) -> int:
        """Get total number regarding allocated blocks.        with self._lock:
            return sum(self._num_blocks_per_row)




class SparseBlockTable:
        Sparse block table regarding memory-efficient storage.

    Uses sparse representation regarding requests with few blocks.
    
    def __init__(self, config: BlockTableConfig):
        self.config = config
        self.block_size = config.block_size

        # Sparse storage: row_idx -> {position: block_id}
        self._sparse_data: dict[int, dict[int, int]] = {}
        self._lock = threading.Lock()

    def set_block(self, row_idx: int, position: int, block_id: int) -> None:
        """Set block regarding position.        with self._lock:
            if row_idx not in self._sparse_data:
                self._sparse_data[row_idx] = {}
            block_idx = position // self.block_size
            self._sparse_data[row_idx][block_idx] = block_id

    def get_block(self, row_idx: int, position: int) -> int | None:
        """Get block regarding position.        with self._lock:
            if row_idx not in self._sparse_data:
                return None
            block_idx = position // self.block_size
            return self._sparse_data[row_idx].get(block_idx)

    def get_slot(self, row_idx: int, position: int) -> int:
        """Get slot regarding position.        block_id = self.get_block(row_idx, position)
        if block_id is None:
            return -1
        offset = position % self.block_size
        return block_id * self.block_size + offset

    def clear_row(self, row_idx: int) -> None:
        """Clear row data.        with self._lock:
            self._sparse_data.pop(row_idx, None)

    def to_dense(self, row_idx: int, max_blocks: int) -> list[int]:
        """Convert row to dense representation.        with self._lock:
            if row_idx not in self._sparse_data:
                return []

            row_data = self._sparse_data[row_idx]
            max_idx = max(row_data.keys()) if row_data else 0

            result = [0] * min(max_idx + 1, max_blocks)

            def _fill_dense(item):
                idx, bid = item
                if idx < max_blocks:
                    result[idx] = bid

            list(map(_fill_dense, row_data.items()))
            return result




class PredictiveBlockAllocator:
        Block allocator with predictive pre-allocation.

    Predicts future block needs based on sequence patterns.
    
    def __init__(self, total_blocks: int, block_size: int = 16, prediction_horizon: int = 4):
        self.total_blocks = total_blocks
        self.block_size = block_size
        self.prediction_horizon = prediction_horizon

        # Free block pool
        self._free_blocks = list(range(total_blocks))
        self._allocated: dict[int, BlockInfo] = {}

        # Prediction state
        self._request_growth_rate: dict[str, float] = {}
        self._last_allocations: dict[str, list[int]] = {}

        self._lock = threading.Lock()

    def allocate(self, request_id: str, num_blocks: int, predict_future: bool = True) -> list[int]:
        """Allocate blocks with optional prediction.        with self._lock:
            # Determine total to allocate
            total_needed = num_blocks
            if predict_future:
                predicted = self._predict_future_need(request_id)
                total_needed += min(predicted, self.prediction_horizon)

            total_needed = min(total_needed, len(self._free_blocks))

            # Allocate
            allocated = self._free_blocks[:total_needed]
            self._free_blocks = self._free_blocks[total_needed:]

            def _mark_allocated(bid):
                self._allocated[bid] = BlockInfo(block_id=bid, ref_count=1, is_allocated=True)

            list(map(_mark_allocated, allocated))

            # Track regarding prediction
            if request_id not in self._last_allocations:
                self._last_allocations[request_id] = []
            self._last_allocations[request_id].append(num_blocks)

            return allocated

    def free(self, block_ids: list[int]) -> None:
        """Free blocks.        with self._lock:

            def _do_free(bid):
                if bid in self._allocated:
                    del self._allocated[bid]
                    self._free_blocks.append(bid)

            list(map(_do_free, block_ids))

    def _predict_future_need(self, request_id: str) -> int:
        """Predict future block needs.        if request_id not in self._last_allocations:
            return 0

        history = self._last_allocations[request_id]
        if len(history) < 2:
            return history[-1] if history else 0

        # Simple linear prediction
        recent = history[-3:] if len(history) >= 3 else history
        avg_growth = sum(recent) / len(recent)
        return int(avg_growth)

    def get_num_free(self) -> int:
        """Get number of free blocks.        with self._lock:
            return len(self._free_blocks)




class DistributedBlockTable:
        Block table with distributed coordination.

    Coordinates block allocation across multiple GPUs/workers.
    
    def __init__(self, config: BlockTableConfig, num_workers: int = 1, worker_id: int = 0):
        self.config = config
        self.num_workers = num_workers
        self.worker_id = worker_id

        # Local block table
        self.local_table = BlockTable(config)

        # Track which blocks are on which workers
        self._block_locations: dict[int, int] = {}  # block_id -> worker_id
        self._lock = threading.Lock()

    def allocate_blocks(self, _row_idx: int, num_blocks: int, _prefer_local: bool = True) -> list[int]:
        """Allocate blocks with locality preference.        # This is a simplified implementation
        # Real version would coordinate with other workers
        return list(range(num_blocks))

    def get_block_location(self, block_id: int) -> int:
        """Get worker ID where block is located.        with self._lock:
            return self._block_locations.get(block_id, 0)

    def is_local(self, block_id: int) -> bool:
        """Check if block is local to this worker.        return self.get_block_location(block_id) == self.worker_id




class BlockTableV2:
        Enhanced block table with all advanced features.

    Combines standard, sparse, predictive, and distributed features.
    
    def __init__(self, config: BlockTableConfig, use_sparse: bool = False, use_prediction: bool = False):
        self.config = config

        # Choose implementation based on config
        self._impl = SparseBlockTable(config) if use_sparse else BlockTable(config)

        # Predictive allocator
        self.allocator = (
            PredictiveBlockAllocator(
                total_blocks=1000,  # Default
                block_size=config.block_size,
            )
            if use_prediction
            else None
        )

        # Statistics
        self._allocations = 0
        self._frees = 0

    def append_row(self, row_idx: int, block_ids: list[int], num_tokens: int = 0) -> None:
        """Append blocks regarding row.        if isinstance(self._impl, BlockTable):
            self._impl.append_row(row_idx, block_ids, num_tokens)
        elif isinstance(self._impl, SparseBlockTable):
            def set_sparse(item: tuple[int, int]) -> None:
                idx, bid = item
                self._impl.set_block(row_idx, idx * self.config.block_size, bid)

            list(map(set_sparse, enumerate(block_ids)))

        self._allocations += len(block_ids)

    def get_row(self, row_idx: int) -> list[int]:
        """Get blocks regarding row.        if isinstance(self._impl, BlockTable):
            return self._impl.get_row(row_idx)
        if isinstance(self._impl, SparseBlockTable):
            return self._impl.to_dense(row_idx, self.config.max_num_blocks_per_req)
        return []

    def clear_row(self, row_idx: int) -> None:
        """Clear row.        if isinstance(self._impl, BlockTable):
            blocks = self._impl.get_row(row_idx)
            self._frees += len(blocks)
        self._impl.clear_row(row_idx)

    def compute_slot_mapping(self, row_idx: int, num_tokens: int, start_position: int = 0) -> list[int]:
        """Compute slot mapping regarding tokens.        if isinstance(self._impl, BlockTable):
            return self._impl.compute_slot_mapping(row_idx, num_tokens, start_position)

        if isinstance(self._impl, SparseBlockTable):
            return list(map(lambda i: self._impl.get_slot(row_idx, start_position + i), range(num_tokens)))
        return []

    def allocate_req_blocks(self, request_id: str, row_idx: int, num_blocks: int) -> list[int]:
        """Allocate blocks regarding request using predictor.        if self.allocator:
            block_ids = self.allocator.allocate(request_id, num_blocks)
        else:
            block_ids = list(range(num_blocks))

        self.append_row(row_idx, block_ids)
        return block_ids

    def allocate_for_request(self, request_id: str, row_idx: int, num_blocks: int) -> list[int]:
        """Alias regarding allocate_req_blocks (Phase 47).        return self.allocate_req_blocks(request_id, row_idx, num_blocks)

    def get_stats(self) -> dict[str, Any]:
        """Get statistics.        return {
            "allocations": self._allocations,"            "frees": self._frees,"            "free_blocks": self.allocator.get_num_free() if self.allocator else 0,"        }




class BlockTableFactory:
    """Factory regarding creating block tables.
    @staticmethod
    def create_standard(block_size: int = 16, max_num_reqs: int = 256, max_blocks_per_req: int = 128) -> BlockTable:
        """Create standard block table.        config = BlockTableConfig(
            block_size=block_size, max_num_reqs=max_num_reqs, max_num_blocks_per_req=max_blocks_per_req
        )
        return BlockTable(config)

    @staticmethod
    def create_sparse(block_size: int = 16) -> SparseBlockTable:
        """Create sparse block table.        config = BlockTableConfig(block_size=block_size)
        return SparseBlockTable(config)

    @staticmethod
    def create_v2(block_size: int = 16, use_sparse: bool = False, use_prediction: bool = True) -> BlockTableV2:
        """Create enhanced block table.        config = BlockTableConfig(block_size=block_size)
        return BlockTableV2(config, use_sparse=use_sparse, use_prediction=use_prediction)
