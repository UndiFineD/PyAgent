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

import pytest
from infrastructure.engine.pooling.pooling_metadata import PoolingStrategy, PoolingCursor, PoolingStates, PoolingMetadata, Pooler, MeanPooler, MaxPooler, LastTokenPooler, AttentionWeightedPooler, PoolerFactory, PoolerOutput, ChunkedPoolingManager, pool_with_rust


def test_poolingstrategy_basic():
    assert PoolingStrategy is not None


def test_poolingcursor_basic():
    assert PoolingCursor is not None


def test_poolingstates_basic():
    assert PoolingStates is not None


def test_poolingmetadata_basic():
    assert PoolingMetadata is not None


def test_pooler_basic():
    assert Pooler is not None


def test_meanpooler_basic():
    assert MeanPooler is not None


def test_maxpooler_basic():
    assert MaxPooler is not None


def test_lasttokenpooler_basic():
    assert LastTokenPooler is not None


def test_attentionweightedpooler_basic():
    assert AttentionWeightedPooler is not None


def test_poolerfactory_basic():
    assert PoolerFactory is not None


def test_pooleroutput_basic():
    assert PoolerOutput is not None


def test_chunkedpoolingmanager_basic():
    assert ChunkedPoolingManager is not None


def test_pool_with_rust_basic():
    assert callable(pool_with_rust)
