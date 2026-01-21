# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
FlashAttention-2 backend.
"""

from __future__ import annotations

import logging
from typing import Any

from .base import AttentionBackend
from .models import AttentionCapabilities, AttentionMetadata, AttentionType
from .sdpa import TorchSDPABackend

logger = logging.getLogger(__name__)


class FlashAttentionBackend(AttentionBackend[None]):
    """
    FlashAttention-2 backend.

    Optimized attention using tiling and recomputation.
    """

    @staticmethod
    def get_name() -> str:
        return "flash_attn"

    @staticmethod
    def get_capabilities() -> AttentionCapabilities:
        return AttentionCapabilities(
            supports_prefill=True,
            supports_decode=True,
            supports_encoder=True,
            supports_cross=True,
            supports_sliding_window=True,
            supports_alibi=True,
            supports_gqa=True,
            supports_mqa=True,
            supports_prefix_caching=True,
            supports_cuda_graphs=True,
            supports_fp8=False,
            requires_cuda=True,
            requires_bf16=False,
            min_sm_version=80,  # Ampere+
            best_for_short_seqs=True,
            best_for_long_seqs=True,
            memory_efficient=True,
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
        """FlashAttention implementation."""
        try:
            from flash_attn import flash_attn_func
        except ImportError:
            logger.warning("flash_attn not available, falling back to SDPA")
            return TorchSDPABackend().forward(
                query, key, value, kv_cache, metadata, scale
            )

        # FlashAttention expects [batch, seqlen, heads, head_dim]
        # Reshape accordingly
        batch_seq, num_heads, head_dim = query.shape

        q = query.unsqueeze(0)  # Add batch dim
        k = key.unsqueeze(0)
        v = value.unsqueeze(0)

        # Compute
        output = flash_attn_func(
            q, k, v,
            softmax_scale=scale,
            causal=(metadata.attn_type != AttentionType.ENCODER),
            window_size=(metadata.sliding_window, metadata.sliding_window)
            if metadata.sliding_window else (-1, -1),
        )

        return output.squeeze(0)
