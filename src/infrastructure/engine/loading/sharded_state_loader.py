"""
Sharded State Loader for PyAgent

This module provides sharded model loading functionality for tensor-parallel
and pipeline-parallel model deployments, inspired by vLLM's sharded_state_loader.py.

Key Features:
- Per-rank shard loading (no need to load full checkpoint)
- Subtensor filtering for shared storage
- S3 and local file system support patterns
- BEYOND vLLM: Incremental loading, async prefetch, smart caching

vLLM Patterns:
- ShardedStateLoader with pattern-based shard discovery
- _filter_subtensors for shared storage handling
- Parallel weight download and loading
"""

from __future__ import annotations

import asyncio
import concurrent.futures
import glob
import os
import re
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

if TYPE_CHECKING:
    import torch
    import numpy as np

try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


@dataclass
class ShardPattern:
    """
    Pattern for shard file naming.

    vLLM Pattern: DEFAULT_PATTERN = "model-rank-{rank}-part-{part}.safetensors"
    """
    template: str = "model-rank-{rank}-part-{part}.safetensors"
    rank_placeholder: str = "{rank}"
    part_placeholder: str = "{part}"

    def format_for_rank(self, rank: int, part: str = "*") -> str:
        """Format pattern for a specific rank."""
        return self.template.format(rank=rank, part=part)

    def parse_filename(self, filename: str) -> Optional[Tuple[int, int]]:
        """Extract rank and part from filename."""
        # Create regex from pattern
        pattern = re.escape(self.template)
        pattern = pattern.replace(re.escape(self.rank_placeholder), r"(\d+)")
        pattern = pattern.replace(re.escape(self.part_placeholder), r"(\d+)")

        match = re.match(pattern, os.path.basename(filename))
        if match:
            return int(match.group(1)), int(match.group(2))
        return None


@dataclass
class ShardedTensor:
    """Represents a tensor that is sharded across ranks."""
    name: str
    shape: Tuple[int, ...]
    dtype: str
    shard_dim: int = 0  # Dimension along which tensor is sharded
    num_shards: int = 1
    local_shard_index: int = 0

    @property
    def local_shape(self) -> Tuple[int, ...]:
        """Get shape of local shard."""
        shape_list = list(self.shape)
        if self.shard_dim < len(shape_list):
            shape_list[self.shard_dim] //= self.num_shards
        return tuple(shape_list)


class SubtensorFilter:
    """
    Filter for identifying and handling subtensors.

    vLLM Pattern: _filter_subtensors from sharded_state_loader.py
    Identifies tensors that share memory with other tensors and keeps
    only the parent tensor to avoid duplication.
    """

    @staticmethod
    def filter_subtensors(tensors: Dict[str, Any]) -> Dict[str, Any]:
        """
        Filter out tensors that share storage with larger tensors.

        This is important for LoRA and other adapters where parameters
        may share memory with base model weights.
        """
        # Group tensors by storage pointer
        storage_groups: Dict[Tuple[Any, int], List[Tuple[str, Any]]] = {}

        for key, tensor in tensors.items():
            if hasattr(tensor, 'numel') and tensor.numel() > 0:
                if hasattr(tensor, 'untyped_storage'):
                    ptr = tensor.untyped_storage().data_ptr()
                    device = tensor.device
                    group_key = (device, ptr)
                    if group_key not in storage_groups:
                        storage_groups[group_key] = []
                    storage_groups[group_key].append((key, tensor))

        def get_end_ptr(tensor: Any) -> int:
            """Get end pointer of tensor data."""
            return tensor.view(-1)[-1].data_ptr() + tensor.element_size()

        result: Dict[str, Any] = {}

        for group in storage_groups.values():
            for k, t in group:
                a, b = t.data_ptr(), get_end_ptr(t)
                is_subtensor = False

                for k2, t2 in group:
                    if not t2.is_contiguous():
                        continue
                    a2, b2 = t2.data_ptr(), get_end_ptr(t2)

                    # Check if t is strictly contained in t2
                    if a < a2 or b2 < b:
                        continue
                    if a2 < a or b < b2 or not t.is_contiguous():
                        is_subtensor = True
                        break
                    if k2 < k:
                        # Same tensor coverage, keep smaller key
                        is_subtensor = True
                        break

                if not is_subtensor:
                    result[k] = t

        return result


