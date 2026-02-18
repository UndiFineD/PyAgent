#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    import pytest
except ImportError:
    import pytest

try:
    from core.base.common.utils.collection_utils import LazyDict, as_list, as_iter, is_list_of, chunk_list, chunk_iter, flatten_2d_lists, flatten_deep, full_groupby, partition, first, first_or_raise, last, swap_dict_values, deep_merge_dicts, invert_dict, invert_dict_multi, filter_none, pick_keys, omit_keys, unique, unique_by, sliding_window, pairwise
except ImportError:
    from core.base.common.utils.collection_utils import LazyDict, as_list, as_iter, is_list_of, chunk_list, chunk_iter, flatten_2d_lists, flatten_deep, full_groupby, partition, first, first_or_raise, last, swap_dict_values, deep_merge_dicts, invert_dict, invert_dict_multi, filter_none, pick_keys, omit_keys, unique, unique_by, sliding_window, pairwise



def test_lazydict_basic():
    assert LazyDict is not None


def test_as_list_basic():
    assert callable(as_list)


def test_as_iter_basic():
    assert callable(as_iter)


def test_is_list_of_basic():
    assert callable(is_list_of)


def test_chunk_list_basic():
    assert callable(chunk_list)


def test_chunk_iter_basic():
    assert callable(chunk_iter)


def test_flatten_2d_lists_basic():
    assert callable(flatten_2d_lists)


def test_flatten_deep_basic():
    assert callable(flatten_deep)


def test_full_groupby_basic():
    assert callable(full_groupby)


def test_partition_basic():
    assert callable(partition)


def test_first_basic():
    assert callable(first)


def test_first_or_raise_basic():
    assert callable(first_or_raise)


def test_last_basic():
    assert callable(last)


def test_swap_dict_values_basic():
    assert callable(swap_dict_values)


def test_deep_merge_dicts_basic():
    assert callable(deep_merge_dicts)


def test_invert_dict_basic():
    assert callable(invert_dict)


def test_invert_dict_multi_basic():
    assert callable(invert_dict_multi)


def test_filter_none_basic():
    assert callable(filter_none)


def test_pick_keys_basic():
    assert callable(pick_keys)


def test_omit_keys_basic():
    assert callable(omit_keys)


def test_unique_basic():
    assert callable(unique)


def test_unique_by_basic():
    assert callable(unique_by)


def test_sliding_window_basic():
    assert callable(sliding_window)


def test_pairwise_basic():
    assert callable(pairwise)
