#!/usr/bin/env python3
"""Task scheduler module for PyAgent."""

import heapq
import time
import uuid
from typing import Any


class TaskScheduler:
    """A simple in-memory task scheduler with priority queues."""

    def __init__(self) -> None:
        """Initialize the task scheduler with empty queues and task store."""
        # priority -> list of tuples (enqueue_time, task_id)
        self._queues: dict[int, list[tuple[float, str]]] = {1: [], 2: [], 3: [], 4: []}
        self._tasks: dict[str, dict[str, Any]] = {}

    def enqueue(self, payload: dict[str, Any], priority: int = 3) -> str:
        """Add a task to the scheduler with the given payload and priority,
        returning its unique ID.
        """
        tid = str(uuid.uuid4())
        self._tasks[tid] = {"id": tid, "payload": payload, "priority": priority}
        heapq.heappush(self._queues[priority], (time.time(), tid))
        return tid

    async def dequeue(self) -> dict[str, Any]:
        """Remove and return the highest priority task from the scheduler,
        or raise IndexError if no tasks are available.
        """
        for pr in sorted(self._queues):
            if self._queues[pr]:
                _, tid = heapq.heappop(self._queues[pr])
                return self._tasks.pop(tid)
        raise IndexError("no tasks")

    def modify(self, task_id: str, priority: int) -> None:
        """Modify the priority of an existing task in the scheduler, if it exists."""
        if task_id in self._tasks:
            # in real impl we would reposition in queue; simplified here
            self._tasks[task_id]["priority"] = priority
