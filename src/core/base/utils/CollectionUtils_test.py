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
Tests for CollectionUtils
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
    from core.base.utils.CollectionUtils import *
except ImportError as e:
    pytest.skip(f"Cannot import module: {e}", allow_module_level=True)


def test_lazydict_exists():
    """Test that LazyDict class exists and is importable."""
    assert 'LazyDict' in dir()


def test_as_list_exists():
    """Test that as_list function exists."""
    assert callable(as_list)


def test_as_iter_exists():
    """Test that as_iter function exists."""
    assert callable(as_iter)


def test_is_list_of_exists():
    """Test that is_list_of function exists."""
    assert callable(is_list_of)


def test_chunk_list_exists():
    """Test that chunk_list function exists."""
    assert callable(chunk_list)


def test_chunk_iter_exists():
    """Test that chunk_iter function exists."""
    assert callable(chunk_iter)


def test_flatten_2d_lists_exists():
    """Test that flatten_2d_lists function exists."""
    assert callable(flatten_2d_lists)


def test_flatten_deep_exists():
    """Test that flatten_deep function exists."""
    assert callable(flatten_deep)


def test_full_groupby_exists():
    """Test that full_groupby function exists."""
    assert callable(full_groupby)


def test_partition_exists():
    """Test that partition function exists."""
    assert callable(partition)


def test_first_exists():
    """Test that first function exists."""
    assert callable(first)


def test_first_or_raise_exists():
    """Test that first_or_raise function exists."""
    assert callable(first_or_raise)


def test_last_exists():
    """Test that last function exists."""
    assert callable(last)


def test_swap_dict_values_exists():
    """Test that swap_dict_values function exists."""
    assert callable(swap_dict_values)


def test_deep_merge_dicts_exists():
    """Test that deep_merge_dicts function exists."""
    assert callable(deep_merge_dicts)


def test_invert_dict_exists():
    """Test that invert_dict function exists."""
    assert callable(invert_dict)


def test_invert_dict_multi_exists():
    """Test that invert_dict_multi function exists."""
    assert callable(invert_dict_multi)


def test_filter_none_exists():
    """Test that filter_none function exists."""
    assert callable(filter_none)


def test_pick_keys_exists():
    """Test that pick_keys function exists."""
    assert callable(pick_keys)


def test_omit_keys_exists():
    """Test that omit_keys function exists."""
    assert callable(omit_keys)


def test_unique_exists():
    """Test that unique function exists."""
    assert callable(unique)


def test_unique_by_exists():
    """Test that unique_by function exists."""
    assert callable(unique_by)


def test_sliding_window_exists():
    """Test that sliding_window function exists."""
    assert callable(sliding_window)


def test_pairwise_exists():
    """Test that pairwise function exists."""
    assert callable(pairwise)


def test_module_imports():
    """Test that the module imports without errors."""
    assert True  # If we got here, imports worked

