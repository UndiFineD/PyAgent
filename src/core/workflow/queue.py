#!/usr/bin/env python3
"""Workflow engine for processing tasks."""
import asyncio
from typing import Optional
from .task import Task


class TaskQueue:
    """A simple asynchronous task queue using asyncio.Queue."""

    def __init__(self) -> None:
        """Initialize the task queue."""
        self._q: asyncio.Queue[Task] = asyncio.Queue()

    async def enqueue(self, task: Task) -> None:
        """Add a task to the queue."""
        await self._q.put(task)

    async def dequeue(self) -> Task:
        """Remove and return a task from the queue."""
        return await self._q.get()


def validate() -> None:
    """Simple check that the queue supports enqueue/dequeue operations."""
    async def _run() -> None:
        q = TaskQueue()
        t = Task(id="x")
        await q.enqueue(t)
        got = await q.dequeue()
        assert got is t

    asyncio.run(_run())
