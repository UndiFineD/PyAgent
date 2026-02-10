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

"""
Mamba Utilities.

vLLM Pattern: vllm/model_executor/layers/mamba/mamba_utils.py
Utility functions for Mamba computation.
"""

# pylint: disable=invalid-name

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# Try to import Rust accelerators
try:
    import rust_core

    HAS_RUST = True
except ImportError:
    HAS_RUST = False


# =============================================================================
# Shape Calculators
# =============================================================================


def compute_ssm_state_shape(
    batch_size: int,
    d_inner: int,
    ssm_state_size: int,
) -> tuple[int, int, int]:
    """
    Compute shape for SSM state tensor.

    vLLM Pattern: MambaStateShapeCalculator
    """
    return (batch_size, d_inner, ssm_state_size)


def compute_conv_state_shape(
    batch_size: int,
    d_inner: int,
    conv_kernel_size: int,
) -> tuple[int, int, int]:
    """
    Compute shape for conv state tensor.

    vLLM Pattern: MambaStateShapeCalculator
    """
    return (batch_size, d_inner, conv_kernel_size)


def compute_state_dtype(
    input_dtype: np.dtype,
    force_fp32: bool = False,
) -> np.dtype:
    """
    Determine appropriate dtype for state tensors.

    vLLM Pattern: MambaStateDtypeCalculator
    """
    if force_fp32:
        return np.float32

    # SSM state typically needs higher precision
    if input_dtype in (np.float16, np.bfloat16):
        return np.float32

    return input_dtype


# =============================================================================
# SSM Operations
# =============================================================================


