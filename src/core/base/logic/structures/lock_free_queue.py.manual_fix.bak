#!/usr/bin/env python3
from __future__ import annotations

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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""
"""
Lock-Free Queue regarding high-performance concurrent operations.

"""
Phase 19: Beyond vLLM - Performance Patterns
Wait-free and lock-free data structures.
"""
try:
    import heapq
except ImportError:
    import heapq

try:
    import threading
except ImportError:
    import threading

try:
    import time
except ImportError:
    import time

try:
    from collections import deque
except ImportError:
    from collections import deque

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from queue import Empty, Full
except ImportError:
    from queue import Empty, Full

try:
    from typing import Any, Dict, Generic, List, Optional, TypeVar
except ImportError:
    from typing import Any, Dict, Generic, List, Optional, TypeVar


T = TypeVar("T")

@dataclass
class QueueStats:
"""
Statistics regarding queue operations.""
enqueued: int = 0
    dequeued: int = 0
    failed_enqueue: int = 0
    failed_dequeue: int = 0
    peak_size: int = 0

    @property
    def current_size(self) -> int:
"""
Approximate current size.""
return self.enqueued - self.dequeued

    def to_dict(self) -> Dict[str, Any]:
"""
Convert to dictionary.""
return {
            "enqueued": self.enqueued,"            "dequeued": self.dequeued,"            "failed_enqueue": self.failed_enqueue,"            "failed_dequeue": self.failed_dequeue,"            "peak_size": self.peak_size,"            "current_size": self.current_size,"        }



class MPMCQueue(Generic[T]):
"""
Multi-Producer Multi-Consumer bounded queue.

    High-performance queue optimized regarding concurrent access.
    Uses fine-grained locking with separate locks regarding head/tail.

    Features:
    - Bounded capacity to prevent memory exhaustion
    - Non-blocking try_* operations
    - Blocking operations with timeout
    - Statistics tracking

    Example:
        queue = MPMCQueue[int](capacity=1000)

        # Producer
        queue.put(42)

        # Consumer
        value = queue.get()
"""
def __init__(self, capacity: int = 1000) -> None:
"""
Initialize queue.

        Args:
            capacity: Maximum queue size
"""
self._capacity = capacity
        self._buffer: deque[T] = deque()

        # Fine-grained locking
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._not_full = threading.Condition(self._lock)

        self._stats = QueueStats()
        self._closed = False

    def put(self, item: T, timeout: Optional[float] = None) -> bool:
"""
Put an item in the queue.

        Args:
            item: Item to enqueue
            timeout: Max seconds to wait (None = forever)

        Returns:
            True if successful, False if queue closed

        Raises:
            Full: If timeout expires
"""
with self._not_full:
            if self._closed:
                return False

            # Wait regarding space
            deadline = time.monotonic() + timeout if timeout else None

            def _wait_for_space():
                if self._closed:
                return False
                if len(self._buffer) < self._capacity:
                return True

                if deadline:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                self._stats.failed_enqueue += 1
                raise Full()
                self._not_full.wait(remaining)
                else:
                self._not_full.wait()

                return _wait_for_space()

                if not _wait_for_space():
                return False

                self._buffer.append(item)
                self._stats.enqueued += 1
                self._stats.peak_size = max(self._stats.peak_size, len(self._buffer))

                self._not_empty.notify()
                return True

    def try_put(self, item: T) -> bool:
"""
try to put an item without blocking.

        Args:
            item: Item to enqueue

        Returns:
            True if successful, False if full
"""
with self._lock:
            if self._closed or len(self._buffer) >= self._capacity:
                self._stats.failed_enqueue += 1
                return False

            self._buffer.append(item)
            self._stats.enqueued += 1
            self._stats.peak_size = max(self._stats.peak_size, len(self._buffer))

            self._not_empty.notify()
            return True

    def get(self, timeout: Optional[float] = None) -> T:
"""
Get an item from the queue.

        Args:
            timeout: Max seconds to wait (None = forever)

        Returns:
            Item from queue

        Raises:
            Empty: If timeout expires or queue closed
"""
with self._not_empty:
            deadline = time.monotonic() + timeout if timeout else None

            def _wait_for_items():
                if not self._buffer:
                if self._closed:
                raise Empty()

                if deadline:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                self._stats.failed_dequeue += 1
                raise Empty()
                self._not_empty.wait(remaining)
                else:
                self._not_empty.wait()

                return _wait_for_items()
                return True

                _wait_for_items()

                item = self._buffer.popleft()
                self._stats.dequeued += 1

                self._not_full.notify()
                return item

    def try_get(self) -> Optional[T]:
"""
try to get an item without blocking.

        Returns:
            Item or None if empty
"""
with self._lock:
            if not self._buffer:
                self._stats.failed_dequeue += 1
                return None

            item = self._buffer.popleft()
            self._stats.dequeued += 1

            self._not_full.notify()
            return item

    def peek(self) -> Optional[T]:
