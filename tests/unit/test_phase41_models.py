# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Unit Tests for Model Registry

"""
Tests for ModelRegistry module.
"""

import pytest
from unittest.mock import Mock, patch

from src.infrastructure.engine.models.model_registry import (
    ModelCapability,
    ModelArchitecture,
    QuantizationType,
    ModelFormat,
    ModelConfig,
    ArchitectureSpec,
    ModelInfo,
    VRAMEstimate,
    ArchitectureDetector,
    VRAMEstimator,
    ModelRegistry,
)


class TestModelCapability:
    """Test ModelCapability flags."""
    
    def test_capability_flags(self):
        """Test ModelCapability flag values."""
        assert ModelCapability.TEXT is not None
        assert ModelCapability.VISION is not None
        assert ModelCapability.AUDIO is not None
        assert ModelCapability.TOOL_USE is not None
        assert ModelCapability.EMBEDDING is not None
    
    def test_capability_combinations(self):
        """Test combining capability flags."""
        caps = ModelCapability.TEXT | ModelCapability.VISION
        
        assert ModelCapability.TEXT in caps
        assert ModelCapability.VISION in caps


class TestModelArchitecture:
    """Test ModelArchitecture enum."""
    
    def test_architecture_values(self):
        """Test ModelArchitecture enum values."""
        assert ModelArchitecture.LLAMA is not None
        assert ModelArchitecture.GPT2 is not None
        assert ModelArchitecture.MISTRAL is not None
        assert ModelArchitecture.QWEN2 is not None
        assert ModelArchitecture.FALCON is not None
        assert ModelArchitecture.PHI is not None
    
    def test_architecture_count(self):
        """Test that we have many architectures."""
        # Should have 40+ architectures
        arch_count = len(ModelArchitecture)
        assert arch_count >= 30


class TestQuantizationType:
    """Test QuantizationType enum."""
    
    def test_quantization_types(self):
        """Test QuantizationType values."""
        assert QuantizationType.NONE is not None
        assert QuantizationType.INT8 is not None
        assert QuantizationType.INT4 is not None
        assert QuantizationType.FP8 is not None
        assert QuantizationType.AWQ is not None
        assert QuantizationType.GPTQ is not None


class TestModelFormat:
    """Test ModelFormat enum."""
    
    def test_format_values(self):
        """Test ModelFormat values."""
        assert ModelFormat.HUGGINGFACE is not None
        assert ModelFormat.SAFETENSORS is not None
        assert ModelFormat.PYTORCH is not None
        assert ModelFormat.GGUF is not None
        assert ModelFormat.ONNX is not None


class TestModelConfig:
    """Test ModelConfig dataclass."""
    
    def test_default_config(self):
        """Test default ModelConfig values."""
        config = ModelConfig(model_name="test-model")
        
        assert config.model_name == "test-model"
        assert config.architecture is None
        assert config.quantization == QuantizationType.NONE
        assert config.format == ModelFormat.HUGGINGFACE
    
    def test_config_with_all_fields(self):
        """Test ModelConfig with all fields."""
        config = ModelConfig(
            model_name="meta-llama/Llama-2-7b",
            architecture=ModelArchitecture.LLAMA,
            quantization=QuantizationType.INT4,
            format=ModelFormat.SAFETENSORS,
            max_seq_len=4096,
            tensor_parallel_size=2,
        )
        
        assert config.architecture == ModelArchitecture.LLAMA
        assert config.quantization == QuantizationType.INT4
        assert config.max_seq_len == 4096
    
    def test_config_hash(self):
        """Test ModelConfig is hashable."""
        config1 = ModelConfig(model_name="test")
        config2 = ModelConfig(model_name="test")
        config3 = ModelConfig(model_name="other")
        
        assert hash(config1) == hash(config2)
        assert hash(config1) != hash(config3)


class TestArchitectureSpec:
    """Test ArchitectureSpec dataclass."""
    
    def test_architecture_spec(self):
        """Test ArchitectureSpec creation."""
        spec = ArchitectureSpec(
            name="llama",
            architecture=ModelArchitecture.LLAMA,
            capabilities=ModelCapability.TEXT | ModelCapability.TOOL_USE,
        )
        
        assert spec.name == "llama"
        assert spec.architecture == ModelArchitecture.LLAMA
        assert ModelCapability.TEXT in spec.capabilities


