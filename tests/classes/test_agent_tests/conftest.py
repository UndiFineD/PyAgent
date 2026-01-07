"""Pytest fixtures for test_agent_tests tests."""

import pytest
import sys
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from tests.agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture
def tests_module() -> Any:
    """Load and return the tests module."""
    with agent_dir_on_path():
        return load_agent_module("agent_tests.py")


@pytest.fixture
def agent(tests_module: Any, tmp_path: Path) -> Any:
    """Create a TestsAgent instance for testing."""
    TestsAgent = tests_module.TestsAgent
    test_file = tmp_path / "test_tests.py"
    test_file.write_text("# Test file\n")
    return TestsAgent(str(test_file))
