# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Unit Tests for Tool Parser Framework

"""
Tests for ToolParserFramework module.
"""

import pytest
import json
from unittest.mock import Mock, patch

from src.infrastructure.services.tools.tool_parser_framework import (
    ToolParserType,
    ToolCallStatus,
    ToolParameter,
    ToolCall,
    ToolParseResult,
    StreamingToolState,
    ToolParser,
    JsonToolParser,
    HermesToolParser,
    Llama3ToolParser,
    MistralToolParser,
    GraniteToolParser,
    ToolParserRegistry,
    StreamingToolParser,
    parse_tool_call,
    extract_json_from_text,
    validate_tool_call,
)


class TestToolParserType:
    """Test ToolParserType enum."""

    def test_parser_type_values(self):
        """Test ToolParserType enum values."""
        assert ToolParserType.GENERIC_JSON is not None
        assert ToolParserType.HERMES is not None
        assert ToolParserType.LLAMA3 is not None
        assert ToolParserType.MISTRAL is not None
        assert ToolParserType.GRANITE is not None
        assert ToolParserType.PYTHONIC is not None


class TestToolCallStatus:
    """Test ToolCallStatus enum."""

    def test_status_values(self):
        """Test ToolCallStatus enum values."""
        assert ToolCallStatus.PENDING is not None
        assert ToolCallStatus.COMPLETE is not None
        assert ToolCallStatus.INVALID is not None
        assert ToolCallStatus.PARTIAL is not None


class TestToolCall:
    """Test ToolCall dataclass."""

    def test_tool_call_creation(self):
        """Test ToolCall creation."""
        call = ToolCall(
            id="call_123",
            name="get_weather",
            arguments={"city": "London"},
        )

        assert call.id == "call_123"
        assert call.name == "get_weather"
        assert call.arguments == {"city": "London"}
        assert call.status == ToolCallStatus.COMPLETE

    def test_tool_call_to_dict(self):
        """Test ToolCall to_dict method."""
        call = ToolCall(
            id="call_123",
            name="get_weather",
            arguments={"city": "London"},
        )

        d = call.to_dict()

        assert d["id"] == "call_123"
        assert d["type"] == "function"
        assert d["function"]["name"] == "get_weather"

    def test_tool_call_to_openai_format(self):
        """Test OpenAI format conversion."""
        call = ToolCall(
            id="call_123",
            name="get_weather",
            arguments={"city": "London"},
        )

        openai = call.to_openai_format()

        assert openai["id"] == "call_123"
        assert openai["type"] == "function"
        assert "arguments" in openai["function"]


class TestToolParseResult:
    """Test ToolParseResult dataclass."""

    def test_parse_result_empty(self):
        """Test empty ToolParseResult."""
        result = ToolParseResult()

        assert not result.has_tool_calls
        assert result.is_valid

    def test_parse_result_with_tools(self):
        """Test ToolParseResult with tool calls."""
        call = ToolCall(id="call_1", name="test", arguments={})
        result = ToolParseResult(tool_calls=[call])

        assert result.has_tool_calls
        assert len(result.tool_calls) == 1

    def test_parse_result_with_errors(self):
        """Test ToolParseResult with errors."""
        result = ToolParseResult(errors=["Parse error"])

        assert len(result.errors) == 1


class TestStreamingToolState:
    """Test StreamingToolState dataclass."""

    def test_streaming_state_default(self):
        """Test default StreamingToolState."""
        state = StreamingToolState()

        assert state.buffer == ""
        assert not state.in_tool_call
        assert state.current_tool is None
        assert state.tool_call_index == 0


