# SPDX-License-Identifier: Apache-2.0
"""
Mamba Mixer - Implementation of Mamba-1 and Mamba-2 mixer layers.
"""

from __future__ import annotations

import math
import numpy as np

# Optional torch import
try:
    import torch
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # type: ignore
    F = None  # type: ignore

from src.infrastructure.compute.ssm.mamba.config import MambaConfig, MambaState, MambaOutput
from src.infrastructure.compute.ssm.mamba.ops import CausalConv1d, SelectiveScan


class MambaMixer:
    """
    Mamba-1 Mixer layer.
    """

    def __init__(self, config: MambaConfig) -> None:
        self.config = config

        # In projection: hidden_size -> 2 * d_inner
        self.in_proj_weight = np.random.randn(
            2 * config.d_inner, config.hidden_size
        ).astype(np.float32) * (1.0 / math.sqrt(config.hidden_size))
        self.in_proj_bias = np.zeros(2 * config.d_inner, dtype=np.float32) if config.use_bias else None

        # Causal conv1d
        self.conv1d = CausalConv1d(
            in_channels=config.d_inner,
            kernel_size=config.conv_kernel_size,
            bias=config.use_conv_bias,
        )

        # X projection for dt, B, C
        self.x_proj_weight = np.random.randn(
            config.dt_rank + 2 * config.ssm_state_size,
            config.d_inner,
        ).astype(np.float32) * (1.0 / math.sqrt(config.d_inner))

        # dt projection
        self.dt_proj_weight = np.random.randn(
            config.d_inner, config.dt_rank
        ).astype(np.float32) * (1.0 / math.sqrt(config.dt_rank))
        self.dt_proj_bias = np.zeros(config.d_inner, dtype=np.float32)

        # Selective scan
        self.ssm = SelectiveScan(config.d_inner, config.ssm_state_size)

        # Output projection
        self.out_proj_weight = np.random.randn(
            config.hidden_size, config.d_inner
        ).astype(np.float32) * (1.0 / math.sqrt(config.d_inner))
        self.out_proj_bias = np.zeros(config.hidden_size, dtype=np.float32) if config.use_bias else None

        # RMS norm layers
        self.dt_layernorm_weight = np.ones(config.dt_rank, dtype=np.float32)
        self.b_layernorm_weight = np.ones(config.ssm_state_size, dtype=np.float32)
        self.c_layernorm_weight = np.ones(config.ssm_state_size, dtype=np.float32)

    def _silu(self, x: np.ndarray) -> np.ndarray:
        """SiLU activation."""
        return x * (1 / (1 + np.exp(-x)))

    def _rms_norm(self, x: np.ndarray, weight: np.ndarray) -> np.ndarray:
        """RMS normalization."""
        variance = np.mean(x ** 2, axis=-1, keepdims=True)
        x_normed = x / np.sqrt(variance + self.config.rms_norm_eps)
        return x_normed * weight

    def forward(
        self,
        hidden_states: np.ndarray,
        state: MambaState | None = None,
    ) -> MambaOutput:
        """Forward pass through Mamba mixer."""
        batch_size, seq_len, _ = hidden_states.shape
        if state is None:
            state = MambaState.zeros(batch_size, self.config, hidden_states.dtype)

        projected = hidden_states @ self.in_proj_weight.T
        if self.in_proj_bias is not None:
            projected = projected + self.in_proj_bias

        x, gate = np.split(projected, 2, axis=-1)
        x_conv, new_conv_state = self.conv1d.forward(x, state.conv_state)
        x_conv = self._silu(x_conv)

        x_dbl = x_conv @ self.x_proj_weight.T
        dt, B, C = np.split(
            x_dbl,
            [self.config.dt_rank, self.config.dt_rank + self.config.ssm_state_size],
            axis=-1,
        )

        if self.config.use_rms_norm:
            dt = self._rms_norm(dt, self.dt_layernorm_weight)
            B = self._rms_norm(B, self.b_layernorm_weight)
            C = self._rms_norm(C, self.c_layernorm_weight)

        dt = dt @ self.dt_proj_weight.T + self.dt_proj_bias
        dt = F.softplus(torch.from_numpy(dt)).numpy() if HAS_TORCH else np.log1p(np.exp(dt))

        ssm_out, new_ssm_state = self.ssm.forward(x_conv, dt, B, C, state.ssm_state)

        output = ssm_out * self._silu(gate)
        output = output @ self.out_proj_weight.T
        if self.out_proj_bias is not None:
            output = output + self.out_proj_bias

        return MambaOutput(
            output=output,
            state=MambaState(conv_state=new_conv_state, ssm_state=new_ssm_state),
        )

    def step(
        self,
        hidden_states: np.ndarray,
        state: MambaState,
    ) -> MambaOutput:
        """Single-step update for decoding."""
        projected = hidden_states @ self.in_proj_weight.T
        if self.in_proj_bias is not None:
            projected = projected + self.in_proj_bias

        x, gate = np.split(projected, 2, axis=-1)
        x_conv, new_conv_state = self.conv1d.update(x, state.conv_state)
        x_conv = self._silu(x_conv)

        x_dbl = x_conv @ self.x_proj_weight.T
        dt, B, C = np.split(
            x_dbl,
            [self.config.dt_rank, self.config.dt_rank + self.config.ssm_state_size],
            axis=-1,
        )

        if self.config.use_rms_norm:
            dt = self._rms_norm(dt, self.dt_layernorm_weight)
            B = self._rms_norm(B, self.b_layernorm_weight)
            C = self._rms_norm(C, self.c_layernorm_weight)

        dt = dt @ self.dt_proj_weight.T + self.dt_proj_bias
        dt = np.log1p(np.exp(dt))  # softplus

        ssm_out, new_ssm_state = self.ssm.update(x_conv, dt, B, C, state.ssm_state)

        output = ssm_out * self._silu(gate)
        output = output @ self.out_proj_weight.T
        if self.out_proj_bias is not None:
            output = output + self.out_proj_bias

        return MambaOutput(
            output=output,
            state=MambaState(conv_state=new_conv_state, ssm_state=new_ssm_state),
        )


class Mamba2Mixer(MambaMixer):
    """
    Mamba-2 Mixer with multi-head SSM.
    """

    def __init__(
        self,
        config: MambaConfig,
        num_heads: int = 8,
    ) -> None:
        super().__init__(config)
        self.num_heads = num_heads
        assert config.d_inner % num_heads == 0
        self.head_dim = config.d_inner // num_heads

        # Multi-head A matrix
        self.ssm.A = -np.exp(
            np.random.randn(num_heads, self.head_dim, config.ssm_state_size).astype(np.float32) * 0.5
        )
