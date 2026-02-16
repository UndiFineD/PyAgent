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
from .test_phase36_cudagraph import TestCUDAGraphManager, TestUBatchProcessor, TestCudagraphDispatcher, TestTorchCompileIntegration, TestInputBufferManager, TestCompilationCounter, TestRustCUDAGraphFunctions, TestPhase36Integration


def test_testcudagraphmanager_basic():
    assert TestCUDAGraphManager is not None


def test_testubatchprocessor_basic():
    assert TestUBatchProcessor is not None


def test_testcudagraphdispatcher_basic():
    assert TestCudagraphDispatcher is not None


def test_testtorchcompileintegration_basic():
    assert TestTorchCompileIntegration is not None


def test_testinputbuffermanager_basic():
    assert TestInputBufferManager is not None


def test_testcompilationcounter_basic():
    assert TestCompilationCounter is not None


def test_testrustcudagraphfunctions_basic():
    assert TestRustCUDAGraphFunctions is not None


def test_testphase36integration_basic():
    assert TestPhase36Integration is not None
