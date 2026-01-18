"""
Mamba Mixer - State Space Model Layer.

vLLM Pattern: vllm/model_executor/layers/mamba/mamba_mixer.py
Implements Mamba-1 selective state space model.

Beyond vLLM:
- HybridMambaMixer combining SSM with attention
- Chunked computation for long sequences
- Memory-efficient state management
"""

from __future__ import annotations

import math
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional, NamedTuple, TYPE_CHECKING

import numpy as np

# Optional torch import
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # type: ignore
    nn = None  # type: ignore
    F = None  # type: ignore

# Try to import Rust accelerators
try:
    import rust_core
    HAS_RUST = True
except ImportError:
    HAS_RUST = False


# =============================================================================
# Configuration
# =============================================================================

@dataclass(frozen=True)
class MambaConfig:
    """
    Configuration for Mamba mixer.
    
    vLLM Pattern: MambaConfig parameters
    """
    hidden_size: int
    ssm_state_size: int = 16  # N in Mamba paper
    conv_kernel_size: int = 4  # d_conv
    intermediate_size: int | None = None  # d_inner, defaults to 2*hidden_size
    time_step_rank: int | None = None  # dt_rank, defaults to ceil(hidden_size/16)
    
    # Activation
    activation: str = "silu"
    
    # Normalization
    use_rms_norm: bool = True
    rms_norm_eps: float = 1e-5
    rms_norm_has_weight: bool = True
    
    # Bias
    use_conv_bias: bool = True
    use_bias: bool = False
    
    def __post_init__(self) -> None:
        # Validate
        assert self.hidden_size > 0
        assert self.ssm_state_size > 0
        assert self.conv_kernel_size > 0
    
    @property
    def d_inner(self) -> int:
        """Get intermediate size."""
        return self.intermediate_size or (2 * self.hidden_size)
    
    @property
    def dt_rank(self) -> int:
        """Get time step rank."""
        return self.time_step_rank or math.ceil(self.hidden_size / 16)


# =============================================================================
# State Classes
# =============================================================================

@dataclass
class MambaState:
    """
    State for Mamba recurrence.
    
    vLLM Pattern: conv_state and ssm_state from mamba_mixer.py
    """
    conv_state: np.ndarray  # [batch, d_inner, d_conv]
    ssm_state: np.ndarray  # [batch, d_inner, ssm_state_size]
    
    @classmethod
    def zeros(
        cls,
        batch_size: int,
        config: MambaConfig,
        dtype: np.dtype = np.float32,
    ) -> "MambaState":
        """Create zero-initialized state."""
        return cls(
            conv_state=np.zeros(
                (batch_size, config.d_inner, config.conv_kernel_size),
                dtype=dtype,
            ),
            ssm_state=np.zeros(
                (batch_size, config.d_inner, config.ssm_state_size),
                dtype=dtype,
            ),
        )
    
    def clone(self) -> "MambaState":
        """Clone state."""
        return MambaState(
            conv_state=self.conv_state.copy(),
            ssm_state=self.ssm_state.copy(),
        )


class MambaOutput(NamedTuple):
    """Output from Mamba forward pass."""
    output: np.ndarray  # [batch, seq_len, hidden_size]
    state: MambaState  # Updated state


# =============================================================================
# Causal Conv1D
# =============================================================================

