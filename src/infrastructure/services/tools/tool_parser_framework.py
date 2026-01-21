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
from .parser import (
    # Enums
    ToolParserType,
    ToolCallStatus,
    # Data Classes
    ToolParameter,
    ToolCall,
    ToolParseResult,
    StreamingToolState,
    # Base Class
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

# Re-export from validator module
from .validator import (
    validate_tool_call,
    validate_tool_schema,
    validate_argument_type,
)

# Re-export from registry module
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
