"""
GPUMemoryAllocator: GPU memory optimization with sleep/wake and pooling.

vLLM Pattern: CuMemAllocator from v1/core/gpu_memory/cumem.py
- sleep() / wake_up() for GPU memory sharing
- use_memory_pool() context manager
- MemorySnapshot for state capture/restore

Beyond vLLM:
- Multi-GPU memory balancing
- Memory pressure detection and response
- Automatic fragmentation management
"""

from __future__ import annotations
import logging
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Generator, Optional, Dict, List
import weakref

logger = logging.getLogger(__name__)


class MemoryState(Enum):
    """GPU memory allocator state."""
    ACTIVE = auto()       # Normal operation
    SLEEPING = auto()     # Memory released for sharing
    SNAPSHOT = auto()     # Snapshot in progress


class AllocationStrategy(Enum):
    """Memory allocation strategy."""
    BEST_FIT = auto()     # Minimize fragmentation
    FIRST_FIT = auto()    # Fast allocation
    POOL = auto()         # Fixed-size pool
    BUDDY = auto()        # Buddy system


@dataclass
class MemoryRegion:
    """A memory region/allocation."""
    region_id: int
    size_bytes: int
    offset: int = 0
    device_id: int = 0
    is_free: bool = True
    allocation_time: float = field(default_factory=time.time)
    last_access: float = field(default_factory=time.time)
    ref_count: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def touch(self) -> None:
        """Update last access time."""
        self.last_access = time.time()


@dataclass
class MemorySnapshot:
    """
    Snapshot of GPU memory state.

    vLLM Pattern: MemorySnapshot for state capture/restore
    """
    snapshot_id: int
    device_id: int
    timestamp: float = field(default_factory=time.time)
    total_bytes: int = 0
    allocated_bytes: int = 0
    free_bytes: int = 0
    num_allocations: int = 0
    fragmentation_ratio: float = 0.0
    region_states: dict[int, bool] = field(default_factory=dict)  # region_id -> is_free

    def to_dict(self) -> dict[str, Any]:
        """Serialize snapshot to dict."""
        return {
            "snapshot_id": self.snapshot_id,
            "device_id": self.device_id,
            "timestamp": self.timestamp,
            "total_bytes": self.total_bytes,
            "allocated_bytes": self.allocated_bytes,
            "free_bytes": self.free_bytes,
            "num_allocations": self.num_allocations,
            "fragmentation_ratio": self.fragmentation_ratio,
        }


@dataclass
class MemoryPoolConfig:
    """Configuration for memory pool."""
    pool_size_bytes: int = 8 * 1024 * 1024 * 1024  # 8GB default
    block_size_bytes: int = 2 * 1024 * 1024        # 2MB blocks
    device_id: int = 0
    strategy: AllocationStrategy = AllocationStrategy.POOL
    enable_defrag: bool = True
    low_memory_threshold: float = 0.1  # 10% free triggers pressure
    sleep_release_ratio: float = 0.5   # Release 50% on sleep


class MemoryPressureEvent:
    """Event for memory pressure notifications."""

    def __init__(self, device_id: int, available_bytes: int, total_bytes: int):
        self.device_id = device_id
        self.available_bytes = available_bytes
        self.total_bytes = total_bytes
        self.timestamp = time.time()
        self.pressure_ratio = 1.0 - (available_bytes / total_bytes) if total_bytes > 0 else 1.0


