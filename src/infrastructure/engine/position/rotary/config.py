from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional

class RoPEVariant(Enum):
    """Supported RoPE variants."""
    NEOX = auto()      # Llama, Mistral, most modern LLMs
    GPTJ = auto()      # GPT-J, GPT-Neo styles
    MROPE = auto()     # Multimodal (vision-language)
    XDROPE = auto()    # Extended Dynamic (NTK, etc.)
    LONGROPE = auto()  # Specialized for very long contexts

class RoPEScalingType(Enum):
    """Supported position scaling types."""
    NONE = auto()
    LINEAR = auto()
    DYNAMIC = auto()
    YARN = auto()

@dataclass
class RoPEConfig:
    """Configuration for Rotary Position Embeddings."""
    head_dim: int = 64
    rotary_dim: Optional[int] = None
    max_position_embeddings: int = 2048
    base: float = 10000.0
    scaling_factor: float = 1.0
    scaling_type: RoPEScalingType = RoPEScalingType.NONE
    is_neox_style: bool = True

    # Advanced features
    dynamic_scaling: bool = False
    original_max_position: int = 2048
    yarn_beta_fast: float = 32.0
    yarn_beta_slow: float = 1.0

    # Multimodal specific
    mrope_sections: List[int] = field(default_factory=list)

    # Variant
    variant: RoPEVariant = RoPEVariant.NEOX

    def __post_init__(self):
        if self.rotary_dim is None:
            self.rotary_dim = self.head_dim
        if self.original_max_position is None:
            self.original_max_position = self.max_position_embeddings

        # Automatic variant detection
        if self.mrope_sections and self.variant == RoPEVariant.NEOX:
            self.variant = RoPEVariant.MROPE
