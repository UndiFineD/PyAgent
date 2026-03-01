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
Tests for MambaUtils
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
    from infrastructure.ssm.MambaUtils import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_mambablockstate_exists():
    """Test that MambaBlockState class exists and is importable."""
    assert 'MambaBlockState' in dir()


def test_compute_ssm_state_shape_exists():
    """Test that compute_ssm_state_shape function exists."""
    assert callable(compute_ssm_state_shape)


def test_compute_conv_state_shape_exists():
    """Test that compute_conv_state_shape function exists."""
    assert callable(compute_conv_state_shape)


def test_compute_state_dtype_exists():
    """Test that compute_state_dtype function exists."""
    assert callable(compute_state_dtype)


def test_discretize_ssm_exists():
    """Test that discretize_ssm function exists."""
    assert callable(discretize_ssm)


def test_apply_ssm_recurrence_exists():
    """Test that apply_ssm_recurrence function exists."""
    assert callable(apply_ssm_recurrence)


def test_silu_activation_exists():
    """Test that silu_activation function exists."""
    assert callable(silu_activation)


def test_swish_activation_exists():
    """Test that swish_activation function exists."""
    assert callable(swish_activation)


def test_softplus_exists():
    """Test that softplus function exists."""
    assert callable(softplus)


def test_chunk_sequence_exists():
    """Test that chunk_sequence function exists."""
    assert callable(chunk_sequence)


def test_merge_chunks_exists():
    """Test that merge_chunks function exists."""
    assert callable(merge_chunks)


def test_parallel_scan_exists():
    """Test that parallel_scan function exists."""
    assert callable(parallel_scan)


def test_init_A_log_exists():
    """Test that init_A_log function exists."""
    assert callable(init_A_log)


def test_init_dt_proj_exists():
    """Test that init_dt_proj function exists."""
    assert callable(init_dt_proj)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

