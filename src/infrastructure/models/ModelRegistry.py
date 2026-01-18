# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Model Registry - Architecture Management

"""
Unified model registry for architecture detection and management.

Inspired by vLLM's model registry patterns, this module provides:
- Model architecture registration
- Capability detection (vision, audio, multimodal)
- Lazy loading support
- VRAM estimation

Beyond vLLM:
- Automatic VRAM requirement estimation
- Architecture fingerprinting
- Subprocess isolation for model loading
- Multi-format support (HF, GGUF, SafeTensors)
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    Union,
)


# =============================================================================
# Enums
# =============================================================================

class ModelCapability(Flag):
    """Model capability flags."""
    TEXT = auto()                 # Text generation
    VISION = auto()               # Image understanding
    AUDIO = auto()                # Audio processing
    VIDEO = auto()                # Video understanding
    EMBEDDING = auto()            # Embedding generation
    CLASSIFICATION = auto()       # Classification tasks
    REWARD = auto()               # Reward model
    TOOL_USE = auto()             # Function calling
    THINKING = auto()             # Chain-of-thought
    MULTIMODAL = VISION | AUDIO   # Combined multimodal


class ModelArchitecture(Enum):
    """Known model architectures."""
    LLAMA = auto()
    MISTRAL = auto()
    QWEN = auto()
    QWEN2 = auto()
    QWEN2_VL = auto()
    GEMMA = auto()
    GEMMA2 = auto()
    PHI = auto()
    PHI3 = auto()
    GPT_NEOX = auto()
    GPT2 = auto()
    FALCON = auto()
    BLOOM = auto()
    MAMBA = auto()
    MAMBA2 = auto()
    DEEPSEEK = auto()
    DEEPSEEK_V2 = auto()
    DEEPSEEK_V3 = auto()
    YI = auto()
    INTERNLM = auto()
    INTERNLM2 = auto()
    BAICHUAN = auto()
    CHATGLM = auto()
    STARCODER = auto()
    STARCODER2 = auto()
    CODELLAMA = auto()
    MIXTRAL = auto()
    ARCTIC = auto()
    DBRX = auto()
    JAMBA = auto()
    OLMO = auto()
    COMMAND_R = auto()
    BERT = auto()
    ROBERTA = auto()
    T5 = auto()
    CLIP = auto()
    SIGLIP = auto()
    LLAVA = auto()
    LLAVA_NEXT = auto()
    PIXTRAL = auto()
    MOLMO = auto()
    IDEFICS = auto()
    FUYU = auto()
    PALIGEMMA = auto()
    WHISPER = auto()
    CUSTOM = auto()


class QuantizationType(Enum):
    """Quantization types."""
    NONE = auto()                 # FP32/FP16/BF16
    INT8 = auto()                 # 8-bit integer
    INT4 = auto()                 # 4-bit integer
    FP8 = auto()                  # 8-bit float
    NF4 = auto()                  # 4-bit NormalFloat
    AWQ = auto()                  # AWQ quantization
    GPTQ = auto()                 # GPTQ quantization
    GGUF = auto()                 # GGML quantization
    EXLLAMA = auto()              # ExLlama quantization
    MARLIN = auto()               # Marlin quantization


class ModelFormat(Enum):
    """Model file formats."""
    HUGGINGFACE = auto()          # Standard HF format
    SAFETENSORS = auto()          # SafeTensors format
    PYTORCH = auto()              # PyTorch .pt/.pth
    GGUF = auto()                 # GGML Unified Format
    ONNX = auto()                 # ONNX format
    TENSORRT = auto()             # TensorRT engine


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class ModelConfig:
    """Model configuration."""
    model_name: str                                    # Model name or path
    architecture: Optional[ModelArchitecture] = None
    quantization: QuantizationType = QuantizationType.NONE
    format: ModelFormat = ModelFormat.HUGGINGFACE
    revision: Optional[str] = None
    trust_remote_code: bool = False
    max_seq_len: Optional[int] = None
    tensor_parallel_size: int = 1
    dtype: str = "auto"                                # auto, float16, bfloat16
    extra_config: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self) -> int:
        return hash((self.model_name, self.architecture, self.quantization))


@dataclass
class ArchitectureSpec:
    """Architecture specification."""
    name: str
    architecture: ModelArchitecture
    capabilities: ModelCapability
    model_cls: Optional[str] = None                   # Class path for loading
    config_cls: Optional[str] = None                  # Config class path
    tokenizer_cls: Optional[str] = None               # Tokenizer class path
    supports_lora: bool = True
    supports_vision: bool = False
    supports_audio: bool = False
    max_seq_len: int = 8192
    default_dtype: str = "bfloat16"
    architecture_patterns: List[str] = field(default_factory=list)  # Config patterns


@dataclass
class ModelInfo:
    """Information about a model."""
    name: str
    architecture: ModelArchitecture
    capabilities: ModelCapability
    num_params: int                                   # Total parameters
    num_layers: int
    hidden_size: int
    num_attention_heads: int
    num_kv_heads: Optional[int] = None
    vocab_size: int = 32000
    max_seq_len: int = 8192
    rope_theta: Optional[float] = None
    intermediate_size: Optional[int] = None
    quantization: QuantizationType = QuantizationType.NONE
    format: ModelFormat = ModelFormat.HUGGINGFACE
    license: Optional[str] = None
    
    @property
    def is_multimodal(self) -> bool:
        return bool(self.capabilities & ModelCapability.MULTIMODAL)
    
    @property
    def has_gqa(self) -> bool:
        """Check if model uses grouped-query attention."""
        return self.num_kv_heads is not None and self.num_kv_heads < self.num_attention_heads
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "architecture": self.architecture.name,
            "num_params": self.num_params,
            "num_layers": self.num_layers,
            "hidden_size": self.hidden_size,
            "num_attention_heads": self.num_attention_heads,
            "num_kv_heads": self.num_kv_heads,
            "vocab_size": self.vocab_size,
            "max_seq_len": self.max_seq_len,
            "is_multimodal": self.is_multimodal,
        }


@dataclass
class VRAMEstimate:
    """VRAM requirement estimation."""
    model_weights_gb: float                           # Weights only
    kv_cache_per_token_mb: float                      # Per-token KV cache
    activation_memory_gb: float                       # Activation memory
    total_inference_gb: float                         # Total for inference
    recommended_gpu: str                              # GPU recommendation
    can_fit_on: List[str] = field(default_factory=list)  # Compatible GPUs
    
    @property
    def kv_cache_for_context(self) -> Callable[[int], float]:
        """Get KV cache size for given context length."""
        return lambda ctx: (self.kv_cache_per_token_mb * ctx) / 1024
    
    def estimate_max_context(self, available_vram_gb: float) -> int:
        """Estimate max context length for given VRAM."""
        overhead = self.model_weights_gb + self.activation_memory_gb
        available_for_kv = available_vram_gb - overhead
        
        if available_for_kv <= 0:
            return 0
        
        return int((available_for_kv * 1024) / self.kv_cache_per_token_mb)


# =============================================================================
# Architecture Detector
# =============================================================================

class ArchitectureDetector:
    """
    Detect model architecture from config.
    
    Supports detection from:
    - HuggingFace config.json
    - Model name patterns
    - Architecture fingerprinting
    """
    
    # Architecture pattern matching
    ARCHITECTURE_PATTERNS = {
        "llama": ModelArchitecture.LLAMA,
        "mistral": ModelArchitecture.MISTRAL,
        "qwen2": ModelArchitecture.QWEN2,
        "qwen": ModelArchitecture.QWEN,
        "gemma2": ModelArchitecture.GEMMA2,
        "gemma": ModelArchitecture.GEMMA,
        "phi-3": ModelArchitecture.PHI3,
        "phi": ModelArchitecture.PHI,
        "gpt-neox": ModelArchitecture.GPT_NEOX,
        "gpt2": ModelArchitecture.GPT2,
        "falcon": ModelArchitecture.FALCON,
        "bloom": ModelArchitecture.BLOOM,
        "mamba2": ModelArchitecture.MAMBA2,
        "mamba": ModelArchitecture.MAMBA,
        "deepseek-v3": ModelArchitecture.DEEPSEEK_V3,
        "deepseek-v2": ModelArchitecture.DEEPSEEK_V2,
        "deepseek": ModelArchitecture.DEEPSEEK,
        "yi": ModelArchitecture.YI,
        "internlm2": ModelArchitecture.INTERNLM2,
        "internlm": ModelArchitecture.INTERNLM,
        "baichuan": ModelArchitecture.BAICHUAN,
        "chatglm": ModelArchitecture.CHATGLM,
        "starcoder2": ModelArchitecture.STARCODER2,
        "starcoder": ModelArchitecture.STARCODER,
        "codellama": ModelArchitecture.CODELLAMA,
        "mixtral": ModelArchitecture.MIXTRAL,
        "arctic": ModelArchitecture.ARCTIC,
        "dbrx": ModelArchitecture.DBRX,
        "jamba": ModelArchitecture.JAMBA,
        "olmo": ModelArchitecture.OLMO,
        "command-r": ModelArchitecture.COMMAND_R,
        "bert": ModelArchitecture.BERT,
        "roberta": ModelArchitecture.ROBERTA,
        "t5": ModelArchitecture.T5,
        "clip": ModelArchitecture.CLIP,
        "siglip": ModelArchitecture.SIGLIP,
        "llava-next": ModelArchitecture.LLAVA_NEXT,
        "llava": ModelArchitecture.LLAVA,
        "pixtral": ModelArchitecture.PIXTRAL,
        "molmo": ModelArchitecture.MOLMO,
        "idefics": ModelArchitecture.IDEFICS,
        "fuyu": ModelArchitecture.FUYU,
        "paligemma": ModelArchitecture.PALIGEMMA,
        "whisper": ModelArchitecture.WHISPER,
    }
    
    # Config key to architecture mapping
    CONFIG_KEYS = {
        "LlamaForCausalLM": ModelArchitecture.LLAMA,
        "MistralForCausalLM": ModelArchitecture.MISTRAL,
        "Qwen2ForCausalLM": ModelArchitecture.QWEN2,
        "QWenLMHeadModel": ModelArchitecture.QWEN,
        "Gemma2ForCausalLM": ModelArchitecture.GEMMA2,
        "GemmaForCausalLM": ModelArchitecture.GEMMA,
        "Phi3ForCausalLM": ModelArchitecture.PHI3,
        "PhiForCausalLM": ModelArchitecture.PHI,
        "GPTNeoXForCausalLM": ModelArchitecture.GPT_NEOX,
        "GPT2LMHeadModel": ModelArchitecture.GPT2,
        "FalconForCausalLM": ModelArchitecture.FALCON,
        "BloomForCausalLM": ModelArchitecture.BLOOM,
        "MambaForCausalLM": ModelArchitecture.MAMBA,
        "Mamba2ForCausalLM": ModelArchitecture.MAMBA2,
        "DeepseekV2ForCausalLM": ModelArchitecture.DEEPSEEK_V2,
        "DeepseekV3ForCausalLM": ModelArchitecture.DEEPSEEK_V3,
        "MixtralForCausalLM": ModelArchitecture.MIXTRAL,
        "DbrxForCausalLM": ModelArchitecture.DBRX,
        "JambaForCausalLM": ModelArchitecture.JAMBA,
        "LlavaForConditionalGeneration": ModelArchitecture.LLAVA,
        "LlavaNextForConditionalGeneration": ModelArchitecture.LLAVA_NEXT,
    }
    
    @classmethod
    def detect_from_config(cls, config: Dict[str, Any]) -> ModelArchitecture:
        """Detect architecture from model config."""
        # Check architectures field
        architectures = config.get("architectures", [])
        for arch_name in architectures:
            if arch_name in cls.CONFIG_KEYS:
                return cls.CONFIG_KEYS[arch_name]
        
        # Check model_type field
        model_type = config.get("model_type", "").lower()
        for pattern, arch in cls.ARCHITECTURE_PATTERNS.items():
            if pattern in model_type:
                return arch
        
        return ModelArchitecture.CUSTOM
    
    @classmethod
    def detect_from_name(cls, model_name: str) -> ModelArchitecture:
        """Detect architecture from model name."""
        name_lower = model_name.lower()
        
        for pattern, arch in cls.ARCHITECTURE_PATTERNS.items():
            if pattern in name_lower:
                return arch
        
        return ModelArchitecture.CUSTOM
    
    @classmethod
    def detect_capabilities(
        cls,
        architecture: ModelArchitecture,
        config: Optional[Dict[str, Any]] = None,
    ) -> ModelCapability:
        """Detect model capabilities."""
        # Vision models
        vision_archs = {
            ModelArchitecture.LLAVA,
            ModelArchitecture.LLAVA_NEXT,
            ModelArchitecture.PIXTRAL,
            ModelArchitecture.MOLMO,
            ModelArchitecture.IDEFICS,
            ModelArchitecture.FUYU,
            ModelArchitecture.PALIGEMMA,
            ModelArchitecture.QWEN2_VL,
            ModelArchitecture.CLIP,
            ModelArchitecture.SIGLIP,
        }
        
        # Audio models
        audio_archs = {
            ModelArchitecture.WHISPER,
        }
        
        # Embedding models
        embedding_archs = {
            ModelArchitecture.BERT,
            ModelArchitecture.ROBERTA,
        }
        
        caps = ModelCapability.TEXT
        
        if architecture in vision_archs:
            caps |= ModelCapability.VISION
        
        if architecture in audio_archs:
            caps |= ModelCapability.AUDIO
        
        if architecture in embedding_archs:
            caps |= ModelCapability.EMBEDDING
        
        # Check config for additional capabilities
        if config:
            if config.get("vision_config") or config.get("image_size"):
                caps |= ModelCapability.VISION
            if config.get("audio_config"):
                caps |= ModelCapability.AUDIO
        
        return caps


# =============================================================================
# VRAM Estimator
# =============================================================================

class VRAMEstimator:
    """
    Estimate VRAM requirements for models.
    
    Beyond vLLM:
    - Accurate per-model estimation
    - Quantization-aware calculations
    - Context-length scaling
    """
    
    # GPU VRAM in GB
    GPU_VRAM = {
        "RTX 4090": 24,
        "RTX 4080": 16,
        "RTX 4070 Ti": 12,
        "RTX 3090": 24,
        "RTX 3080": 10,
        "A100-40GB": 40,
        "A100-80GB": 80,
        "H100": 80,
        "A10G": 24,
        "L4": 24,
        "T4": 16,
    }
    
    # Bytes per parameter by dtype
    BYTES_PER_PARAM = {
        "float32": 4,
        "float16": 2,
        "bfloat16": 2,
        "int8": 1,
        "int4": 0.5,
        "fp8": 1,
    }
    
    @classmethod
    def estimate(
        cls,
        model_info: ModelInfo,
        context_length: int = 4096,
        batch_size: int = 1,
        dtype: str = "float16",
    ) -> VRAMEstimate:
        """Estimate VRAM requirements."""
        # Calculate bytes per parameter based on quantization
        if model_info.quantization == QuantizationType.INT8:
            bytes_per_param = 1
        elif model_info.quantization in (QuantizationType.INT4, QuantizationType.NF4, 
                                         QuantizationType.AWQ, QuantizationType.GPTQ):
            bytes_per_param = 0.5
        else:
            bytes_per_param = cls.BYTES_PER_PARAM.get(dtype, 2)
        
        # Model weights
        model_weights_gb = (model_info.num_params * bytes_per_param) / (1024**3)
        
        # KV cache per token
        # KV cache size = 2 * num_layers * (num_kv_heads * head_dim) * bytes
        num_kv_heads = model_info.num_kv_heads or model_info.num_attention_heads
        head_dim = model_info.hidden_size // model_info.num_attention_heads
        kv_per_layer = 2 * num_kv_heads * head_dim * bytes_per_param
        kv_cache_per_token_bytes = model_info.num_layers * kv_per_layer
        kv_cache_per_token_mb = kv_cache_per_token_bytes / (1024**2)
        
        # Total KV cache for context
        kv_cache_total_gb = (kv_cache_per_token_mb * context_length * batch_size) / 1024
        
        # Activation memory (rough estimate: ~10-20% of model weights)
        activation_memory_gb = model_weights_gb * 0.15
        
        # Total inference memory
        total_inference_gb = model_weights_gb + kv_cache_total_gb + activation_memory_gb
        
        # Find compatible GPUs
        can_fit_on = [
            gpu for gpu, vram in cls.GPU_VRAM.items()
            if vram >= total_inference_gb
        ]
        
        # Recommend GPU
        if total_inference_gb <= 16:
            recommended = "RTX 4080 / T4"
        elif total_inference_gb <= 24:
            recommended = "RTX 4090 / A10G / L4"
        elif total_inference_gb <= 40:
            recommended = "A100-40GB"
        elif total_inference_gb <= 80:
            recommended = "A100-80GB / H100"
        else:
            recommended = f"Multi-GPU ({int(total_inference_gb / 80) + 1}x H100)"
        
        return VRAMEstimate(
            model_weights_gb=model_weights_gb,
            kv_cache_per_token_mb=kv_cache_per_token_mb,
            activation_memory_gb=activation_memory_gb,
            total_inference_gb=total_inference_gb,
            recommended_gpu=recommended,
            can_fit_on=can_fit_on,
        )
    
    @classmethod
    def estimate_from_params(
        cls,
        num_params_billions: float,
        num_layers: int = 32,
        hidden_size: int = 4096,
        num_heads: int = 32,
        num_kv_heads: Optional[int] = None,
        quantization: QuantizationType = QuantizationType.NONE,
        context_length: int = 4096,
    ) -> VRAMEstimate:
        """Estimate from basic parameters."""
        model_info = ModelInfo(
            name="estimate",
            architecture=ModelArchitecture.LLAMA,
            capabilities=ModelCapability.TEXT,
            num_params=int(num_params_billions * 1e9),
            num_layers=num_layers,
            hidden_size=hidden_size,
            num_attention_heads=num_heads,
            num_kv_heads=num_kv_heads,
            quantization=quantization,
        )
        return cls.estimate(model_info, context_length=context_length)


# =============================================================================
# Model Registry
# =============================================================================

class ModelRegistry:
    """
    Central registry for model architectures.
    
    Features:
    - Architecture registration
    - Lazy loading support
    - Capability detection
    - VRAM estimation
    """
    
    _instance: Optional['ModelRegistry'] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'ModelRegistry':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._architectures: Dict[ModelArchitecture, ArchitectureSpec] = {}
        self._model_cache: Dict[str, ModelInfo] = {}
        self._cache_lock = threading.RLock()
        
        self._register_defaults()
        self._initialized = True
    
    def _register_defaults(self):
        """Register default architectures."""
        defaults = [
            ArchitectureSpec(
                name="llama",
                architecture=ModelArchitecture.LLAMA,
                capabilities=ModelCapability.TEXT | ModelCapability.TOOL_USE,
                supports_lora=True,
                max_seq_len=131072,
            ),
            ArchitectureSpec(
                name="mistral",
                architecture=ModelArchitecture.MISTRAL,
                capabilities=ModelCapability.TEXT | ModelCapability.TOOL_USE,
                supports_lora=True,
                max_seq_len=32768,
            ),
            ArchitectureSpec(
                name="qwen2",
                architecture=ModelArchitecture.QWEN2,
                capabilities=ModelCapability.TEXT | ModelCapability.TOOL_USE | ModelCapability.THINKING,
                supports_lora=True,
                max_seq_len=131072,
            ),
            ArchitectureSpec(
                name="deepseek-v3",
                architecture=ModelArchitecture.DEEPSEEK_V3,
                capabilities=ModelCapability.TEXT | ModelCapability.TOOL_USE | ModelCapability.THINKING,
                supports_lora=True,
                max_seq_len=131072,
            ),
            ArchitectureSpec(
                name="llava",
                architecture=ModelArchitecture.LLAVA,
                capabilities=ModelCapability.TEXT | ModelCapability.VISION,
                supports_lora=True,
                supports_vision=True,
                max_seq_len=4096,
            ),
            ArchitectureSpec(
                name="pixtral",
                architecture=ModelArchitecture.PIXTRAL,
                capabilities=ModelCapability.TEXT | ModelCapability.VISION,
                supports_lora=True,
                supports_vision=True,
                max_seq_len=131072,
            ),
            ArchitectureSpec(
                name="mamba",
                architecture=ModelArchitecture.MAMBA,
                capabilities=ModelCapability.TEXT,
                supports_lora=False,
                max_seq_len=1048576,  # Theoretically unlimited
            ),
        ]
        
        for spec in defaults:
            self._architectures[spec.architecture] = spec
    
    def register(self, spec: ArchitectureSpec):
        """Register an architecture."""
        self._architectures[spec.architecture] = spec
    
    def get_architecture(self, arch: ModelArchitecture) -> Optional[ArchitectureSpec]:
        """Get architecture specification."""
        return self._architectures.get(arch)
    
    def detect_architecture(
        self,
        model_name_or_config: Union[str, Dict[str, Any]],
    ) -> ModelArchitecture:
        """Detect architecture from model name or config."""
        if isinstance(model_name_or_config, dict):
            return ArchitectureDetector.detect_from_config(model_name_or_config)
        return ArchitectureDetector.detect_from_name(model_name_or_config)
    
    def get_model_info(
        self,
        model_name: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> ModelInfo:
        """Get model information, loading config if needed."""
        with self._cache_lock:
            if model_name in self._model_cache:
                return self._model_cache[model_name]
        
        # Load config if not provided
        if config is None:
            config = self._load_config(model_name)
        
        # Detect architecture
        architecture = self.detect_architecture(config or model_name)
        capabilities = ArchitectureDetector.detect_capabilities(architecture, config)
        
        # Extract model info from config
        if config:
            info = ModelInfo(
                name=model_name,
                architecture=architecture,
                capabilities=capabilities,
                num_params=self._estimate_params(config),
                num_layers=config.get("num_hidden_layers", 32),
                hidden_size=config.get("hidden_size", 4096),
                num_attention_heads=config.get("num_attention_heads", 32),
                num_kv_heads=config.get("num_key_value_heads"),
                vocab_size=config.get("vocab_size", 32000),
                max_seq_len=config.get("max_position_embeddings", 8192),
                rope_theta=config.get("rope_theta"),
                intermediate_size=config.get("intermediate_size"),
            )
        else:
            # Fallback to defaults
            info = ModelInfo(
                name=model_name,
                architecture=architecture,
                capabilities=capabilities,
                num_params=7_000_000_000,  # Default 7B
                num_layers=32,
                hidden_size=4096,
                num_attention_heads=32,
            )
        
        with self._cache_lock:
            self._model_cache[model_name] = info
        
        return info
    
    def _load_config(self, model_name: str) -> Optional[Dict[str, Any]]:
        """Load model config from HuggingFace or local path."""
        try:
            # Try local path first
            if os.path.isdir(model_name):
                config_path = Path(model_name) / "config.json"
                if config_path.exists():
                    with open(config_path) as f:
                        return json.load(f)
            
            # Try HuggingFace
            from huggingface_hub import hf_hub_download
            
            config_path = hf_hub_download(
                repo_id=model_name,
                filename="config.json",
            )
            with open(config_path) as f:
                return json.load(f)
                
        except Exception:
            return None
    
    def _estimate_params(self, config: Dict[str, Any]) -> int:
        """Estimate parameter count from config."""
        hidden = config.get("hidden_size", 4096)
        layers = config.get("num_hidden_layers", 32)
        vocab = config.get("vocab_size", 32000)
        intermediate = config.get("intermediate_size", hidden * 4)
        
        # Embedding params
        embed_params = vocab * hidden
        
        # Per-layer params (attention + FFN)
        attn_params = 4 * hidden * hidden  # Q, K, V, O
        ffn_params = 3 * hidden * intermediate  # Up, Gate, Down
        layer_params = attn_params + ffn_params
        
        total = embed_params + (layers * layer_params) + embed_params  # +LM head
        return int(total)
    
    def estimate_vram(
        self,
        model_name: str,
        context_length: int = 4096,
        quantization: QuantizationType = QuantizationType.NONE,
    ) -> VRAMEstimate:
        """Estimate VRAM requirements for a model."""
        info = self.get_model_info(model_name)
        info.quantization = quantization
        return VRAMEstimator.estimate(info, context_length=context_length)
    
    def list_architectures(self) -> List[ModelArchitecture]:
        """List all registered architectures."""
        return list(self._architectures.keys())


# =============================================================================
# Utility Functions
# =============================================================================

def register_model(spec: ArchitectureSpec):
    """Register a model architecture."""
    registry = ModelRegistry()
    registry.register(spec)


def get_model_info(model_name: str) -> ModelInfo:
    """Get model information."""
    registry = ModelRegistry()
    return registry.get_model_info(model_name)


def detect_architecture(model_name: str) -> ModelArchitecture:
    """Detect model architecture from name."""
    registry = ModelRegistry()
    return registry.detect_architecture(model_name)


def estimate_vram(
    model_name: str,
    context_length: int = 4096,
    quantization: QuantizationType = QuantizationType.NONE,
) -> VRAMEstimate:
    """Estimate VRAM requirements."""
    registry = ModelRegistry()
    return registry.estimate_vram(model_name, context_length, quantization)
