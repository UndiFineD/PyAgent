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
from .test_phase40_rust import TestReasoningParserRust, TestMultiModalCacheRust, TestPoolingRust, TestInputPreprocessorRust, TestAdvancedSamplingRust


def test_testreasoningparserrust_basic():
    assert TestReasoningParserRust is not None


def test_testmultimodalcacherust_basic():
    assert TestMultiModalCacheRust is not None


def test_testpoolingrust_basic():
    assert TestPoolingRust is not None


def test_testinputpreprocessorrust_basic():
    assert TestInputPreprocessorRust is not None


def test_testadvancedsamplingrust_basic():
    assert TestAdvancedSamplingRust is not None
