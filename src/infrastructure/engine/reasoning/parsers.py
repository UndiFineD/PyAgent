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

"""
Parsers.py module.
"""

from abc import ABC, abstractmethod
from typing import Generator, Iterator, List, Optional, Tuple

from .data_classes import ParseResult, ThinkingBlock, ToolCall
from .enums import ParseState, ReasoningFormat, ToolCallFormat


class ReasoningParser(ABC):
    """Abstract base for reasoning token extraction."""

    def __init__(
        self,
        reasoning_format: ReasoningFormat = ReasoningFormat.GENERIC,
        start_marker: str = "<think>",
        end_marker: str = "</think>",
    ) -> None:
        self.reasoning_format = reasoning_format
        self.start_marker = start_marker
        self.end_marker = end_marker
        self.state = ParseState.IDLE
        self.buffer = ""
        self.thinking_blocks: List[ThinkingBlock] = []
        self._current_block_start = 0

    @abstractmethod
    def extract_thinking(self, text: str) -> Tuple[str, List[ThinkingBlock]]:
        """Extract thinking blocks from text, return content and blocks."""
        raise NotImplementedError

    @abstractmethod
    def parse_streaming(self, token_stream: Iterator[str]) -> Generator[Tuple[str, bool], None, ParseResult]:
        """Parse streaming tokens, yield (token, is_thinking)."""
        raise NotImplementedError

    def reset(self) -> None:
        """Reset parser state."""
        self.state = ParseState.IDLE
        self.buffer = ""
        self.thinking_blocks = []
        self._current_block_start = 0


class ToolParser(ABC):
    """Abstract base for tool/function call parsing."""

    def __init__(
        self,
        tool_format: ToolCallFormat = ToolCallFormat.OPENAI,
        strict: bool = False,
    ) -> None:
        self.tool_format = tool_format
        self.strict = strict
        self._tool_call_counter = 0

    @abstractmethod
    def parse_tool_calls(self, text: str) -> List[ToolCall]:
        """Parse tool calls from text."""
        raise NotImplementedError

    @abstractmethod
    def parse_streaming(
        self, token_stream: Iterator[str]
    ) -> Generator[Tuple[str, Optional[ToolCall]], None, List[ToolCall]]:
        """Parse streaming tokens for tool calls."""
        raise NotImplementedError

    def generate_call_id(self) -> str:
        """Generate unique tool call ID."""
        self._tool_call_counter += 1
        return f"call_{self._tool_call_counter:08d}"

    def reset(self) -> None:
        """Reset parser state."""
        self._tool_call_counter = 0
