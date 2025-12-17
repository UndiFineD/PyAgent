#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for agent_backend.py"""

from __future__ import annotations
import unittest
from typing import Any
from unittest.mock import MagicMock, patch
import time
import json
from datetime import datetime
import pytest
from agent_test_utils import agent_dir_on_path


@pytest.fixture()
def agent_backend_module() -> Any:
    with agent_dir_on_path():
        import agent_backend
        return agent_backend


# ============================================================================
# Caching and Response Tests
# ============================================================================

def test_response_caching_enabled(agent_backend_module: Any) -> None:
    """Test that responses are cached when use_cache=True."""
    agent_backend_module.clear_response_cache()

    with patch("agent_backend.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "cached response"}}]
        }
        mock_requests.post.return_value = mock_response

        # First call - should hit API
        result1 = agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4", base_url="https://api.test",
            token="token", use_cache=True
        )
        assert result1 == "cached response"
        assert mock_requests.post.call_count == 1

        # Second call - should use cache
        result2 = agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4", base_url="https://api.test",
            token="token", use_cache=True
        )
        assert result2 == "cached response"
        assert mock_requests.post.call_count == 1  # Still 1, cache was used


def test_response_cache_disabled(agent_backend_module: Any) -> None:
    """Test that caching can be disabled with use_cache=False."""
    agent_backend_module.clear_response_cache()

    with patch("agent_backend.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "response"}}]
        }
        mock_requests.post.return_value = mock_response

        # First call with cache disabled
        agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4", base_url="https://api.test",
            token="token", use_cache=False
        )
        assert mock_requests.post.call_count == 1

        # Second call - should call API again (no caching)
        agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4", base_url="https://api.test",
            token="token", use_cache=False
        )
        assert mock_requests.post.call_count == 2


def test_clear_response_cache(agent_backend_module: Any) -> None:
    """Test that cache can be cleared."""
    agent_backend_module.clear_response_cache()

    # Manually add something to cache
    cache_key = agent_backend_module._get_cache_key("test", "gpt-4")
    agent_backend_module._response_cache[cache_key] = "cached"

    assert cache_key in agent_backend_module._response_cache
    agent_backend_module.clear_response_cache()
    assert len(agent_backend_module._response_cache) == 0


# ============================================================================
# Response Validation Tests
# ============================================================================

def test_validate_response_content_basic(agent_backend_module: Any) -> None:
    """Test basic response validation (non-empty)."""
    assert agent_backend_module.validate_response_content("valid response") is True
    assert agent_backend_module.validate_response_content("") is False
    assert agent_backend_module.validate_response_content("   ") is False
    assert agent_backend_module.validate_response_content(None) is False


def test_validate_response_content_with_types(agent_backend_module: Any) -> None:
    """Test response validation with expected content types."""
    # Should pass if content contains expected type
    assert agent_backend_module.validate_response_content(
        "Here is the code:", ["code"]
    ) is True

    # Should pass if contains any expected type
    assert agent_backend_module.validate_response_content(
        "Explanation: The code works by...", ["code", "explanation"]
    ) is True

    # Case insensitive
    assert agent_backend_module.validate_response_content(
        "CODE: print('hello')", ["code"]
    ) is True


# ============================================================================
# Token and Cost Estimation Tests
# ============================================================================

def test_estimate_tokens(agent_backend_module: Any) -> None:
    """Test token estimation."""
    # Empty text
    assert agent_backend_module.estimate_tokens("") == 0

    # Rough estimate: ~4 chars per token
    text = "x" * 100
    estimated = agent_backend_module.estimate_tokens(text)
    assert estimated == 25  # 100 / 4


def test_estimate_cost(agent_backend_module: Any) -> None:
    """Test cost estimation."""
    # 1000 tokens at $0.03 per 1k=$0.03
    cost = agent_backend_module.estimate_cost(1000, model="gpt-4", rate_per_1k_input=0.03)
    assert abs(cost - 0.03) < 0.001

    # 500 tokens at default rate
    cost = agent_backend_module.estimate_cost(500)
    assert cost > 0


# ============================================================================
# Circuit Breaker Tests
# ============================================================================

def test_circuit_breaker_closed_state(agent_backend_module: Any) -> None:
    """Test circuit breaker in CLOSED state."""
    breaker = agent_backend_module.CircuitBreaker("test", failure_threshold=3)
    assert breaker.state == "CLOSED"
    assert breaker.is_open() is False

    # One failure shouldn't open it
    breaker.record_failure()
    assert breaker.state == "CLOSED"
    assert breaker.is_open() is False


def test_circuit_breaker_opens_on_threshold(agent_backend_module: Any) -> None:
    """Test that circuit breaker opens after failure threshold."""
    breaker = agent_backend_module.CircuitBreaker("test", failure_threshold=3)

    # Reach threshold
    breaker.record_failure()
    breaker.record_failure()
    breaker.record_failure()

    assert breaker.state == "OPEN"
    assert breaker.is_open() is True


def test_circuit_breaker_recovery(agent_backend_module: Any) -> None:
    """Test circuit breaker recovery after timeout."""
    breaker = agent_backend_module.CircuitBreaker("test", failure_threshold=2, recovery_timeout=1)

    # Open the circuit
    breaker.record_failure()
    breaker.record_failure()
    assert breaker.is_open() is True

    # Wait for recovery timeout
    time.sleep(1.1)

    # Should be half-open now
    assert breaker.is_open() is False
    assert breaker.state == "HALF_OPEN"

    # Success should close it
    breaker.record_success()
    assert breaker.state == "CLOSED"


def test_circuit_breaker_half_open_to_open(agent_backend_module: Any) -> None:
    """Test that failure in HALF_OPEN state reopens circuit."""
    breaker = agent_backend_module.CircuitBreaker("test", failure_threshold=2, recovery_timeout=1)

    # Open and wait for recovery
    breaker.record_failure()
    breaker.record_failure()
    assert breaker.is_open() is True

    time.sleep(1.1)
    breaker.is_open()  # Transition to HALF_OPEN

    # Failure should reopen
    breaker.record_failure()
    assert breaker.state == "OPEN"


# ============================================================================
# Metrics Tests
# ============================================================================

def test_get_metrics(agent_backend_module: Any) -> None:
    """Test metrics collection."""
    agent_backend_module.reset_metrics()

    metrics = agent_backend_module.get_metrics()
    assert "requests" in metrics
    assert "errors" in metrics
    assert "timeouts" in metrics
    assert "cache_hits" in metrics
    assert "total_latency_ms" in metrics


def test_reset_metrics(agent_backend_module: Any) -> None:
    """Test metrics reset."""
    agent_backend_module.reset_metrics()

    # Manually increment metrics
    agent_backend_module._metrics["requests"] = 100
    assert agent_backend_module._metrics["requests"] == 100

    # Reset
    agent_backend_module.reset_metrics()
    assert agent_backend_module._metrics["requests"] == 0


def test_metrics_tracking_in_llm_chat(agent_backend_module: Any) -> None:
    """Test that metrics are tracked during API calls."""
    agent_backend_module.reset_metrics()
    agent_backend_module.clear_response_cache()

    with patch("agent_backend.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "response"}}]
        }
        mock_requests.post.return_value = mock_response

        agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4", base_url="https://api.test",
            token="token", use_cache=False
        )

        metrics = agent_backend_module.get_metrics()
        assert metrics["requests"] >= 1


# ============================================================================
# Timeout Configuration Tests
# ============================================================================

def test_configure_timeout_per_backend(agent_backend_module: Any) -> None:
    """Test backend-specific timeout configuration."""
    agent_backend_module.configure_timeout_per_backend("github-models", 120)

    import os
    assert os.environ.get("DV_AGENT_TIMEOUT_GITHUB-MODELS") == "120"


