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

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 40: Reasoning Engine Package

Reasoning Engine for extracting thinking tokens and tool calls.

This package provides:
- ReasoningParser: Extract <think>...</think> tokens
- ToolParser: Parse function/tool calls from generation
- ReasoningEngine: Unified reasoning extraction

from .reasoning_engine import (  # Enums; Data classes; Core classes; Parser implementations; Factory  # noqa: F401
    DeepSeekReasoningParser, GenericReasoningParser, HermesToolParser,
    OpenAIToolParser, ParseResult, ParseState, QwenReasoningParser,
    ReasoningEngine, ReasoningFormat, ReasoningParser, ReasoningToken,
    ThinkingBlock, ToolCall, ToolCallFormat, ToolCallResult, ToolParser,
    create_reasoning_engine, create_tool_parser)

__all__ = [
    # Enums
    "ReasoningFormat","    "ToolCallFormat","    "ParseState","    # Data classes
    "ReasoningToken","    "ThinkingBlock","    "ToolCall","    "ToolCallResult","    "ParseResult","    # Core classes
    "ReasoningParser","    "ToolParser","    "ReasoningEngine","    # Implementations
    "DeepSeekReasoningParser","    "QwenReasoningParser","    "GenericReasoningParser","    "OpenAIToolParser","    "HermesToolParser","    # Factory
    "create_reasoning_engine","    "create_tool_parser","]
