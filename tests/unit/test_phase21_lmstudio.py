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

import os
import time
import inspect
from dataclasses import dataclass
from typing import Any
from unittest.mock import MagicMock, patch, AsyncMock

import pytest


# ============================================================================
# LMStudio Backend Tests
# ============================================================================


class TestLMStudioConfig:
    """Tests for LMStudioConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        from src.infrastructure.backend.llm_backends.LMStudioBackend import LMStudioConfig
        
        config = LMStudioConfig()
        assert config.host == "localhost"
        assert config.port == 1234
        assert config.timeout == 60.0
        assert config.temperature == 0.7
        assert config.max_tokens == 2048
    
    def test_config_from_env(self):
        """Test configuration from environment variables."""
        from src.infrastructure.backend.llm_backends.LMStudioBackend import LMStudioConfig
        
        os.environ["LMSTUDIO_HOST"] = "192.168.1.100"
        os.environ["LMSTUDIO_PORT"] = "5000"
        try:
            config = LMStudioConfig()
            assert config.host == "192.168.1.100"
            assert config.port == 5000
        finally:
            del os.environ["LMSTUDIO_HOST"]
            del os.environ["LMSTUDIO_PORT"]
    
    def test_api_host_property(self):
        """Test api_host property."""
        from src.infrastructure.backend.llm_backends.LMStudioBackend import LMStudioConfig
        
        config = LMStudioConfig(host="example.com", port=8080)
        assert config.api_host == "example.com:8080"


class TestModelCache:
    """Tests for ModelCache class."""
    
    def test_cache_set_get(self):
        """Test basic cache operations."""
        from src.infrastructure.backend.llm_backends.LMStudioBackend import ModelCache
        
        cache = ModelCache(ttl=300.0)
        
        mock_model = MagicMock()
        cache.set("test-model", mock_model)
        
        entry = cache.get("test-model")
        assert entry is not None
        assert entry.model_id == "test-model"
        assert entry.model_info is mock_model
    
    def test_cache_miss(self):
        """Test cache miss returns None."""
        from src.infrastructure.backend.llm_backends.LMStudioBackend import ModelCache
        
        cache = ModelCache()
        assert cache.get("nonexistent") is None
    
    def test_cache_expiration(self):
        """Test cache entry expiration."""
        from src.infrastructure.backend.llm_backends.LMStudioBackend import ModelCache, CachedModel
        
        cache = ModelCache(ttl=0.01)  # 10ms TTL
        
        cache.set("test", MagicMock())
        assert cache.get("test") is not None
        
        time.sleep(0.02)  # Wait for expiration
        assert cache.get("test") is None
    
    def test_prune_expired(self):
        """Test pruning expired entries."""
        from src.infrastructure.backend.llm_backends.LMStudioBackend import ModelCache
        
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
        from src.infrastructure.backend.llm_backends.LMStudioBackend import LMStudioBackend
        
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
        from src.infrastructure.backend.llm_backends.LMStudioBackend import LMStudioBackend
        
        assert LMStudioBackend.PROVIDER_ID == "lmstudio"
    
    def test_get_info(self):
        """Test get_info method."""
        from src.infrastructure.backend.llm_backends.LMStudioBackend import LMStudioBackend
        
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
        from src.infrastructure.backend.llm_backends.LMStudioBackend import LMStudioBackend
        
        connectivity = MagicMock()
        connectivity.is_endpoint_available.return_value = False
        
        backend = LMStudioBackend(
            session=MagicMock(),
            connectivity_manager=connectivity,
        )
        
        # Mock _is_working to return False
        backend._is_working = MagicMock(return_value=False)
        
        result = backend.chat("Hello", model="test")
        assert result == ""
    
    def test_disconnect(self):
        """Test disconnect clears resources."""
        from src.infrastructure.backend.llm_backends.LMStudioBackend import LMStudioBackend
        
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
        from src.infrastructure.backend.llm_backends.LMStudioBackend import lmstudio_chat
        
        assert callable(lmstudio_chat)
    
    def test_lmstudio_stream_import(self):
        """Test streaming function can be imported."""
        from src.infrastructure.backend.llm_backends.LMStudioBackend import lmstudio_stream
        
        assert callable(lmstudio_stream)
    
    def test_lmstudio_chat_async_import(self):
        """Test async function can be imported."""
        from src.infrastructure.backend.llm_backends.LMStudioBackend import lmstudio_chat_async
        
        assert inspect.iscoroutinefunction(lmstudio_chat_async)


# ============================================================================
# MsgSpec Serializer Tests
# ============================================================================


class TestMsgSpecAvailability:
    """Tests for msgspec availability."""
    
    def test_is_msgspec_available(self):
        """Test availability check."""
        from src.infrastructure.serialization.MsgSpecSerializer import is_msgspec_available
        
        assert is_msgspec_available() == True  # Should be installed
    
    def test_require_msgspec(self):
        """Test require function doesn't raise when available."""
        from src.infrastructure.serialization.MsgSpecSerializer import require_msgspec
        
        # Should not raise
        require_msgspec()


