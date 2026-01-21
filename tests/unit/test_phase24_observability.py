"""
Phase 24: Advanced Observability & Parsing Tests

Tests for:
- StructuredCounter: Metric counters with expect() testing
- FlatLogprobs: Memory-efficient logprob storage
- ToolParser: Extensible tool call parsing
- EnhancedLogger: Deduplicated logging with scope control
- UsageMessage: Structured telemetry
- TypedPrompts: Type-safe prompt schemas
"""

import json
import logging
from dataclasses import dataclass

import pytest


# ============================================================================
# StructuredCounter Tests
# ============================================================================

class TestStructuredCounter:
    """Tests for StructuredCounter base class."""

    def test_counter_creation(self):
        """Test creating a structured counter."""
        from src.observability.stats.structured_counter import RequestCounter

        counter = RequestCounter()
        assert counter.requests_received == 0
        assert counter.requests_completed == 0
        assert counter.requests_failed == 0

    def test_counter_increment(self):
        """Test incrementing counter fields."""
        from src.observability.stats.structured_counter import RequestCounter

        counter = RequestCounter()
        counter.requests_received += 1
        counter.requests_received += 1
        counter.requests_completed += 1

        assert counter.requests_received == 2
        assert counter.requests_completed == 1

    def test_counter_clone(self):
        """Test cloning a counter."""
        from src.observability.stats.structured_counter import CacheCounter

        counter = CacheCounter()
        counter.cache_hits = 10
        counter.cache_misses = 5

        clone = counter.clone()
        assert clone.cache_hits == 10
        assert clone.cache_misses == 5

        # Modify original, clone should be unchanged
        counter.cache_hits = 20
        assert clone.cache_hits == 10

    def test_counter_diff(self):
        """Test computing diff between counters."""
        from src.observability.stats.structured_counter import CacheCounter

        before = CacheCounter()
        before.cache_hits = 10
        before.cache_misses = 5

        after = CacheCounter()
        after.cache_hits = 15
        after.cache_misses = 8

        diff = after.diff(before)
        assert diff["cache_hits"] == 5
        assert diff["cache_misses"] == 3

    def test_counter_expect(self):
        """Test expect() context manager."""
        from src.observability.stats.structured_counter import RequestCounter

        counter = RequestCounter()

        with counter.expect(requests_received=2, requests_completed=1):
            counter.requests_received += 2
            counter.requests_completed += 1

    def test_counter_expect_failure(self):
        """Test expect() raises on mismatch."""
        from src.observability.stats.structured_counter import RequestCounter

        counter = RequestCounter()

        with pytest.raises(AssertionError) as excinfo:
            with counter.expect(requests_received=5):
                counter.requests_received += 3

        assert "not as expected" in str(excinfo.value)

    def test_counter_as_dict(self):
        """Test converting counter to dict."""
        from src.observability.stats.structured_counter import CacheCounter

        counter = CacheCounter()
        counter.cache_hits = 100
        counter.cache_misses = 10

        d = counter.as_dict()
        assert d["cache_hits"] == 100
        assert d["cache_misses"] == 10

    def test_cache_counter_hit_ratio(self):
        """Test cache hit ratio computation."""
        from src.observability.stats.structured_counter import CacheCounter

        counter = CacheCounter()
        counter.cache_hits = 80
        counter.cache_misses = 20

        assert counter.hit_ratio == 0.8

    def test_pool_counter_active_objects(self):
        """Test pool active objects computation."""
        from src.observability.stats.structured_counter import PoolCounter

        counter = PoolCounter()
        counter.objects_acquired = 10
        counter.objects_released = 7

        assert counter.active_objects == 3


# ============================================================================
# FlatLogprobs Tests
# ============================================================================

