# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
GPU-resident input buffers for batch management.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)

# Try to import torch, but provide fallback for testing
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # type: ignore


class InputBuffers:
    """
    Pre-allocated GPU tensors for batch inputs.

    Maintains persistent buffers to avoid runtime allocation overhead.
    CUDA graph compatible through fixed-size allocation.
    """

    def __init__(
        self,
        max_num_reqs: int,
        max_num_tokens: int,
        inputs_embeds_size: int,
        vocab_size: int,
        dtype: Any,  # torch.dtype
        device: Any,  # torch.device
    ):
        self.max_num_reqs = max_num_reqs
        self.max_num_tokens = max_num_tokens
        self.device = device
        self.dtype = dtype
        self.vocab_size = vocab_size

        if not HAS_TORCH:
            # Fallback to numpy for testing
            self._init_numpy_buffers(max_num_reqs, max_num_tokens)
            return

        # Core input tensors
        self.input_ids = torch.zeros(max_num_tokens, dtype=torch.int32, device=device)
        self.positions = torch.zeros(max_num_tokens, dtype=torch.int64, device=device)
        self.query_start_loc = torch.zeros(max_num_reqs + 1, dtype=torch.int32, device=device)
        self.seq_lens = torch.zeros(max_num_reqs, dtype=torch.int32, device=device)

        # Multi-rope positions (with dummy for non-contiguous)
        self.mrope_positions = torch.zeros((3, max_num_tokens + 1), dtype=torch.int64, device=device)

        # Logits indices
        self.logits_indices = torch.zeros(max_num_reqs, dtype=torch.int32, device=device)
        self.cu_num_logits = torch.zeros(max_num_reqs + 1, dtype=torch.int32, device=device)

        # Optional embeddings
        if inputs_embeds_size > 0:
            self.inputs_embeds = torch.zeros(
                (max_num_tokens, inputs_embeds_size), dtype=dtype, device=device
            )
        else:
            self.inputs_embeds = None

        logger.debug(
            f"InputBuffers initialized: max_reqs={max_num_reqs}, max_tokens={max_num_tokens}"
        )

    def _init_numpy_buffers(self, max_num_reqs: int, max_num_tokens: int) -> None:
        """Initialize numpy buffers for testing without torch."""
        self.input_ids = np.zeros(max_num_tokens, dtype=np.int32)
        self.positions = np.zeros(max_num_tokens, dtype=np.int64)
        self.query_start_loc = np.zeros(max_num_reqs + 1, dtype=np.int32)
        self.seq_lens = np.zeros(max_num_reqs, dtype=np.int32)
        self.mrope_positions = np.zeros((3, max_num_tokens + 1), dtype=np.int64)
        self.logits_indices = np.zeros(max_num_reqs, dtype=np.int32)
        self.cu_num_logits = np.zeros(max_num_reqs + 1, dtype=np.int32)
        self.inputs_embeds = None
