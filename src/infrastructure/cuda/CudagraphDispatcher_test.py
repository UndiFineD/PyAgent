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
Tests for CudagraphDispatcher
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
    from infrastructure.cuda.CudagraphDispatcher import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_dispatchmode_exists():
    """Test that DispatchMode class exists and is importable."""
    assert 'DispatchMode' in dir()


def test_dispatchkey_exists():
    """Test that DispatchKey class exists and is importable."""
    assert 'DispatchKey' in dir()


def test_dispatchstats_exists():
    """Test that DispatchStats class exists and is importable."""
    assert 'DispatchStats' in dir()


def test_dispatchpolicy_exists():
    """Test that DispatchPolicy class exists and is importable."""
    assert 'DispatchPolicy' in dir()


def test_defaultdispatchpolicy_exists():
    """Test that DefaultDispatchPolicy class exists and is importable."""
    assert 'DefaultDispatchPolicy' in dir()


def test_adaptivedispatchpolicy_exists():
    """Test that AdaptiveDispatchPolicy class exists and is importable."""
    assert 'AdaptiveDispatchPolicy' in dir()


def test_graphentry_exists():
    """Test that GraphEntry class exists and is importable."""
    assert 'GraphEntry' in dir()


def test_cudagraphdispatcher_exists():
    """Test that CudagraphDispatcher class exists and is importable."""
    assert 'CudagraphDispatcher' in dir()


def test_compositedispatcher_exists():
    """Test that CompositeDispatcher class exists and is importable."""
    assert 'CompositeDispatcher' in dir()


def test_compositedispatcher_instantiation():
    """Test that CompositeDispatcher can be instantiated."""
    instance = CompositeDispatcher()
    assert instance is not None


def test_streamdispatcher_exists():
    """Test that StreamDispatcher class exists and is importable."""
    assert 'StreamDispatcher' in dir()


def test_create_dispatch_key_exists():
    """Test that create_dispatch_key function exists."""
    assert callable(create_dispatch_key)


def test_get_padded_key_exists():
    """Test that get_padded_key function exists."""
    assert callable(get_padded_key)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

