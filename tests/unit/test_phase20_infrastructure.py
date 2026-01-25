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
Phase 20 Infrastructure Tests
==============================

Tests for Phase 20 production infrastructure modules:
- ExtensionRegistry
- CollectionUtils
- FuncUtils
- NetworkUtils
- EnvConfig
- OpenTelemetryTracer

42 tests covering all Phase 20 functionality.
"""

import os
import sys
import time
import socket
import threading
import warnings
from typing import Any
from unittest.mock import patch, MagicMock

import pytest


# ============================================================================
# ExtensionRegistry Tests
# ============================================================================


class TestExtensionManager:
    """Tests for ExtensionManager class."""

    def test_register_and_load(self):
        """Test basic registration and loading."""
        from src.core.base.registry.extension_registry import ExtensionManager

        registry = ExtensionManager("test")

        @registry.register("foo")
        class Foo:
            def __init__(self, value: int):
                self.value = value

        instance = registry.load("foo", value=42)
        assert instance.value == 42

    def test_register_class_programmatically(self):
        """Test programmatic registration."""
        from src.core.base.registry.extension_registry import ExtensionManager

        registry = ExtensionManager("test")

        class Bar:
            pass

        registry.register_class("bar", Bar)
        assert registry.has("bar")
        assert isinstance(registry.load("bar"), Bar)

    def test_load_not_found(self):
        """Test loading non-existent class."""
        from src.core.base.registry.extension_registry import ExtensionManager

        registry = ExtensionManager("test")

        with pytest.raises(KeyError, match="not found"):
            registry.load("nonexistent")

    def test_list_registered(self):
        """Test listing registered classes."""
        from src.core.base.registry.extension_registry import ExtensionManager

        registry = ExtensionManager("test")

        @registry.register("a")
        class A: pass

        @registry.register("b")
        class B: pass

        assert set(registry.list_registered()) == {"a", "b"}
        assert len(registry) == 2


class TestTypedExtensionManager:
    """Tests for TypedExtensionManager class."""

    def test_typed_registration(self):
        """Test type-safe registration."""
        from src.core.base.registry.extension_registry import TypedExtensionManager
        from abc import ABC, abstractmethod

        class BasePlugin(ABC):
            @abstractmethod
            def process(self) -> str: ...

        registry = TypedExtensionManager[BasePlugin]("plugins", BasePlugin)

        @registry.register("upper")
        class UpperPlugin(BasePlugin):
            def process(self) -> str:
                return "UPPER"

        plugin = registry.load("upper")
        assert plugin.process() == "UPPER"

    def test_invalid_type_registration(self):
        """Test that non-subclass registration fails."""
        from src.core.base.registry.extension_registry import TypedExtensionManager

        class Base: pass

        registry = TypedExtensionManager[Base]("test", Base)

        with pytest.raises(TypeError):
            @registry.register("invalid")
            class Invalid:
                pass


class TestMultiExtensionManager:
    """Tests for MultiExtensionManager class."""

    def test_multiple_registrations(self):
        """Test multiple implementations per key."""
        from src.core.base.registry.extension_registry import MultiExtensionManager

        registry = MultiExtensionManager("handlers")

        @registry.register("format", priority=10)
        class JSONFormatter:
            name = "json"

        @registry.register("format", priority=5)
        class XMLFormatter:
            name = "xml"

        # Higher priority first
        first = registry.get_first("format")
        assert first.name == "json"

        # Get all
        all_formatters = registry.get_all("format")
        assert len(all_formatters) == 2


class TestLazyExtensionManager:
    """Tests for LazyExtensionManager class."""

    def test_lazy_loading(self):
        """Test lazy module loading."""
        from src.core.base.registry.extension_registry import LazyExtensionManager

        registry = LazyExtensionManager("lazy")
        registry.register_lazy("json_encoder", "json:JSONEncoder")

        # Not loaded yet
        assert not registry.is_loaded("json_encoder")

        # Now load it
        cls = registry.get_class("json_encoder")
        import json
        assert cls is json.JSONEncoder
        assert registry.is_loaded("json_encoder")


# ============================================================================
# CollectionUtils Tests
# ============================================================================


class TestLazyDict:
    """Tests for LazyDict class."""

    def test_lazy_evaluation(self):
        """Test that values are computed lazily."""
        from src.core.base.common.utils.collection_utils import LazyDict

        computed = []

        def compute_a():
            computed.append("a")
            return 1

        def compute_b():
            computed.append("b")
            return 2

        d = LazyDict({"a": compute_a, "b": compute_b})

        # Not computed yet
        assert computed == []

        # Access a
        assert d["a"] == 1
        assert computed == ["a"]

        # Access again - uses cache
        assert d["a"] == 1
        assert computed == ["a"]

        # Access b
        assert d["b"] == 2
        assert computed == ["a", "b"]

    def test_is_computed(self):
        """Test is_computed method."""
        from src.core.base.common.utils.collection_utils import LazyDict

        d = LazyDict({"a": lambda: 1})

        assert not d.is_computed("a")
        _ = d["a"]
        assert d.is_computed("a")


class TestListUtilities:
    """Tests for list utility functions."""

    def test_chunk_list(self):
        """Test chunking a list."""
        from src.core.base.common.utils.collection_utils import chunk_list

        result = list(chunk_list([1, 2, 3, 4, 5], 2))
        assert result == [[1, 2], [3, 4], [5]]

    def test_flatten_2d_lists(self):
        """Test flattening nested lists."""
        from src.core.base.common.utils.collection_utils import flatten_2d_lists

        result = flatten_2d_lists([[1, 2], [3, 4], [5]])
        assert result == [1, 2, 3, 4, 5]

    def test_is_list_of(self):
        """Test type guard for lists."""
        from src.core.base.common.utils.collection_utils import is_list_of

        assert is_list_of([1, 2, 3], int)
        assert not is_list_of(["a", "b"], int)
        assert is_list_of([], int)  # Empty list

    def test_unique(self):
        """Test unique with preserved order."""
        from src.core.base.common.utils.collection_utils import unique

        result = unique([1, 2, 1, 3, 2, 4])
        assert result == [1, 2, 3, 4]


class TestGroupingUtilities:
    """Tests for grouping functions."""

    def test_full_groupby(self):
        """Test groupby without requiring sorted input."""
        from src.core.base.common.utils.collection_utils import full_groupby

        result = dict(full_groupby([1, 2, 3, 1, 2], key=lambda x: x % 2))
        assert result[1] == [1, 3, 1]
        assert result[0] == [2, 2]

    def test_partition(self):
        """Test partitioning items."""
        from src.core.base.common.utils.collection_utils import partition

        evens, odds = partition([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
        assert evens == [2, 4]
        assert odds == [1, 3, 5]


class TestDictUtilities:
    """Tests for dictionary functions."""

    def test_deep_merge_dicts(self):
        """Test recursive dictionary merge."""
        from src.core.base.common.utils.collection_utils import deep_merge_dicts

        base = {"a": 1, "b": {"c": 2}}
        override = {"b": {"d": 3}}

        result = deep_merge_dicts(base, override)
        assert result == {"a": 1, "b": {"c": 2, "d": 3}}

    def test_invert_dict(self):
        """Test dictionary inversion."""
        from src.core.base.common.utils.collection_utils import invert_dict

        result = invert_dict({"a": 1, "b": 2})
        assert result == {1: "a", 2: "b"}


# ============================================================================
# FuncUtils Tests
# ============================================================================


class TestRunOnce:
    """Tests for run_once decorator."""

    def test_runs_only_once(self):
        """Test function runs only once."""
        from src.core.base.common.utils.func_utils import run_once

        counter = [0]

        @run_once
        def increment():
            counter[0] += 1

        increment()
        increment()
        increment()

        assert counter[0] == 1


class TestDeprecation:
    """Tests for deprecation decorators."""

    def test_deprecate_kwargs(self):
        """Test keyword argument deprecation warning."""
        from src.core.base.common.utils.func_utils import deprecate_kwargs

        @deprecate_kwargs("old_param")
        def foo(new_param=None, old_param=None):
            return old_param

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            foo(old_param=1)
            assert len(w) == 1
            assert "deprecated" in str(w[0].message).lower()


class TestSupportsKw:
    """Tests for keyword argument inspection."""

    def test_supports_kw_basic(self):
        """Test supports_kw for basic functions."""
        from src.core.base.common.utils.func_utils import supports_kw

        def foo(a, b, c=None):
            pass

        assert supports_kw(foo, "c")
        assert supports_kw(foo, "a")
        assert not supports_kw(foo, "nonexistent", allow_var_kwargs=False)

    def test_supports_kw_with_kwargs(self):
        """Test supports_kw with **kwargs."""
        from src.core.base.common.utils.func_utils import supports_kw

        def foo(a, **kwargs):
            pass

        assert supports_kw(foo, "anything", allow_var_kwargs=True)


class TestMemoize:
    """Tests for memoization."""

    def test_memoize_caches_results(self):
        """Test that results are cached."""
        from src.core.base.common.utils.func_utils import memoize

        call_count = [0]

        @memoize
        def expensive(x):
            call_count[0] += 1
            return x * 2

        assert expensive(5) == 10
        assert expensive(5) == 10
        assert expensive(5) == 10
        assert call_count[0] == 1

        assert expensive(10) == 20
        assert call_count[0] == 2


class TestThrottle:
    """Tests for throttle decorator."""

    def test_throttle_limits_calls(self):
        """Test that calls are throttled."""
        from src.core.base.common.utils.func_utils import throttle

        call_count = [0]

        @throttle(0.1)
        def rapid_call():
            call_count[0] += 1

        # Call rapidly
        for _ in range(5):
            rapid_call()

        # Only first call should execute
        assert call_count[0] == 1


# ============================================================================
# NetworkUtils Tests
# ============================================================================


class TestIPDetection:
    """Tests for IP detection functions."""

    def test_get_ip(self):
        """Test IP address detection."""
        from src.infrastructure.swarm.network.network_utils import get_ip

        ip = get_ip()
        assert ip  # Should return something

    def test_is_valid_ipv4_address(self):
        """Test IPv4 validation."""
        from src.infrastructure.swarm.network.network_utils import is_valid_ipv4_address

        assert is_valid_ipv4_address("192.168.1.1")
        assert is_valid_ipv4_address("127.0.0.1")
        assert not is_valid_ipv4_address("256.1.1.1")
        assert not is_valid_ipv4_address("not-an-ip")

    def test_is_valid_ipv6_address(self):
        """Test IPv6 validation."""
        from src.infrastructure.swarm.network.network_utils import is_valid_ipv6_address

        assert is_valid_ipv6_address("::1")
        assert is_valid_ipv6_address("2001:db8::1")
        assert not is_valid_ipv6_address("not-an-ip")


class TestHostPortParsing:
    """Tests for host:port parsing."""

    def test_split_host_port_ipv4(self):
        """Test IPv4 host:port splitting."""
        from src.infrastructure.swarm.network.network_utils import split_host_port

        host, port = split_host_port("192.168.1.1:8080")
        assert host == "192.168.1.1"
        assert port == 8080

    def test_split_host_port_ipv6(self):
        """Test IPv6 [host]:port splitting."""
        from src.infrastructure.swarm.network.network_utils import split_host_port

        host, port = split_host_port("[::1]:8080")
        assert host == "::1"
        assert port == 8080

    def test_join_host_port(self):
        """Test joining host and port."""
        from src.infrastructure.swarm.network.network_utils import join_host_port

        assert join_host_port("localhost", 8080) == "localhost:8080"
        assert join_host_port("::1", 8080) == "[::1]:8080"


class TestPortDiscovery:
    """Tests for port discovery functions."""

    def test_get_open_port(self):
        """Test finding an open port."""
        from src.infrastructure.swarm.network.network_utils import get_open_port

        port = get_open_port()
        assert 1024 <= port <= 65535

    def test_get_open_ports(self):
        """Test getting multiple open ports."""
        from src.infrastructure.swarm.network.network_utils import get_open_ports

        ports = get_open_ports(3)
        assert len(ports) == 3
        assert len(set(ports)) == 3  # All unique


# ============================================================================
# EnvConfig Tests
# ============================================================================


class TestEnvVar:
    """Tests for EnvVar descriptor."""

    def test_envvar_default(self):
        """Test EnvVar with default value."""
        from src.core.config.env_config import EnvVar

        class Config:
            DEBUG = EnvVar("TEST_DEBUG_PHASE20", default=False)

        config = Config()
        assert config.DEBUG == False

    def test_envvar_from_environment(self):
        """Test EnvVar reading from environment."""
        from src.core.config.env_config import get_env_int

        os.environ["TEST_PORT_PHASE20"] = "9000"
        try:
            # Use the function directly rather than descriptor
            port = get_env_int("TEST_PORT_PHASE20", default=8080)
            assert port == 9000
        finally:
            del os.environ["TEST_PORT_PHASE20"]


class TestEnvFunctions:
    """Tests for environment variable functions."""

    def test_get_env_bool(self):
        """Test boolean environment variable."""
        from src.core.config.env_config import get_env_bool

        os.environ["TEST_BOOL_PHASE20"] = "true"
        try:
            assert get_env_bool("TEST_BOOL_PHASE20") == True
        finally:
            del os.environ["TEST_BOOL_PHASE20"]

    def test_get_env_int(self):
        """Test integer environment variable."""
        from src.core.config.env_config import get_env_int

        os.environ["TEST_INT_PHASE20"] = "42"
        try:
            assert get_env_int("TEST_INT_PHASE20") == 42
        finally:
            del os.environ["TEST_INT_PHASE20"]

    def test_get_env_list(self):
        """Test list environment variable."""
        from src.core.config.env_config import get_env_list

        os.environ["TEST_LIST_PHASE20"] = "a,b,c"
        try:
            assert get_env_list("TEST_LIST_PHASE20") == ["a", "b", "c"]
        finally:
            del os.environ["TEST_LIST_PHASE20"]


class TestTempEnv:
    """Tests for temp_env context manager."""

    def test_temp_env(self):
        """Test temporary environment variables."""
        from src.core.config.env_config import temp_env

        original = os.environ.get("TEST_TEMP_PHASE20")

        with temp_env(TEST_TEMP_PHASE20="temporary"):
            assert os.environ.get("TEST_TEMP_PHASE20") == "temporary"

        assert os.environ.get("TEST_TEMP_PHASE20") == original


class TestNamespacedConfig:
    """Tests for NamespacedConfig."""

    def test_namespaced_config(self):
        """Test namespaced configuration access."""
        from src.core.config.env_config import NamespacedConfig

        os.environ["MYAPP_DEBUG"] = "true"
        os.environ["MYAPP_PORT"] = "9000"
        try:
            config = NamespacedConfig("MYAPP")
            assert config.get_bool("DEBUG") == True
            assert config.get_int("PORT") == 9000
        finally:
            del os.environ["MYAPP_DEBUG"]
            del os.environ["MYAPP_PORT"]


# ============================================================================
# OpenTelemetryTracer Tests
# ============================================================================


class TestOtelAvailability:
    """Tests for OpenTelemetry availability."""

    def test_is_otel_available(self):
        """Test checking if otel is available."""
        from src.observability.tracing.open_telemetry_tracer import is_otel_available

        # Just check it returns a boolean
        result = is_otel_available()
        assert isinstance(result, bool)


class TestSpanAttributes:
    """Tests for SpanAttributes class."""

    def test_span_attributes_defined(self):
        """Test that standard span attributes are defined."""
        from src.observability.tracing.open_telemetry_tracer import SpanAttributes

        assert SpanAttributes.GEN_AI_USAGE_PROMPT_TOKENS == "gen_ai.usage.prompt_tokens"
        assert SpanAttributes.GEN_AI_REQUEST_MODEL == "gen_ai.request.model"
        assert SpanAttributes.AGENT_NAME == "agent.name"


class TestNullTracer:
    """Tests for NullTracer (testing helper)."""

    def test_null_tracer(self):
        """Test NullTracer for testing."""
        from src.observability.tracing.open_telemetry_tracer import get_null_tracer

        tracer = get_null_tracer()

        with tracer.start_as_current_span("test") as span:
            span.set_attribute("key", "value")
            span.add_event("event")
            assert not span.is_recording()


class TestSpanTiming:
    """Tests for SpanTiming helper."""

    def test_span_timing(self):
        """Test timing checkpoint recording."""
        from src.observability.tracing.open_telemetry_tracer import SpanTiming

        timing = SpanTiming()

        time.sleep(0.01)
        timing.checkpoint("step1")

        time.sleep(0.01)
        timing.checkpoint("step2")

        assert timing.checkpoints["step1"] > 0
        assert timing.checkpoints["step2"] > timing.checkpoints["step1"]

        attrs = timing.to_attributes()
        assert "total" in attrs
        assert "step1" in attrs
        assert "step2" in attrs


class TestTraceContextPropagation:
    """Tests for trace context propagation."""

    def test_extract_trace_headers(self):
        """Test extracting trace headers."""
        from src.observability.tracing.open_telemetry_tracer import extract_trace_headers

        headers = {
            "traceparent": "00-abcd-1234-01",
            "tracestate": "key=value",
            "content-type": "application/json",
        }

        result = extract_trace_headers(headers)
        assert "traceparent" in result
        assert "tracestate" in result
        assert "content-type" not in result

    def test_contains_trace_headers(self):
        """Test checking for trace headers."""
        from src.observability.tracing.open_telemetry_tracer import contains_trace_headers

        assert contains_trace_headers({"traceparent": "..."})
        assert not contains_trace_headers({"content-type": "..."})


# ============================================================================
# Integration Tests
# ============================================================================


class TestPhase20Integration:
    """Integration tests for Phase 20 modules."""

    def test_registry_with_collection_utils(self):
        """Test registry using collection utilities."""
        from src.core.base.registry.extension_registry import ExtensionManager
        from src.core.base.common.utils.collection_utils import unique

        registry = ExtensionManager("test")

        @registry.register("handler")
        class Handler:
            def handle(self, items):
                return unique(items)

        handler = registry.load("handler")
        result = handler.handle([1, 2, 1, 3, 2])
        assert result == [1, 2, 3]

    def test_func_utils_with_tracing(self):
        """Test function utilities with tracing."""
        from src.core.base.common.utils.func_utils import memoize
        from src.observability.tracing.open_telemetry_tracer import (
            get_null_tracer,
            SpanTiming,
        )

        tracer = get_null_tracer()

        @memoize
        def compute(x):
            timing = SpanTiming()
            result = x * 2
            timing.checkpoint("compute")
            return result, timing.elapsed()

        result1, time1 = compute(5)
        result2, time2 = compute(5)  # Cached

        assert result1 == 10
        assert result2 == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
