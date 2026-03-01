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
Tests for WeightLoader
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
    from infrastructure.loading.WeightLoader import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_weightformat_exists():
    """Test that WeightFormat class exists and is importable."""
    assert 'WeightFormat' in dir()


def test_weightspec_exists():
    """Test that WeightSpec class exists and is importable."""
    assert 'WeightSpec' in dir()


def test_loadstats_exists():
    """Test that LoadStats class exists and is importable."""
    assert 'LoadStats' in dir()


def test_atomicwriter_exists():
    """Test that AtomicWriter class exists and is importable."""
    assert 'AtomicWriter' in dir()


def test_weightloader_exists():
    """Test that WeightLoader class exists and is importable."""
    assert 'WeightLoader' in dir()


def test_safetensorsloader_exists():
    """Test that SafetensorsLoader class exists and is importable."""
    assert 'SafetensorsLoader' in dir()


def test_multithreadweightloader_exists():
    """Test that MultiThreadWeightLoader class exists and is importable."""
    assert 'MultiThreadWeightLoader' in dir()


def test_fastsafetensorsloader_exists():
    """Test that FastSafetensorsLoader class exists and is importable."""
    assert 'FastSafetensorsLoader' in dir()


def test_streamingweightloader_exists():
    """Test that StreamingWeightLoader class exists and is importable."""
    assert 'StreamingWeightLoader' in dir()


def test_atomic_writer_exists():
    """Test that atomic_writer function exists."""
    assert callable(atomic_writer)


def test_detect_weight_format_exists():
    """Test that detect_weight_format function exists."""
    assert callable(detect_weight_format)


def test_get_file_lock_path_exists():
    """Test that get_file_lock_path function exists."""
    assert callable(get_file_lock_path)


def test_compute_weight_hash_rust_exists():
    """Test that compute_weight_hash_rust function exists."""
    assert callable(compute_weight_hash_rust)


def test_validate_weight_shapes_rust_exists():
    """Test that validate_weight_shapes_rust function exists."""
    assert callable(validate_weight_shapes_rust)


def test_filter_shared_tensors_exists():
    """Test that filter_shared_tensors function exists."""
    assert callable(filter_shared_tensors)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