class CuMemAllocator:
    """
    Custom CUDA memory allocator with sleep/wake support.

    vLLM Pattern: CuMemAllocator from cumem.py

    Beyond vLLM:
    - Multi-GPU memory balancing
    - Pressure-aware allocation
    - Automatic defragmentation
    """

    def __init__(self, config: Optional[MemoryPoolConfig] = None):
        self.config = config or MemoryPoolConfig()
        self._state = MemoryState.ACTIVE

        # Memory regions
        self._regions: dict[int, MemoryRegion] = {}
        self._next_region_id = 0

        # Free list (sorted by size for best-fit)
        self._free_regions: list[int] = []

        # Allocated tracking
        self._allocated_bytes = 0

        # Snapshot management
        self._snapshots: dict[int, MemorySnapshot] = {}
        self._next_snapshot_id = 0

        # Callbacks
        self._allocation_callbacks: list[Callable[[int, int], None]] = []
        self._deallocation_callbacks: list[Callable[[int, int], None]] = []
        self._pressure_callbacks: list[Callable[[MemoryPressureEvent], None]] = []

        # Initialize pool
        self._init_pool()

        self._lock = threading.RLock()

        logger.info(f"CuMemAllocator initialized: {self.config.pool_size_bytes / (1024**3):.1f}GB")

    def _init_pool(self) -> None:
        """Initialize memory pool with free regions."""
        if self.config.strategy == AllocationStrategy.POOL:
            # Fixed-size blocks
            num_blocks = self.config.pool_size_bytes // self.config.block_size_bytes
            for i in range(num_blocks):
                region = MemoryRegion(
                    region_id=i,
                    size_bytes=self.config.block_size_bytes,
                    offset=i * self.config.block_size_bytes,
                    device_id=self.config.device_id,
                    is_free=True
                )
                self._regions[i] = region
                self._free_regions.append(i)
            self._next_region_id = num_blocks
        else:
            # Single large region
            region = MemoryRegion(
                region_id=0,
                size_bytes=self.config.pool_size_bytes,
                offset=0,
                device_id=self.config.device_id,
                is_free=True
            )
            self._regions[0] = region
            self._free_regions.append(0)
            self._next_region_id = 1

    def allocate(self, size_bytes: int) -> Optional[int]:
        """
        Allocate memory region.

        Returns region_id or None if allocation failed.
        """
        with self._lock:
            if self._state == MemoryState.SLEEPING:
                logger.warning("Cannot allocate while sleeping")
                return None

            # Check for memory pressure
            self._check_memory_pressure()

            if self.config.strategy == AllocationStrategy.POOL:
                return self._allocate_pool(size_bytes)
            else:
                return self._allocate_best_fit(size_bytes)

    def _allocate_pool(self, size_bytes: int) -> Optional[int]:
        """Allocate from fixed-size pool."""
        blocks_needed = (size_bytes + self.config.block_size_bytes - 1) // self.config.block_size_bytes

        if len(self._free_regions) < blocks_needed:
            return None

        # Allocate first free block(s)
        allocated_ids: list[int] = []
        for _ in range(blocks_needed):
            if not self._free_regions:
                break
            region_id = self._free_regions.pop(0)
            region = self._regions[region_id]
            region.is_free = False
            region.ref_count = 1
            region.touch()
            allocated_ids.append(region_id)

        if len(allocated_ids) == blocks_needed:
            # Use first region as the allocation handle
            primary_id = allocated_ids[0]
            region = self._regions[primary_id]
            region.metadata["sub_regions"] = allocated_ids[1:] if len(allocated_ids) > 1 else []

            self._allocated_bytes += blocks_needed * self.config.block_size_bytes

            # Notify callbacks
            for cb in self._allocation_callbacks:
                try:
                    cb(primary_id, size_bytes)
                except Exception as e:
                    logger.error(f"Allocation callback error: {e}")

            return primary_id
        else:
            # Rollback
            for region_id in allocated_ids:
                self._regions[region_id].is_free = True
                self._free_regions.append(region_id)
            return None

    def _allocate_best_fit(self, size_bytes: int) -> Optional[int]:
        """Allocate using best-fit strategy."""
        best_region_id = None
        best_size = float('inf')

        for region_id in self._free_regions:
            region = self._regions[region_id]
            if region.size_bytes >= size_bytes and region.size_bytes < best_size:
                best_region_id = region_id
                best_size = region.size_bytes

        if best_region_id is None:
            return None

        region = self._regions[best_region_id]
        self._free_regions.remove(best_region_id)

        # Split if significantly larger
        if region.size_bytes > size_bytes * 2:
            # Create new free region with remainder
            new_region = MemoryRegion(
                region_id=self._next_region_id,
                size_bytes=region.size_bytes - size_bytes,
                offset=region.offset + size_bytes,
                device_id=self.config.device_id,
                is_free=True
            )
            self._regions[self._next_region_id] = new_region
            self._free_regions.append(self._next_region_id)
            self._next_region_id += 1

            region.size_bytes = size_bytes

        region.is_free = False
        region.ref_count = 1
        region.touch()

        self._allocated_bytes += region.size_bytes

        # Notify callbacks
        for cb in self._allocation_callbacks:
            try:
                cb(best_region_id, size_bytes)
            except Exception as e:
                logger.error(f"Allocation callback error: {e}")

        return best_region_id

    def deallocate(self, region_id: int) -> bool:
        """
        Deallocate memory region.

        Returns True if successful.
        """
        with self._lock:
            if region_id not in self._regions:
                return False

            region = self._regions[region_id]

            if region.is_free:
                return False  # Already free

            # Handle sub-regions for pool allocation
            sub_regions = region.metadata.get("sub_regions", [])
            for sub_id in sub_regions:
                if sub_id in self._regions:
                    sub_region = self._regions[sub_id]
                    sub_region.is_free = True
                    sub_region.ref_count = 0
                    self._free_regions.append(sub_id)

            size_bytes = region.size_bytes
            region.is_free = True
            region.ref_count = 0
            region.metadata.clear()

            self._free_regions.append(region_id)
            self._allocated_bytes -= size_bytes

            # Notify callbacks
            for cb in self._deallocation_callbacks:
                try:
                    cb(region_id, size_bytes)
                except Exception as e:
                    logger.error(f"Deallocation callback error: {e}")

            return True

    def sleep(self) -> int:
        """
        Release GPU memory for sharing with other processes.

        vLLM Pattern: CuMemAllocator.sleep()

        Returns number of bytes released.
        """
        with self._lock:
            if self._state == MemoryState.SLEEPING:
                return 0

            self._state = MemoryState.SLEEPING

            # Take snapshot before sleeping
            snapshot = self.take_snapshot()

            # Release configurable ratio of free regions
            release_count = int(len(self._free_regions) * self.config.sleep_release_ratio)
            released_bytes = 0

            for _ in range(release_count):
                if self._free_regions:
                    region_id = self._free_regions.pop()
                    region = self._regions[region_id]
                    released_bytes += region.size_bytes
                    # In real implementation, this would call cudaFree

            logger.info(f"Sleep: released {released_bytes / (1024**2):.1f}MB")
            return released_bytes

    def wake_up(self) -> int:
        """
        Reclaim GPU memory after sleep.

        vLLM Pattern: CuMemAllocator.wake_up()

        Returns number of bytes reclaimed.
        """
        with self._lock:
            if self._state != MemoryState.SLEEPING:
                return 0

            self._state = MemoryState.ACTIVE

            # Restore from latest snapshot
            if self._snapshots:
                latest_id = max(self._snapshots.keys())
                self.restore_snapshot(latest_id)

            # In real implementation, this would reallocate CUDA memory
            reclaimed_bytes = self.config.pool_size_bytes - self._allocated_bytes

            logger.info(f"Wake up: reclaimed {reclaimed_bytes / (1024**2):.1f}MB")
            return reclaimed_bytes

    @contextmanager
    def use_memory_pool(self) -> Generator[None, None, None]:
        """
        Context manager for memory pool usage.

        vLLM Pattern: use_memory_pool()
        """
        self.wake_up()
        try:
            yield
        finally:
            pass  # Don't automatically sleep, let caller decide

    def take_snapshot(self) -> MemorySnapshot:
        """
        Take snapshot of current memory state.

        vLLM Pattern: MemorySnapshot
        """
        with self._lock:
            snapshot = MemorySnapshot(
                snapshot_id=self._next_snapshot_id,
                device_id=self.config.device_id,
                total_bytes=self.config.pool_size_bytes,
                allocated_bytes=self._allocated_bytes,
                free_bytes=self.config.pool_size_bytes - self._allocated_bytes,
                num_allocations=sum(1 for r in self._regions.values() if not r.is_free),
                fragmentation_ratio=self._calculate_fragmentation(),
                region_states={rid: r.is_free for rid, r in self._regions.items()}
            )

            self._snapshots[self._next_snapshot_id] = snapshot
            self._next_snapshot_id += 1

            logger.debug(f"Snapshot {snapshot.snapshot_id} taken")
            return snapshot

    def restore_snapshot(self, snapshot_id: int) -> bool:
        """Restore memory state from snapshot."""
        with self._lock:
            if snapshot_id not in self._snapshots:
                return False

            snapshot = self._snapshots[snapshot_id]

            # Restore region states
            for region_id, is_free in snapshot.region_states.items():
                if region_id in self._regions:
                    self._regions[region_id].is_free = is_free

            # Rebuild free list
            self._free_regions = [
                rid for rid, region in self._regions.items() if region.is_free
            ]

            # Update allocated bytes
            self._allocated_bytes = sum(
                r.size_bytes for r in self._regions.values() if not r.is_free
            )

            logger.debug(f"Snapshot {snapshot_id} restored")
            return True

    def _calculate_fragmentation(self) -> float:
        """Calculate memory fragmentation ratio."""
        if not self._free_regions:
            return 0.0

        free_sizes = [self._regions[rid].size_bytes for rid in self._free_regions]
        total_free = sum(free_sizes)
        max_free = max(free_sizes)

        if total_free == 0:
            return 0.0

        # Fragmentation = 1 - (largest_free / total_free)
        return 1.0 - (max_free / total_free)

    def _check_memory_pressure(self) -> None:
        """Check and notify on memory pressure."""
        free_ratio = (self.config.pool_size_bytes - self._allocated_bytes) / self.config.pool_size_bytes

        if free_ratio < self.config.low_memory_threshold:
            event = MemoryPressureEvent(
                device_id=self.config.device_id,
                available_bytes=self.config.pool_size_bytes - self._allocated_bytes,
                total_bytes=self.config.pool_size_bytes
            )

            for cb in self._pressure_callbacks:
                try:
                    cb(event)
                except Exception as e:
                    logger.error(f"Pressure callback error: {e}")

    def defragment(self) -> int:
        """
        Defragment memory pool.

        Beyond vLLM: Automatic fragmentation management.

        Returns number of bytes compacted.
        """
        with self._lock:
            if not self.config.enable_defrag:
                return 0

            if self.config.strategy == AllocationStrategy.POOL:
                return 0  # Fixed-size pools don't fragment

            # Compact free regions (merge adjacent)
            compacted = 0
            sorted_free = sorted(self._free_regions, key=lambda rid: self._regions[rid].offset)

            i = 0
            while i < len(sorted_free) - 1:
                region1 = self._regions[sorted_free[i]]
                region2 = self._regions[sorted_free[i + 1]]

                # Check if adjacent
                if region1.offset + region1.size_bytes == region2.offset:
                    # Merge
                    region1.size_bytes += region2.size_bytes
                    del self._regions[sorted_free[i + 1]]
                    sorted_free.pop(i + 1)
                    compacted += region2.size_bytes
                else:
                    i += 1

            self._free_regions = sorted_free

            if compacted > 0:
                logger.info(f"Defragmented: {compacted / (1024**2):.1f}MB compacted")

            return compacted

    def add_allocation_callback(self, callback: Callable[[int, int], None]) -> None:
        """Add callback for allocation events."""
        self._allocation_callbacks.append(callback)

    def add_deallocation_callback(self, callback: Callable[[int, int], None]) -> None:
        """Add callback for deallocation events."""
        self._deallocation_callbacks.append(callback)

    def add_pressure_callback(self, callback: Callable[[MemoryPressureEvent], None]) -> None:
        """Add callback for memory pressure events."""
        self._pressure_callbacks.append(callback)

    def get_stats(self) -> dict[str, Any]:
        """Get allocator statistics."""
        with self._lock:
            return {
                "state": self._state.name,
                "total_bytes": self.config.pool_size_bytes,
                "allocated_bytes": self._allocated_bytes,
                "free_bytes": self.config.pool_size_bytes - self._allocated_bytes,
                "num_regions": len(self._regions),
                "num_free_regions": len(self._free_regions),
                "fragmentation_ratio": self._calculate_fragmentation(),
                "num_snapshots": len(self._snapshots),
            }

    @property
    def is_sleeping(self) -> bool:
        """Check if allocator is sleeping."""
        return self._state == MemoryState.SLEEPING

    @property
    def available_bytes(self) -> int:
        """Get available bytes for allocation."""
        with self._lock:
            return self.config.pool_size_bytes - self._allocated_bytes


