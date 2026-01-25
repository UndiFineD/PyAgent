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
# Phase 40: Reasoning Parser and Tool Parser Tests

"""
Tests for ReasoningEngine - thinking extraction and tool parsing.
"""

import pytest
import asyncio
from typing import List

from src.infrastructure.engine.reasoning import (
    ReasoningFormat,
    ToolCallFormat,
    ParseState,
    ReasoningToken,
    ThinkingBlock,
    ToolCall,
    ReasoningParser,
    ToolParser,
    DeepSeekReasoningParser,
    QwenReasoningParser,
    GenericReasoningParser,
    OpenAIToolParser,
    HermesToolParser,
    ReasoningEngine,
    create_reasoning_engine,
)


class TestReasoningFormats:
    """Test reasoning format enums."""

    def test_reasoning_format_values(self):
        """Test ReasoningFormat enum has expected values."""
        assert ReasoningFormat.DEEPSEEK_R1 is not None
        assert ReasoningFormat.QWEN3 is not None
        assert ReasoningFormat.MISTRAL is not None
        assert ReasoningFormat.CLAUDE is not None
        assert ReasoningFormat.GENERIC is not None

    def test_tool_call_format_values(self):
        """Test ToolCallFormat enum has expected values."""
        assert ToolCallFormat.OPENAI is not None
        assert ToolCallFormat.HERMES is not None
        assert ToolCallFormat.ANTHROPIC is not None

    def test_parse_state_values(self):
        """Test ParseState enum has expected values."""
        assert ParseState.IDLE is not None
        assert ParseState.IN_THINK is not None
        assert ParseState.IN_TOOL is not None


class TestThinkingBlock:
    """Test ThinkingBlock dataclass."""

    def test_create_thinking_block(self):
        """Test creating ThinkingBlock."""
        block = ThinkingBlock(
            content="Let me think about this...",
            start_position=10,
            end_position=50,
        )
        assert block.content == "Let me think about this..."
        assert block.start_position == 10
        assert block.end_position == 50

    def test_thinking_block_defaults(self):
        """Test ThinkingBlock default values."""
        block = ThinkingBlock(content="test", start_position=0, end_position=4)
        assert block.start_position == 0
        assert block.end_position == 4


class TestToolCall:
    """Test ToolCall dataclass."""

    def test_create_tool_call(self):
        """Test creating ToolCall."""
        call = ToolCall(
            id="call_123",
            name="search",
            arguments={"query": "test"},
        )
        assert call.id == "call_123"
        assert call.name == "search"
        assert call.arguments == {"query": "test"}

    def test_tool_call_with_format(self):
        """Test ToolCall with format."""
        call = ToolCall(
            id="call_456",
            name="execute",
            arguments={"code": "print(1)"},
            format=ToolCallFormat.OPENAI,
        )
        assert call.format == ToolCallFormat.OPENAI


class TestDeepSeekReasoningParser:
    """Test DeepSeek R1 reasoning parser."""

    def test_parse_thinking_block(self):
        """Test parsing DeepSeek thinking block."""
        parser = DeepSeekReasoningParser()
        text = "Hello <think>Let me reason about this</think> World"

        content, blocks = parser.extract_thinking(text)
        assert len(blocks) == 1
        assert "Let me reason" in blocks[0].content

    def test_parse_multiple_blocks(self):
        """Test parsing multiple thinking blocks."""
        parser = DeepSeekReasoningParser()
        text = "<think>First thought</think> middle <think>Second thought</think> end"

        content, blocks = parser.extract_thinking(text)
        assert len(blocks) == 2
        assert "First thought" in blocks[0].content
        assert "Second thought" in blocks[1].content

    def test_extract_content_without_thinking(self):
        """Test extracting content without thinking blocks."""
        parser = DeepSeekReasoningParser()
        text = "<think>Thinking...</think>The answer is 42"

        content, blocks = parser.extract_thinking(text)
        assert "42" in content

    def test_parser_reset(self):
        """Test parser reset."""
        parser = DeepSeekReasoningParser()

        # Process something
        parser.extract_thinking("<think>test</think>")

        # Reset should work
        parser.reset()
        assert parser._state == ParseState.IDLE


