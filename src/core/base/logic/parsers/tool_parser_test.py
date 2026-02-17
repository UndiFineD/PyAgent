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
from core.base.logic.parsers.tool_parser import ToolCall, ExtractedToolCalls, StreamingToolCallDelta, ToolParser, JSONToolParser, XMLToolParser, ToolParserManager, tool_parser, extract_tool_calls


def test_toolcall_basic():
    assert ToolCall is not None


def test_extractedtoolcalls_basic():
    assert ExtractedToolCalls is not None


def test_streamingtoolcalldelta_basic():
    assert StreamingToolCallDelta is not None


def test_toolparser_basic():
    assert ToolParser is not None


def test_jsontoolparser_basic():
    assert JSONToolParser is not None


def test_xmltoolparser_basic():
    assert XMLToolParser is not None


def test_toolparsermanager_basic():
    assert ToolParserManager is not None


def test_tool_parser_basic():
    assert callable(tool_parser)


def test_extract_tool_calls_basic():
    assert callable(extract_tool_calls)
