#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from core.base.logic.structures.object_pool import Resettable, PoolStats, ObjectPool, TypedObjectPool, BufferPool, TieredBufferPool, PooledContextManager, get_list_pool, get_dict_pool, get_set_pool, pooled_list, pooled_dict, pooled_set


def test_resettable_basic():
    assert Resettable is not None


def test_poolstats_basic():
    assert PoolStats is not None


def test_objectpool_basic():
    assert ObjectPool is not None


def test_typedobjectpool_basic():
    assert TypedObjectPool is not None


def test_bufferpool_basic():
    assert BufferPool is not None


def test_tieredbufferpool_basic():
    assert TieredBufferPool is not None


def test_pooledcontextmanager_basic():
    assert PooledContextManager is not None


def test_get_list_pool_basic():
    assert callable(get_list_pool)


def test_get_dict_pool_basic():
    assert callable(get_dict_pool)


def test_get_set_pool_basic():
    assert callable(get_set_pool)


def test_pooled_list_basic():
    assert callable(pooled_list)


def test_pooled_dict_basic():
    assert callable(pooled_dict)


def test_pooled_set_basic():
    assert callable(pooled_set)
