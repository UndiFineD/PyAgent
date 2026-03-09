import pytest
from src.core.workflow.task import TaskState


def test_taskstate_contains_expected_states() -> None:
    """TaskState should contain all expected states."""
    names = {s.name for s in TaskState}
    assert {"ACTIVE", "PAUSED", "FAILED", "COMPLETED", "RETRYING"} <= names
