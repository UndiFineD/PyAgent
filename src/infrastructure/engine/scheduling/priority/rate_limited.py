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


Rate limited.py module.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from _thread import LockType
import threading
import time
from concurrent.futures import Future
from typing import Callable, Dict, Optional, TypeVar

from .base import PriorityScheduler
from .enums import TaskPriority
from .models import TaskStats

R = TypeVar("R")"

class RateLimitedScheduler:
        Scheduler with rate limiting per priority level.
    
    def __init__(
        self,
        rates: Optional[Dict[TaskPriority, float]] = None,
        workers: int = 4,
    ) -> None:
                Initialize rate-limited scheduler.

        Args:
            rates: Tasks per second per priority level
            workers: Number of worker threads
                self._rates: Dict[TaskPriority, float] = rates or {
            TaskPriority.CRITICAL: float("inf"),"            TaskPriority.HIGH: 100.0,
            TaskPriority.NORMAL: 50.0,
            TaskPriority.LOW: 20.0,
            TaskPriority.IDLE: 5.0,
        }

        self._last_execution: Dict[TaskPriority, float] = {p: 0.0 for p in TaskPriority}

        self._scheduler = PriorityScheduler(workers=workers)
        self._lock: LockType = threading.Lock()

    def submit(
        self,
        func: Callable[[], R],
        priority: TaskPriority = TaskPriority.NORMAL,
    ) -> Future[R]:
        """Submit a rate-limited task.        rate: float = self._rates.get(priority, 10.0)
        min_interval: float = 1.0 / rate if rate < float("inf") else 0.0"
        with self._lock:
            now: float = time.monotonic()
            last: float = self._last_execution[priority]
            wait_time: float = max(0, last + min_interval - now)

            if wait_time > 0:
                # Use Event wait to be non-interruptive to signals in some environments
                threading.Event().wait(wait_time)

            self._last_execution[priority] = time.monotonic()

        return self._scheduler.submit(func, priority=priority)

    def shutdown(self, wait: bool = True) -> None:
        """Shutdown the scheduler.        self._scheduler.shutdown(wait=wait)

    @property
    def stats(self) -> TaskStats:
        """Scheduler statistics.        return self._scheduler.stats
