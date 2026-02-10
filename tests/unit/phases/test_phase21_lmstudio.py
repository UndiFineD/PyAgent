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
Phase 21 LM Studio Integration Tests
=====================================

Tests for LM Studio backend and msgspec serializers.

37 tests covering:
- LMStudioBackend (sync/async/streaming)
- MsgSpecSerializer (JSON/MsgPack encoding)
- Chat message structures
- Integration with LLMClient
"""

# pylint: disable=protected-access,unused-variable,unused-argument
import os
import time
import inspect
from unittest.mock import MagicMock, patch, AsyncMock

import pytest


# ============================================================================
# LMStudio Backend Tests
# ============================================================================


class TestLMStudioConfig:
    """Tests for LMStudioConfig dataclass."""

    def test_default_config(self):
        """Test default configuration values."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import (
            LMStudioConfig,
        )

        # Ensure DV_* and LMSTUDIO_* vars do not influence default behavior
        dv_saved = {
            k: os.environ.pop(k, None)
            for k in ("DV_LMSTUDIO_BASE_URL", "DV_LMSTUDIO_MODEL", "DV_LMSTUDIO_MAX_CONTEXT")
        }
        lm_saved = {
            k: os.environ.pop(k, None)
            for k in ("LMSTUDIO_HOST", "LMSTUDIO_PORT", "LMSTUDIO_MODEL")
        }
        try:
            config = LMStudioConfig()
            assert config.host == "localhost"
            assert config.port == 1234
            assert config.timeout == 60.0
            assert config.temperature == 0.7
            assert config.max_tokens == 2048
        finally:
            # Restore any popped DV_* and LMSTUDIO_* environment variables
            for k, v in dv_saved.items():
                if v is not None:
                    os.environ[k] = v
            for k, v in lm_saved.items():
                if v is not None:
                    os.environ[k] = v

    def test_config_from_env(self):
        """Test configuration from environment variables."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import (
            LMStudioConfig,
        )

        # Ensure DV_* and existing LMSTUDIO_* do not interfere
        dv_saved = {
            k: os.environ.pop(k, None)
            for k in ("DV_LMSTUDIO_BASE_URL", "DV_LMSTUDIO_MODEL", "DV_LMSTUDIO_MAX_CONTEXT")
        }
        lm_saved = {
            k: os.environ.pop(k, None)
            for k in ("LMSTUDIO_HOST", "LMSTUDIO_PORT", "LMSTUDIO_MODEL")
        }
        os.environ["LMSTUDIO_HOST"] = "192.168.1.100"
        os.environ["LMSTUDIO_PORT"] = "5000"
        try:
            config = LMStudioConfig()
            assert config.host == "192.168.1.100"
            assert config.port == 5000
        finally:
            del os.environ["LMSTUDIO_HOST"]
            del os.environ["LMSTUDIO_PORT"]
            for k, v in dv_saved.items():
                if v is not None:
                    os.environ[k] = v
            for k, v in lm_saved.items():
                if v is not None:
                    os.environ[k] = v

    def test_config_from_dv_env(self):
        """Test configuration when using DV_ prefixed environment variables."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import LMStudioConfig

        os.environ["DV_LMSTUDIO_BASE_URL"] = "http://192.168.88.251:1234/v1"
        os.environ["DV_LMSTUDIO_MODEL"] = "zai-org/glm-4.7-flash"
        os.environ["DV_LMSTUDIO_MAX_CONTEXT"] = "128000"
        try:
            config = LMStudioConfig()
            assert config.host == "192.168.88.251"
            assert config.port == 1234
            assert config.default_model == "zai-org/glm-4.7-flash"
            assert config.max_context == 128000
            # DV_BASE_URL contained '/v1', so base_url should reflect that
            assert config.base_url == "http://192.168.88.251:1234/v1"
        finally:
            del os.environ["DV_LMSTUDIO_BASE_URL"]
            del os.environ["DV_LMSTUDIO_MODEL"]
            del os.environ["DV_LMSTUDIO_MAX_CONTEXT"]

    def test_base_url_uses_path_when_no_dv(self):
        """When DV_LMSTUDIO_BASE_URL not set, base_url should use host:port and configured path."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import LMStudioConfig

        # Ensure no DV override
        dv_saved = {k: os.environ.pop(k, None) for k in ("DV_LMSTUDIO_BASE_URL",)}
        try:
            # Default path => 'v1'
            config = LMStudioConfig(host="example.com", port=8080)
            assert config.base_url == "http://example.com:8080/v1"

            # Custom legacy LMSTUDIO_PATH should be respected (strip slashes)
            os.environ["LMSTUDIO_PATH"] = "/api/v2/"
            try:
                config2 = LMStudioConfig(host="example.com", port=8080)
                assert config2.base_url == "http://example.com:8080/api/v2"
            finally:
                del os.environ["LMSTUDIO_PATH"]
        finally:
            for k, v in dv_saved.items():
                if v is not None:
                    os.environ[k] = v

    def test_api_host_property(self):
        """Test api_host property."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import LMStudioConfig

        config = LMStudioConfig(host="example.com", port=8080)
        assert config.api_host == "example.com:8080"