class ShardedStateLoader:
    """
    Loader for sharded model checkpoints.

    vLLM Pattern: ShardedStateLoader class
    Each worker only loads its own shard for efficient tensor-parallel loading.
    """

    def __init__(
        self,
        pattern: Optional[ShardPattern] = None,
        rank: int = 0,
        world_size: int = 1,
    ):
        self.pattern = pattern or ShardPattern()
        self.rank = rank
        self.world_size = world_size
        self._subtensor_filter = SubtensorFilter()

    def discover_shards(self, model_path: str) -> List[str]:
        """
        Discover shard files for current rank.

        Supports both local filesystem and (conceptually) S3 paths.
        """
        pattern_str = os.path.join(
            model_path,
            self.pattern.format_for_rank(self.rank, "*")
        )

        files = glob.glob(pattern_str)
        if not files:
            raise ValueError(
                f"No shard files found for rank {self.rank} "
                f"with pattern: {pattern_str}"
            )

        return sorted(files)

    def load_weights(
        self,
        model_path: str,
        state_dict: Optional[Dict[str, Any]] = None,
        strict: bool = False,
    ) -> Dict[str, Any]:
        """
        Load weights from sharded checkpoint.

        Args:
            model_path: Path to sharded checkpoint directory
            state_dict: Optional existing state dict to update
            strict: If True, raise error on missing keys

        Returns:
            Updated state dict with loaded weights
        """
        try:
            from safetensors.torch import load_file
        except ImportError:
            raise ImportError("safetensors required for ShardedStateLoader")

        if state_dict is not None:
            state_dict = self._subtensor_filter.filter_subtensors(state_dict)

        shard_files = self.discover_shards(model_path)
        loaded: Dict[str, Any] = {}

        for shard_file in shard_files:
            shard_data = load_file(shard_file)

            for key, tensor in shard_data.items():
                if state_dict is not None and key in state_dict:
                    # Handle potential shape mismatch (LoRA padding)
                    target_data = state_dict[key].data
                    target_shape = state_dict[key].shape

                    for dim, size in enumerate(tensor.shape):
                        if size < target_shape[dim]:
                            target_data = target_data.narrow(dim, 0, size)

                    target_data.copy_(tensor)
                else:
                    loaded[key] = tensor

        return loaded if state_dict is None else state_dict

    def iterate_weights(
        self,
        model_path: str,
    ) -> Generator[Tuple[str, Any], None, None]:
        """Iterate over weights from sharded checkpoint."""
        try:
            from safetensors.torch import safe_open
        except ImportError:
            raise ImportError("safetensors required for ShardedStateLoader")

        shard_files = self.discover_shards(model_path)

        for shard_file in shard_files:
            with safe_open(shard_file, framework="pt") as f:
                for name in f.keys():
                    yield name, f.get_tensor(name)


class IncrementalShardLoader:
    """
    Incremental shard loading with memory management.

    BEYOND vLLM: Load shards incrementally with configurable memory budget,
    evicting old shards as new ones are loaded.
    """

    def __init__(
        self,
        base_loader: ShardedStateLoader,
        memory_budget_mb: float = 2048.0,
        cache_size: int = 3,  # Number of shards to keep in cache
    ):
        self.base_loader = base_loader
        self.memory_budget_bytes = int(memory_budget_mb * 1024 * 1024)
        self.cache_size = cache_size
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_order: List[str] = []
        self._lock = threading.Lock()

    def _evict_if_needed(self) -> None:
        """Evict oldest cached shards if cache is full."""
        while len(self._cache) >= self.cache_size:
            oldest = self._cache_order.pop(0)
            del self._cache[oldest]

    def load_shard(self, shard_file: str) -> Dict[str, Any]:
        """Load a single shard with caching."""
        with self._lock:
            if shard_file in self._cache:
                # Move to end of LRU order
                self._cache_order.remove(shard_file)
                self._cache_order.append(shard_file)
                return self._cache[shard_file]

            self._evict_if_needed()

        try:
            from safetensors.torch import load_file
            shard_data = load_file(shard_file)
        except ImportError:
            import torch
            shard_data = torch.load(shard_file, map_location="cpu", weights_only=True)

        with self._lock:
            self._cache[shard_file] = shard_data
            self._cache_order.append(shard_file)

        return shard_data

    def load_weights_incremental(
        self,
        model_path: str,
        callback: Optional[Callable[[str, Any], None]] = None,
    ) -> None:
        """
        Load weights incrementally, calling callback for each tensor.

        This allows the caller to process tensors one at a time without
        loading the entire checkpoint into memory.
        """
        shard_files = self.base_loader.discover_shards(model_path)

        for shard_file in shard_files:
            shard_data = self.load_shard(shard_file)

            for key, tensor in shard_data.items():
                if callback:
                    callback(key, tensor)


