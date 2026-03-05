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

Structure:
    - parser/     - Base classes and parser implementations
    - validator/  - Schema validation logic
    - registry/   - Parser registry and streaming parser
"""

# Import from split modules (preferred)
from .parser import (
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
    # Utilities
    extract_json_from_text,
)

from .validator import (
    validate_tool_call,
    validate_tool_schema,
    validate_argument_type,
)

from .registry import (
    ToolParserRegistry,
    StreamingToolParser,
    parse_tool_call,
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
    "validate_tool_schema",
    "validate_argument_type",
]
