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
from infrastructure.services.execution.cuda_graph_manager import CUDAGraphMode, BatchDescriptor, CUDAGraphEntry, CUDAGraphRegistry, CUDAGraphManager, compute_graph_key, generate_warmup_sizes


def test_cudagraphmode_basic():
    assert CUDAGraphMode is not None


def test_batchdescriptor_basic():
    assert BatchDescriptor is not None


def test_cudagraphentry_basic():
    assert CUDAGraphEntry is not None


def test_cudagraphregistry_basic():
    assert CUDAGraphRegistry is not None


def test_cudagraphmanager_basic():
    assert CUDAGraphManager is not None


def test_compute_graph_key_basic():
    assert callable(compute_graph_key)


def test_generate_warmup_sizes_basic():
    assert callable(generate_warmup_sizes)
