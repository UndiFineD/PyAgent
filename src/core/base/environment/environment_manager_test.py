#!/usr/bin/env python3
try:
    import pytest
except ImportError:
    import pytest

try:
    from core.base.environment.environment_manager import EnvironmentManager
except ImportError:
    from core.base.environment.environment_manager import EnvironmentManager


def test_environment_manager_basic():
    assert EnvironmentManager is not None