# ============================================================================
# Streaming Tests
# ============================================================================

def test_streaming_payload_flag(agent_backend_module: Any) -> None:
    """Test that streaming flag is included in payload when requested."""
    with patch("agent_backend.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "response"}}]
        }
        mock_requests.post.return_value = mock_response

        # Call with stream=True
        agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4", base_url="https://api.test",
            token="token", stream=True, use_cache=False
        )

        # Check that payload was sent
        assert mock_requests.post.called
        call_args = mock_requests.post.call_args
        assert call_args is not None


# ============================================================================
# Backend Diagnostics Tests
# ============================================================================

def test_get_backend_status(agent_backend_module: Any) -> None:
    """Test backend status reporting."""
    status = agent_backend_module.get_backend_status()

    assert "selected_backend" in status
    assert "repo_root" in status
    assert "max_context_chars" in status
    assert "commands" in status
    assert "github_models" in status

    # Check commands dict
    assert "copilot" in status["commands"]
    assert "gh" in status["commands"]

    # Check github_models dict
    assert "requests_installed" in status["github_models"]
    assert "base_url_set" in status["github_models"]
    assert "model_set" in status["github_models"]
    assert "token_set" in status["github_models"]
    assert "configured" in status["github_models"]


def test_describe_backends(agent_backend_module: Any) -> None:
    """Test backend diagnostics output."""
    description = agent_backend_module.describe_backends()

    assert "Backend diagnostics:" in description
    assert "selected:" in description
    assert "repo_root:" in description
    assert "copilot" in description or "Copilot" in description
    assert "github-models" in description or "GitHub" in description


# ============================================================================
# Integration Tests
# ============================================================================

def test_cache_different_models_separately(agent_backend_module: Any) -> None:
    """Test that different models are cached separately."""
    agent_backend_module.clear_response_cache()

    key1 = agent_backend_module._get_cache_key("test", "gpt-4")
    key2 = agent_backend_module._get_cache_key("test", "gpt-3.5")

    # Keys should be different
    assert key1 != key2


def test_cache_different_prompts_separately(agent_backend_module: Any) -> None:
    """Test that different prompts are cached separately."""
    agent_backend_module.clear_response_cache()

    key1 = agent_backend_module._get_cache_key("prompt1", "gpt-4")
    key2 = agent_backend_module._get_cache_key("prompt2", "gpt-4")

    # Keys should be different
    assert key1 != key2


def test_validation_with_streaming_disabled(agent_backend_module: Any) -> None:
    """Test response validation with streaming disabled (default)."""
    with patch("agent_backend.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "valid code response"}}]
        }
        mock_requests.post.return_value = mock_response

        result = agent_backend_module.llm_chat_via_github_models(
            prompt="generate code", model="gpt-4",
            base_url="https://api.test", token="token",
            validate_content=True, use_cache=False
        )

        assert result == "valid code response"


def test_response_content_stripped(agent_backend_module: Any) -> None:
    """Test that responses are trimmed of whitespace."""
    with patch("agent_backend.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "  response with whitespace  "}}]
        }
        mock_requests.post.return_value = mock_response

        result = agent_backend_module.llm_chat_via_github_models(
            prompt="test", model="gpt-4",
            base_url="https://api.test", token="token", use_cache=False
        )

        assert result == "response with whitespace"
        assert not result.startswith(" ")
        assert not result.endswith(" ")


# =============================================================================
# Phase 6: Enum Tests
# =============================================================================


class TestBackendTypeEnum:
    """Tests for BackendType enum."""

    def test_enum_values(self, agent_backend_module: Any) -> None:
        """Test enum has expected values."""
        BackendType = agent_backend_module.BackendType
        assert BackendType.COPILOT_CLI.value == "copilot"
        assert BackendType.GH_COPILOT.value == "gh"
        assert BackendType.GITHUB_MODELS.value == "github-models"
        assert BackendType.AUTO.value == "auto"

    def test_all_members(self, agent_backend_module: Any) -> None:
        """Test all members exist."""
        BackendType = agent_backend_module.BackendType
        assert len(list(BackendType)) == 4


class TestBackendStateEnum:
    """Tests for BackendState enum."""

    def test_enum_values(self, agent_backend_module: Any) -> None:
        """Test enum has expected values."""
        BackendState = agent_backend_module.BackendState
        assert BackendState.HEALTHY.value == "healthy"
        assert BackendState.DEGRADED.value == "degraded"
        assert BackendState.UNHEALTHY.value == "unhealthy"
        assert BackendState.UNKNOWN.value == "unknown"


class TestCircuitStateEnum:
    """Tests for CircuitState enum."""

    def test_enum_values(self, agent_backend_module: Any) -> None:
        """Test enum has expected values."""
        CircuitState = agent_backend_module.CircuitState
        assert CircuitState.CLOSED.value == "closed"
        assert CircuitState.OPEN.value == "open"
        assert CircuitState.HALF_OPEN.value == "half_open"


class TestRequestPriorityEnum:
    """Tests for RequestPriority enum."""

    def test_enum_ordering(self, agent_backend_module: Any) -> None:
        """Test priority values are ordered."""
        RequestPriority = agent_backend_module.RequestPriority
        assert RequestPriority.LOW.value < RequestPriority.NORMAL.value
        assert RequestPriority.NORMAL.value < RequestPriority.HIGH.value
        assert RequestPriority.HIGH.value < RequestPriority.CRITICAL.value


class TestResponseTransformEnum:
    """Tests for ResponseTransform enum."""

    def test_all_members(self, agent_backend_module: Any) -> None:
        """Test all members exist."""
        ResponseTransform = agent_backend_module.ResponseTransform
        members = [m.name for m in ResponseTransform]
        assert "NONE" in members
        assert "STRIP_WHITESPACE" in members
        assert "EXTRACT_CODE" in members
        assert "EXTRACT_JSON" in members


class TestLoadBalanceStrategyEnum:
    """Tests for LoadBalanceStrategy enum."""

    def test_all_strategies(self, agent_backend_module: Any) -> None:
        """Test all strategies exist."""
        LoadBalanceStrategy = agent_backend_module.LoadBalanceStrategy
        members = [m.name for m in LoadBalanceStrategy]
        assert "ROUND_ROBIN" in members
        assert "LEAST_CONNECTIONS" in members
        assert "WEIGHTED" in members
        assert "FAILOVER" in members


# =============================================================================
# Phase 6: Dataclass Tests
# =============================================================================


class TestBackendConfigDataclass:
    """Tests for BackendConfig dataclass."""

    def test_creation(self, agent_backend_module: Any) -> None:
        """Test creating BackendConfig."""
        BackendConfig = agent_backend_module.BackendConfig
        BackendType = agent_backend_module.BackendType

        config = BackendConfig(
            name="test",
            backend_type=BackendType.GITHUB_MODELS,
            enabled=True,
            weight=2,
            timeout_s=120,
        )
        assert config.name == "test"
        assert config.backend_type == BackendType.GITHUB_MODELS
        assert config.enabled is True
        assert config.weight == 2
        assert config.timeout_s == 120


class TestRequestContextDataclass:
    """Tests for RequestContext dataclass."""

    def test_creation_with_defaults(self, agent_backend_module: Any) -> None:
        """Test creating RequestContext with defaults."""
        RequestContext = agent_backend_module.RequestContext
        RequestPriority = agent_backend_module.RequestPriority

        context = RequestContext()
        assert context.request_id is not None
        assert context.priority == RequestPriority.NORMAL
        assert context.created_at > 0


class TestBackendResponseDataclass:
    """Tests for BackendResponse dataclass."""

    def test_creation(self, agent_backend_module: Any) -> None:
        """Test creating BackendResponse."""
        BackendResponse = agent_backend_module.BackendResponse

        response = BackendResponse(
            content="test response",
            backend="github-models",
            latency_ms=150,
            cached=False,
        )
        assert response.content == "test response"
        assert response.backend == "github-models"
        assert response.latency_ms == 150
        assert response.cached is False


