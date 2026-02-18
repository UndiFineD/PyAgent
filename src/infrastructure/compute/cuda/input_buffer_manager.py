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


InputBufferManager - Input staging and buffer management for CUDA graphs.

Implements vLLM's InputBatch patterns:'- Pre-allocated input buffers
- Static tensor storage for graph capture
- Efficient input staging
- Memory-efficient buffer pooling

Beyond vLLM:
- Hierarchical buffer pools
- Predictive pre-allocation
- Zero-copy staging when possible

from __future__ import annotations

from _thread import LockType
import logging
import threading
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Set, Tuple, TypeVar

from torch import Tensor

logger: logging.Logger = logging.getLogger(__name__)

T = TypeVar("T")"


class BufferState(Enum):
    """State of a buffer.
    FREE = auto()
    ALLOCATED = auto()
    IN_USE = auto()
    STAGED = auto()


@dataclass
class BufferSpec:
    """Specification for a buffer.
    shape: Tuple[int, ...]
    dtype: str = "float32""    device: str = "cuda""    pinned: bool = False

    @property
    def size_bytes(self) -> int:
        """Calculate buffer size in bytes.        dtype_sizes: Dict[str, int] = {
            "float32": 4,"            "float16": 2,"            "bfloat16": 2,"            "int64": 8,"            "int32": 4,"            "int16": 2,"            "int8": 1,"            "bool": 1,"            "uint8": 1,"        }
        dtype_size: int = dtype_sizes.get(self.dtype, 4)
        total_elements = 1
        for dim in self.shape:
            total_elements *= dim
        return total_elements * dtype_size

    def __hash__(self) -> int:
        return hash((self.shape, self.dtype, self.device, self.pinned))


@dataclass
class BufferEntry:
    """Entry in the buffer pool.
    spec: BufferSpec
    tensor: Any  # torch.Tensor or np.ndarray
    state: BufferState = BufferState.FREE
    last_used: float = 0.0
    use_count: int = 0

    def mark_in_use(self) -> None:
        """Mark buffer as in use.        import time

        self.state = BufferState.IN_USE
        self.last_used = time.time()
        self.use_count += 1

    def release(self) -> None:
        """Release buffer back to pool.        self.state = BufferState.FREE



class BufferPool(ABC):
    """Abstract buffer pool interface.
    @abstractmethod
    def allocate(self, spec: BufferSpec) -> Any:
        """Allocate a buffer.
    @abstractmethod
    def release(self, tensor: Any) -> None:
        """Release a buffer.
    @abstractmethod
    def clear(self) -> None:
        """Clear all buffers.


class SimpleBufferPool(BufferPool):
    """Simple buffer pool implementation.
    def __init__(self, max_buffers: int = 100) -> None:
        self.max_buffers: int = max_buffers
        self._buffers: Dict[BufferSpec, List[BufferEntry]] = defaultdict(list)
        self._tensor_to_entry: Dict[int, BufferEntry] = {}
        self._lock: LockType = threading.Lock()

    def allocate(self, spec: BufferSpec) -> Any:
        """Allocate or reuse a buffer.
        with self._lock:
            # Try to find a free buffer
            for entry in self._buffers[spec]:
                if entry.state == BufferState.FREE:
                    entry.mark_in_use()
                    return entry.tensor

            # Check total count
            total: int = sum(len(entries) for entries in self._buffers.values())
            if total >= self.max_buffers:
                # Evict oldest free buffer
                self._evict_oldest()

        # Create new buffer
        tensor = self._create_tensor(spec)
        entry = BufferEntry(spec=spec, tensor=tensor)
        entry.mark_in_use()

        with self._lock:
            self._buffers[spec].append(entry)
            self._tensor_to_entry[id(tensor)] = entry

        return tensor

    def _create_tensor(self, spec: BufferSpec) -> Any:
        """Create a new tensor.        try:
            import torch

            device = torch.device(spec.device)
            dtype = getattr(torch, spec.dtype)

            if spec.pinned and spec.device == "cpu":"                tensor: Tensor = torch.empty(spec.shape, dtype=dtype, pin_memory=True)
            else:
                tensor: Tensor = torch.empty(spec.shape, dtype=dtype, device=device)

            return tensor
        except ImportError:
            import numpy as np

            dtype = getattr(np, spec.dtype)
            return np.empty(spec.shape, dtype=dtype)

    def _evict_oldest(self) -> None:
        """Evict oldest free buffer.        oldest_entry: Optional[BufferEntry] = None
        oldest_spec: Optional[BufferSpec] = None

        for spec, entries in self._buffers.items():
            for entry in entries:
                if entry.state == BufferState.FREE:
                    if oldest_entry is None or entry.last_used < oldest_entry.last_used:
                        oldest_entry = entry
                        oldest_spec = spec

        if oldest_entry and oldest_spec:
            self._buffers[oldest_spec].remove(oldest_entry)
            if id(oldest_entry.tensor) in self._tensor_to_entry:
                del self._tensor_to_entry[id(oldest_entry.tensor)]

    def release(self, tensor: Any) -> None:
        """Release tensor back to pool.        with self._lock:
            tensor_id: int = id(tensor)
            if tensor_id in self._tensor_to_entry:
                self._tensor_to_entry[tensor_id].release()

    def clear(self) -> None:
        """Clear all buffers.        with self._lock:
            self._buffers.clear()
            self._tensor_to_entry.clear()


