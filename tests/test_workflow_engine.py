#!/usr/bin/env python3
"""Test the WorkflowEngine processes tasks from the TaskQueue and updates their state."""

import pytest

from src.core.workflow.engine import WorkflowEngine
from src.core.workflow.queue import TaskQueue
from src.core.workflow.task import Task, TaskState


@pytest.mark.asyncio
async def test_engine_process_changes_state() -> None:
    """Running the engine should process a task and change its state to COMPLETED."""
    q = TaskQueue()
    engine = WorkflowEngine(q)
    t = Task(id="z")
    await q.enqueue(t)
    await engine.run_once()  # process single task
    assert t.state == TaskState.COMPLETED
