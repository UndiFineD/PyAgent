#!/usr/bin/env python
"""Test the message model validation."""

import pytest

# importing the message model might raise a SystemError due to pydantic-core
# version mismatch; skip tests if that happens.
try:
    from src.swarm.message_model import validate_message
except SystemError as e:
    pytest.skip(f"Skipping message_model tests due to import error: {e}", allow_module_level=True)


def test_validate_message_accepts_valid() -> None:
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


def test_validate_message_rejects_missing_field() -> None:
    """A message missing required fields should raise a ValueError."""
    invalid = {"id": "uuid-1"}
    with pytest.raises(ValueError):
        validate_message(invalid)
