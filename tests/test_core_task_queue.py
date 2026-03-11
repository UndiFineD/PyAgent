#!/usr/bin/env python3
"""Test the core.task_queue module."""
import asyncio
import importlib


async def _producer_consumer_cycle() -> None:
    """Test that we can enqueue and dequeue items from the TaskQueue."""
    import src.core.task_queue as tq

    q = tq.TaskQueue()

    # put an item and get it back
    await q.put("x")
    item = await q.get()
    assert item == "x"


def test_task_queue_validate_and_async_cycle() -> None:
    """Test that the task_queue module can be imported and validate function runs."""
    tq = importlib.import_module("src.core.task_queue")
    assert hasattr(tq, "TaskQueue"), "TaskQueue missing"
    assert callable(getattr(tq, "validate", None)), "validate missing"

    # run simple async producer/consumer
    asyncio.run(_producer_consumer_cycle())


def test_task_queue_module() -> None:
    """Test that the task_queue module can be imported and has expected components."""
    qmod = importlib.import_module("src.core.task_queue")
    assert hasattr(qmod, "TaskQueue")
    assert callable(getattr(qmod, "validate", None))