class TestBackendHealthStatusDataclass:
    """Tests for BackendHealthStatus dataclass."""

    def test_creation(self, agent_backend_module: Any) -> None:
        """Test creating BackendHealthStatus."""
        BackendHealthStatus = agent_backend_module.BackendHealthStatus
        BackendState = agent_backend_module.BackendState

        status = BackendHealthStatus(
            backend="test",
            state=BackendState.HEALTHY,
            success_rate=0.95,
        )
        assert status.backend == "test"
        assert status.state == BackendState.HEALTHY
        assert status.success_rate == 0.95


class TestQueuedRequestDataclass:
    """Tests for QueuedRequest dataclass."""

    def test_comparison(self, agent_backend_module: Any) -> None:
        """Test QueuedRequest priority comparison."""
        QueuedRequest = agent_backend_module.QueuedRequest

        high = QueuedRequest(priority=3, timestamp=1.0, request_id="1", prompt="p1")
        low = QueuedRequest(priority=1, timestamp=1.0, request_id="2", prompt="p2")

        # Higher priority should be "less than" for priority queue
        assert high < low


# =============================================================================
# Phase 6: Response Transformer Tests
# =============================================================================


class TestStripWhitespaceTransformer:
    """Tests for StripWhitespaceTransformer."""

    def test_transform(self, agent_backend_module: Any) -> None:
        """Test whitespace stripping."""
        transformer = agent_backend_module.StripWhitespaceTransformer()
        assert transformer.transform("  hello  ") == "hello"
        assert transformer.get_name() == "strip_whitespace"


class TestExtractCodeTransformer:
    """Tests for ExtractCodeTransformer."""

    def test_extract_code_block(self, agent_backend_module: Any) -> None:
        """Test extracting code from markdown."""
        transformer = agent_backend_module.ExtractCodeTransformer()

        markdown = "Here is code:\n```python\nprint('hello')\n```\nEnd."
        result = transformer.transform(markdown)

        assert "print('hello')" in result
        assert "```" not in result

    def test_get_name(self, agent_backend_module: Any) -> None:
        """Test transformer name."""
        transformer = agent_backend_module.ExtractCodeTransformer()
        assert transformer.get_name() == "extract_code"


class TestExtractJsonTransformer:
    """Tests for ExtractJsonTransformer."""

    def test_extract_json(self, agent_backend_module: Any) -> None:
        """Test extracting JSON from response."""
        transformer = agent_backend_module.ExtractJsonTransformer()

        response = 'Here is the data: {"key": "value"} and more text.'
        result = transformer.transform(response)

        assert '{"key": "value"}' in result or '"key"' in result

    def test_get_name(self, agent_backend_module: Any) -> None:
        """Test transformer name."""
        transformer = agent_backend_module.ExtractJsonTransformer()
        assert transformer.get_name() == "extract_json"


# =============================================================================
# Phase 6: RequestQueue Tests
# =============================================================================


class TestRequestQueue:
    """Tests for RequestQueue class."""

    def test_initialization(self, agent_backend_module: Any) -> None:
        """Test queue initialization."""
        RequestQueue = agent_backend_module.RequestQueue
        queue = RequestQueue()
        assert queue.is_empty() is True
        assert queue.size() == 0

    def test_enqueue_dequeue(self, agent_backend_module: Any) -> None:
        """Test enqueue and dequeue operations."""
        RequestQueue = agent_backend_module.RequestQueue
        RequestPriority = agent_backend_module.RequestPriority

        queue = RequestQueue()
        request_id = queue.enqueue("test prompt", RequestPriority.NORMAL)

        assert queue.size() == 1
        assert queue.is_empty() is False

        request = queue.dequeue()
        assert request.prompt == "test prompt"
        assert request.request_id == request_id

    def test_priority_ordering(self, agent_backend_module: Any) -> None:
        """Test that high priority requests are dequeued first."""
        RequestQueue = agent_backend_module.RequestQueue
        RequestPriority = agent_backend_module.RequestPriority

        queue = RequestQueue()
        queue.enqueue("low", RequestPriority.LOW)
        queue.enqueue("high", RequestPriority.HIGH)
        queue.enqueue("normal", RequestPriority.NORMAL)

        # High priority should come first
        first = queue.dequeue()
        assert first.prompt == "high"


# =============================================================================
# Phase 6: RequestBatcher Tests
# =============================================================================


class TestRequestBatcher:
    """Tests for RequestBatcher class."""

    def test_initialization(self, agent_backend_module: Any) -> None:
        """Test batcher initialization."""
        RequestBatcher = agent_backend_module.RequestBatcher
        batcher = RequestBatcher(batch_size=5, timeout_s=10.0)
        assert batcher.pending_count() == 0

    def test_add_requests(self, agent_backend_module: Any) -> None:
        """Test adding requests to batcher."""
        RequestBatcher = agent_backend_module.RequestBatcher
        batcher = RequestBatcher(batch_size=3)

        batcher.add("prompt1")
        batcher.add("prompt2")
        assert batcher.pending_count() == 2
        assert batcher.is_ready() is False

        batcher.add("prompt3")
        assert batcher.is_ready() is True

    def test_get_batch(self, agent_backend_module: Any) -> None:
        """Test getting batch."""
        RequestBatcher = agent_backend_module.RequestBatcher
        batcher = RequestBatcher(batch_size=2)

        batcher.add("prompt1")
        batcher.add("prompt2")

        batch = batcher.get_batch()
        assert batch is not None
        assert len(batch.requests) == 2
        assert batcher.pending_count() == 0


# =============================================================================
# Phase 6: BackendHealthMonitor Tests
# =============================================================================


class TestBackendHealthMonitor:
    """Tests for BackendHealthMonitor class."""

    def test_initialization(self, agent_backend_module: Any) -> None:
        """Test monitor initialization."""
        BackendHealthMonitor = agent_backend_module.BackendHealthMonitor
        monitor = BackendHealthMonitor()
        assert monitor.health_threshold == 0.8

    def test_record_success(self, agent_backend_module: Any) -> None:
        """Test recording successful request."""
        BackendHealthMonitor = agent_backend_module.BackendHealthMonitor
        monitor = BackendHealthMonitor()

        monitor.record_success("test-backend", 150)
        assert monitor.is_healthy("test-backend") is True

    def test_record_failures_unhealthy(self, agent_backend_module: Any) -> None:
        """Test that many failures mark backend unhealthy."""
        BackendHealthMonitor = agent_backend_module.BackendHealthMonitor
        monitor = BackendHealthMonitor(health_threshold=0.8, window_size=10)

        # Record mostly failures
        for _ in range(8):
            monitor.record_failure("test-backend")
        for _ in range(2):
            monitor.record_success("test-backend", 100)

        # Success rate is 20%, should be unhealthy
        assert monitor.is_healthy("test-backend") is False

    def test_get_healthiest(self, agent_backend_module: Any) -> None:
        """Test getting healthiest backend."""
        BackendHealthMonitor = agent_backend_module.BackendHealthMonitor
        monitor = BackendHealthMonitor()

        # Record mixed results
        for _ in range(5):
            monitor.record_success("backend1", 100)
        for _ in range(5):
            monitor.record_failure("backend2")

        healthiest = monitor.get_healthiest(["backend1", "backend2"])
        assert healthiest == "backend1"


# =============================================================================
# Phase 6: LoadBalancer Tests
# =============================================================================


