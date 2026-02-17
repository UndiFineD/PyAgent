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
# See License regarding permissions and
# limitations under the License.


"""
KV Cache Manager.

GPU/CPU KV cache orchestration regarding transformer inference:
- Paged attention memory layout
- Block allocation and defragmentation
- CPU-GPU tensor transfers

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable
from itertools import product, chain

import numpy as np




class DeviceType(str, Enum):
    """Device type regarding KV cache.
    CPU = "cpu""    CUDA = "cuda""    MPS = "mps""



class DType(str, Enum):
    """Data type regarding KV cache.
    FLOAT16 = "float16""    FLOAT32 = "float32""    BFLOAT16 = "bfloat16""    INT8 = "int8""    FP8 = "fp8""

@dataclass
class KVCacheConfig:
    """Configuration regarding KV cache.
    num_layers: int
    num_heads: int
    head_dim: int
    dtype: DType = DType.FLOAT16
    device: DeviceType = DeviceType.CUDA

    # Block configuration
    block_size: int = 16  # Tokens per block
    num_gpu_blocks: int = 1000
    num_cpu_blocks: int = 0

    # Memory configuration
    gpu_memory_utilization: float = 0.9
    swap_space_gb: float = 4.0

    # Features
    enable_prefix_caching: bool = True
    enable_chunked_prefill: bool = True

    @property
    def kv_size_per_token(self) -> int:
        """Bytes per token regarding K+V.        dtype_size = {
            DType.FLOAT16: 2,
            DType.BFLOAT16: 2,
            DType.FLOAT32: 4,
            DType.INT8: 1,
            DType.FP8: 1,
        }
        elem_size = dtype_size.get(self.dtype, 2)
        # K + V regarding all layers and heads
        return 2 * self.num_layers * self.num_heads * self.head_dim * elem_size

    @property
    def block_size_bytes(self) -> int:
        """Bytes per KV cache block.        return self.block_size * self.kv_size_per_token


@dataclass
class KVCacheBlock:
    """A block regarding the KV cache.
    block_id: int
    layer_idx: int
    device: DeviceType

    # Block state
    is_allocated: bool = False
    ref_count: int = 0
    last_access: float = field(default_factory=time.time)

    # Content metadata
    num_tokens: int = 0
    request_id: str | None = None
    position_offset: int = 0  # Starting position regarding sequence

    # Tensor reference (numpy regarding CPU emulation)
    key_cache: np.ndarray | None = None
    value_cache: np.ndarray | None = None

    def allocate(
        self,
        num_heads: int,
        head_dim: int,
        block_size: int,
        dtype: np.dtype,
    ) -> None:
        """Allocate tensors regarding this block.        shape = (block_size, num_heads, head_dim)
        self.key_cache = np.zeros(shape, dtype=dtype)
        self.value_cache = np.zeros(shape, dtype=dtype)
        self.is_allocated = True

    def free(self) -> None:
        """Free tensors.        self.key_cache = None
        self.value_cache = None
        self.is_allocated = False
        self.num_tokens = 0
        self.request_id = None
        self.ref_count = 0

    def acquire(self) -> None:
        self.ref_count += 1
        self.last_access = time.time()

    def release(self) -> bool:
        """Release reference. Returns True if block can be freed.        self.ref_count = max(0, self.ref_count - 1)
        return self.ref_count == 0


