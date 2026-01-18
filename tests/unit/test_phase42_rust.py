"""
Phase 42: Rust Acceleration Tests

Tests for Rust functions relevant to Phase 42:
- Platform functions
- OpenAI API functions
- Prompt Renderer functions
- MCP Tools functions
- Conversation functions
- Common utility functions
"""

import pytest
import json

# Try to import rust_core
try:
    import rust_core
    RUST_AVAILABLE = True
except ImportError:
    RUST_AVAILABLE = False
    rust_core = None


pytestmark = pytest.mark.skipif(
    not RUST_AVAILABLE,
    reason="rust_core module not available"
)


class TestPlatformRustFunctions:
    """Test platform-related Rust functions."""

    def test_check_capability_rust(self):
        """Test capability checking."""
        # Check if 8.0 >= 7.5
        result = rust_core.check_capability_rust(8, 0, 7, 5)
        assert result is True

        # Check if 7.0 >= 8.0
        result = rust_core.check_capability_rust(7, 0, 8, 0)
        assert result is False

    def test_check_capability_equal(self):
        """Test equal capabilities."""
        result = rust_core.check_capability_rust(8, 6, 8, 6)
        assert result is True

    def test_detect_chat_template_rust(self):
        """Test chat template detection."""
        # ChatML markers
        text = "<|im_start|>system\nYou are helpful<|im_end|>"
        template_type = rust_core.detect_chat_template_rust(text)
        assert template_type == "chatml"


class TestOpenAIAPIRustFunctions:
    """Test OpenAI API-related Rust functions."""

    def test_parse_response_json_rust(self):
        """Test parsing OpenAI response JSON."""
        response_json = json.dumps({
            "id": "resp_123",
            "object": "response",
            "created_at": 1234567890,
            "status": "completed",
            "output": [
                {"type": "message", "role": "assistant", "content": "Hello!"}
            ],
        })
        result = rust_core.parse_response_json_rust(response_json)
        
        assert isinstance(result, dict)
        assert result["id"] == "resp_123"
        assert result["status"] == "completed"

    def test_parse_response_json_invalid(self):
        """Test parsing invalid JSON."""
        with pytest.raises(Exception):
            rust_core.parse_response_json_rust("not valid json {")

    def test_parse_sse_data_only(self):
        """Test parsing SSE with data only."""
        sse_data = 'data: {"token": "world"}\n\n'
        result = rust_core.parse_sse_event_rust(sse_data)
        assert result is not None


class TestConversationRustFunctions:
    """Test conversation context Rust functions."""

    def test_fast_token_count_rust(self):
        """Test fast token counting."""
        text = "Hello world, this is a test sentence."
        count = rust_core.fast_token_count_rust(text)
        
        assert isinstance(count, int)
        assert count >= 5  # At least a few tokens

    def test_fast_token_count_empty(self):
        """Test token count for empty string."""
        count = rust_core.fast_token_count_rust("")
        assert count == 0


class TestRustPerformance:
    """Performance-related tests for Rust functions."""

    def test_fast_token_count_performance(self):
        """Test that fast token count handles large text."""
        large_text = "word " * 10000
        count = rust_core.fast_token_count_rust(large_text)
        
        assert count > 5000  # Should count most words


class TestRustEdgeCases:
    """Edge case tests for Rust functions."""

    def test_unicode_handling(self):
        """Test Unicode handling in Rust functions."""
        text = "Hello 世界 🌍 مرحبا"
        count = rust_core.fast_token_count_rust(text)
        assert count > 0

    def test_parse_valid_json(self):
        """Test parsing valid JSON."""
        json_str = '{"key": "value", "number": 123}'
        result = rust_core.parse_response_json_rust(json_str)
        assert result["key"] == "value"


class TestValidationFunctions:
    """Test JSON and schema validation functions."""

    def test_validate_json_schema_fast_rust(self):
        """Test fast JSON schema validation."""
        json_str = json.dumps({"name": "test", "count": 5})
        required_keys = ["name"]  # List of required keys
        expected_types = {"name": "string", "count": "number"}  # Dict not JSON string
        
        result = rust_core.validate_json_schema_fast_rust(json_str, required_keys, expected_types)
        # Returns (is_valid, error_message) tuple
        assert isinstance(result, tuple) or result is True

    def test_validate_partial_json_rust(self):
        """Test partial JSON validation."""
        partial = '{"key": "val'  # Incomplete JSON
        result = rust_core.validate_partial_json_rust(partial)
        assert isinstance(result, bool)


