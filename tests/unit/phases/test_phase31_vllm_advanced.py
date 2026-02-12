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
Phase 31 Tests: Advanced vLLM Integration

Tests for AsyncVllmEngine, StreamingEngine, LoraManager, and GuidedDecoder.
"""

import pytest


# ============================================================================
# AsyncVllmEngine Tests
# ============================================================================

class TestAsyncEngineConfig:
    """Tests for AsyncEngineConfig."""

    def test_default_config(self):
        from src.infrastructure.compute.backend.vllm_advanced.async_vllm_engine import AsyncEngineConfig

        config = AsyncEngineConfig()

        assert config.model == "meta-llama/Llama-3-8B-Instruct"
        assert config.tensor_parallel_size == 1
        assert config.gpu_memory_utilization == 0.85
        assert config.enable_prefix_caching is True

    def test_custom_config(self):
        from src.infrastructure.compute.backend.vllm_advanced.async_vllm_engine import AsyncEngineConfig

        config = AsyncEngineConfig(
            model="custom-model",
            tensor_parallel_size=2,
            max_num_seqs=512,
        )

        assert config.model == "custom-model"
        assert config.tensor_parallel_size == 2
        assert config.max_num_seqs == 512


class TestRequestState:
    """Tests for RequestState enum."""

    def test_request_states(self):
        from src.infrastructure.compute.backend.vllm_advanced.async_vllm_engine import RequestState

        assert RequestState.PENDING.name == "PENDING"
        assert RequestState.RUNNING.name == "RUNNING"
        assert RequestState.STREAMING.name == "STREAMING"
        assert RequestState.COMPLETED.name == "COMPLETED"
        assert RequestState.FAILED.name == "FAILED"
        assert RequestState.ABORTED.name == "ABORTED"


class TestAsyncRequestHandle:
    """Tests for AsyncRequestHandle."""

    def test_handle_creation(self):
        from src.infrastructure.compute.backend.vllm_advanced.async_vllm_engine import (
            AsyncRequestHandle, RequestState
        )

        handle = AsyncRequestHandle(
            request_id="test-123",
            prompt="Hello world",
        )

        assert handle.request_id == "test-123"
        assert handle.prompt == "Hello world"
        assert handle.state == RequestState.PENDING
        assert not handle.is_finished

    def test_handle_finished_states(self):
        from src.infrastructure.compute.backend.vllm_advanced.async_vllm_engine import (
            AsyncRequestHandle, RequestState
        )

        handle = AsyncRequestHandle(request_id="test", prompt="")

        handle.state = RequestState.COMPLETED
        assert handle.is_finished

        handle.state = RequestState.FAILED
        assert handle.is_finished

        handle.state = RequestState.ABORTED
        assert handle.is_finished

        handle.state = RequestState.RUNNING
        assert not handle.is_finished

    def test_handle_metrics(self):
        from src.infrastructure.compute.backend.vllm_advanced.async_vllm_engine import AsyncRequestHandle

        handle = AsyncRequestHandle(
            request_id="test",
            prompt="",
            started_at=1000.0,
            completed_at=1001.0,
            generated_tokens=100,
        )

        assert handle.latency_ms == 1000.0
        assert handle.tokens_per_second == 100.0


class TestAsyncVllmEngine:
    """Tests for AsyncVllmEngine."""

    def test_engine_creation(self):
        from src.infrastructure.compute.backend.vllm_advanced.async_vllm_engine import AsyncVllmEngine

        engine = AsyncVllmEngine()

        assert not engine.is_running
        assert engine._requests == {}

    def test_engine_singleton(self):
        from src.infrastructure.compute.backend.vllm_advanced.async_vllm_engine import (
            AsyncVllmEngine
        )

        # Reset singleton
        AsyncVllmEngine._instance = None

        engine1 = AsyncVllmEngine.get_instance()
        engine2 = AsyncVllmEngine.get_instance()

        assert engine1 is engine2

    def test_generate_request_id(self):
        from src.infrastructure.compute.backend.vllm_advanced.async_vllm_engine import AsyncVllmEngine

        engine = AsyncVllmEngine()

        id1 = engine._generate_request_id()
        id2 = engine._generate_request_id()

        assert id1.startswith("req-")
        assert id2.startswith("req-")
        assert id1 != id2

    def test_get_stats(self):
        from src.infrastructure.compute.backend.vllm_advanced.async_vllm_engine import AsyncVllmEngine

        engine = AsyncVllmEngine()
        stats = engine.get_stats()

        assert "total_requests" in stats
        assert "completed_requests" in stats
        assert "is_running" in stats


# ============================================================================
# StreamingEngine Tests
# ============================================================================

class TestStreamingConfig:
    """Tests for StreamingConfig."""

    def test_default_config(self):
        from src.infrastructure.compute.backend.vllm_advanced.streaming_engine import StreamingConfig

        config = StreamingConfig()

        assert config.model == "meta-llama/Llama-3-8B-Instruct"
        assert config.min_tokens_per_yield == 1
        assert config.skip_special_tokens is True


class TestStreamToken:
    """Tests for StreamToken."""

    def test_token_creation(self):
        from src.infrastructure.compute.backend.vllm_advanced.streaming_engine import StreamToken

        token = StreamToken(
            text="Hello",
            token_id=100,
            index=0,
        )

        assert token.text == "Hello"
        assert token.token_id == 100
        assert token.index == 0
        assert not token.is_special


class TestTokenStreamIterator:
    """Tests for TokenStreamIterator."""

    @pytest.mark.asyncio
    async def test_iterator_put_and_get(self):
        from src.infrastructure.compute.backend.vllm_advanced.streaming_engine import (
            TokenStreamIterator, StreamToken
        )

        iterator = TokenStreamIterator()

        # Put tokens
        await iterator.put(StreamToken("Hello", 1, 0))
        await iterator.put(StreamToken(" ", 2, 1))
        await iterator.put(StreamToken("World", 3, 2))
        await iterator.finish()

        # Get tokens
        tokens = []
        async for token in iterator:
            tokens.append(token)

        assert len(tokens) == 3
        assert tokens[0].text == "Hello"
        assert tokens[2].text == "World"

    @pytest.mark.asyncio
    async def test_iterator_get_full_text(self):
        from src.infrastructure.compute.backend.vllm_advanced.streaming_engine import (
            TokenStreamIterator, StreamToken
        )

        iterator = TokenStreamIterator()

        await iterator.put(StreamToken("Hello", 1, 0))
        await iterator.put(StreamToken(" ", 2, 1))
        await iterator.put(StreamToken("World", 3, 2))

        assert iterator.get_full_text() == "Hello World"

    @pytest.mark.asyncio
    async def test_iterator_error_handling(self):
        from src.infrastructure.compute.backend.vllm_advanced.streaming_engine import TokenStreamIterator

        iterator = TokenStreamIterator()

        test_error = RuntimeError("Test error")
        await iterator.error(test_error)

        with pytest.raises(RuntimeError, match="Test error"):
            async for _ in iterator:
                pass


class TestStreamingVllmEngine:
    """Tests for StreamingVllmEngine."""

    def test_engine_creation(self):
        from src.infrastructure.compute.backend.vllm_advanced.streaming_engine import StreamingVllmEngine

        engine = StreamingVllmEngine()

        assert not engine._initialized
        assert engine._llm is None

    def test_engine_singleton(self):
        from src.infrastructure.compute.backend.vllm_advanced.streaming_engine import StreamingVllmEngine

        StreamingVllmEngine._instance = None

        engine1 = StreamingVllmEngine.get_instance()
        engine2 = StreamingVllmEngine.get_instance()

        assert engine1 is engine2

    def test_get_stats(self):
        from src.infrastructure.compute.backend.vllm_advanced.streaming_engine import StreamingVllmEngine

        engine = StreamingVllmEngine()
        stats = engine.get_stats()

        assert "total_streams" in stats
        assert "total_tokens_streamed" in stats
        assert "is_initialized" in stats


# ============================================================================
# LoraManager Tests
# ============================================================================

class TestLoraConfig:
    """Tests for LoraConfig."""

    def test_default_config(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraConfig

        config = LoraConfig()

        assert config.max_lora_rank == 64
        assert config.max_loras == 4
        assert config.cache_enabled is True


class TestLoraAdapter:
    """Tests for LoraAdapter."""

    def test_adapter_creation(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraAdapter, AdapterState

        adapter = LoraAdapter(
            adapter_id=1,
            name="code-assistant",
            path="/path/to/adapter",
        )

        assert adapter.adapter_id == 1
        assert adapter.name == "code-assistant"
        assert adapter.state == AdapterState.UNLOADED

    def test_adapter_hash(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraAdapter

        adapter = LoraAdapter(
            adapter_id=1,
            name="test",
            path="/path",
        )

        hash1 = adapter.hash
        hash2 = adapter.hash

        assert hash1 == hash2
        assert len(hash1) == 12

    def test_adapter_mark_used(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraAdapter

        adapter = LoraAdapter(adapter_id=1, name="test", path="/path")

        initial_count = adapter.load_count
        adapter.mark_used()

        assert adapter.load_count == initial_count + 1
        assert adapter.last_used is not None


class TestLoraRegistry:
    """Tests for LoraRegistry."""

    def test_registry_creation(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraRegistry

        registry = LoraRegistry()

        assert len(registry.list_adapters()) == 0

    def test_register_adapter(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraRegistry

        registry = LoraRegistry()

        adapter = registry.register("test-adapter", "/path/to/adapter", rank=32)

        assert adapter.name == "test-adapter"
        assert adapter.adapter_id == 1
        assert adapter.rank == 32
        assert len(registry.list_adapters()) == 1

    def test_register_duplicate(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraRegistry

        registry = LoraRegistry()

        adapter1 = registry.register("test", "/path1")
        adapter2 = registry.register("test", "/path2")

        assert adapter1 is adapter2
        assert adapter2.path == "/path2"

    def test_unregister_adapter(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraRegistry

        registry = LoraRegistry()

        registry.register("test", "/path")
        assert len(registry.list_adapters()) == 1

        result = registry.unregister("test")

        assert result is True
        assert len(registry.list_adapters()) == 0

    def test_get_adapter(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraRegistry

        registry = LoraRegistry()
        registry.register("test", "/path")

        adapter = registry.get("test")

        assert adapter is not None
        assert adapter.name == "test"

        missing = registry.get("nonexistent")
        assert missing is None

    def test_find_by_base_model(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraRegistry

        registry = LoraRegistry()

        registry.register("adapter1", "/path1", base_model="llama-3")
        registry.register("adapter2", "/path2", base_model="llama-3")
        registry.register("adapter3", "/path3", base_model="mistral")

        llama_adapters = registry.find_by_base_model("llama-3")

        assert len(llama_adapters) == 2


class TestLoraManager:
    """Tests for LoraManager."""

    def test_manager_creation(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraManager

        manager = LoraManager()

        assert len(manager._active_adapters) == 0
        assert len(manager._lru_cache) == 0

    def test_register_and_get(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraManager

        manager = LoraManager()

        adapter = manager.register_adapter("test", "/path")
        retrieved = manager.get_adapter("test")

        assert adapter is retrieved

    def test_activate_adapter(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraManager, AdapterState

        manager = LoraManager()
        manager.register_adapter("test", "/path")

        result = manager.activate("test")

        assert result is True
        assert "test" in manager._active_adapters

        adapter = manager.get_adapter("test")
        assert adapter.state == AdapterState.ACTIVE

    def test_activate_nonexistent(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraManager

        manager = LoraManager()

        result = manager.activate("nonexistent")

        assert result is False

    def test_deactivate_adapter(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraManager, AdapterState

        manager = LoraManager()
        manager.register_adapter("test", "/path")
        manager.activate("test")

        result = manager.deactivate("test")

        assert result is True
        assert "test" not in manager._active_adapters

        adapter = manager.get_adapter("test")
        assert adapter.state == AdapterState.LOADED

    def test_lru_eviction(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraManager, LoraConfig

        config = LoraConfig(max_loras=2)
        manager = LoraManager(config=config)

        manager.register_adapter("adapter1", "/path1")
        manager.register_adapter("adapter2", "/path2")
        manager.register_adapter("adapter3", "/path3")

        manager.activate("adapter1")
        manager.activate("adapter2")

        # This should evict adapter1 (LRU)
        manager.activate("adapter3")

        assert "adapter3" in manager._active_adapters
        assert "adapter2" in manager._active_adapters
        assert "adapter1" not in manager._active_adapters

    def test_get_stats(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraManager

        manager = LoraManager()
        stats = manager.get_stats()

        assert "active_count" in stats
        assert "registered_count" in stats
        assert "hit_rate" in stats

    def test_list_adapters(self):
        from src.infrastructure.compute.backend.vllm_advanced.lora_manager import LoraManager

        manager = LoraManager()
        manager.register_adapter("adapter1", "/path1")
        manager.register_adapter("adapter2", "/path2")
        manager.activate("adapter1")

        adapters = manager.list_adapters()

        assert len(adapters) == 2

        active = [a for a in adapters if a["is_active"]]
        assert len(active) == 1
        assert active[0]["name"] == "adapter1"


# ============================================================================
# GuidedDecoder Tests
# ============================================================================

class TestGuidedMode:
    """Tests for GuidedMode enum."""

    def test_modes(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import GuidedMode

        assert GuidedMode.NONE.name == "NONE"
        assert GuidedMode.JSON.name == "JSON"
        assert GuidedMode.REGEX.name == "REGEX"
        assert GuidedMode.CHOICE.name == "CHOICE"


class TestGuidedConfig:
    """Tests for GuidedConfig."""

    def test_default_config(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import GuidedConfig, GuidedMode

        config = GuidedConfig()

        assert config.mode == GuidedMode.NONE
        assert config.json_schema is None

    def test_json_mode_kwargs(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import GuidedConfig, GuidedMode

        schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        config = GuidedConfig(mode=GuidedMode.JSON, json_schema=schema)

        kwargs = config.to_sampling_params_kwargs()

        assert "guided_json" in kwargs
        assert kwargs["guided_json"] == schema

    def test_regex_mode_kwargs(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import GuidedConfig, GuidedMode

        config = GuidedConfig(mode=GuidedMode.REGEX, regex_pattern=r"\d{3}-\d{4}")

        kwargs = config.to_sampling_params_kwargs()

        assert "guided_regex" in kwargs
        assert kwargs["guided_regex"] == r"\d{3}-\d{4}"

    def test_choice_mode_kwargs(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import GuidedConfig, GuidedMode

        config = GuidedConfig(mode=GuidedMode.CHOICE, choices=["yes", "no"])

        kwargs = config.to_sampling_params_kwargs()

        assert "guided_choice" in kwargs
        assert kwargs["guided_choice"] == ["yes", "no"]


class TestJsonSchema:
    """Tests for JsonSchema builder."""

    def test_basic_schema(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import JsonSchema

        schema = JsonSchema(title="Person", description="A person object")

        result = schema.build()

        assert result["type"] == "object"
        assert result["title"] == "Person"
        assert result["description"] == "A person object"

    def test_add_string_property(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import JsonSchema

        schema = JsonSchema().add_string("name", required=True, min_length=1)

        result = schema.build()

        assert "name" in result["properties"]
        assert result["properties"]["name"]["type"] == "string"
        assert result["properties"]["name"]["minLength"] == 1
        assert "name" in result["required"]

    def test_add_integer_property(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import JsonSchema

        schema = JsonSchema().add_integer("age", required=True, minimum=0, maximum=150)

        result = schema.build()

        assert result["properties"]["age"]["type"] == "integer"
        assert result["properties"]["age"]["minimum"] == 0
        assert result["properties"]["age"]["maximum"] == 150

    def test_add_array_property(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import JsonSchema

        schema = JsonSchema().add_array("tags", items_type="string", max_items=10)

        result = schema.build()

        assert result["properties"]["tags"]["type"] == "array"
        assert result["properties"]["tags"]["items"]["type"] == "string"
        assert result["properties"]["tags"]["maxItems"] == 10

    def test_add_enum_property(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import JsonSchema

        schema = JsonSchema().add_enum("status", ["active", "inactive", "pending"])

        result = schema.build()

        assert result["properties"]["status"]["enum"] == ["active", "inactive", "pending"]

    def test_fluent_api(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import JsonSchema

        schema = (JsonSchema()
                  .add_string("name", required=True)
                  .add_integer("age", minimum=0)
                  .add_array("tags")
                  .add_boolean("active")
                  .build())

        assert len(schema["properties"]) == 4
        assert "name" in schema["required"]

    def test_to_guided_config(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import JsonSchema, GuidedMode

        schema = JsonSchema().add_string("test")
        config = schema.to_guided_config()

        assert config.mode == GuidedMode.JSON
        assert config.json_schema is not None


class TestRegexPattern:
    """Tests for RegexPattern builder."""

    def test_pattern_creation(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import RegexPattern

        pattern = RegexPattern(pattern=r"\d+", name="digits")

        assert pattern.pattern == r"\d+"
        assert pattern.name == "digits"

    def test_invalid_pattern(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import RegexPattern

        with pytest.raises(ValueError, match="Invalid regex"):
            RegexPattern(pattern=r"[invalid")

    def test_predefined_patterns(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import RegexPattern

        assert RegexPattern.EMAIL
        assert RegexPattern.URL
        assert RegexPattern.DATE_ISO
        assert RegexPattern.UUID

    def test_factory_methods(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import RegexPattern

        email = RegexPattern.email()
        assert email.name == "email"

        date = RegexPattern.date_iso()
        assert date.name == "date_iso"

    def test_one_of(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import RegexPattern

        pattern = RegexPattern.one_of(r"\d+", r"[a-z]+")

        assert "|" in pattern.pattern

    def test_to_guided_config(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import RegexPattern, GuidedMode

        pattern = RegexPattern(pattern=r"\d+")
        config = pattern.to_guided_config()

        assert config.mode == GuidedMode.REGEX
        assert config.regex_pattern == r"\d+"


class TestChoiceConstraint:
    """Tests for ChoiceConstraint."""

    def test_constraint_creation(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import ChoiceConstraint

        constraint = ChoiceConstraint(choices=["a", "b", "c"])

        assert constraint.choices == ["a", "b", "c"]

    def test_empty_choices_error(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import ChoiceConstraint

        with pytest.raises(ValueError, match="At least one choice"):
            ChoiceConstraint(choices=[])

    def test_factory_methods(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import ChoiceConstraint

        yes_no = ChoiceConstraint.yes_no()
        assert yes_no.choices == ["yes", "no"]

        sentiment = ChoiceConstraint.sentiment()
        assert "positive" in sentiment.choices
        assert "negative" in sentiment.choices

        rating = ChoiceConstraint.rating(1, 5)
        assert rating.choices == ["1", "2", "3", "4", "5"]

    def test_to_guided_config(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import ChoiceConstraint, GuidedMode

        constraint = ChoiceConstraint(["a", "b"])
        config = constraint.to_guided_config()

        assert config.mode == GuidedMode.CHOICE
        assert config.choices == ["a", "b"]


class TestGuidedDecoder:
    """Tests for GuidedDecoder main class."""

    def test_decoder_creation(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import GuidedDecoder

        decoder = GuidedDecoder(model="test-model")

        assert decoder.model == "test-model"
        assert not decoder._initialized

    def test_decoder_singleton(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import GuidedDecoder

        GuidedDecoder._instance = None

        decoder1 = GuidedDecoder.get_instance(model="test")
        decoder2 = GuidedDecoder.get_instance()

        assert decoder1 is decoder2

    def test_get_stats(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import GuidedDecoder

        decoder = GuidedDecoder()
        stats = decoder.get_stats()

        assert "json_generations" in stats
        assert "regex_generations" in stats
        assert "choice_generations" in stats
        assert "validation_failures" in stats


# ============================================================================
# Integration Tests
# ============================================================================

class TestModuleImports:
    """Test that all modules can be imported correctly."""

    def test_import_async_engine(self):
        from src.infrastructure.compute.backend.vllm_advanced import (
            AsyncVllmEngine,
            AsyncEngineConfig,
        )

        assert AsyncVllmEngine is not None
        assert AsyncEngineConfig is not None

    def test_import_streaming(self):
        from src.infrastructure.compute.backend.vllm_advanced import (
            StreamingVllmEngine,
            TokenStreamIterator,
        )

        assert StreamingVllmEngine is not None
        assert TokenStreamIterator is not None

    def test_import_lora(self):
        from src.infrastructure.compute.backend.vllm_advanced import (
            LoraManager,
            LoraRegistry,
        )

        assert LoraManager is not None
        assert LoraRegistry is not None

    def test_import_guided(self):
        from src.infrastructure.compute.backend.vllm_advanced import (
            GuidedDecoder,
            JsonSchema,
        )

        assert GuidedDecoder is not None
        assert JsonSchema is not None


class TestVllmNativeEngineAdvanced:
    """Test VllmNativeEngine with advanced features."""

    def test_generate_signature(self):
        from src.infrastructure.compute.backend.vllm_native_engine import VllmNativeEngine

        engine = VllmNativeEngine()

        # Check that generate accepts new parameters
        import inspect
        sig = inspect.signature(engine.generate)
        params = list(sig.parameters.keys())

        assert "lora_request" in params
        assert "guided_json" in params
        assert "guided_regex" in params
        assert "guided_choice" in params

    def test_generate_json_method(self):
        from src.infrastructure.compute.backend.vllm_native_engine import VllmNativeEngine

        engine = VllmNativeEngine()

        assert hasattr(engine, "generate_json")
        assert callable(engine.generate_json)

    def test_generate_choice_method(self):
        from src.infrastructure.compute.backend.vllm_native_engine import VllmNativeEngine

        engine = VllmNativeEngine()

        assert hasattr(engine, "generate_choice")
        assert callable(engine.generate_choice)

    def test_generate_regex_method(self):
        from src.infrastructure.compute.backend.vllm_native_engine import VllmNativeEngine

        engine = VllmNativeEngine()

        assert hasattr(engine, "generate_regex")
        assert callable(engine.generate_regex)


class TestEndToEndSchemaBuilding:
    """End-to-end tests for schema building workflows."""

    def test_complex_schema_building(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import JsonSchema

        # Build a complex person schema
        address_schema = (JsonSchema()
                          .add_string("street", required=True)
                          .add_string("city", required=True)
                          .add_string("zip", pattern=r"^\d{5}$"))

        person_schema = (JsonSchema(title="Person")
                         .add_string("name", required=True, min_length=1, max_length=100)
                         .add_integer("age", minimum=0, maximum=150)
                         .add_string("email", pattern=r"^[\w.-]+@[\w.-]+\.\w+$")
                         .add_array("tags", items_type="string", max_items=10)
                         .add_enum("status", ["active", "inactive"])
                         .add_object("address", address_schema))

        result = person_schema.build()

        assert result["title"] == "Person"
        assert len(result["properties"]) == 6
        assert "address" in result["properties"]
        assert result["properties"]["address"]["properties"]["city"]["type"] == "string"

    def test_config_chaining(self):
        from src.infrastructure.compute.backend.vllm_advanced.guided_decoder import (
            JsonSchema, RegexPattern, ChoiceConstraint
        )

        # Test that all builders can convert to GuidedConfig
        json_config = JsonSchema().add_string("test").to_guided_config()
        regex_config = RegexPattern.email().to_guided_config()
        choice_config = ChoiceConstraint.yes_no().to_guided_config()

        assert json_config.json_schema is not None
        assert regex_config.regex_pattern is not None
        assert choice_config.choices is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
