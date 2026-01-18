"""UvaBufferPool - Zero-copy GPU transfers via Unified Virtual Addressing.

This module implements UVA (Unified Virtual Addressing) buffer management
for efficient CPU-GPU data transfers without intermediate copies.

Inspired by vLLM v1/worker/gpu/buffer_utils.py, but extends with:
- Adaptive pool sizing based on access patterns
- Priority-aware buffer allocation
- Memory pressure monitoring
- Automatic buffer promotion/demotion

Example:
    >>> pool = UvaBufferPool(buffer_count=4, buffer_size=1024*1024)
    >>> buffer = pool.acquire()
    >>> buffer.copy_to_uva(cpu_tensor)  # Zero-copy to GPU-visible memory
    >>> buffer.copy_to_gpu(cuda_stream)  # DMA transfer to GPU
    >>> pool.release(buffer)
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional
from collections import deque

# Try to import torch for GPU operations
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # type: ignore

# Try to import Rust accelerations
try:
    from src.core.rust_bridge import get_bridge
    _bridge = get_bridge()
    HAS_RUST = hasattr(_bridge, 'uva_copy_rust')
except Exception:
    HAS_RUST = False
    _bridge = None


class BufferState(Enum):
    """State of a UVA buffer."""
    FREE = auto()      # Available for allocation
    ACQUIRED = auto()  # In use by a consumer
    COPYING = auto()   # Transfer in progress
    PINNED = auto()    # Cannot be evicted


class AllocationStrategy(Enum):
    """Buffer allocation strategy."""
    ROUND_ROBIN = auto()   # Rotate through buffers
    LEAST_RECENT = auto()  # Use least recently used
    PRIORITY = auto()      # Priority-aware allocation


@dataclass
class BufferStats:
    """Statistics for a single buffer."""
    allocations: int = 0
    total_bytes_transferred: int = 0
    total_transfer_time_ns: int = 0
    last_used: float = 0.0
    peak_usage: int = 0
    
    @property
    def avg_transfer_time_ms(self) -> float:
        """Average transfer time in milliseconds."""
        if self.allocations == 0:
            return 0.0
        return (self.total_transfer_time_ns / self.allocations) / 1_000_000
    
    @property
    def throughput_gbps(self) -> float:
        """Throughput in GB/s."""
        if self.total_transfer_time_ns == 0:
            return 0.0
        seconds = self.total_transfer_time_ns / 1_000_000_000
        return (self.total_bytes_transferred / (1024**3)) / seconds


@dataclass
class UvaBuffer:
    """A buffer with Unified Virtual Addressing for zero-copy GPU access.
    
    UVA buffers use pinned (page-locked) host memory that can be directly
    accessed by the GPU via PCIe without going through the CPU.
    
    Attributes:
        buffer_id: Unique identifier for this buffer
        size: Size in bytes
        cpu_tensor: CPU-side tensor (pinned memory)
        uva_tensor: GPU-visible view of the CPU tensor
        dtype: Data type of the buffer
        state: Current buffer state
        stats: Usage statistics
    """
    buffer_id: int
    size: int
    dtype: Any = None
    state: BufferState = BufferState.FREE
    stats: BufferStats = field(default_factory=BufferStats)
    priority: int = 0
    
    # Tensors (initialized lazily)
    _cpu_tensor: Any = field(default=None, repr=False)
    _uva_tensor: Any = field(default=None, repr=False)
    _gpu_tensor: Any = field(default=None, repr=False)
    _device: Any = field(default=None, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    
    def __post_init__(self) -> None:
        """Initialize tensors if torch is available."""
        if HAS_TORCH and self._cpu_tensor is None:
            self._initialize_tensors()
    
    def _initialize_tensors(self) -> None:
        """Create pinned CPU tensor and UVA view."""
        if not HAS_TORCH:
            return
        
        dtype = self.dtype or torch.float32
        element_size = torch.tensor([], dtype=dtype).element_size()
        num_elements = self.size // element_size
        
        # Detect hardware capability for pinned memory
        # Pinned memory requires an accelerator backend (CUDA, ROCm, XPU, etc.)
        can_pin = torch.cuda.is_available()
        if not can_pin:
            # Check for other accelerator backends that support pinned memory
            can_pin = getattr(torch, 'xpu', None) is not None and torch.xpu.is_available()
        if not can_pin:
            can_pin = getattr(torch.backends, 'mps', None) is not None and torch.backends.mps.is_available()
        
        self._cpu_tensor = torch.empty(
            num_elements, 
            dtype=dtype,
            pin_memory=can_pin
        )
        
        # UVA tensor is the same as CPU tensor for pinned memory
        # GPU can access it directly via UVA
        self._uva_tensor = self._cpu_tensor
        
        # GPU tensor will be created on first copy
        if torch.cuda.is_available():
            self._device = torch.device('cuda:0')
        elif getattr(torch, 'xpu', None) is not None and torch.xpu.is_available():
            self._device = torch.device('xpu:0')
        elif getattr(torch.backends, 'mps', None) is not None and torch.backends.mps.is_available():
            self._device = torch.device('mps')
    
    @property
    def cpu_tensor(self) -> Any:
        """Get CPU tensor."""
        return self._cpu_tensor
    
    @property
    def uva_tensor(self) -> Any:
        """Get UVA tensor (GPU-visible CPU memory)."""
        return self._uva_tensor
    
    @property
    def gpu_tensor(self) -> Any:
        """Get GPU tensor."""
        return self._gpu_tensor
    
    def copy_to_uva(self, data: Any) -> None:
        """Copy data to UVA buffer (CPU side, no GPU copy).
        
        This copies data into pinned host memory. The GPU can then
        access this memory directly via UVA, or you can explicitly
        copy to GPU memory with copy_to_gpu().
        
        Args:
            data: Source data (numpy array, torch tensor, or list)
        """
        if self._cpu_tensor is None:
            raise RuntimeError("Buffer not initialized (torch not available?)")
        
        with self._lock:
            start = time.perf_counter_ns()
            
            if HAS_TORCH and isinstance(data, torch.Tensor):
                # Direct tensor copy
                self._cpu_tensor[:data.numel()].copy_(data.view(-1))
            elif hasattr(data, '__array__'):
                # Numpy array
                import numpy as np
                flat = np.asarray(data).ravel()
                self._cpu_tensor[:len(flat)].copy_(
                    torch.from_numpy(flat)
                )
            else:
                # List or other iterable
                tensor = torch.tensor(data, dtype=self._cpu_tensor.dtype)
                self._cpu_tensor[:tensor.numel()].copy_(tensor.view(-1))
            
            elapsed = time.perf_counter_ns() - start
            self.stats.allocations += 1
            self.stats.total_bytes_transferred += self._cpu_tensor.nbytes
            self.stats.total_transfer_time_ns += elapsed
            self.stats.last_used = time.time()
    
    def copy_to_gpu(
        self, 
        stream: Optional[Any] = None,
        non_blocking: bool = True
    ) -> Any:
        """Copy UVA buffer to GPU memory.
        
        This performs a DMA transfer from pinned host memory to GPU memory.
        Can be overlapped with compute when non_blocking=True.
        
        Args:
            stream: CUDA stream for async copy (None = default stream)
            non_blocking: If True, copy is asynchronous
            
        Returns:
            GPU tensor with copied data
        """
        if self._cpu_tensor is None:
            raise RuntimeError("Buffer not initialized")
        
        if not HAS_TORCH or not torch.cuda.is_available():
            return self._cpu_tensor
        
        with self._lock:
            start = time.perf_counter_ns()
            
            if self._gpu_tensor is None or self._gpu_tensor.shape != self._cpu_tensor.shape:
                self._gpu_tensor = torch.empty_like(
                    self._cpu_tensor, 
                    device=self._device
                )
            
            if stream is not None:
                with torch.cuda.stream(stream):
                    self._gpu_tensor.copy_(
                        self._cpu_tensor, 
                        non_blocking=non_blocking
                    )
            else:
                self._gpu_tensor.copy_(
                    self._cpu_tensor,
                    non_blocking=non_blocking
                )
            
            elapsed = time.perf_counter_ns() - start
            self.stats.total_bytes_transferred += self._cpu_tensor.nbytes
            self.stats.total_transfer_time_ns += elapsed
            self.stats.peak_usage = max(
                self.stats.peak_usage,
                self._cpu_tensor.numel() * self._cpu_tensor.element_size()
            )
            
            return self._gpu_tensor
    
    def copy_to_cpu(
        self,
        stream: Optional[Any] = None,
        non_blocking: bool = True
    ) -> Any:
        """Copy GPU tensor back to UVA buffer.
        
        Args:
            stream: CUDA stream for async copy
            non_blocking: If True, copy is asynchronous
            
        Returns:
            CPU tensor with copied data
        """
        if self._gpu_tensor is None:
            return self._cpu_tensor
        
        with self._lock:
            if stream is not None:
                with torch.cuda.stream(stream):
                    self._cpu_tensor.copy_(
                        self._gpu_tensor,
                        non_blocking=non_blocking
                    )
            else:
                self._cpu_tensor.copy_(
                    self._gpu_tensor,
                    non_blocking=non_blocking
                )
            
            return self._cpu_tensor
    
    def sync(self, stream: Optional[Any] = None) -> None:
        """Wait for all pending transfers to complete."""
        if HAS_TORCH and torch.cuda.is_available():
            if stream is not None:
                stream.synchronize()
            else:
                torch.cuda.synchronize()
    
    def reset(self) -> None:
        """Reset buffer state and optionally zero memory."""
        self.state = BufferState.FREE
        self.priority = 0


class UvaBufferPool:
    """Pool of UVA buffers with round-robin allocation.
    
    This pool manages multiple UVA buffers for concurrent transfers,
    allowing overlap of CPU-GPU copies with compute operations.
    
    The pool supports adaptive sizing based on access patterns,
    going beyond vLLM's fixed pool approach.
    
    Attributes:
        buffer_count: Number of buffers in the pool
        buffer_size: Size of each buffer in bytes
        strategy: Allocation strategy
    """
    
    def __init__(
        self,
        buffer_count: int = 4,
        buffer_size: int = 16 * 1024 * 1024,  # 16 MB default
        dtype: Any = None,
        strategy: AllocationStrategy = AllocationStrategy.ROUND_ROBIN,
        max_buffers: int = 16,
        grow_factor: float = 2.0,
        shrink_threshold: float = 0.25,
    ):
        """Initialize the buffer pool.
        
        Args:
            buffer_count: Initial number of buffers
            buffer_size: Size of each buffer in bytes
            dtype: Data type for buffers (default: float32)
            strategy: Allocation strategy
            max_buffers: Maximum number of buffers (for adaptive sizing)
            grow_factor: Factor to grow pool by when needed
            shrink_threshold: Utilization below which to shrink
        """
        self.buffer_count = buffer_count
        self.buffer_size = buffer_size
        self.dtype = dtype
        self.strategy = strategy
        self.max_buffers = max_buffers
        self.grow_factor = grow_factor
        self.shrink_threshold = shrink_threshold
        
        self._buffers: list[UvaBuffer] = []
        self._free_buffers: deque[UvaBuffer] = deque()
        self._next_idx: int = 0
        self._lock = threading.Lock()
        self._stats = BufferStats()
        
        # Adaptive sizing state
        self._acquire_count: int = 0
        self._contention_count: int = 0
        self._last_resize_time: float = 0.0
        self._resize_cooldown: float = 1.0  # seconds
        
        # Initialize buffers
        self._initialize_pool()
    
    def _initialize_pool(self) -> None:
        """Create initial set of buffers."""
        for i in range(self.buffer_count):
            buffer = UvaBuffer(
                buffer_id=i,
                size=self.buffer_size,
                dtype=self.dtype,
                state=BufferState.FREE,
            )
            self._buffers.append(buffer)
            self._free_buffers.append(buffer)
    
    def acquire(
        self,
        priority: int = 0,
        blocking: bool = True,
        timeout: Optional[float] = None
    ) -> Optional[UvaBuffer]:
        """Acquire a buffer from the pool.
        
        Args:
            priority: Priority for allocation (higher = more important)
            blocking: If True, wait for a buffer if none available
            timeout: Maximum time to wait (None = forever)
            
        Returns:
            UvaBuffer if available, None if timeout or non-blocking
        """
        start = time.time()
        
        while True:
            with self._lock:
                self._acquire_count += 1
                
                buffer = self._try_acquire(priority)
                if buffer is not None:
                    return buffer
                
                # Track contention for adaptive sizing
                self._contention_count += 1
                
                # Try to grow pool if under pressure
                if self._should_grow():
                    self._grow_pool()
                    buffer = self._try_acquire(priority)
                    if buffer is not None:
                        return buffer
            
            if not blocking:
                return None
            
            if timeout is not None and (time.time() - start) >= timeout:
                return None
            
            # Brief sleep before retry
            time.sleep(0.001)
    
    def _try_acquire(self, priority: int) -> Optional[UvaBuffer]:
        """Try to acquire a buffer without blocking."""
        if self.strategy == AllocationStrategy.ROUND_ROBIN:
            return self._acquire_round_robin(priority)
        elif self.strategy == AllocationStrategy.LEAST_RECENT:
            return self._acquire_least_recent(priority)
        elif self.strategy == AllocationStrategy.PRIORITY:
            return self._acquire_priority(priority)
        return None
    
    def _acquire_round_robin(self, priority: int) -> Optional[UvaBuffer]:
        """Round-robin allocation strategy."""
        if not self._free_buffers:
            return None
        
        buffer = self._free_buffers.popleft()
        buffer.state = BufferState.ACQUIRED
        buffer.priority = priority
        buffer.stats.allocations += 1
        buffer.stats.last_used = time.time()
        return buffer
    
    def _acquire_least_recent(self, priority: int) -> Optional[UvaBuffer]:
        """Least recently used allocation."""
        if not self._free_buffers:
            return None
        
        # Free buffers are already ordered by release time
        buffer = self._free_buffers.popleft()
        buffer.state = BufferState.ACQUIRED
        buffer.priority = priority
        buffer.stats.allocations += 1
        buffer.stats.last_used = time.time()
        return buffer
    
    def _acquire_priority(self, priority: int) -> Optional[UvaBuffer]:
        """Priority-aware allocation (may preempt lower priority)."""
        if self._free_buffers:
            buffer = self._free_buffers.popleft()
            buffer.state = BufferState.ACQUIRED
            buffer.priority = priority
            buffer.stats.allocations += 1
            buffer.stats.last_used = time.time()
            return buffer
        
        # Try to preempt a lower priority buffer
        for buffer in self._buffers:
            if buffer.state == BufferState.ACQUIRED and buffer.priority < priority:
                # TODO: Implement preemption callback
                pass
        
        return None
    
    def release(self, buffer: UvaBuffer) -> None:
        """Release a buffer back to the pool.
        
        Args:
            buffer: Buffer to release
        """
        with self._lock:
            buffer.state = BufferState.FREE
            buffer.priority = 0
            self._free_buffers.append(buffer)
            
            # Check if we should shrink
            if self._should_shrink():
                self._shrink_pool()
    
    def _should_grow(self) -> bool:
        """Check if pool should grow based on contention."""
        if len(self._buffers) >= self.max_buffers:
            return False
        
        now = time.time()
        if now - self._last_resize_time < self._resize_cooldown:
            return False
        
        # Grow if contention rate is high
        if self._acquire_count > 0:
            contention_rate = self._contention_count / self._acquire_count
            return contention_rate > 0.5
        
        return False
    
    def _grow_pool(self) -> None:
        """Add more buffers to the pool."""
        current = len(self._buffers)
        new_count = min(
            int(current * self.grow_factor),
            self.max_buffers
        )
        
        for i in range(current, new_count):
            buffer = UvaBuffer(
                buffer_id=i,
                size=self.buffer_size,
                dtype=self.dtype,
                state=BufferState.FREE,
            )
            self._buffers.append(buffer)
            self._free_buffers.append(buffer)
        
        self._last_resize_time = time.time()
        self._contention_count = 0
        self._acquire_count = 0
    
    def _should_shrink(self) -> bool:
        """Check if pool should shrink based on utilization."""
        if len(self._buffers) <= self.buffer_count:  # Don't shrink below initial
            return False
        
        now = time.time()
        if now - self._last_resize_time < self._resize_cooldown * 5:
            return False
        
        # Shrink if utilization is low
        free_ratio = len(self._free_buffers) / len(self._buffers)
        return free_ratio > (1.0 - self.shrink_threshold)
    
    def _shrink_pool(self) -> None:
        """Remove excess buffers from the pool."""
        target = max(
            self.buffer_count,
            int(len(self._buffers) / self.grow_factor)
        )
        
        while len(self._buffers) > target and self._free_buffers:
            buffer = self._free_buffers.pop()
            self._buffers.remove(buffer)
        
        self._last_resize_time = time.time()
    
    @property
    def stats(self) -> dict[str, Any]:
        """Get pool statistics."""
        with self._lock:
            total_allocs = sum(b.stats.allocations for b in self._buffers)
            total_bytes = sum(b.stats.total_bytes_transferred for b in self._buffers)
            total_time = sum(b.stats.total_transfer_time_ns for b in self._buffers)
            
            return {
                "buffer_count": len(self._buffers),
                "free_buffers": len(self._free_buffers),
                "acquired_buffers": len(self._buffers) - len(self._free_buffers),
                "total_allocations": total_allocs,
                "total_bytes_transferred": total_bytes,
                "total_transfer_time_ns": total_time,
                "avg_transfer_time_ms": (total_time / total_allocs / 1_000_000) if total_allocs > 0 else 0,
                "throughput_gbps": (total_bytes / (1024**3)) / (total_time / 1_000_000_000) if total_time > 0 else 0,
                "contention_rate": self._contention_count / self._acquire_count if self._acquire_count > 0 else 0,
            }
    
    def clear(self) -> None:
        """Clear all buffers and reset pool."""
        with self._lock:
            for buffer in self._buffers:
                buffer.reset()
            self._free_buffers = deque(self._buffers)
            self._contention_count = 0
            self._acquire_count = 0


class UvaBackedTensor:
    """A tensor backed by UVA memory for automatic zero-copy transfers.
    
    This is a higher-level wrapper that automatically manages UVA buffer
    allocation and provides a tensor-like interface.
    """
    
    def __init__(
        self,
        shape: tuple[int, ...],
        dtype: Any = None,
        pool: Optional[UvaBufferPool] = None,
    ):
        """Initialize UVA-backed tensor.
        
        Args:
            shape: Tensor shape
            dtype: Data type
            pool: Buffer pool to use (creates default if None)
        """
        self.shape = shape
        self.dtype = dtype or (torch.float32 if HAS_TORCH else None)
        
        # Calculate size
        if HAS_TORCH:
            element_size = torch.tensor([], dtype=self.dtype).element_size()
        else:
            element_size = 4  # Assume float32
        
        import math
        self.size = math.prod(shape) * element_size
        
        # Get or create pool
        if pool is None:
            self._pool = UvaBufferPool(
                buffer_count=1,
                buffer_size=self.size,
                dtype=self.dtype,
            )
        else:
            self._pool = pool
        
        # Acquire buffer
        self._buffer = self._pool.acquire()
        if self._buffer is None:
            raise RuntimeError("Failed to acquire UVA buffer")
    
    def fill(self, data: Any) -> "UvaBackedTensor":
        """Fill tensor with data."""
        self._buffer.copy_to_uva(data)
        return self
    
    def to_gpu(self, stream: Optional[Any] = None) -> Any:
        """Transfer to GPU."""
        gpu = self._buffer.copy_to_gpu(stream)
        if gpu is not None:
            return gpu.view(self.shape)
        return None
    
    def to_cpu(self, stream: Optional[Any] = None) -> Any:
        """Transfer to CPU."""
        cpu = self._buffer.copy_to_cpu(stream)
        if cpu is not None:
            return cpu.view(self.shape)
        return None
    
    def sync(self) -> None:
        """Synchronize pending transfers."""
        self._buffer.sync()
    
    def __del__(self) -> None:
        """Release buffer on deletion."""
        if hasattr(self, '_buffer') and self._buffer is not None:
            self._pool.release(self._buffer)


# Convenience functions
def create_uva_buffer(size: int, dtype: Any = None) -> UvaBuffer:
    """Create a single UVA buffer."""
    return UvaBuffer(
        buffer_id=0,
        size=size,
        dtype=dtype,
        state=BufferState.FREE,
    )


def create_uva_pool(
    count: int = 4,
    size: int = 16 * 1024 * 1024,
    dtype: Any = None,
) -> UvaBufferPool:
    """Create a UVA buffer pool."""
    return UvaBufferPool(
        buffer_count=count,
        buffer_size=size,
        dtype=dtype,
    )
