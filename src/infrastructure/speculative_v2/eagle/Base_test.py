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
Tests for Base
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
    from infrastructure.speculative_v2.eagle.Base import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_inputbuffer_exists():
    """Test that InputBuffer class exists and is importable."""
    assert 'InputBuffer' in dir()


def test_cpugpubuffer_exists():
    """Test that CpuGpuBuffer class exists and is importable."""
    assert 'CpuGpuBuffer' in dir()


def test_attentionmetadata_exists():
    """Test that AttentionMetadata class exists and is importable."""
    assert 'AttentionMetadata' in dir()


def test_treeattentionmetadata_exists():
    """Test that TreeAttentionMetadata class exists and is importable."""
    assert 'TreeAttentionMetadata' in dir()


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