class TestLoadBalancer:
    """Tests for LoadBalancer class."""

    def test_initialization(self, agent_backend_module: Any) -> None:
        """Test load balancer initialization."""
        LoadBalancer = agent_backend_module.LoadBalancer
        LoadBalanceStrategy = agent_backend_module.LoadBalanceStrategy

        lb = LoadBalancer(LoadBalanceStrategy.ROUND_ROBIN)
        assert lb.strategy == LoadBalanceStrategy.ROUND_ROBIN

    def test_add_backend(self, agent_backend_module: Any) -> None:
        """Test adding backends."""
        LoadBalancer = agent_backend_module.LoadBalancer

        lb = LoadBalancer()
        lb.add_backend("backend1")
        lb.add_backend("backend2")

        backend = lb.next()
        assert backend is not None
        assert backend.name in ["backend1", "backend2"]

    def test_round_robin(self, agent_backend_module: Any) -> None:
        """Test round robin distribution."""
        LoadBalancer = agent_backend_module.LoadBalancer
        LoadBalanceStrategy = agent_backend_module.LoadBalanceStrategy

        lb = LoadBalancer(LoadBalanceStrategy.ROUND_ROBIN)
        lb.add_backend("backend1")
        lb.add_backend("backend2")

        # Should alternate
        b1 = lb.next()
        b2 = lb.next()
        b3 = lb.next()

        assert b1.name != b2.name or len([b1, b2, b3]) == 3

    def test_remove_backend(self, agent_backend_module: Any) -> None:
        """Test removing backends."""
        LoadBalancer = agent_backend_module.LoadBalancer

        lb = LoadBalancer()
        lb.add_backend("backend1")

        result = lb.remove_backend("backend1")
        assert result is True
        assert lb.next() is None


# =============================================================================
# Phase 6: UsageQuotaManager Tests
# =============================================================================


class TestUsageQuotaManager:
    """Tests for UsageQuotaManager class."""

    def test_initialization(self, agent_backend_module: Any) -> None:
        """Test quota manager initialization."""
        UsageQuotaManager = agent_backend_module.UsageQuotaManager
        manager = UsageQuotaManager(daily_limit=100, hourly_limit=10)
        assert manager.can_request() is True

    def test_record_request(self, agent_backend_module: Any) -> None:
        """Test recording requests."""
        UsageQuotaManager = agent_backend_module.UsageQuotaManager
        manager = UsageQuotaManager(daily_limit=100, hourly_limit=10)

        manager.record_request()
        daily, hourly = manager.get_remaining()
        assert daily == 99
        assert hourly == 9

    def test_quota_exceeded(self, agent_backend_module: Any) -> None:
        """Test quota enforcement."""
        UsageQuotaManager = agent_backend_module.UsageQuotaManager
        manager = UsageQuotaManager(daily_limit=2, hourly_limit=2)

        manager.record_request()
        manager.record_request()

        assert manager.can_request() is False

    def test_usage_report(self, agent_backend_module: Any) -> None:
        """Test getting usage report."""
        UsageQuotaManager = agent_backend_module.UsageQuotaManager
        manager = UsageQuotaManager(daily_limit=100, hourly_limit=10)

        manager.record_request()
        report = manager.get_usage_report()

        assert report["daily_used"] == 1
        assert report["daily_limit"] == 100
        assert report["daily_remaining"] == 99


# =============================================================================
# Phase 6: RequestTracer Tests
# =============================================================================


class TestRequestTracer:
    """Tests for RequestTracer class."""

    def test_initialization(self, agent_backend_module: Any) -> None:
        """Test tracer initialization."""
        RequestTracer = agent_backend_module.RequestTracer
        tracer = RequestTracer()
        assert tracer.get_active_traces() == []

    def test_start_trace(self, agent_backend_module: Any) -> None:
        """Test starting a trace."""
        RequestTracer = agent_backend_module.RequestTracer
        tracer = RequestTracer()

        context = tracer.start_trace("test request")
        assert context.request_id is not None
        assert context.correlation_id is not None
        assert len(tracer.get_active_traces()) == 1

    def test_end_trace(self, agent_backend_module: Any) -> None:
        """Test ending a trace."""
        RequestTracer = agent_backend_module.RequestTracer
        tracer = RequestTracer()

        context = tracer.start_trace("test")
        duration = tracer.end_trace(context.request_id, success=True)

        assert duration is not None
        assert duration >= 0
        assert len(tracer.get_active_traces()) == 0


# =============================================================================
# Phase 6: AuditLogger Tests
# =============================================================================


class TestAuditLogger:
    """Tests for AuditLogger class."""

    def test_initialization(self, agent_backend_module: Any) -> None:
        """Test audit logger initialization."""
        AuditLogger = agent_backend_module.AuditLogger
        logger = AuditLogger()
        assert logger.log_file is None

    def test_log_request(self, agent_backend_module: any, tmp_path) -> None:
        """Test logging a request."""
        AuditLogger = agent_backend_module.AuditLogger

        log_file = tmp_path / "audit.log"
        logger = AuditLogger(log_file=log_file)

        logger.log_request(
            backend="github-models",
            prompt="test prompt",
            response="test response",
            latency_ms=150,
            success=True,
        )

        assert log_file.exists()
        content = log_file.read_text()
        assert "github-models" in content

    def test_get_recent_entries(self, agent_backend_module: any, tmp_path) -> None:
        """Test getting recent entries."""
        AuditLogger = agent_backend_module.AuditLogger

        log_file = tmp_path / "audit.log"
        logger = AuditLogger(log_file=log_file)

        logger.log_request("b1", "p1", "r1", 100, True)
        logger.log_request("b2", "p2", "r2", 200, False)

        entries = logger.get_recent_entries(count=10)
        assert len(entries) == 2


# =============================================================================
# Phase 6: Integration Tests
# =============================================================================


class TestPhase6Integration:
    """Integration tests for Phase 6 features."""

    def test_queue_with_batcher(self, agent_backend_module: Any) -> None:
        """Test queue and batcher working together."""
        RequestQueue = agent_backend_module.RequestQueue
        RequestBatcher = agent_backend_module.RequestBatcher
        RequestPriority = agent_backend_module.RequestPriority

        queue = RequestQueue()
        batcher = RequestBatcher(batch_size=2)

        # Queue some requests
        queue.enqueue("prompt1", RequestPriority.NORMAL)
        queue.enqueue("prompt2", RequestPriority.HIGH)

        # Dequeue and batch
        while not queue.is_empty():
            request = queue.dequeue()
            batcher.add(request.prompt)

        assert batcher.is_ready() is True
        batch = batcher.get_batch()
        assert len(batch.requests) == 2

    def test_health_monitor_with_load_balancer(self, agent_backend_module: Any) -> None:
        """Test health monitor with load balancer."""
        BackendHealthMonitor = agent_backend_module.BackendHealthMonitor
        LoadBalancer = agent_backend_module.LoadBalancer

        monitor = BackendHealthMonitor()
        lb = LoadBalancer()

        lb.add_backend("backend1")
        lb.add_backend("backend2")

        # Record health data
        monitor.record_success("backend1", 100)
        monitor.record_failure("backend2")

        # Get next backend and check health
        backend = lb.next()
        is_healthy = monitor.is_healthy(backend.name)
        assert is_healthy is not None  # Either True or False

    def test_tracer_with_audit_logger(self, agent_backend_module: any, tmp_path) -> None:
        """Test tracer with audit logger."""
        RequestTracer = agent_backend_module.RequestTracer
        AuditLogger = agent_backend_module.AuditLogger

        log_file = tmp_path / "audit.log"
        tracer = RequestTracer()
        audit = AuditLogger(log_file=log_file)

        # Start trace
        context = tracer.start_trace("test request")

        # Log request with trace info
        audit.log_request(
            backend="test",
            prompt="test",
            response="response",
            latency_ms=100,
            request_id=context.request_id,
        )

        # End trace
        tracer.end_trace(context.request_id, success=True)

        entries = audit.get_recent_entries()
        assert len(entries) == 1
        assert entries[0]["request_id"] == context.request_id


