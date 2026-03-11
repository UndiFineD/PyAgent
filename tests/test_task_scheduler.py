#!/usr/bin/env python3
"""Test the task scheduler."""
import pytest

from swarm.task_scheduler import TaskScheduler


@pytest.mark.asyncio
async def test_enqueue_dequeue_priority() -> None:
    """Tasks should be dequeued in order of priority (lower number = higher priority)."""
    sched = TaskScheduler()
    sched.enqueue({"name": "a"}, priority=2)
    sched.enqueue({"name": "b"}, priority=1)
    first = await sched.dequeue()
    assert first["payload"]["name"] == "b"
    second = await sched.dequeue()
    assert second["payload"]["name"] == "a"


def test_modify_priority() -> None:
    """Modifying a task's priority should update its stored priority, even if it doesn't requeue the task."""
    sched = TaskScheduler()
    t = sched.enqueue({"x": 1}, priority=3)
    sched.modify(t, priority=1)
    # even though modify doesn't requeue, the stored priority should reflect change
    assert sched._tasks[t]["priority"] == 1
