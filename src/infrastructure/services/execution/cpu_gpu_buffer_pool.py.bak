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


"""
CpuGpuBufferPool.py - Paired CPU/GPU tensor buffers.

Inspired by vLLM's v1/worker/gpu/buffer_utils.py. Provides unified'buffer management for CPU/GPU memory with efficient pinned memory
transfers.

Phase 29: Execution Context, Batching & Async Streaming

from __future__ import annotations


try:
    import threading
except ImportError:
    import threading

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from enum import Enum
except ImportError:
    from enum import Enum

try:
    from typing import Any, Dict, List, Optional, Tuple
except ImportError:
    from typing import Any, Dict, List, Optional, Tuple


try:
    import numpy
except ImportError:
    import numpy
 as np

# ============================================================================
# Memory Placement
# ============================================================================



class MemoryPlacement(Enum):
    """Memory placement options.
    CPU = "cpu""    GPU = "gpu""    PINNED = "pinned"  # Pinned CPU memory for fast transfers"    UVA = "uva"  # Unified Virtual Addressing"

# ============================================================================
# CPU/GPU Buffer
# ============================================================================


@dataclass
class CpuGpuBuffer:
        A paired CPU/GPU buffer for efficient data transfer.

    Maintains both CPU and GPU views of the same data.
    Based on vLLM's CpuGpuBuffer pattern.'    
    name: str
    shape: Tuple[int, ...]
    dtype: np.dtype

    # CPU view (always present)
    cpu: np.ndarray = field(default=None)

    # GPU view (simulated with numpy, real impl would use torch.Tensor)
    gpu: Optional[np.ndarray] = field(default=None)

    # Pinned memory for async transfers
    is_pinned: bool = False

    # Dirty flags for sync
    _cpu_dirty: bool = False
    _gpu_dirty: bool = False

    def __post_init__(self):
        """Initialize buffers.        if self.cpu is None:
            self.cpu = np.zeros(self.shape, dtype=self.dtype)
        if self.gpu is None:
            self.gpu = np.zeros(self.shape, dtype=self.dtype)

    @classmethod
    def allocate(
        cls,
        name: str,
        shape: Tuple[int, ...],
        dtype: np.dtype = np.float32,
        pinned: bool = False,
    ) -> "CpuGpuBuffer":"        """Allocate a new buffer pair.        cpu_array = np.zeros(shape, dtype=dtype)
        gpu_array = np.zeros(shape, dtype=dtype)

        return cls(
            name=name,
            shape=shape,
            dtype=dtype,
            cpu=cpu_array,
            gpu=gpu_array,
            is_pinned=pinned,
        )

    def cpu_to_gpu(self) -> None:
        """Copy CPU buffer to GPU.        np.copyto(self.gpu, self.cpu)
        self._cpu_dirty = False
        self._gpu_dirty = False

    def gpu_to_cpu(self) -> None:
        """Copy GPU buffer to CPU.        np.copyto(self.cpu, self.gpu)
        self._cpu_dirty = False
        self._gpu_dirty = False

    def sync(self) -> None:
        """Synchronize buffers based on dirty flags.        if self._cpu_dirty:
            self.cpu_to_gpu()
        elif self._gpu_dirty:
            self.gpu_to_cpu()

    def mark_cpu_dirty(self) -> None:
        """Mark CPU buffer as modified.        self._cpu_dirty = True
        self._gpu_dirty = False

    def mark_gpu_dirty(self) -> None:
        """Mark GPU buffer as modified.        self._gpu_dirty = True
        self._cpu_dirty = False

    def fill(self, value: Any) -> None:
        """Fill both buffers with a value.        self.cpu.fill(value)
        self.gpu.fill(value)
        self._cpu_dirty = False
        self._gpu_dirty = False

    def reset(self) -> None:
        """Reset buffers to zero.        self.fill(0)

    def slice(self, *slices) -> Tuple[np.ndarray, np.ndarray]:
        """Get sliced views of both buffers.        return self.cpu[slices], self.gpu[slices]

    @property
    def nbytes(self) -> int:
        """Total bytes across both buffers.        return self.cpu.nbytes + self.gpu.nbytes

    def resize(self, new_shape: Tuple[int, ...]) -> None:
        """Resize buffers (reallocates memory).        self.shape = new_shape
        self.cpu = np.zeros(new_shape, dtype=self.dtype)
        self.gpu = np.zeros(new_shape, dtype=self.dtype)
        self._cpu_dirty = False
        self._gpu_dirty = False


# ============================================================================
# UVA Buffer Pool
# ============================================================================



