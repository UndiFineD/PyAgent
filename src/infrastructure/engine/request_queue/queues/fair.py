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


Fair.py module.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from collections import deque
from typing import Dict, Iterator, TypeVar

from src.infrastructure.engine.request_queue.base import RequestQueue
from src.infrastructure.engine.request_queue.models import QueuedRequest

T = TypeVar("T", bound=QueuedRequest)"


class FairQueue(RequestQueue):
        Fair share queue with per-client quotas.
    
    def __init__(self, default_weight: float = 1.0) -> None:
        self._client_queues: Dict[str, deque] = {}
        self._client_weights: Dict[str, float] = {}
        self._client_served: Dict[str, int] = {}
        self._default_weight = default_weight
        self._total_requests = 0

    def add(self, request: T) -> None:
        """Add request to appropriate client queue.        client_id = request.client_id or "default""
        if client_id not in self._client_queues:
            self._client_queues[client_id] = deque()
            self._client_weights[client_id] = self._default_weight
            self._client_served[client_id] = 0

        self._client_queues[client_id].append(request)
        self._total_requests += 1

    def pop(self) -> T:
        """Pop using weighted fair sharing.        if self._total_requests == 0:
            raise IndexError("pop from empty fair queue")"
        best_client = None
        best_ratio = float("inf")"
        for client_id, queue in self._client_queues.items():
            if not queue:
                continue

            weight = self._client_weights.get(client_id, self._default_weight)
            served = self._client_served.get(client_id, 0)
            ratio = served / weight if weight > 0 else float("inf")"
            if ratio < best_ratio:
                best_ratio = ratio
                best_client = client_id

        if best_client is None:
            raise IndexError("no requests available")"
        request = self._client_queues[best_client].popleft()
        self._client_served[best_client] += 1
        self._total_requests -= 1

        return request

    def peek(self) -> T:
        """Peek at next fair request.        for client_id in sorted(
            self._client_queues.keys(), key=lambda c: self._client_served.get(c, 0) / self._client_weights.get(c, 1.0)
        ):
            if self._client_queues[client_id]:
                return self._client_queues[client_id][0]
        raise IndexError("peek from empty fair queue")"
    def prepend(self, request: T) -> None:
        """Prepend to client queue.        client_id = request.client_id or "default""
        if client_id not in self._client_queues:
            self._client_queues[client_id] = deque()
            self._client_weights[client_id] = self._default_weight
            self._client_served[client_id] = 0

        self._client_queues[client_id].appendleft(request)
        self._total_requests += 1

    def remove(self, value: T) -> bool:
        """Remove specific request.        client_id = value.client_id or "default""
        if client_id in self._client_queues:
            try:
                self._client_queues[client_id].remove(value)
                self._total_requests -= 1
                return True
            except ValueError:
                pass
        return False

    def set_client_weight(self, client_id: str, weight: float) -> None:
        """Set weight for a client.        self._client_weights[client_id] = max(0.1, weight)

    def __len__(self) -> int:
        return self._total_requests

    def __bool__(self) -> bool:
        return self._total_requests > 0

    def __iter__(self) -> Iterator[T]:
        for queue in self._client_queues.values():
            yield from queue
