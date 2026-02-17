#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Config.py module.

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional


class RoPEVariant(Enum):
    """Supported RoPE variants.
    NEOX = auto()  # Llama, Mistral, most modern LLMs
    GPTJ = auto()  # GPT-J, GPT-Neo styles
    MROPE = auto()  # Multimodal (vision-language)
    XDROPE = auto()  # Extended Dynamic (NTK, etc.)
    LONGROPE = auto()  # Specialized for very long contexts


class RoPEScalingType(Enum):
    """Supported position scaling types.
    NONE = auto()
    LINEAR = auto()
    DYNAMIC = auto()
    YARN = auto()


@dataclass
class RoPEConfig:
    """Configuration for Rotary Position Embeddings.
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

    def __post_init__(self) -> None:
        if self.rotary_dim is None:
            self.rotary_dim = self.head_dim
        if self.original_max_position is None:
            self.original_max_position = self.max_position_embeddings

        # Automatic variant detection
        if self.mrope_sections and self.variant == RoPEVariant.NEOX:
            self.variant = RoPEVariant.MROPE