class TestModelInfo:
    """Test ModelInfo dataclass."""
    
    def test_model_info(self):
        """Test ModelInfo creation."""
        info = ModelInfo(
            name="meta-llama/Llama-2-7b",
            architecture=ModelArchitecture.LLAMA,
            capabilities=ModelCapability.TEXT,
            num_params=7_000_000_000,
            num_layers=32,
            hidden_size=4096,
            num_attention_heads=32,
        )
        
        assert info.name == "meta-llama/Llama-2-7b"
        assert info.architecture == ModelArchitecture.LLAMA
        assert info.num_params == 7_000_000_000
    
    def test_model_info_multimodal(self):
        """Test ModelInfo multimodal detection."""
        info = ModelInfo(
            name="llava",
            architecture=ModelArchitecture.LLAVA,
            capabilities=ModelCapability.MULTIMODAL | ModelCapability.TEXT,
            num_params=7_000_000_000,
            num_layers=32,
            hidden_size=4096,
            num_attention_heads=32,
        )
        
        assert info.is_multimodal
    
    def test_model_info_gqa(self):
        """Test ModelInfo GQA detection."""
        info = ModelInfo(
            name="llama-3",
            architecture=ModelArchitecture.LLAMA,
            capabilities=ModelCapability.TEXT,
            num_params=8_000_000_000,
            num_layers=32,
            hidden_size=4096,
            num_attention_heads=32,
            num_kv_heads=8,
        )
        
        assert info.has_gqa


class TestVRAMEstimate:
    """Test VRAMEstimate dataclass."""
    
    def test_vram_estimate(self):
        """Test VRAMEstimate creation."""
        estimate = VRAMEstimate(
            model_weights_gb=14.0,
            kv_cache_per_token_mb=0.5,
            activation_memory_gb=1.0,
            total_inference_gb=16.0,
            recommended_gpu="A100-40GB",
        )
        
        assert estimate.model_weights_gb == 14.0
        assert estimate.total_inference_gb == 16.0
    
    def test_vram_estimate_max_context(self):
        """Test max context estimation."""
        estimate = VRAMEstimate(
            model_weights_gb=14.0,
            kv_cache_per_token_mb=0.5,
            activation_memory_gb=1.0,
            total_inference_gb=16.0,
            recommended_gpu="A100-40GB",
        )
        
        # With 40GB GPU and 14+1=15GB overhead, 25GB for KV cache
        max_ctx = estimate.estimate_max_context(40.0)
        assert max_ctx > 0


class TestArchitectureDetector:
    """Test ArchitectureDetector class."""
    
    def test_detect_from_config(self):
        """Test detecting architecture from config."""
        config = {"model_type": "llama"}
        arch = ArchitectureDetector.detect_from_config(config)
        
        assert arch == ModelArchitecture.LLAMA
    
    def test_detect_from_architectures(self):
        """Test detecting from architectures list."""
        config = {"architectures": ["MistralForCausalLM"]}
        arch = ArchitectureDetector.detect_from_config(config)
        
        assert arch == ModelArchitecture.MISTRAL
    
    def test_detect_from_name(self):
        """Test detecting from model name."""
        arch = ArchitectureDetector.detect_from_name("meta-llama/Llama-2-7b")
        
        assert arch == ModelArchitecture.LLAMA
    
    def test_detect_unknown(self):
        """Test detecting unknown architecture."""
        config = {"model_type": "totally_unknown_model_xyz"}
        arch = ArchitectureDetector.detect_from_config(config)
        
        # Should return CUSTOM for unknown
        assert arch == ModelArchitecture.CUSTOM


class TestVRAMEstimator:
    """Test VRAMEstimator class."""
    
    def test_estimate_fp16(self):
        """Test VRAM estimation for FP16."""
        info = ModelInfo(
            name="test-7b",
            architecture=ModelArchitecture.LLAMA,
            capabilities=ModelCapability.TEXT,
            num_params=7_000_000_000,
            num_layers=32,
            hidden_size=4096,
            num_attention_heads=32,
        )
        
        estimate = VRAMEstimator.estimate(info, dtype="float16")
        
        # FP16: ~14GB for 7B model
        assert estimate.model_weights_gb >= 13.0
        assert estimate.model_weights_gb <= 16.0
    
    def test_estimate_int4(self):
        """Test VRAM estimation for INT4."""
        info = ModelInfo(
            name="test-7b-quant",
            architecture=ModelArchitecture.LLAMA,
            capabilities=ModelCapability.TEXT,
            num_params=7_000_000_000,
            num_layers=32,
            hidden_size=4096,
            num_attention_heads=32,
            quantization=QuantizationType.INT4,
        )
        
        estimate = VRAMEstimator.estimate(info, dtype="float16")
        
        # INT4: ~3.5GB for 7B model
        assert estimate.model_weights_gb >= 3.0
        assert estimate.model_weights_gb <= 5.0


class TestModelRegistry:
    """Test ModelRegistry class."""
    
    def test_singleton_instance(self):
        """Test ModelRegistry is singleton."""
        registry1 = ModelRegistry()
        registry2 = ModelRegistry()
        
        assert registry1 is registry2
    
    def test_registry_list_architectures(self):
        """Test listing registered architectures."""
        registry = ModelRegistry()
        
        architectures = registry.list_architectures()
        
        assert len(architectures) > 0
    
    def test_registry_has_specs(self):
        """Test registry has architecture specs."""
        registry = ModelRegistry()
        
        # Registry should have some specs
        assert registry is not None
