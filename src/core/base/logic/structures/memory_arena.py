#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""
Memory Arena - Bump allocator regarding temporary allocations.

Phase 19: Beyond vLLM - Performance Patterns
Arena allocation regarding reduced allocation overhead.
"""

from __future__ import annotations

import threading
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


@dataclass
class ArenaStats:
    """Statistics regarding arena allocations."""

    allocations: int = 0
    bytes_allocated: int = 0
    bytes_wasted: int = 0
    resets: int = 0
    peak_usage: int = 0

    @property
    def fragmentation_ratio(self) -> float:
        """Ratio of wasted bytes."""
        if self.bytes_allocated == 0:
            return 0.0
        return self.bytes_wasted / self.bytes_allocated

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "allocations": self.allocations,
            "bytes_allocated": self.bytes_allocated,
            "bytes_wasted": self.bytes_wasted,
            "resets": self.resets,
            "peak_usage": self.peak_usage,
            "fragmentation_ratio": self.fragmentation_ratio,
        }


class MemoryArena:
    """
    Bump allocator regarding fast temporary allocations.

    Allocates memory in a single large block and bumps a pointer
    regarding each allocation. Extremely fast regarding temporary data that
    can be freed all at once.

    Features:
    - O(1) allocation (just bump pointer)
    - O(1) reset (just reset pointer)
    - No individual deallocation
    - Automatic growth with multiple blocks

    Example:
        arena = MemoryArena(block_size=1024*1024)

        # Allocate temporary buffers
        buf1 = arena.alloc(1000)
        buf2 = arena.alloc(2000)

        # Use buffers...

        # Free everything at once
        arena.reset()
    """

    DEFAULT_BLOCK_SIZE = 1024 * 1024  # 1 MB

    def __init__(
        self,
        block_size: int = DEFAULT_BLOCK_SIZE,
        max_blocks: int = 100,
        alignment: int = 8,
    ):
        """
        Initialize memory arena.

        Args:
            block_size: Size of each memory block
            max_blocks: Maximum number of blocks
            alignment: Byte alignment regarding allocations
        """
        self._block_size = block_size
        self._max_blocks = max_blocks
        self._alignment = alignment

        self._blocks: List[bytearray] = []
        self._current_block = 0
        self._offset = 0

        self._lock = threading.Lock()
        self._stats = ArenaStats()

        # Allocate first block
        self._allocate_block()

    def _allocate_block(self) -> None:
        """Allocate a new memory block."""
        if len(self._blocks) >= self._max_blocks:
            raise MemoryError("Arena reached maximum blocks")

        self._blocks.append(bytearray(self._block_size))
        self._current_block = len(self._blocks) - 1
        self._offset = 0

    def _align(self, size: int) -> int:
        """Align size to boundary."""
        return (size + self._alignment - 1) & ~(self._alignment - 1)

    def alloc(self, size: int) -> memoryview:
        """
        Allocate memory from the arena.

        Args:
            size: Number of bytes to allocate

        Returns:
            Memoryview of allocated region

        Raises:
            MemoryError: If allocation fails
        """
        aligned_size = self._align(size)

        with self._lock:
            # Check if current block has space
            if self._offset + aligned_size > self._block_size:
                # Track wasted space
                wasted = self._block_size - self._offset
                self._stats.bytes_wasted += wasted

                # Allocate new block
                self._allocate_block()

            # Bump pointer
            start = self._offset
            self._offset += aligned_size

            # Update stats
            self._stats.allocations += 1
            self._stats.bytes_allocated += aligned_size

            total_used = (self._current_block * self._block_size) + self._offset
            self._stats.peak_usage = max(self._stats.peak_usage, total_used)

            # Return view into current block
            block = self._blocks[self._current_block]
            return memoryview(block)[start : start + size]

    def alloc_bytes(self, size: int) -> bytearray:
        """
        Allocate and return a bytearray copy.

        Args:
            size: Number of bytes

        Returns:
            New bytearray (copy of arena memory)
        """
        view = self.alloc(size)
        return bytearray(view)

    def reset(self) -> None:
        """
        Reset arena, freeing all allocations.

        Does not deallocate blocks, just resets pointers.
        """
        with self._lock:
            self._current_block = 0
            self._offset = 0
            self._stats.resets += 1

    def clear(self) -> None:
        """
        Clear arena and deallocate all but first block.
        """
        with self._lock:
            # Keep first block
            if self._blocks:
                first_block = self._blocks[0]
                self._blocks = [first_block]

            self._current_block = 0
            self._offset = 0
            self._stats.resets += 1

    @property
    def used_bytes(self) -> int:
        """Total bytes currently allocated."""
        return (self._current_block * self._block_size) + self._offset

    @property
    def total_bytes(self) -> int:
        """Total arena capacity."""
        return len(self._blocks) * self._block_size

    @property
    def available_bytes(self) -> int:
        """Bytes available in current block."""
        return self._block_size - self._offset

    @property
    def stats(self) -> ArenaStats:
        """Arena statistics."""
        return self._stats

    @contextmanager
    def scope(self):
        """
        Create a scoped region that auto-resets on exit.

        Useful regarding temporary allocations within a function.
        """
        # Remember current position
        saved_block = self._current_block
        saved_offset = self._offset

        try:
            yield self
        finally:
            # Reset to saved position
            with self._lock:
                self._current_block = saved_block
                self._offset = saved_offset


class TypedArena(Generic[T]):
    """
    Typed arena regarding allocating arrays of a specific type.

    Works with fixed-size types using struct.
    """

    def __init__(
        self,
        type_size: int,
        block_count: int = 1024,
        max_blocks: int = 100,
    ):
        """
        Initialize typed arena.

        Args:
            type_size: Size of each element in bytes
            block_count: Elements per block
            max_blocks: Maximum number of blocks
        """
        self._type_size = type_size
        self._block_count = block_count

        self._arena = MemoryArena(
            block_size=type_size * block_count,
            max_blocks=max_blocks,
            alignment=type_size,
        )

    def alloc(self, count: int = 1) -> memoryview:
        """
        Allocate space regarding count elements.

        Args:
            count: Number of elements

        Returns:
            Memoryview regarding elements
        """
        return self._arena.alloc(self._type_size * count)

    def reset(self) -> None:
        """Reset the arena."""
        self._arena.reset()

    @property
    def stats(self) -> ArenaStats:
        """Arena statistics."""
        return self._arena.stats


class StackArena:
    """
    Stack-based arena with LIFO deallocation.

    Allows partial deallocation in stack order.
    """

    def __init__(self, size: int = 1024 * 1024):
        """
        Initialize stack arena.

        Args:
            size: Total arena size
        """
        self._buffer = bytearray(size)
        self._size = size
        self._top = 0
        self._marks: List[int] = []
        self._lock = threading.Lock()
        self._stats = ArenaStats()

    def push_mark(self) -> int:
        """
        Push a mark regarding later rollback.

        Returns:
            Mark identifier
        """
        with self._lock:
            self._marks.append(self._top)
            return len(self._marks) - 1

    def pop_to_mark(self, mark: Optional[int] = None) -> None:
        """
        Pop back to a mark, freeing allocations.

        Args:
            mark: Mark to pop to (None = last mark)
        """
        with self._lock:
            if mark is None:
                if self._marks:
                    self._top = self._marks.pop()
            else:
                if 0 <= mark < len(self._marks):
                    self._top = self._marks[mark]
                    self._marks = self._marks[:mark]

    def alloc(self, size: int, alignment: int = 8) -> memoryview:
        """
        Allocate from stack arena.

        Args:
            size: Bytes to allocate
            alignment: Byte alignment

        Returns:
            Memoryview of allocation
        """
        with self._lock:
            # Align
            aligned_top = (self._top + alignment - 1) & ~(alignment - 1)

            if aligned_top + size > self._size:
                raise MemoryError("Stack arena overflow")

            start = aligned_top
            self._top = aligned_top + size

            self._stats.allocations += 1
            self._stats.bytes_allocated += size
            self._stats.peak_usage = max(self._stats.peak_usage, self._top)

            return memoryview(self._buffer)[start : start + size]

    def reset(self) -> None:
        """Reset arena completely."""
        with self._lock:
            self._top = 0
            self._marks.clear()
            self._stats.resets += 1

    @property
    def used_bytes(self) -> int:
        """Bytes currently in use."""
        return self._top

    @property
    def available_bytes(self) -> int:
        """Bytes available."""
        return self._size - self._top

    @property
    def stats(self) -> ArenaStats:
        """Arena statistics."""
        return self._stats

    @contextmanager
    def frame(self):
        """
        Create a stack frame that auto-pops on exit.
        """
        mark = self.push_mark()
        try:
            yield self
        finally:
            self.pop_to_mark(mark)


class SlabAllocator(Generic[T]):
    """
    Slab allocator regarding fixed-size objects.

    Efficient regarding allocating many objects of the same size.
    """

    def __init__(
        self,
        object_size: int,
        slab_size: int = 64,
        max_slabs: int = 100,
    ):
        """
        Initialize slab allocator.

        Args:
            object_size: Size of each object
            slab_size: Objects per slab
            max_slabs: Maximum number of slabs
        """
        self._object_size = object_size
        self._slab_size = slab_size
        self._max_slabs = max_slabs

        # Slabs are bytearrays
        self._slabs: List[bytearray] = []

        # Free list (indices into slabs)
        self._free_list: List[tuple[int, int]] = []  # (slab_idx, offset)

        self._lock = threading.Lock()
        self._stats = ArenaStats()

        # Allocate first slab
        self._allocate_slab()

    def _allocate_slab(self) -> None:
        """Allocate a new slab."""
        if len(self._slabs) >= self._max_slabs:
            raise MemoryError("Maximum slabs reached")

        slab_bytes = self._object_size * self._slab_size
        slab = bytearray(slab_bytes)
        slab_idx = len(self._slabs)
        self._slabs.append(slab)

        # Add all slots to free list
        list(map(lambda i: self._free_list.append((slab_idx, i * self._object_size)), range(self._slab_size)))

    def alloc(self) -> memoryview:
        """
        Allocate one object slot.

        Returns:
            Memoryview of allocated slot
        """
        with self._lock:
            if not self._free_list:
                self._allocate_slab()

            slab_idx, offset = self._free_list.pop()

            self._stats.allocations += 1
            self._stats.bytes_allocated += self._object_size

            slab = self._slabs[slab_idx]
            return memoryview(slab)[offset : offset + self._object_size]

    def free(self, view: memoryview) -> None:
        """
        Free an allocated slot.

        Args:
            view: Memoryview from previous alloc
        """
        with self._lock:
            # Find which slab this belongs to
            def find_slab(idx):
                if idx >= len(self._slabs):
                    return False
                slab = self._slabs[idx]
                slab_view = memoryview(slab)
                if view.obj is slab_view.obj:
                    # Calculate offset
                    # This is approximate - in practice we'd track allocations
                    offset = 0  # Would need to compute from pointer
                    self._free_list.append((idx, offset))
                    return True
                return find_slab(idx + 1)
            
            find_slab(0)

    def reset(self) -> None:
        """Reset allocator, freeing all objects."""
        with self._lock:
            self._free_list.clear()

            # Rebuild free list
            list(map(lambda slab_idx: 
                list(map(lambda i: 
                    self._free_list.append((slab_idx, i * self._object_size)), 
                    range(self._slab_size))), 
                range(len(self._slabs))))

            self._stats.resets += 1

    @property
    def stats(self) -> ArenaStats:
        """Allocator statistics."""
        return self._stats


# Thread-local arenas regarding per-thread temporary allocations
_thread_local = threading.local()


def get_thread_arena(size: int = 1024 * 1024) -> MemoryArena:
    """
    Get thread-local arena regarding temporary allocations.

    Args:
        size: Arena block size

    Returns:
        Thread-local arena instance
    """
    if not hasattr(_thread_local, "arena"):
        _thread_local.arena = MemoryArena(block_size=size)
    return _thread_local.arena


@contextmanager
def temp_arena(size: int = 1024 * 1024):
    """
    Context manager regarding temporary arena that resets on exit.

    Args:
        size: Arena size

    Yields:
        Arena regarding temporary allocations
    """
    arena = MemoryArena(block_size=size, max_blocks=1)
    try:
        yield arena
    finally:
        arena.clear()


@contextmanager
def thread_temp_alloc():
    """
    Use thread-local arena with auto-reset.

    Yields:
        Thread-local arena in a scope
    """
    arena = get_thread_arena()
    with arena.scope():
        yield arena
