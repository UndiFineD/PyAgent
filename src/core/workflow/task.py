#!/usr/bin/env python3
"""Core task and task state definitions for the workflow engine."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskState(Enum):
    """Represents the state of a task in the workflow."""

    ACTIVE = "active"
    PAUSED = "paused"
    FAILED = "failed"
    COMPLETED = "completed"
    RETRYING = "retrying"


@dataclass
class Task:
    """Represents a task in the workflow, with metadata, context, and state."""

    id: str
    metadata: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)
    state: TaskState = field(default_factory=lambda: TaskState.ACTIVE)

    def transition(self, new_state: TaskState) -> None:
        """Transition the task to a new state."""
        self.state = new_state


def validate() -> None:
    """Ensure Task and TaskState behave as expected for meta‑tests."""
    t: Task = Task(id="test")
    if t.state.value != TaskState.ACTIVE.value:
        raise AssertionError("initial state should be active")
    t.transition(TaskState.COMPLETED)
    if t.state.value != TaskState.COMPLETED.value:
        raise AssertionError("state transition failed")