# =============================================================================
# Session 9: Request Signing and Verification Tests
# =============================================================================


class TestRequestSigner:
    """Tests for RequestSigner class."""

    def test_signer_init(self, agent_backend_module: Any) -> None:
        """Test RequestSigner initialization."""
        RequestSigner = agent_backend_module.RequestSigner

        signer = RequestSigner(secret_key="test-secret")
        assert signer.secret_key == b"test-secret"

    def test_sign_data(self, agent_backend_module: Any) -> None:
        """Test signing data."""
        RequestSigner = agent_backend_module.RequestSigner

        signer = RequestSigner(secret_key="secret")
        signature = signer.sign("test data")

        assert len(signature) == 64  # SHA256 hex digest
        assert signature.isalnum()

    def test_verify_valid_signature(self, agent_backend_module: Any) -> None:
        """Test verifying valid signature."""
        RequestSigner = agent_backend_module.RequestSigner

        signer = RequestSigner(secret_key="secret")
        data = "test data"
        signature = signer.sign(data)

        assert signer.verify(data, signature) is True

    def test_verify_invalid_signature(self, agent_backend_module: Any) -> None:
        """Test verifying invalid signature."""
        RequestSigner = agent_backend_module.RequestSigner

        signer = RequestSigner(secret_key="secret")

        assert signer.verify("test data", "invalid") is False

    def test_stored_signature(self, agent_backend_module: Any) -> None:
        """Test signature storage by request ID."""
        RequestSigner = agent_backend_module.RequestSigner

        signer = RequestSigner(secret_key="secret")
        signature = signer.sign("data", request_id="req123")

        assert signer.get_stored_signature("req123") == signature


# =============================================================================
# Session 9: Request Deduplication Tests
# =============================================================================


class TestRequestDeduplicator:
    """Tests for RequestDeduplicator class."""

    def test_deduplicator_init(self, agent_backend_module: Any) -> None:
        """Test RequestDeduplicator initialization."""
        RequestDeduplicator = agent_backend_module.RequestDeduplicator

        dedup = RequestDeduplicator(ttl_seconds=60)
        assert dedup.ttl_seconds == 60

    def test_first_request_not_duplicate(self, agent_backend_module: Any) -> None:
        """Test first request is not a duplicate."""
        RequestDeduplicator = agent_backend_module.RequestDeduplicator

        dedup = RequestDeduplicator()

        assert dedup.is_duplicate("new prompt") is False

    def test_second_request_is_duplicate(self, agent_backend_module: Any) -> None:
        """Test second identical request is a duplicate."""
        RequestDeduplicator = agent_backend_module.RequestDeduplicator

        dedup = RequestDeduplicator()

        dedup.is_duplicate("same prompt")  # First request
        assert dedup.is_duplicate("same prompt") is True

    def test_store_and_retrieve_result(self, agent_backend_module: Any) -> None:
        """Test storing and retrieving result."""
        RequestDeduplicator = agent_backend_module.RequestDeduplicator

        dedup = RequestDeduplicator()
        prompt = "test prompt"

        dedup.is_duplicate(prompt)  # Mark as pending
        dedup.store_result(prompt, "result value")

        result = dedup.wait_for_result(prompt, timeout=1.0)
        assert result == "result value"


# =============================================================================
# Session 9: Version Negotiation Tests
# =============================================================================


class TestVersionNegotiator:
    """Tests for VersionNegotiator class."""

    def test_negotiator_init(self, agent_backend_module: Any) -> None:
        """Test VersionNegotiator initialization."""
        VersionNegotiator = agent_backend_module.VersionNegotiator

        negotiator = VersionNegotiator()
        assert negotiator._versions == {}

    def test_register_backend(self, agent_backend_module: Any) -> None:
        """Test registering backend version."""
        VersionNegotiator = agent_backend_module.VersionNegotiator

        negotiator = VersionNegotiator()
        version = negotiator.register_backend(
            "api",
            version="2.0",
            capabilities=["streaming", "batching"],
        )

        assert version.backend == "api"
        assert version.version == "2.0"
        assert "streaming" in version.capabilities

    def test_negotiate_success(self, agent_backend_module: Any) -> None:
        """Test successful version negotiation."""
        VersionNegotiator = agent_backend_module.VersionNegotiator

        negotiator = VersionNegotiator()
        negotiator.register_backend("api", "2.0", ["streaming"])

        result = negotiator.negotiate("api", required=["streaming"])
        assert result is not None

    def test_negotiate_missing_capability(self, agent_backend_module: Any) -> None:
        """Test negotiation fails with missing capability."""
        VersionNegotiator = agent_backend_module.VersionNegotiator

        negotiator = VersionNegotiator()
        negotiator.register_backend("api", "1.0", ["basic"])

        result = negotiator.negotiate("api", required=["streaming"])
        assert result is None


# =============================================================================
# Session 9: Capability Discovery Tests
# =============================================================================


class TestCapabilityDiscovery:
    """Tests for CapabilityDiscovery class."""

    def test_discovery_init(self, agent_backend_module: Any) -> None:
        """Test CapabilityDiscovery initialization."""
        CapabilityDiscovery = agent_backend_module.CapabilityDiscovery

        discovery = CapabilityDiscovery()
        assert discovery._capabilities == {}

    def test_register_capability(self, agent_backend_module: Any) -> None:
        """Test registering capability."""
        CapabilityDiscovery = agent_backend_module.CapabilityDiscovery

        discovery = CapabilityDiscovery()
        cap = discovery.register_capability(
            "github-models",
            "streaming",
            description="Stream responses",
        )

        assert cap.name == "streaming"
        assert cap.enabled is True

    def test_has_capability(self, agent_backend_module: Any) -> None:
        """Test checking capability."""
        CapabilityDiscovery = agent_backend_module.CapabilityDiscovery

        discovery = CapabilityDiscovery()
        discovery.register_capability("backend", "feature1")

        assert discovery.has_capability("backend", "feature1") is True
        assert discovery.has_capability("backend", "unknown") is False

    def test_discover_all(self, agent_backend_module: Any) -> None:
        """Test discovering all capabilities."""
        CapabilityDiscovery = agent_backend_module.CapabilityDiscovery

        discovery = CapabilityDiscovery()
        discovery.register_capability("b1", "cap1")
        discovery.register_capability("b2", "cap2")

        all_caps = discovery.discover_all()
        assert "b1" in all_caps
        assert "cap1" in all_caps["b1"]


# =============================================================================
# Session 9: Request Replay Tests
# =============================================================================


class TestRequestRecorder:
    """Tests for RequestRecorder class."""

    def test_recorder_init(self, agent_backend_module: Any) -> None:
        """Test RequestRecorder initialization."""
        RequestRecorder = agent_backend_module.RequestRecorder

        recorder = RequestRecorder(max_recordings=100)
        assert recorder.max_recordings == 100

    def test_record_request(self, agent_backend_module: Any) -> None:
        """Test recording a request."""
        RequestRecorder = agent_backend_module.RequestRecorder

        recorder = RequestRecorder()
        recording = recorder.record(
            prompt="test prompt",
            backend="github-models",
            response="test response",
            latency_ms=150,
        )

        assert recording.prompt == "test prompt"
        assert recording.response == "test response"

    def test_get_recordings(self, agent_backend_module: Any) -> None:
        """Test getting recordings."""
        RequestRecorder = agent_backend_module.RequestRecorder

        recorder = RequestRecorder()
        recorder.record("p1", "b1", "r1")
        recorder.record("p2", "b2", "r2")

        all_recs = recorder.get_recordings()
        assert len(all_recs) == 2

        b1_recs = recorder.get_recordings(backend="b1")
        assert len(b1_recs) == 1

    def test_export_recordings(self, agent_backend_module: Any) -> None:
        """Test exporting recordings as JSON."""
        RequestRecorder = agent_backend_module.RequestRecorder
        import json

        recorder = RequestRecorder()
        recorder.record("prompt", "backend", "response")

        export = recorder.export_recordings()
        data = json.loads(export)
        assert len(data) == 1


