"""Pytest configuration
"""

import pytest


@pytest.fixture
def mock_logger(mocker):
    """Mock logger fixture"""
    return mocker.MagicMock()

def pytest_configure(config):
    """Configure pytest"""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