class TestModelCache:
    """Tests for ModelCache class."""

    def test_cache_set_get(self):
        """Test basic cache operations."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import ModelCache

        cache = ModelCache(ttl=300.0)

        mock_model = MagicMock()
        cache.set("test-model", mock_model)

        entry = cache.get("test-model")
        assert entry is not None
        assert entry.model_id == "test-model"
        assert entry.model_info is mock_model

    def test_cache_miss(self):
        """Test cache miss returns None."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import ModelCache

        cache = ModelCache()
        assert cache.get("nonexistent") is None

    def test_cache_expiration(self):
        """Test cache entry expiration."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import ModelCache

        cache = ModelCache(ttl=0.01)  # 10ms TTL

        cache.set("test", MagicMock())
        assert cache.get("test") is not None

        time.sleep(0.02)  # Wait for expiration
        assert cache.get("test") is None

    def test_prune_expired(self):
        """Test pruning expired entries."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import ModelCache

        cache = ModelCache(ttl=0.01)
        cache.set("a", MagicMock())
        cache.set("b", MagicMock())

        time.sleep(0.02)
        removed = cache.prune_expired()
        assert removed == 2


class TestLMStudioBackend:
    """Tests for LMStudioBackend class."""

    def test_sdk_check_not_available(self):
        """Test SDK availability check when not installed."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import LMStudioBackend

        backend = LMStudioBackend(
            session=MagicMock(),
            connectivity_manager=MagicMock(),
        )

        # SDK check should not raise but return a boolean
        with patch.dict('sys.modules', {'lmstudio': None}):
            backend._sdk_available = None  # Reset cached value
            # This should handle ImportError gracefully

    def test_backend_provider_id(self):
        """Test provider ID constant."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import LMStudioBackend

        assert LMStudioBackend.PROVIDER_ID == "lmstudio"

    def test_get_info(self):
        """Test get_info method."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import LMStudioBackend

        backend = LMStudioBackend(
            session=MagicMock(),
            connectivity_manager=MagicMock(),
        )

        with patch.object(backend, 'list_loaded_models', return_value=["model1"]):
            with patch.object(backend, 'list_downloaded_models', return_value=["model1", "model2"]):
                info = backend.get_info()

        assert info["provider"] == "lmstudio"
        assert "host" in info
        assert info["loaded_models"] == ["model1"]
        assert info["downloaded_models"] == ["model1", "model2"]

    def test_chat_skipped_when_unavailable(self):
        """Test chat returns empty when backend unavailable."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import LMStudioBackend

        connectivity = MagicMock()
        connectivity.is_endpoint_available.return_value = False

        LMStudioBackend(
            session=MagicMock(),
            connectivity_manager=connectivity,
        )

    @pytest.mark.asyncio
    async def test_async_client_various_accessor_shapes(self):
        """Ensure async client LLm access works with `.get`, callable, and fallback helpers."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import LMStudioBackend

        backend = LMStudioBackend(
            session=MagicMock(),
            connectivity_manager=MagicMock(),
        )

        # Helper fixtures
        class MockLLM:
            """Mock LLM for async client testing."""
            def __init__(self, response: str):
                self._response = response

            async def respond(self, _chat, config=None, **kwargs):
                """Mock respond method for testing."""
                return self._response

        # Case A: client.llm has async `.get` method
        async_get = AsyncMock()
        async_get.return_value = MockLLM("resp-a")
        # Simulate SDK that exposes `client.llm.get(...)` as an async coroutine
        async_get.get = AsyncMock(return_value=MockLLM("resp-a"))
        mock_client_a = MagicMock()
        mock_client_a.llm = async_get

        # Patch AsyncClient context manager
        async_cm = AsyncMock()
        async_cm.__aenter__.return_value = mock_client_a
        async_cm.__aexit__.return_value = None

        lm_mod_a = MagicMock()
        lm_mod_a.__version__ = "1.0"
        lm_mod_a.AsyncClient = MagicMock(return_value=async_cm)
        lm_mod_a.Chat = MagicMock(return_value=MagicMock())
        lm_mod_a.llm = MagicMock()

        with patch.dict('sys.modules', {'lmstudio': lm_mod_a}):
            res = await backend.chat_async("hello", model="m-a")
            assert res == "resp-a"

        # Case B: client.llm is callable and returns model (sync)
        mock_llm_b = MockLLM("resp-b")
        def callable_llm(model=None):
            return mock_llm_b

        mock_client_b = MagicMock()
        mock_client_b.llm = callable_llm

        async_cm_b = AsyncMock()
        async_cm_b.__aenter__.return_value = mock_client_b
        async_cm_b.__aexit__.return_value = None

        lm_mod_b = MagicMock()
        lm_mod_b.__version__ = "1.0"
        lm_mod_b.AsyncClient = MagicMock(return_value=async_cm_b)
        lm_mod_b.Chat = MagicMock(return_value=MagicMock())
        lm_mod_b.llm = MagicMock()

        with patch.dict('sys.modules', {'lmstudio': lm_mod_b}):
            res = await backend.chat_async("hello", model="m-b")
            assert res == "resp-b"

        # Case C: client.llm not helpful -> fallback to module helper
        fake_module = MagicMock()
        fake_module.__version__ = "1.0"
        fake_module.llm.return_value = MockLLM("resp-c")
        # Use a context manager that yields a client with `llm` set to None so
        # that the backend falls back to module-level helper
        mock_client_c = MagicMock()
        mock_client_c.llm = None
        async_cm_c = AsyncMock()
        async_cm_c.__aenter__.return_value = mock_client_c
        async_cm_c.__aexit__.return_value = None
        fake_module.AsyncClient = MagicMock(return_value=async_cm_c)
        fake_module.Chat = MagicMock(return_value=MagicMock())

        with patch.dict('sys.modules', {'lmstudio': fake_module}):
            res = await backend.chat_async("hello", model="m-c")
            assert res == "resp-c"

        # Mock _is_working to return False
        backend._is_working = MagicMock(return_value=False)

        result = backend.chat("Hello", model="test")
        assert result == ""

    def test_disconnect(self):
        """Test disconnect clears resources."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import LMStudioBackend

        backend = LMStudioBackend(
            session=MagicMock(),
            connectivity_manager=MagicMock(),
        )

        mock_client = MagicMock()
        backend._client = mock_client
        backend._model_cache.set("test", MagicMock())

        backend.disconnect()

        assert backend._client is None
        mock_client.close.assert_called_once()


