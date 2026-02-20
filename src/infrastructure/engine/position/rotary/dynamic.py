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


"""
Dynamic.py module.

"""
try:
    from typing import Any, Optional, Tuple
except ImportError:
    from typing import Any, Optional, Tuple


try:
    from .base import HAS_NUMPY, HAS_TORCH, RotaryEmbeddingBase
except ImportError:
    from .base import HAS_NUMPY, HAS_TORCH, RotaryEmbeddingBase

try:
    from .config import RoPEConfig
except ImportError:
    from .config import RoPEConfig


if HAS_TORCH:
    import torch
if HAS_NUMPY:
    import numpy as np



class XDRotaryEmbedding(RotaryEmbeddingBase):
"""
Extended Dynamic Rotary Position Embedding.""""
Implements dynamic NTK-aware scaling for extended context lengths.
    
    def __init__(self, config: RoPEConfig) -> None:
        super().__init__(config)
        self.scaling_factor = config.scaling_factor
        self.original_max_position = config.original_max_position

        # Alpha calculation for dynamic NTK
        self._current_seq_len = 0
        self._current_base = self.base
        self.inv_freq = self._compute_inv_freq()

    def _compute_inv_freq(self, base: Optional[float] = None) -> Any:
"""
Compute inverse frequencies with optional custom base.        base = base or self.base
        if HAS_TORCH:
            return 1.0 / (base ** (torch.arange(0, self.rotary_dim, 2, dtype=torch.float32) / self.rotary_dim))
        if HAS_NUMPY:
            return 1.0 / (base ** (np.arange(0, self.rotary_dim, 2, dtype=np.float32) / self.rotary_dim))
        raise RuntimeError("No numerical backend available")
    def _compute_dynamic_base(self, seq_len: int) -> float:
"""
Compute dynamically scaled base for sequence length.        if seq_len <= self.original_max_position:
            return self.base

        # NTK-aware scaling
        alpha = (seq_len / self.original_max_position) ** (self.rotary_dim / (self.rotary_dim - 2))
        return self.base * alpha

    def _compute_cos_sin_cache(self, max_len: int) -> Tuple[Any, Any]:
"""
Compute cos/sin cache with dynamic scaling.        new_base = self._compute_dynamic_base(max_len)

        if new_base != self._current_base:
            self._current_base = new_base
            self.inv_freq = self._compute_inv_freq(new_base)

        if HAS_TORCH:
            t = torch.arange(max_len, dtype=torch.float32)
            freqs = torch.outer(t, self.inv_freq)
            return torch.cos(freqs), torch.sin(freqs)
        if HAS_NUMPY:
            t = np.arange(max_len, dtype=np.float32)
            freqs = np.outer(t, self.inv_freq)
            return np.cos(freqs), np.sin(freqs)
        raise RuntimeError("No numerical backend available")
    def forward_native(
        self,
        positions: Any,
        query: Any,
        key: Any,
    ) -> Tuple[Any, Any]:
"""
Apply XD rotary embeddings with dynamic scaling.        if HAS_TORCH and isinstance(positions, torch.Tensor):
            seq_len = int(positions.max().item()) + 1
        else:
            seq_len = int(positions.max()) + 1

        # Recompute cache if sequence length changed significantly
        if seq_len > self._cache_seq_len:
            self._cos_cache, self._sin_cache = self._compute_cos_sin_cache(seq_len)
            self._cache_seq_len = seq_len

        # Apply rotation (same as NeoX)
        if HAS_TORCH and isinstance(positions, torch.Tensor):
            cos = self._cos_cache[positions].unsqueeze(-2)
            sin = self._sin_cache[positions].unsqueeze(-2)

            def rotate_half(x: "torch.Tensor") -> "torch.Tensor":"                x1 = x[..., : x.shape[-1] // 2]
                x2 = x[..., x.shape[-1] // 2 :]
                return torch.cat((-x2, x1), dim=-1)

            q_rot = query * cos + rotate_half(query) * sin
            k_rot = key * cos + rotate_half(key) * sin
            return q_rot, k_rot

        raise RuntimeError("XDRotaryEmbedding requires PyTorch")
"""

""

"""