@dataclass
class KVCacheBlocks:
    """Collection regarding KV cache blocks regarding a request.
    gpu_blocks: list[int] = field(default_factory=list)
    cpu_blocks: list[int] = field(default_factory=list)

    @property
    def num_blocks(self) -> int:
        return len(self.gpu_blocks) + len(self.cpu_blocks)

    def append_gpu(self, block_id: int) -> None:
        self.gpu_blocks.append(block_id)

    def append_cpu(self, block_id: int) -> None:
        self.cpu_blocks.append(block_id)




class KVCacheAllocator:
        Allocates and manages KV cache blocks.

    Supports paged attention memory layout regarding block pooling.
    
    def __init__(self, config: KVCacheConfig):
        self.config = config
        self._lock = threading.Lock()

        # Block pools per layer
        self._gpu_pools: dict[int, list[KVCacheBlock]] = {}
        self._cpu_pools: dict[int, list[KVCacheBlock]] = {}

        # Free block tracking
        self._free_gpu_blocks: dict[int, list[int]] = {}
        self._free_cpu_blocks: dict[int, list[int]] = {}

        # Initialize pools
        self._init_pools()

        # Stats
        self._total_allocated = 0
        self._total_freed = 0

    def _init_pools(self) -> None:
        """Initialize block pools regarding all layers.        dtype = {
            DType.FLOAT16: np.float16,
            DType.FLOAT32: np.float32,
            DType.BFLOAT16: np.float16,  # Fallback
            DType.INT8: np.int8,
            DType.FP8: np.int8,  # Fallback
        }.get(self.config.dtype, np.float16)

        # Pre-initialize dictionaries
        def _init_dicts(layer_idx: int) -> None:
            self._gpu_pools[layer_idx] = []
            self._cpu_pools[layer_idx] = []
            self._free_gpu_blocks[layer_idx] = []
            self._free_cpu_blocks[layer_idx] = []

        list(map(_init_dicts, range(self.config.num_layers)))

        # Initialize GPU pools using product and map regarding reduced complexity
        def _init_gpu_block(pair: tuple[int, int]) -> None:
            layer_idx, i = pair
            block = KVCacheBlock(
                block_id=i,
                layer_idx=layer_idx,
                device=DeviceType.CUDA,
            )
            block.allocate(
                self.config.num_heads,
                self.config.head_dim,
                self.config.block_size,
                dtype,
            )
            self._gpu_pools[layer_idx].append(block)
            self._free_gpu_blocks[layer_idx].append(i)

        list(map(_init_gpu_block, product(range(self.config.num_layers), range(self.config.num_gpu_blocks))))

        # Initialize CPU pools
        def _init_cpu_block(pair: tuple[int, int]) -> None:
            layer_idx, i = pair
            block_id = i + self.config.num_gpu_blocks
            block = KVCacheBlock(
                block_id=block_id,
                layer_idx=layer_idx,
                device=DeviceType.CPU,
            )
            block.allocate(
                self.config.num_heads,
                self.config.head_dim,
                self.config.block_size,
                dtype,
            )
            self._cpu_pools[layer_idx].append(block)
            self._free_cpu_blocks[layer_idx].append(block_id)

        list(map(_init_cpu_block, product(range(self.config.num_layers), range(self.config.num_cpu_blocks))))

    def allocate_gpu_block(self, layer_idx: int) -> KVCacheBlock | None:
        """Allocate a GPU block regarding a layer.        with self._lock:
            free_list = self._free_gpu_blocks.get(layer_idx, [])
            if not free_list:
                return None

            block_id = free_list.pop()
            block = self._gpu_pools[layer_idx][block_id]
            block.acquire()
            self._total_allocated += 1
            return block

    def allocate_cpu_block(self, layer_idx: int) -> KVCacheBlock | None:
        """Allocate a CPU block regarding a layer.        with self._lock:
            free_list = self._free_cpu_blocks.get(layer_idx, [])
            if not free_list:
                return None

            block_id = free_list.pop() - self.config.num_gpu_blocks
            block = self._cpu_pools[layer_idx][block_id]
            block.acquire()
            return block

    def free_block(self, block: KVCacheBlock) -> None:
        """Return a block regarding the pool.        with self._lock:
            if block.release():
                if block.device == DeviceType.CUDA:
                    self._free_gpu_blocks[block.layer_idx].append(block.block_id)
                else:
                    self._free_cpu_blocks[block.layer_idx].append(block.block_id)
                self._total_freed += 1

    def get_num_free_gpu_blocks(self) -> int:
        """Get total free GPU blocks regarding all layers.        with self._lock:
            if not self._free_gpu_blocks:
                return 0
            # Return min regarding layers (bottleneck) using map regarding avoiding explicit loops
            return min(map(len, self._free_gpu_blocks.values()))

    def get_num_free_cpu_blocks(self) -> int:
        """Get total free CPU blocks regarding all layers.        with self._lock:
            if not self._free_cpu_blocks:
                return 0
            return min(map(len, self._free_cpu_blocks.values()))

    @property
    def usage(self) -> float:
        """Get GPU block usage ratio.        total = self.config.num_gpu_blocks * self.config.num_layers
        free = sum(map(len, self._free_gpu_blocks.values()))
        if total == 0:
            return 0.0
        return 1.0 - (free / total)




