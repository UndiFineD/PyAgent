import pytest

from swarm.message_model import validate_message


def test_validate_message_accepts_valid():
    """A valid message should pass validation without exceptions."""
    valid = {
        "id": "uuid-1",
        "timestamp": "2026-03-09T00:00Z",
        "type": "task_request",
        "priority": "high",
        "source": "agent-1",
        "destination": "scheduler",
        "payload": {"foo": "bar"},
        "checksum": "abc",
    }
    assert validate_message(valid)


def test_validate_message_rejects_missing_field():
    """A message missing required fields should raise a ValueError."""
    invalid = {"id": "uuid-1"}
    with pytest.raises(Exception):
        validate_message(invalid)
