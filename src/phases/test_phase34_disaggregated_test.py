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
from .test_phase34_disaggregated import TestKVTransferConnector, TestRotaryEmbeddingEngine, TestSpeculativeEngine, TestDisaggregatedScheduler, TestTritonAttentionOps, TestBatchDCPWrapper, TestRustPhase34Accelerations, TestPhase34Integration, TestPhase34Performance, fixture_rust_core, fixture_rust_core_alias


def test_testkvtransferconnector_basic():
    assert TestKVTransferConnector is not None


def test_testrotaryembeddingengine_basic():
    assert TestRotaryEmbeddingEngine is not None


def test_testspeculativeengine_basic():
    assert TestSpeculativeEngine is not None


def test_testdisaggregatedscheduler_basic():
    assert TestDisaggregatedScheduler is not None


def test_testtritonattentionops_basic():
    assert TestTritonAttentionOps is not None


def test_testbatchdcpwrapper_basic():
    assert TestBatchDCPWrapper is not None


def test_testrustphase34accelerations_basic():
    assert TestRustPhase34Accelerations is not None


def test_testphase34integration_basic():
    assert TestPhase34Integration is not None


def test_testphase34performance_basic():
    assert TestPhase34Performance is not None


def test_fixture_rust_core_basic():
    assert callable(fixture_rust_core)


def test_fixture_rust_core_alias_basic():
    assert callable(fixture_rust_core_alias)
