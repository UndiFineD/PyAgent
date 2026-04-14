#!/usr/bin/env python3
"""Test the TaskState enum."""

import pytest

from src.core.workflow.task import TaskState


@pytest.mark.asyncio
async def test_taskstate_contains_expected_states() -> None:
    """TaskState should contain all expected states."""
    names = {s.name for s in TaskState}
    assert {"ACTIVE", "PAUSED", "FAILED", "COMPLETED", "RETRYING"} <= names
