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

"""
Multiproc logic.py module.
"""

from __future__ import annotations

import contextlib
import multiprocessing as mp
import queue
import signal
import threading
import time
import traceback
from typing import Any, Callable, Dict, List, Optional

from src.infrastructure.services.executor.multiproc.base import Executor
from src.infrastructure.services.executor.multiproc.future import FutureWrapper
from src.infrastructure.services.executor.multiproc.types import (
    ResultMessage, TaskMessage, WorkerInfo, WorkerState)


class MultiprocExecutor(Executor):
    """
    Multiprocess executor (vLLM MultiprocExecutor equivalent).
    """

    uses_ray = False
    supports_pp = True
    supports_tp = False

    def __init__(
        self,
        num_workers: int = 4,
        functions: Dict[str, Callable] = None,
        heartbeat_interval: float = 5.0,
        worker_timeout: float = 30.0,
    ):
        self._num_workers = num_workers
        self._functions = functions or {}
        self._heartbeat_interval = heartbeat_interval
        self._worker_timeout = worker_timeout

        # Worker management
        self._workers: Dict[int, mp.Process] = {}
        self._worker_info: Dict[int, WorkerInfo] = {}

        # Communication queues
        self._task_queue: Optional[mp.Queue] = None
        self._result_queue: Optional[mp.Queue] = None
        self._control_queues: Dict[int, mp.Queue] = {}

        # Task tracking
        self._pending_tasks: Dict[str, FutureWrapper[Any]] = {}
        self._task_counter = 0

        # Threading
        self._result_thread: Optional[threading.Thread] = None
        self._monitor_thread: Optional[threading.Thread] = None
        self._shutdown_event = threading.Event()
        self._lock = threading.Lock()

        self._started = False

    def register_function(self, name: str, func: Callable) -> None:
        """Register a function for workers to execute."""
        self._functions[name] = func

    def start(self) -> None:
        """Start the executor."""
        if self._started:
            return

        # Create queues
        self._task_queue = mp.Queue()
        self._result_queue = mp.Queue()

        # Start workers
        for worker_id in range(self._num_workers):
            self._start_worker(worker_id)

        # Start result collector thread
        self._result_thread = threading.Thread(
            target=self._collect_results,
            daemon=True,
        )
        self._result_thread.start()

        # Start monitor thread
        self._monitor_thread = threading.Thread(
            target=self._monitor_workers,
            daemon=True,
        )
        self._monitor_thread.start()

        self._started = True

    def _start_worker(self, worker_id: int) -> None:
        """Start a worker process."""
        control_queue = mp.Queue()
        self._control_queues[worker_id] = control_queue

        process = mp.Process(
            target=self._worker_loop,
            args=(worker_id, self._task_queue, self._result_queue, control_queue, self._functions),
            daemon=True,
        )
        process.start()

        self._workers[worker_id] = process
        self._worker_info[worker_id] = WorkerInfo(
            worker_id=worker_id,
            pid=process.pid,
            state=WorkerState.STARTING,
            start_time=time.time(),
            last_heartbeat=time.time(),
        )

    @staticmethod
    def _worker_loop(
        worker_id: int,
        task_queue: mp.Queue,
        result_queue: mp.Queue,
        control_queue: mp.Queue,
        functions: Dict[str, Callable],
    ) -> None:
        """Worker process main loop."""
        # Set up signal handlers
        signal.signal(signal.SIGTERM, lambda *_: None)

        while True:
            try:
                # Check for control messages (non-blocking)
                try:
                    control = control_queue.get_nowait()
                    if control == "shutdown":
                        break
                except queue.Empty:
                    pass

                # Get task (with timeout for responsiveness)
                try:
                    task: TaskMessage = task_queue.get(timeout=1.0)
                except queue.Empty:
                    # Send heartbeat
                    result_queue.put(
                        ResultMessage(
                            task_id="__heartbeat__",
                            worker_id=worker_id,
                            success=True,
                        )
                    )
                    continue

                # Execute task
                start_time = time.time_ns()
                try:
                    if task.func_name not in functions:
                        raise ValueError(f"Unknown function: {task.func_name}")
                    result = functions[task.func_name](*task.args, **task.kwargs)
                    end_time = time.time_ns()

                    result_queue.put(
                        ResultMessage(
                            task_id=task.task_id,
                            worker_id=worker_id,
                            success=True,
                            result=result,
                            execution_time_ns=end_time - start_time,
                        )
                    )
                except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                    end_time = time.time_ns()
                    result_queue.put(
                        ResultMessage(
                            task_id=task.task_id,
                            worker_id=worker_id,
                            success=False,
                            error=str(e),
                            traceback=traceback.format_exc(),
                            execution_time_ns=end_time - start_time,
                        )
                    )

            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                with contextlib.suppress(Exception):
                    # Worker loop error - try to continue
                    pass

    def _collect_results(self) -> None:
        """Collect results from workers."""
        while not self._shutdown_event.is_set():
            try:
                result: ResultMessage = self._result_queue.get(timeout=1.0)

                if result.task_id == "__heartbeat__":
                    # Update heartbeat
                    with self._lock:
                        if result.worker_id in self._worker_info:
                            self._worker_info[result.worker_id].last_heartbeat = time.time()
                    continue

                # Find and complete the future
                with self._lock:
                    future = self._pending_tasks.pop(result.task_id, None)
                    if result.worker_id in self._worker_info:
                        self._worker_info[result.worker_id].tasks_completed += 1
                        self._worker_info[result.worker_id].current_task_id = None
                        self._worker_info[result.worker_id].state = WorkerState.READY

                if future:
                    if result.success:
                        future.set_result(result.result)
                    else:
                        future.set_exception(Exception(f"{result.error}\n{result.traceback}"))

            except queue.Empty:
                continue
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                pass

    def _monitor_workers(self) -> None:
        """Monitor worker health.

        Uses the shutdown event's wait() method so the loop can be interrupted
        promptly during shutdown rather than being stuck in a blocking sleep.
        """
        while not self._shutdown_event.is_set():
            # Use the Event.wait to be interruptible on shutdown
            self._shutdown_event.wait(self._heartbeat_interval)

            now = time.time()
            with self._lock:
                for worker_id, info in list(self._worker_info.items()):
                    # Check for timeout
                    if now - info.last_heartbeat > self._worker_timeout:
                        info.state = WorkerState.ERROR
                        info.error_count += 1

                        # Try to restart worker
                        self._restart_worker(worker_id)

    def _restart_worker(self, worker_id: int) -> None:
        """Restart a failed worker."""
        # Terminate old process
        if worker_id in self._workers:
            with contextlib.suppress(Exception):
                self._workers[worker_id].terminate()
                self._workers[worker_id].join(timeout=5.0)

        # Start new process
        self._start_worker(worker_id)

    def shutdown(self, graceful: bool = True) -> None:
        """Shutdown the executor."""
        if not self._started:
            return

        self._shutdown_event.set()

        # Signal workers to stop
        for worker_id, control_queue in self._control_queues.items():
            with contextlib.suppress(Exception):
                control_queue.put("shutdown")

        # Wait for workers
        if graceful:
            for worker_id, process in self._workers.items():
                with contextlib.suppress(Exception):
                    process.join(timeout=5.0)

        # Terminate remaining
        for process in self._workers.values():
            with contextlib.suppress(Exception):
                if process.is_alive():
                    process.terminate()

        self._started = False

    def submit(self, func_name: str, *args: Any, **kwargs: Any) -> FutureWrapper[Any]:
        """Submit a task."""
        with self._lock:
            self._task_counter += 1
            task_id = f"task-{self._task_counter}"

            future: FutureWrapper[Any] = FutureWrapper(task_id)
            self._pending_tasks[task_id] = future

        task = TaskMessage(
            task_id=task_id,
            func_name=func_name,
            args=args,
            kwargs=kwargs,
        )

        self._task_queue.put(task)
        return future

    def broadcast(self, func_name: str, *args: Any, **kwargs: Any) -> List[FutureWrapper[Any]]:
        """Broadcast to all workers."""
        futures = []
        for _ in range(self._num_workers):
            futures.append(self.submit(func_name, *args, **kwargs))
        return futures

    def get_num_workers(self) -> int:
        """Get number of workers."""
        return self._num_workers

    def get_worker_stats(self) -> Dict[int, WorkerInfo]:
        """Get worker statistics."""
        with self._lock:
            return {
                wid: WorkerInfo(
                    worker_id=info.worker_id,
                    pid=info.pid,
                    state=info.state,
                    gpu_id=info.gpu_id,
                    start_time=info.start_time,
                    last_heartbeat=info.last_heartbeat,
                    tasks_completed=info.tasks_completed,
                    error_count=info.error_count,
                    current_task_id=info.current_task_id,
                )
                for wid, info in self._worker_info.items()
            }

    def is_healthy(self) -> bool:
        """Check executor health."""
        if not self._started:
            return False

        with self._lock:
            healthy_workers = sum(
                1 for info in self._worker_info.values() if info.state in (WorkerState.READY, WorkerState.BUSY)
            )
            return healthy_workers >= self._num_workers // 2
