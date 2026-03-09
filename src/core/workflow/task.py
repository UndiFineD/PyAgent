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
