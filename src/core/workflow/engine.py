import asyncio
from .queue import TaskQueue
from .task import Task, TaskState


class WorkflowEngine:
    """A simple workflow engine that processes tasks from a queue."""

    def __init__(self, queue: TaskQueue) -> None:
        """Initialize the engine with a task queue."""
        self.queue = queue

    async def run_once(self) -> None:
        """Process a single task from the queue."""
        task: Task = await self.queue.dequeue()
        # simple prototype: mark complete immediately
        task.transition(TaskState.COMPLETED)