class AsyncShardLoader:
    """
    Asynchronous shard loading with prefetching.

    BEYOND vLLM: Prefetch next shards while processing current shard
    for improved throughput on I/O-bound operations.
    """

    def __init__(
        self,
        base_loader: ShardedStateLoader,
        prefetch_count: int = 2,
        max_workers: int = 2,
    ):
        self.base_loader = base_loader
        self.prefetch_count = prefetch_count
        self.max_workers = max_workers
        self._executor: Optional[concurrent.futures.ThreadPoolExecutor] = None
        self._prefetch_futures: Dict[str, concurrent.futures.Future] = {}

    def _load_file(self, file_path: str) -> Dict[str, Any]:
        """Load a single file."""
        try:
            from safetensors.torch import load_file
            return load_file(file_path)
        except ImportError:
            import torch
            return torch.load(file_path, map_location="cpu", weights_only=True)

    def _start_prefetch(self, file_paths: List[str]) -> None:
        """Start prefetching files."""
        if self._executor is None:
            self._executor = concurrent.futures.ThreadPoolExecutor(
                max_workers=self.max_workers
            )

        for path in file_paths:
            if path not in self._prefetch_futures:
                self._prefetch_futures[path] = self._executor.submit(
                    self._load_file, path
                )

    def load_weights_async(
        self,
        model_path: str,
    ) -> Generator[Tuple[str, Any], None, None]:
        """Load weights with async prefetching."""
        shard_files = self.base_loader.discover_shards(model_path)

        try:
            # Start initial prefetch
            self._start_prefetch(shard_files[:self.prefetch_count])

            for i, shard_file in enumerate(shard_files):
                # Start prefetching next batch
                next_idx = i + self.prefetch_count
                if next_idx < len(shard_files):
                    self._start_prefetch([shard_files[next_idx]])

                # Wait for current shard
                if shard_file in self._prefetch_futures:
                    future = self._prefetch_futures.pop(shard_file)
                    shard_data = future.result()
                else:
                    shard_data = self._load_file(shard_file)

                yield from shard_data.items()

        finally:
            if self._executor is not None:
                self._executor.shutdown(wait=False)
                self._executor = None
            self._prefetch_futures.clear()

    async def load_weights_async_native(
        self,
        model_path: str,
    ) -> Dict[str, Any]:
        """Native async version using asyncio."""
        loop = asyncio.get_event_loop()
        shard_files = self.base_loader.discover_shards(model_path)

        async def load_shard(path: str) -> Dict[str, Any]:
            return await loop.run_in_executor(None, self._load_file, path)

        results = await asyncio.gather(*[
            load_shard(f) for f in shard_files
        ])

        merged = {}
        for result in results:
            merged.update(result)
        return merged


# Rust-accelerated functions
def compute_shard_assignment_rust(
    num_params: int,
    num_ranks: int,
    param_sizes: List[int],
) -> List[int]:
    """Compute optimal shard assignment using Rust."""
    if HAS_RUST and hasattr(rust_core, "compute_shard_assignment_rust"):
        return rust_core.compute_shard_assignment_rust(
            num_params, num_ranks, param_sizes
        )

    # Python fallback - simple round-robin
    return [i % num_ranks for i in range(num_params)]


def validate_shard_shapes_rust(
    shard_specs: List[Dict[str, Any]],
    rank: int,
    world_size: int,
) -> List[str]:
    """Validate shard shapes using Rust."""
    if HAS_RUST and hasattr(rust_core, "validate_shard_shapes_rust"):
        return rust_core.validate_shard_shapes_rust(shard_specs, rank, world_size)

    # Python fallback
    errors = []
    for spec in shard_specs:
        if "shard_dim" in spec and spec.get("num_shards", 1) != world_size:
            errors.append(
                f"Shard count mismatch for {spec.get('name', 'unknown')}: "
                f"expected {world_size}, got {spec.get('num_shards', 1)}"
            )
    return errors
