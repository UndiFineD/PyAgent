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
