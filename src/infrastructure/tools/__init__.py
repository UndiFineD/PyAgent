# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Tool Parser Framework Package

"""
Tool/function call parsing framework with model-specific parsers.

Exports:
    - ToolParserType: Parser type enum
    - ToolCall: Parsed tool call
    - ToolParseResult: Parse result with validation
    - ToolParser: Base parser protocol
    - ToolParserRegistry: Parser registration
    - StreamingToolParser: Streaming extraction
"""

from .ToolParserFramework import (
    # Enums
    ToolParserType,
    ToolCallStatus,
    # Data Classes
    ToolParameter,
    ToolCall,
    ToolParseResult,
    StreamingToolState,
    # Protocols/Base
    ToolParser,
    # Parsers
    JsonToolParser,
    HermesToolParser,
    Llama3ToolParser,
    MistralToolParser,
    GraniteToolParser,
    # Registry
    ToolParserRegistry,
    # Streaming
    StreamingToolParser,
    # Utilities
    parse_tool_call,
    extract_json_from_text,
    validate_tool_call,
)

__all__ = [
    # Enums
    "ToolParserType",
    "ToolCallStatus",
    # Data Classes
    "ToolParameter",
    "ToolCall",
    "ToolParseResult",
    "StreamingToolState",
    # Protocols/Base
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
]
