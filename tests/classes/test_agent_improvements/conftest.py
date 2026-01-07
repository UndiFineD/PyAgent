"""Pytest fixtures for test_agent_improvements tests."""

import pytest
import sys
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from tests.agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture
def improvements_module() -> Any:
    """Load and return the improvements module."""
    with agent_dir_on_path():
        return load_agent_module("agent_improvements.py")


@pytest.fixture
def agent(improvements_module: Any, tmp_path: Path) -> Any:
    """Create an ImprovementsAgent instance for testing."""
    ImprovementsAgent = improvements_module.ImprovementsAgent
    test_file = tmp_path / "test_improvements.md"
    test_file.write_text("# Test Improvements\n")
    return ImprovementsAgent(str(test_file))