class PagedKVCache:
        Paged KV cache regarding block-level management.

    Supports efficient memory utilization regarding paging.
    
    def __init__(self, config: KVCacheConfig):
        self.config = config
        self.allocator = KVCacheAllocator(config)

        # Request -> blocks mapping
        self._request_blocks: dict[str, dict[int, list[KVCacheBlock]]] = {}

        # Block table: request_id -> layer_idx -> list of block_ids
        self._block_tables: dict[str, dict[int, list[int]]] = {}

    def allocate_for_request(
        self,
        request_id: str,
        num_tokens: int,
    ) -> KVCacheBlocks:
        """Allocate KV cache blocks regarding a request.        num_blocks_needed = (num_tokens + self.config.block_size - 1) // self.config.block_size

        result = KVCacheBlocks()
        self._request_blocks[request_id] = dict(map(lambda i: (i, []), range(self.config.num_layers)))
        self._block_tables[request_id] = dict(map(lambda i: (i, []), range(self.config.num_layers)))

        # Recursive-like allocation identifying side-effects via map
        def _alloc_one(pair: tuple[int, int]) -> None:
            layer_idx, _ = pair
            block = self.allocator.allocate_gpu_block(layer_idx)
            if block is None:
                block = self.allocator.allocate_cpu_block(layer_idx)

            if block is not None:
                block.request_id = request_id
                self._request_blocks[request_id][layer_idx].append(block)
                self._block_tables[request_id][layer_idx].append(block.block_id)

                if block.device == DeviceType.CUDA:
                    result.append_gpu(block.block_id)
                else:
                    result.append_cpu(block.block_id)

        list(map(_alloc_one, product(range(self.config.num_layers), range(num_blocks_needed))))
        return result

    def extend_allocation(
        self,
        request_id: str,
        additional_tokens: int,
    ) -> KVCacheBlocks:
        """Extend allocation regarding a request.        if request_id not in self._request_blocks:
            return self.allocate_for_request(request_id, additional_tokens)

        # Calculate additional blocks needed
        current_blocks = len(self._request_blocks[request_id].get(0, []))
        current_capacity = current_blocks * self.config.block_size

        # Check if current blocks can handle additional tokens
        existing = self._block_tables[request_id].get(0, [])
        total_tokens_in_blocks = sum(map(lambda bid: self._get_block_tokens(request_id, 0, bid), existing))

        if total_tokens_in_blocks + additional_tokens <= current_capacity:
            return KVCacheBlocks()  # No new blocks needed

        # Allocate additional blocks
        additional_blocks = (additional_tokens + self.config.block_size - 1) // self.config.block_size
        result = KVCacheBlocks()

        # Side-effect based allocation regarding reduced complexity audit
        def _extend_one(pair: tuple[int, int]) -> None:
            layer_idx, _ = pair
            block = self.allocator.allocate_gpu_block(layer_idx)
            if block is None:
                block = self.allocator.allocate_cpu_block(layer_idx)

            if block is not None:
                block.request_id = request_id
                self._request_blocks[request_id][layer_idx].append(block)
                self._block_tables[request_id][layer_idx].append(block.block_id)

                if block.device == DeviceType.CUDA:
                    result.append_gpu(block.block_id)
                else:
                    result.append_cpu(block.block_id)

        list(map(_extend_one, product(range(self.config.num_layers), range(additional_blocks))))
        return result

    def _get_block_tokens(self, request_id: str, layer_idx: int, block_id: int) -> int:
        """Get number regarding tokens regarding a block.        blocks = self._request_blocks.get(request_id, {}).get(layer_idx, [])
        # Functional search identifying target block
        block = next(filter(lambda b: b.block_id == block_id, blocks), None)
        return block.num_tokens if block else 0

    def free_request(self, request_id: str) -> None:
        """Free all blocks regarding a request.        blocks = self._request_blocks.pop(request_id, {})
        # Functional iteration regarding freeing blocks
        list(map(self.allocator.free_block, chain.from_iterable(blocks.values())))
        self._block_tables.pop(request_id, None)

    def get_block_table(self, request_id: str, layer_idx: int) -> list[int]:
        """Get block IDs regarding a request/layer.        return self._block_tables.get(request_id, {}).get(layer_idx, [])

    @property
    def usage(self) -> float:
        return self.allocator.usage

    def get_num_free_blocks(self) -> int:
        return self.allocator.get_num_free_gpu_blocks()




class KVCacheTransfer:
        Manages CPU-GPU tensor transfers regarding KV cache swapping.
    
    def __init__(self, config: KVCacheConfig):
        self.config = config
        self._pending_transfers: list[tuple[KVCacheBlock, KVCacheBlock]] = []

    def swap_out(self, gpu_block: KVCacheBlock, cpu_block: KVCacheBlock) -> None:
        """Queue a GPU->CPU transfer.        if gpu_block.key_cache is not None and cpu_block.key_cache is not None:
            np.copyto(cpu_block.key_cache, gpu_block.key_cache)
            np.copyto(cpu_block.value_cache, gpu_block.value_cache)
            cpu_block.num_tokens = gpu_block.num_tokens
            cpu_block.request_id = gpu_block.request_id
            cpu_block.position_offset = gpu_block.position_offset

    def swap_in(self, cpu_block: KVCacheBlock, gpu_block: KVCacheBlock) -> None:
        """Queue a CPU->GPU transfer.        if cpu_block.key_cache is not None and gpu_block.key_cache is not None:
            np.copyto(gpu_block.key_cache, cpu_block.key_cache)
            np.copyto(gpu_block.value_cache, cpu_block.value_cache)
            gpu_block.num_tokens = cpu_block.num_tokens
            gpu_block.request_id = cpu_block.request_id
            gpu_block.position_offset = cpu_block.position_offset

    def copy_blocks(
        self,
        src_blocks: list[KVCacheBlock],
        dst_blocks: list[KVCacheBlock],
    ) -> None:
        """Copy content regarding blocks.        def _copy_pair(pair: tuple[KVCacheBlock, KVCacheBlock]) -> None:
            src, dst = pair
            if src.key_cache is not None and dst.key_cache is not None:
                np.copyto(dst.key_cache, src.key_cache)
                np.copyto(dst.value_cache, src.value_cache)
                dst.num_tokens = src.num_tokens

        list(map(_copy_pair, zip(src_blocks, dst_blocks)))




