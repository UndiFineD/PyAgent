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
Async Pipeline Core - Orchestrates asynchronous coding agent pipelines
Based on patterns from agentic-patterns repository (Asynchronous Coding Agent Pipeline)
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Callable, Awaitable
from dataclasses import dataclass
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
import time

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Status of a pipeline task"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Priority levels for tasks"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class PipelineTask:
    """Represents a task in the async pipeline"""
    task_id: str
    name: str
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    dependencies: List[str] = None  # Task IDs this task depends on
    max_retries: int = 0
    retry_count: int = 0
    created_at: float = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Any = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.created_at is None:
            self.created_at = time.time()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class PipelineConfig:
    """Configuration for the async pipeline"""
    max_concurrent_tasks: int = 10
    max_queue_size: int = 1000
    task_timeout: float = 300.0  # 5 minutes
    retry_delay: float = 1.0
    enable_priority_queue: bool = True
    enable_dependency_resolution: bool = True


class AsyncPipelineCore:
    """
    Orchestrates asynchronous coding agent pipelines
    Based on the Asynchronous Coding Agent Pipeline pattern from agentic-patterns
    """

    def __init__(self, config: PipelineConfig = None):
        self.config = config or PipelineConfig()
        self.tasks: Dict[str, PipelineTask] = {}
        self.task_queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=self.config.max_queue_size)
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.completed_tasks: Dict[str, PipelineTask] = {}
        self.task_handlers: Dict[str, Callable[[PipelineTask], Awaitable[Any]]] = {}
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_concurrent_tasks)
        self._shutdown = False

        # Start the pipeline processor
        self._processor_task = None

    async def start(self):
        """Start the async pipeline processor"""
        if self._processor_task is not None:
            return

        self._shutdown = False
        self._processor_task = asyncio.create_task(self._process_queue())
        logger.info("Async Pipeline Core started")

    async def stop(self):
        """Stop the async pipeline processor"""
        self._shutdown = True

        # Cancel all running tasks
        for task_id, task in self.running_tasks.items():
            if not task.done():
                task.cancel()
                logger.info(f"Cancelled running task: {task_id}")

        # Wait for processor to finish
        if self._processor_task:
            await self._processor_task

        # Shutdown executor
        self.executor.shutdown(wait=True)
        logger.info("Async Pipeline Core stopped")

    def register_handler(self, task_type: str, handler: Callable[[PipelineTask], Awaitable[Any]]):
        """Register a handler for a specific task type"""
        self.task_handlers[task_type] = handler
        logger.info(f"Registered handler for task type: {task_type}")

    async def submit_task(self, task: PipelineTask) -> str:
        """Submit a task to the pipeline"""
        if task.task_id in self.tasks:
            raise ValueError(f"Task {task.task_id} already exists")

        self.tasks[task.task_id] = task

        # Calculate priority for queue (lower number = higher priority)
        queue_priority = (5 - task.priority.value, task.created_at)

        try:
            await self.task_queue.put((queue_priority, task.task_id))
            logger.info(f"Submitted task: {task.task_id} ({task.name})")
            return task.task_id
        except asyncio.QueueFull:
            raise RuntimeError("Task queue is full")

    async def submit_batch(self, tasks: List[PipelineTask]) -> List[str]:
        """Submit multiple tasks to the pipeline"""
        task_ids = []
        for task in tasks:
            task_id = await self.submit_task(task)
            task_ids.append(task_id)
        return task_ids

    def get_task_status(self, task_id: str) -> Optional[PipelineTask]:
        """Get the status of a task"""
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> Dict[str, PipelineTask]:
        """Get all tasks"""
        return self.tasks.copy()

    def get_pending_tasks(self) -> List[PipelineTask]:
        """Get all pending tasks"""
        return [task for task in self.tasks.values() if task.status == TaskStatus.PENDING]

    def get_running_tasks(self) -> List[PipelineTask]:
        """Get all running tasks"""
        return [task for task in self.tasks.values() if task.status == TaskStatus.RUNNING]

    def get_completed_tasks(self) -> List[PipelineTask]:
        """Get all completed tasks"""
        statuses = [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]
        return [task for task in self.tasks.values() if task.status in statuses]

    async def wait_for_task(self, task_id: str, timeout: Optional[float] = None) -> PipelineTask:
        """Wait for a task to complete"""
        start_time = time.time()

        while True:
            task = self.get_task_status(task_id)
            if task is None:
                raise ValueError(f"Task {task_id} not found")

            if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                return task

            if timeout and (time.time() - start_time) > timeout:
                raise asyncio.TimeoutError(f"Task {task_id} timed out after {timeout} seconds")

            await asyncio.sleep(0.1)  # Poll every 100ms

    async def wait_for_all(self, task_ids: List[str], timeout: Optional[float] = None) -> List[PipelineTask]:
        """Wait for all tasks to complete"""
        start_time = time.time()
        results = []

        while len(results) < len(task_ids):
            for task_id in task_ids:
                if any(r.task_id == task_id for r in results):
                    continue

                task = self.get_task_status(task_id)
                if task and task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                    results.append(task)

            if timeout and (time.time() - start_time) > timeout:
                raise asyncio.TimeoutError(f"Tasks timed out after {timeout} seconds")

            await asyncio.sleep(0.1)

        return results

    async def _process_queue(self):
        """Main queue processing loop"""
        logger.info("Pipeline processor started")

        while not self._shutdown:
            try:
                # Get next task from queue with timeout
                try:
                    priority, task_id = await asyncio.wait_for(
                        self.task_queue.get(),
                        timeout=1.0
                    )
                except asyncio.TimeoutError:
                    continue

                task = self.tasks.get(task_id)
                if not task:
                    logger.warning(f"Task {task_id} not found in tasks dict")
                    continue

                # Check dependencies
                if self.config.enable_dependency_resolution and not self._check_dependencies(task):
                    # Dependencies not met, re-queue
                    await self.task_queue.put((priority, task_id))
                    await asyncio.sleep(0.5)  # Brief delay before retry
                    continue

                # Start task execution
                asyncio.create_task(self._execute_task(task))

            except Exception as e:
                logger.error(f"Error in queue processor: {e}")
                await asyncio.sleep(1.0)

        logger.info("Pipeline processor stopped")

    def _check_dependencies(self, task: PipelineTask) -> bool:
        """Check if all dependencies are satisfied"""
        for dep_id in task.dependencies:
            dep_task = self.tasks.get(dep_id)
            if not dep_task or dep_task.status != TaskStatus.COMPLETED:
                return False
        return True

    async def _execute_task(self, task: PipelineTask):
        """Execute a single task"""
        task.status = TaskStatus.RUNNING
        task.started_at = time.time()
        self.running_tasks[task.task_id] = asyncio.current_task()

        try:
            logger.info(f"Executing task: {task.task_id} ({task.name})")

            # Get task type from metadata or name
            task_type = task.metadata.get('task_type', task.name.lower().replace(' ', '_'))

            # Get handler
            handler = self.task_handlers.get(task_type)
            if not handler:
                raise ValueError(f"No handler registered for task type: {task_type}")

            # Execute with timeout
            try:
                result = await asyncio.wait_for(
                    handler(task),
                    timeout=self.config.task_timeout
                )
                task.result = result
                task.status = TaskStatus.COMPLETED
                logger.info(f"Task completed: {task.task_id}")

            except asyncio.TimeoutError:
                raise TimeoutError(f"Task timed out after {self.config.task_timeout} seconds")

        except Exception as e:
            logger.error(f"Task failed: {task.task_id} - {e}")
            task.error = str(e)
            task.status = TaskStatus.FAILED

            # Retry logic
            if task.retry_count < task.max_retries:
                task.retry_count += 1
                task.status = TaskStatus.PENDING
                logger.info(f"Retrying task: {task.task_id} (attempt {task.retry_count}/{task.max_retries})")

                # Re-queue with backoff
                await asyncio.sleep(self.config.retry_delay * task.retry_count)
                queue_priority = (5 - task.priority.value, time.time())
                await self.task_queue.put((queue_priority, task.task_id))
                return

        finally:
            task.completed_at = time.time()
            if task.task_id in self.running_tasks:
                del self.running_tasks[task.task_id]

    # Convenience methods for common coding tasks
    async def submit_code_task(
        self,
        name: str,
        code: str,
        task_type: str = "execute_code",
        dependencies: List[str] = None,
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> str:
        """Submit a coding task"""
        task = PipelineTask(
            task_id=f"{task_type}_{int(time.time() * 1000)}",
            name=name,
            priority=priority,
            dependencies=dependencies or [],
            metadata={
                'task_type': task_type,
                'code': code
            }
        )
        return await self.submit_task(task)

    async def submit_test_task(self, name: str, test_code: str, dependencies: List[str] = None) -> str:
        """Submit a testing task"""
        return await self.submit_code_task(name, test_code, "run_tests", dependencies)

    async def submit_lint_task(self, name: str, files: List[str], dependencies: List[str] = None) -> str:
        """Submit a linting task"""
        task = PipelineTask(
            task_id=f"lint_{int(time.time() * 1000)}",
            name=name,
            dependencies=dependencies or [],
            metadata={
                'task_type': 'lint',
                'files': files
            }
        )
        return await self.submit_task(task)
