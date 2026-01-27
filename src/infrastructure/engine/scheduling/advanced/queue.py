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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Priority queue implementation for request scheduling."""

import heapq
import threading
import time
from typing import Optional

from .config import RequestState
from .request import ScheduledRequest


class PriorityRequestQueue:
    """Heap-based priority queue for inference requests."""

    def __init__(self, enable_starvation_prevention: bool = True) -> None:
        """Initialize priority queue."""
        self.enable_starvation_prevention = enable_starvation_prevention
        self._heap: list[tuple[float, float, float, int, ScheduledRequest]] = []
        self._sequence = 0
        self._lock = threading.Lock()
        self._request_map: dict[str, ScheduledRequest] = {}

        # Starvation prevention
        self._age_interval = 1.0  # seconds
        self._max_age = 10.0  # seconds before priority boost
        self._last_age_time = time.time()

    def _get_priority_score(self, request: ScheduledRequest) -> float:
        """Calculate priority score for heap ordering."""
        base_priority = request.priority.value

        if request.deadline is not None:
            time_to_deadline = request.deadline - time.time()
            if time_to_deadline < 0:
                return -1000  # Overdue
            deadline_factor = 1.0 / max(time_to_deadline, 0.001)
            return base_priority - min(deadline_factor * 10, 2.0)

        return float(base_priority)

    def push(self, request: ScheduledRequest) -> None:
        """Add request to queue."""
        with self._lock:
            self._sequence += 1
            request.sequence = self._sequence

            priority_score = self._get_priority_score(request)
            deadline = request.deadline if request.deadline else float("inf")

            entry = (
                priority_score,
                deadline,
                request.arrival_time,
                self._sequence,
                request,
            )
            heapq.heappush(self._heap, entry)
            self._request_map[request.request_id] = request

    def pop(self) -> Optional[ScheduledRequest]:
        """Remove and return highest priority request."""
        with self._lock:
            self._maybe_age_priorities()

            while self._heap:
                entry = heapq.heappop(self._heap)
                request = entry[4]

                if request.request_id not in self._request_map:
                    continue

                if request.state not in (RequestState.WAITING, RequestState.PREEMPTED):
                    continue

                del self._request_map[request.request_id]
                return request

            return None

    def peek(self) -> Optional[ScheduledRequest]:
        """Return highest priority request without removing."""
        with self._lock:
            for entry in self._heap:
                request = entry[4]
                if request.request_id in self._request_map:
                    if request.state in (RequestState.WAITING, RequestState.PREEMPTED):
                        return request
            return None

    def remove(self, request_id: str) -> Optional[ScheduledRequest]:
        """Remove request by ID (lazy removal)."""
        with self._lock:
            if request_id in self._request_map:
                request = self._request_map.pop(request_id)
                return request
            return None

    def _maybe_age_priorities(self) -> None:
        """Apply priority aging to prevent starvation."""
        if not self.enable_starvation_prevention:
            return

        now = time.time()
        if now - self._last_age_time < self._age_interval:
            return

        self._last_age_time = now

        new_heap: list[tuple[float, float, float, int, ScheduledRequest]] = []

        for entry in self._heap:
            request = entry[4]
            if request.request_id not in self._request_map:
                continue

            age = now - request.arrival_time
            if age > self._max_age:
                boost = min((age - self._max_age) / self._max_age, 1.0)
                new_priority = self._get_priority_score(request) - boost
            else:
                new_priority = entry[0]

            new_heap.append(
                (
                    new_priority,
                    entry[1],
                    entry[2],
                    entry[3],
                    request,
                )
            )

        heapq.heapify(new_heap)
        self._heap = new_heap

    def __len__(self) -> int:
        """Number of requests in queue."""
        with self._lock:
            return len(self._request_map)

    def __bool__(self) -> bool:
        """Whether queue has requests."""
        return bool(len(self))
