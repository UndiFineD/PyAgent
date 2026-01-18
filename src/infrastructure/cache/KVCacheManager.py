"""
KV Cache Manager.

GPU/CPU KV cache orchestration for transformer inference:
- Paged attention memory layout
- Block allocation and defragmentation
- CPU-GPU tensor transfers

Inspired by vLLM's v1/core/kv_cache_manager.py architecture.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Generic, Protocol, TypeVar

import numpy as np


class DeviceType(str, Enum):
    """Device type for KV cache."""
    CPU = "cpu"
    CUDA = "cuda"
    MPS = "mps"


class DType(str, Enum):
    """Data type for KV cache."""
    FLOAT16 = "float16"
    FLOAT32 = "float32"
    BFLOAT16 = "bfloat16"
    INT8 = "int8"
    FP8 = "fp8"


@dataclass
class KVCacheConfig:
    """Configuration for KV cache."""
    
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
        """Bytes per token for K+V."""
        dtype_size = {
            DType.FLOAT16: 2,
            DType.BFLOAT16: 2,
            DType.FLOAT32: 4,
            DType.INT8: 1,
            DType.FP8: 1,
        }
        elem_size = dtype_size.get(self.dtype, 2)
        # K + V for all layers and heads
        return 2 * self.num_layers * self.num_heads * self.head_dim * elem_size
    
    @property
    def block_size_bytes(self) -> int:
        """Bytes per KV cache block."""
        return self.block_size * self.kv_size_per_token


@dataclass
class KVCacheBlock:
    """A block in the KV cache."""
    
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
    position_offset: int = 0  # Starting position in sequence
    
    # Tensor reference (numpy for CPU emulation)
    key_cache: np.ndarray | None = None
    value_cache: np.ndarray | None = None
    
    def allocate(
        self,
        num_heads: int,
        head_dim: int,
        block_size: int,
        dtype: np.dtype,
    ) -> None:
        """Allocate tensors for this block."""
        shape = (block_size, num_heads, head_dim)
        self.key_cache = np.zeros(shape, dtype=dtype)
        self.value_cache = np.zeros(shape, dtype=dtype)
        self.is_allocated = True
    
    def free(self) -> None:
        """Free tensors."""
        self.key_cache = None
        self.value_cache = None
        self.is_allocated = False
        self.num_tokens = 0
        self.request_id = None
        self.ref_count = 0
    
    def acquire(self) -> None:
        self.ref_count += 1
        self.last_access = time.time()
    
    def release(self) -> bool:
        """Release reference. Returns True if block can be freed."""
        self.ref_count = max(0, self.ref_count - 1)
        return self.ref_count == 0


@dataclass
class KVCacheBlocks:
    """Collection of KV cache blocks for a request."""
    
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
    """
    Allocates and manages KV cache blocks.
    
    Supports paged attention memory layout with block pooling.
    """
    
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
        """Initialize block pools for all layers."""
        dtype = {
            DType.FLOAT16: np.float16,
            DType.FLOAT32: np.float32,
            DType.BFLOAT16: np.float16,  # Fallback
            DType.INT8: np.int8,
            DType.FP8: np.int8,  # Fallback
        }.get(self.config.dtype, np.float16)
        
        for layer_idx in range(self.config.num_layers):
            # GPU blocks
            gpu_blocks: list[KVCacheBlock] = []
            free_gpu: list[int] = []
            
            for i in range(self.config.num_gpu_blocks):
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
                gpu_blocks.append(block)
                free_gpu.append(i)
            
            self._gpu_pools[layer_idx] = gpu_blocks
            self._free_gpu_blocks[layer_idx] = free_gpu
            
            # CPU blocks
            cpu_blocks: list[KVCacheBlock] = []
            free_cpu: list[int] = []
            
            for i in range(self.config.num_cpu_blocks):
                block = KVCacheBlock(
                    block_id=i + self.config.num_gpu_blocks,
                    layer_idx=layer_idx,
                    device=DeviceType.CPU,
                )
                block.allocate(
                    self.config.num_heads,
                    self.config.head_dim,
                    self.config.block_size,
                    dtype,
                )
                cpu_blocks.append(block)
                free_cpu.append(block.block_id)
            
            self._cpu_pools[layer_idx] = cpu_blocks
            self._free_cpu_blocks[layer_idx] = free_cpu
    
    def allocate_gpu_block(self, layer_idx: int) -> KVCacheBlock | None:
        """Allocate a GPU block for a layer."""
        with self._lock:
            free_list = self._free_gpu_blocks.get(layer_idx, [])
            if not free_list:
                return None
            
            block_id = free_list.pop()
            block = self._gpu_pools[layer_idx][block_id]
            block.acquire()
            self._total_allocated += 1
            return block
    
    def allocate_cpu_block(self, layer_idx: int) -> KVCacheBlock | None:
        """Allocate a CPU block for a layer."""
        with self._lock:
            free_list = self._free_cpu_blocks.get(layer_idx, [])
            if not free_list:
                return None
            
            block_id = free_list.pop() - self.config.num_gpu_blocks
            block = self._cpu_pools[layer_idx][block_id]
            block.acquire()
            return block
    
    def free_block(self, block: KVCacheBlock) -> None:
        """Return a block to the pool."""
        with self._lock:
            if block.release():
                if block.device == DeviceType.CUDA:
                    self._free_gpu_blocks[block.layer_idx].append(block.block_id)
                else:
                    self._free_cpu_blocks[block.layer_idx].append(block.block_id)
                self._total_freed += 1
    
    def get_num_free_gpu_blocks(self) -> int:
        """Get total free GPU blocks across all layers."""
        with self._lock:
            if not self._free_gpu_blocks:
                return 0
            # Return min across layers (bottleneck)
            return min(len(free) for free in self._free_gpu_blocks.values())
    
    def get_num_free_cpu_blocks(self) -> int:
        """Get total free CPU blocks across all layers."""
        with self._lock:
            if not self._free_cpu_blocks:
                return 0
            return min(len(free) for free in self._free_cpu_blocks.values())
    
    @property
    def usage(self) -> float:
        """Get GPU block usage ratio."""
        total = self.config.num_gpu_blocks * self.config.num_layers
        free = sum(len(free) for free in self._free_gpu_blocks.values())
        if total == 0:
            return 0.0
        return 1.0 - (free / total)


class PagedKVCache:
    """
    Paged KV cache with block-level management.
    
    Supports efficient memory utilization through paging.
    """
    
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
        """Allocate KV cache blocks for a request."""
        num_blocks_needed = (num_tokens + self.config.block_size - 1) // self.config.block_size
        
        result = KVCacheBlocks()
        self._request_blocks[request_id] = {}
        self._block_tables[request_id] = {}
        
        for layer_idx in range(self.config.num_layers):
            layer_blocks: list[KVCacheBlock] = []
            block_ids: list[int] = []
            
            for _ in range(num_blocks_needed):
                block = self.allocator.allocate_gpu_block(layer_idx)
                if block is None:
                    # Try CPU
                    block = self.allocator.allocate_cpu_block(layer_idx)
                
                if block is None:
                    # Out of memory
                    break
                
                block.request_id = request_id
                layer_blocks.append(block)
                block_ids.append(block.block_id)
                
                if block.device == DeviceType.CUDA:
                    result.append_gpu(block.block_id)
                else:
                    result.append_cpu(block.block_id)
            
            self._request_blocks[request_id][layer_idx] = layer_blocks
            self._block_tables[request_id][layer_idx] = block_ids
        
        return result
    
    def extend_allocation(
        self,
        request_id: str,
        additional_tokens: int,
    ) -> KVCacheBlocks:
        """Extend allocation for a request."""
        if request_id not in self._request_blocks:
            return self.allocate_for_request(request_id, additional_tokens)
        
        # Calculate additional blocks needed
        current_blocks = len(self._request_blocks[request_id].get(0, []))
        current_capacity = current_blocks * self.config.block_size
        
        # Check if current blocks can handle additional tokens
        existing = self._block_tables[request_id].get(0, [])
        total_tokens_in_blocks = sum(
            self._get_block_tokens(request_id, 0, bid) for bid in existing
        )
        
        if total_tokens_in_blocks + additional_tokens <= current_capacity:
            return KVCacheBlocks()  # No new blocks needed
        
        # Allocate additional blocks
        additional_blocks = (additional_tokens + self.config.block_size - 1) // self.config.block_size
        result = KVCacheBlocks()
        
        for layer_idx in range(self.config.num_layers):
            for _ in range(additional_blocks):
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
        
        return result
    
    def _get_block_tokens(self, request_id: str, layer_idx: int, block_id: int) -> int:
        """Get number of tokens in a block."""
        blocks = self._request_blocks.get(request_id, {}).get(layer_idx, [])
        for block in blocks:
            if block.block_id == block_id:
                return block.num_tokens
        return 0
    
    def free_request(self, request_id: str) -> None:
        """Free all blocks for a request."""
        blocks = self._request_blocks.pop(request_id, {})
        for layer_blocks in blocks.values():
            for block in layer_blocks:
                self.allocator.free_block(block)
        self._block_tables.pop(request_id, None)
    
    def get_block_table(self, request_id: str, layer_idx: int) -> list[int]:
        """Get block IDs for a request/layer."""
        return self._block_tables.get(request_id, {}).get(layer_idx, [])
    
    @property
    def usage(self) -> float:
        return self.allocator.usage
    
    def get_num_free_blocks(self) -> int:
        return self.allocator.get_num_free_gpu_blocks()


class KVCacheTransfer:
    """
    Manages CPU-GPU tensor transfers for KV cache swapping.
    """
    
    def __init__(self, config: KVCacheConfig):
        self.config = config
        self._pending_transfers: list[tuple[KVCacheBlock, KVCacheBlock]] = []
    
    def swap_out(self, gpu_block: KVCacheBlock, cpu_block: KVCacheBlock) -> None:
        """Queue a GPU->CPU transfer."""
        if gpu_block.key_cache is not None and cpu_block.key_cache is not None:
            np.copyto(cpu_block.key_cache, gpu_block.key_cache)
            np.copyto(cpu_block.value_cache, gpu_block.value_cache)
            cpu_block.num_tokens = gpu_block.num_tokens
            cpu_block.request_id = gpu_block.request_id
            cpu_block.position_offset = gpu_block.position_offset
    
    def swap_in(self, cpu_block: KVCacheBlock, gpu_block: KVCacheBlock) -> None:
        """Queue a CPU->GPU transfer."""
        if cpu_block.key_cache is not None and gpu_block.key_cache is not None:
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
        """Copy content between blocks."""
        for src, dst in zip(src_blocks, dst_blocks):
            if src.key_cache is not None and dst.key_cache is not None:
                np.copyto(dst.key_cache, src.key_cache)
                np.copyto(dst.value_cache, src.value_cache)
                dst.num_tokens = src.num_tokens


class KVCacheManager:
    """
    Main KV cache manager coordinating allocation, caching, and transfers.
    """
    
    def __init__(self, config: KVCacheConfig):
        self.config = config
        self.paged_cache = PagedKVCache(config)
        self.transfer = KVCacheTransfer(config)
        
        # Callbacks
        self._memory_pressure_callbacks: list[Callable[[], None]] = []
    
    def allocate(self, request_id: str, num_tokens: int) -> KVCacheBlocks:
        """Allocate KV cache for a request."""
        return self.paged_cache.allocate_for_request(request_id, num_tokens)
    
    def extend(self, request_id: str, additional_tokens: int) -> KVCacheBlocks:
        """Extend KV cache allocation."""
        return self.paged_cache.extend_allocation(request_id, additional_tokens)
    
    def free(self, request_id: str) -> None:
        """Free KV cache for a request."""
        self.paged_cache.free_request(request_id)
    
    def get_block_table(self, request_id: str, layer_idx: int) -> list[int]:
        """Get block table for attention."""
        return self.paged_cache.get_block_table(request_id, layer_idx)
    
    @property
    def usage(self) -> float:
        return self.paged_cache.usage
    
    def get_num_free_blocks(self) -> int:
        return self.paged_cache.get_num_free_blocks()
    
    def can_allocate(self, num_tokens: int) -> bool:
        """Check if we can allocate blocks for num_tokens."""
        blocks_needed = (num_tokens + self.config.block_size - 1) // self.config.block_size
        return self.get_num_free_blocks() >= blocks_needed
    
    def on_memory_pressure(self, callback: Callable[[], None]) -> None:
        """Register memory pressure callback."""
        self._memory_pressure_callbacks.append(callback)
    
    def _trigger_memory_pressure(self) -> None:
        """Trigger memory pressure callbacks."""
        for callback in self._memory_pressure_callbacks:
            callback()


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
    """Create a KV cache manager."""
    config = KVCacheConfig(
        num_layers=num_layers,
        num_heads=num_heads,
        head_dim=head_dim,
        num_gpu_blocks=num_blocks,
        block_size=block_size,
    )
    return KVCacheManager(config)
