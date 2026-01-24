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

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Tool Parser Framework - Model-Specific Parsing

"""
Tool/function call parsing with model-specific parsers.

Inspired by vLLM's tool_parsers patterns, this module provides:
- Model-specific tool call parsing (Hermes, Llama3, Mistral, etc.)
- Streaming tool call extraction
- JSON schema validation
- Multi-tool support

Beyond vLLM:
- Unified parser registry
- Streaming partial JSON parsing
- Auto-detection of tool format
- Tool call validation

NOTE: This file is now a backwards-compatibility wrapper.
The actual implementations have been split into:
- parser/ - Base classes and parser implementations
- validator/ - Schema validation
- registry/ - Parser registry and streaming parser
"""

from __future__ import annotations

# Re-export from parser module
from .parser import (  # Enums; Data Classes; Base Class; Parsers; Utilities
    GraniteToolParser, HermesToolParser, JsonToolParser, Llama3ToolParser,
    MistralToolParser, StreamingToolState, ToolCall, ToolCallStatus,
    ToolParameter, ToolParser, ToolParseResult, ToolParserType,
    extract_json_from_text)
# Re-export from registry module
from .registry import StreamingToolParser, ToolParserRegistry, parse_tool_call
# Re-export from validator module
from .validator import (validate_argument_type, validate_tool_call,
                        validate_tool_schema)

__all__ = [
    # Enums
    "ToolParserType",
    "ToolCallStatus",
    # Data Classes
    "ToolParameter",
    "ToolCall",
    "ToolParseResult",
    "StreamingToolState",
    # Base Class
    "ToolParser",
    # Parsers
    "JsonToolParser",
    "HermesToolParser",
    "Llama3ToolParser",
    "MistralToolParser",
    "GraniteToolParser",
    # Registry
    "ToolParserRegistry",
    # Streaming
    "StreamingToolParser",
    # Utilities
    "parse_tool_call",
    "extract_json_from_text",
    "validate_tool_call",
    "validate_tool_schema",
    "validate_argument_type",
]