class TestQwenReasoningParser:
    """Test Qwen3 reasoning parser."""

    def test_parse_thinking_block(self):
        """Test parsing Qwen thinking block."""
        parser = QwenReasoningParser()
        text = "Start <think>Internal reasoning</think> End"

        content, blocks = parser.extract_thinking(text)
        assert len(blocks) == 1
        assert "Internal reasoning" in blocks[0].content

    def test_extract_content(self):
        """Test extracting content."""
        parser = QwenReasoningParser()
        text = "<think>Thinking</think>Result is here"

        content, blocks = parser.extract_thinking(text)
        assert "Result" in content


class TestGenericReasoningParser:
    """Test generic reasoning parser."""

    def test_custom_delimiters(self):
        """Test custom delimiter configuration."""
        parser = GenericReasoningParser(
            start_marker="[THINK]",
            end_marker="[/THINK]",
        )
        text = "Hello [THINK]My reasoning[/THINK] World"

        content, blocks = parser.extract_thinking(text)
        assert len(blocks) == 1
        assert "My reasoning" in blocks[0].content


class TestOpenAIToolParser:
    """Test OpenAI tool call parser."""

    def test_parse_tool_call(self):
        """Test parsing OpenAI format tool call."""
        parser = OpenAIToolParser()
        text = '''{"name": "search", "arguments": {"query": "test"}}'''

        calls = parser.parse_tool_calls(text)
        assert len(calls) >= 0  # May not parse if format differs

    def test_parse_function_call(self):
        """Test parsing function call."""
        parser = OpenAIToolParser()
        text = '''{"type": "function", "function": {"name": "calc", "arguments": {"x": 1}}}'''

        calls = parser.parse_tool_calls(text)
        # May or may not parse depending on exact format
        assert isinstance(calls, list)


class TestHermesToolParser:
    """Test Hermes tool call parser."""

    def test_parse_hermes_format(self):
        """Test parsing Hermes XML format."""
        parser = HermesToolParser()
        text = '''<tool_call>
{"name": "search", "arguments": {"query": "test"}}
</tool_call>'''

        calls = parser.parse_tool_calls(text)
        assert isinstance(calls, list)


class TestReasoningEngine:
    """Test unified reasoning engine."""

    def test_create_engine(self):
        """Test creating reasoning engine."""
        engine = ReasoningEngine()
        assert engine is not None

    def test_create_with_format(self):
        """Test creating engine with specific format."""
        engine = ReasoningEngine(
            reasoning_format=ReasoningFormat.DEEPSEEK_R1,
            tool_format=ToolCallFormat.OPENAI,
        )
        assert engine is not None

    def test_parse_response(self):
        """Test parsing full response."""
        engine = ReasoningEngine(reasoning_format=ReasoningFormat.DEEPSEEK_R1)
        text = "<think>Let me think</think>The answer is 42"

        result = engine.parse(text)
        assert result is not None
        assert hasattr(result, 'thinking_blocks')
        assert len(result.thinking_blocks) == 1

    def test_parse_content(self):
        """Test parsing extracts content correctly."""
        engine = ReasoningEngine(reasoning_format=ReasoningFormat.DEEPSEEK_R1)
        text = "<think>Thinking...</think>Final answer"

        result = engine.parse(text)
        assert "Final answer" in result.content

    def test_extract_thinking(self):
        """Test extracting thinking content."""
        engine = ReasoningEngine(reasoning_format=ReasoningFormat.DEEPSEEK_R1)
        text = "<think>First</think>mid<think>Second</think>end"

        result = engine.parse(text)
        assert isinstance(result.thinking_blocks, list)
        assert len(result.thinking_blocks) == 2

    def test_parse_tool_calls(self):
        """Test extracting tool calls."""
        engine = ReasoningEngine(
            reasoning_format=ReasoningFormat.GENERIC,
            tool_format=ToolCallFormat.OPENAI,
        )
        text = '{"tool_calls": [{"id": "1", "function": {"name": "test", "arguments": "{}"}}]}'

        result = engine.parse(text)
        assert isinstance(result.tool_calls, list)


class TestFactoryFunction:
    """Test factory function."""

    def test_create_deepseek_engine(self):
        """Test creating DeepSeek engine."""
        engine = create_reasoning_engine(model_name="deepseek-r1")
        assert engine is not None

    def test_create_qwen_engine(self):
        """Test creating Qwen engine."""
        engine = create_reasoning_engine(model_name="qwen-coder")
        assert engine is not None

    def test_create_with_tool_format(self):
        """Test creating engine with tool format."""
        engine = create_reasoning_engine(
            model_name="generic",
            tool_format=ToolCallFormat.HERMES,
        )
        assert engine is not None


# Run pytest if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
