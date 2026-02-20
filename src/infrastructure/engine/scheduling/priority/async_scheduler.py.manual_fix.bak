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


"""
Async scheduler.py module.

"""

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

import asyncio
import time
from typing import Any, Coroutine, Dict, Optional, TypeVar

from .enums import TaskPriority
from .models import TaskStats

R = TypeVar("R")


class AsyncPriorityScheduler:
        Async priority scheduler for coroutine-based workloads.
    
    def __init__(self, max_concurrent: int = 100) -> None:
                Initialize async scheduler.

        Args:
            max_concurrent: Maximum concurrent tasks
                self._max_concurrent: int = max_concurrent
        self._semaphore = asyncio.Semaphore(max_concurrent)

        self._queues: Dict[TaskPriority, asyncio.PriorityQueue] = {}
        self._stats = TaskStats()
        self._sequence = 0
        self._lock = asyncio.Lock()

    async def submit(
        self,
        coro: Coroutine[Any, Any, R],
        _priority: TaskPriority = TaskPriority.NORMAL,
        deadline_ms: Optional[float] = None,
    ) -> R:
                Submit and await a coroutine.

        Args:
            coro: Coroutine to execute
            priority: Task priority
            deadline_ms: Deadline in milliseconds

        Returns:
            Coroutine result
                async with self._semaphore:
            start: float = time.monotonic()

            timeout = None
            if deadline_ms:
                timeout: float = deadline_ms / 1000.0

            try:
                if timeout:
                    result: R = await asyncio.wait_for(coro, timeout=timeout)
                else:
                    result: R = await coro

                exec_time: float = (time.monotonic() - start) * 1000
                async with self._lock:
                    self._stats.completed += 1
                    self._stats.total_exec_time_ms += exec_time

                return result

            except asyncio.TimeoutError:
                async with self._lock:
                    self._stats.timeouts += 1
                raise

            except Exception:  # pylint: disable=broad-exception-caught
                async with self._lock:
                    self._stats.failed += 1
                raise

    @property
    def stats(self) -> TaskStats:
"""
Scheduler statistics.        return self._stats

"""
