# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 40: Reasoning Engine Package

"""
Reasoning Engine for extracting thinking tokens and tool calls.

This package provides:
- ReasoningParser: Extract <think>...</think> tokens
- ToolParser: Parse function/tool calls from generation
- ReasoningEngine: Unified reasoning extraction
"""

from .reasoning_engine import (
    # Enums
    ReasoningFormat,
    ToolCallFormat,
    ParseState,

    # Data classes
    ReasoningToken,
    ThinkingBlock,
    ToolCall,
    ToolCallResult,
    ParseResult,

    # Core classes
    ReasoningParser,
    ToolParser,
    ReasoningEngine,

    # Parser implementations
    DeepSeekReasoningParser,
    QwenReasoningParser,
    GenericReasoningParser,
    OpenAIToolParser,
    HermesToolParser,

    # Factory
    create_reasoning_engine,
    create_tool_parser,
)

__all__ = [
    # Enums
    "ReasoningFormat",
    "ToolCallFormat",
    "ParseState",

    # Data classes
    "ReasoningToken",
    "ThinkingBlock",
    "ToolCall",
    "ToolCallResult",
    "ParseResult",

    # Core classes
    "ReasoningParser",
    "ToolParser",
    "ReasoningEngine",

    # Implementations
    "DeepSeekReasoningParser",
    "QwenReasoningParser",
    "GenericReasoningParser",
    "OpenAIToolParser",
    "HermesToolParser",

    # Factory
    "create_reasoning_engine",
    "create_tool_parser",
]
