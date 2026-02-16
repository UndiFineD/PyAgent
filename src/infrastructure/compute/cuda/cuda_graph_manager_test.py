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
from infrastructure.compute.cuda.cuda_graph_manager import CUDAGraphMode, BatchDescriptor, CUDAGraphEntry, CUDAGraphOptions, CUDAGraphStats, MockCUDAGraph, CUDAGraphWrapper, AdaptiveCUDAGraphWrapper, cudagraph_context, get_cudagraph_sizes


def test_cudagraphmode_basic():
    assert CUDAGraphMode is not None


def test_batchdescriptor_basic():
    assert BatchDescriptor is not None


def test_cudagraphentry_basic():
    assert CUDAGraphEntry is not None


def test_cudagraphoptions_basic():
    assert CUDAGraphOptions is not None


def test_cudagraphstats_basic():
    assert CUDAGraphStats is not None


def test_mockcudagraph_basic():
    assert MockCUDAGraph is not None


def test_cudagraphwrapper_basic():
    assert CUDAGraphWrapper is not None


def test_adaptivecudagraphwrapper_basic():
    assert AdaptiveCUDAGraphWrapper is not None


def test_cudagraph_context_basic():
    assert callable(cudagraph_context)


def test_get_cudagraph_sizes_basic():
    assert callable(get_cudagraph_sizes)
