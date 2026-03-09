import pytest
import asyncio
from src.core.workflow.queue import TaskQueue
from src.core.workflow.task import Task


@pytest.mark.asyncio
async def test_enqueue_dequeue() -> None:
    """Enqueueing a task and then dequeueing should return the same task."""
    q = TaskQueue()
    t = Task(id="1")
    await q.enqueue(t)
    got = await q.dequeue()
    assert got is t
