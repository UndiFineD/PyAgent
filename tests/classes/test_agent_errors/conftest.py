"""Pytest fixtures for test_agent_errors tests."""

import pytest
import sys
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'src'))

from tests.agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture
def errors_module() -> Any:
    """Load and return the errors module."""
    with agent_dir_on_path():
        return load_agent_module("agent_errors.py")


@pytest.fixture
def agent(errors_module: Any, tmp_path: Path) -> Any:
    """Create an ErrorsAgent instance for testing."""
    ErrorsAgent = errors_module.ErrorsAgent
    test_file = tmp_path / "test_errors.md"
    test_file.write_text("# Test Errors\n")
    return ErrorsAgent(str(test_file))