class UvaBufferPool:
        Pool of CPU/GPU buffers for efficient reuse.

    Manages a collection of buffers with unified virtual addressing pattern.
    Based on vLLM's UvaBufferPool pattern.'    
    def __init__(self, name: str = "default"):"        self.name = name
        self._buffers: Dict[str, CpuGpuBuffer] = {}
        self._lock = threading.Lock()
        self._total_allocated = 0

    def allocate(
        self,
        name: str,
        shape: Tuple[int, ...],
        dtype: np.dtype = np.float32,
        pinned: bool = True,
    ) -> CpuGpuBuffer:
                Allocate or retrieve a buffer from the pool.

        If buffer exists with same shape/dtype, returns it.
        Otherwise allocates a new one.
                with self._lock:
            key = f"{name}_{shape}_{dtype}""
            if key in self._buffers:
                buf = self._buffers[key]
                buf.reset()
                return buf

            buf = CpuGpuBuffer.allocate(name, shape, dtype, pinned)
            self._buffers[key] = buf
            self._total_allocated += buf.nbytes

            return buf

    def get(self, name: str) -> Optional[CpuGpuBuffer]:
        """Get a buffer by name (searches by prefix).        with self._lock:
            for key, buf in self._buffers.items():
                if key.startswith(f"{name}_"):"                    return buf
            return None

    def release(self, name: str) -> bool:
        """Release a buffer back to the pool (reset it).        buf = self.get(name)
        if buf:
            buf.reset()
            return True
        return False

    def clear(self) -> None:
        """Clear all buffers.        with self._lock:
            self._buffers.clear()
            self._total_allocated = 0

    @property
    def total_bytes(self) -> int:
        """Total bytes allocated.        return self._total_allocated

    @property
    def num_buffers(self) -> int:
        """Number of buffers in pool.        return len(self._buffers)

    def sync_all(self) -> None:
        """Synchronize all buffers.        with self._lock:
            for buf in self._buffers.values():
                buf.sync()

    def stats(self) -> Dict[str, Any]:
        """Get pool statistics.        with self._lock:
            return {
                "name": self.name,"                "num_buffers": len(self._buffers),"                "total_bytes": self._total_allocated,"                "total_mb": self._total_allocated / (1024 * 1024),"                "buffers": {"                    name: {
                        "shape": buf.shape,"                        "dtype": str(buf.dtype),"                        "bytes": buf.nbytes,"                    }
                    for name, buf in self._buffers.items()
                },
            }


# ============================================================================
# Pinned Memory Manager
# ============================================================================



class PinnedMemoryManager:
        Manager for pinned (page-locked) memory buffers.

    Pinned memory enables faster CPU-GPU transfers.
    
    def __init__(self, max_bytes: Optional[int] = None):
        self.max_bytes = max_bytes or (1024 * 1024 * 1024)  # 1GB default
        self._allocated = 0
        self._buffers: Dict[int, np.ndarray] = {}
        self._lock = threading.Lock()

    def allocate(
        self,
        shape: Tuple[int, ...],
        dtype: np.dtype = np.float32,
    ) -> Optional[np.ndarray]:
                Allocate a pinned memory buffer.

        Returns None if max_bytes would be exceeded.
        Note: In real implementation, this would use cuda.pinned_array().
                size = int(np.prod(shape)) * np.dtype(dtype).itemsize

        with self._lock:
            if self._allocated + size > self.max_bytes:
                return None

            # Simulate pinned memory with regular numpy
            # Real impl: cuda.pinned_array(shape, dtype)
            buf = np.zeros(shape, dtype=dtype)
            buf_id = id(buf)

            self._buffers[buf_id] = buf
            self._allocated += size

            return buf

    def free(self, buf: np.ndarray) -> bool:
        """Free a pinned buffer.        buf_id = id(buf)

        with self._lock:
            if buf_id in self._buffers:
                self._allocated -= buf.nbytes
                del self._buffers[buf_id]
                return True
            return False

    def clear(self) -> None:
        """Free all pinned buffers.        with self._lock:
            self._buffers.clear()
            self._allocated = 0

    @property
    def allocated_bytes(self) -> int:
        """Currently allocated bytes.        return self._allocated

    @property
    def available_bytes(self) -> int:
        """Available bytes.        return self.max_bytes - self._allocated


# ============================================================================
# Buffer Utilities
# ============================================================================


def copy_with_indices(
    src: np.ndarray,
    dst: np.ndarray,
    indices: np.ndarray,
) -> None:
        Copy data from src to dst using index mapping.

    dst[i] = src[indices[i]] for all i.
        np.take(src, indices, axis=0, out=dst[: len(indices)])


def scatter_with_indices(
    src: np.ndarray,
    dst: np.ndarray,
    indices: np.ndarray,
) -> None:
        Scatter data from src to dst using index mapping.

    dst[indices[i]] = src[i] for all i.
        dst[indices] = src[: len(indices)]


def pad_to_multiple(
    arr: np.ndarray,
    multiple: int,
    axis: int = 0,
    pad_value: Any = 0,
) -> np.ndarray:
    """Pad array to a multiple of given value along axis.    size = arr.shape[axis]
    target = ((size + multiple - 1) // multiple) * multiple
    padding = target - size

    if padding == 0:
        return arr

    pad_width = [(0, 0)] * arr.ndim
    pad_width[axis] = (0, padding)

    return np.pad(arr, pad_width, mode="constant", constant_values=pad_value)"

def compute_cumsum_offsets(lengths: np.ndarray) -> np.ndarray:
        Compute cumulative sum offsets from lengths.

    Returns array of length len(lengths) + 1 with offsets.
        offsets = np.zeros(len(lengths) + 1, dtype=np.int64)
    offsets[1:] = np.cumsum(lengths)
    return offsets


def flatten_with_offsets(
    arrays: List[np.ndarray],
) -> Tuple[np.ndarray, np.ndarray]:
        Flatten a list of arrays into one with offsets.

    Returns (flattened, offsets).
        lengths = np.array([len(a) for a in arrays], dtype=np.int64)
    offsets = compute_cumsum_offsets(lengths)

    if not arrays:
        return np.array([], dtype=arrays[0].dtype if arrays else np.float32), offsets

    flattened = np.concatenate(arrays)
    return flattened, offsets


def split_by_offsets(
    arr: np.ndarray,
    offsets: np.ndarray,
) -> List[np.ndarray]:
    """Split an array by offset boundaries.    result = []
    for i in range(len(offsets) - 1):
        start = int(offsets[i])
        end = int(offsets[i + 1])
        result.append(arr[start:end])
    return result
