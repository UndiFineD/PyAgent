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


"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

import logging
import threading
import time
import uuid
from collections.abc import Callable
from queue import PriorityQueue

from src.core.base.lifecycle.version import VERSION
from src.infrastructure.compute.backend.local_context_recorder import \
    LocalContextRecorder

from .queued_request import QueuedRequest
from .request_priority import RequestPriority

# Infrastructure
__version__ = VERSION


class RequestQueue:
    """Priority queue for backend requests.

    Manages request ordering by priority and timestamp.
    Thread - safe for concurrent access.

    Example:
        queue=RequestQueue()
        queue.enqueue("prompt", RequestPriority.HIGH)
        request=queue.dequeue()
    """

    def __init__(self, max_size: int = 1000, recorder: LocalContextRecorder | None = None) -> None:
        """Initialize request queue.

        Args:
            max_size: Maximum queue size.
            recorder: Infrastructure recorder for intelligence harvesting.
        """
        self._queue: PriorityQueue[QueuedRequest] = PriorityQueue(maxsize=max_size)
        self.recorder = recorder
        self._lock = threading.Lock()
        self._pending: dict[str, QueuedRequest] = {}

    def enqueue(
        self,
        prompt: str,
        priority: RequestPriority = RequestPriority.NORMAL,
        callback: Callable[[str], None] | None = None,
    ) -> str:
        """Add request to queue.

        Args:
            prompt: The prompt to queue.
            priority: Request priority level.
            callback: Optional callback when processed.

        Returns:
            str: Request ID for tracking.
        """
        request_id = str(uuid.uuid4())
        request = QueuedRequest(
            priority=priority.value,
            timestamp=time.time(),
            request_id=request_id,
            prompt=prompt,
            callback=callback,
        )

        with self._lock:
            self._queue.put(request)
            self._pending[request_id] = request

        if self.recorder:
            self.recorder.record_lesson("request_queued", {"id": request_id, "priority": priority.name})

        logging.debug(f"Queued request {request_id} with priority {priority.name}")
        return request_id

    def dequeue(self, timeout: float | None = None) -> QueuedRequest | None:
        """Get next request from queue.

        Args:
            timeout: Maximum wait time in seconds.

        Returns:
            Optional[QueuedRequest]: Next request or None if empty / timeout.
        """
        try:
            request = self._queue.get(timeout=timeout)
            with self._lock:
                self._pending.pop(request.request_id, None)
            return request
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            return None

    def size(self) -> int:
        """Get current queue size."""
        return self._queue.qsize()

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self._queue.empty()

    def get_pending(self, request_id: str) -> QueuedRequest | None:
        """Get pending request by ID."""
        with self._lock:
            return self._pending.get(request_id)
