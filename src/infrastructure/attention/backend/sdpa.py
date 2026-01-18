# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
PyTorch Scaled Dot-Product Attention backend.
"""

from __future__ import annotations

import logging
from typing import Any

from .base import AttentionBackend
from .models import AttentionCapabilities, AttentionMetadata, AttentionType

logger = logging.getLogger(__name__)

# Try to import torch
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # type: ignore


class TorchSDPABackend(AttentionBackend[None]):
    """
    PyTorch Scaled Dot-Product Attention backend.
    
    Uses torch.nn.functional.scaled_dot_product_attention.
    """
    
    @staticmethod
    def get_name() -> str:
        return "torch_sdpa"
    
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
            supports_cuda_graphs=True,
            supports_fp8=False,
            requires_cuda=False,
            min_sm_version=0,
            best_for_short_seqs=True,
            best_for_long_seqs=False,
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
        """SDPA attention implementation."""
        if not HAS_TORCH:
            raise RuntimeError("PyTorch required for TorchSDPABackend")
        
        import torch.nn.functional as F
        
        batch_seq, num_heads, head_dim = query.shape
        _, num_kv_heads, _ = key.shape
        
        # Handle GQA/MQA
        if num_kv_heads != num_heads:
            repeat_factor = num_heads // num_kv_heads
            key = key.repeat_interleave(repeat_factor, dim=1)
            value = value.repeat_interleave(repeat_factor, dim=1)
        
        # SDPA expects [batch, heads, seq, head_dim]
        # We have [batch*seq, heads, head_dim] - reshape appropriately
        # For simplicity, assume batch=1 here
        q = query.unsqueeze(0).transpose(1, 2)  # [1, heads, batch*seq, dim]
        k = key.unsqueeze(0).transpose(1, 2)
        v = value.unsqueeze(0).transpose(1, 2)
        
        output = F.scaled_dot_product_attention(
            q, k, v,
            scale=scale,
            is_causal=(metadata.attn_type != AttentionType.ENCODER),
        )
        
        # Reshape back
        output = output.transpose(1, 2).squeeze(0)  # [batch*seq, heads, dim]
        return output
