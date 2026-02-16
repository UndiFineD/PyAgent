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

import pytest
from .test_phase53_kv_v2 import test_block_table_allocation_v2, test_kv_cache_interface_storage, test_block_hash_manager, test_context_parallel_mask


def test_test_block_table_allocation_v2_basic():
    assert callable(test_block_table_allocation_v2)


def test_test_kv_cache_interface_storage_basic():
    assert callable(test_kv_cache_interface_storage)


def test_test_block_hash_manager_basic():
    assert callable(test_block_hash_manager)


def test_test_context_parallel_mask_basic():
    assert callable(test_context_parallel_mask)
