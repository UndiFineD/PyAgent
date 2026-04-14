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
"""Core async task queue utilities."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class TaskQueue:
    """Simple FIFO async-friendly queue wrapper.

    Provides a thin typed wrapper over ``asyncio.Queue`` with common queue
    inspection and lifecycle helpers used across core workflow modules.
    """

    maxsize: int = 0

    _queue: Optional[asyncio.Queue[Any]] = None

    def __post_init__(self) -> None:
        """Post-init to ensure the queue is created lazily."""
        if self._queue is None:
            self._queue = asyncio.Queue[Any](maxsize=self.maxsize)

    async def put(self, item: Any) -> None:
        """Put an item into the queue."""
        assert self._queue is not None  # noqa: S101
        await self._queue.put(item)

    async def get(self) -> Any:
        """Get an item from the queue."""
        assert self._queue is not None  # noqa: S101
        return await self._queue.get()

    def qsize(self) -> int:
        """Return the current queue size."""
        assert self._queue is not None  # noqa: S101
        return self._queue.qsize()

    def empty(self) -> bool:
        """Return whether the queue is currently empty."""
        assert self._queue is not None  # noqa: S101
        return self._queue.empty()

    def full(self) -> bool:
        """Return whether the queue reached maxsize."""
        assert self._queue is not None  # noqa: S101
        return self._queue.full()

    def task_done(self) -> None:
        """Indicate a formerly enqueued task is complete."""
        assert self._queue is not None  # noqa: S101
        self._queue.task_done()

    async def join(self) -> None:
        """Block until all queued tasks are marked done."""
        assert self._queue is not None  # noqa: S101
        await self._queue.join()


def validate() -> None:
    """Lightweight import-safe validation hook."""
    q = TaskQueue()
    if not hasattr(q, "put") or not hasattr(q, "get"):
        raise RuntimeError("TaskQueue missing core put/get methods")
    if q.qsize() != 0 or not q.empty():
        raise RuntimeError("TaskQueue initial state is invalid")