class TestFlatLogprobs:
    """Tests for FlatLogprobs memory-efficient storage."""

    def test_append_logprobs(self):
        """Test appending logprobs for a position."""
        from src.core.base.logic.structures.flat_logprobs import FlatLogprobs, Logprob

        logprobs = FlatLogprobs()
        logprobs.append({
            100: Logprob(logprob=-0.5, rank=1, decoded_token="hello"),
            200: Logprob(logprob=-1.2, rank=2, decoded_token="world"),
        })

        assert len(logprobs) == 1
        assert logprobs.total_entries == 2

    def test_getitem_single(self):
        """Test accessing single position."""
        from src.core.base.logic.structures.flat_logprobs import FlatLogprobs, Logprob

        logprobs = FlatLogprobs()
        logprobs.append({
            100: Logprob(logprob=-0.5, rank=1, decoded_token="hello"),
        })

        pos0 = logprobs[0]
        assert 100 in pos0
        assert pos0[100].logprob == -0.5
        assert pos0[100].decoded_token == "hello"

    def test_getitem_slice(self):
        """Test slicing FlatLogprobs."""
        from src.core.base.logic.structures.flat_logprobs import FlatLogprobs, Logprob

        logprobs = FlatLogprobs()
        for i in range(5):
            logprobs.append({
                i: Logprob(logprob=-float(i), rank=1),
            })

        sliced = logprobs[1:4]
        assert len(sliced) == 3
        assert sliced[0][1].logprob == -1.0

    def test_append_fast(self):
        """Test fast append without dict creation."""
        from src.core.base.logic.structures.flat_logprobs import FlatLogprobs

        logprobs = FlatLogprobs()
        logprobs.append_fast(
            token_ids=[100, 200, 300],
            logprobs=[-0.5, -1.0, -1.5],
            ranks=[1, 2, 3],
            decoded_tokens=["a", "b", "c"],
        )

        assert len(logprobs) == 1
        assert logprobs.total_entries == 3

    def test_iteration(self):
        """Test iterating over positions."""
        from src.core.base.logic.structures.flat_logprobs import FlatLogprobs, Logprob

        logprobs = FlatLogprobs()
        for i in range(3):
            logprobs.append({i: Logprob(logprob=-float(i), rank=1)})

        positions = list(logprobs)
        assert len(positions) == 3
        assert 0 in positions[0]
        assert 1 in positions[1]
        assert 2 in positions[2]

    def test_immutability(self):
        """Test that setitem/delitem raise errors."""
        from src.core.base.logic.structures.flat_logprobs import FlatLogprobs, Logprob

        logprobs = FlatLogprobs()
        logprobs.append({100: Logprob(logprob=-0.5, rank=1)})

        with pytest.raises(TypeError):
            logprobs[0] = {}

        with pytest.raises(TypeError):
            del logprobs[0]

    def test_negative_index(self):
        """Test negative indexing."""
        from src.core.base.logic.structures.flat_logprobs import FlatLogprobs, Logprob

        logprobs = FlatLogprobs()
        for i in range(5):
            logprobs.append({i: Logprob(logprob=-float(i), rank=1)})

        last = logprobs[-1]
        assert 4 in last

    def test_create_prompt_logprobs(self):
        """Test creating prompt logprobs container."""
        from src.core.base.logic.structures.flat_logprobs import create_prompt_logprobs

        logprobs = create_prompt_logprobs(flat_logprobs=True)
        # First position should be None (for first token)
        assert len(logprobs) == 1


# ============================================================================
# ToolParser Tests
# ============================================================================

