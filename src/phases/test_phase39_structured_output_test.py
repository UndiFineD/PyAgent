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
from .test_phase39_structured_output import TestStructuredOutputManager, TestGrammarEngine, TestLogitProcessor, TestSpeculativeDecodingV2, TestTensorizer, TestPhase39RustFunctions, TestPhase39Integration


def test_teststructuredoutputmanager_basic():
    assert TestStructuredOutputManager is not None


def test_testgrammarengine_basic():
    assert TestGrammarEngine is not None


def test_testlogitprocessor_basic():
    assert TestLogitProcessor is not None


def test_testspeculativedecodingv2_basic():
    assert TestSpeculativeDecodingV2 is not None


def test_testtensorizer_basic():
    assert TestTensorizer is not None


def test_testphase39rustfunctions_basic():
    assert TestPhase39RustFunctions is not None


def test_testphase39integration_basic():
    assert TestPhase39Integration is not None