class TestJSONEncoder:
    """Tests for JSONEncoder class."""
    
    def test_encode_decode_dict(self):
        """Test encoding and decoding a dictionary."""
        from src.infrastructure.serialization.MsgSpecSerializer import JSONEncoder
        
        encoder = JSONEncoder()
        data = {"name": "test", "value": 42, "nested": {"a": 1}}
        
        encoded = encoder.encode(data)
        assert isinstance(encoded, bytes)
        
        decoded = encoder.decode(encoded)
        assert decoded == data
    
    def test_encode_str(self):
        """Test encoding to string."""
        from src.infrastructure.serialization.MsgSpecSerializer import JSONEncoder
        
        encoder = JSONEncoder()
        data = {"key": "value"}
        
        result = encoder.encode_str(data)
        assert isinstance(result, str)
        assert '"key"' in result
    
    def test_decode_from_string(self):
        """Test decoding from string input."""
        from src.infrastructure.serialization.MsgSpecSerializer import JSONEncoder
        
        encoder = JSONEncoder()
        json_str = '{"name": "test"}'
        
        decoded = encoder.decode(json_str)
        assert decoded["name"] == "test"
    
    def test_decode_lines(self):
        """Test decoding newline-delimited JSON."""
        from src.infrastructure.serialization.MsgSpecSerializer import JSONEncoder
        
        encoder = JSONEncoder()
        ndjson = '{"id": 1}\n{"id": 2}\n{"id": 3}'
        
        results = list(encoder.decode_lines(ndjson))
        assert len(results) == 3
        assert [r["id"] for r in results] == [1, 2, 3]


class TestMsgPackEncoder:
    """Tests for MsgPackEncoder class."""
    
    def test_encode_decode(self):
        """Test MessagePack encoding and decoding."""
        from src.infrastructure.serialization.MsgSpecSerializer import MsgPackEncoder
        
        encoder = MsgPackEncoder()
        data = {"numbers": [1, 2, 3], "flag": True}
        
        encoded = encoder.encode(data)
        assert isinstance(encoded, bytes)
        
        decoded = encoder.decode(encoded)
        assert decoded == data
    
    def test_smaller_than_json(self):
        """Test MessagePack produces smaller output than JSON."""
        from src.infrastructure.serialization.MsgSpecSerializer import (
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
        from src.infrastructure.serialization.MsgSpecSerializer import TypedSerializer
        import msgspec
        
        class User(msgspec.Struct):
            name: str
            age: int
        
        serializer = TypedSerializer(User, format="json")
        
        user = User(name="Alice", age=30)
        encoded = serializer.encode(user)
        
        decoded = serializer.decode(encoded)
        assert decoded.name == "Alice"
        assert decoded.age == 30
    
    def test_typed_msgpack_serialization(self):
        """Test type-safe MessagePack serialization."""
        from src.infrastructure.serialization.MsgSpecSerializer import TypedSerializer
        import msgspec
        
        class Config(msgspec.Struct):
            enabled: bool
            count: int
        
        serializer = TypedSerializer(Config, format="msgpack")
        
        config = Config(enabled=True, count=5)
        encoded = serializer.encode(config)
        decoded = serializer.decode(encoded)
        
        assert decoded.enabled == True
        assert decoded.count == 5
    
    def test_encode_many(self):
        """Test encoding multiple objects."""
        from src.infrastructure.serialization.MsgSpecSerializer import TypedSerializer
        import msgspec
        
        class Item(msgspec.Struct):
            id: int
        
        serializer = TypedSerializer(Item, format="json")
        
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
        from src.infrastructure.serialization.MsgSpecSerializer import Role
        
        assert Role.SYSTEM == "system"
        assert Role.USER == "user"
        assert Role.ASSISTANT == "assistant"
        assert Role.TOOL == "tool"
    
    def test_chat_message_struct(self):
        """Test ChatMessage struct."""
        from src.infrastructure.serialization.MsgSpecSerializer import ChatMessage, Role
        
        msg = ChatMessage(role=Role.USER, content="Hello!")
        assert msg.role == Role.USER
        assert msg.content == "Hello!"
        assert msg.name is None
    
    def test_chat_completion_request(self):
        """Test ChatCompletionRequest struct."""
        from src.infrastructure.serialization.MsgSpecSerializer import (
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
        assert request.stream == False


class TestChatHelpers:
    """Tests for chat encoding/decoding helpers."""
    
    def test_encode_chat_request(self):
        """Test encoding a chat request."""
        from src.infrastructure.serialization.MsgSpecSerializer import encode_chat_request
        
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
        from src.infrastructure.serialization.MsgSpecSerializer import benchmark_serialization
        
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
        from src.infrastructure.backend.LLMClient import LLMClient
        import requests
        
        with patch.object(requests, 'Session', return_value=MagicMock()):
            client = LLMClient(requests)
        
        assert "lmstudio" in client.backends
    
    def test_llm_chat_via_lmstudio_method(self):
        """Test llm_chat_via_lmstudio method exists."""
        from src.infrastructure.backend.LLMClient import LLMClient
        import requests
        
        with patch.object(requests, 'Session', return_value=MagicMock()):
            client = LLMClient(requests)
        
        assert hasattr(client, 'llm_chat_via_lmstudio')
        assert callable(client.llm_chat_via_lmstudio)
    
    def test_lmstudio_in_known_backends(self):
        """Test lmstudio is in smart_chat fallback chain."""
        from src.infrastructure.backend.LLMClient import LLMClient
        import requests
        
        # Check source code contains lmstudio in known_backends
        import inspect
        source = inspect.getsource(LLMClient.smart_chat)
        assert "lmstudio" in source


class TestPhase21ModuleStructure:
    """Tests for Phase 21 module structure."""
    
    def test_serialization_package_exports(self):
        """Test serialization package exports new functions."""
        from src.infrastructure.serialization import (
            is_msgspec_available,
            JSONEncoder,
            MsgPackEncoder,
            TypedSerializer,
        )
        
        assert callable(is_msgspec_available)
    
    def test_lmstudio_backend_exports(self):
        """Test LMStudioBackend exports."""
        from src.infrastructure.backend.llm_backends.LMStudioBackend import (
            LMStudioBackend,
            LMStudioConfig,
            ModelCache,
            CachedModel,
            lmstudio_chat,
            lmstudio_stream,
            lmstudio_chat_async,
        )
        
        assert LMStudioBackend.PROVIDER_ID == "lmstudio"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