class TestToolParser:
    """Tests for ToolParser framework."""

    def test_json_tool_parser_single(self):
        """Test parsing single JSON tool call."""
        from src.core.base.logic.parsers.tool_parser import JSONToolParser

        parser = JSONToolParser()
        output = '[{"name": "get_weather", "arguments": {"city": "London"}}]'

        result = parser.extract_tool_calls(output)
        assert result.has_tool_calls
        assert len(result.tool_calls) == 1
        assert result.tool_calls[0].name == "get_weather"
        assert result.tool_calls[0].arguments["city"] == "London"

    def test_json_tool_parser_multiple(self):
        """Test parsing multiple JSON tool calls."""
        from src.core.base.logic.parsers.tool_parser import JSONToolParser

        parser = JSONToolParser()
        output = '''[
            {"name": "search", "arguments": {"query": "AI"}},
            {"name": "read", "arguments": {"file": "doc.txt"}}
        ]'''

        result = parser.extract_tool_calls(output)
        assert len(result.tool_calls) == 2
        assert result.tool_calls[0].name == "search"
        assert result.tool_calls[1].name == "read"

    def test_json_tool_parser_with_content(self):
        """Test parsing tool calls with surrounding content."""
        from src.core.base.logic.parsers.tool_parser import JSONToolParser

        parser = JSONToolParser()
        output = 'I will help you. [{"name": "help", "arguments": {}}]'

        result = parser.extract_tool_calls(output)
        assert result.has_tool_calls
        assert result.content == "I will help you."

    def test_xml_tool_parser(self):
        """Test parsing XML tool calls."""
        from src.core.base.logic.parsers.tool_parser import XMLToolParser

        parser = XMLToolParser()
        output = '''<tool_call>
            <name>search</name>
            <arguments>{"query": "test"}</arguments>
        </tool_call>'''

        result = parser.extract_tool_calls(output)
        assert result.has_tool_calls
        assert result.tool_calls[0].name == "search"

    def test_tool_parser_manager_get(self):
        """Test getting parser from registry."""
        from src.core.base.logic.parsers.tool_parser import ToolParserManager, JSONToolParser

        parser_cls = ToolParserManager.get("json")
        assert parser_cls == JSONToolParser

    def test_tool_parser_manager_create(self):
        """Test creating parser instance from registry."""
        from src.core.base.logic.parsers.tool_parser import ToolParserManager

        parser = ToolParserManager.create("json")
        assert parser is not None

    def test_tool_parser_decorator(self):
        """Test @tool_parser decorator."""
        from src.core.base.logic.parsers.tool_parser import tool_parser, ToolParser, ToolParserManager, ExtractedToolCalls

        @tool_parser("custom_test")
        class CustomParser(ToolParser):
            def extract_tool_calls(self, model_output, tools=None):
                return ExtractedToolCalls()

            def extract_tool_calls_streaming(self, *args, **kwargs):
                return None

        assert "custom_test" in ToolParserManager.list_parsers()

    def test_extract_tool_calls_convenience(self):
        """Test convenience function."""
        from src.core.base.logic.parsers.tool_parser import extract_tool_calls

        output = '[{"name": "test", "arguments": {}}]'
        result = extract_tool_calls(output, parser_name="json")

        assert result.has_tool_calls
        assert result.tool_calls[0].name == "test"


# ============================================================================
# EnhancedLogger Tests
# ============================================================================

class TestEnhancedLogger:
    """Tests for EnhancedLogger with deduplication."""

    def test_init_logger(self):
        """Test initializing enhanced logger."""
        from src.observability.logging.enhanced_logger import init_logger

        logger = init_logger("test")
        assert hasattr(logger, "debug_once")
        assert hasattr(logger, "info_once")
        assert hasattr(logger, "warning_once")

    def test_enhanced_logger_adapter(self):
        """Test EnhancedLoggerAdapter."""
        from src.observability.logging.enhanced_logger import EnhancedLoggerAdapter

        base_logger = logging.getLogger("test_adapter")
        adapter = EnhancedLoggerAdapter(base_logger)

        # Log same message twice
        adapter.info_once("Test message")
        adapter.info_once("Test message")

        # Should only count once
        assert adapter.get_logged_count() == 1

    def test_enhanced_logger_different_messages(self):
        """Test that different messages are logged."""
        from src.observability.logging.enhanced_logger import EnhancedLoggerAdapter

        base_logger = logging.getLogger("test_diff")
        adapter = EnhancedLoggerAdapter(base_logger)

        adapter.info_once("Message 1")
        adapter.info_once("Message 2")
        adapter.info_once("Message 3")

        assert adapter.get_logged_count() == 3

    def test_reset_once_cache(self):
        """Test resetting the deduplication cache."""
        from src.observability.logging.enhanced_logger import EnhancedLoggerAdapter

        base_logger = logging.getLogger("test_reset")
        adapter = EnhancedLoggerAdapter(base_logger)

        adapter.info_once("Test")
        assert adapter.get_logged_count() == 1

        adapter.reset_once_cache()
        assert adapter.get_logged_count() == 0

    def test_global_dedup_cache_info(self):
        """Test getting cache statistics."""
        from src.observability.logging.enhanced_logger import get_dedup_cache_info

        info = get_dedup_cache_info()
        assert "debug" in info
        assert "info" in info
        assert "warning" in info
        assert "error" in info


# ============================================================================
# UsageMessage Tests
# ============================================================================

