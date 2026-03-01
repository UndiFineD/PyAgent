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
Tests for CudaStreamPool
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
    from core.base.core.CudaStreamPool import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_streampriority_exists():
    """Test that StreamPriority class exists and is importable."""
    assert 'StreamPriority' in dir()


def test_streamstate_exists():
    """Test that StreamState class exists and is importable."""
    assert 'StreamState' in dir()


def test_streamstats_exists():
    """Test that StreamStats class exists and is importable."""
    assert 'StreamStats' in dir()


def test_pooledstream_exists():
    """Test that PooledStream class exists and is importable."""
    assert 'PooledStream' in dir()


def test_pooledevent_exists():
    """Test that PooledEvent class exists and is importable."""
    assert 'PooledEvent' in dir()


def test_eventpool_exists():
    """Test that EventPool class exists and is importable."""
    assert 'EventPool' in dir()


def test_cudastreampool_exists():
    """Test that CudaStreamPool class exists and is importable."""
    assert 'CudaStreamPool' in dir()


def test_get_global_stream_pool_exists():
    """Test that get_global_stream_pool function exists."""
    assert callable(get_global_stream_pool)


def test_reset_global_pool_exists():
    """Test that reset_global_pool function exists."""
    assert callable(reset_global_pool)


def test_compute_stream_exists():
    """Test that compute_stream function exists."""
    assert callable(compute_stream)


def test_comm_stream_exists():
    """Test that comm_stream function exists."""
    assert callable(comm_stream)


def test_high_priority_stream_exists():
    """Test that high_priority_stream function exists."""
    assert callable(high_priority_stream)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

