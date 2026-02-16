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
from core.base.logic.math.batch_invariant_ops import BatchInvariantOps, matmul_persistent, softmax_batch_invariant, log_softmax_batch_invariant, mean_batch_invariant, mm_batch_invariant, bmm_batch_invariant, addmm_batch_invariant, gelu_batch_invariant, layer_norm_batch_invariant, rms_norm_batch_invariant, attention_score_batch_invariant, attention_output_batch_invariant


def test_batchinvariantops_basic():
    assert BatchInvariantOps is not None


def test_matmul_persistent_basic():
    assert callable(matmul_persistent)


def test_softmax_batch_invariant_basic():
    assert callable(softmax_batch_invariant)


def test_log_softmax_batch_invariant_basic():
    assert callable(log_softmax_batch_invariant)


def test_mean_batch_invariant_basic():
    assert callable(mean_batch_invariant)


def test_mm_batch_invariant_basic():
    assert callable(mm_batch_invariant)


def test_bmm_batch_invariant_basic():
    assert callable(bmm_batch_invariant)


def test_addmm_batch_invariant_basic():
    assert callable(addmm_batch_invariant)


def test_gelu_batch_invariant_basic():
    assert callable(gelu_batch_invariant)


def test_layer_norm_batch_invariant_basic():
    assert callable(layer_norm_batch_invariant)


def test_rms_norm_batch_invariant_basic():
    assert callable(rms_norm_batch_invariant)


def test_attention_score_batch_invariant_basic():
    assert callable(attention_score_batch_invariant)


def test_attention_output_batch_invariant_basic():
    assert callable(attention_output_batch_invariant)
