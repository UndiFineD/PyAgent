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
# Phase 41: Tool Parser Framework - Parser Package

"""
Tool parser implementations for various model formats.

Exports all parser classes and base types.
"""

from .base import (  # Enums; Data Classes; Base Class; Utilities  # noqa: F401
    StreamingToolState, ToolCall, ToolCallStatus, ToolParameter, ToolParser,
    ToolParseResult, ToolParserType, extract_json_from_text)
from .granite_parser import GraniteToolParser  # noqa: F401
from .hermes_parser import HermesToolParser  # noqa: F401
from .json_parser import JsonToolParser  # noqa: F401
from .llama3_parser import Llama3ToolParser  # noqa: F401
from .mistral_parser import MistralToolParser  # noqa: F401

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
    # Utilities
    "extract_json_from_text",
]
