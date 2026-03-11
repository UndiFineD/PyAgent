#!/usr/bin/env python3
"""Test the Task class."""
import pytest

from src.core.workflow.task import Task, TaskState


@pytest.mark.asyncio
async def test_task_initial_state_and_metadata() -> None:
    """A new Task should have the correct initial state and store metadata/context."""
    t = Task(id="123", metadata={"foo": "bar"}, context={"a": 1})
    assert t.id == "123"
    assert t.metadata["foo"] == "bar"
    assert t.context["a"] == 1
    assert t.state == TaskState.ACTIVE


@pytest.mark.asyncio
async def test_task_state_transitions() -> None:
    """A Task should transition between states correctly."""
    t = Task(id="x")
    t.transition(TaskState.FAILED)
    assert t.state.value == TaskState.FAILED.value
    t.transition(TaskState.RETRYING)
    assert t.state.value == TaskState.RETRYING.value
