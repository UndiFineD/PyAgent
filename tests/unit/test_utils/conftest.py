"""Pytest fixtures for test_agent_test_utils tests."""

import pytest
import sys
from pathlib import Path
from typing import Any

# Add src to path

from tests.utils.agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture
def utils_module() -> Any:
    """Load and return the agent_test_utils module."""
    with agent_dir_on_path():
        return load_agent_module("test_utils/benchmarking.py")
