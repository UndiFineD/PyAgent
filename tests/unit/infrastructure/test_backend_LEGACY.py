import pytest
import time
from unittest.mock import patch, MagicMock
from pathlib import Path
from typing import Any, List, Dict, Optional
import sys
try:
    from tests.utils.agent_test_utils import *
except ImportError:
    pass

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


def test_configure_timeout_per_backend(agent_backend_module: Any) -> None:
    """Test backend-specific timeout configuration."""
    agent_backend_module.configure_timeout_per_backend("github-models", 120)

    import os
    assert os.environ.get("DV_AGENT_TIMEOUT_GITHUB-MODELS") == "120"


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


def test_get_backend_status(agent_backend_module: Any) -> None:
    """Test backend status reporting."""
    status = agent_backend_module.get_backend_status()

    assert "selected_backend" in status
    assert "repo_root" in status
    assert "max_context_chars" in status
    assert "commands" in status
    assert "github_models" in status

    # Check commands dict
    assert "codex" in status["commands"]
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
    assert "codex" in description or "Codex" in description
    assert "copilot" in description or "Copilot" in description
    assert "github-models" in description or "GitHub" in description


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
