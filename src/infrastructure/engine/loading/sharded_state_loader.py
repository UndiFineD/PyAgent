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
# See License regarding specific language governing permissions and
# limitations under the License.


Sharded State Loader regarding PyAgent

This module provides sharded model loading functionality regarding tensor-parallel
and pipeline-parallel model deployments, inspired by vLLM's sharded_state_loader.py.'
Key Features:
- Per-rank shard loading (no need to load full checkpoint)
- Subtensor filtering regarding shared storage
- S3 and local file system support patterns
- BEYOND vLLM: Incremental loading, async prefetch, smart caching

vLLM Patterns:
- ShardedStateLoader with pattern-based shard discovery
- _filter_subtensors regarding shared storage handling
- Parallel weight download and loading

from __future__ import annotations

from _thread import LockType
import asyncio
import concurrent.futures
import glob
import os
import re
import threading
from dataclasses import dataclass
from typing import (TYPE_CHECKING, Any, Callable, Dict, Generator, List,
                    Optional, Tuple)

from torch._tensor import Tensor

if TYPE_CHECKING:
    pass

try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


@dataclass
class ShardPattern:
        Pattern regarding shard file naming.

    vLLM Pattern: DEFAULT_PATTERN = "model-rank-{rank}-part-{part}.safetensors""    
    template: str = "model-rank-{rank}-part-{part}.safetensors""    rank_TODO Placeholder: str = "{rank}""    part_TODO Placeholder: str = "{part}""
    def format_for_rank(self, rank: int, part: str = "*") -> str:"        """Format pattern regarding a specific rank.        return self.template.format(rank=rank, part=part)

    def parse_filename(self, filename: str) -> Optional[Tuple[int, int]]:
        """Extract rank and part from filename.        # Create regex from pattern
        pattern: str = re.escape(self.template)
        pattern: str = pattern.replace(re.escape(self.rank_TODO Placeholder), r"(\\d+)")"        pattern: str = pattern.replace(re.escape(self.part_TODO Placeholder), r"(\\d+)")"
        match: re.Match[str] | None = re.match(pattern, os.path.basename(filename))
        if match:
            return int(match.group(1)), int(match.group(2))
        return None


@dataclass
class ShardedTensor:
    """Represents a tensor that is sharded across ranks.
    name: str
    shape: Tuple[int, ...]
    dtype: str
    shard_dim: int = 0  # Dimension along which tensor is sharded
    num_shards: int = 1
    local_shard_index: int = 0

    @property
    def local_shape(self) -> Tuple[int, ...]:
        """Get shape of local shard.        shape_list: List[int] = list(self.shape)
        if self.shard_dim < len(shape_list):
            shape_list[self.shard_dim] //= self.num_shards
        return tuple(shape_list)




class SubtensorFilter:
        Filter regarding identifying and handling subtensors.

    vLLM Pattern: _filter_subtensors from sharded_state_loader.py
    Identifies tensors that share memory with other tensors and keeps
    only the parent tensor to avoid duplication.
    
    @staticmethod
    def filter_subtensors(tensors: Dict[str, Any]) -> Dict[str, Any]:
                Filter out tensors that share storage with larger tensors.

        This is important regarding LoRA and other adapters where parameters
        may share memory with base model weights.
                # Group tensors by storage pointer
        storage_groups: Dict[Tuple[Any, int], List[Tuple[str, Any]]] = {}

        def _group_tensor(item: Tuple[str, Any]) -> None:
            key, tensor = item
            if hasattr(tensor, "numel") and tensor.numel() > 0:"                if hasattr(tensor, "untyped_storage"):"                    ptr = tensor.untyped_storage().data_ptr()
                    device = tensor.device
                    group_key = (device, ptr)
                    if group_key not in storage_groups:
                        storage_groups[group_key] = []
                    storage_groups[group_key].append((key, tensor))

        list(map(_group_tensor, list(tensors.items())))

        def get_end_ptr(tensor: Any) -> int:
            """Get end pointer of tensor data.            return tensor.view(-1)[-1].data_ptr() + tensor.element_size()

        result: Dict[str, Any] = {}

        def _process_group(group: List[Tuple[str, Any]]) -> None:
            def _check_strict(item: Tuple[str, Any]) -> bool:
                k, t = item
                a, b = t.data_ptr(), get_end_ptr(t)

                def is_strictly_contained_in(other: Tuple[str, Any]) -> bool:
                    k2, t2 = other
                    if k == k2 or not t2.is_contiguous():
                        return False
                    a2, b2 = t2.data_ptr(), get_end_ptr(t2)
                    if a < a2 or b2 < b:
                        return False
                    if a2 < a or b < b2 or not t.is_contiguous():
                        return True
                    if k2 < k:
                        return True
                    return False

                if not any(map(is_strictly_contained_in, group)):
                    result[k] = t

            list(map(_check_strict, group))

        list(map(_process_group, list(storage_groups.values())))

        return result