class TestUsageMessage:
    """Tests for UsageMessage telemetry."""

    def test_usage_message_creation(self):
        """Test creating a usage message."""
        from src.observability.telemetry.usage_message import UsageMessage

        msg = UsageMessage()
        assert msg.uuid is not None
        assert msg.source == "pyagent"

    def test_detect_cloud_provider_unknown(self):
        """Test cloud provider detection returns UNKNOWN when not on cloud."""
        from src.observability.telemetry.usage_message import detect_cloud_provider

        provider = detect_cloud_provider()
        # Will be UNKNOWN unless running on actual cloud
        assert isinstance(provider, str)

    def test_get_cpu_info(self):
        """Test getting CPU information."""
        from src.observability.telemetry.usage_message import get_cpu_info

        info = get_cpu_info()
        assert "count" in info
        assert "arch" in info

    def test_get_memory_info(self):
        """Test getting memory information."""
        from src.observability.telemetry.usage_message import get_memory_info

        info = get_memory_info()
        # May be empty if psutil not installed
        if info:
            assert "total" in info

    def test_usage_stats_enabled_default(self):
        """Test usage stats enabled check."""
        from src.observability.telemetry.usage_message import is_usage_stats_enabled

        # Should return a boolean
        result = is_usage_stats_enabled()
        assert isinstance(result, bool)

    def test_set_runtime_usage_data(self):
        """Test setting runtime usage data."""
        from src.observability.telemetry.usage_message import (
            set_runtime_usage_data,
            get_runtime_usage_data,
            clear_runtime_usage_data,
        )

        set_runtime_usage_data("test_key", "test_value")
        data = get_runtime_usage_data()
        assert data["test_key"] == "test_value"

        clear_runtime_usage_data()
        data = get_runtime_usage_data()
        assert "test_key" not in data

    def test_usage_message_to_dict(self):
        """Test converting usage message to dict."""
        from src.observability.telemetry.usage_message import UsageMessage

        msg = UsageMessage()
        msg.provider = "AWS"
        msg.num_cpu = 4

        d = msg.to_dict()
        assert d["provider"] == "AWS"
        assert d["num_cpu"] == 4
        assert "uuid" in d

    def test_get_platform_summary(self):
        """Test getting platform summary."""
        from src.observability.telemetry.usage_message import get_platform_summary

        summary = get_platform_summary()
        assert "architecture" in summary
        assert "platform" in summary


# ============================================================================
# TypedPrompts Tests
# ============================================================================

