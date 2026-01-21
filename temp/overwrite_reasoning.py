"""
Script to overwrite ReasoningEngine with a modular wrapper.
"""

FILE_PATH = r"c:\DEV\PyAgent\src\infrastructure\reasoning\ReasoningEngine.py"
WRAPPER_CONTENT = """# Copyright (c) 2026 PyAgent Authors. All rights reserved.
\"\"\"
ReasoningEngine: Wrapper for modular reasoning and tool call components.
\"\"\"

from .Enums import ReasoningFormat, ToolCallFormat, ParseState
from .DataClasses import ReasoningToken, ThinkingBlock, ToolCall, ToolCallResult, ParseResult
from .Parsers import ReasoningParser, ToolParser
from .Implementations import (
    DeepSeekReasoningParser, QwenReasoningParser, GenericReasoningParser,
    OpenAIToolParser, HermesToolParser
)
from .Engine import ReasoningEngine, create_reasoning_engine, create_tool_parser

__all__ = [
    "ReasoningFormat",
    "ToolCallFormat",
    "ParseState",
    "ReasoningToken",
    "ThinkingBlock",
    "ToolCall",
    "ToolCallResult",
    "ParseResult",
    "ReasoningParser",
    "ToolParser",
    "DeepSeekReasoningParser",
    "QwenReasoningParser",
    "GenericReasoningParser",
    "OpenAIToolParser",
    "HermesToolParser",
    "ReasoningEngine",
    "create_reasoning_engine",
    "create_tool_parser",
]
"""

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(WRAPPER_CONTENT)

print(f"Successfully overwrote {FILE_PATH}")
