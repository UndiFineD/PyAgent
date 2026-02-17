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
from infrastructure.engine.loading.weight_loader import WeightFormat, WeightSpec, LoadStats, AtomicWriter, WeightLoader, SafetensorsLoader, MultiThreadWeightLoader, FastSafetensorsLoader, StreamingWeightLoader, GGUFLoader, atomic_writer, detect_weight_format, get_file_lock_path, compute_weight_hash_rust, validate_weight_shapes_rust, filter_shared_tensors


def test_weightformat_basic():
    assert WeightFormat is not None


def test_weightspec_basic():
    assert WeightSpec is not None


def test_loadstats_basic():
    assert LoadStats is not None


def test_atomicwriter_basic():
    assert AtomicWriter is not None


def test_weightloader_basic():
    assert WeightLoader is not None


def test_safetensorsloader_basic():
    assert SafetensorsLoader is not None


def test_multithreadweightloader_basic():
    assert MultiThreadWeightLoader is not None


def test_fastsafetensorsloader_basic():
    assert FastSafetensorsLoader is not None


def test_streamingweightloader_basic():
    assert StreamingWeightLoader is not None


def test_ggufloader_basic():
    assert GGUFLoader is not None


def test_atomic_writer_basic():
    assert callable(atomic_writer)


def test_detect_weight_format_basic():
    assert callable(detect_weight_format)


def test_get_file_lock_path_basic():
    assert callable(get_file_lock_path)


def test_compute_weight_hash_rust_basic():
    assert callable(compute_weight_hash_rust)


def test_validate_weight_shapes_rust_basic():
    assert callable(validate_weight_shapes_rust)


def test_filter_shared_tensors_basic():
    assert callable(filter_shared_tensors)
