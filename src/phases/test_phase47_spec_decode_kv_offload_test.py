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
from .test_phase47_spec_decode_kv_offload import TestEagleProposer, TestNgramProposer, TestSpecDecodeMetadataV2, TestARCOffloadManager, TestLRUOffloadManager, TestBlockTableV2, TestRustPhase47, TestPhase47Integration


def test_testeagleproposer_basic():
    assert TestEagleProposer is not None


def test_testngramproposer_basic():
    assert TestNgramProposer is not None


def test_testspecdecodemetadatav2_basic():
    assert TestSpecDecodeMetadataV2 is not None


def test_testarcoffloadmanager_basic():
    assert TestARCOffloadManager is not None


def test_testlruoffloadmanager_basic():
    assert TestLRUOffloadManager is not None


def test_testblocktablev2_basic():
    assert TestBlockTableV2 is not None


def test_testrustphase47_basic():
    assert TestRustPhase47 is not None


def test_testphase47integration_basic():
    assert TestPhase47Integration is not None