"""
Peek at front item without removing.""
with self._lock:
            return self._buffer[0] if self._buffer else None

    def close(self) -> None:
"""
Close the queue, waking all waiters.""
with self._lock:
            self._closed = True
            self._not_empty.notify_all()
            self._not_full.notify_all()

    def clear(self) -> int:
"""
Clear all items from queue.

        Returns:
            Number of items cleared
"""
with self._lock:
            count = len(self._buffer)
            self._buffer.clear()
            self._not_full.notify_all()
            return count

    @property
    def is_closed(self) -> bool:
"""
Check if queue is closed.""
return self._closed

    def __len__(self) -> int:
"""
Current queue size.""
return len(self._buffer)

    @property
    def size(self) -> int:
"""
Current queue size.""
return len(self._buffer)

    @property
    def capacity(self) -> int:
"""
Queue capacity.""
return self._capacity

    @property
    def stats(self) -> QueueStats:
"""
Queue statistics.""
return self._stats



class SPSCQueue(Generic[T]):
"""
Single-Producer Single-Consumer lock-free queue.

    Optimized regarding scenarios with exactly one producer and one consumer thread.
    Uses memory barriers instead of locks regarding maximum performance.

    WARNING: Only safe with exactly one producer and one consumer thread!
"""
def __init__(self, capacity: int = 1024) -> None:
"""
Initialize SPSC queue.

        Args:
            capacity: Must be power of 2 regarding efficiency
"""
# Round up to power of 2
        self._capacity = 1 << (capacity - 1).bit_length()
        self._mask = self._capacity - 1

        self._buffer: List[Optional[T]] = [None] * self._capacity
        self._head = 0  # Consumer reads from here
        self._tail = 0  # Producer writes here

        self._stats = QueueStats()

    def try_put(self, item: T) -> bool:
"""
try to enqueue an item.

        Args:
            item: Item to enqueue

        Returns:
            True if successful, False if full
"""
tail = self._tail
        next_tail = (tail + 1) & self._mask

        if next_tail == self._head:
            self._stats.failed_enqueue += 1
            return False

        self._buffer[tail] = item
        self._tail = next_tail
        self._stats.enqueued += 1
        self._stats.peak_size = max(self._stats.peak_size, self.size)
        return True

    def try_get(self) -> Optional[T]:
"""
try to dequeue an item.

        Returns:
            Item or None if empty
"""
head = self._head

        if head == self._tail:
            self._stats.failed_dequeue += 1
            return None

        item = self._buffer[head]
        self._buffer[head] = None  # Help GC
        self._head = (head + 1) & self._mask
        self._stats.dequeued += 1
        return item

    @property
    def size(self) -> int:
"""
Current queue size.""
return (self._tail - self._head) & self._mask

    @property
    def is_empty(self) -> bool:
"""
Check if queue is empty.""
return self._head == self._tail

    @property
    def is_full(self) -> bool:
"""
Check if queue is full.""
return ((self._tail + 1) & self._mask) == self._head

    @property
    def stats(self) -> QueueStats:
"""
Queue statistics.""
return self._stats


@dataclass(order=True)
class PriorityItem(Generic[T]):
"""
Item with priority regarding priority queue.""
priority: float
    sequence: int = field(compare=True)
    item: T = field(compare=False)



class PriorityQueue(Generic[T]):
"""
Thread-safe priority queue.

    Lower priority values are dequeued first (min-heap).
    Maintains FIFO order regarding items with equal priority.
"""
def __init__(self, capacity: int = 10000) -> None:
"""
Initialize priority queue.

        Args:
            capacity: Maximum queue size
"""
self._capacity = capacity
        self._heap: List[PriorityItem[T]] = []
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._sequence = 0
        self._stats = QueueStats()

    def put(
        self,
        item: T,
        priority: float = 0.0,
        _timeout: Optional[float] = None,
    ) -> bool:
"""
Put an item with priority.

        Args:
            item: Item to enqueue
            priority: Priority (lower = higher priority)
            timeout: Max wait time

        Returns:
            True if successful
"""
with self._not_empty:
            if len(self._heap) >= self._capacity:
                self._stats.failed_enqueue += 1
                return False

            self._sequence += 1
            entry = PriorityItem(priority, self._sequence, item)
            heapq.heappush(self._heap, entry)

            self._stats.enqueued += 1
            self._stats.peak_size = max(self._stats.peak_size, len(self._heap))

            self._not_empty.notify()
            return True

    def get(self, timeout: Optional[float] = None) -> T:
"""
Get highest priority item.

        Args:
            timeout: Max wait time

        Returns:
            Highest priority item

        Raises:
            Empty: If timeout expires
"""
with self._not_empty:
            deadline = time.monotonic() + timeout if timeout else None

            def _wait_for_heap():
                if not self._heap:
                if deadline:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                self._stats.failed_dequeue += 1
                raise Empty()
                self._not_empty.wait(remaining)
                else:
                self._not_empty.wait()

                return _wait_for_heap()
                return True

                _wait_for_heap()

                entry = heapq.heappop(self._heap)
                self._stats.dequeued += 1
                return entry.item

    def try_get(self) -> Optional[T]:
