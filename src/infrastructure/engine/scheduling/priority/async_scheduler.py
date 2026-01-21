# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import asyncio
import time
from typing import (
    Any,
    Coroutine,
    Dict,
    Optional,
    TypeVar,
)
from .enums import TaskPriority
from .models import TaskStats

R = TypeVar('R')

class AsyncPriorityScheduler:
    """
    Async priority scheduler for coroutine-based workloads.
    """

    def __init__(self, max_concurrent: int = 100):
        """
        Initialize async scheduler.

        Args:
            max_concurrent: Maximum concurrent tasks
        """
        self._max_concurrent = max_concurrent
        self._semaphore = asyncio.Semaphore(max_concurrent)

        self._queues: Dict[TaskPriority, asyncio.PriorityQueue] = {}
        self._stats = TaskStats()
        self._sequence = 0
        self._lock = asyncio.Lock()

    async def submit(
        self,
        coro: Coroutine[Any, Any, R],
        priority: TaskPriority = TaskPriority.NORMAL,
        deadline_ms: Optional[float] = None,
    ) -> R:
        """
        Submit and await a coroutine.

        Args:
            coro: Coroutine to execute
            priority: Task priority
            deadline_ms: Deadline in milliseconds

        Returns:
            Coroutine result
        """
        async with self._semaphore:
            start = time.monotonic()

            timeout = None
            if deadline_ms:
                timeout = deadline_ms / 1000.0

            try:
                if timeout:
                    result = await asyncio.wait_for(coro, timeout=timeout)
                else:
                    result = await coro

                exec_time = (time.monotonic() - start) * 1000
                async with self._lock:
                    self._stats.completed += 1
                    self._stats.total_exec_time_ms += exec_time

                return result

            except asyncio.TimeoutError:
                async with self._lock:
                    self._stats.timeouts += 1
                raise

            except Exception:
                async with self._lock:
                    self._stats.failed += 1
                raise

    @property
    def stats(self) -> TaskStats:
        """Scheduler statistics."""
        return self._stats
