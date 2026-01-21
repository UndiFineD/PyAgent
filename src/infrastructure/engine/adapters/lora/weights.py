# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""LoRA layer weight implementations."""

from __future__ import annotations
from dataclasses import dataclass
import numpy as np

try:
    from numpy.typing import NDArray
except ImportError:
    from typing import Any
    NDArray = Any


@dataclass
class LoRALayerWeights:
    """LoRA weights for a single layer."""
    lora_a: NDArray[np.float32]  # [rank, in_features]
    lora_b: NDArray[np.float32]  # [out_features, rank]
    scaling: float
    module_name: str
    dropout: float = 0.0
    
    @property
    def rank(self) -> int:
        """LoRA rank."""
        return self.lora_a.shape[0]
    
    @property
    def in_features(self) -> int:
        """Input dimension."""
        return self.lora_a.shape[1]
    
    @property
    def out_features(self) -> int:
        """Output dimension."""
        return self.lora_b.shape[0]
    
    def forward(
        self,
        x: NDArray[np.float32],
        apply_dropout: bool = False,
    ) -> NDArray[np.float32]:
        """Compute LoRA output."""
        # x @ A.T @ B.T * scaling
        hidden = x @ self.lora_a.T  # [..., rank]
        
        if apply_dropout and self.dropout > 0:
            mask = np.random.binomial(1, 1 - self.dropout, hidden.shape)
            hidden = hidden * mask / (1 - self.dropout)
        
        output = hidden @ self.lora_b.T  # [..., out_features]
        return output * self.scaling
    
    def merge_into_base(
        self,
        base_weight: NDArray[np.float32],
    ) -> NDArray[np.float32]:
        """Merge LoRA weights into base weight."""
        # W_merged = W_base + B @ A * scaling
        delta = self.lora_b @ self.lora_a * self.scaling
        return base_weight + delta
    
    def get_memory_bytes(self) -> int:
        """Memory usage in bytes."""
        return self.lora_a.nbytes + self.lora_b.nbytes


@dataclass
class PackedLoRAWeights:
    """Packed LoRA weights for fused QKV or gate+up projections."""
    lora_a: NDArray[np.float32]  # [num_layers, rank, in_features]
    lora_b: NDArray[np.float32]  # [num_layers, out_features, rank]
    scalings: list[float]
    module_names: list[str]
    
    @classmethod
    def from_individual(
        cls,
        layer_weights: list[LoRALayerWeights],
    ) -> PackedLoRAWeights:
        """Create packed weights from individual layer weights."""
        if not layer_weights:
            raise ValueError("layer_weights cannot be empty")
        
        lora_a = np.stack([lw.lora_a for lw in layer_weights])
        lora_b = np.stack([lw.lora_b for lw in layer_weights])
        scalings = [lw.scaling for lw in layer_weights]
        module_names = [lw.module_name for lw in layer_weights]
        
        return cls(lora_a, lora_b, scalings, module_names)
    
    def unpack(self) -> list[LoRALayerWeights]:
        """Unpack into individual layer weights."""
        return [
            LoRALayerWeights(
                lora_a=self.lora_a[i],
                lora_b=self.lora_b[i],
                scaling=self.scalings[i],
                module_name=self.module_names[i],
            )
            for i in range(len(self.module_names))
        ]
    
    @property
    def num_layers(self) -> int:
        """Number of packed layers."""
        return len(self.module_names)