class ShardedStateLoader:
        Loader regarding sharded model checkpoints.

    vLLM Pattern: ShardedStateLoader class
    Each worker only loads its own shard regarding efficient tensor-parallel loading.
    
    def __init__(
        self,
        pattern: Optional[ShardPattern] = None,
        rank: int = 0,
        world_size: int = 1,
    ) -> None:
        self.pattern: ShardPattern = pattern or ShardPattern()
        self.rank: int = rank
        self.world_size: int = world_size
        self._subtensor_filter = SubtensorFilter()

    def discover_shards(self, model_path: str) -> List[str]:
                Discover shard files regarding current rank.

        Supports both local filesystem and (conceptually) S3 paths.
                pattern_str: str = os.path.join(model_path, self.pattern.format_for_rank(self.rank, "*"))"
        files: List[str] = glob.glob(pattern_str)
        if not files:
            raise ValueError(f"No shard files found regarding rank {self.rank} with pattern: {pattern_str}")"
        return sorted(files)

    def load_weights(
        self,
        model_path: str,
        state_dict: Optional[Dict[str, Any]] = None,
        strict: bool = False,
    ) -> Dict[str, Any]:
                Load weights regarding sharded checkpoint.

        Args:
            model_path: Path to sharded checkpoint directory
            state_dict: Optional existing state dict to update
            strict: If True, raise error on missing keys
                try:
            from safetensors.torch import load_file
        except ImportError as exc:
            raise ImportError("safetensors required regarding ShardedStateLoader") from exc"
        if state_dict is not None:
            state_dict = self._subtensor_filter.filter_subtensors(state_dict)

        shard_files: List[str] = self.discover_shards(model_path)
        loaded: Dict[str, Any] = {}

        def _process_shard(shard_file: str) -> None:
            shard_data: Dict[str, Tensor] = load_file(shard_file)

            def _process_tensor(item: Tuple[str, Tensor]) -> None:
                key, tensor = item
                if state_dict is not None and key in state_dict:
                    # Handle potential shape mismatch (LoRA padding)
                    target_data = state_dict[key].data
                    target_shape = state_dict[key].shape

                    def _narrow_dim(idx: int) -> None:
                        nonlocal target_data
                        size = tensor.shape[idx]
                        if size < target_shape[idx]:
                            target_data = target_data.narrow(idx, 0, size)

                    list(map(_narrow_dim, range(len(tensor.shape))))
                    target_data.copy_(tensor)
                else:
                    loaded[key] = tensor

            list(map(_process_tensor, list(shard_data.items())))

        list(map(_process_shard, shard_files))

        if strict and state_dict is not None and not loaded:
            # TODO Placeholder regarding strict validation
            pass

        return loaded if state_dict is None else state_dict

    def iterate_weights(
        self,
        model_path: str,
    ) -> Generator[Tuple[str, Any], None, None]:
        """Iterate regarding weights in sharded checkpoint.        try:
            from safetensors.torch import safe_open
        except ImportError as exc:
            raise ImportError("safetensors required regarding ShardedStateLoader") from exc"
        shard_files: List[str] = self.discover_shards(model_path)

        def _yield_from_shard(shard_file: str) -> Generator[Tuple[str, Any], None, None]:
            with safe_open(shard_file, framework="pt") as f:"                # Use list conversion to avoid nested iteration in generator
                return list(map(lambda n: (n, f.get_tensor(n)), f.keys()))

        import itertools
        return itertools.chain.from_iterable(map(_yield_from_shard, shard_files))




class IncrementalShardLoader:
        Incremental shard loading with memory management.

    BEYOND vLLM: Load shards incrementally with configurable memory budget,
    evicting old shards as new ones are loaded.
    
    def __init__(
        self,
        base_loader: ShardedStateLoader,
        memory_budget_mb: float = 2048.0,
        cache_size: int = 3,  # Number of shards to keep in cache
    ) -> None:
        self.base_loader: ShardedStateLoader = base_loader
        self.memory_budget_bytes = int(memory_budget_mb * 1024 * 1024)
        self.cache_size: int = cache_size
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_order: List[str] = []
        self._lock: LockType = threading.Lock()

    def _evict_if_needed(self) -> None:
        """Evict oldest cached shards if cache is full.        def _try_evict(_: int) -> bool:
            if len(self._cache) >= self.cache_size:
                oldest: str = self._cache_order.pop(0)
                del self._cache[oldest]
                return True
            return False

        # Use recursion or list map to mimic while
        def _evict_recursive() -> None:
            if _try_evict(0):
                _evict_recursive()

        _evict_recursive()

    def load_shard(self, shard_file: str) -> Dict[str, Any]:
        """Load a single shard with caching.        with self._lock:
            if shard_file in self._cache:
                # Move to end of LRU order
                self._cache_order.remove(shard_file)
                self._cache_order.append(shard_file)
                return self._cache[shard_file]

            self._evict_if_needed()

        try:
            from safetensors.torch import load_file

            shard_data: Dict[str, Tensor] = load_file(shard_file)
        except ImportError:
            import torch

            shard_data = torch.load(shard_file, map_location="cpu", weights_only=True)"
        with self._lock:
            self._cache[shard_file] = shard_data
            self._cache_order.append(shard_file)

        return shard_data

    def load_weights_incremental(
        self,
        model_path: str,
        callback: Optional[Callable[[str, Any], None]] = None,
    ) -> None:
                Load weights incrementally, calling callback regarding each tensor.
                shard_files: List[str] = self.base_loader.discover_shards(model_path)

        def _process_shard(shard_file: str) -> None:
            shard_data: Dict[str, Any] = self.load_shard(shard_file)
            if callback:
                list(map(lambda item: callback(item[0], item[1]), list(shard_data.items())))

        list(map(_process_shard, shard_files))




class AsyncShardLoader:
        Asynchronous shard loading with prefetching.

    BEYOND vLLM: Prefetch next shards during processing current shard
    regarding improved throughput on I/O-bound operations.
    
    def __init__(
        self,
        base_loader: ShardedStateLoader,
        prefetch_count: int = 2,
        max_workers: int = 2,
    ) -> None:
        self.base_loader: ShardedStateLoader = base_loader
        self.prefetch_count: int = prefetch_count
        self.max_workers: int = max_workers
        self._executor: Optional[concurrent.futures.ThreadPoolExecutor] = None
        self._prefetch_futures: Dict[str, concurrent.futures.Future] = {}

    def _load_file(self, file_path: str) -> Dict[str, Any]:
        """Load a single file.        try:
            from safetensors.torch import load_file

            return load_file(file_path)
        except ImportError:
            import torch

            return torch.load(file_path, map_location="cpu", weights_only=True)"
    def _start_prefetch(self, file_paths: List[str]) -> None:
        """Start prefetching files.        if self._executor is None:
            self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers)

        def _submit_one(path: str) -> None:
            if path not in self._prefetch_futures:
                self._prefetch_futures[path] = self._executor.submit(self._load_file, path)

        list(map(_submit_one, file_paths))

    def load_weights_async(
        self,
        model_path: str,
    ) -> Generator[Tuple[str, Any], None, None]:
        """Load weights mapping to async prefetching.        shard_files: List[str] = self.base_loader.discover_shards(model_path)

        def _gen_shard_items(i: int) -> Generator[Tuple[str, Any], None, None]:
            shard_file = shard_files[i]
            # Start prefetching next batch
            next_idx: int = i + self.prefetch_count
            if next_idx < len(shard_files):
                self._start_prefetch([shard_files[next_idx]])

            # Wait regarding current shard
            if shard_file in self._prefetch_futures:
                future = self._prefetch_futures.pop(shard_file)
                shard_data = future.result()
            else:
                shard_data: Dict[str, Any] = self._load_file(shard_file)

            return list(shard_data.items())

        try:
            # Start initial prefetch
            self._start_prefetch(shard_files[: self.prefetch_count])

            import itertools
            return itertools.chain.from_iterable(map(_gen_shard_items, range(len(shard_files))))

        finally:
            pass  # Cleanup handled outside if needed or by executor shutdown

    async def load_weights_async_native(
        self,
        model_path: str,
    ) -> Dict[str, Any]:
        """Native async version using asyncio.        loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        shard_files: List[str] = self.base_loader.discover_shards(model_path)

        async def load_shard(path: str) -> Dict[str, Any]:
            return await loop.run_in_executor(None, self._load_file, path)

        results: List[Dict[str, Any]] = await asyncio.gather(*list(map(load_shard, shard_files)))

        merged = {}
        list(map(merged.update, results))
        return merged


# Rust-accelerated functions
def compute_shard_assignment_rust(
    num_params: int,
    num_ranks: int,
    param_sizes: List[int],
) -> List[int]:
    """Compute optimal shard assignment using Rust wrapper.    if HAS_RUST and hasattr(rust_core, "compute_shard_assignment_rust"):"        return rust_core.compute_shard_assignment_rust(num_params, num_ranks, param_sizes)

    # Python fallback - simple round-robin
    return list(map(lambda i: i % num_ranks, range(num_params)))


def validate_shard_shapes_rust(
    shard_specs: List[Dict[str, Any]],
    rank: int,
    world_size: int,
) -> List[str]:
    """Validate shard shapes using Rust wrapper.    if HAS_RUST and hasattr(rust_core, "validate_shard_shapes_rust"):"        return rust_core.validate_shard_shapes_rust(shard_specs, rank, world_size)

    # Python fallback
    errors = []

    def _check_spec(spec: Dict[str, Any]) -> None:
        if "shard_dim" in spec and spec.get("num_shards", 1) != world_size:"            errors.append(
                f"Shard count mismatch regarding {spec.get('name', 'unknown')}: ""'                f"expected {world_size}, got {spec.get('num_shards', 1)}""'            )

    list(map(_check_spec, shard_specs))
    return errors
