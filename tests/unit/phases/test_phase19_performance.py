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
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Phase 19 Tests: Beyond vLLM - Performance Patterns.

Tests for:
- ObjectPool - Reduce GC pressure
- LockFreeQueue - High-performance queues
- FastSerializer - msgpack/cbor/binary serialization
- PriorityScheduler - Deadline-aware scheduling
- ConnectionPool - Generic connection pooling
- MemoryArena - Bump allocator

Phase 19: Beyond vLLM - Performance
"""
import pytest
import time
import threading
from concurrent.futures import Future
from queue import Empty


class TestObjectPool:
    """Tests for ObjectPool."""

    def test_basic_acquire_release(self):
        """Test basic pool operations."""
        from src.core.base.logic.structures.object_pool import ObjectPool

        pool = ObjectPool(factory=list, max_size=10)

        obj = pool.acquire()
        assert isinstance(obj, list)
        assert pool.stats.created == 1

        pool.release(obj)
        assert pool.size == 1

    def test_object_reuse(self):
        """Test objects are reused from pool."""
        from src.core.base.logic.structures.object_pool import ObjectPool

        pool = ObjectPool(
            factory=list,
            reset=lambda x: x.clear(),
            max_size=10,
        )

        obj1 = pool.acquire()
        obj1.append(1)
        pool.release(obj1)

        obj2 = pool.acquire()
        assert obj2 is obj1  # Same object reused
        assert len(obj2) == 0  # Was reset
        assert pool.stats.reused == 1

    def test_borrow_context_manager(self):
        """Test context manager auto-returns."""
        from src.core.base.logic.structures.object_pool import ObjectPool

        pool = ObjectPool(factory=dict, max_size=5)

        with pool.borrow() as d:
            d['key'] = 'value'

        assert pool.size == 1
        assert pool.stats.returned == 1

    def test_max_size_limit(self):
        """Test pool respects max size."""
        from src.core.base.logic.structures.object_pool import ObjectPool

        pool = ObjectPool(factory=list, max_size=2)

        obj1 = pool.acquire()
        obj2 = pool.acquire()
        obj3 = pool.acquire()

        pool.release(obj1)
        pool.release(obj2)
        pool.release(obj3)  # Should be discarded

        assert pool.size == 2
        assert pool.stats.discarded == 1

    def test_buffer_pool(self):
        """Test specialized buffer pool."""
        from src.core.base.logic.structures.object_pool import BufferPool

        pool = BufferPool(buffer_size=4096, max_buffers=10)

        buf = pool.acquire()
        assert len(buf) == 4096

        pool.release(buf)
        assert pool.stats.returned == 1

    def test_tiered_buffer_pool(self):
        """Test multi-tier buffer pool."""
        from src.core.base.logic.structures.object_pool import TieredBufferPool

        pool = TieredBufferPool()

        # Small buffer
        small = pool.acquire(100)
        assert len(small) >= 100

        # Large buffer
        large = pool.acquire(50000)
        assert len(large) >= 50000

        pool.release(small)
        pool.release(large)

    def test_pooled_list_dict_set(self):
        """Test convenience functions."""
        from src.core.base.logic.structures.object_pool import (
            pooled_list, pooled_dict, pooled_set
        )

        with pooled_list() as lst:
            lst.append(1)
            assert 1 in lst

        with pooled_dict() as d:
            d['key'] = 'value'
            assert d['key'] == 'value'

        with pooled_set() as s:
            s.add(42)
            assert 42 in s


class TestLockFreeQueue:
    """Tests for queue implementations."""

    def test_mpmc_basic(self):
        """Test MPMC queue basic operations."""
        from src.core.base.logic.structures.lock_free_queue import MPMCQueue

        queue = MPMCQueue[int](capacity=100)

        queue.put(1)
        queue.put(2)
        queue.put(3)

        assert queue.get() == 1
        assert queue.get() == 2
        assert queue.get() == 3

    def test_mpmc_try_operations(self):
        """Test non-blocking operations."""
        from src.core.base.logic.structures.lock_free_queue import MPMCQueue

        queue = MPMCQueue[int](capacity=2)

        assert queue.try_put(1)
        assert queue.try_put(2)
        assert not queue.try_put(3)  # Full

        assert queue.try_get() == 1
        assert queue.try_get() == 2
        assert queue.try_get() is None  # Empty

    def test_mpmc_concurrent(self):
        """Test concurrent access."""
        from src.core.base.logic.structures.lock_free_queue import MPMCQueue

        queue = MPMCQueue[int](capacity=1000)
        results = []

        def producer(start):
            for i in range(100):
                queue.put(start + i)

        def consumer():
            for _ in range(100):
                try:
                    results.append(queue.get(timeout=1.0))
                except Empty:
                    break

        # Start producers
        producers = [
            threading.Thread(target=producer, args=(i * 100,))
            for i in range(4)
        ]
        for p in producers:
            p.start()
        for p in producers:
            p.join()

        # Start consumers
        consumers = [
            threading.Thread(target=consumer)
            for _ in range(4)
        ]
        for c in consumers:
            c.start()
        for c in consumers:
            c.join()

        assert len(results) == 400

    def test_spsc_queue(self):
        """Test single-producer single-consumer queue."""
        from src.core.base.logic.structures.lock_free_queue import SPSCQueue

        queue = SPSCQueue[int](capacity=16)

        for i in range(10):
            assert queue.try_put(i)

        for i in range(10):
            assert queue.try_get() == i

        assert queue.is_empty

    def test_priority_queue(self):
        """Test priority queue."""
        from src.core.base.logic.structures.lock_free_queue import PriorityQueue

        queue = PriorityQueue[str]()

        queue.put("low", priority=10.0)
        queue.put("high", priority=1.0)
        queue.put("medium", priority=5.0)

        # Should come out in priority order
        assert queue.get() == "high"
        assert queue.get() == "medium"
        assert queue.get() == "low"

    def test_work_stealing_deque(self):
        """Test work-stealing deque."""
        from src.core.base.logic.structures.lock_free_queue import WorkStealingDeque

        deque = WorkStealingDeque[int](capacity=100)

        # Owner pushes
        for i in range(10):
            deque.push(i)

        # Owner pops (LIFO)
        assert deque.pop() == 9
        assert deque.pop() == 8

        # Thief steals (FIFO)
        assert deque.steal() == 0
        assert deque.steal() == 1

    def test_batching_queue(self):
        """Test batching queue."""
        from src.core.base.logic.structures.lock_free_queue import BatchingQueue

        queue = BatchingQueue[int](batch_size=5, batch_timeout=0.1)

        for i in range(5):
            queue.put(i)

        batch = queue.get_batch(timeout=0.05)
        assert len(batch) == 5
        assert batch == [0, 1, 2, 3, 4]


class TestFastSerializer:
    """Tests for serialization."""

    def test_json_serializer(self):
        """Test JSON serialization."""
        from src.infrastructure.storage.serialization.fast_serializer import JSONSerializer

        s = JSONSerializer()

        data = {'key': 'value', 'number': 42}
        encoded = s.serialize(data)
        decoded = s.deserialize(encoded)

        assert decoded == data

    def test_json_compressed(self):
        """Test compressed JSON."""
        from src.infrastructure.storage.serialization.fast_serializer import JSONSerializer

        s = JSONSerializer(compress=True)

        data = {'key': 'value' * 100}
        encoded = s.serialize(data)
        decoded = s.deserialize(encoded)

        assert decoded == data
        # Compressed should be smaller
        s_plain = JSONSerializer(compress=False)
        assert len(encoded) < len(s_plain.serialize(data))

    def test_pickle_serializer(self):
        """Test Pickle serialization."""
        from src.infrastructure.storage.serialization.fast_serializer import PickleSerializer

        s = PickleSerializer()

        data = {'key': 'value', 'list': [1, 2, 3]}
        encoded = s.serialize(data)
        decoded = s.deserialize(encoded)

        assert decoded == data

    def test_binary_serializer(self):
        """Test custom binary serialization."""
        from src.infrastructure.storage.serialization.fast_serializer import BinarySerializer

        s = BinarySerializer()

        # Test various types
        test_cases = [
            None,
            True,
            False,
            42,
            3.14159,
            "hello world",
            b"bytes data",
            [1, 2, 3],
            {'a': 1, 'b': 2},
        ]

        for data in test_cases:
            encoded = s.serialize(data)
            decoded = s.deserialize(encoded)
            assert decoded == data, f"Failed for {data}"

    def test_binary_nested(self):
        """Test binary serialization with nested data."""
        from src.infrastructure.storage.serialization.fast_serializer import BinarySerializer

        s = BinarySerializer()

        data = {
            'users': [
                {'name': 'Alice', 'age': 30},
                {'name': 'Bob', 'age': 25},
            ],
            'count': 2,
        }

        encoded = s.serialize(data)
        decoded = s.deserialize(encoded)

        assert decoded == data

    def test_serializer_registry(self):
        """Test serializer registry."""
        from src.infrastructure.storage.serialization.fast_serializer import (
            SerializerRegistry, SerializationFormat
        )

        registry = SerializerRegistry()

        data = {'test': 123}

        # Use different formats
        json_bytes = registry.serialize(data, SerializationFormat.JSON)
        pickle_bytes = registry.serialize(data, SerializationFormat.PICKLE)

        assert registry.deserialize(json_bytes, SerializationFormat.JSON) == data
        assert registry.deserialize(pickle_bytes, SerializationFormat.PICKLE) == data

    def test_fast_serialize(self):
        """Test fast serialize convenience function."""
        from src.infrastructure.storage.serialization.fast_serializer import (
            fast_serialize, fast_deserialize
        )

        data = {'key': 'value'}
        encoded = fast_serialize(data)
        decoded = fast_deserialize(encoded)

        assert decoded == data


class TestPriorityScheduler:
    """Tests for priority scheduler."""

    def test_basic_scheduling(self):
        """Test basic task scheduling."""
        from src.infrastructure.engine.scheduling.priority_scheduler import (
            PriorityScheduler, TaskPriority
        )

        scheduler = PriorityScheduler(workers=2)

        try:
            future = scheduler.submit(lambda: 42)
            result = future.result(timeout=5.0)
            assert result == 42
        finally:
            scheduler.shutdown()

    def test_priority_order(self):
        """Test tasks execute in priority order."""
        from src.infrastructure.engine.scheduling.priority_scheduler import (
            PriorityScheduler, TaskPriority
        )

        scheduler = PriorityScheduler(workers=1)
        results = []

        try:
            # Submit in reverse priority order
            f3 = scheduler.submit(
                lambda: results.append('low'),
                priority=TaskPriority.LOW,
            )
            f2 = scheduler.submit(
                lambda: results.append('normal'),
                priority=TaskPriority.NORMAL,
            )
            f1 = scheduler.submit(
                lambda: results.append('high'),
                priority=TaskPriority.HIGH,
            )

            f1.result(timeout=5.0)
            f2.result(timeout=5.0)
            f3.result(timeout=5.0)

            # High priority should execute first
            assert results[0] == 'high'
        finally:
            scheduler.shutdown()

    def test_deadline_scheduler(self):
        """Test deadline-based scheduler."""
        from src.infrastructure.engine.scheduling.priority_scheduler import DeadlineScheduler

        scheduler = DeadlineScheduler(workers=2)

        try:
            future = scheduler.submit(lambda: "done", deadline_ms=1000.0)
            result = future.result(timeout=5.0)
            assert result == "done"
        finally:
            scheduler.shutdown()

    def test_scheduler_stats(self):
        """Test scheduler statistics."""
        from src.infrastructure.engine.scheduling.priority_scheduler import PriorityScheduler

        scheduler = PriorityScheduler(workers=2)

        try:
            futures = [
                scheduler.submit(lambda: i)
                for i in range(10)
            ]

            for f in futures:
                f.result(timeout=5.0)

            stats = scheduler.stats
            assert stats.scheduled == 10
            assert stats.completed == 10
        finally:
            scheduler.shutdown()


class TestConnectionPool:
    """Tests for connection pool."""

    def test_basic_pool(self):
        """Test basic connection pool."""
        from src.infrastructure.engine.pooling.connection_pool import ConnectionPool

        # Mock connection
        class MockConnection:
            def __init__(self):
                self.closed = False

            def close(self):
                self.closed = True

        pool = ConnectionPool(factory=MockConnection, min_size=2, max_size=5)

        try:
            conn = pool.acquire()
            assert isinstance(conn, MockConnection)
            assert pool.in_use_count == 1

            pool.release(conn)
            assert pool.idle_count >= 1
        finally:
            pool.close()

    def test_connection_context_manager(self):
        """Test connection pool context manager."""
        from src.infrastructure.engine.pooling.connection_pool import ConnectionPool

        class MockConnection:
            def close(self):
                pass

        pool = ConnectionPool(factory=MockConnection, max_size=5)

        try:
            with pool.connection() as conn:
                assert isinstance(conn, MockConnection)
                assert pool.in_use_count == 1

            assert pool.in_use_count == 0
        finally:
            pool.close()

    def test_pool_stats(self):
        """Test pool statistics."""
        from src.infrastructure.engine.pooling.connection_pool import ConnectionPool

        class MockConnection:
            def close(self):
                pass

        pool = ConnectionPool(factory=MockConnection, min_size=0, max_size=5)

        try:
            conn1 = pool.acquire()
            conn2 = pool.acquire()

            assert pool.stats.created == 2

            pool.release(conn1)
            pool.release(conn2)

            # Reacquire (should reuse)
            conn3 = pool.acquire()
            assert pool.stats.reused >= 1
        finally:
            pool.close()

    def test_pool_timeout(self):
        """Test connection acquisition timeout."""
        from src.infrastructure.engine.pooling.connection_pool import ConnectionPool

        class MockConnection:
            def close(self):
                pass

        pool = ConnectionPool(
            factory=MockConnection,
            max_size=1,
            acquire_timeout_seconds=0.1,
        )

        try:
            conn = pool.acquire()

            # Second acquire should timeout
            with pytest.raises(TimeoutError):
                pool.acquire(timeout=0.1)
        finally:
            pool.close()


class TestMemoryArena:
    """Tests for memory arena."""

    def test_basic_allocation(self):
        """Test basic arena allocation."""
        from src.core.base.logic.structures.memory_arena import MemoryArena

        arena = MemoryArena(block_size=4096)

        buf1 = arena.alloc(100)
        assert len(buf1) == 100

        buf2 = arena.alloc(200)
        assert len(buf2) == 200

        assert arena.stats.allocations == 2

    def test_arena_reset(self):
        """Test arena reset frees all allocations."""
        from src.core.base.logic.structures.memory_arena import MemoryArena

        arena = MemoryArena(block_size=1024)

        arena.alloc(100)
        arena.alloc(200)

        used_before = arena.used_bytes
        assert used_before > 0

        arena.reset()
        assert arena.used_bytes == 0
        assert arena.stats.resets == 1

    def test_arena_scope(self):
        """Test scoped allocation with auto-reset."""
        from src.core.base.logic.structures.memory_arena import MemoryArena

        arena = MemoryArena(block_size=1024)

        arena.alloc(100)
        base_used = arena.used_bytes

        with arena.scope():
            arena.alloc(200)
            arena.alloc(300)
            # Used bytes increased
            assert arena.used_bytes > base_used

        # After scope, reset to base
        assert arena.used_bytes == base_used

    def test_stack_arena(self):
        """Test stack arena with marks."""
        from src.core.base.logic.structures.memory_arena import StackArena

        arena = StackArena(size=4096)

        arena.alloc(100)
        mark = arena.push_mark()
        arena.alloc(200)
        arena.alloc(300)

        assert arena.used_bytes > 100

        arena.pop_to_mark(mark)
        # Should be back to ~100 bytes
        assert arena.used_bytes <= 112  # Allow alignment

    def test_stack_arena_frame(self):
        """Test stack arena frame context manager."""
        from src.core.base.logic.structures.memory_arena import StackArena

        arena = StackArena(size=4096)

        arena.alloc(100)
        base = arena.used_bytes

        with arena.frame():
            arena.alloc(200)
            arena.alloc(300)

        assert arena.used_bytes == base

    def test_temp_arena(self):
        """Test temporary arena context manager."""
        from src.core.base.logic.structures.memory_arena import temp_arena

        with temp_arena(size=1024) as arena:
            buf = arena.alloc(100)
            assert len(buf) == 100

    def test_thread_local_arena(self):
        """Test thread-local arena."""
        from src.core.base.logic.structures.memory_arena import thread_temp_alloc

        with thread_temp_alloc() as arena:
            buf = arena.alloc(64)
            assert len(buf) == 64


class TestIntegration:
    """Integration tests combining Phase 19 components."""

    def test_pool_with_scheduler(self):
        """Test object pool with scheduler."""
        from src.core.base.logic.structures.object_pool import ObjectPool
        from src.infrastructure.engine.scheduling.priority_scheduler import PriorityScheduler

        pool = ObjectPool(factory=list, max_size=10)
        scheduler = PriorityScheduler(workers=2)

        try:
            def task():
                with pool.borrow() as lst:
                    lst.append(42)
                    return 42

            futures = [scheduler.submit(task) for _ in range(20)]
            results = [f.result(timeout=5.0) for f in futures]

            assert all(r == 42 for r in results)
            assert len(results) == 20
        finally:
            scheduler.shutdown()

    def test_serializer_with_queue(self):
        """Test serializer with queue."""
        from src.infrastructure.storage.serialization.fast_serializer import BinarySerializer
        from src.core.base.logic.structures.lock_free_queue import MPMCQueue

        serializer = BinarySerializer()
        queue = MPMCQueue[bytes](capacity=100)

        # Producer serializes
        data = {'message': 'hello', 'count': 42}
        encoded = serializer.serialize(data)
        queue.put(encoded)

        # Consumer deserializes
        received = queue.get()
        decoded = serializer.deserialize(received)

        assert decoded == data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

