# SPDX-License-Identifier: Apache-2.0
"""
STEM: Dynamic Embedding Expansion for long-context handling.
Implemented based on arXiv:2601.10639 (STEM Scaling, Jan 2026).
"""

import torch
import torch.nn as nn
from typing import Optional

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
