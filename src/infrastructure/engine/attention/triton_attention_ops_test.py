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
    from infrastructure.engine.attention.triton_attention_ops import AttentionBackend, PrecisionMode, AttentionConfig, AttentionMetadata, AttentionKernel, TritonPagedAttention, NaiveAttention, SlidingWindowAttention, KVSplitConfig, TritonAttentionOps, create_attention_ops
except ImportError:
    from infrastructure.engine.attention.triton_attention_ops import AttentionBackend, PrecisionMode, AttentionConfig, AttentionMetadata, AttentionKernel, TritonPagedAttention, NaiveAttention, SlidingWindowAttention, KVSplitConfig, TritonAttentionOps, create_attention_ops



def test_attentionbackend_basic():
    assert AttentionBackend is not None


def test_precisionmode_basic():
    assert PrecisionMode is not None


def test_attentionconfig_basic():
    assert AttentionConfig is not None


def test_attentionmetadata_basic():
    assert AttentionMetadata is not None


def test_attentionkernel_basic():
    assert AttentionKernel is not None


def test_tritonpagedattention_basic():
    assert TritonPagedAttention is not None


def test_naiveattention_basic():
    assert NaiveAttention is not None


def test_slidingwindowattention_basic():
    assert SlidingWindowAttention is not None


def test_kvsplitconfig_basic():
    assert KVSplitConfig is not None


def test_tritonattentionops_basic():
    assert TritonAttentionOps is not None


def test_create_attention_ops_basic():
    assert callable(create_attention_ops)
