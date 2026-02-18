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
    from infrastructure.engine.pooling.strategies import BasePooler, MeanPooler, CLSPooler, LastTokenPooler, MaxPooler, AttentionPooler, WeightedMeanPooler, MatryoshkaPooler, MultiVectorPooler, StepPooler
except ImportError:
    from infrastructure.engine.pooling.strategies import BasePooler, MeanPooler, CLSPooler, LastTokenPooler, MaxPooler, AttentionPooler, WeightedMeanPooler, MatryoshkaPooler, MultiVectorPooler, StepPooler



def test_basepooler_basic():
    assert BasePooler is not None


def test_meanpooler_basic():
    assert MeanPooler is not None


def test_clspooler_basic():
    assert CLSPooler is not None


def test_lasttokenpooler_basic():
    assert LastTokenPooler is not None


def test_maxpooler_basic():
    assert MaxPooler is not None


def test_attentionpooler_basic():
    assert AttentionPooler is not None


def test_weightedmeanpooler_basic():
    assert WeightedMeanPooler is not None


def test_matryoshkapooler_basic():
    assert MatryoshkaPooler is not None


def test_multivectorpooler_basic():
    assert MultiVectorPooler is not None


def test_steppooler_basic():
    assert StepPooler is not None
