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

# SPDX-License-Identifier: Apache-2.0
"""
STEM: Dynamic Embedding Expansion for long-context handling.
Implemented based on arXiv:2601.10639 (STEM Scaling, Jan 2026).
"""

import torch
from torch import nn


class STEMScalingLayer(nn.Module):
    """
    Implements the STEM (Dynamic Embedding Expansion) logic.
    Optimizes embeddings for ultra-long contexts (1M+ tokens).
    """

    def __init__(self, hidden_dim: int, expansion_factor: int = 4):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.expansion_factor = expansion_factor

        # STEM scaling parameters
        self.scaling_weight = nn.Parameter(torch.ones(hidden_dim))
        self.expansion_proj = nn.Linear(hidden_dim, hidden_dim * expansion_factor)
        self.contraction_proj = nn.Linear(hidden_dim * expansion_factor, hidden_dim)

    def forward(self, x: torch.Tensor, context_length: int) -> torch.Tensor:
        """
        Apply STEM scaling based on context length.
        """
        # Context-aware scaling factor
        # STEM suggests scaling increases logarithmically with context length
        scale = torch.log2(torch.tensor(context_length, dtype=x.dtype, device=x.device)) / 20.0
        scale = torch.clamp(scale, min=1.0)

        # Apply scaling
        x = x * self.scaling_weight * scale

        # Higher-order expansion for long contexts
        if context_length > 32768:
            expanded = torch.relu(self.expansion_proj(x))
            x = self.contraction_proj(expanded)

        return x


class STEMManager:
    """
    Manages STEM scaling across layers and context windows.
    """

    def __init__(self, hidden_dim: int):
        self.layer = STEMScalingLayer(hidden_dim)

    def process_hidden_states(self, hidden_states: torch.Tensor, current_context_len: int) -> torch.Tensor:
        """Apply STEM processing to hidden states."""
        return self.layer(hidden_states, current_context_len)
