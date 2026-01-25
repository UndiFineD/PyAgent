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
Multimodal.py module.
"""

from typing import Any, Tuple

from .base import HAS_TORCH, RotaryEmbeddingBase
from .config import RoPEConfig

if HAS_TORCH:
    import torch
else:
    torch = None  # pylint: disable=invalid-name


class MRotaryEmbedding(RotaryEmbeddingBase):
    """Multimodal Rotary Position Embedding.

    Applies separate rotary embeddings for different modality sections:
    - Temporal (time/frame index)
    - Height (spatial y)
    - Width (spatial x)
    """

    def __init__(self, config: RoPEConfig):
        super().__init__(config)
        self.mrope_sections = config.mrope_sections or [8, 8, 8]
        assert len(self.mrope_sections) == 3, "Need 3 sections: temporal, height, width"
        assert sum(self.mrope_sections) * 2 <= self.rotary_dim

        self.inv_freq = self._compute_inv_freq()

    def _compute_inv_freq(self) -> Any:
        """Compute inverse frequencies for each section."""
        if not HAS_TORCH:
            raise RuntimeError("MRotaryEmbedding requires PyTorch")

        inv_freqs = []
        for section_size in self.mrope_sections:
            inv_freq = 1.0 / (
                self.base ** (torch.arange(0, section_size * 2, 2, dtype=torch.float32) / (section_size * 2))
            )
            inv_freqs.append(inv_freq)
        return inv_freqs

    def _compute_cos_sin_cache(self, max_len: int) -> Tuple[Any, Any]:
        """Compute cos/sin cache for each section."""
        if not HAS_TORCH:
            raise RuntimeError("MRotaryEmbedding requires PyTorch")

        t = torch.arange(max_len, dtype=torch.float32)

        cos_caches = []
        sin_caches = []

        for inv_freq in self.inv_freq:
            freqs = torch.outer(t, inv_freq)
            cos_caches.append(torch.cos(freqs))
            sin_caches.append(torch.sin(freqs))

        return cos_caches, sin_caches

    def forward_native(
        self,
        positions: Any,  # [3, seq_len] for temporal, height, width
        query: Any,
        key: Any,
    ) -> Tuple[Any, Any]:
        """Apply multimodal rotary embeddings."""
        if not HAS_TORCH:
            raise RuntimeError("MRotaryEmbedding requires PyTorch")

        if positions.dim() == 1:
            # Fallback to single positions
            positions = positions.unsqueeze(0).expand(3, -1)

        seq_len = int(positions.max().item()) + 1
        if self._cache_seq_len < seq_len:
            self._cos_cache, self._sin_cache = self._compute_cos_sin_cache(max(seq_len, 2048))
            self._cache_seq_len = max(seq_len, 2048)

        # Apply rotation for each section
        q_parts = []
        k_parts = []

        dim_offset = 0
        for i, section_size in enumerate(self.mrope_sections):
            section_dim = section_size * 2
            pos_i = positions[i]  # [seq_len]

            cos = self._cos_cache[i][pos_i]  # [seq_len, section_size]
            sin = self._sin_cache[i][pos_i]

            q_section = query[..., dim_offset : dim_offset + section_dim]
            k_section = key[..., dim_offset : dim_offset + section_dim]

            # Apply rotation
            q_rot, k_rot = self._apply_rotation(q_section, k_section, cos, sin)
            q_parts.append(q_rot)
            k_parts.append(k_rot)

            dim_offset += section_dim

        # Passthrough for remaining dimensions
        if dim_offset < query.shape[-1]:
            q_parts.append(query[..., dim_offset:])
            k_parts.append(key[..., dim_offset:])

        return torch.cat(q_parts, dim=-1), torch.cat(k_parts, dim=-1)

    def _apply_rotation(
        self,
        q: "torch.Tensor",
        k: "torch.Tensor",
        cos: "torch.Tensor",
        sin: "torch.Tensor",
    ) -> Tuple["torch.Tensor", "torch.Tensor"]:
        """Apply rotation to a section."""

        def rotate_half(x: "torch.Tensor") -> "torch.Tensor":
            x1 = x[..., : x.shape[-1] // 2]
            x2 = x[..., x.shape[-1] // 2 :]
            return torch.cat((-x2, x1), dim=-1)

        cos = cos.unsqueeze(-2)
        sin = sin.unsqueeze(-2)

        q_rot = q * cos + rotate_half(q) * sin
        k_rot = k * cos + rotate_half(k) * sin

        return q_rot, k_rot
