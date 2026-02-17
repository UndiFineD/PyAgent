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
from infrastructure.services.tools.parser.base import ToolParserType, ToolCallStatus, ToolParameter, ToolCall, ToolParseResult, StreamingToolState, ToolParser, extract_json_from_text


def test_toolparsertype_basic():
    assert ToolParserType is not None


def test_toolcallstatus_basic():
    assert ToolCallStatus is not None


def test_toolparameter_basic():
    assert ToolParameter is not None


def test_toolcall_basic():
    assert ToolCall is not None


def test_toolparseresult_basic():
    assert ToolParseResult is not None


def test_streamingtoolstate_basic():
    assert StreamingToolState is not None


def test_toolparser_basic():
    assert ToolParser is not None


def test_extract_json_from_text_basic():
    assert callable(extract_json_from_text)
