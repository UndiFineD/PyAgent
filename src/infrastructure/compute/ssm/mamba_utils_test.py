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
from infrastructure.compute.ssm.mamba_utils import MambaBlockState, compute_ssm_state_shape, compute_conv_state_shape, compute_state_dtype, discretize_ssm, apply_ssm_recurrence, silu_activation, swish_activation, softplus, chunk_sequence, merge_chunks, parallel_scan, init_A_log, init_dt_proj


def test_mambablockstate_basic():
    assert MambaBlockState is not None


def test_compute_ssm_state_shape_basic():
    assert callable(compute_ssm_state_shape)


def test_compute_conv_state_shape_basic():
    assert callable(compute_conv_state_shape)


def test_compute_state_dtype_basic():
    assert callable(compute_state_dtype)


def test_discretize_ssm_basic():
    assert callable(discretize_ssm)


def test_apply_ssm_recurrence_basic():
    assert callable(apply_ssm_recurrence)


def test_silu_activation_basic():
    assert callable(silu_activation)


def test_swish_activation_basic():
    assert callable(swish_activation)


def test_softplus_basic():
    assert callable(softplus)


def test_chunk_sequence_basic():
    assert callable(chunk_sequence)


def test_merge_chunks_basic():
    assert callable(merge_chunks)


def test_parallel_scan_basic():
    assert callable(parallel_scan)


def test_init_A_log_basic():
    assert callable(init_A_log)


def test_init_dt_proj_basic():
    assert callable(init_dt_proj)
