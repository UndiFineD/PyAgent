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
# Phase 41: Tool Parser Framework - Base Classes

"""
Base classes and data structures for tool parsing.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

# =============================================================================
# Enums
# =============================================================================


class ToolParserType(Enum):
    """Supported tool parser types."""

    GENERIC_JSON = auto()  # Generic JSON parsing
    HERMES = auto()  # Hermes/NousResearch format
    LLAMA3 = auto()  # Llama 3 function calling
    MISTRAL = auto()  # Mistral AI format
    GRANITE = auto()  # IBM Granite format
    QWEN = auto()  # Qwen format
    JAMBA = auto()  # AI21 Jamba format
    DEEPSEEKV3 = auto()  # DeepSeek V3 format
    INTERNLM = auto()  # InternLM format
    PYTHONIC = auto()  # Python-style function calls


class ToolCallStatus(Enum):
    """Tool call parsing status."""

    PENDING = auto()  # Still parsing
    COMPLETE = auto()  # Successfully parsed
    INVALID = auto()  # Parse error
    PARTIAL = auto()  # Partial/streaming


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class ToolParameter:
    """Tool parameter definition."""

    name: str
    param_type: str = "string"
    description: str = ""
    required: bool = True
    default: Optional[Any] = None
    enum: Optional[List[str]] = None


@dataclass
class ToolCall:
    """Parsed tool/function call."""

    id: str  # Unique call ID
    name: str  # Function/tool name
    arguments: Dict[str, Any]  # Parsed arguments
    raw_arguments: str = ""  # Original JSON string
    status: ToolCallStatus = ToolCallStatus.COMPLETE
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": "function",
            "function": {
                "name": self.name,
                "arguments": self.raw_arguments or json.dumps(self.arguments),
            },
        }

    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI API format."""
        return {
            "id": self.id,
            "type": "function",
            "function": {
                "name": self.name,
                "arguments": self.raw_arguments or json.dumps(self.arguments),
            },
        }


@dataclass
class ToolParseResult:
    """Result of tool call parsing."""

    tool_calls: List[ToolCall] = field(default_factory=list)
    content: str = ""  # Non-tool content
    raw_output: str = ""  # Full raw output
    complete: bool = True
    errors: List[str] = field(default_factory=list)

    @property
    def has_tool_calls(self) -> bool:
        return bool(self.tool_calls)

    @property
    def is_valid(self) -> bool:
        return all(tc.status == ToolCallStatus.COMPLETE for tc in self.tool_calls)


@dataclass
class StreamingToolState:
    """State for streaming tool parsing."""

    buffer: str = ""
    in_tool_call: bool = False
    current_tool: Optional[ToolCall] = None
    completed_tools: List[ToolCall] = field(default_factory=list)
    tool_call_index: int = 0
    brace_depth: int = 0
    in_string: bool = False


# =============================================================================
# Base Tool Parser
# =============================================================================


class ToolParser(ABC):
    """Base class for tool parsers."""

    @property
    @abstractmethod
    def parser_type(self) -> ToolParserType:
        """Return parser type."""
        ...

    @abstractmethod
    def parse(self, text: str) -> ToolParseResult:
        """
        Parse tool calls from text.

        Args:
            text: Model output text

        Returns:
            ToolParseResult with extracted tool calls
        """
        ...

    @abstractmethod
    def parse_streaming(
        self,
        delta: str,
        state: StreamingToolState,
    ) -> Tuple[StreamingToolState, Optional[ToolCall]]:
        """
        Parse streaming token.

        Args:
            delta: New token(s)
            state: Current parsing state

        Returns:
            (updated_state, completed_tool_call_if_any)
        """
        ...

    def _generate_call_id(self, index: int = 0) -> str:
        """Generate a unique call ID."""
        import uuid

        return f"call_{uuid.uuid4().hex[:24]}"


# =============================================================================
# Utility Functions
# =============================================================================


def extract_json_from_text(text: str) -> List[str]:
    """
    Extract all JSON objects from text.

    Returns:
        List of JSON strings
    """
    results = []

    brace_depth = 0
    start_idx = -1
    in_string = False

    for i, char in enumerate(text):
        if char == '"' and (i == 0 or text[i - 1] != "\\"):
            in_string = not in_string
        elif not in_string:
            if char == "{":
                if brace_depth == 0:
                    start_idx = i
                brace_depth += 1
            elif char == "}":
                brace_depth -= 1
                if brace_depth == 0 and start_idx >= 0:
                    results.append(text[start_idx : i + 1])
                    start_idx = -1

    return results
