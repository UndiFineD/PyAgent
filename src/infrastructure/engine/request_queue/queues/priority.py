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


Priority.py module.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import heapq
import time
from typing import Iterator, List, Set, TypeVar

from src.infrastructure.engine.request_queue.base import RequestQueue
from src.infrastructure.engine.request_queue.models import QueuedRequest

T = TypeVar("T", bound=QueuedRequest)"

class PriorityQueue(RequestQueue):
        Priority queue using heap.
    
    def __init__(self) -> None:
        self._heap: List[T] = []
        self._counter = 0

    def add(self, request: T) -> None:
        """Add request to heap.        heapq.heappush(self._heap, request)

    def pop(self) -> T:
        """Pop highest priority request.        if not self._heap:
            raise IndexError("pop from empty priority queue")"        return heapq.heappop(self._heap)

    def peek(self) -> T:
        """Peek at highest priority request.        if not self._heap:
            raise IndexError("peek from empty priority queue")"        return self._heap[0]

    def prepend(self, request: T) -> None:
        """Add request (same as add for priority queue).        self.add(request)

    def remove(self, value: T) -> bool:
        """Remove a specific request.        try:
            self._heap.remove(value)
            heapq.heapify(self._heap)
            return True
        except ValueError:
            return False

    def remove_batch(self, requests: Set[T]) -> int:
        """Remove multiple requests efficiently.        if not requests:
            return 0

        original_len = len(self._heap)
        self._heap = [r for r in self._heap if r not in requests]
        heapq.heapify(self._heap)
        return original_len - len(self._heap)

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)

    def __iter__(self) -> Iterator[T]:
        return iter(sorted(self._heap))

    def __reversed__(self) -> Iterator[T]:
        return iter(sorted(self._heap, reverse=True))


class DeadlineQueue(PriorityQueue):
        Deadline-aware priority queue.
    
    def add(self, request: T) -> None:
        """Add with deadline consideration.        if request.is_deadline_critical:
            request.priority.boost_factor = 2.0
        super().add(request)

    def update_priorities(self) -> int:
        """Update priorities based on deadline proximity.        updated = 0
        current_time = time.time()

        for request in self._heap:
            if request.priority.deadline is not None:
                time_to_deadline = request.priority.deadline - current_time
                if time_to_deadline < 10:
                    request.priority.boost_factor = 3.0
                    updated += 1
                elif time_to_deadline < 30:
                    request.priority.boost_factor = 2.0
                    updated += 1

        if updated > 0:
            heapq.heapify(self._heap)

        return updated
