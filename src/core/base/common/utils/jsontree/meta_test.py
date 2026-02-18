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
    from core.base.common.utils.jsontree.meta import json_count_leaves, json_depth, json_filter_leaves, json_validate_leaves, json_find_leaves
except ImportError:
    from core.base.common.utils.jsontree.meta import json_count_leaves, json_depth, json_filter_leaves, json_validate_leaves, json_find_leaves



def test_json_count_leaves_basic():
    assert callable(json_count_leaves)


def test_json_depth_basic():
    assert callable(json_depth)


def test_json_filter_leaves_basic():
    assert callable(json_filter_leaves)


def test_json_validate_leaves_basic():
    assert callable(json_validate_leaves)


def test_json_find_leaves_basic():
    assert callable(json_find_leaves)
