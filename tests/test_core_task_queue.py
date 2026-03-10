#!/usr/bin/env python3
"""Test the core.task_queue module."""
import importlib


def test_task_queue_module() -> None:
    """Test that the task_queue module can be imported and has expected components."""
    qmod = importlib.import_module("src.core.task_queue")
    assert hasattr(qmod, "TaskQueue")
    assert callable(getattr(qmod, "validate", None))
