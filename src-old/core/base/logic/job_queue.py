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

"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/job_queue.description.md

# job_queue

**File**: `src\\core\base\\logic\\job_queue.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 251  
**Complexity**: 10 (moderate)

## Overview

In-Memory Job Queue System
==========================

Inspired by 4o-ghibli-at-home's job queue pattern.
Provides thread-safe job queuing with background processing and TTL cleanup.

## Classes (1)

### `JobQueue`

Thread-safe in-memory job queue with background processing.

Features:
- Thread-safe job queuing and processing
- Background worker threads
- Job status tracking
- TTL-based cleanup
- Configurable queue size limits

**Methods** (10):
- `__init__(self, max_queue_size, job_ttl_seconds, cleanup_interval_seconds, num_workers)`
- `set_job_processor(self, processor)`
- `start(self)`
- `stop(self)`
- `submit_job(self, job_data)`
- `get_job_status(self, job_id)`
- `cancel_job(self, job_id)`
- `_worker_loop(self)`
- `_cleanup_loop(self)`
- `get_stats(self)`

## Dependencies

**Imports** (10):
- `collections.deque`
- `datetime.datetime`
- `datetime.timedelta`
- `threading`
- `time`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`
- `uuid`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/job_queue.improvements.md

# Improvements for job_queue

**File**: `src\\core\base\\logic\\job_queue.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 251 lines (medium)  
**Complexity**: 10 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `job_queue_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
In-Memory Job Queue System
==========================

