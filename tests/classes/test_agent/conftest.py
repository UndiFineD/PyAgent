"""Pytest fixtures for test_agent tests."""

import pytest
import sys
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from tests.agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture
def agent_module() -> Any:
    """Load and return the agent module."""
    with agent_dir_on_path():
        return load_agent_module("agent.py")


@pytest.fixture
def agent(agent_module: Any, tmp_path: Path) -> Any:
    """Create an Agent instance for testing."""
    Agent = agent_module.Agent
    test_file = tmp_path / "test_agent.py"
    test_file.write_text("print('hello')\n")
    return Agent([str(test_file)])