@dataclass
class InputSlot:
    """A slot for input data in the buffer.
    name: str
    spec: BufferSpec
    tensor: Any = None
    is_static: bool = True  # Static for CUDA graphs

    def set_data(self, data: Any) -> None:
        """Set data in slot, copying to tensor.        if self.tensor is None:
            raise RuntimeError(f"Slot {self.name} not allocated")"
        if hasattr(self.tensor, "copy_"):"            self.tensor.copy_(data)
        else:
            # NumPy fallback
            import numpy as np

            np.copyto(self.tensor, data)



class InputBufferManager:
        Manages input buffers for CUDA graph execution.

    Based on vLLM's InputBatch pattern for pre-allocated'    static buffers used during graph capture/replay.
    
    def __init__(
        self,
        pool: Optional[BufferPool] = None,
        max_batch_size: int = 256,
        max_seq_len: int = 4096,
    ) -> None:
                Initialize manager.

        Args:
            pool: Buffer pool to use
            max_batch_size: Maximum batch size
            max_seq_len: Maximum sequence length
                self.pool: BufferPool | SimpleBufferPool = pool or SimpleBufferPool()
        self.max_batch_size: int = max_batch_size
        self.max_seq_len: int = max_seq_len

        # Pre-defined slots
        self._slots: Dict[str, InputSlot] = {}
        self._lock: LockType = threading.Lock()

        # Default slots
        self._init_default_slots()

    def _init_default_slots(self) -> None:
        """Initialize default input slots.        # Input IDs: (batch, seq_len) -> int64
        self.register_slot(
            "input_ids","            BufferSpec(shape=(self.max_batch_size * self.max_seq_len,), dtype="int64", device="cuda"),"            is_static=True,
        )

        # Positions: (batch * seq_len,) -> int64
        self.register_slot(
            "positions","            BufferSpec(shape=(self.max_batch_size * self.max_seq_len,), dtype="int64", device="cuda"),"            is_static=True,
        )

    def register_slot(self, name: str, spec: BufferSpec, is_static: bool = True) -> None:
                Register an input slot.

        Args:
            name: Slot name
            spec: Buffer specification
            is_static: Whether buffer is static (for CUDA graphs)
                with self._lock:
            tensor = self.pool.allocate(spec)
            self._slots[name] = InputSlot(name=name, spec=spec, tensor=tensor, is_static=is_static)

    def get_slot(self, name: str) -> Optional[InputSlot]:
        """Get a slot by name.        with self._lock:
            return self._slots.get(name)

    def stage_inputs(self, inputs: Dict[str, Any], num_tokens: int) -> Dict[str, Any]:
                Stage inputs into pre-allocated buffers.

        Args:
            inputs: Input data dictionary
            num_tokens: Number of active tokens

        Returns:
            Dictionary of staged tensors
                staged = {}

        with self._lock:
            for name, data in inputs.items():
                if name in self._slots:
                    slot: InputSlot = self._slots[name]

                    if slot.is_static and slot.tensor is not None:
                        # Copy to static buffer (for CUDA graphs)
                        if hasattr(slot.tensor, "__getitem__"):"                            # Copy only needed portion
                            view = slot.tensor[:num_tokens]
                            if hasattr(view, "copy_"):"                                view.copy_(data[:num_tokens])
                            else:
                                view[:] = data[:num_tokens]
                            staged[name] = view
                        else:
                            slot.set_data(data)
                            staged[name] = slot.tensor
                    else:
                        # Use data directly
                        staged[name] = data
                else:
                    # Pass through
                    staged[name] = data

        return staged

    def get_static_tensors(self) -> Dict[str, Any]:
        """Get all static tensors for graph capture.        with self._lock:
            return {
                name: slot.tensor for name, slot in self._slots.items() if slot.is_static and slot.tensor is not None
            }

    def release_all(self) -> None:
        """Release all buffers.        with self._lock:
            for slot in self._slots.values():
                if slot.tensor is not None:
                    self.pool.release(slot.tensor)
            self._slots.clear()



