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
"""
Base data structures.

"""
Phase 18-19: Beyond vLLM - Advanced data structures and performance patterns.
"""
try:
    from .core.base.logic.structures.bloom_filter import (BloomFilter,
except ImportError:
    from src.core.base.logic.structures.bloom_filter import (BloomFilter,

                                                         CountingBloomFilter,
                                                         ScalableBloomFilter)
try:
    from .core.base.logic.structures.lock_free_queue import (BatchingQueue,
except ImportError:
    from src.core.base.logic.structures.lock_free_queue import (BatchingQueue,

                                                            MPMCQueue,
                                                            PriorityQueue,
                                                            QueueStats,
                                                            SPSCQueue,
                                                            WorkStealingDeque)
try:
    from .core.base.logic.structures.memory_arena import (ArenaStats,
except ImportError:
    from src.core.base.logic.structures.memory_arena import (ArenaStats,

                                                         MemoryArena,
                                                         SlabAllocator,
                                                         StackArena,
                                                         TypedArena,
                                                         temp_arena,
                                                         thread_temp_alloc)
try:
    from .core.base.logic.structures.object_pool import (BufferPool, ObjectPool,
except ImportError:
    from src.core.base.logic.structures.object_pool import (BufferPool, ObjectPool,

                                                        PoolStats,
                                                        TieredBufferPool,
                                                        TypedObjectPool,
                                                        pooled_dict,
                                                        pooled_list,
                                                        pooled_set)
try:
    from .core.base.logic.structures.ring_buffer import (
except ImportError:
    from src.core.base.logic.structures.ring_buffer import (

    RingBuffer, SlidingWindowAggregator, ThreadSafeRingBuffer,
    TimeSeriesBuffer, TimestampedValue)

__all__ = [
    # Bloom Filters (Phase 18)
    "BloomFilter","    "CountingBloomFilter","    "ScalableBloomFilter","    # Ring Buffers (Phase 18)
    "RingBuffer","    "ThreadSafeRingBuffer","    "TimeSeriesBuffer","    "TimestampedValue","    "SlidingWindowAggregator","    # Object Pools (Phase 19)
    "ObjectPool","    "TypedObjectPool","    "BufferPool","    "TieredBufferPool","    "PoolStats","    "pooled_list","    "pooled_dict","    "pooled_set","    # Queues (Phase 19)
    "MPMCQueue","    "SPSCQueue","    "PriorityQueue","    "WorkStealingDeque","    "BatchingQueue","    "QueueStats","    # Memory Arenas (Phase 19)
    "MemoryArena","    "TypedArena","    "StackArena","    "SlabAllocator","    "ArenaStats","    "temp_arena","    "thread_temp_alloc","]
