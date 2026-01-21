# SPDX-License-Identifier: Apache-2.0
"""
Hybrid Mamba Mixer - Combining SSM with Attention.
"""

from __future__ import annotations

import math
import numpy as np

from src.infrastructure.compute.ssm.mamba.config import MambaConfig, MambaState, MambaOutput
from src.infrastructure.compute.ssm.mamba.mixer import MambaMixer


class HybridMambaMixer:
    """
    Hybrid layer combining Mamba SSM with attention.
    """

    def __init__(
        self,
        config: MambaConfig,
        num_attention_heads: int = 8,
        attention_ratio: float = 0.25,
    ) -> None:
        self.config = config
        self.num_attention_heads = num_attention_heads
        self.attention_ratio = attention_ratio

        # Split dimensions
        self.attn_dim = int(config.d_inner * attention_ratio)
        self.ssm_dim = config.d_inner - self.attn_dim

        # SSM component
        ssm_config = MambaConfig(
            hidden_size=self.ssm_dim,
            ssm_state_size=config.ssm_state_size,
            conv_kernel_size=config.conv_kernel_size,
            intermediate_size=self.ssm_dim,
            use_rms_norm=config.use_rms_norm,
        )
        self.ssm = MambaMixer(ssm_config)

        # Simple attention component
        self.q_proj = np.random.randn(self.attn_dim, config.hidden_size).astype(np.float32) * 0.01
        self.k_proj = np.random.randn(self.attn_dim, config.hidden_size).astype(np.float32) * 0.01
        self.v_proj = np.random.randn(self.attn_dim, config.hidden_size).astype(np.float32) * 0.01
        self.o_proj = np.random.randn(config.hidden_size, config.d_inner).astype(np.float32) * 0.01

        self.scale = 1.0 / math.sqrt(self.attn_dim // num_attention_heads)

    def forward(
        self,
        hidden_states: np.ndarray,
        state: MambaState | None = None,
    ) -> MambaOutput:
        """Forward with hybrid SSM + attention."""
        batch_size, seq_len, _ = hidden_states.shape

        # SSM path
        ssm_input = hidden_states[:, :, :self.ssm_dim]
        if state is not None:
            ssm_state = MambaState(
                conv_state=state.conv_state[:, :self.ssm_dim],
                ssm_state=state.ssm_state[:, :self.ssm_dim],
            )
        else:
            ssm_state = None

        ssm_output = self.ssm.forward(ssm_input, ssm_state)

        # Attention path
        Q = hidden_states @ self.q_proj.T
        K = hidden_states @ self.k_proj.T
        V = hidden_states @ self.v_proj.T

        # Reshape for multi-head
        head_dim = self.attn_dim // self.num_attention_heads
        Q = Q.reshape(batch_size, seq_len, self.num_attention_heads, head_dim)
        K = K.reshape(batch_size, seq_len, self.num_attention_heads, head_dim)
        V = V.reshape(batch_size, seq_len, self.num_attention_heads, head_dim)

        # Attention scores
        # scores = [batch, heads, seq_len, seq_len]
        scores = np.einsum('bqhd,bkhd->bhqk', Q, K) * self.scale

        # Causal mask
        mask = np.triu(np.ones((seq_len, seq_len)), k=1) * -1e9
        scores = scores + mask

        # Softmax and weighted sum
        attn_weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
        attn_weights = attn_weights / attn_weights.sum(axis=-1, keepdims=True)
        attn_output = np.einsum('bhqk,bkhd->bqhd', attn_weights, V)
        attn_output = attn_output.reshape(batch_size, seq_len, self.attn_dim)

        # Combine outputs
        combined = np.concatenate([ssm_output.output, attn_output], axis=-1)
        output = combined @ self.o_proj.T

        return MambaOutput(output=output, state=ssm_output.state)
