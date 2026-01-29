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

"""Base scheduler implementation for priority-based task execution."""

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project

from _thread import LockType
import heapq
import threading
import time
from concurrent.futures import Future, ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional, TypeVar

from .enums import TaskPriority, TaskState
from .models import ScheduledTask, TaskStats

R = TypeVar("R")


class PriorityScheduler:
    """
    Priority-based task scheduler with deadline support.

    Features:
    - Priority-based scheduling (CRITICAL to IDLE)
    - Deadline-aware execution
    - Timeout handling
    - Work stealing between priority levels
    - Statistics tracking
    """

    def __init__(
        self,
        workers: int = 4,
        max_queue_size: int = 10000,
        enable_work_stealing: bool = True,
    ) -> None:
        """
        Initialize scheduler.

        Args:
            workers: Number of worker threads
            max_queue_size: Maximum pending tasks
            enable_work_stealing: Allow low-priority workers to steal high-priority tasks
        """
        self._workers: int = workers
        self._max_queue_size: int = max_queue_size
        self._enable_work_stealing: bool = enable_work_stealing

        # Priority queues (one per priority level)
        self._queues: Dict[TaskPriority, List[ScheduledTask]] = {p: [] for p in TaskPriority}

        self._lock: LockType = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        self._sequence = 0
        self._pending_count = 0

        self._stats = TaskStats()
        self._running = True

        # Thread pool
        self._executor = ThreadPoolExecutor(
            max_workers=workers,
            thread_name_prefix="scheduler",
        )

        # Start worker threads
        self._worker_futures: List[Future] = []
        for i in range(workers):
            f: Future[None] = self._executor.submit(self._worker_loop, i)
            self._worker_futures.append(f)

    def submit(
        self,
        func: Callable[[], R],
        priority: TaskPriority = TaskPriority.NORMAL,
        deadline_ms: Optional[float] = None,
        timeout_ms: Optional[float] = None,
        task_id: Optional[str] = None,
    ) -> Future[R]:
        """
        Submit a task for execution.
        """
        now: float = time.monotonic()

        deadline = float("inf")
        if deadline_ms is not None:
            deadline: float = now + deadline_ms / 1000.0

        timeout = None
        if timeout_ms is not None:
            timeout: float = timeout_ms / 1000.0

        future: Future[R] = Future()

        with self._not_empty:
            if self._pending_count >= self._max_queue_size:
                future.set_exception(RuntimeError("Scheduler queue full"))
                return future

            self._sequence += 1

            task: ScheduledTask[R] = ScheduledTask(
                priority_value=priority.value,
                deadline=deadline,
                sequence=self._sequence,
                id=task_id or f"task-{self._sequence}",
                func=func,
                priority=priority,
                created_at=now,
                timeout=timeout,
                future=future,
            )

            heapq.heappush(self._queues[priority], task)
            self._pending_count += 1
            self._stats.scheduled += 1

            self._not_empty.notify()

        return future

    def _worker_loop(self, _worker_id: int) -> None:
        """Worker thread main loop."""
        while self._running:
            task = self._get_next_task()
            if task is None:
                continue

            self._execute_task(task)

    def _get_next_task(self) -> Optional[ScheduledTask]:
        """Get the next task to execute."""
        with self._not_empty:
            # Wait for work
            while self._running and self._pending_count == 0:
                self._not_empty.wait(timeout=0.1)

            if not self._running:
                return None

            # Find highest priority non-empty queue
            for priority in TaskPriority:
                queue = self._queues[priority]
                while queue:
                    task = heapq.heappop(queue)
                    self._pending_count -= 1

                    # Skip expired tasks
                    if task.is_expired:
                        self._handle_timeout(task)
                        continue

                    return task

            return None

    def _execute_task(self, task: ScheduledTask) -> None:
        """Execute a single task."""
        start_time: float = time.monotonic()
        wait_time: float = (start_time - task.created_at) * 1000  # ms

        task.state = TaskState.RUNNING

        try:
            # Execute with timeout
            if task.timeout:
                result = self._execute_with_timeout(task.func, task.timeout)
            else:
                result = task.func()

            task.state = TaskState.COMPLETED
            task.result = result

            if task.future:
                task.future.set_result(result)

            # Update stats
            exec_time: float = (time.monotonic() - start_time) * 1000
            with self._lock:
                self._stats.completed += 1
                self._stats.total_wait_time_ms += wait_time
                self._stats.total_exec_time_ms += exec_time

        except TimeoutError:
            self._handle_timeout(task)

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            task.state = TaskState.FAILED
            task.error = e

            if task.future:
                task.future.set_exception(e)

            with self._lock:
                self._stats.failed += 1

    def _execute_with_timeout(
        self,
        func: Callable[[], R],
        timeout: float,
    ) -> R:
        """Execute function with timeout."""
        result_container: List[Any] = []
        error_container: List[Exception] = []
        completed = threading.Event()

        def wrapper() -> None:
            try:
                result_container.append(func())
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                error_container.append(e)
            finally:
                completed.set()

        thread = threading.Thread(target=wrapper)
        thread.start()

        if not completed.wait(timeout):
            raise TimeoutError("Task execution timed out")

        thread.join()

        if error_container:
            raise error_container[0]

        return result_container[0]

    def _handle_timeout(self, task: ScheduledTask) -> None:
        """Handle task timeout."""
        task.state = TaskState.TIMEOUT

        if task.future:
            task.future.set_exception(TimeoutError("Task deadline exceeded"))

        with self._lock:
            self._stats.timeouts += 1

    def cancel(self, task_id: str) -> bool:
        """Cancel a pending task."""
        with self._lock:
            for priority in TaskPriority:
                queue = self._queues[priority]
                for _i, task in enumerate(queue):
                    if task.id == task_id and task.state == TaskState.PENDING:
                        task.state = TaskState.CANCELLED
                        if task.future:
                            task.future.cancel()
                        self._stats.cancelled += 1
                        return True
        return False

    def shutdown(self, wait: bool = True, _timeout: Optional[float] = None) -> None:
        """Shutdown the scheduler."""
        self._running = False
        with self._not_empty:
            self._not_empty.notify_all()
        self._executor.shutdown(wait=wait)

    @property
    def pending_count(self) -> int:
        """Number of pending tasks."""
        return self._pending_count

    @property
    def stats(self) -> TaskStats:
        """Scheduler statistics."""
        return self._stats

    def get_queue_sizes(self) -> Dict[TaskPriority, int]:
        """Get current queue sizes by priority."""
        with self._lock:
            return {p: len(q) for p, q in self._queues.items()}