class MultiGPUMemoryBalancer:
    """
    Balance memory allocation across multiple GPUs.

    Beyond vLLM: Multi-GPU memory coordination.
    """

    def __init__(self, num_devices: int):
        self.num_devices = num_devices
        self._allocators: dict[int, CuMemAllocator] = {}

        for device_id in range(num_devices):
            config = MemoryPoolConfig(device_id=device_id)
            self._allocators[device_id] = CuMemAllocator(config)

        self._lock = threading.Lock()

    def get_allocator(self, device_id: int) -> CuMemAllocator:
        """Get allocator for device."""
        return self._allocators[device_id]

    def allocate_balanced(self, size_bytes: int) -> Optional[tuple[int, int]]:
        """
        Allocate on device with most free memory.

        Returns (device_id, region_id) or None.
        """
        with self._lock:
            # Find device with most free memory
            best_device = max(
                self._allocators.keys(),
                key=lambda d: self._allocators[d].available_bytes
            )

            allocator = self._allocators[best_device]
            region_id = allocator.allocate(size_bytes)

            if region_id is not None:
                return (best_device, region_id)
            return None

    def deallocate(self, device_id: int, region_id: int) -> bool:
        """Deallocate on specific device."""
        if device_id not in self._allocators:
            return False
        return self._allocators[device_id].deallocate(region_id)

    def sleep_all(self) -> dict[int, int]:
        """Sleep all allocators. Returns bytes released per device."""
        with self._lock:
            return {
                device_id: allocator.sleep()
                for device_id, allocator in self._allocators.items()
            }

    def wake_up_all(self) -> dict[int, int]:
        """Wake up all allocators. Returns bytes reclaimed per device."""
        with self._lock:
            return {
                device_id: allocator.wake_up()
                for device_id, allocator in self._allocators.items()
            }

    def get_total_stats(self) -> dict[str, Any]:
        """Get aggregated stats across all devices."""
        with self._lock:
            total_bytes = 0
            allocated_bytes = 0

            for allocator in self._allocators.values():
                stats = allocator.get_stats()
                total_bytes += stats["total_bytes"]
                allocated_bytes += stats["allocated_bytes"]

            return {
                "num_devices": self.num_devices,
                "total_bytes": total_bytes,
                "allocated_bytes": allocated_bytes,
                "free_bytes": total_bytes - allocated_bytes,
                "utilization": allocated_bytes / total_bytes if total_bytes > 0 else 0.0,
            }


# Convenience exports
__all__ = [
    "MemoryState",
    "AllocationStrategy",
    "MemoryRegion",
    "MemorySnapshot",
    "MemoryPoolConfig",
    "MemoryPressureEvent",
    "CuMemAllocator",
    "MultiGPUMemoryBalancer",
]