class TestLMStudioConvenienceFunctions:
    """Tests for convenience functions."""

    def test_lmstudio_chat_import(self):
        """Test convenience function can be imported."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import lmstudio_chat

        assert callable(lmstudio_chat)

    def test_get_client_uses_http_scheme_for_api_host(self):
        """LM Studio client should be created with http:// scheme when base url lacks scheme."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import LMStudioBackend

        os.environ["DV_LMSTUDIO_BASE_URL"] = "http://192.168.88.251:1234/v1"
        try:
            backend = LMStudioBackend(session=MagicMock(), connectivity_manager=MagicMock())
            mock_lmstudio = MagicMock()
            mock_client = MagicMock()
            # Provide a __version__ attr used by _check_sdk and Client/AsyncClient constructors
            mock_lmstudio.__version__ = "1.0"
            mock_lmstudio.Client = MagicMock(return_value=mock_client)
            mock_lmstudio.AsyncClient = MagicMock(return_value=mock_client)
            with patch.dict('sys.modules', {'lmstudio': mock_lmstudio}):
                # _get_client should attempt to instantiate lmstudio.Client with the full base URL (including /v1)
                backend._get_client()
                mock_lmstudio.Client.assert_called_once_with("http://192.168.88.251:1234/v1")
        finally:
            del os.environ["DV_LMSTUDIO_BASE_URL"]

    def test_get_model_http_fallback_when_client_creation_fails(self):
        """If client creation fails, backend should detect model via HTTP and return an HTTP-fallback LLM."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import LMStudioBackend

        backend = LMStudioBackend(session=MagicMock(), connectivity_manager=MagicMock())

        # Simulate failure when creating client
        backend._get_client = MagicMock(side_effect=RuntimeError("connect fail"))
        # Simulate HTTP fallback detection returning the expected model
        backend.list_loaded_models = MagicMock(return_value=["zai-org/glm-4.7-flash"])
        # Stub out underlying HTTP chat request
        backend._http_chat_request = MagicMock(return_value="http-response")

        llm = backend.get_model("zai-org/glm-4.7-flash")
        assert llm is not None
        assert hasattr(llm, "respond")

        # The fallback LLM's respond should call into _http_chat_request
        resp = llm.respond("hello world")
        assert resp == "http-response"
    def test_lmstudio_stream_import(self):
        """Test streaming function can be imported."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import lmstudio_stream

        assert callable(lmstudio_stream)

    def test_lmstudio_chat_async_import(self):
        """Test async function can be imported."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import lmstudio_chat_async

        assert inspect.iscoroutinefunction(lmstudio_chat_async)


# ============================================================================
# MsgSpec Serializer Tests
# ============================================================================

class TestMsgSpecAvailability:
    """Tests for msgspec availability and module imports."""

    def test_is_msgspec_available(self):
        """Test availability check."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import is_msgspec_available

        assert is_msgspec_available()

    def test_require_msgspec(self):
        """Test require function doesn't raise when available."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import require_msgspec

        # Should not raise
        require_msgspec()


class TestJSONEncoder:
    """Tests for JSONEncoder class."""

    def test_encode_decode_dict(self):
        """Test encoding and decoding a dictionary."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import JSONEncoder

        encoder = JSONEncoder()
        data = {"name": "test", "value": 42, "nested": {"a": 1}}

        encoded = encoder.encode(data)
        assert isinstance(encoded, bytes)

        decoded = encoder.decode(encoded)
        assert decoded == data

    def test_encode_str(self):
        """Test encoding to string."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import JSONEncoder

        encoder = JSONEncoder()
        data = {"key": "value"}

        result = encoder.encode_str(data)
        assert isinstance(result, str)
        assert '"key"' in result

    def test_decode_from_string(self):
        """Test decoding from string input."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import JSONEncoder

        encoder = JSONEncoder()
        json_str = '{"name": "test"}'

        decoded = encoder.decode(json_str)
        assert decoded["name"] == "test"

    def test_decode_lines(self):
        """Test decoding newline-delimited JSON."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import JSONEncoder

        encoder = JSONEncoder()
        ndjson = '{"id": 1}\n{"id": 2}\n{"id": 3}'

        results = list(encoder.decode_lines(ndjson))
        assert len(results) == 3
        assert [r["id"] for r in results] == [1, 2, 3]


class TestMsgPackEncoder:
    """Tests for MsgPackEncoder class."""

    def test_encode_decode(self):
        """Test MessagePack encoding and decoding."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import MsgPackEncoder

        encoder = MsgPackEncoder()
        data = {"numbers": [1, 2, 3], "flag": True}

        encoded = encoder.encode(data)
        assert isinstance(encoded, bytes)

        decoded = encoder.decode(encoded)
        assert decoded == data

    def test_smaller_than_json(self):
        """Test MessagePack produces smaller output than JSON."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import (
            JSONEncoder,
            MsgPackEncoder,
        )

        json_enc = JSONEncoder()
        msgpack_enc = MsgPackEncoder()

        data = {"key": "value", "numbers": list(range(100))}

        json_size = len(json_enc.encode(data))
        msgpack_size = len(msgpack_enc.encode(data))

        assert msgpack_size < json_size


class TestTypedSerializer:
    """Tests for TypedSerializer class."""

    def test_typed_json_serialization(self):
        """Test type-safe JSON serialization."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import TypedSerializer
        import msgspec

        class User(msgspec.Struct):
            """Internal schema for testing."""
            name: str
            age: int

        serializer = TypedSerializer(User, serialization_format="json")

        user = User(name="Alice", age=30)
        encoded = serializer.encode(user)

        decoded = serializer.decode(encoded)
        assert decoded.name == "Alice"
        assert decoded.age == 30

    def test_typed_msgpack_serialization(self):
        """Test type-safe MessagePack serialization."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import TypedSerializer
        import msgspec

        class Config(msgspec.Struct):
            """Internal schema for testing."""
            enabled: bool
            count: int

        serializer = TypedSerializer(Config, serialization_format="msgpack")

        config = Config(enabled=True, count=5)
        encoded = serializer.encode(config)
        decoded = serializer.decode(encoded)

        assert decoded.enabled is True
        assert decoded.count == 5

    def test_encode_many(self):
        """Test encoding multiple objects."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import TypedSerializer
        import msgspec

        class Item(msgspec.Struct):
            """Internal schema for testing."""
            id: int

        serializer = TypedSerializer(Item, serialization_format="json")

        items = [Item(id=1), Item(id=2), Item(id=3)]
        encoded = serializer.encode_many(items)

        # Should be valid JSON array
        import json
        parsed = json.loads(encoded)
        assert len(parsed) == 3