Inspired by 4o-ghibli-at-home's job queue pattern.
Provides thread-safe job queuing with background processing and TTL cleanup.
"""

import threading
import time
import uuid
from collections import deque
from datetime import datetime
from typing import Any, Callable, Dict, Optional


class JobQueue:
    """Thread-safe in-memory job queue with background processing.

    Features:
    - Thread-safe job queuing and processing
    - Background worker threads
    - Job status tracking
    - TTL-based cleanup
    - Configurable queue size limits
    """

    def __init__(
        self,
        max_queue_size: int = 100,
        job_ttl_seconds: int = 3600,  # 1 hour
        cleanup_interval_seconds: int = 300,  # 5 minutes
        num_workers: int = 1,
    ):
        self.max_queue_size = max_queue_size
        self.job_ttl_seconds = job_ttl_seconds
        self.cleanup_interval_seconds = cleanup_interval_seconds
        self.num_workers = num_workers

        # Thread-safe data structures
        self.job_queue: deque[str] = deque()
        self.job_results: Dict[str, Dict[str, Any]] = {}
        self.queue_lock = threading.Lock()

        # Worker management
        self.workers: list[threading.Thread] = []
        self.cleanup_worker: Optional[threading.Thread] = None
        self.running = False

        # Job processor function
        self.job_processor: Optional[Callable[[str, Dict[str, Any]], Any]] = None

    def set_job_processor(self, processor: Callable[[str, Dict[str, Any]], Any]):
        """Set the function that will process jobs."""
        self.job_processor = processor

    def start(self):
        """Start the job queue workers."""
        if self.running:
            return

        self.running = True

        # Start worker threads
        for i in range(self.num_workers):
            worker = threading.Thread(
                target=self._worker_loop, name=f"JobQueue-Worker-{i+1}", daemon=True
            )
            worker.start()
            self.workers.append(worker)

        # Start cleanup worker
        self.cleanup_worker = threading.Thread(
            target=self._cleanup_loop, name="JobQueue-Cleanup", daemon=True
        )
        self.cleanup_worker.start()

    def stop(self):
        """Stop the job queue workers."""
        self.running = False

        # Wait for workers to finish
        for worker in self.workers:
            worker.join(timeout=5.0)

        if self.cleanup_worker:
            self.cleanup_worker.join(timeout=5.0)

        self.workers.clear()
        self.cleanup_worker = None

    def submit_job(self, job_data: Dict[str, Any]) -> str:
        """Submit a job to the queue.

        Args:
            job_data: Dictionary containing job parameters

        Returns:
            Job ID string

        Raises:
            RuntimeError: If queue is full

        """
        with self.queue_lock:
            if len(self.job_queue) >= self.max_queue_size:
                raise RuntimeError("Job queue is full")

            job_id = str(uuid.uuid4())

            self.job_results[job_id] = {
                "status": "queued",
                "data": job_data,
                "submit_time": datetime.now(),
                "queue_position": len(self.job_queue),
            }

            self.job_queue.append(job_id)

        return job_id

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a job."""
        with self.queue_lock:
            job = self.job_results.get(job_id)
            if not job:
                return None

            # Calculate current queue position for queued jobs
            if job["status"] == "queued":
                try:
                    current_position = list(self.job_queue).index(job_id)
                    job = job.copy()
                    job["queue_position"] = current_position
                except ValueError:
                    pass  # Job might be processing

            return job.copy()

    def cancel_job(self, job_id: str) -> bool:
        """Cancel a queued job."""
        with self.queue_lock:
            if job_id in self.job_results:
                job = self.job_results[job_id]
                if job["status"] == "queued":
                    try:
                        self.job_queue.remove(job_id)
                        job["status"] = "cancelled"
                        job["completion_time"] = datetime.now()
                        return True
                    except ValueError:
                        pass

            return False

    def _worker_loop(self):
        """Main worker loop that processes jobs."""
        while self.running:
            job_id = None

            with self.queue_lock:
                if self.job_queue:
                    job_id = self.job_queue.popleft()
                    if job_id in self.job_results:
                        self.job_results[job_id]["status"] = "processing"
                        self.job_results[job_id]["start_time"] = datetime.now()

            if job_id and self.job_processor:
                try:
                    job_data = self.job_results[job_id]["data"]
                    result = self.job_processor(job_id, job_data)

                    with self.queue_lock:
                        if job_id in self.job_results:
                            self.job_results[job_id].update(
                                {
                                    "status": "completed",
                                    "result": result,
                                    "completion_time": datetime.now(),
                                }
                            )

                except Exception as e:
                    with self.queue_lock:
                        if job_id in self.job_results:
                            self.job_results[job_id].update(
                                {
                                    "status": "failed",
                                    "error": str(e),
                                    "completion_time": datetime.now(),
                                }
                            )

            else:
                # No jobs available, sleep briefly
                time.sleep(0.1)

    def _cleanup_loop(self):
        """Cleanup loop that removes expired jobs."""
        while self.running:
            time.sleep(self.cleanup_interval_seconds)

            with self.queue_lock:
                expired_jobs = []
                current_time = datetime.now()

                for job_id, job in self.job_results.items():
                    if job["status"] in ["completed", "failed", "cancelled"]:
                        completion_time = job.get("completion_time")
                        if completion_time and isinstance(completion_time, datetime):
                            if (
                                current_time - completion_time
                            ).total_seconds() > self.job_ttl_seconds:
                                expired_jobs.append(job_id)

                for job_id in expired_jobs:
                    del self.job_results[job_id]

    def get_stats(self) -> Dict[str, Any]:
        """Get queue statistics."""
        with self.queue_lock:
            total_jobs = len(self.job_results)
            queued_jobs = sum(
                1 for job in self.job_results.values() if job["status"] == "queued"
            )
            processing_jobs = sum(
                1 for job in self.job_results.values() if job["status"] == "processing"
            )
            completed_jobs = sum(
                1 for job in self.job_results.values() if job["status"] == "completed"
            )
            failed_jobs = sum(
                1 for job in self.job_results.values() if job["status"] == "failed"
            )

            return {
                "total_jobs": total_jobs,
                "queued_jobs": queued_jobs,
                "processing_jobs": processing_jobs,
                "completed_jobs": completed_jobs,
                "failed_jobs": failed_jobs,
                "queue_size": len(self.job_queue),
                "max_queue_size": self.max_queue_size,
                "workers_active": len(self.workers),
                "running": self.running,
            }
