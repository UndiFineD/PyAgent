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

"""Property-based tests for BaseAgentCore.

Tests pure logic methods before Rust conversion.
"""

from hypothesis import given, strategies as st
from src.core.base.lifecycle.base_agent_core import BaseAgentCore
from src.core.base.common.models import AgentConfig, AgentPriority


class TestBaseAgentCoreValidation:
    """Test validation methods."""

    def test_validate_config_valid(self) -> None:
        """Test config validation with valid configuration."""
        core = BaseAgentCore()
        config = AgentConfig(
            backend="openai",
            model="gpt-4",
            max_tokens=1000,
            temperature=0.7,
            retry_count=3,
            timeout=30,
        )
        is_valid, error = core.validate_config(config)
        assert is_valid
        assert error == ""

    def test_validate_config_invalid_backend(self) -> None:
        """Test config validation with missing backend."""
        core = BaseAgentCore()
        config = AgentConfig(
            backend="",
            model="gpt-4",
            max_tokens=1000,
        )
        is_valid, error = core.validate_config(config)
        assert not is_valid
        assert "Backend" in error

    def test_validate_config_invalid_max_tokens(self) -> None:
        """Test config validation with invalid max_tokens."""
        core = BaseAgentCore()
        config = AgentConfig(
            backend="openai",
            model="gpt-4",
            max_tokens=0,
        )
        is_valid, error = core.validate_config(config)
        assert not is_valid
        assert "max_tokens" in error

    def test_validate_config_invalid_temperature(self) -> None:
        """Test config validation with invalid temperature."""
        core = BaseAgentCore()
        config = AgentConfig(
            backend="openai",
            model="gpt-4",
            temperature=3.0,
        )
        is_valid, error = core.validate_config(config)
        assert not is_valid
        assert "temperature" in error

    def test_is_response_valid_empty(self) -> None:
        """Test response validation with empty response."""
        core = BaseAgentCore()
        is_valid, reason = core.is_response_valid("")
        assert not is_valid
        assert "empty" in reason.lower()

    def test_is_response_valid_too_short(self) -> None:
        """Test response validation with short response."""
        core = BaseAgentCore()
        is_valid, reason = core.is_response_valid("short", min_length=10)
        assert not is_valid
        assert "short" in reason.lower()

    def test_is_response_valid_valid(self) -> None:
        """Test response validation with valid response."""
        core = BaseAgentCore()
        is_valid, reason = core.is_response_valid("This is a valid response")
        assert is_valid
        assert reason == ""


class TestBaseAgentCoreCalculations:
    """Test calculation methods."""

    def test_calculate_priority_score_critical(self) -> None:
        """Test priority score for CRITICAL priority."""
        core = BaseAgentCore()
        score = core.calculate_priority_score(AgentPriority.CRITICAL, 0.5)
        assert 0.8 <= score <= 1.0

    def test_calculate_priority_score_low(self) -> None:
        """Test priority score for LOW priority."""
        core = BaseAgentCore()
        score = core.calculate_priority_score(AgentPriority.LOW, 0.5)
        assert 0.0 <= score <= 0.5

    def test_calculate_token_estimate(self) -> None:
        """Test token estimation."""
        core = BaseAgentCore()
        text = "This is a test" * 100
        tokens = core.calculate_token_estimate(text)
        assert tokens > 0
        assert tokens < len(text)

    def test_assess_response_quality_basic(self) -> None:
        """Test response quality assessment."""
        core = BaseAgentCore()
        response = "This is a good response with sufficient length"
        quality = core.assess_response_quality(response)
        # Returns ResponseQuality enum
        assert quality in [member for member in type(quality)]

    def test_assess_response_quality_with_metadata(self) -> None:
        """Test response quality with metadata."""
        core = BaseAgentCore()
        response = "Response with references"
        metadata = {"has_references": True, "is_complete": True}
        quality = core.assess_response_quality(response, metadata)
        # Returns ResponseQuality enum
        assert quality in [member for member in type(quality)]


class TestBaseAgentCoreDataOperations:
    """Test data manipulation methods."""

    def test_filter_events_no_filter(self) -> None:
        """Test event filtering without filter."""
        core = BaseAgentCore()
        events = [{"type": "error"}, {"type": "info"}]
        filtered = core.filter_events(events)
        assert len(filtered) == 2

    def test_filter_events_with_filter(self) -> None:
        """Test event filtering with type filter."""
        core = BaseAgentCore()
        events = [{"type": "error"}, {"type": "info"}, {"type": "error"}]
        filtered = core.filter_events(events, "error")
        assert len(filtered) == 2
        assert all(e["type"] == "error" for e in filtered)

    def test_deduplicate_entries(self) -> None:
        """Test entry deduplication."""
        core = BaseAgentCore()
        entries = ["a", "b", "a", "c", "b"]
        deduped = core.deduplicate_entries(entries)
        assert deduped == ["a", "b", "c"]

    def test_normalize_response(self) -> None:
        """Test response normalization."""
        core = BaseAgentCore()
        response = "  Multiple   spaces\r\nand   line\nendings  "
        normalized = core.normalize_response(response)
        assert "  " not in normalized
        assert "\r\n" not in normalized