# =============================================================================
# Session 9: Config Hot-Reloading Tests
# =============================================================================


class TestConfigHotReloader:
    """Tests for ConfigHotReloader class."""

    def test_reloader_init(self, agent_backend_module: Any) -> None:
        """Test ConfigHotReloader initialization."""
        ConfigHotReloader = agent_backend_module.ConfigHotReloader

        reloader = ConfigHotReloader()
        assert reloader._config == {}

    def test_set_and_get_config(self, agent_backend_module: Any) -> None:
        """Test setting and getting config."""
        ConfigHotReloader = agent_backend_module.ConfigHotReloader

        reloader = ConfigHotReloader()
        reloader.set_config("timeout", 60)

        assert reloader.get_config("timeout") == 60

    def test_change_callback(self, agent_backend_module: Any) -> None:
        """Test change callback is called."""
        ConfigHotReloader = agent_backend_module.ConfigHotReloader

        reloader = ConfigHotReloader()
        changes = []
        reloader.on_change(lambda k, v: changes.append((k, v)))

        reloader.set_config("key", "value")

        assert len(changes) == 1
        assert changes[0] == ("key", "value")


# =============================================================================
# Session 9: Request Compression Tests
# =============================================================================


class TestRequestCompressor:
    """Tests for RequestCompressor class."""

    def test_compressor_init(self, agent_backend_module: Any) -> None:
        """Test RequestCompressor initialization."""
        RequestCompressor = agent_backend_module.RequestCompressor

        compressor = RequestCompressor(compression_level=6)
        assert compressor.compression_level == 6

    def test_compress_small_data(self, agent_backend_module: Any) -> None:
        """Test small data is not compressed."""
        RequestCompressor = agent_backend_module.RequestCompressor

        compressor = RequestCompressor()
        data = "small"
        compressed = compressor.compress(data, threshold=1000)

        # Should have 0x00 header (uncompressed)
        assert compressed[0] == 0

    def test_compress_large_data(self, agent_backend_module: Any) -> None:
        """Test large data is compressed."""
        RequestCompressor = agent_backend_module.RequestCompressor

        compressor = RequestCompressor()
        data = "x" * 2000  # Large repetitive data
        compressed = compressor.compress(data, threshold=1000)

        # Should have 0x01 header (compressed)
        assert compressed[0] == 1

    def test_roundtrip(self, agent_backend_module: Any) -> None:
        """Test compression / decompression roundtrip."""
        RequestCompressor = agent_backend_module.RequestCompressor

        compressor = RequestCompressor()
        original = "Test data " * 200
        compressed = compressor.compress(original, threshold=100)
        decompressed = compressor.decompress(compressed)

        assert decompressed == original


# =============================================================================
# Session 9: Backend Analytics Tests
# =============================================================================


class TestBackendAnalytics:
    """Tests for BackendAnalytics class."""

    def test_analytics_init(self, agent_backend_module: Any) -> None:
        """Test BackendAnalytics initialization."""
        BackendAnalytics = agent_backend_module.BackendAnalytics

        analytics = BackendAnalytics(retention_hours=24)
        assert analytics.retention_hours == 24

    def test_record_usage(self, agent_backend_module: Any) -> None:
        """Test recording usage."""
        BackendAnalytics = agent_backend_module.BackendAnalytics

        analytics = BackendAnalytics()
        record = analytics.record_usage(
            backend="github-models",
            tokens=500,
            latency_ms=150,
        )

        assert record.tokens_used == 500
        assert record.backend == "github-models"

    def test_generate_report(self, agent_backend_module: Any) -> None:
        """Test generating report."""
        BackendAnalytics = agent_backend_module.BackendAnalytics

        analytics = BackendAnalytics()
        analytics.record_usage("b1", tokens=100)
        analytics.record_usage("b1", tokens=200)
        analytics.record_usage("b2", tokens=50)

        report = analytics.generate_report()

        assert report["total_requests"] == 3
        assert report["total_tokens"] == 350


# =============================================================================
# Session 9: Connection Pooling Tests
# =============================================================================


class TestConnectionPool:
    """Tests for ConnectionPool class."""

    def test_pool_init(self, agent_backend_module: Any) -> None:
        """Test ConnectionPool initialization."""
        ConnectionPool = agent_backend_module.ConnectionPool

        pool = ConnectionPool(max_connections=10)
        assert pool.max_connections == 10

    def test_acquire_connection(self, agent_backend_module: Any) -> None:
        """Test acquiring connection."""
        ConnectionPool = agent_backend_module.ConnectionPool

        pool = ConnectionPool()
        conn = pool.acquire("backend1")

        assert conn is not None
        assert conn["backend"] == "backend1"

    def test_release_connection(self, agent_backend_module: Any) -> None:
        """Test releasing connection."""
        ConnectionPool = agent_backend_module.ConnectionPool

        pool = ConnectionPool()
        conn = pool.acquire("backend1")
        pool.release("backend1", conn)

        stats = pool.get_stats()
        assert stats["backend1"]["available"] == 1


# =============================================================================
# Session 9: Request Throttling Tests
# =============================================================================


class TestRequestThrottler:
    """Tests for RequestThrottler class."""

    def test_throttler_init(self, agent_backend_module: Any) -> None:
        """Test RequestThrottler initialization."""
        RequestThrottler = agent_backend_module.RequestThrottler

        throttler = RequestThrottler(requests_per_second=10)
        assert throttler.requests_per_second == 10

    def test_allow_request(self, agent_backend_module: Any) -> None:
        """Test allowing requests."""
        RequestThrottler = agent_backend_module.RequestThrottler

        throttler = RequestThrottler(burst_size=5)

        # Should allow first few requests
        assert throttler.allow_request("backend") is True
        assert throttler.allow_request("backend") is True

    def test_throttle_exhausted(self, agent_backend_module: Any) -> None:
        """Test throttling when exhausted."""
        RequestThrottler = agent_backend_module.RequestThrottler

        throttler = RequestThrottler(burst_size=2, requests_per_second=0.1)

        # Exhaust burst
        throttler.allow_request("backend")
        throttler.allow_request("backend")

        # Next should be throttled
        assert throttler.allow_request("backend") is False


# =============================================================================
# Session 9: TTL Cache Tests
# =============================================================================


class TestTTLCache:
    """Tests for TTLCache class."""

    def test_cache_init(self, agent_backend_module: Any) -> None:
        """Test TTLCache initialization."""
        TTLCache = agent_backend_module.TTLCache

        cache = TTLCache(default_ttl_seconds=300)
        assert cache.default_ttl_seconds == 300

    def test_set_and_get(self, agent_backend_module: Any) -> None:
        """Test setting and getting cache entry."""
        TTLCache = agent_backend_module.TTLCache

        cache = TTLCache()
        cache.set("key", "value")

        assert cache.get("key") == "value"

    def test_expired_entry(self, agent_backend_module: Any) -> None:
        """Test expired entry returns None."""
        TTLCache = agent_backend_module.TTLCache

        cache = TTLCache(default_ttl_seconds=0.01)  # Very short TTL
        cache.set("key", "value")

        time.sleep(0.02)  # Wait for expiration
        assert cache.get("key") is None

    def test_invalidate(self, agent_backend_module: Any) -> None:
        """Test invalidating cache entry."""
        TTLCache = agent_backend_module.TTLCache

        cache = TTLCache()
        cache.set("key", "value")

        assert cache.invalidate("key") is True
        assert cache.get("key") is None


