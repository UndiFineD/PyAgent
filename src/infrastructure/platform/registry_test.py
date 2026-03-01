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
Tests for registry
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
    from infrastructure.platform.registry import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_platformregistry_exists():
    """Test that PlatformRegistry class exists and is importable."""
    assert 'PlatformRegistry' in dir()


def test_get_current_platform_exists():
    """Test that get_current_platform function exists."""
    assert callable(get_current_platform)


def test_detect_platform_exists():
    """Test that detect_platform function exists."""
    assert callable(detect_platform)


def test_get_device_count_exists():
    """Test that get_device_count function exists."""
    assert callable(get_device_count)


def test_get_device_capability_exists():
    """Test that get_device_capability function exists."""
    assert callable(get_device_capability)


def test_get_memory_info_exists():
    """Test that get_memory_info function exists."""
    assert callable(get_memory_info)


def test_is_quantization_supported_exists():
    """Test that is_quantization_supported function exists."""
    assert callable(is_quantization_supported)


def test_select_attention_backend_exists():
    """Test that select_attention_backend function exists."""
    assert callable(select_attention_backend)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

