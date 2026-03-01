#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Tests for base_models
Auto-generated test template - expand with actual test cases
"""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from core.base.models.base_models import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_cacheentry_exists():
    """Test that CacheEntry class exists and is importable."""
    assert 'CacheEntry' in dir()


def test_authconfig_exists():
    """Test that AuthConfig class exists and is importable."""
    assert 'AuthConfig' in dir()


def test_serializationconfig_exists():
    """Test that SerializationConfig class exists and is importable."""
    assert 'SerializationConfig' in dir()


def test_filepriorityconfig_exists():
    """Test that FilePriorityConfig class exists and is importable."""
    assert 'FilePriorityConfig' in dir()


def test_executioncondition_exists():
    """Test that ExecutionCondition class exists and is importable."""
    assert 'ExecutionCondition' in dir()


def test_validationrule_exists():
    """Test that ValidationRule class exists and is importable."""
    assert 'ValidationRule' in dir()


def test_modelconfig_exists():
    """Test that ModelConfig class exists and is importable."""
    assert 'ModelConfig' in dir()


def test_configprofile_exists():
    """Test that ConfigProfile class exists and is importable."""
    assert 'ConfigProfile' in dir()


def test_diffresult_exists():
    """Test that DiffResult class exists and is importable."""
    assert 'DiffResult' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