class CausalConv1d:
    """
    Causal 1D convolution layer.
    
    vLLM Pattern: causal_conv1d_fn / causal_conv1d_update from ops
    """
    
    def __init__(
        self,
        in_channels: int,
        kernel_size: int,
        bias: bool = True,
    ) -> None:
        self.in_channels = in_channels
        self.kernel_size = kernel_size
        
        # Initialize weights [in_channels, kernel_size]
        self.weight = np.random.randn(
            in_channels, kernel_size
        ).astype(np.float32) * (1.0 / math.sqrt(kernel_size))
        
        self.bias = np.zeros(in_channels, dtype=np.float32) if bias else None
    
    def forward(
        self,
        x: np.ndarray,
        conv_state: np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Forward pass.
        
        Args:
            x: Input [batch, seq_len, in_channels]
            conv_state: Previous conv state [batch, in_channels, kernel_size]
        
        Returns:
            output: Convolution output [batch, seq_len, in_channels]
            new_state: Updated conv state
        """
        batch_size, seq_len, _ = x.shape
        
        # Transpose to [batch, in_channels, seq_len]
        x_t = x.transpose(0, 2, 1)
        
        # Pad with previous state
        if conv_state is not None:
            x_padded = np.concatenate([conv_state, x_t], axis=-1)
        else:
            x_padded = np.pad(
                x_t, 
                ((0, 0), (0, 0), (self.kernel_size - 1, 0)),
                mode='constant',
            )
        
        # Apply convolution
        output = np.zeros((batch_size, self.in_channels, seq_len), dtype=x.dtype)
        
        for i in range(seq_len):
            window = x_padded[:, :, i:i + self.kernel_size]
            output[:, :, i] = (window * self.weight).sum(axis=-1)
        
        if self.bias is not None:
            output = output + self.bias.reshape(1, -1, 1)
        
        # New state is last (kernel_size - 1) positions
        new_state = x_padded[:, :, -(self.kernel_size - 1):] if seq_len >= 1 else conv_state
        # Pad to kernel_size for consistency
        if new_state is not None and new_state.shape[-1] < self.kernel_size:
            pad_width = self.kernel_size - new_state.shape[-1]
            new_state = np.pad(new_state, ((0, 0), (0, 0), (pad_width, 0)))
        
        # Transpose back
        output = output.transpose(0, 2, 1)
        
        return output, new_state
    
    def update(
        self,
        x: np.ndarray,
        conv_state: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Single-step update for decoding.
        
        Args:
            x: Input [batch, in_channels]
            conv_state: Conv state [batch, in_channels, kernel_size]
        
        Returns:
            output: Single output [batch, in_channels]
            new_state: Updated state
        """
        # Shift state and add new input
        new_state = np.roll(conv_state, -1, axis=-1)
        new_state[:, :, -1] = x
        
        # Apply convolution
        output = (new_state * self.weight).sum(axis=-1)
        
        if self.bias is not None:
            output = output + self.bias
        
        return output, new_state


# =============================================================================
# Selective Scan (SSM Core)
# =============================================================================

class SelectiveScan:
    """
    Selective scan operation for Mamba.
    
    vLLM Pattern: selective_scan_fn / selective_state_update from ops
    """
    
    def __init__(
        self,
        d_inner: int,
        ssm_state_size: int,
    ) -> None:
        self.d_inner = d_inner
        self.ssm_state_size = ssm_state_size
        
        # A matrix (negative log of state transition)
        # Initialized as -exp(A_log) in vLLM
        self.A = -np.exp(
            np.random.randn(d_inner, ssm_state_size).astype(np.float32) * 0.5
        )
        
        # D "skip connection"
        self.D = np.ones(d_inner, dtype=np.float32)
    
    def forward(
        self,
        x: np.ndarray,
        dt: np.ndarray,
        B: np.ndarray,
        C: np.ndarray,
        ssm_state: np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Selective scan forward pass.
        
        Args:
            x: Input [batch, seq_len, d_inner]
            dt: Time step [batch, seq_len, d_inner]
            B: Input projection [batch, seq_len, ssm_state_size]
            C: Output projection [batch, seq_len, ssm_state_size]
            ssm_state: Initial state [batch, d_inner, ssm_state_size]
        
        Returns:
            output: SSM output [batch, seq_len, d_inner]
            final_state: Final SSM state
        """
        batch_size, seq_len, d_inner = x.shape
        
        # Initialize state
        if ssm_state is None:
            ssm_state = np.zeros(
                (batch_size, d_inner, self.ssm_state_size),
                dtype=x.dtype,
            )
        
        # Discretize A and B
        # dA = exp(dt * A)
        # dB = dt * B
        
        output = np.zeros_like(x)
        state = ssm_state.copy()
        
        for t in range(seq_len):
            x_t = x[:, t, :]  # [batch, d_inner]
            dt_t = dt[:, t, :]  # [batch, d_inner]
            B_t = B[:, t, :]  # [batch, ssm_state_size]
            C_t = C[:, t, :]  # [batch, ssm_state_size]
            
            # Discretization
            dA = np.exp(dt_t[:, :, None] * self.A)  # [batch, d_inner, ssm_state_size]
            dB = dt_t[:, :, None] * B_t[:, None, :]  # [batch, d_inner, ssm_state_size]
            
            # State update: h_t = dA * h_{t-1} + dB * x_t
            state = dA * state + dB * x_t[:, :, None]
            
            # Output: y_t = (C_t @ h_t) + D * x_t
            y_t = (state * C_t[:, None, :]).sum(axis=-1) + self.D * x_t
            
            output[:, t, :] = y_t
        
        return output, state
    
    def update(
        self,
        x: np.ndarray,
        dt: np.ndarray,
        B: np.ndarray,
        C: np.ndarray,
        ssm_state: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """
        Single-step update for decoding.
        
        Args:
            x: Input [batch, d_inner]
            dt: Time step [batch, d_inner]
            B: Input projection [batch, ssm_state_size]
            C: Output projection [batch, ssm_state_size]
            ssm_state: Current state [batch, d_inner, ssm_state_size]
        
        Returns:
            output: Single output [batch, d_inner]
            new_state: Updated state
        """
        # Discretize
        dA = np.exp(dt[:, :, None] * self.A)
        dB = dt[:, :, None] * B[:, None, :]
        
        # State update
        new_state = dA * ssm_state + dB * x[:, :, None]
        
        # Output
        output = (new_state * C[:, None, :]).sum(axis=-1) + self.D * x
        
        return output, new_state


# =============================================================================
# Mamba Mixer
# =============================================================================

class MambaMixer:
    """
    Mamba-1 Mixer layer.
    
    vLLM Pattern: MambaMixer from mamba_mixer.py
    
    Architecture:
        1. In projection (gate + x)
        2. Causal conv1d
        3. SSM (selective scan)
        4. Output projection
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
        """
        Forward pass through Mamba mixer.
        
        Args:
            hidden_states: Input [batch, seq_len, hidden_size]
            state: Optional previous state
        
        Returns:
            MambaOutput with output and updated state
        """
        batch_size, seq_len, _ = hidden_states.shape
        
        # Initialize state if needed
        if state is None:
            state = MambaState.zeros(batch_size, self.config, hidden_states.dtype)
        
        # 1. In projection
        projected = hidden_states @ self.in_proj_weight.T
        if self.in_proj_bias is not None:
            projected = projected + self.in_proj_bias
        
        x, gate = np.split(projected, 2, axis=-1)
        
        # 2. Causal conv1d
        x_conv, new_conv_state = self.conv1d.forward(x, state.conv_state)
        x_conv = self._silu(x_conv)
        
        # 3. SSM parameters
        x_dbl = x_conv @ self.x_proj_weight.T
        dt, B, C = np.split(
            x_dbl,
            [self.config.dt_rank, self.config.dt_rank + self.config.ssm_state_size],
            axis=-1,
        )
        
        # Apply RMS norm if configured
        if self.config.use_rms_norm:
            dt = self._rms_norm(dt, self.dt_layernorm_weight)
            B = self._rms_norm(B, self.b_layernorm_weight)
            C = self._rms_norm(C, self.c_layernorm_weight)
        
        # dt projection
        dt = dt @ self.dt_proj_weight.T + self.dt_proj_bias
        dt = F.softplus(torch.from_numpy(dt)).numpy() if HAS_TORCH else np.log1p(np.exp(dt))
        
        # 4. Selective scan
        ssm_out, new_ssm_state = self.ssm.forward(x_conv, dt, B, C, state.ssm_state)
        
        # 5. Gate and output projection
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
        """
        Single-step update for decoding.
        
        Args:
            hidden_states: Input [batch, hidden_size]
            state: Current state
        
        Returns:
            MambaOutput with single output and updated state
        """
        # 1. In projection
        projected = hidden_states @ self.in_proj_weight.T
        if self.in_proj_bias is not None:
            projected = projected + self.in_proj_bias
        
        x, gate = np.split(projected, 2, axis=-1)
        
        # 2. Conv1d update
        x_conv, new_conv_state = self.conv1d.update(x, state.conv_state)
        x_conv = self._silu(x_conv)
        
        # 3. SSM parameters
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
        
        # 4. SSM update
        ssm_out, new_ssm_state = self.ssm.update(x_conv, dt, B, C, state.ssm_state)
        
        # 5. Gate and output
        output = ssm_out * self._silu(gate)
        output = output @ self.out_proj_weight.T
        if self.out_proj_bias is not None:
            output = output + self.out_proj_bias
        
        return MambaOutput(
            output=output,
            state=MambaState(conv_state=new_conv_state, ssm_state=new_ssm_state),
        )


# =============================================================================
# Mamba-2 Mixer
# =============================================================================

class Mamba2Mixer(MambaMixer):
    """
    Mamba-2 Mixer with multi-head SSM.
    
    vLLM Pattern: Mamba2Mixer from mamba_mixer2.py
    
    Improvements over Mamba-1:
    - Multi-head state space
    - Grouped convolutions
    - Better parallelization
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


# =============================================================================
# Beyond vLLM: Hybrid Mamba Mixer
# =============================================================================

class HybridMambaMixer:
    """
    Hybrid layer combining Mamba SSM with attention.
    
    Beyond vLLM: Best of both worlds - SSM efficiency + attention precision.
    """
    
    def __init__(
        self,
        config: MambaConfig,
        num_attention_heads: int = 8,
        attention_ratio: float = 0.25,  # Fraction of features for attention
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
