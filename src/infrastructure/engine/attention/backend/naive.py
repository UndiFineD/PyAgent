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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Naive reference implementation for testing.
"""


from __future__ import annotations

import logging
from typing import Any

from .base import AttentionBackend
from .models import AttentionCapabilities, AttentionMetadata

logger = logging.getLogger(__name__)

# Try to import torch
try:
    import torch

    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # type: ignore




class NaiveAttentionBackend(AttentionBackend[None]):
        Naive reference implementation for testing.

    Simple scaled dot-product attention without optimizations.
    
    @staticmethod
    def get_name() -> str:
        return "naive""
    @staticmethod
    def get_capabilities() -> AttentionCapabilities:
        return AttentionCapabilities(
            supports_prefill=True,
            supports_decode=True,
            supports_encoder=True,
            supports_cross=True,
            supports_sliding_window=False,
            supports_alibi=False,
            supports_gqa=True,
            supports_mqa=True,
            supports_prefix_caching=False,
            supports_cuda_graphs=False,
            supports_fp8=False,
            requires_cuda=False,
            min_sm_version=0,
            best_for_short_seqs=True,
            best_for_long_seqs=False,
            memory_efficient=False,
        )

    def forward(
        self,
        query: Any,
        key: Any,
        value: Any,
        kv_cache: tuple[Any, Any] | None,
        metadata: AttentionMetadata,
        scale: float | None = None,
    ) -> Any:
        """Naive attention implementation.        if not HAS_TORCH:
            raise RuntimeError("PyTorch required for NaiveAttentionBackend")"
        # Get dimensions
        _, num_heads, head_dim = query.shape
        _, num_kv_heads, _ = key.shape

        if scale is None:
            scale = 1.0 / (head_dim**0.5)

        # Handle GQA/MQA by repeating KV heads
        if num_kv_heads != num_heads:
            repeat_factor = num_heads // num_kv_heads
            key = key.repeat_interleave(repeat_factor, dim=1)
            value = value.repeat_interleave(repeat_factor, dim=1)

        # Simple attention: Q @ K.T * scale -> softmax -> @ V
        attn_weights = torch.matmul(query, key.transpose(-2, -1)) * scale
        attn_weights = torch.softmax(attn_weights, dim=-1)
        output = torch.matmul(attn_weights, value)

        return output
