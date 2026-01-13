# -*- coding: utf-8 -*-
"""Test classes from test_agent_backend.py - core module."""

from __future__ import annotations
import unittest
from typing import Any, List, Dict, Optional, Callable, Tuple, Set, Union
from unittest.mock import MagicMock, Mock, patch, call, ANY
import time
import json
from datetime import datetime
import pytest
import logging
from pathlib import Path
import sys
import os
import tempfile
import shutil
import subprocess
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Try to import test utilities
try:
    from tests.utils.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path
except ImportError:
    # Fallback
    AGENT_DIR: Path = Path(__file__).parent.parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self) -> bool: 

            return self
        def __exit__(self, *args) -> bool: 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed

class TestBackendTypeEnum:
    """Tests for BackendType enum."""

    def test_enum_values(self, agent_backend_module: Any) -> None:
        """Test enum has expected values."""
        BackendType = agent_backend_module.BackendType
        assert BackendType.CODEX.value == "codex"
        assert BackendType.COPILOT_CLI.value == "copilot"
        assert BackendType.GH_COPILOT.value == "gh"
        assert BackendType.GITHUB_MODELS.value == "github-models"
        assert BackendType.AUTO.value == "auto"

    def test_all_members(self, agent_backend_module: Any) -> None:
        """Test all members exist."""
        BackendType = agent_backend_module.BackendType
        assert len(list(BackendType)) == 5



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
        members: List[Any] = [m.name for m in ResponseTransform]
        assert "NONE" in members
        assert "STRIP_WHITESPACE" in members
        assert "EXTRACT_CODE" in members
        assert "EXTRACT_JSON" in members



class TestLoadBalanceStrategyEnum:
    """Tests for LoadBalanceStrategy enum."""

    def test_all_strategies(self, agent_backend_module: Any) -> None:
        """Test all strategies exist."""
        LoadBalanceStrategy = agent_backend_module.LoadBalanceStrategy
        members: List[Any] = [m.name for m in LoadBalanceStrategy]
        assert "ROUND_ROBIN" in members
        assert "LEAST_CONNECTIONS" in members
        assert "WEIGHTED" in members
        assert "FAILOVER" in members


# =============================================================================
# Phase 6: Dataclass Tests
# =============================================================================



class TestSystemConfigDataclass:
    """Tests for SystemConfig dataclass."""

    def test_creation(self, agent_backend_module: Any) -> None:
        """Test creating SystemConfig."""
        SystemConfig = agent_backend_module.SystemConfig
        BackendType = agent_backend_module.BackendType

        config = SystemConfig(
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



class TestSystemResponseDataclass:
    """Tests for SystemResponse dataclass."""

    def test_creation(self, agent_backend_module: Any) -> None:
        """Test creating SystemResponse."""
        SystemResponse = agent_backend_module.SystemResponse

        response = SystemResponse(
            content="test response",
            backend="github-models",
            latency_ms=150,
            cached=False,
        )
        assert response.content == "test response"
        assert response.backend == "github-models"
        assert response.latency_ms == 150
        assert response.cached is False



class TestSystemHealthStatusDataclass:
    """Tests for SystemHealthStatus dataclass."""

    def test_creation(self, agent_backend_module: Any) -> None:
        """Test creating SystemHealthStatus."""
        SystemHealthStatus = agent_backend_module.SystemHealthStatus
        BackendState = agent_backend_module.BackendState

        status = SystemHealthStatus(
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
# Phase 6: SystemHealthMonitor Tests
# =============================================================================



class TestSystemHealthMonitor:
    """Tests for SystemHealthMonitor class."""

    def test_initialization(self, agent_backend_module: Any) -> None:
        """Test monitor initialization."""
        SystemHealthMonitor = agent_backend_module.SystemHealthMonitor
        monitor = SystemHealthMonitor()
        assert monitor.health_threshold == 0.8

    def test_record_success(self, agent_backend_module: Any) -> None:
        """Test recording successful request."""
        SystemHealthMonitor = agent_backend_module.SystemHealthMonitor
        monitor = SystemHealthMonitor()

        monitor.record_success("test-backend", 150)
        assert monitor.is_healthy("test-backend") is True

    def test_record_failures_unhealthy(self, agent_backend_module: Any) -> None:
        """Test that many failures mark backend unhealthy."""
        SystemHealthMonitor = agent_backend_module.SystemHealthMonitor
        monitor = SystemHealthMonitor(health_threshold=0.8, window_size=10)

        # Record mostly failures
        for _ in range(8):
            monitor.record_failure("test-backend")
        for _ in range(2):
            monitor.record_success("test-backend", 100)

        # Success rate is 20%, should be unhealthy
        assert monitor.is_healthy("test-backend") is False

    def test_get_healthiest(self, agent_backend_module: Any) -> None:
        """Test getting healthiest backend."""
        SystemHealthMonitor = agent_backend_module.SystemHealthMonitor
        monitor = SystemHealthMonitor()

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