class TestTypedPrompts:
    """Tests for TypedPrompts type-safe schemas."""

    def test_is_string_prompt(self):
        """Test string prompt type guard."""
        from src.core.base.common.types.typed_prompts import is_string_prompt

        assert is_string_prompt("Hello world")
        assert not is_string_prompt({"prompt": "Hello"})

    def test_is_text_prompt(self):
        """Test TextPrompt type guard."""
        from src.core.base.common.types.typed_prompts import is_text_prompt

        assert is_text_prompt({"prompt": "Hello world"})
        assert not is_text_prompt("Hello")
        assert not is_text_prompt({"prompt_token_ids": [1, 2, 3]})

    def test_is_tokens_prompt(self):
        """Test TokensPrompt type guard."""
        from src.core.base.common.types.typed_prompts import is_tokens_prompt

        assert is_tokens_prompt({"prompt_token_ids": [1, 2, 3]})
        assert not is_tokens_prompt({"prompt": "Hello"})

    def test_is_embeds_prompt(self):
        """Test EmbedsPrompt type guard."""
        from src.core.base.common.types.typed_prompts import is_embeds_prompt

        assert is_embeds_prompt({"prompt_embeds": [0.1, 0.2, 0.3]})
        assert not is_embeds_prompt({"prompt": "Hello"})

    def test_is_explicit_encoder_decoder(self):
        """Test encoder/decoder prompt type guard."""
        from src.core.base.common.types.typed_prompts import is_explicit_encoder_decoder_prompt

        prompt = {
            "encoder_prompt": "Translate this",
            "decoder_prompt": None,
        }
        assert is_explicit_encoder_decoder_prompt(prompt)

    def test_parse_prompt_string(self):
        """Test parsing string prompt."""
        from src.core.base.common.types.typed_prompts import parse_prompt

        result = parse_prompt("Hello world")
        assert result["type"] == "text"
        assert result["prompt"] == "Hello world"

    def test_parse_prompt_text(self):
        """Test parsing TextPrompt."""
        from src.core.base.common.types.typed_prompts import parse_prompt

        result = parse_prompt({"prompt": "Hello"})
        assert result["type"] == "text"
        assert result["prompt"] == "Hello"

    def test_parse_prompt_tokens(self):
        """Test parsing TokensPrompt."""
        from src.core.base.common.types.typed_prompts import parse_prompt

        result = parse_prompt({"prompt_token_ids": [1, 2, 3]})
        assert result["type"] == "tokens"
        assert result["prompt_token_ids"] == [1, 2, 3]

    def test_get_prompt_text(self):
        """Test extracting text from prompts."""
        from src.core.base.common.types.typed_prompts import get_prompt_text

        assert get_prompt_text("Hello") == "Hello"
        assert get_prompt_text({"prompt": "World"}) == "World"
        assert get_prompt_text({"prompt_embeds": []}) is None

    def test_has_multi_modal_data(self):
        """Test checking for multi-modal data."""
        from src.core.base.common.types.typed_prompts import has_multi_modal_data

        assert has_multi_modal_data({"prompt": "Hi", "multi_modal_data": {"images": []}})
        assert not has_multi_modal_data({"prompt": "Hi"})
        assert not has_multi_modal_data("Hello")

    def test_make_text_prompt(self):
        """Test creating TextPrompt."""
        from src.core.base.common.types.typed_prompts import make_text_prompt

        prompt = make_text_prompt("Hello", cache_salt="abc")
        assert prompt["prompt"] == "Hello"
        assert prompt["cache_salt"] == "abc"

    def test_make_tokens_prompt(self):
        """Test creating TokensPrompt."""
        from src.core.base.common.types.typed_prompts import make_tokens_prompt

        prompt = make_tokens_prompt([1, 2, 3], prompt_text="Hi")
        assert prompt["prompt_token_ids"] == [1, 2, 3]
        assert prompt["prompt"] == "Hi"

    def test_validate_prompt_valid(self):
        """Test validating valid prompts."""
        from src.core.base.common.types.typed_prompts import validate_prompt

        errors = validate_prompt("Hello")
        assert len(errors) == 0

        errors = validate_prompt({"prompt": "Hi"})
        assert len(errors) == 0

        errors = validate_prompt({"prompt_token_ids": [1, 2, 3]})
        assert len(errors) == 0

    def test_validate_prompt_empty(self):
        """Test validating empty prompts."""
        from src.core.base.common.types.typed_prompts import validate_prompt

        errors = validate_prompt("")
        assert len(errors) == 1
        assert "Empty" in errors[0]

        errors = validate_prompt({"prompt_token_ids": []})
        assert len(errors) == 1


# ============================================================================
# Integration Tests
# ============================================================================

class TestPhase24Integration:
    """Integration tests for Phase 24 components."""

    def test_counter_with_tool_parsing(self):
        """Test using counters while parsing tool calls."""
        from src.observability.stats.structured_counter import RequestCounter
        from src.core.base.logic.parsers.tool_parser import extract_tool_calls

        counter = RequestCounter()

        with counter.expect(requests_received=1, requests_completed=1):
            counter.requests_received += 1
            result = extract_tool_calls('[{"name": "test", "arguments": {}}]')
            if result.has_tool_calls:
                counter.requests_completed += 1

    def test_logger_with_telemetry(self):
        """Test enhanced logger with usage telemetry."""
        from src.observability.logging.enhanced_logger import EnhancedLoggerAdapter
        from src.observability.telemetry.usage_message import UsageContext

        logger = EnhancedLoggerAdapter(logging.getLogger("integration"))

        # Log startup once
        logger.info_once("Starting phase 24 integration test")

        # Should not log again
        logger.info_once("Starting phase 24 integration test")

        assert logger.get_logged_count() == 1

    def test_flat_logprobs_with_typed_prompts(self):
        """Test FlatLogprobs with TypedPrompts."""
        from src.core.base.logic.structures.flat_logprobs import FlatLogprobs, Logprob
        from src.core.base.common.types.typed_prompts import make_tokens_prompt

        # Create prompt
        prompt = make_tokens_prompt([100, 200, 300])

        # Track logprobs for each token
        logprobs = FlatLogprobs()
        for i, token_id in enumerate(prompt["prompt_token_ids"]):
            logprobs.append({
                token_id: Logprob(logprob=-float(i) * 0.5, rank=1)
            })

        assert len(logprobs) == 3
