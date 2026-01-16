"""Pytest fixtures for test_agent_test_utils tests."""

import pytest
from typing import Any

# Add src to path

from tests.utils.agent_test_utils import agent_dir_on_path


@pytest.fixture
def utils_module() -> Any:
    """Load and return the agent_test_utils module."""
    with agent_dir_on_path():
        import src.infrastructure.dev.test_utils as test_utils

        return test_utils
