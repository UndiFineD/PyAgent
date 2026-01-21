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
from src.core.base.lifecycle.version import VERSION
from .batch_request import BatchRequest
import threading
import time
from src.infrastructure.compute.backend.local_context_recorder import LocalContextRecorder

# Infrastructure
__version__ = VERSION


class RequestBatcher:
    """Batches multiple requests for efficient processing.

    Collects requests and processes them together when batch
    size or timeout is reached.

    Example:
        batcher=RequestBatcher(batch_size=10, timeout_s=5.0)
        batcher.add("prompt1")
        batcher.add("prompt2")
        batch=batcher.get_batch()  # Returns when ready
    """

    def __init__(
        self,
        batch_size: int = 10,
        timeout_s: float = 5.0,
        recorder: LocalContextRecorder | None = None,
    ) -> None:
        """Initialize request batcher.

        Args:
            batch_size: Requests per batch.
            timeout_s: Max wait time before processing partial batch.
            recorder: Infrastructure recorder for intelligence harvesting.
        """
        self.batch_size = batch_size
        self.timeout_s = timeout_s
        self.recorder = recorder
        self._buffer: list[str] = []
        self._lock = threading.Lock()
        self._batch_start: float | None = None

    def add(self, prompt: str) -> bool:
        """Add request to current batch.

        Args:
            prompt: Request prompt.

        Returns:
            bool: True if batch is now ready.
        """
        with self._lock:
            if not self._buffer:
                self._batch_start = time.time()
            self._buffer.append(prompt)
            return len(self._buffer) >= self.batch_size

    def is_ready(self) -> bool:
        """Check if batch is ready for processing."""
        with self._lock:
            if len(self._buffer) >= self.batch_size:
                return True
            if (
                self._batch_start
                and (time.time() - self._batch_start) >= self.timeout_s
            ):
                return bool(self._buffer)
            return False

    def get_batch(self) -> BatchRequest | None:
        """Get current batch and reset buffer.

        Returns:
            Optional[BatchRequest]: Current batch or None if empty.
        """
        with self._lock:
            if not self._buffer:
                return None

            if self.recorder:
                self.recorder.record_lesson(
                    "batch_created", {"size": len(self._buffer)}
                )

            batch = BatchRequest(requests=self._buffer.copy())
            self._buffer.clear()
            self._batch_start = None
            return batch

    def pending_count(self) -> int:
        """Get number of pending requests."""
        with self._lock:
            return len(self._buffer)
