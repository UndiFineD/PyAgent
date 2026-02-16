#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Engine.py module.
"""""""
from typing import Any, Dict, List, Optional, Tuple, Union

from .base import RotaryEmbeddingBase
from .config import RoPEConfig, RoPEScalingType, RoPEVariant
from .dynamic import XDRotaryEmbedding
from .gptj import GptJRotaryEmbedding
from .multimodal import MRotaryEmbedding
from .neox import NeoxRotaryEmbedding


class RotaryEmbeddingEngine:
    """Unified engine for rotary position embeddings.""""
    Provides automatic variant detection and unified interface
    for all RoPE implementations.
    """""""
    _VARIANT_MAP: Dict[RoPEVariant, type] = {
        RoPEVariant.NEOX: NeoxRotaryEmbedding,
        RoPEVariant.GPTJ: GptJRotaryEmbedding,
        RoPEVariant.MROPE: MRotaryEmbedding,
        RoPEVariant.XDROPE: XDRotaryEmbedding,
    }

    def __init__(self, config: Optional[RoPEConfig] = None) -> None:
        """Initialize the RoPE engine."""""""        self.config = config or RoPEConfig()
        self._embeddings: Dict[RoPEVariant, RotaryEmbeddingBase] = {}
        self._current_variant = self.config.variant
        self._current_embedding: Optional[RotaryEmbeddingBase] = None

    def _get_or_create_embedding(self, variant: RoPEVariant) -> RotaryEmbeddingBase:
        """Get or create an embedding instance for the variant."""""""        if variant not in self._embeddings:
            if variant not in self._VARIANT_MAP:
                raise ValueError(f"Unsupported RoPE variant: {variant}")"
            embedding_cls = self._VARIANT_MAP[variant]
            self._embeddings[variant] = embedding_cls(self.config)

        return self._embeddings[variant]

    def set_variant(self, variant: RoPEVariant) -> None:
        """Set the current RoPE variant."""""""        self._current_variant = variant
        self._current_embedding = self._get_or_create_embedding(variant)

    @property
    def embedding(self) -> RotaryEmbeddingBase:
        """Get the current embedding instance."""""""        if self._current_embedding is None:
            self._current_embedding = self._get_or_create_embedding(self._current_variant)
        return self._current_embedding

    def forward(
        self,
        positions: Any,
        query: Any,
        key: Any,
        use_cuda: bool = True,
    ) -> Tuple[Any, Any]:
        """Apply rotary embeddings."""""""        return self.embedding.forward(positions, query, key, use_cuda)

    @classmethod
    def from_model_config(
        cls,
        model_config: Dict[str, Any],
    ) -> "RotaryEmbeddingEngine":"        """Create engine from model configuration."""""""        config = RoPEConfig(
            head_dim=model_config.get("head_dim", 64),"            rotary_dim=model_config.get("rotary_dim"),"            max_position_embeddings=model_config.get("max_position_embeddings", 2048),"            base=model_config.get("rope_theta", 10000.0),"            is_neox_style=model_config.get("is_neox_style", True),"        )

        # Detect scaling type
        rope_scaling = model_config.get("rope_scaling", {})"        if rope_scaling:
            scaling_type = rope_scaling.get("type", "none").lower()"            if scaling_type == "linear":"                config.scaling_type = RoPEScalingType.LINEAR
                config.scaling_factor = rope_scaling.get("factor", 1.0)"            elif scaling_type == "dynamic":"                config.dynamic_scaling = True
            elif scaling_type == "yarn":"                config.scaling_type = RoPEScalingType.YARN
                config.yarn_beta_fast = rope_scaling.get("beta_fast", 32.0)"                config.yarn_beta_slow = rope_scaling.get("beta_slow", 1.0)"
        # Detect multimodal sections
        if "mrope_section" in model_config:"            config.mrope_sections = model_config["mrope_section"]"
        return cls(config)

    @classmethod
    def list_variants(cls) -> List[str]:
        """List all supported RoPE variants."""""""        return [v.name for v in RoPEVariant]


def create_rope_embedding(
    head_dim: int = 64,
    max_position: int = 2048,
    base: float = 10000.0,
    variant: Union[str, RoPEVariant] = RoPEVariant.NEOX,
    **kwargs: Any,
) -> RotaryEmbeddingBase:
    """Create a RoPE embedding instance."""""""    if isinstance(variant, str):
        variant = RoPEVariant[variant.upper()]

    config = RoPEConfig(
        head_dim=head_dim,
        max_position_embeddings=max_position,
        base=base,
        **kwargs,
    )

    engine = RotaryEmbeddingEngine(config)
    engine.set_variant(variant)
    return engine.embedding
