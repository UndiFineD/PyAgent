"""Pytest fixtures for test_agent_backend tests."""

import pytest
import sys
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from tests.utils.agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture
def agent_backend_module() -> Any:
    """Load and return the agent_backend module."""
    with agent_dir_on_path():
        return load_agent_module("backend/execution_engine.py")