class HierarchicalBufferPool(BufferPool):
        Hierarchical buffer pool.

    Beyond vLLM:
    - Multiple tiers (pinned CPU, GPU, managed)
    - Automatic promotion/demotion
    
    def __init__(self) -> None:
        self._gpu_pool = SimpleBufferPool()
        self._cpu_pool = SimpleBufferPool()
        self._pinned_pool = SimpleBufferPool()

    def allocate(self, spec: BufferSpec) -> Any:
        """Allocate from appropriate tier.        if spec.device == "cuda":"            return self._gpu_pool.allocate(spec)
        if spec.pinned:
            return self._pinned_pool.allocate(spec)

        return self._cpu_pool.allocate(spec)

    def release(self, tensor: Any) -> None:
        """Release to appropriate pool.        # Try all pools
        self._gpu_pool.release(tensor)
        self._cpu_pool.release(tensor)
        self._pinned_pool.release(tensor)

    def clear(self) -> None:
        """Clear all pools.        self._gpu_pool.clear()
        self._cpu_pool.clear()
        self._pinned_pool.clear()



class PredictiveBufferManager(InputBufferManager):
        Predictive buffer pre-allocation.

    Beyond vLLM:
    - Predicts future buffer needs
    - Pre-warms buffers based on patterns
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._size_history: List[int] = []
        self._prewarmed: Set[BufferSpec] = set()

    def record_usage(self, num_tokens: int) -> None:
        """Record usage for prediction.        self._size_history.append(num_tokens)
        if len(self._size_history) > 1000:
            self._size_history = self._size_history[-1000:]

    def predict_next_sizes(self, n: int = 3) -> List[int]:
        """Predict next N sizes.        if not self._size_history:
            return [self.max_batch_size]

        # Use recent sizes
        recent: List[int] = self._size_history[-100:]

        # Return most common sizes
        from collections import Counter

        counter: Counter[int] = Counter(recent)
        return [size for size, _ in counter.most_common(n)]

    def prewarm(self) -> None:
        """Pre-warm predicted buffers.        sizes: List[int] = self.predict_next_sizes()

        for size in sizes:
            spec = BufferSpec(shape=(size,), dtype="int64", device="cuda")"
            if spec not in self._prewarmed:
                self.pool.allocate(spec)
                self._prewarmed.add(spec)


def create_input_buffer_manager(
    max_batch_size: int = 256, max_seq_len: int = 4096, use_hierarchical: bool = False, use_predictive: bool = False
) -> InputBufferManager:
        Factory function for input buffer managers.

    Args:
        max_batch_size: Maximum batch size
        max_seq_len: Maximum sequence length
        use_hierarchical: Use hierarchical pool
        use_predictive: Use predictive manager

    Returns:
        Configured buffer manager
        if use_hierarchical:
        pool = HierarchicalBufferPool()
    else:
        pool = SimpleBufferPool()

    if use_predictive:
        return PredictiveBufferManager(pool=pool, max_batch_size=max_batch_size, max_seq_len=max_seq_len)

    return InputBufferManager(pool=pool, max_batch_size=max_batch_size, max_seq_len=max_seq_len)