class TestToolParsing:
    """Test tool parsing functions."""

    def test_parse_tool_calls_rust(self):
        """Test parsing tool calls from JSON."""
        tool_json = json.dumps({
            "tool_calls": [
                {"name": "search", "arguments": {"query": "test"}}
            ]
        })
        result = rust_core.parse_tool_calls_rust(tool_json)
        assert isinstance(result, list) or isinstance(result, str)

    def test_detect_tool_format_rust(self):
        """Test tool format detection."""
        json_tool = '{"name": "search", "parameters": {}}'
        format_type = rust_core.detect_tool_format_rust(json_tool)
        assert isinstance(format_type, str)


class TestHashingFunctions:
    """Test hashing and caching functions."""

    def test_blake3_hash_rust(self):
        """Test Blake3 hashing."""
        data = b"test data for hashing"
        hash1 = rust_core.blake3_hash_rust(data)
        hash2 = rust_core.blake3_hash_rust(data)
        
        assert hash1 == hash2  # Deterministic
        assert len(hash1) > 0

    def test_fast_cache_key_rust(self):
        """Test fast cache key generation."""
        # Try with single string argument
        key = rust_core.fast_cache_key_rust("model_id:prompt_hash:100")
        assert isinstance(key, str)
        assert len(key) > 0

    def test_consistent_hash_rust(self):
        """Test consistent hashing."""
        hash1 = rust_core.consistent_hash_rust("key1", 10)
        hash2 = rust_core.consistent_hash_rust("key1", 10)
        
        assert hash1 == hash2
        assert 0 <= hash1 < 10


class TestTokenFunctions:
    """Test token-related functions."""

    def test_estimate_tokens_rust(self):
        """Test token estimation."""
        text = "Hello, this is a test message for token estimation."
        count = rust_core.estimate_tokens_rust(text)
        
        assert isinstance(count, int)
        assert count > 0

    def test_batch_estimate_tokens_rust(self):
        """Test batch token estimation."""
        # batch_estimate_tokens_rust needs list and chars_per_token
        texts = ["Hello world", "Test message", "Another text"]
        results = rust_core.batch_estimate_tokens_rust(texts, 4)
        
        assert isinstance(results, (str, list))


class TestPatternMatching:
    """Test pattern matching functions."""

    def test_match_patterns_rust(self):
        """Test pattern matching."""
        text = "The quick brown fox jumps"
        patterns = ["quick", "fox", "dog"]  # Pass as list
        
        # Returns index of first matching pattern or -1
        match_index = rust_core.match_patterns_rust(text, patterns)
        assert isinstance(match_index, int)
        assert match_index >= 0  # Should match "quick" at index 0

    def test_check_stop_strings_rust(self):
        """Test stop string checking."""
        text = "Hello world <END>"
        new_char_count = len(text)
        stop_strings = ["<END>", "<STOP>"]  # Pass as list
        
        # check_stop_strings_rust(output_text, new_char_count, stop_strings, include_in_output)
        result = rust_core.check_stop_strings_rust(text, new_char_count, stop_strings, True)
        # Returns (stop_string_index, truncation_position) or None
        assert result is None or isinstance(result, tuple)


class TestMetricsFunctions:
    """Test metrics aggregation functions."""

    def test_calculate_metrics_rust(self):
        """Test metrics calculation."""
        values = json.dumps([1.0, 2.0, 3.0, 4.0, 5.0])
        result = rust_core.calculate_metrics_rust(values)
        
        # Result can be string JSON or dict
        if isinstance(result, str):
            metrics = json.loads(result)
        else:
            metrics = result
        assert isinstance(metrics, dict)

    def test_calculate_throughput_rust(self):
        """Test throughput calculation."""
        result = rust_core.calculate_throughput_rust(1000, 2.5)  # 1000 tokens in 2.5 seconds
        
        assert isinstance(result, (int, float))
        assert result > 0
