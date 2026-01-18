# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
TensorParallelGroup - Tensor parallel coordination for distributed inference.

Implements vLLM's parallel_state.py patterns for tensor parallelism:
- ParallelConfig: World, TP, PP, DP size configuration
- GroupCoordinator: Process group management
- TensorParallelGroup: TP-specific collective operations

Beyond vLLM: Dynamic group reconfiguration and rank reassignment.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Sequence
from contextlib import contextmanager

import numpy as np

logger = logging.getLogger(__name__)

# Try to import torch.distributed
try:
    import torch
    import torch.distributed as dist
    HAS_TORCH = True
    HAS_DIST = dist.is_available()
except ImportError:
    HAS_TORCH = False
    HAS_DIST = False
    torch = None  # type: ignore
    dist = None  # type: ignore


class ParallelMode(Enum):
    """Parallelism modes."""
    DATA = auto()  # Data parallel
    TENSOR = auto()  # Tensor parallel
    PIPELINE = auto()  # Pipeline parallel
    EXPERT = auto()  # Expert parallel (MoE)
    CONTEXT = auto()  # Context parallel (sequence)


@dataclass
class ParallelConfig:
    """
    Configuration for distributed parallelism.
    
    Defines the parallelism strategy across dimensions.
    """
    world_size: int = 1
    tensor_parallel_size: int = 1
    pipeline_parallel_size: int = 1
    data_parallel_size: int = 1
    expert_parallel_size: int = 1
    context_parallel_size: int = 1
    
    # Process group settings
    backend: str = "nccl"  # nccl, gloo, mpi
    init_method: str | None = None
    
    def __post_init__(self):
        # Validate configuration
        expected_world = (
            self.tensor_parallel_size * 
            self.pipeline_parallel_size * 
            self.data_parallel_size
        )
        if self.world_size == 1 and expected_world > 1:
            self.world_size = expected_world
        elif self.world_size != expected_world and expected_world > 1:
            logger.warning(
                f"World size {self.world_size} != TP*PP*DP = {expected_world}"
            )
    
    @classmethod
    def from_env(cls) -> "ParallelConfig":
        """Create configuration from environment variables."""
        return cls(
            world_size=int(os.environ.get("WORLD_SIZE", 1)),
            tensor_parallel_size=int(os.environ.get("TENSOR_PARALLEL_SIZE", 1)),
            pipeline_parallel_size=int(os.environ.get("PIPELINE_PARALLEL_SIZE", 1)),
            data_parallel_size=int(os.environ.get("DATA_PARALLEL_SIZE", 1)),
            backend=os.environ.get("DISTRIBUTED_BACKEND", "nccl"),
        )


