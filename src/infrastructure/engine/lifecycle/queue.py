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
"""Request queue manager."""

import threading
from collections import deque
from typing import Dict, Iterable, List, Optional, Set, Union

from .enums import FinishReason, RequestEventType
from .request import Request


class RequestQueue:
    """
    Thread-safe queue for managing waiting and running requests.

    This class manages the lifecycle of requests as they move between
    waiting, running, and finished states.

    Attributes:
        waiting: Deque of waiting request IDs
        running: Set of running request IDs
        requests: Dict mapping request_id to Request
        finished: Set of finished request IDs (recent)
    """

    def __init__(self, max_finished_history: int = 1000) -> None:
        """
        Initialize the request queue.

        Args:
            max_finished_history: Maximum number of finished requests to track
        """
        self._lock = threading.RLock()
        self._waiting: deque = deque()
        self._running: Set[str] = set()
        self._request_map: Dict[str, Request] = {}
        self._finished: deque = deque(maxlen=max_finished_history)

    def add_request(self, request: Request) -> None:
        """Add a new request to the waiting queue."""
        with self._lock:
            if request.request_id in self._request_map:
                raise ValueError(f"Request {request.request_id} already exists")
            self._request_map[request.request_id] = request
            self._waiting.append(request.request_id)
            request.record_event(RequestEventType.QUEUED)

    def get_request(self, request_id: str) -> Optional[Request]:
        """Get a request by ID."""
        with self._lock:
            return self._request_map.get(request_id)

    def schedule_next(self, n: int = 1) -> List[Request]:
        """
        Schedule the next n waiting requests.

        Returns:
            List of requests that were scheduled
        """
        scheduled = []
        with self._lock:
            while len(scheduled) < n and self._waiting:
                request_id = self._waiting.popleft()
                request = self._request_map.get(request_id)
                if request and not request.is_finished():
                    request.start_running()
                    self._running.add(request_id)
                    scheduled.append(request)
        return scheduled

    def finish_request(
        self,
        request_id: str,
        reason: FinishReason,
        stop_reason: Optional[Union[int, str]] = None,
    ) -> Optional[Request]:
        """Mark a request as finished."""
        with self._lock:
            request = self._request_map.get(request_id)
            if request is None:
                return None

            request.finish(reason, stop_reason)
            self._running.discard(request_id)
            self._finished.append(request_id)
            return request

    def abort_request(self, request_id: str) -> Optional[Request]:
        """Abort a request."""
        with self._lock:
            request = self._request_map.get(request_id)
            if request is None:
                return None

            request.abort()
            self._waiting = deque(rid for rid in self._waiting if rid != request_id)
            self._running.discard(request_id)
            self._finished.append(request_id)
            return request

    def abort_requests(
        self,
        request_ids: Union[str, Iterable[str]],
    ) -> List[Request]:
        """Abort multiple requests."""
        if isinstance(request_ids, str):
            request_ids = [request_ids]

        aborted = []
        for request_id in request_ids:
            request = self.abort_request(request_id)
            if request:
                aborted.append(request)
        return aborted

    def preempt_request(self, request_id: str) -> Optional[Request]:
        """Preempt a running request back to waiting."""
        with self._lock:
            request = self._request_map.get(request_id)
            if request is None or not request.is_running():
                return None

            request.preempt()
            self._running.discard(request_id)
            self._waiting.appendleft(request_id)  # Add to front
            return request

    def get_num_waiting(self) -> int:
        """Get the number of waiting requests."""
        with self._lock:
            return len(self._waiting)

    def get_num_running(self) -> int:
        """Get the number of running requests."""
        with self._lock:
            return len(self._running)

    def get_num_unfinished(self) -> int:
        """Get total number of unfinished requests."""
        return self.get_num_waiting() + self.get_num_running()

    def has_unfinished_requests(self) -> bool:
        """Check if there are any unfinished requests."""
        return self.get_num_unfinished() > 0

    def get_waiting_requests(self) -> List[Request]:
        """Get all waiting requests (ordered)."""
        with self._lock:
            return [self._request_map[rid] for rid in self._waiting if rid in self._request_map]

    def get_running_requests(self) -> List[Request]:
        """Get all running requests."""
        with self._lock:
            return [self._request_map[rid] for rid in self._running if rid in self._request_map]

    def cleanup_finished(self, older_than_seconds: float = 3600.0) -> int:
        """
        Remove finished requests older than the threshold.

        Returns:
            Number of requests removed
        """
        import time as _time

        cutoff = _time.time() - older_than_seconds
        removed = 0
        with self._lock:
            to_remove = []
            for request_id in self._finished:
                request = self._request_map.get(request_id)
                if request and request.finished_time and request.finished_time < cutoff:
                    to_remove.append(request_id)

            for request_id in to_remove:
                del self._request_map[request_id]
                removed += 1
        return removed