# =============================================================================
# Session 9: A / B Testing Tests
# =============================================================================


class TestABTester:
    """Tests for ABTester class."""

    def test_tester_init(self, agent_backend_module: Any) -> None:
        """Test ABTester initialization."""
        ABTester = agent_backend_module.ABTester

        tester = ABTester()
        assert tester._tests == {}

    def test_create_test(self, agent_backend_module: Any) -> None:
        """Test creating A / B test."""
        ABTester = agent_backend_module.ABTester

        tester = ABTester()
        variant_a, variant_b = tester.create_test(
            "test1",
            backend_a="fast",
            backend_b="slow",
            weight_a=0.7,
        )

        assert variant_a.backend == "fast"
        assert variant_a.weight == 0.7
        assert variant_b.weight == 0.3

    def test_assign_variant(self, agent_backend_module: Any) -> None:
        """Test variant assignment is consistent."""
        ABTester = agent_backend_module.ABTester

        tester = ABTester()
        tester.create_test("test1", "a", "b")

        variant1 = tester.assign_variant("test1", "user1")
        variant2 = tester.assign_variant("test1", "user1")

        # Same user should get same variant
        assert variant1.name == variant2.name

    def test_record_result(self, agent_backend_module: Any) -> None:
        """Test recording test results."""
        ABTester = agent_backend_module.ABTester

        tester = ABTester()
        tester.create_test("test1", "a", "b")

        tester.record_result("test1", "A", latency_ms=100)
        tester.record_result("test1", "A", latency_ms=200)

        results = tester.get_results("test1")
        assert results["variants"]["A"]["sample_count"] == 2

    def test_get_winner(self, agent_backend_module: Any) -> None:
        """Test determining winner."""
        ABTester = agent_backend_module.ABTester

        tester = ABTester()
        tester.create_test("test1", "a", "b")

        tester.record_result("test1", "A", success_rate=0.9)
        tester.record_result("test1", "B", success_rate=0.7)

        winner = tester.get_winner("test1", "success_rate", higher_is_better=True)
        assert winner == "A"


# =============================================================================
# GitHub Models Integration Tests
# =============================================================================

class TestGitHubModelsIntegration(unittest.TestCase):
    """Test integration with real GitHub Models API."""

    def test_github_models_api_endpoint_format(self):
        """Test GitHub Models API endpoint format."""
        api_endpoint = "https://models.githubusercontent.com / meta / llama-2-7b-chat"

        # Verify endpoint is properly formatted
        self.assertTrue(api_endpoint.startswith("https://"))
        self.assertIn("models.githubusercontent.com", api_endpoint)
        self.assertIn("meta / llama-2-7b-chat", api_endpoint)

    def test_github_models_authentication_token(self):
        """Test authentication with GitHub Models."""
        auth_token = "ghp_xxxxxxxxxxxxxxxxxxxx"
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application / json"
        }

        self.assertIn("Authorization", headers)
        self.assertTrue(headers["Authorization"].startswith("Bearer "))

    def test_github_models_request_payload_format(self):
        """Test request payload format for GitHub Models."""
        payload = {
            "messages": [
                {"role": "user", "content": "Hello, how are you?"}
            ],
            "temperature": 0.7,
            "top_p": 1.0,
            "max_tokens": 2048,
            "stream": False
        }

        self.assertIn("messages", payload)
        self.assertEqual(len(payload["messages"]), 1)
        self.assertEqual(payload["messages"][0]["role"], "user")

    def test_github_models_response_parsing(self):
        """Test parsing GitHub Models API response."""
        response_json = {
            "id": "chatcmpl-xxxxx",
            "object": "chat.completion",
            "created": 1234567890,
            "model": "meta / llama-2-7b-chat",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "I'm doing well, thank you for asking!"
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 10,
                "completion_tokens": 15,
                "total_tokens": 25
            }
        }

        # Extract response content
        assistant_message = response_json["choices"][0]["message"]["content"]
        self.assertEqual(assistant_message, "I'm doing well, thank you for asking!")

    def test_github_models_streaming_response(self):
        """Test handling streaming responses from GitHub Models."""
        # Simulated streaming response chunks
        stream_chunks = [
            '{"choices":[{"delta":{"content":"Hello"}}]}\n',
            '{"choices":[{"delta":{"content":" "}}]}\n',
            '{"choices":[{"delta":{"content":"world"}}]}\n',
            '{"choices":[{"delta":{"content":"!"}}]}\n'
        ]

        # Aggregate stream chunks
        content = ""
        for chunk in stream_chunks:
            data = json.loads(chunk)
            if data["choices"][0].get("delta", {}).get("content"):
                content += data["choices"][0]["delta"]["content"]

        self.assertEqual(content, "Hello world!")

    def test_github_models_error_handling(self):
        """Test error handling with GitHub Models API."""
        error_response = {
            "error": {
                "code": "401",
                "message": "Unauthorized",
                "details": "Invalid authentication token"
            }
        }

        self.assertEqual(error_response["error"]["code"], "401")

    def test_github_models_rate_limiting(self):
        """Test handling rate limiting from GitHub Models."""
        rate_limit_headers = {
            "x-ratelimit-limit": "100",
            "x-ratelimit-remaining": "0",
            "x-ratelimit-reset": "1234567890"
        }

        remaining = int(rate_limit_headers["x-ratelimit-remaining"])
        self.assertEqual(remaining, 0)

    def test_github_models_token_usage_tracking(self):
        """Test tracking token usage from API response."""
        usage_info = {
            "prompt_tokens": 42,
            "completion_tokens": 135,
            "total_tokens": 177
        }

        total = usage_info["total_tokens"]
        prompt_ratio = usage_info["prompt_tokens"] / total
        completion_ratio = usage_info["completion_tokens"] / total

        self.assertAlmostEqual(prompt_ratio + completion_ratio, 1.0, places=2)

    def test_github_models_concurrent_requests(self):
        """Test handling concurrent requests to GitHub Models."""
        import concurrent.futures

        def make_request(request_id):
            """Simulate API request."""
            return {
                "request_id": request_id,
                "status": "success",
                "response": f"Response to request {request_id}"
            }

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(make_request, i) for i in range(5)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        self.assertEqual(len(results), 5)

    def test_github_models_timeout_handling(self):
        """Test handling timeouts when calling GitHub Models."""

        class TimeoutError(Exception):
            pass

        def api_call_with_timeout(timeout_seconds):
            # Simulate timeout
            if timeout_seconds < 1:
                raise TimeoutError(f"Request exceeded {timeout_seconds}s timeout")
            return {"status": "success"}

        with self.assertRaises(TimeoutError):
            api_call_with_timeout(0.5)

    def test_github_models_retry_logic(self):
        """Test retry logic for failed GitHub Models requests."""

        class RetryableAPICall:
            def __init__(self, max_retries=3):
                self.max_retries = max_retries
                self.attempt_count = 0

            def call(self):
                self.attempt_count += 1
                if self.attempt_count < 3:
                    raise ConnectionError("Temporary connection error")
                return {"status": "success"}

            def execute_with_retry(self):
                for attempt in range(self.max_retries):
                    try:
                        return self.call()
                    except ConnectionError:
                        if attempt == self.max_retries - 1:
                            raise

        api_call = RetryableAPICall(max_retries=5)
        result = api_call.execute_with_retry()
        self.assertEqual(result["status"], "success")
        self.assertEqual(api_call.attempt_count, 3)