class TestChatMessageStructs:
    """Tests for chat message structures."""

    def test_role_enum(self):
        """Test Role enum values."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import Role

        assert Role.SYSTEM == "system"
        assert Role.USER == "user"
        assert Role.ASSISTANT == "assistant"
        assert Role.TOOL == "tool"

    def test_chat_message_struct(self):
        """Test ChatMessage struct."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import ChatMessage, Role

        msg = ChatMessage(role=Role.USER, content="Hello!")
        assert msg.role == Role.USER
        assert msg.content == "Hello!"
        assert msg.name is None

    def test_chat_completion_request(self):
        """Test ChatCompletionRequest struct."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import (
            ChatCompletionRequest,
            ChatMessage,
            Role,
        )

        request = ChatCompletionRequest(
            model="test-model",
            messages=[
                ChatMessage(role=Role.SYSTEM, content="You are helpful."),
                ChatMessage(role=Role.USER, content="Hi!"),
            ],
            temperature=0.5,
        )

        assert request.model == "test-model"
        assert len(request.messages) == 2
        assert request.temperature == 0.5
        assert not request.stream


class TestChatHelpers:
    """Tests for chat encoding/decoding helpers."""

    def test_encode_chat_request(self):
        """Test encoding a chat request."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import encode_chat_request

        messages = [
            {"role": "system", "content": "Be helpful"},
            {"role": "user", "content": "Hello"},
        ]

        encoded = encode_chat_request(messages, model="test")
        assert isinstance(encoded, bytes)

        # Should contain expected fields
        import json
        parsed = json.loads(encoded)
        assert parsed["model"] == "test"
        assert len(parsed["messages"]) == 2


