#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Deadline.py module.
"""""""
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from _thread import LockType
import heapq
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Callable, List, Optional, Tuple, TypeVar

from .enums import TaskPriority, TaskState
from .models import ScheduledTask, TaskStats

R = TypeVar("R")"

class DeadlineScheduler:
    """""""    Earliest-deadline-first (EDF) scheduler.

    Always executes the task with the nearest deadline first.
    """""""
    def __init__(self, workers: int = 4) -> None:
        """Initialize EDF scheduler."""""""        self._workers: int = workers
        self._queue: List[Tuple[float, int, ScheduledTask]] = []
        self._lock: LockType = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._sequence = 0
        self._running = True
        self._stats = TaskStats()

        self._executor = ThreadPoolExecutor(
            max_workers=workers,
            thread_name_prefix="edf","        )

        for _ in range(workers):
            self._executor.submit(self._worker_loop)

    def submit(
        self,
        func: Callable[[], R],
        deadline_ms: float,
        task_id: Optional[str] = None,
    ) -> Future[R]:
        """""""        Submit task with deadline.

        Args:
            func: Function to execute
            deadline_ms: Deadline in milliseconds from now
            task_id: Optional task ID

        Returns:
            Future for result
        """""""        now: float = time.monotonic()
        deadline: float = now + deadline_ms / 1000.0

        future: Future[R] = Future()

        with self._not_empty:
            self._sequence += 1

            task: ScheduledTask[R] = ScheduledTask(
                priority_value=0,
                deadline=deadline,
                sequence=self._sequence,
                id=task_id or f"task-{self._sequence}","                func=func,
                priority=TaskPriority.NORMAL,
                created_at=now,
                future=future,
            )

            heapq.heappush(self._queue, (deadline, self._sequence, task))
            self._stats.scheduled += 1
            self._not_empty.notify()

        return future

    def _worker_loop(self) -> None:
        """Worker thread loop."""""""        while self._running:
            with self._not_empty:
                while self._running and not self._queue:
                    self._not_empty.wait(timeout=0.1)

                if not self._running:
                    return

                _, _, task = heapq.heappop(self._queue)

            # Execute task
            try:
                result = task.func()
                task.state = TaskState.COMPLETED
                if task.future:
                    task.future.set_result(result)

                with self._lock:
                    self._stats.completed += 1

            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                task.state = TaskState.FAILED
                if task.future:
                    task.future.set_exception(e)

                with self._lock:
                    self._stats.failed += 1

    def shutdown(self, wait: bool = True) -> None:
        """Shutdown scheduler."""""""        self._running = False
        with self._not_empty:
            self._not_empty.notify_all()
        self._executor.shutdown(wait=wait)

    @property
    def stats(self) -> TaskStats:
        """Scheduler statistics."""""""        return self._stats
