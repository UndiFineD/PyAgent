from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, Flag, auto
from typing import Any, Callable, Dict, List, Optional, Union

class ModelCapability(Flag):
    """Model capability flags."""
    TEXT = auto()
    VISION = auto()
    AUDIO = auto()
    VIDEO = auto()
    EMBEDDING = auto()
    CLASSIFICATION = auto()
    REWARD = auto()
    TOOL_USE = auto()
    THINKING = auto()
    MULTIMODAL = VISION | AUDIO

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
    NONE = auto()
    INT8 = auto()
    INT4 = auto()
    FP8 = auto()
    NF4 = auto()
    AWQ = auto()
    GPTQ = auto()
    GGUF = auto()
    EXLLAMA = auto()
    MARLIN = auto()

class ModelFormat(Enum):
    """Model file formats."""
    HUGGINGFACE = auto()
    SAFETENSORS = auto()
    PYTORCH = auto()
    GGUF = auto()
    ONNX = auto()
    TENSORRT = auto()

@dataclass
class ModelConfig:
    """Model configuration."""
    model_name: str
    architecture: Optional[ModelArchitecture] = None
    quantization: QuantizationType = QuantizationType.NONE
    format: ModelFormat = ModelFormat.HUGGINGFACE
    revision: Optional[str] = None
    trust_remote_code: bool = False
    max_seq_len: Optional[int] = None
    tensor_parallel_size: int = 1
    dtype: str = "auto"
    extra_config: Dict[str, Any] = field(default_factory=dict)
    
    def __hash__(self) -> int:
        return hash((self.model_name, self.architecture, self.quantization))

@dataclass
class ArchitectureSpec:
    """Architecture specification."""
    name: str
    architecture: ModelArchitecture
    capabilities: ModelCapability
    model_cls: Optional[str] = None
    config_cls: Optional[str] = None
    tokenizer_cls: Optional[str] = None
    supports_lora: bool = True
    supports_vision: bool = False
    supports_audio: bool = False
    max_seq_len: int = 8192
    default_dtype: str = "bfloat16"
    architecture_patterns: List[str] = field(default_factory=list)

@dataclass
class ModelInfo:
    """Information about a model."""
    name: str
    architecture: ModelArchitecture
    capabilities: ModelCapability
    num_params: int
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
        return self.num_kv_heads is not None and self.num_kv_heads < self.num_attention_heads
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name, "architecture": self.architecture.name, "num_params": self.num_params,
            "num_layers": self.num_layers, "hidden_size": self.hidden_size, "vocab_size": self.vocab_size,
            "max_seq_len": self.max_seq_len, "is_multimodal": self.is_multimodal,
        }

@dataclass
class VRAMEstimate:
    """VRAM requirement estimation."""
    model_weights_gb: float
    kv_cache_per_token_mb: float
    activation_memory_gb: float
    total_inference_gb: float
    recommended_gpu: str
    can_fit_on: List[str] = field(default_factory=list)