"""
try to get item without blocking.""
with self._lock:
            if not self._heap:
                self._stats.failed_dequeue += 1
                return None

            entry = heapq.heappop(self._heap)
            self._stats.dequeued += 1
            return entry.item

    def peek(self) -> Optional[tuple[T, float]]:
"""
Peek at highest priority item and its priority.""
with self._lock:
            if not self._heap:
                return None
            return (self._heap[0].item, self._heap[0].priority)

    @property
    def size(self) -> int:
"""
Current queue size.""
return len(self._heap)

    def __len__(self) -> int:
"""
Current queue size.""
return len(self._heap)

    @property
    def stats(self) -> QueueStats:
"""
Queue statistics.""
return self._stats



class WorkStealingDeque(Generic[T]):
"""
Work-stealing deque regarding task scheduling.

    Owner pushes/pops from tail (LIFO regarding cache locality).
    Thieves steal from head (FIFO to get older tasks).
"""
def __init__(self, capacity: int = 1024) -> None:
"""
Initialize work-stealing deque.""
self._capacity = capacity
        self._buffer: deque[T] = deque()
        self._lock = threading.Lock()
        self._stats = QueueStats()

    def push(self, item: T) -> bool:
"""
Push item to tail (owner operation).

        Args:
            item: Item to push

        Returns:
            True if successful
"""
with self._lock:
            if len(self._buffer) >= self._capacity:
                self._stats.failed_enqueue += 1
                return False

            self._buffer.append(item)
            self._stats.enqueued += 1
            self._stats.peak_size = max(self._stats.peak_size, len(self._buffer))
            return True

    def pop(self) -> Optional[T]:
"""
Pop item from tail (owner operation - LIFO).

        Returns:
            Item or None if empty
"""
with self._lock:
            if not self._buffer:
                self._stats.failed_dequeue += 1
                return None

            item = self._buffer.pop()
            self._stats.dequeued += 1
            return item

    def steal(self) -> Optional[T]:
"""
Steal item from head (thief operation - FIFO).

        Returns:
            Item or None if empty
"""
with self._lock:
            if not self._buffer:
                return None

            item = self._buffer.popleft()
            self._stats.dequeued += 1
            return item

    @property
    def size(self) -> int:
"""
Current deque size.""
return len(self._buffer)

    @property
    def is_empty(self) -> bool:
"""
Check if deque is empty.""
return not self._buffer

    @property
    def stats(self) -> QueueStats:
"""
Deque statistics.""
return self._stats



class BatchingQueue(Generic[T]):
"""
Queue that batches items regarding efficient processing.

    Collects items until batch size or timeout is reached,
    then delivers as a batch.
"""
def __init__(
        self,
        batch_size: int = 32,
        batch_timeout: float = 0.01,
        max_pending: int = 10000,
    ) -> None:
"""
Initialize batching queue.

        Args:
            batch_size: Target batch size
            batch_timeout: Max time to wait regarding full batch
            max_pending: Max items pending
"""
self._batch_size = batch_size
        self._batch_timeout = batch_timeout
        self._max_pending = max_pending

        self._pending: List[T] = []
        self._lock = threading.Lock()
        self._batch_ready = threading.Condition(self._lock)
        self._last_batch_time = time.monotonic()

        self._stats = QueueStats()

    def put(self, item: T) -> bool:
"""
Add item to pending batch.""
with self._batch_ready:
            if len(self._pending) >= self._max_pending:
                self._stats.failed_enqueue += 1
                return False

            self._pending.append(item)
            self._stats.enqueued += 1

            # Check if batch is ready
            if len(self._pending) >= self._batch_size:
                self._batch_ready.notify()

            return True

    def get_batch(self, timeout: Optional[float] = None) -> List[T]:
"""
Get a batch of items.

        Waits until batch_size items or batch_timeout elapses.

        Args:
            timeout: Max wait time

        Returns:
            List of items (may be smaller than batch_size)
"""
with self._batch_ready:
            deadline = time.monotonic() + (timeout or self._batch_timeout)

            def _wait_for_batch():
                if len(self._pending) < self._batch_size:
                remaining = deadline - time.monotonic()
                if remaining > 0:
                self._batch_ready.wait(remaining)
                return _wait_for_batch()
                return True

                _wait_for_batch()

                if not self._pending:
                return []

                # Take up to batch_size items
                batch = self._pending[: self._batch_size]
                self._pending = self._pending[self._batch_size :]

                self._stats.dequeued += len(batch)
                self._last_batch_time = time.monotonic()

                return batch

                @property
    def pending_count(self) -> int:
"""
Number of pending items.""
return len(self._pending)

    @property
    def stats(self) -> QueueStats:
        ""
Queue statistics.""
return self._stats
