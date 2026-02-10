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
Task Queue Mixin for BaseAgent.
Provides asynchronous task processing with job queue, inspired by 4o-ghibli-at-home.
"""

from __future__ import annotations

import asyncio
import time
import uuid
from typing import Any, Dict, Optional


class TaskQueueMixin:
    """
    Mixin to provide asynchronous task queue capabilities to agents.
    Enables background processing of heavy tasks like model inference.
    """

    def __init__(self, **kwargs: Any) -> None:
        self.task_queue: asyncio.Queue[str] = asyncio.Queue()
        self.task_results: Dict[str, Dict[str, Any]] = {}
        self.max_queue_size: int = kwargs.get('max_queue_size', 10)
        self.task_ttl: int = kwargs.get('task_ttl', 600)  # 10 minutes
        self.cleanup_interval: int = kwargs.get('cleanup_interval', 300)  # 5 minutes
        self._cleanup_task: Optional[asyncio.Task[None]] = None
        self._worker_task: Optional[asyncio.Task[None]] = None

    async def start_task_processing(self) -> None:
        """Start the background task processor and cleanup worker."""
        if self._worker_task is None:
            self._worker_task = asyncio.create_task(self._task_worker())
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_worker())

    async def stop_task_processing(self) -> None:
        """Stop the background tasks."""
        if self._worker_task:
            self._worker_task.cancel()
            try:
                await self._worker_task
            except asyncio.CancelledError:
                pass
            self._worker_task = None

        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
            self._cleanup_task = None

    async def submit_task(self, task_data: Dict[str, Any]) -> str:
        """Submit a task to the queue. Returns job_id."""
        if self.task_queue.qsize() >= self.max_queue_size:
            raise ValueError("Task queue is full. Please try again later.")

        job_id = str(uuid.uuid4())
        task_data.update({
            'job_id': job_id,
            'status': 'queued',
            'submit_time': time.time(),
        })
        self.task_results[job_id] = task_data
        await self.task_queue.put(job_id)
        return job_id

    async def get_task_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a task."""
        return self.task_results.get(job_id)

    async def _task_worker(self) -> None:
        """Background worker to process tasks."""
        while True:
            try:
                job_id = await self.task_queue.get()
                task_data = self.task_results.get(job_id)
                if not task_data:
                    continue

                task_data['status'] = 'processing'
                task_data['start_time'] = time.time()

                try:
                    # Process the task - override in subclass
                    result = await self._process_task(task_data)
                    task_data.update({
                        'status': 'completed',
                        'result': result,
                        'completion_time': time.time(),
                    })
                except Exception as e:
                    task_data.update({
                        'status': 'failed',
                        'error': str(e),
                        'completion_time': time.time(),
                    })

                self.task_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                # Log error
                print(f"Task worker error: {e}")

    async def _process_task(self, task_data: Dict[str, Any]) -> Any:
        """Override this method to implement task processing logic."""
        raise NotImplementedError("Subclasses must implement _process_task")

    async def _cleanup_worker(self) -> None:
        """Background worker to clean up old completed tasks."""
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)
                current_time = time.time()
                to_remove = []

                for job_id, task_data in self.task_results.items():
                    if task_data.get('status') in ['completed', 'failed']:
                        submit_time = task_data.get('submit_time', 0)
                        completion_time = task_data.get('completion_time', current_time)
                        age = current_time - max(submit_time, completion_time)
                        if age > self.task_ttl:
                            to_remove.append(job_id)

                for job_id in to_remove:
                    del self.task_results[job_id]

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Cleanup worker error: {e}")