class TestBaseAgentCorePropertyBased:
    """Property-based tests using Hypothesis."""

    @given(
        max_tokens=st.integers(min_value=1, max_value=100000),
        temperature=st.floats(min_value=0.0, max_value=2.0),
        retry_count=st.integers(min_value=0, max_value=10),
        timeout=st.integers(min_value=1, max_value=300),
    )
    def test_validate_config_property(
        self, max_tokens: int, temperature: float, retry_count: int, timeout: int
    ) -> None:
        """Property: Valid configs pass validation."""
        core = BaseAgentCore()
        config = AgentConfig(
            backend="openai",
            model="gpt-4",
            max_tokens=max_tokens,
            temperature=temperature,
            retry_count=retry_count,
            timeout=timeout,
        )
        is_valid, _ = core.validate_config(config)
        assert is_valid

    @given(urgency=st.floats(min_value=0.0, max_value=1.0))
    def test_priority_score_range(self, urgency: float) -> None:
        """Property: Priority scores are within valid range."""
        core = BaseAgentCore()
        for priority in AgentPriority:
            score = core.calculate_priority_score(priority, urgency)
            assert 0.0 <= score <= 1.0

    @given(text=st.text(min_size=1, max_size=1000))
    def test_token_estimate_positive(self, text: str) -> None:
        """Property: Token estimates are always positive."""
        core = BaseAgentCore()
        tokens = core.calculate_token_estimate(text)
        assert tokens >= 1

    @given(entries=st.lists(st.text(min_size=1, max_size=20), min_size=0, max_size=100))
    def test_deduplicate_preserves_order(self, entries: list[str]) -> None:
        """Property: Deduplication preserves first occurrence order."""
        core = BaseAgentCore()
        deduped = core.deduplicate_entries(entries)

        # All unique
        assert len(deduped) == len(set(deduped))

        # Order preserved
        if entries:
            first_occurrence = {}
            for i, entry in enumerate(entries):
                if entry not in first_occurrence:
                    first_occurrence[entry] = i

            for i in range(len(deduped) - 1):
                assert first_occurrence[deduped[i]] < first_occurrence[deduped[i + 1]]

    @given(response=st.text(min_size=10, max_size=10000))
    def test_normalize_response_idempotent(self, response: str) -> None:
        """Property: Normalizing twice produces same result."""
        core = BaseAgentCore()
        normalized_once = core.normalize_response(response)
        normalized_twice = core.normalize_response(normalized_once)
        assert normalized_once == normalized_twice

    @given(
        events=st.lists(
            st.fixed_dictionaries({"type": st.sampled_from(["error", "info", "warn"])}),
            min_size=0,
            max_size=50,
        )
    )
    def test_filter_events_subset(self, events: list[dict]) -> None:
        """Property: Filtered events are subset of original."""
        core = BaseAgentCore()
        filtered = core.filter_events(events, "error")
        assert len(filtered) <= len(events)
        assert all(e in events for e in filtered)


class TestBaseAgentCoreConfigMerging:
    """Test configuration merging logic."""

    def test_merge_configurations_override_all(self) -> None:
        """Test merging with all overrides."""
        core = BaseAgentCore()
        base = AgentConfig(
            backend="openai",
            model="gpt-3.5-turbo",
            max_tokens=500,
            temperature=0.5,
        )
        override = AgentConfig(
            backend="anthropic",
            model="claude-3",
            max_tokens=1000,
            temperature=0.8,
        )
        merged = core.merge_configurations(base, override)
        assert merged.backend == "anthropic"
        assert merged.model == "claude-3"
        assert merged.max_tokens == 1000
        assert merged.temperature == 0.8

    def test_merge_configurations_partial_override(self) -> None:
        """Test merging with partial overrides."""
        core = BaseAgentCore()
        base = AgentConfig(
            backend="openai",
            model="gpt-4",
            max_tokens=1000,
        )
        override = AgentConfig(
            backend="",
            model="",
            max_tokens=2000,
        )
        merged = core.merge_configurations(base, override)
        assert merged.backend == "openai"  # Base value
        assert merged.model == "gpt-4"  # Base value
        assert merged.max_tokens == 2000  # Override value


class TestBaseAgentCoreStrategyValidation:
    """Test strategy validation."""

    def test_set_strategy_none(self) -> None:
        """Test strategy validation with None."""
        core = BaseAgentCore()
        result = core.set_strategy(None)
        assert "ERROR" in result

    def test_set_strategy_missing_execute(self) -> None:
        """Test strategy validation with missing execute method."""
        core = BaseAgentCore()

        class InvalidStrategy:
            pass

        result = core.set_strategy(InvalidStrategy())
        assert "ERROR" in result
        assert "execute" in result

    def test_set_strategy_valid(self) -> None:
        """Test strategy validation with valid strategy."""
        core = BaseAgentCore()

        class ValidStrategy:
            def execute(self):
                pass

        result = core.set_strategy(ValidStrategy())
        assert "ERROR" not in result
        assert "ValidStrategy" in result


class TestBaseAgentCoreEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_calculate_token_estimate_empty_string(self) -> None:
        """Test token estimation with empty string."""
        core = BaseAgentCore()
        tokens = core.calculate_token_estimate("")
        assert tokens == 1  # Minimum 1 token

    def test_filter_events_empty_list(self) -> None:
        """Test filtering with empty event list."""
        core = BaseAgentCore()
        filtered = core.filter_events([])
        assert filtered == []

    def test_deduplicate_entries_empty(self) -> None:
        """Test deduplication with empty list."""
        core = BaseAgentCore()
        deduped = core.deduplicate_entries([])
        assert deduped == []

    def test_normalize_response_empty(self) -> None:
        """Test normalization with empty string."""
        core = BaseAgentCore()
        normalized = core.normalize_response("")
        assert normalized == ""

    def test_is_response_valid_max_length(self) -> None:
        """Test response validation at max length boundary."""
        core = BaseAgentCore()
        # Just under limit
        is_valid, _ = core.is_response_valid("x" * 999999)
        assert is_valid

        # Over limit
        is_valid, reason = core.is_response_valid("x" * 1000001)
        assert not is_valid
        assert "long" in reason.lower()