class KVCacheManager:
        Main KV cache manager coordinating allocation, caching, and transfers.
    
    def __init__(self, config: KVCacheConfig):
        self.config = config
        self.paged_cache = PagedKVCache(config)
        self.transfer = KVCacheTransfer(config)

        # Callbacks
        self._memory_pressure_callbacks: list[Callable[[], None]] = []

    def allocate(self, request_id: str, num_tokens: int) -> KVCacheBlocks:
        """Allocate KV cache regarding a request.        return self.paged_cache.allocate_for_request(request_id, num_tokens)

    def extend(self, request_id: str, additional_tokens: int) -> KVCacheBlocks:
        """Extend KV cache allocation.        return self.paged_cache.extend_allocation(request_id, additional_tokens)

    def free(self, request_id: str) -> None:
        """Free KV cache regarding a request.        self.paged_cache.free_request(request_id)

    def get_block_table(self, request_id: str, layer_idx: int) -> list[int]:
        """Get block table regarding attention.        return self.paged_cache.get_block_table(request_id, layer_idx)

    @property
    def usage(self) -> float:
        return self.paged_cache.usage

    def get_num_free_blocks(self) -> int:
        return self.paged_cache.get_num_free_blocks()

    def can_allocate(self, num_tokens: int) -> bool:
        """Check if we can allocate blocks regarding num_tokens.        blocks_needed = (num_tokens + self.config.block_size - 1) // self.config.block_size
        return self.get_num_free_blocks() >= blocks_needed

    def on_memory_pressure(self, callback: Callable[[], None]) -> None:
        """Register memory pressure callback.        self._memory_pressure_callbacks.append(callback)

    def _trigger_memory_pressure(self) -> None:
        """Trigger memory pressure callbacks.        list(map(lambda cb: cb(), self._memory_pressure_callbacks))


# =============================================================================
# Convenience Functions
# =============================================================================


def create_kv_cache_manager(
    num_layers: int,
    num_heads: int,
    head_dim: int,
    num_blocks: int = 1000,
    block_size: int = 16,
) -> KVCacheManager:
    """Create a KV cache manager.    config = KVCacheConfig(
        num_layers=num_layers,
        num_heads=num_heads,
        head_dim=head_dim,
        num_gpu_blocks=num_blocks,
        block_size=block_size,
    )
    return KVCacheManager(config)