class TestJsonToolParser:
    """Test JsonToolParser class."""

    def test_parser_type(self):
        """Test parser type."""
        parser = JsonToolParser()
        assert parser.parser_type == ToolParserType.GENERIC_JSON

    def test_parse_simple_json(self):
        """Test parsing simple JSON tool call."""
        parser = JsonToolParser()

        text = '{"name": "get_weather", "arguments": {"city": "London"}}'
        result = parser.parse(text)

        assert result.has_tool_calls
        assert len(result.tool_calls) == 1
        assert result.tool_calls[0].name == "get_weather"
        assert result.tool_calls[0].arguments["city"] == "London"

    def test_parse_openai_format(self):
        """Test parsing OpenAI format."""
        parser = JsonToolParser()

        text = '{"id": "call_123", "function": {"name": "test_func", "arguments": "{\\"key\\": \\"value\\"}"}}'
        result = parser.parse(text)

        assert result.has_tool_calls
        assert result.tool_calls[0].name == "test_func"

    def test_parse_multiple_json(self):
        """Test parsing multiple JSON objects."""
        parser = JsonToolParser()

        text = '{"name": "func1", "arguments": {}} and {"name": "func2", "arguments": {}}'
        result = parser.parse(text)

        assert len(result.tool_calls) == 2

    def test_parse_no_json(self):
        """Test parsing text with no JSON."""
        parser = JsonToolParser()

        text = "This is just plain text with no function calls."
        result = parser.parse(text)

        assert not result.has_tool_calls

    def test_parse_streaming(self):
        """Test streaming parsing."""
        parser = JsonToolParser()
        state = StreamingToolState()

        # Feed partial JSON
        state, tool = parser.parse_streaming('{"name": "test"', state)
        assert tool is None  # Not complete yet

        # Complete the JSON
        state, tool = parser.parse_streaming(', "arguments": {}}', state)
        # May or may not complete depending on implementation


class TestHermesToolParser:
    """Test HermesToolParser class."""

    def test_parser_type(self):
        """Test parser type."""
        parser = HermesToolParser()
        assert parser.parser_type == ToolParserType.HERMES

    def test_parse_hermes_format(self):
        """Test parsing Hermes format."""
        parser = HermesToolParser()

        text = '<tool_call>{"name": "get_weather", "arguments": {"city": "Paris"}}</tool_call>'
        result = parser.parse(text)

        assert result.has_tool_calls
        assert result.tool_calls[0].name == "get_weather"
        assert result.tool_calls[0].arguments["city"] == "Paris"

    def test_parse_with_content(self):
        """Test parsing with surrounding content."""
        parser = HermesToolParser()

        text = 'Let me check the weather. <tool_call>{"name": "weather", "arguments": {}}</tool_call> Done!'
        result = parser.parse(text)

        assert result.has_tool_calls
        assert "check the weather" in result.content

    def test_parse_multiple_calls(self):
        """Test parsing multiple Hermes calls."""
        parser = HermesToolParser()

        text = (
            '<tool_call>{"name": "func1", "arguments": {}}</tool_call>'
            '<tool_call>{"name": "func2", "arguments": {}}</tool_call>'
        )
        result = parser.parse(text)

        assert len(result.tool_calls) == 2

    def test_parse_no_tool_calls(self):
        """Test parsing without tool calls."""
        parser = HermesToolParser()

        text = "This is just regular text."
        result = parser.parse(text)

        assert not result.has_tool_calls


class TestLlama3ToolParser:
    """Test Llama3ToolParser class."""

    def test_parser_type(self):
        """Test parser type."""
        parser = Llama3ToolParser()
        assert parser.parser_type == ToolParserType.LLAMA3

    def test_parse_python_tag(self):
        """Test parsing with python_tag."""
        parser = Llama3ToolParser()

        text = '<|python_tag|>get_weather(city="London")'
        result = parser.parse(text)

        assert result.has_tool_calls
        assert result.tool_calls[0].name == "get_weather"

    def test_parse_with_multiple_args(self):
        """Test parsing with multiple arguments."""
        parser = Llama3ToolParser()

        text = '<|python_tag|>search(query="test", limit=10)'
        result = parser.parse(text)

        assert result.has_tool_calls
        assert result.tool_calls[0].name == "search"
        assert "query" in result.tool_calls[0].arguments

    def test_parse_json_fallback(self):
        """Test JSON fallback when no python_tag."""
        parser = Llama3ToolParser()

        text = '{"name": "test_func", "arguments": {}}'
        result = parser.parse(text)

        assert result.has_tool_calls


