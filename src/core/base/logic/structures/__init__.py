"""
Base data structures.

Phase 18-19: Beyond vLLM - Advanced data structures and performance patterns.
"""
from src.core.base.logic.structures.bloom_filter import (
    BloomFilter,
    CountingBloomFilter,
    ScalableBloomFilter,
)
from src.core.base.logic.structures.ring_buffer import (
    RingBuffer,
    ThreadSafeRingBuffer,
    TimeSeriesBuffer,
    TimestampedValue,
    SlidingWindowAggregator,
)
from src.core.base.logic.structures.object_pool import (
    ObjectPool,
    TypedObjectPool,
    BufferPool,
    TieredBufferPool,
    PoolStats,
    pooled_list,
    pooled_dict,
    pooled_set,
)
from src.core.base.logic.structures.lock_free_queue import (
    MPMCQueue,
    SPSCQueue,
    PriorityQueue,
    WorkStealingDeque,
    BatchingQueue,
    QueueStats,
)
from src.core.base.logic.structures.memory_arena import (
    MemoryArena,
    TypedArena,
    StackArena,
    SlabAllocator,
    ArenaStats,
    temp_arena,
    thread_temp_alloc,
)

__all__ = [
    # Bloom Filters (Phase 18)
    'BloomFilter',
    'CountingBloomFilter',
    'ScalableBloomFilter',

    # Ring Buffers (Phase 18)
    'RingBuffer',
    'ThreadSafeRingBuffer',
    'TimeSeriesBuffer',
    'TimestampedValue',
    'SlidingWindowAggregator',

    # Object Pools (Phase 19)
    'ObjectPool',
    'TypedObjectPool',
    'BufferPool',
    'TieredBufferPool',
    'PoolStats',
    'pooled_list',
    'pooled_dict',
    'pooled_set',

    # Queues (Phase 19)
    'MPMCQueue',
    'SPSCQueue',
    'PriorityQueue',
    'WorkStealingDeque',
    'BatchingQueue',
    'QueueStats',

    # Memory Arenas (Phase 19)
    'MemoryArena',
    'TypedArena',
    'StackArena',
    'SlabAllocator',
    'ArenaStats',
    'temp_arena',
    'thread_temp_alloc',
]