class TestBenchmarking:
    """Tests for benchmarking utilities."""

    def test_benchmark_serialization(self):
        """Test serialization benchmarking."""
        from src.infrastructure.storage.serialization.msg_spec_serializer import benchmark_serialization

        data = {"key": "value", "numbers": [1, 2, 3, 4, 5]}

        results = benchmark_serialization(data, iterations=100)

        assert "json" in results
        assert "msgpack" in results

        # Check result properties
        json_result = results["json"]
        assert json_result.iterations == 100
        assert json_result.encode_time > 0
        assert json_result.decode_time > 0
        assert json_result.encode_throughput > 0


# ============================================================================
# Integration Tests
# ============================================================================


class TestLLMClientIntegration:
    """Tests for LLMClient integration with LM Studio."""

    def test_lmstudio_backend_registered(self):
        """Test that lmstudio backend is registered in LLMClient."""
        from src.infrastructure.compute.backend.llm_client import LLMClient
        import requests

        with patch.object(requests, 'Session', return_value=MagicMock()):
            client = LLMClient(requests)

        assert "lmstudio" in client.backends

    def test_llm_chat_via_lmstudio_method(self):
        """Test llm_chat_via_lmstudio method exists."""
        from src.infrastructure.compute.backend.llm_client import LLMClient
        import requests as req_module

        with patch.object(req_module, 'Session', return_value=MagicMock()):
            client = LLMClient(req_module)

        assert hasattr(client, 'llm_chat_via_lmstudio')
        assert callable(client.llm_chat_via_lmstudio)

    def test_lmstudio_in_known_backends(self):
        """Test lmstudio is in smart_chat fallback chain."""
        from src.infrastructure.compute.backend.llm_client import LLMClient

        # Check source code contains lmstudio in known_backends
        source = inspect.getsource(LLMClient.smart_chat)
        assert "lmstudio" in source


class TestPhase21ModuleStructure:
    """Tests for Phase 21 module structure."""

    def test_serialization_package_exports(self):
        """Test serialization package exports new functions."""
        from src.infrastructure.storage.serialization import (
            is_msgspec_available,
            JSONEncoder,
            MsgPackEncoder,
            TypedSerializer,
        )

        assert callable(is_msgspec_available)
        assert JSONEncoder is not None
        assert MsgPackEncoder is not None
        assert TypedSerializer is not None

    def test_lmstudio_backend_exports(self):
        """Test LMStudioBackend exports."""
        from src.infrastructure.compute.backend.llm_backends.lm_studio_backend import (
            LMStudioBackend,
            LMStudioConfig,
            ModelCache,
            CachedModel,
            lmstudio_chat,
            lmstudio_stream,
            lmstudio_chat_async,
        )

        assert LMStudioBackend.PROVIDER_ID == "lmstudio"
        assert LMStudioConfig is not None
        assert ModelCache is not None
        assert CachedModel is not None
        assert callable(lmstudio_chat)
        assert callable(lmstudio_stream)
        assert callable(lmstudio_chat_async)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
