#!/usr/bin/env python3
from __future__ import annotations
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


"""LoRA layer weight implementations."""

from dataclasses import dataclass

import numpy as np

try:
    from numpy.typing import NDArray
except ImportError:
    from typing import Any

    NDArray = Any

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None


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
        # Try Rust acceleration for inference
        if rc and not apply_dropout and hasattr(rc, "lora_forward_rust"):
            try:
                # Handle ndarray to flat list
                orig_shape = x.shape
                x_flat = x.reshape(-1, self.in_features).astype(np.float32)
                batch_size = x_flat.shape[0]

                result_flat = rc.lora_forward_rust(
                    x_flat.flatten().tolist(),
                    self.lora_a.flatten().tolist(),
                    self.lora_b.flatten().tolist(),
                    batch_size,
                    self.in_features,
                    self.out_features,
                    self.rank,
                    self.scaling,
                )

                # Reshape back to original dimensions as needed
                new_shape = list(orig_shape[:-1]) + [self.out_features]
                return np.array(result_flat, dtype=np.float32).reshape(new_shape)
            except Exception:  # pylint: disable=broad-exception-caught
                pass

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
        # Try Rust acceleration
        if rc and hasattr(rc, "lora_merge_rust"):
            try:
                merged_flat = rc.lora_merge_rust(
                    base_weight.flatten().tolist(),
                    self.lora_a.flatten().tolist(),
                    self.lora_b.flatten().tolist(),
                    self.out_features,
                    self.in_features,
                    self.rank,
                    self.scaling,
                )
                return np.array(merged_flat, dtype=np.float32).reshape(base_weight.shape)
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        # W_merged = W_base + B @ A * scaling
        delta = self.lora_b @ self.lora_a * self.scaling
        return base_weight + delta

    def get_memory_bytes(self) -> int:
        """Memory usage in bytes."""
        return self.lora_a.nbytes + self.lora_b.nbytes


@dataclass
class IA3LayerWeights:
    """IA3 (Input-Activation-Attention Scaling) weights for a single layer."""
    scaling_vector: NDArray[np.float32]  # [features]
    module_name: str

    def forward(
        self,
        x: NDArray[np.float32],
    ) -> NDArray[np.float32]:
        """Apply IA3 scaling."""
        if rc and hasattr(rc, "apply_ia3_scaling_rust"):
            try:
                res = rc.apply_ia3_scaling_rust(x.flatten().tolist(), self.scaling_vector.tolist())
                return np.array(res, dtype=np.float32).reshape(x.shape)
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        return x * self.scaling_vector

    def get_memory_bytes(self) -> int:
        """Memory usage in bytes."""
        return self.scaling_vector.nbytes


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
    ) -> "PackedLoRAWeights":
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
