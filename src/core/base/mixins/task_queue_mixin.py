#!/usr/bin/env python3
"""Task Queue Mixin providing simple async job queue for tests."""

from __future__ import annotations

import asyncio
import time
import uuid
from typing import Any, Dict, Optional


class TaskQueueMixin:
    def __init__(self, **kwargs: Any) -> None:
        self.task_queue: asyncio.Queue[str] = asyncio.Queue()
        self.task_results: Dict[str, Dict[str, Any]] = {}
        self.max_queue_size: int = kwargs.get("max_queue_size", 10)
        self.task_ttl: int = kwargs.get("task_ttl", 600)
        self.cleanup_interval: int = kwargs.get("cleanup_interval", 300)
        self._cleanup_task: Optional[asyncio.Task[None]] = None
        self._worker_task: Optional[asyncio.Task[None]] = None

    async def start_task_processing(self) -> None:
        if self._worker_task is None:
            self._worker_task = asyncio.create_task(self._task_worker())
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_worker())

    async def stop_task_processing(self) -> None:
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
        if self.task_queue.qsize() >= self.max_queue_size:
            raise ValueError("Task queue is full. Please try again later.")
        job_id = str(uuid.uuid4())
        task_data.update({"job_id": job_id, "status": "queued", "submit_time": time.time()})
        self.task_results[job_id] = task_data
        await self.task_queue.put(job_id)
        return job_id

    async def get_task_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self.task_results.get(job_id)

    async def _task_worker(self) -> None:
        while True:
            try:
                job_id = await self.task_queue.get()
                task_data = self.task_results.get(job_id)
                if not task_data:
                    continue

                task_data["status"] = "processing"
                task_data["start_time"] = time.time()
                try:
                    result = await self._process_task(task_data)
                    task_data.update({"status": "completed", "result": result, "completion_time": time.time()})
                except Exception as e:
                    task_data.update({"status": "failed", "error": str(e), "completion_time": time.time()})

                self.task_queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Task worker error: {e}")

    async def _process_task(self, task_data: Dict[str, Any]) -> Any:
        raise NotImplementedError("Subclasses must implement _process_task")

    async def _cleanup_worker(self) -> None:
        while True:
            try:
                await asyncio.sleep(self.cleanup_interval)
                current_time = time.time()
                to_remove = []
                for job_id, task_data in list(self.task_results.items()):
                    if task_data.get("status") in ["completed", "failed"]:
                        submit_time = task_data.get("submit_time", 0)
                        completion_time = task_data.get("completion_time", current_time)
                        age = current_time - max(submit_time, completion_time)
                        if age > self.task_ttl:
                            to_remove.append(job_id)

                for job_id in to_remove:
                    del self.task_results[job_id]

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Cleanup worker error: {e}")