def discretize_ssm(
    A: np.ndarray,
    B: np.ndarray,
    dt: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Discretize continuous SSM matrices.

    Zero-order hold discretization:
        dA = exp(dt * A)
        dB = (dA - I) * inv(A) * B ≈ dt * B (for small dt)

    Args:
        A: State transition [d_inner, ssm_state_size]
        B: Input projection [batch, seq_len, ssm_state_size] or [batch, ssm_state_size]
        dt: Time step [batch, seq_len, d_inner] or [batch, d_inner]

    Returns:
        dA: Discretized state transition
        dB: Discretized input projection
    """
    if HAS_RUST and hasattr(rust_core, "discretize_ssm_rust"):
        return rust_core.discretize_ssm_rust(A, B, dt)

    # Expand dimensions for broadcasting
    if dt.ndim == 2:
        # Single step: [batch, d_inner]
        # [batch, d_inner, ssm_state_size]
        dA: np.ndarray[tuple[int, ...], np.dtype[math.Any]] = np.exp(dt[:, :, None] * A)
        dB = dt[:, :, None] * B[:, None, :]  # [batch, d_inner, ssm_state_size]
    else:
        # Sequence: [batch, seq_len, d_inner]
        # [batch, seq_len, d_inner, ssm_state_size]
        dA: np.ndarray[tuple[int, ...], np.dtype[math.Any]] = np.exp(dt[:, :, :, None] * A)
        dB = dt[:, :, :, None] * B[:, :, None, :]  # [batch, seq_len, d_inner, ssm_state_size]

    return dA, dB


def apply_ssm_recurrence(
    x: np.ndarray,
    dA: np.ndarray,
    dB: np.ndarray,
    C: np.ndarray,
    D: np.ndarray,
    initial_state: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Apply SSM recurrence.

    h_t = dA * h_{t-1} + dB * x_t
    y_t = C @ h_t + D * x_t

    Args:
        x: Input [batch, seq_len, d_inner]
        dA: Discretized A [batch, seq_len, d_inner, ssm_state_size]
        dB: Discretized B [batch, seq_len, d_inner, ssm_state_size]
        C: Output projection [batch, seq_len, ssm_state_size]
        D: Skip connection [d_inner]
        initial_state: Initial state [batch, d_inner, ssm_state_size]

    Returns:
        output: SSM output [batch, seq_len, d_inner]
        final_state: Final state [batch, d_inner, ssm_state_size]
    """
    batch_size, seq_len, d_inner = x.shape
    ssm_state_size = dA.shape[-1]

    # Initialize state
    if initial_state is None:
        state = np.zeros((batch_size, d_inner, ssm_state_size), dtype=x.dtype)
    else:
        state = initial_state.copy()

    output = np.zeros_like(x)

    # Sequential recurrence (can be parallelized with scan)
    for t in range(seq_len):
        # State update
        state = dA[:, t] * state + dB[:, t] * x[:, t : t + 1, :].transpose(0, 2, 1)
        state = state.squeeze(-1) if state.ndim == 4 else state

        # Handle shape mismatch
        if state.ndim == 3 and state.shape[-1] != ssm_state_size:
            state = state.reshape(batch_size, d_inner, ssm_state_size)

        # Output
        y_t = (state * C[:, t : t + 1, :].transpose(0, 2, 1)).sum(axis=-1) + D * x[:, t]
        output[:, t] = y_t

    return output, state


# =============================================================================
# Activation Functions
# =============================================================================


def silu_activation(x: np.ndarray) -> np.ndarray:
    """
    SiLU (Swish) activation: x * sigmoid(x).

    More numerically stable than naive implementation.
    """
    if HAS_RUST and hasattr(rust_core, "silu_activation_rust"):
        return rust_core.silu_activation_rust(x)

    # Stable implementation avoiding overflow
    positive = x * (1 / (1 + np.exp(-np.clip(x, -20, 20))))
    return positive


def swish_activation(x: np.ndarray, beta: float = 1.0) -> np.ndarray:
    """
    Swish activation with configurable beta: x * sigmoid(beta * x).
    """
    return x * (1 / (1 + np.exp(-beta * np.clip(x, -20, 20))))


def softplus(x: np.ndarray, beta: float = 1.0, threshold: float = 20.0) -> np.ndarray:
    """
    Softplus activation: (1/beta) * log(1 + exp(beta * x)).

    Reverts to linear for large values.
    """
    scaled = beta * x
    return np.where(scaled > threshold, x, (1.0 / beta) * np.log1p(np.exp(scaled)))


# =============================================================================
# State Management
# =============================================================================


@dataclass
class MambaBlockState:
    """State for a block of Mamba layers."""

    layer_states: list[tuple[np.ndarray, np.ndarray]]  # List of (conv_state, ssm_state)

    @classmethod
    def zeros(
        cls,
        num_layers: int,
        batch_size: int,
        d_inner: int,
        conv_kernel_size: int,
        ssm_state_size: int,
        dtype: np.dtype = np.float32,
    ) -> "MambaBlockState":
        """Create zero-initialized block state."""
        layer_states = []
        for _ in range(num_layers):
            conv_state = np.zeros(
                (batch_size, d_inner, conv_kernel_size),
                dtype=dtype,
            )
            ssm_state = np.zeros(
                (batch_size, d_inner, ssm_state_size),
                dtype=dtype,
            )
            layer_states.append((conv_state, ssm_state))

        return cls(layer_states=layer_states)

    def get_layer(self, layer_idx: int) -> tuple[np.ndarray, np.ndarray]:
        """Get state for a specific layer."""
        return self.layer_states[layer_idx]

    def set_layer(
        self,
        layer_idx: int,
        conv_state: np.ndarray,
        ssm_state: np.ndarray,
    ) -> None:
        """Set state for a specific layer."""
        self.layer_states[layer_idx] = (conv_state, ssm_state)

    def clone(self) -> "MambaBlockState":
        """Deep clone the state."""
        return MambaBlockState(layer_states=[(conv.copy(), ssm.copy()) for conv, ssm in self.layer_states])


# =============================================================================
# Chunked Processing
# =============================================================================


def chunk_sequence(
    x: np.ndarray,
    chunk_size: int,
) -> list[np.ndarray]:
    """
    Split sequence into chunks for memory-efficient processing.

    Args:
        x: Input [batch, seq_len, hidden]
        chunk_size: Maximum chunk length

    Returns:
        List of chunks
    """
    seq_len = x.shape[1]
    chunks = []

    for start in range(0, seq_len, chunk_size):
        end: int = min(start + chunk_size, seq_len)
        chunks.append(x[:, start:end])

    return chunks


def merge_chunks(chunks: list[np.ndarray]) -> np.ndarray:
    """Merge chunked outputs back to single sequence."""
    return np.concatenate(chunks, axis=1)


# =============================================================================
# Parallel Scan (Associative Scan)
# =============================================================================


def parallel_scan(
    gates: np.ndarray,
    values: np.ndarray,
) -> np.ndarray:
    """
    Parallel (associative) scan for SSM computation.

    Computes: output[t] = gates[t] * output[t-1] + values[t]

    Uses work-efficient parallel prefix scan algorithm.
    This is O(n) work with O(log n) depth.

    Args:
        gates: Gate values [batch, seq_len, dim]
        values: Input values [batch, seq_len, dim]

    Returns:
        Scan output [batch, seq_len, dim]
    """
    _, seq_len, _ = gates.shape

    if seq_len <= 1:
        return values.copy()

    # Use Rust implementation if available
    if HAS_RUST and hasattr(rust_core, "parallel_scan_rust"):
        return rust_core.parallel_scan_rust(gates, values)

    # Python implementation (sequential for correctness)
    output = np.zeros_like(values)
    output[:, 0] = values[:, 0]

    for t in range(1, seq_len):
        output[:, t] = gates[:, t] * output[:, t - 1] + values[:, t]

    return output


# =============================================================================
# Initialization Helpers
# =============================================================================


def init_A_log(
    d_inner: int,
    ssm_state_size: int,
    _dt_min: float = 0.001,
    _dt_max: float = 0.1,
) -> np.ndarray:
    """
    Initialize A_log parameter for Mamba.

    A = -exp(A_log) gives negative real eigenvalues for stability.
    """
    # Initialize as log of linearly spaced values
    A: np.ndarray[tuple[int], np.dtype[np.floating[np._32Bit]]] = np.arange(1, ssm_state_size + 1, dtype=np.float32)
    A: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] = np.tile(A, (d_inner, 1))
    A_log: np.ndarray[tuple[int, ...], np.dtype[math.Any]] = np.log(A)

    return A_log


def init_dt_proj(
    d_inner: int,
    dt_rank: int,
    dt_min: float = 0.001,
    dt_max: float = 0.1,
    dt_init: str = "random",
) -> tuple[np.ndarray, np.ndarray]:
    """
    Initialize dt projection layer.

    Returns (weight, bias) tuple.
    """
    # Weight initialization
    weight: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] = (
        np.random.randn(d_inner, dt_rank).astype(np.float32)
    )
    weight = weight * (1.0 / math.sqrt(dt_rank))

    # Bias initialization
    if dt_init == "random":
        bias: np.ndarray[tuple[int, ...], np.dtype[np.floating[np._32Bit]]] = np.random.uniform(
            math.log(dt_min),
            math.log(dt_max),
            size=d_inner,
        ).astype(np.float32)
    else:
        bias: np.ndarray[tuple[int], np.dtype[np.floating[np._32Bit]]] = (
            np.full(d_inner, math.log(0.01), dtype=np.float32)
        )

    return weight, bias
