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
from infrastructure.engine.reasoning.data_classes import ReasoningToken, ThinkingBlock, ToolCall, ToolCallResult, ParseResult


def test_reasoningtoken_basic():
    assert ReasoningToken is not None


def test_thinkingblock_basic():
    assert ThinkingBlock is not None


def test_toolcall_basic():
    assert ToolCall is not None


def test_toolcallresult_basic():
    assert ToolCallResult is not None


def test_parseresult_basic():
    assert ParseResult is not None