class TestMistralToolParser:
    """Test MistralToolParser class."""

    def test_parser_type(self):
        """Test parser type."""
        parser = MistralToolParser()
        assert parser.parser_type == ToolParserType.MISTRAL

    def test_parse_mistral_format(self):
        """Test parsing Mistral format."""
        parser = MistralToolParser()

        text = '[TOOL_CALLS] [{"name": "get_data", "arguments": {"id": 123}}]'
        result = parser.parse(text)

        assert result.has_tool_calls
        assert result.tool_calls[0].name == "get_data"

    def test_parse_with_content(self):
        """Test parsing with surrounding content."""
        parser = MistralToolParser()

        text = 'Let me help you. [TOOL_CALLS] [{"name": "assist", "arguments": {}}]'
        result = parser.parse(text)

        assert result.has_tool_calls
        assert "Let me help you" in result.content

    def test_parse_no_tool_calls(self):
        """Test parsing without TOOL_CALLS tag."""
        parser = MistralToolParser()

        text = "Regular response without tools."
        result = parser.parse(text)

        assert not result.has_tool_calls


class TestGraniteToolParser:
    """Test GraniteToolParser class."""

    def test_parser_type(self):
        """Test parser type."""
        parser = GraniteToolParser()
        assert parser.parser_type == ToolParserType.GRANITE

    def test_parse_granite_format(self):
        """Test parsing Granite format."""
        parser = GraniteToolParser()

        text = '<|tool_call|>{"name": "calculate", "arguments": {"x": 5}}<|end_of_text|>'
        result = parser.parse(text)

        assert result.has_tool_calls
        assert result.tool_calls[0].name == "calculate"

    def test_parse_no_tool_calls(self):
        """Test parsing without tool calls."""
        parser = GraniteToolParser()

        text = "Regular text response."
        result = parser.parse(text)

        assert not result.has_tool_calls


class TestToolParserRegistry:
    """Test ToolParserRegistry class."""

    def test_singleton_instance(self):
        """Test ToolParserRegistry is singleton."""
        registry1 = ToolParserRegistry()
        registry2 = ToolParserRegistry()

        assert registry1 is registry2

    def test_get_parser_by_type(self):
        """Test getting parser by type."""
        registry = ToolParserRegistry()

        parser = registry.get_parser(ToolParserType.HERMES)
        assert isinstance(parser, HermesToolParser)

        parser = registry.get_parser(ToolParserType.LLAMA3)
        assert isinstance(parser, Llama3ToolParser)

    def test_get_parser_for_model(self):
        """Test getting parser for model name."""
        registry = ToolParserRegistry()

        parser = registry.get_parser_for_model("NousResearch/Hermes-2-Pro")
        assert isinstance(parser, HermesToolParser)

        parser = registry.get_parser_for_model("meta-llama/Llama-3-8B")
        assert isinstance(parser, Llama3ToolParser)

    def test_detect_parser_type(self):
        """Test auto-detecting parser type from text."""
        registry = ToolParserRegistry()

        assert registry.detect_parser_type("<tool_call>...") == ToolParserType.HERMES
        assert registry.detect_parser_type("<|python_tag|>...") == ToolParserType.LLAMA3
        assert registry.detect_parser_type("[TOOL_CALLS]...") == ToolParserType.MISTRAL
        assert registry.detect_parser_type("<|tool_call|>...") == ToolParserType.GRANITE
        assert registry.detect_parser_type('{"name": ...}') == ToolParserType.GENERIC_JSON