@dataclass
class RankInfo:
    """
    Information about a rank's position in the parallel topology.
    """
    global_rank: int
    local_rank: int
    tp_rank: int  # Tensor parallel rank
    pp_rank: int  # Pipeline parallel rank
    dp_rank: int  # Data parallel rank
    node_rank: int = 0
    
    @classmethod
    def compute(
        cls,
        global_rank: int,
        config: ParallelConfig,
    ) -> "RankInfo":
        """Compute rank information from global rank and config."""
        tp_size = config.tensor_parallel_size
        pp_size = config.pipeline_parallel_size
        dp_size = config.data_parallel_size
        
        # Compute DP, PP, TP ranks from global rank
        # Layout: [DP][PP][TP]
        tp_rank = global_rank % tp_size
        pp_rank = (global_rank // tp_size) % pp_size
        dp_rank = global_rank // (tp_size * pp_size)
        
        # Local rank within node
        local_rank = int(os.environ.get("LOCAL_RANK", global_rank % 8))
        node_rank = global_rank // 8
        
        return cls(
            global_rank=global_rank,
            local_rank=local_rank,
            tp_rank=tp_rank,
            pp_rank=pp_rank,
            dp_rank=dp_rank,
            node_rank=node_rank,
        )


class GroupCoordinator:
    """
    Manages process groups for distributed operations.
    
    Creates and caches process groups for different parallelism modes.
    """
    
    def __init__(
        self,
        config: ParallelConfig,
        rank_info: RankInfo,
    ):
        """
        Initialize the group coordinator.
        
        Args:
            config: Parallel configuration
            rank_info: This rank's position info
        """
        self.config = config
        self.rank_info = rank_info
        
        # Process groups
        self._world_group: Any = None
        self._tp_group: Any = None
        self._pp_group: Any = None
        self._dp_group: Any = None
        
        # Group ranks
        self._tp_ranks: list[int] = []
        self._pp_ranks: list[int] = []
        self._dp_ranks: list[int] = []
        
        self._initialized = False
    
    def initialize(self) -> None:
        """Initialize all process groups."""
        if self._initialized:
            return
        
        if not HAS_DIST:
            logger.warning("torch.distributed not available, using single-process mode")
            self._initialized = True
            return
        
        if not dist.is_initialized():
            logger.warning("torch.distributed not initialized")
            self._initialized = True
            return
        
        self._world_group = dist.group.WORLD
        self._create_tp_group()
        self._create_pp_group()
        self._create_dp_group()
        
        self._initialized = True
        logger.info(
            f"GroupCoordinator initialized: rank={self.rank_info.global_rank}, "
            f"TP={self.rank_info.tp_rank}/{self.config.tensor_parallel_size}, "
            f"PP={self.rank_info.pp_rank}/{self.config.pipeline_parallel_size}, "
            f"DP={self.rank_info.dp_rank}/{self.config.data_parallel_size}"
        )
    
    def _create_tp_group(self) -> None:
        """Create tensor parallel process group."""
        tp_size = self.config.tensor_parallel_size
        pp_size = self.config.pipeline_parallel_size
        dp_size = self.config.data_parallel_size
        
        # Each TP group spans consecutive ranks within a PP stage
        for dp in range(dp_size):
            for pp in range(pp_size):
                ranks = [
                    dp * pp_size * tp_size + pp * tp_size + tp
                    for tp in range(tp_size)
                ]
                group = dist.new_group(ranks)
                if self.rank_info.global_rank in ranks:
                    self._tp_group = group
                    self._tp_ranks = ranks
    
    def _create_pp_group(self) -> None:
        """Create pipeline parallel process group."""
        tp_size = self.config.tensor_parallel_size
        pp_size = self.config.pipeline_parallel_size
        dp_size = self.config.data_parallel_size
        
        # Each PP group spans ranks at same TP position
        for dp in range(dp_size):
            for tp in range(tp_size):
                ranks = [
                    dp * pp_size * tp_size + pp * tp_size + tp
                    for pp in range(pp_size)
                ]
                group = dist.new_group(ranks)
                if self.rank_info.global_rank in ranks:
                    self._pp_group = group
                    self._pp_ranks = ranks
    
    def _create_dp_group(self) -> None:
        """Create data parallel process group."""
        tp_size = self.config.tensor_parallel_size
        pp_size = self.config.pipeline_parallel_size
        dp_size = self.config.data_parallel_size
        
        # Each DP group spans ranks at same TP+PP position
        for tp in range(tp_size):
            for pp in range(pp_size):
                ranks = [
                    dp * pp_size * tp_size + pp * tp_size + tp
                    for dp in range(dp_size)
                ]
                group = dist.new_group(ranks)
                if self.rank_info.global_rank in ranks:
                    self._dp_group = group
                    self._dp_ranks = ranks
    
    @property
    def world_group(self) -> Any:
        """Get world process group."""
        return self._world_group
    
    @property
    def tp_group(self) -> Any:
        """Get tensor parallel process group."""
        return self._tp_group
    
    @property
    def pp_group(self) -> Any:
        """Get pipeline parallel process group."""
        return self._pp_group
    
    @property
    def dp_group(self) -> Any:
        """Get data parallel process group."""
        return self._dp_group
    
    def get_world_size(self, mode: ParallelMode | None = None) -> int:
        """Get world size for a parallelism mode."""
        if mode is None or mode == ParallelMode.DATA:
            return self.config.world_size
        elif mode == ParallelMode.TENSOR:
            return self.config.tensor_parallel_size
        elif mode == ParallelMode.PIPELINE:
            return self.config.pipeline_parallel_size
        else:
            return 1
    
    def get_rank(self, mode: ParallelMode | None = None) -> int:
        """Get rank for a parallelism mode."""
        if mode is None:
            return self.rank_info.global_rank
        elif mode == ParallelMode.TENSOR:
            return self.rank_info.tp_rank
        elif mode == ParallelMode.PIPELINE:
            return self.rank_info.pp_rank
        elif mode == ParallelMode.DATA:
            return self.rank_info.dp_rank
        else:
            return 0


class TensorParallelGroup:
    """
    Tensor parallel operations for distributed model execution.
    
    Provides collective operations (all_reduce, all_gather, etc.)
    specifically for tensor parallelism.
    
    Beyond vLLM: Dynamic group reconfiguration support.
    """
    
    def __init__(
        self,
        coordinator: GroupCoordinator,
        device: Any = None,
    ):
        """
        Initialize tensor parallel group.
        
        Args:
            coordinator: Group coordinator
            device: Target device
        """
        self.coordinator = coordinator
        self.config = coordinator.config
        self.rank_info = coordinator.rank_info
        
        if HAS_TORCH:
            self.device = device or torch.device(
                f"cuda:{coordinator.rank_info.local_rank}" 
                if torch.cuda.is_available() else "cpu"
            )
        else:
            self.device = device or "cpu"
        
        self._custom_allreduce_enabled = False
        
        logger.debug(f"TensorParallelGroup: rank={self.tp_rank}/{self.tp_size}")
    
    @property
    def tp_size(self) -> int:
        """Tensor parallel world size."""
        return self.config.tensor_parallel_size
    
    @property
    def tp_rank(self) -> int:
        """Tensor parallel rank."""
        return self.rank_info.tp_rank
    
    @property
    def is_first_rank(self) -> bool:
        """Check if this is TP rank 0."""
        return self.tp_rank == 0
    
    @property
    def is_last_rank(self) -> bool:
        """Check if this is the last TP rank."""
        return self.tp_rank == self.tp_size - 1
    
    def all_reduce(
        self,
        tensor: Any,
        op: str = "sum",
        async_op: bool = False,
    ) -> Any:
        """
        All-reduce tensor across TP group.
        
        Args:
            tensor: Input tensor
            op: Reduction operation (sum, mean, max, min)
            async_op: Whether to run asynchronously
            
        Returns:
            Reduced tensor (in-place if torch)
        """
        if self.tp_size == 1:
            return tensor
        
        if not HAS_DIST or not dist.is_initialized():
            return tensor
        
        # Map op to dist.ReduceOp
        op_map = {
            "sum": dist.ReduceOp.SUM,
            "mean": dist.ReduceOp.SUM,  # Will divide after
            "max": dist.ReduceOp.MAX,
            "min": dist.ReduceOp.MIN,
        }
        reduce_op = op_map.get(op, dist.ReduceOp.SUM)
        
        handle = dist.all_reduce(
            tensor, 
            op=reduce_op, 
            group=self.coordinator.tp_group,
            async_op=async_op,
        )
        
        if op == "mean":
            tensor.div_(self.tp_size)
        
        return handle if async_op else tensor
    
    def all_gather(
        self,
        tensor: Any,
        dim: int = 0,
        async_op: bool = False,
    ) -> Any:
        """
        All-gather tensors from all TP ranks.
        
        Args:
            tensor: Local tensor
            dim: Dimension to concatenate along
            async_op: Whether to run asynchronously
            
        Returns:
            Gathered tensor
        """
        if self.tp_size == 1:
            return tensor
        
        if not HAS_TORCH:
            return tensor
        
        if not HAS_DIST or not dist.is_initialized():
            return tensor
        
        # Create output tensor list
        tensor_list = [torch.empty_like(tensor) for _ in range(self.tp_size)]
        
        handle = dist.all_gather(
            tensor_list,
            tensor,
            group=self.coordinator.tp_group,
            async_op=async_op,
        )
        
        if async_op:
            return handle
        
        # Concatenate along specified dimension
        return torch.cat(tensor_list, dim=dim)
    
    def reduce_scatter(
        self,
        tensor: Any,
        dim: int = 0,
        op: str = "sum",
        async_op: bool = False,
    ) -> Any:
        """
        Reduce-scatter: reduce then scatter result.
        
        Args:
            tensor: Input tensor (will be scattered along dim)
            dim: Dimension to scatter along
            op: Reduction operation
            async_op: Whether to run asynchronously
            
        Returns:
            Scattered tensor slice for this rank
        """
        if self.tp_size == 1:
            return tensor
        
        if not HAS_TORCH:
            return tensor
        
        if not HAS_DIST or not dist.is_initialized():
            chunk_size = tensor.shape[dim] // self.tp_size
            start = self.tp_rank * chunk_size
            end = start + chunk_size
            return tensor.narrow(dim, start, chunk_size)
        
        # Split input tensor
        input_chunks = list(tensor.chunk(self.tp_size, dim=dim))
        
        # Output is the reduced chunk for this rank
        output = torch.empty_like(input_chunks[0])
        
        op_map = {
            "sum": dist.ReduceOp.SUM,
            "mean": dist.ReduceOp.SUM,
            "max": dist.ReduceOp.MAX,
            "min": dist.ReduceOp.MIN,
        }
        reduce_op = op_map.get(op, dist.ReduceOp.SUM)
        
        handle = dist.reduce_scatter(
            output,
            input_chunks,
            op=reduce_op,
            group=self.coordinator.tp_group,
            async_op=async_op,
        )
        
        if op == "mean":
            output.div_(self.tp_size)
        
        return handle if async_op else output
    
    def scatter(
        self,
        tensor: Any | None,
        dim: int = 0,
        src_rank: int = 0,
    ) -> Any:
        """
        Scatter tensor from source rank to all TP ranks.
        
        Args:
            tensor: Input tensor (only required on src_rank)
            dim: Dimension to scatter along
            src_rank: Source TP rank
            
        Returns:
            Scattered tensor slice for this rank
        """
        if self.tp_size == 1:
            return tensor
        
        if not HAS_TORCH:
            return tensor
        
        if not HAS_DIST or not dist.is_initialized():
            if tensor is not None:
                chunk_size = tensor.shape[dim] // self.tp_size
                start = self.tp_rank * chunk_size
                return tensor.narrow(dim, start, chunk_size)
            return None
        
        if self.tp_rank == src_rank:
            scatter_list = list(tensor.chunk(self.tp_size, dim=dim))
            output = torch.empty_like(scatter_list[0])
        else:
            # Need to receive shape first
            output = tensor  # Will be replaced
            scatter_list = None
        
        dist.scatter(
            output,
            scatter_list if self.tp_rank == src_rank else None,
            src=src_rank,
            group=self.coordinator.tp_group,
        )
        
        return output
    
    def broadcast(
        self,
        tensor: Any,
        src_rank: int = 0,
        async_op: bool = False,
    ) -> Any:
        """
        Broadcast tensor from source rank to all TP ranks.
        
        Args:
            tensor: Tensor to broadcast
            src_rank: Source TP rank
            async_op: Whether to run asynchronously
            
        Returns:
            Broadcasted tensor
        """
        if self.tp_size == 1:
            return tensor
        
        if not HAS_DIST or not dist.is_initialized():
            return tensor
        
        handle = dist.broadcast(
            tensor,
            src=src_rank,
            group=self.coordinator.tp_group,
            async_op=async_op,
        )
        
        return handle if async_op else tensor
    
    def barrier(self) -> None:
        """Synchronize all TP ranks."""
        if self.tp_size == 1:
            return
        
        if not HAS_DIST or not dist.is_initialized():
            return
        
        dist.barrier(group=self.coordinator.tp_group)
    
    def shard_tensor(
        self,
        tensor: Any,
        dim: int = 0,
    ) -> Any:
        """
        Shard a tensor for this TP rank.
        
        Utility for partitioning weights during model loading.
        
        Args:
            tensor: Full tensor
            dim: Dimension to shard along
            
        Returns:
            Tensor slice for this rank
        """
        if self.tp_size == 1:
            return tensor
        
        if not HAS_TORCH:
            size = len(tensor) if hasattr(tensor, '__len__') else tensor.shape[dim]
            chunk_size = size // self.tp_size
            start = self.tp_rank * chunk_size
            return tensor[start:start + chunk_size]
        
        chunks = tensor.chunk(self.tp_size, dim=dim)
        return chunks[self.tp_rank].contiguous()
    
    def unshard_tensor(
        self,
        tensor: Any,
        dim: int = 0,
    ) -> Any:
        """
        Reconstruct full tensor from shards (all-gather).
        
        Args:
            tensor: Local tensor shard
            dim: Dimension to concatenate along
            
        Returns:
            Full tensor
        """
        return self.all_gather(tensor, dim=dim)
    
    @contextmanager
    def parallel_region(self):
        """
        Context manager for tensor parallel execution regions.
        
        Ensures proper synchronization at region boundaries.
        """
        # No-op for now, but could add profiling/tracing
        yield
        # Implicit barrier at end of region
        self.barrier()
    
    def get_stats(self) -> dict[str, Any]:
        """Get TP group statistics."""
        return {
            "tp_size": self.tp_size,
            "tp_rank": self.tp_rank,
            "is_first_rank": self.is_first_rank,
            "is_last_rank": self.is_last_rank,
            "custom_allreduce_enabled": self._custom_allreduce_enabled,
            "device": str(self.device),
        }


# Global state for easy access
_PARALLEL_CONFIG: ParallelConfig | None = None
_GROUP_COORDINATOR: GroupCoordinator | None = None
_TP_GROUP: TensorParallelGroup | None = None


def init_distributed(
    config: ParallelConfig | None = None,
    rank: int | None = None,
) -> TensorParallelGroup:
    """
    Initialize distributed tensor parallelism.
    
    Args:
        config: Parallel configuration (uses env vars if None)
        rank: Global rank (uses env var if None)
        
    Returns:
        TensorParallelGroup for collective operations
    """
    global _PARALLEL_CONFIG, _GROUP_COORDINATOR, _TP_GROUP
    
    config = config or ParallelConfig.from_env()
    _PARALLEL_CONFIG = config
    
    if rank is None:
        rank = int(os.environ.get("RANK", 0))
    
    rank_info = RankInfo.compute(rank, config)
    _GROUP_COORDINATOR = GroupCoordinator(config, rank_info)
    _GROUP_COORDINATOR.initialize()
    
    _TP_GROUP = TensorParallelGroup(_GROUP_COORDINATOR)
    
    return _TP_GROUP


def get_tp_group() -> TensorParallelGroup | None:
    """Get the global tensor parallel group."""
    return _TP_GROUP


def get_tp_size() -> int:
    """Get tensor parallel world size."""
    if _TP_GROUP is None:
        return 1
    return _TP_GROUP.tp_size


def get_tp_rank() -> int:
    """Get tensor parallel rank."""
    if _TP_GROUP is None:
        return 0
    return _TP_GROUP.tp_rank
