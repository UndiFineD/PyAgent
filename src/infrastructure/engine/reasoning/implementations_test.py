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
from infrastructure.engine.reasoning.implementations import DeepSeekReasoningParser, QwenReasoningParser, GenericReasoningParser, OpenAIToolParser, HermesToolParser


def test_deepseekreasoningparser_basic():
    assert DeepSeekReasoningParser is not None


def test_qwenreasoningparser_basic():
    assert QwenReasoningParser is not None


def test_genericreasoningparser_basic():
    assert GenericReasoningParser is not None


def test_openaitoolparser_basic():
    assert OpenAIToolParser is not None


def test_hermestoolparser_basic():
    assert HermesToolParser is not None