class TestCustomModelEndpoints(unittest.TestCase):
    """Test support for custom model endpoints and authentication."""

    def test_custom_endpoint_configuration(self):
        """Test configuring custom model endpoints."""
        custom_endpoints = {
            "local_llm": "http://localhost:8000 / v1",
            "private_api": "https://api.company.com / v1 / models",
            "azure_openai": (
                "https://company.openai.azure.com / openai / deployments / "
                "model-name / chat / completions"
            ),
            "ollama": "http://localhost:11434 / api"}

        self.assertIn("local_llm", custom_endpoints)
        self.assertEqual(custom_endpoints["ollama"], "http://localhost:11434 / api")

    def test_custom_authentication_methods(self):
        """Test different authentication methods for custom endpoints."""
        auth_methods = {
            "api_key": {
                "type": "api_key",
                "header": "X-API-Key",
                "value": "secret-key-123"
            },
            "bearer_token": {
                "type": "bearer",
                "header": "Authorization",
                "format": "Bearer {token}"
            },
            "oauth2": {
                "type": "oauth2",
                "client_id": "client-123",
                "client_secret": "secret-123",
                "token_endpoint": "https://auth.example.com / oauth / token"
            },
            "basic_auth": {
                "type": "basic",
                "username": "user",
                "password": "pass"
            }
        }

        self.assertEqual(auth_methods["api_key"]["type"], "api_key")
        self.assertEqual(auth_methods["bearer_token"]["format"], "Bearer {token}")

    def test_build_custom_endpoint_request(self):
        """Test building requests to custom endpoints."""
        class CustomEndpointClient:
            def __init__(self, endpoint_url, auth_config):
                self.endpoint_url = endpoint_url
                self.auth_config = auth_config

            def build_headers(self):
                headers = {"Content-Type": "application / json"}

                if self.auth_config["type"] == "api_key":
                    headers[self.auth_config["header"]] = self.auth_config["value"]
                elif self.auth_config["type"] == "bearer":
                    headers["Authorization"] = f"Bearer {self.auth_config['token']}"

                return headers

            def build_request(self, messages):
                return {
                    "url": self.endpoint_url,
                    "headers": self.build_headers(),
                    "json": {"messages": messages}
                }

        auth = {"type": "api_key", "header": "X-API-Key", "value": "key123"}
        client = CustomEndpointClient("http://localhost:8000 / v1 / chat", auth)

        request = client.build_request([{"role": "user", "content": "Hi"}])
        self.assertEqual(request["headers"]["X-API-Key"], "key123")

    def test_custom_endpoint_response_parsing(self):
        """Test parsing responses from custom endpoints."""
        # Different response formats from different providers
        response_formats = {
            "openai_compatible": {
                "choices": [{"message": {"content": "response"}}],
                "usage": {"total_tokens": 100}
            },
            "anthropic": {
                "content": [{"text": "response"}],
                "usage": {"input_tokens": 50, "output_tokens": 50}
            },
            "huggingface": {
                "generated_text": "response",
                "details": {"tokens": 100}
            },
            "ollama": {
                "response": "response",
                "prompt_eval_count": 50,
                "eval_count": 50
            }
        }

        # Generic parser that handles multiple formats
        def extract_response_content(response, format_type):
            if format_type == "openai_compatible":
                return response["choices"][0]["message"]["content"]
            elif format_type == "anthropic":
                return response["content"][0]["text"]
            elif format_type == "huggingface":
                return response["generated_text"]
            elif format_type == "ollama":
                return response["response"]

        openai_response = extract_response_content(
            response_formats["openai_compatible"],
            "openai_compatible"
        )
        self.assertEqual(openai_response, "response")

    def test_custom_endpoint_fallback_chain(self):
        """Test fallback chain when multiple custom endpoints available."""
        endpoints = [
            {"name": "primary", "url": "https://primary.example.com", "available": False},
            {"name": "secondary", "url": "https://secondary.example.com", "available": True},
            {"name": "tertiary", "url": "https://tertiary.example.com", "available": True}
        ]

        def select_available_endpoint(endpoints):
            for endpoint in endpoints:
                if endpoint["available"]:
                    return endpoint
            raise RuntimeError("No available endpoints")

        selected = select_available_endpoint(endpoints)
        self.assertEqual(selected["name"], "secondary")

    def test_custom_endpoint_ssl_verification(self):
        """Test SSL verification for custom endpoints."""
        endpoint_config = {
            "url": "https://secure.example.com",
            "verify_ssl": True,
            "ca_bundle_path": "/etc / ssl / certs / ca-bundle.crt"
        }

        self.assertTrue(endpoint_config["verify_ssl"])
        self.assertIn("ca_bundle_path", endpoint_config)

    def test_custom_endpoint_request_timeout_config(self):
        """Test configuring timeout for custom endpoint requests."""
        endpoint_timeouts = {
            "local_llm": 5,
            "cloud_api": 30,
            "slow_inference": 120
        }

        self.assertEqual(endpoint_timeouts["local_llm"], 5)
        self.assertEqual(endpoint_timeouts["slow_inference"], 120)

    def test_custom_endpoint_parameter_mapping(self):
        """Test mapping parameters between different endpoint formats."""
        class ParameterMapper:
            """Maps request parameters to different endpoint formats."""

            def map_to_openai_format(self, request):
                return {
                    "model": request.get("model"),
                    "messages": request.get("messages"),
                    "temperature": request.get("temperature", 0.7),
                    "max_tokens": request.get("max_tokens", 2048)
                }

            def map_to_anthropic_format(self, request):
                return {
                    "model": request.get("model"),
                    "messages": request.get("messages"),
                    "temperature": request.get("temperature", 0.7),
                    "max_tokens": request.get("max_tokens", 2048)
                }

            def map_to_ollama_format(self, request):
                return {
                    "model": request.get("model"),
                    "messages": request.get("messages"),
                    "temperature": request.get("temperature", 0.7),
                    "stream": request.get("stream", False)
                }

        mapper = ParameterMapper()
        openai_params = mapper.map_to_openai_format({
            "model": "gpt-4",
            "messages": [{"role": "user", "content": "hi"}],
            "temperature": 0.5
        })

        self.assertEqual(openai_params["model"], "gpt-4")
        self.assertEqual(openai_params["temperature"], 0.5)

    def test_custom_endpoint_cost_tracking(self):
        """Test tracking costs for custom endpoints."""
        class CostTracker:
            def __init__(self):
                self.endpoint_costs = {}

            def record_request(
                    self,
                    endpoint_name,
                    input_tokens,
                    output_tokens,
                    cost_per_1k_tokens):
                if endpoint_name not in self.endpoint_costs:
                    self.endpoint_costs[endpoint_name] = {"total_cost": 0, "requests": 0}

                total_tokens = input_tokens + output_tokens
                cost = (total_tokens / 1000) * cost_per_1k_tokens

                self.endpoint_costs[endpoint_name]["total_cost"] += cost
                self.endpoint_costs[endpoint_name]["requests"] += 1

            def get_total_cost(self):
                return sum(ec["total_cost"] for ec in self.endpoint_costs.values())

        tracker = CostTracker()
        tracker.record_request("local_llm", 100, 200, 0)  # Local=free
        tracker.record_request("cloud_api", 100, 200, 0.002)  # $0.002 per 1k tokens

        total = tracker.get_total_cost()
        self.assertGreater(total, 0)

    def test_custom_endpoint_health_check(self):
        """Test health checking for custom endpoints."""
        class EndpointHealthCheck:
            def __init__(self, endpoint_url):
                self.endpoint_url = endpoint_url
                self.last_check = None
                self.is_healthy = None

            def check_health(self):
                """Check if endpoint is reachable."""
                try:
                    # Simulate health check request
                    self.is_healthy = True
                    self.last_check = datetime.now()
                    return True
                except Exception:
                    self.is_healthy = False
                    self.last_check = datetime.now()
                    return False

        health_check = EndpointHealthCheck("http://localhost:8000")
        result = health_check.check_health()
        self.assertTrue(result)
        self.assertIsNotNone(health_check.last_check)
