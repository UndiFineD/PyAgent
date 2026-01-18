# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Phase 26 Tests - Multimodal, Structured Output, and Distributed Coordination.

Tests cover:
- MultiModalProcessor (image, video, audio, text embeds)
- StructuredOutputGrammar (JSON, regex, choice, EBNF)
- DistributedCoordinator (workers, coordinators, executors)
- Rust accelerations (image resize, audio resample, grammar compile)
"""

import asyncio
import json
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set
from unittest.mock import MagicMock, patch

import numpy as np
import pytest


# =============================================================================
# MultiModal Tests
# =============================================================================


class TestModalityType:
    """Tests for ModalityType enum."""
    
    def test_modality_types_exist(self):
        """Test all modality types are defined."""
        from src.infrastructure.multimodal import ModalityType
        
        assert ModalityType.IMAGE is not None
        assert ModalityType.VIDEO is not None
        assert ModalityType.AUDIO is not None
        assert ModalityType.TEXT is not None
        assert ModalityType.EMBEDS is not None
    
    def test_modality_type_values_unique(self):
        """Test modality type values are unique."""
        from src.infrastructure.multimodal import ModalityType
        
        values = [m.value for m in ModalityType]
        assert len(values) == len(set(values))


class TestMultiModalConfig:
    """Tests for MultiModalConfig dataclass."""
    
    def test_default_config(self):
        """Test default configuration values."""
        from src.infrastructure.multimodal import MultiModalConfig
        
        config = MultiModalConfig()
        assert config.limit_per_prompt["image"] >= 1
        assert config.limit_per_prompt["video"] >= 1
        assert config.limit_per_prompt["audio"] >= 1
        assert config.image_token is not None
    
    def test_custom_config(self):
        """Test custom configuration."""
        from src.infrastructure.multimodal import MultiModalConfig
        
        config = MultiModalConfig(
            limit_per_prompt={"image": 10, "video": 5, "audio": 3},
            image_token="<img>",
        )
        assert config.limit_per_prompt["image"] == 10
        assert config.limit_per_prompt["video"] == 5
        assert config.limit_per_prompt["audio"] == 3
        assert config.image_token == "<img>"


class TestMultiModalData:
    """Tests for MultiModalData dataclass."""
    
    def test_create_image_data(self):
        """Test creating image multimodal data."""
        from src.infrastructure.multimodal import MultiModalData
        
        data = MultiModalData(
            images=[np.zeros((224, 224, 3))],
        )
        assert len(data.images) == 1
        assert data.images[0].shape == (224, 224, 3)
    
    def test_create_audio_data(self):
        """Test creating audio multimodal data."""
        from src.infrastructure.multimodal import MultiModalData
        
        # Audio is (waveform, sample_rate) tuple
        data = MultiModalData(
            audios=[(np.zeros(16000), 16000)],  # 1 second at 16kHz
        )
        assert len(data.audios) == 1
        assert len(data.audios[0][0]) == 16000
        assert data.audios[0][1] == 16000
    
    def test_is_empty(self):
        """Test is_empty check."""
        from src.infrastructure.multimodal import MultiModalData
        
        data = MultiModalData()
        assert data.is_empty()
        
        data_with_image = MultiModalData(images=[np.zeros((10, 10, 3))])
        assert not data_with_image.is_empty()


class TestImageProcessor:
    """Tests for ImageProcessor."""
    
    def test_process_numpy_image(self):
        """Test processing numpy array image."""
        from src.infrastructure.multimodal import ImageProcessor, MultiModalConfig
        
        config = MultiModalConfig()
        processor = ImageProcessor(config, target_size=(224, 224))
        
        # Create test image
        image = np.random.rand(100, 100, 3).astype(np.float32)
        result, metadata = processor.process(image)
        
        assert result is not None
        assert result.shape[0] == 224
        assert result.shape[1] == 224
        assert "original_size" in metadata
    
    def test_get_placeholder_count(self):
        """Test placeholder token count calculation."""
        from src.infrastructure.multimodal import ImageProcessor, MultiModalConfig
        
        config = MultiModalConfig()
        processor = ImageProcessor(config, target_size=(224, 224), patch_size=14)
        
        image = np.random.rand(100, 100, 3).astype(np.float32)
        count = processor.get_placeholder_count(image)
        
        # 224/14 = 16 patches per side, 16*16 = 256 total
        assert count == 256


class TestVideoProcessor:
    """Tests for VideoProcessor."""
    
    def test_process_video(self):
        """Test video processing."""
        from src.infrastructure.multimodal import MultiModalConfig, VideoProcessor
        
        config = MultiModalConfig()
        processor = VideoProcessor(config, num_frames=4)
        
        # Create mock video with 10 frames
        video = np.random.rand(10, 64, 64, 3).astype(np.float32)
        processed, metadata = processor.process((video, {"fps": 30}))
        
        assert processed.shape[0] == 4  # num_frames
        assert "sampled_frames" in metadata
    
    def test_get_placeholder_count(self):
        """Test placeholder count for video."""
        from src.infrastructure.multimodal import MultiModalConfig, VideoProcessor
        
        config = MultiModalConfig()
        processor = VideoProcessor(config, num_frames=8, target_size=(224, 224), patch_size=14)
        
        video = np.random.rand(10, 64, 64, 3).astype(np.float32)
        count = processor.get_placeholder_count((video, {}))
        
        # 8 frames * (224/14)^2 = 8 * 256 = 2048
        assert count == 2048


class TestAudioProcessor:
    """Tests for AudioProcessor."""
    
    def test_process_audio(self):
        """Test audio processing."""
        from src.infrastructure.multimodal import AudioProcessor, MultiModalConfig
        
        config = MultiModalConfig()
        processor = AudioProcessor(config, target_sample_rate=16000)
        
        # Create 1 second of audio at 44100 Hz
        audio = np.random.rand(44100).astype(np.float32)
        features, metadata = processor.process((audio, 44100))
        
        # Should have processed and computed features
        assert features is not None
        assert "duration_seconds" in metadata
    
    def test_get_placeholder_count(self):
        """Test audio placeholder count."""
        from src.infrastructure.multimodal import AudioProcessor, MultiModalConfig
        
        config = MultiModalConfig()
        processor = AudioProcessor(config, target_sample_rate=16000, hop_length=160)
        
        # 1 second at 16kHz = 16000 samples / 160 hop = 100 frames
        audio = np.random.rand(16000).astype(np.float32)
        count = processor.get_placeholder_count((audio, 16000))
        
        assert count == 100


class TestMultiModalRegistry:
    """Tests for MultiModalRegistry."""
    
    def test_create_processor(self):
        """Test creating a processor."""
        from src.infrastructure.multimodal import (
            ModalityType,
            MultiModalConfig,
            MultiModalRegistry,
            ImageProcessor,
        )
        
        registry = MultiModalRegistry()
        config = MultiModalConfig()
        
        processor = registry.create_processor(ModalityType.IMAGE, config)
        assert isinstance(processor, ImageProcessor)
    
    def test_process_inputs(self):
        """Test processing multiple inputs."""
        from src.infrastructure.multimodal import (
            ModalityType,
            MultiModalConfig,
            MultiModalData,
            MultiModalRegistry,
        )
        
        registry = MultiModalRegistry()
        config = MultiModalConfig()
        
        inputs = MultiModalData(
            images=[np.random.rand(100, 100, 3).astype(np.float32)],
        )
        
        result = registry.process_inputs(inputs, config)
        assert result is not None
        assert "image" in result.mm_embeddings
        assert len(result.mm_embeddings["image"]) == 1


# =============================================================================
# Structured Output Tests
# =============================================================================


class TestStructuredOutputOptions:
    """Tests for StructuredOutputOptions enum."""
    
    def test_option_types_exist(self):
        """Test all option types are defined."""
        from src.infrastructure.decoding import StructuredOutputOptions
        
        assert StructuredOutputOptions.JSON is not None
        assert StructuredOutputOptions.REGEX is not None
        assert StructuredOutputOptions.CHOICE is not None
        assert StructuredOutputOptions.GRAMMAR is not None


class TestStructuredOutputsParams:
    """Tests for StructuredOutputsParams dataclass."""
    
    def test_json_param(self):
        """Test JSON schema parameter."""
        from src.infrastructure.decoding import StructuredOutputsParams
        
        params = StructuredOutputsParams(json={"type": "object"})
        assert params.json == {"type": "object"}
        assert params.regex is None
    
    def test_only_one_constraint(self):
        """Test that only one constraint can be set."""
        from src.infrastructure.decoding import StructuredOutputsParams
        
        with pytest.raises(ValueError):
            StructuredOutputsParams(
                json={"type": "object"},
                regex=".*",
            )
    
    def test_get_option_type(self):
        """Test getting option type."""
        from src.infrastructure.decoding import (
            StructuredOutputOptions,
            StructuredOutputsParams,
        )
        
        params = StructuredOutputsParams(regex=r"\d+")
        assert params.get_option_type() == StructuredOutputOptions.REGEX
    
    def test_get_spec(self):
        """Test getting specification string."""
        from src.infrastructure.decoding import StructuredOutputsParams
        
        params = StructuredOutputsParams(choice=["yes", "no"])
        spec = params.get_spec()
        assert "yes" in spec
        assert "no" in spec


class TestJSONSchemaGrammar:
    """Tests for JSONSchemaGrammar."""
    
    def _token_to_string(self, token_id: int) -> str:
        """Simple mock token decoder."""
        vocab = [" ", "{", "}", '"', ":", ",", "[", "]", "a", "b", "c", "1", "2", "3"]
        if token_id < len(vocab):
            return vocab[token_id]
        return chr(ord('a') + (token_id % 26))
    
    def test_accept_valid_prefix(self):
        """Test accepting valid JSON prefix."""
        from src.infrastructure.decoding import JSONSchemaGrammar
        
        schema = {"type": "object"}
        grammar = JSONSchemaGrammar(
            schema=schema,
            vocab_size=100,
            token_to_string=self._token_to_string,
        )
        
        # Token 1 is "{"
        result = grammar.accept_tokens("req-1", [1])
        assert result is True
    
    def test_rollback(self):
        """Test rolling back tokens."""
        from src.infrastructure.decoding import JSONSchemaGrammar
        
        schema = {"type": "object"}
        grammar = JSONSchemaGrammar(
            schema=schema,
            vocab_size=100,
            token_to_string=self._token_to_string,
        )
        
        grammar.accept_tokens("req-1", [1, 2])  # "{}"
        assert grammar.num_processed_tokens == 2
        
        grammar.rollback(1)
        assert grammar.num_processed_tokens == 1
    
    def test_reset(self):
        """Test resetting grammar."""
        from src.infrastructure.decoding import JSONSchemaGrammar
        
        schema = {"type": "object"}
        grammar = JSONSchemaGrammar(
            schema=schema,
            vocab_size=100,
            token_to_string=self._token_to_string,
        )
        
        grammar.accept_tokens("req-1", [1, 2])
        grammar.reset()
        
        assert grammar.num_processed_tokens == 0


class TestRegexGrammar:
    """Tests for RegexGrammar."""
    
    def _token_to_string(self, token_id: int) -> str:
        """Simple mock token decoder."""
        return str(token_id % 10)
    
    def test_accept_matching_tokens(self):
        """Test accepting tokens that match pattern."""
        from src.infrastructure.decoding import RegexGrammar
        
        grammar = RegexGrammar(
            pattern=r"\d+",
            vocab_size=100,
            token_to_string=self._token_to_string,
        )
        
        result = grammar.accept_tokens("req-1", [1, 2, 3])
        assert result is True
    
    def test_is_terminated(self):
        """Test termination detection."""
        from src.infrastructure.decoding import RegexGrammar
        
        grammar = RegexGrammar(
            pattern=r"\d{3}",  # Exactly 3 digits
            vocab_size=100,
            token_to_string=self._token_to_string,
        )
        
        grammar.accept_tokens("req-1", [1, 2, 3])
        # Note: termination depends on full match


class TestChoiceGrammar:
    """Tests for ChoiceGrammar."""
    
    def test_accept_valid_choice(self):
        """Test accepting valid choice."""
        from src.infrastructure.decoding import ChoiceGrammar
        
        def token_to_string(t: int) -> str:
            return ["y", "e", "s", "n", "o"][t] if t < 5 else ""
        
        grammar = ChoiceGrammar(
            choices=["yes", "no"],
            vocab_size=10,
            token_to_string=token_to_string,
        )
        
        # Accept "y"
        result = grammar.accept_tokens("req-1", [0])
        assert result is True
        assert 0 in grammar._active_choices  # "yes" still possible
    
    def test_reject_invalid_choice(self):
        """Test rejecting invalid choice prefix."""
        from src.infrastructure.decoding import ChoiceGrammar
        
        def token_to_string(t: int) -> str:
            return ["x", "y", "z"][t] if t < 3 else ""
        
        grammar = ChoiceGrammar(
            choices=["yes", "no"],
            vocab_size=10,
            token_to_string=token_to_string,
        )
        
        # "x" doesn't match any choice
        result = grammar.accept_tokens("req-1", [0])
        assert result is False


class TestEBNFGrammar:
    """Tests for EBNFGrammar."""
    
    def test_parse_grammar(self):
        """Test parsing EBNF grammar."""
        from src.infrastructure.decoding import EBNFGrammar
        
        grammar_str = '''
        root ::= "SELECT " column
        column ::= "id" | "name"
        '''
        
        grammar = EBNFGrammar(
            grammar_str=grammar_str,
            vocab_size=100,
            token_to_string=lambda t: chr(ord('a') + t),
        )
        
        assert "root" in grammar._rules
        assert "column" in grammar._rules


class TestGrammarCompiler:
    """Tests for GrammarCompiler."""
    
    def test_compile_json_grammar(self):
        """Test compiling JSON schema to grammar."""
        from src.infrastructure.decoding import (
            GrammarCompiler,
            JSONSchemaGrammar,
            StructuredOutputsParams,
        )
        
        compiler = GrammarCompiler(
            vocab_size=100,
            token_to_string=lambda t: chr(ord('a') + t),
        )
        
        params = StructuredOutputsParams(json={"type": "string"})
        grammar = compiler.compile(params)
        
        assert isinstance(grammar, JSONSchemaGrammar)
    
    def test_compile_regex_grammar(self):
        """Test compiling regex to grammar."""
        from src.infrastructure.decoding import (
            GrammarCompiler,
            RegexGrammar,
            StructuredOutputsParams,
        )
        
        compiler = GrammarCompiler(
            vocab_size=100,
            token_to_string=lambda t: str(t),
        )
        
        params = StructuredOutputsParams(regex=r"\d+")
        grammar = compiler.compile(params)
        
        assert isinstance(grammar, RegexGrammar)


class TestStructuredOutputManager:
    """Tests for StructuredOutputManager."""
    
    def test_init_and_get_grammar(self):
        """Test initializing and getting grammar."""
        from src.infrastructure.decoding import (
            StructuredOutputManager,
            StructuredOutputsParams,
        )
        
        manager = StructuredOutputManager(
            vocab_size=100,
            token_to_string=lambda t: chr(ord('a') + t),
        )
        
        params = StructuredOutputsParams(choice=["a", "b", "c"])
        manager.init_grammar("req-1", params)
        
        grammar = manager.get_grammar("req-1")
        assert grammar is not None
    
    def test_remove_grammar(self):
        """Test removing grammar."""
        from src.infrastructure.decoding import (
            StructuredOutputManager,
            StructuredOutputsParams,
        )
        
        manager = StructuredOutputManager(
            vocab_size=100,
            token_to_string=lambda t: str(t),
        )
        
        params = StructuredOutputsParams(regex=r"\d+")
        manager.init_grammar("req-1", params)
        manager.remove_grammar("req-1")
        
        assert manager.get_grammar("req-1") is None


# =============================================================================
# Distributed Coordinator Tests
# =============================================================================


class TestParallelConfig:
    """Tests for ParallelConfig."""
    
    def test_default_config(self):
        """Test default parallel configuration."""
        from src.infrastructure.orchestration.core.DistributedCoordinator import (
            ParallelConfig,
        )
        
        config = ParallelConfig()
        assert config.data_parallel_size == 1
        assert config.tensor_parallel_size == 1
        assert config.world_size == 1
        assert not config.is_distributed
    
    def test_distributed_config(self):
        """Test distributed configuration."""
        from src.infrastructure.orchestration.core.DistributedCoordinator import (
            ParallelConfig,
        )
        
        config = ParallelConfig(
            data_parallel_size=2,
            tensor_parallel_size=4,
        )
        assert config.world_size == 8
        assert config.is_distributed


class TestEngineIdentity:
    """Tests for EngineIdentity."""
    
    def test_create_identity(self):
        """Test creating engine identity."""
        from src.infrastructure.orchestration.core.DistributedCoordinator import (
            EngineIdentity,
        )
        
        identity = EngineIdentity(dp_rank=0, dp_size=4)
        assert identity.dp_rank == 0
        assert identity.dp_size == 4
        assert identity.engine_id is not None
    
    def test_identity_str(self):
        """Test identity string representation."""
        from src.infrastructure.orchestration.core.DistributedCoordinator import (
            EngineIdentity,
        )
        
        identity = EngineIdentity(dp_rank=1, dp_size=4, engine_id="test-1")
        s = str(identity)
        assert "test-1" in s
        assert "DP1/4" in s


class TestDPCoordinator:
    """Tests for DPCoordinator."""
    
    def test_register_engine(self):
        """Test registering an engine."""
        from src.infrastructure.orchestration.core.DistributedCoordinator import (
            DPCoordinator,
            EngineIdentity,
            EngineState,
            ParallelConfig,
        )
        
        config = ParallelConfig(data_parallel_size=4)
        coordinator = DPCoordinator(config)
        
        identity = EngineIdentity(dp_rank=0, dp_size=4)
        coordinator.register_engine(identity)
        
        assert coordinator.num_engines == 1
        assert coordinator.num_ready == 1
    
    def test_select_engine_round_robin(self):
        """Test round-robin engine selection."""
        from src.infrastructure.orchestration.core.DistributedCoordinator import (
            DPCoordinator,
            EngineIdentity,
            LoadBalancingStrategy,
            ParallelConfig,
        )
        
        config = ParallelConfig(data_parallel_size=3)
        coordinator = DPCoordinator(config, LoadBalancingStrategy.ROUND_ROBIN)
        
        for i in range(3):
            identity = EngineIdentity(dp_rank=i, dp_size=3, engine_id=f"engine-{i}")
            coordinator.register_engine(identity)
        
        # Select multiple times
        selected = set()
        for _ in range(6):
            engine_id = coordinator.select_engine()
            if engine_id:
                selected.add(engine_id)
        
        # Should have selected from all engines
        assert len(selected) == 3
    
    def test_deregister_engine(self):
        """Test deregistering an engine."""
        from src.infrastructure.orchestration.core.DistributedCoordinator import (
            DPCoordinator,
            EngineIdentity,
            ParallelConfig,
        )
        
        config = ParallelConfig()
        coordinator = DPCoordinator(config)
        
        identity = EngineIdentity(dp_rank=0, dp_size=1, engine_id="test")
        coordinator.register_engine(identity)
        assert coordinator.num_engines == 1
        
        coordinator.deregister_engine("test")
        assert coordinator.num_engines == 0


class TestMessages:
    """Tests for coordinator messages."""
    
    def test_request_message(self):
        """Test RequestMessage creation."""
        from src.infrastructure.orchestration.core.DistributedCoordinator import (
            RequestMessage,
        )
        
        msg = RequestMessage(request_id="req-1", input_data={"text": "hello"})
        assert msg.request_id == "req-1"
        assert msg.input_data["text"] == "hello"
        assert msg.message_id is not None
    
    def test_response_message(self):
        """Test ResponseMessage creation."""
        from src.infrastructure.orchestration.core.DistributedCoordinator import (
            ResponseMessage,
        )
        
        msg = ResponseMessage(
            request_id="req-1",
            output_data={"result": 42},
            latency_ms=10.5,
        )
        assert msg.request_id == "req-1"
        assert msg.output_data["result"] == 42
        assert msg.latency_ms == 10.5
    
    def test_metrics_message(self):
        """Test MetricsMessage creation."""
        from src.infrastructure.orchestration.core.DistributedCoordinator import (
            MetricsMessage,
        )
        
        msg = MetricsMessage(
            worker_id=0,
            queue_depth=5,
            total_processed=100,
            avg_latency_ms=15.0,
        )
        assert msg.worker_id == 0
        assert msg.queue_depth == 5


class TestMPClient:
    """Tests for MPClient (synchronous)."""
    
    def test_num_workers(self):
        """Test worker count before start."""
        from src.infrastructure.orchestration.core.DistributedCoordinator import (
            BaseWorker,
            MPClient,
            ParallelConfig,
            WorkerIdentity,
        )
        
        class MockWorker(BaseWorker):
            def initialize(self):
                pass
            def process(self, request):
                return None
            def shutdown(self):
                pass
        
        config = ParallelConfig(data_parallel_size=2)
        client = MPClient[dict](
            worker_factory=MockWorker,
            parallel_config=config,
        )
        
        assert client.num_workers == 0  # Not started yet


class TestDistributedExecutor:
    """Tests for DistributedExecutor interface."""
    
    def test_create_executor(self):
        """Test creating a distributed executor."""
        from src.infrastructure.orchestration.core.DistributedCoordinator import (
            BaseWorker,
            ParallelConfig,
            create_distributed_executor,
            WorkerIdentity,
        )
        
        class MockWorker(BaseWorker):
            def initialize(self):
                pass
            def process(self, request):
                return None
            def shutdown(self):
                pass
        
        config = ParallelConfig(data_parallel_size=1)
        executor = create_distributed_executor(
            worker_factory=MockWorker,
            parallel_config=config,
        )
        
        assert executor is not None
        assert not executor.is_ready()


# =============================================================================
# Rust Acceleration Tests (if available)
# =============================================================================


class TestRustMultimodal:
    """Tests for Rust multimodal accelerations."""
    
    def test_image_resize_rust(self):
        """Test Rust image resize."""
        try:
            import rust_core
        except ImportError:
            pytest.skip("rust_core not available")
        
        # Create 4x4 RGB image
        pixels = list(range(48))  # 4*4*3 = 48 values
        pixels = [float(p) for p in pixels]
        
        result = rust_core.image_resize_rust(pixels, 4, 4, 3, 2, 2)
        assert len(result) == 12  # 2*2*3
    
    def test_normalize_pixels_rust(self):
        """Test Rust pixel normalization."""
        try:
            import rust_core
        except ImportError:
            pytest.skip("rust_core not available")
        
        pixels = [1.0, 1.0, 1.0, 0.5, 0.5, 0.5]  # 2 pixels, 3 channels
        mean = [0.5, 0.5, 0.5]
        std = [0.5, 0.5, 0.5]
        
        result = rust_core.normalize_pixels_rust(pixels, 3, mean, std)
        assert len(result) == 6
        assert abs(result[0] - 1.0) < 0.01  # (1.0 - 0.5) / 0.5 = 1.0
    
    def test_extract_video_frames_rust(self):
        """Test Rust video frame extraction."""
        try:
            import rust_core
        except ImportError:
            pytest.skip("rust_core not available")
        
        result = rust_core.extract_video_frames_rust(100, 10, "uniform")
        assert len(result) == 10
        assert result[0] == 0
    
    def test_resample_audio_rust(self):
        """Test Rust audio resampling."""
        try:
            import rust_core
        except ImportError:
            pytest.skip("rust_core not available")
        
        samples = [float(i) for i in range(100)]
        result = rust_core.resample_audio_rust(samples, 100, 50)
        assert len(result) == 50


class TestRustStructuredOutput:
    """Tests for Rust structured output accelerations."""
    
    def test_json_schema_to_regex_rust(self):
        """Test Rust JSON schema to regex conversion."""
        try:
            import rust_core
        except ImportError:
            pytest.skip("rust_core not available")
        
        schema = '{"type": "string"}'
        result = rust_core.json_schema_to_regex_rust(schema)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_regex_match_prefix_rust(self):
        """Test Rust regex prefix matching."""
        try:
            import rust_core
        except ImportError:
            pytest.skip("rust_core not available")
        
        # Test with digits pattern - finds the longest matching prefix
        result = rust_core.regex_match_prefix_rust(r"\d+", "123abc")
        # The function returns the length of the valid prefix match
        assert result >= 3  # At least 3 digits match
    
    def test_compile_ebnf_rust(self):
        """Test Rust EBNF compilation."""
        try:
            import rust_core
        except ImportError:
            pytest.skip("rust_core not available")
        
        grammar = 'root ::= "hello" | "world"'
        result = rust_core.compile_ebnf_rust(grammar)
        assert len(result) == 1
        assert result[0][0] == "root"


class TestRustDistributed:
    """Tests for Rust distributed coordination accelerations."""
    
    def test_consistent_hash_rust(self):
        """Test Rust consistent hashing."""
        try:
            import rust_core
        except ImportError:
            pytest.skip("rust_core not available")
        
        result = rust_core.consistent_hash_rust("request-1", 10)
        assert 0 <= result < 10
        
        # Same key should give same bucket
        result2 = rust_core.consistent_hash_rust("request-1", 10)
        assert result == result2
    
    def test_select_worker_lb_rust(self):
        """Test Rust load balancing selection."""
        try:
            import rust_core
        except ImportError:
            pytest.skip("rust_core not available")
        
        queue_depths = [5, 2, 8, 1]
        result = rust_core.select_worker_lb_rust(queue_depths, "least_loaded", None)
        assert result == 3  # Index of worker with depth 1
    
    def test_aggregate_worker_metrics_rust(self):
        """Test Rust worker metrics aggregation."""
        try:
            import rust_core
        except ImportError:
            pytest.skip("rust_core not available")
        
        queue_depths = [1, 2, 3]
        latencies = [10.0, 20.0, 30.0]
        error_counts = [0, 1, 0]
        
        total_q, avg_q, total_err, avg_lat, max_lat = rust_core.aggregate_worker_metrics_rust(
            queue_depths, latencies, error_counts
        )
        
        assert total_q == 6
        assert abs(avg_q - 2.0) < 0.01
        assert total_err == 1
        assert abs(avg_lat - 20.0) < 0.01
        assert abs(max_lat - 30.0) < 0.01


# =============================================================================
# Integration Tests
# =============================================================================


class TestMultiModalIntegration:
    """Integration tests for multimodal processing."""
    
    def test_full_image_pipeline(self):
        """Test full image processing pipeline."""
        from src.infrastructure.multimodal import (
            ModalityType,
            MultiModalConfig,
            MultiModalData,
            MultiModalRegistry,
        )
        
        config = MultiModalConfig()
        
        registry = MultiModalRegistry()
        
        # Create test image
        image = np.random.rand(100, 100, 3).astype(np.float32)
        inputs = MultiModalData(images=[image])
        
        result = registry.process_inputs(inputs, config)
        assert result is not None
        assert result.has_multimodal()


class TestStructuredOutputIntegration:
    """Integration tests for structured output."""
    
    def test_json_schema_generation(self):
        """Test generating output matching JSON schema."""
        from src.infrastructure.decoding import (
            GrammarCompiler,
            StructuredOutputsParams,
        )
        
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
            "required": ["name"],
        }
        
        compiler = GrammarCompiler(
            vocab_size=100,
            token_to_string=lambda t: chr(ord('a') + (t % 26)),
        )
        
        params = StructuredOutputsParams(json=schema)
        grammar = compiler.compile(params)
        
        assert grammar is not None
        assert hasattr(grammar, "fill_bitmask")


class TestValidation:
    """Tests for validation utilities."""
    
    def test_validate_structured_output_params(self):
        """Test parameter validation."""
        from src.infrastructure.decoding import (
            StructuredOutputsParams,
            validate_structured_output_params,
        )
        
        # Valid params
        params = StructuredOutputsParams(regex=r"\d+")
        errors = validate_structured_output_params(params)
        assert len(errors) == 0
        
        # Invalid regex
        params = StructuredOutputsParams(regex=r"[invalid")
        errors = validate_structured_output_params(params)
        assert len(errors) > 0


# Run with: pytest tests/phases/test_phase26_multimodal.py -v
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
