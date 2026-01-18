import os

file_path = r"c:\DEV\PyAgent\src\infrastructure\reasoning\ReasoningEngine.py"
wrapper_content = """# Copyright (c) 2026 PyAgent Authors. All rights reserved.
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

with open(file_path, "w", encoding="utf-8") as f:
    f.write(wrapper_content)

print(f"Successfully overwrote {file_path}")
