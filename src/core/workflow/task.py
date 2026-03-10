#!/usr/bin/env python3
"""Core task and task state definitions for the workflow engine."""
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
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
    metadata: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    state: TaskState = field(default_factory=lambda: TaskState.ACTIVE)

    def transition(self, new_state: TaskState) -> None:
        """Transition the task to a new state."""
        self.state = new_state


def validate() -> None:
    """Ensure Task and TaskState behave as expected for meta‑tests."""
    t = Task(id="test")
    assert t.state == TaskState.ACTIVE
    t.transition(TaskState.COMPLETED)
    if t.state != TaskState.COMPLETED:  # type: ignore[arg-type]
        raise AssertionError("state transition failed")