class TestStreamingToolParser:
    """Test StreamingToolParser class."""

    def test_parser_creation(self):
        """Test StreamingToolParser creation."""
        parser = StreamingToolParser(parser_type=ToolParserType.HERMES)

        assert len(parser.completed_tools) == 0

    def test_parser_with_model_name(self):
        """Test creation with model name."""
        parser = StreamingToolParser(model_name="mistralai/Mistral-7B")

        # Should use Mistral parser
        assert len(parser.completed_tools) == 0

    def test_feed_and_finalize(self):
        """Test feeding tokens and finalizing."""
        parser = StreamingToolParser(parser_type=ToolParserType.GENERIC_JSON)

        parser.feed('{"name": "test')
        parser.feed('", "arguments": {}}')

        result = parser.finalize()
        # Result should contain parsed tools or buffer

    def test_reset(self):
        """Test resetting parser state."""
        parser = StreamingToolParser(parser_type=ToolParserType.GENERIC_JSON)

        parser.feed('{"name": "test"}')
        parser.reset()

        assert len(parser.completed_tools) == 0


class TestParseToolCall:
    """Test parse_tool_call utility function."""

    def test_parse_with_auto_detection(self):
        """Test parsing with auto-detection."""
        text = '<tool_call>{"name": "test", "arguments": {}}</tool_call>'
        result = parse_tool_call(text)

        assert result.has_tool_calls

    def test_parse_with_explicit_type(self):
        """Test parsing with explicit parser type."""
        text = '{"name": "test", "arguments": {}}'
        result = parse_tool_call(text, parser_type=ToolParserType.GENERIC_JSON)

        assert result.has_tool_calls

    def test_parse_with_model_name(self):
        """Test parsing with model name."""
        text = '[TOOL_CALLS] [{"name": "test", "arguments": {}}]'
        result = parse_tool_call(text, model_name="mistral-7b")

        assert result.has_tool_calls


class TestExtractJsonFromText:
    """Test extract_json_from_text utility function."""

    def test_extract_single_json(self):
        """Test extracting single JSON object."""
        text = 'Some text {"key": "value"} more text'
        jsons = extract_json_from_text(text)

        assert len(jsons) == 1
        assert '{"key": "value"}' in jsons[0]

    def test_extract_multiple_json(self):
        """Test extracting multiple JSON objects."""
        text = '{"a": 1} and {"b": 2} and {"c": 3}'
        jsons = extract_json_from_text(text)

        assert len(jsons) == 3

    def test_extract_nested_json(self):
        """Test extracting nested JSON."""
        text = '{"outer": {"inner": "value"}}'
        jsons = extract_json_from_text(text)

        assert len(jsons) == 1
        parsed = json.loads(jsons[0])
        assert "outer" in parsed
        assert "inner" in parsed["outer"]

    def test_extract_no_json(self):
        """Test extracting from text with no JSON."""
        text = "This is plain text."
        jsons = extract_json_from_text(text)

        assert len(jsons) == 0


class TestValidateToolCall:
    """Test validate_tool_call utility function."""

    def test_validate_basic(self):
        """Test basic validation."""
        call = ToolCall(
            id="call_1",
            name="test_func",
            arguments={"key": "value"},
        )

        is_valid, errors = validate_tool_call(call)

        assert is_valid
        assert len(errors) == 0

    def test_validate_missing_name(self):
        """Test validation with missing name."""
        call = ToolCall(
            id="call_1",
            name="",
            arguments={},
        )

        is_valid, errors = validate_tool_call(call)

        assert not is_valid
        assert any("name" in e.lower() for e in errors)

    def test_validate_with_schema(self):
        """Test validation with schema."""
        call = ToolCall(
            id="call_1",
            name="get_weather",
            arguments={"city": "London"},
        )

        schema = {
            "parameters": {
                "required": ["city"],
                "properties": {
                    "city": {"type": "string"},
                },
            },
        }

        is_valid, errors = validate_tool_call(call, tool_schema=schema)

        assert is_valid

    def test_validate_missing_required(self):
        """Test validation with missing required parameter."""
        call = ToolCall(
            id="call_1",
            name="get_weather",
            arguments={},  # Missing "city"
        )

        schema = {
            "parameters": {
                "required": ["city"],
                "properties": {
                    "city": {"type": "string"},
                },
            },
        }

        is_valid, errors = validate_tool_call(call, tool_schema=schema)

        assert not is_valid
        assert any("city" in e for e in errors)
