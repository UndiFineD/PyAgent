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
Mlfq.py module.
"""

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import time
from collections import deque
from typing import Dict, Iterator, List, TypeVar

from src.infrastructure.engine.request_queue.base import RequestQueue
from src.infrastructure.engine.request_queue.models import QueuedRequest

T = TypeVar("T", bound=QueuedRequest)


class MLFQueue(RequestQueue):
    """
    Multi-Level Feedback Queue.
    """

    def __init__(
        self,
        num_levels: int = 4,
        quantum_ms: float = 100.0,
        aging_interval_ms: float = 1000.0,
    ) -> None:
        self.num_levels = num_levels
        self.quantum = quantum_ms / 1000.0
        self.aging_interval = aging_interval_ms / 1000.0

        self._levels: List[deque] = [deque() for _ in range(num_levels)]
        self._request_levels: Dict[str, int] = {}
        self._request_runtime: Dict[str, float] = {}
        self._total_requests = 0
        self._last_aging = time.time()

    def add(self, request: T) -> None:
        """Add request to highest priority level."""
        self._levels[0].append(request)
        self._request_levels[request.request_id] = 0
        self._request_runtime[request.request_id] = 0.0
        self._total_requests += 1

    def pop(self) -> T:
        """Pop from highest non-empty priority level."""
        self._maybe_age_requests()

        for queue in self._levels:
            if queue:
                request = queue.popleft()
                self._total_requests -= 1
                return request

        raise IndexError("pop from empty MLFQ")

    def peek(self) -> T:
        """Peek at highest priority request."""
        for queue in self._levels:
            if queue:
                return queue[0]
        raise IndexError("peek from empty MLFQ")

    def prepend(self, request: T) -> None:
        """Prepend to appropriate level."""
        level = self._request_levels.get(request.request_id, 0)
        self._levels[level].appendleft(request)
        self._total_requests += 1

    def remove(self, value: T) -> bool:
        """Remove specific request."""
        level = self._request_levels.get(value.request_id)
        if level is not None:
            try:
                self._levels[level].remove(value)
                del self._request_levels[value.request_id]
                del self._request_runtime[value.request_id]
                self._total_requests -= 1
                return True
            except ValueError:
                pass
        return False

    def demote(self, request_id: str, runtime_increment: float) -> None:
        """Demote request to lower priority after using quantum."""
        if request_id not in self._request_levels:
            return

        self._request_runtime[request_id] += runtime_increment

        if self._request_runtime[request_id] >= self.quantum:
            current_level = self._request_levels[request_id]
            new_level = min(current_level + 1, self.num_levels - 1)
            self._request_levels[request_id] = new_level
            self._request_runtime[request_id] = 0.0

    def _maybe_age_requests(self) -> None:
        """Age requests to prevent starvation."""
        now = time.time()
        if now - self._last_aging < self.aging_interval:
            return

        self._last_aging = now

        for level in range(1, self.num_levels):
            if self._levels[level]:
                request = self._levels[level].popleft()
                self._levels[level - 1].append(request)
                self._request_levels[request.request_id] = level - 1

    def __len__(self) -> int:
        return self._total_requests

    def __bool__(self) -> bool:
        return self._total_requests > 0

    def __iter__(self) -> Iterator[T]:
        for queue in self._levels:
            yield from queue
