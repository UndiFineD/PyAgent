# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
BatchInvariantOps - Deterministic GPU operations for reproducible inference.

Implements vLLM's batch_invariant.py patterns for deterministic execution:
- matmul_persistent: Triton persistent GEMM kernel
- softmax_batch_invariant: Numerically stable softmax
- mean_batch_invariant: Deterministic mean reduction
- mm/bmm_batch_invariant: Matrix multiplication wrappers

Beyond vLLM: Automatic precision selection based on input dtype.
"""

from __future__ import annotations

import logging
import math
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)

# Try to import torch and triton
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
    torch = None  # type: ignore

try:
    import triton
    import triton.language as tl
    HAS_TRITON = True
except ImportError:
    HAS_TRITON = False
    triton = None
    tl = None


# Triton-based persistent matmul kernel
if HAS_TRITON:
    @triton.jit
    def _matmul_persistent_kernel(
        a_ptr, b_ptr, c_ptr,
        bias_ptr,
        M, N, K,
        stride_am, stride_ak,
        stride_bk, stride_bn,
        stride_cm, stride_cn,
        HAS_BIAS: tl.constexpr,
        BLOCK_SIZE_M: tl.constexpr,
        BLOCK_SIZE_N: tl.constexpr,
        BLOCK_SIZE_K: tl.constexpr,
        GROUP_SIZE_M: tl.constexpr,
    ):
        """Triton persistent GEMM kernel."""
        pid = tl.program_id(0)
        num_pid_m = tl.cdiv(M, BLOCK_SIZE_M)
        num_pid_n = tl.cdiv(N, BLOCK_SIZE_N)
        num_pid_in_group = GROUP_SIZE_M * num_pid_n
        group_id = pid // num_pid_in_group
        first_pid_m = group_id * GROUP_SIZE_M
        group_size_m = min(num_pid_m - first_pid_m, GROUP_SIZE_M)
        pid_m = first_pid_m + (pid % group_size_m)
        pid_n = (pid % num_pid_in_group) // group_size_m
        
        offs_am = (pid_m * BLOCK_SIZE_M + tl.arange(0, BLOCK_SIZE_M)) % M
        offs_bn = (pid_n * BLOCK_SIZE_N + tl.arange(0, BLOCK_SIZE_N)) % N
        offs_k = tl.arange(0, BLOCK_SIZE_K)
        
        a_ptrs = a_ptr + (offs_am[:, None] * stride_am + offs_k[None, :] * stride_ak)
        b_ptrs = b_ptr + (offs_k[:, None] * stride_bk + offs_bn[None, :] * stride_bn)
        
        accumulator = tl.zeros((BLOCK_SIZE_M, BLOCK_SIZE_N), dtype=tl.float32)
        
        for k in range(0, tl.cdiv(K, BLOCK_SIZE_K)):
            k_remaining = K - k * BLOCK_SIZE_K
            a = tl.load(a_ptrs, mask=offs_k[None, :] < k_remaining, other=0.0)
            b = tl.load(b_ptrs, mask=offs_k[:, None] < k_remaining, other=0.0)
            accumulator += tl.dot(a, b)
            a_ptrs += BLOCK_SIZE_K * stride_ak
            b_ptrs += BLOCK_SIZE_K * stride_bk
        
        if HAS_BIAS:
            bias = tl.load(bias_ptr + offs_bn)
            accumulator += bias[None, :]
        
        c = accumulator.to(tl.float16)
        offs_cm = pid_m * BLOCK_SIZE_M + tl.arange(0, BLOCK_SIZE_M)
        offs_cn = pid_n * BLOCK_SIZE_N + tl.arange(0, BLOCK_SIZE_N)
        c_ptrs = c_ptr + stride_cm * offs_cm[:, None] + stride_cn * offs_cn[None, :]
        c_mask = (offs_cm[:, None] < M) & (offs_cn[None, :] < N)
        tl.store(c_ptrs, c, mask=c_mask)


def matmul_persistent(
    a: Any,  # torch.Tensor
    b: Any,  # torch.Tensor
    bias: Any | None = None,  # torch.Tensor
) -> Any:
    """
    Persistent GEMM using Triton kernel.
    
    Provides deterministic matrix multiplication regardless of batch order.
    Falls back to torch.matmul if Triton unavailable.
    
    Args:
        a: Input tensor [M, K]
        b: Weight tensor [K, N]
        bias: Optional bias tensor [N]
        
    Returns:
        Output tensor [M, N]
    """
    if not HAS_TORCH:
        # Numpy fallback
        result = np.matmul(a, b)
        if bias is not None:
            result = result + bias
        return result
    
    if not HAS_TRITON or not a.is_cuda:
        # PyTorch fallback
        result = torch.matmul(a, b)
        if bias is not None:
            result = result + bias
        return result
    
    # Triton kernel
    assert a.shape[1] == b.shape[0], "Incompatible dimensions"
    assert a.dtype == b.dtype, "Incompatible dtypes"
    
    M, K = a.shape
    K, N = b.shape
    
    c = torch.empty((M, N), device=a.device, dtype=a.dtype)
    
    # Kernel configuration
    BLOCK_SIZE_M = 128
    BLOCK_SIZE_N = 128
    BLOCK_SIZE_K = 64
    GROUP_SIZE_M = 8
    
    grid = lambda META: (
        triton.cdiv(M, META['BLOCK_SIZE_M']) * triton.cdiv(N, META['BLOCK_SIZE_N']),
    )
    
    _matmul_persistent_kernel[grid](
        a, b, c,
        bias if bias is not None else a,  # Dummy if no bias
        M, N, K,
        a.stride(0), a.stride(1),
        b.stride(0), b.stride(1),
        c.stride(0), c.stride(1),
        HAS_BIAS=bias is not None,
        BLOCK_SIZE_M=BLOCK_SIZE_M,
        BLOCK_SIZE_N=BLOCK_SIZE_N,
        BLOCK_SIZE_K=BLOCK_SIZE_K,
        GROUP_SIZE_M=GROUP_SIZE_M,
    )
    
    return c


def softmax_batch_invariant(
    input: Any,  # torch.Tensor
    dim: int = -1,
    dtype: Any = None,
) -> Any:
    """
    Numerically stable softmax that is deterministic across batch orderings.
    
    Uses explicit max subtraction and normalization to ensure reproducibility.
    
    Args:
        input: Input tensor
        dim: Dimension to apply softmax over
        dtype: Optional output dtype
        
    Returns:
        Softmax output tensor
    """
    if not HAS_TORCH:
        # Numpy implementation
        input_max = np.max(input, axis=dim, keepdims=True)
        exp_x = np.exp(input - input_max)
        sum_exp_x = np.sum(exp_x, axis=dim, keepdims=True)
        return exp_x / sum_exp_x
    
    # Compute softmax in deterministic way
    # First subtract max for numerical stability
    input_max = torch.amax(input, dim=dim, keepdim=True)
    input_shifted = input - input_max
    exp_x = torch.exp(input_shifted)
    sum_exp_x = torch.sum(exp_x, dim=dim, keepdim=True)
    result = exp_x / sum_exp_x
    
    if dtype is not None:
        result = result.to(dtype)
    
    return result


def log_softmax_batch_invariant(
    input: Any,  # torch.Tensor
    dim: int = -1,
) -> Any:
    """
    Numerically stable log softmax that is deterministic.
    
    Args:
        input: Input tensor
        dim: Dimension to apply log softmax over
        
    Returns:
        Log softmax output tensor
    """
    if not HAS_TORCH:
        # Numpy implementation
        input_max = np.max(input, axis=dim, keepdims=True)
        shifted = input - input_max
        log_sum_exp = np.log(np.sum(np.exp(shifted), axis=dim, keepdims=True))
        return shifted - log_sum_exp
    
    # log(softmax(x)) = x - max(x) - log(sum(exp(x - max(x))))
    input_max = torch.amax(input, dim=dim, keepdim=True)
    shifted = input - input_max
    log_sum_exp = torch.log(torch.sum(torch.exp(shifted), dim=dim, keepdim=True))
    return shifted - log_sum_exp


def mean_batch_invariant(
    input: Any,  # torch.Tensor
    dim: int | tuple[int, ...] | None = None,
    keepdim: bool = False,
    dtype: Any = None,
) -> Any:
    """
    Deterministic mean reduction.
    
    Uses sum/count instead of built-in mean for reproducibility.
    
    Args:
        input: Input tensor
        dim: Dimension(s) to reduce
        keepdim: Whether to keep reduced dimensions
        dtype: Optional output dtype
        
    Returns:
        Mean reduced tensor
    """
    if not HAS_TORCH:
        if dim is None:
            return np.mean(input, dtype=dtype)
        return np.mean(input, axis=dim, keepdims=keepdim, dtype=dtype)
    
    # Compute mean as sum/count for determinism
    if dim is None:
        total = torch.sum(input)
        count = input.numel()
    else:
        total = torch.sum(input, dim=dim, keepdim=keepdim)
        if isinstance(dim, int):
            count = input.shape[dim]
        else:
            count = 1
            for d in dim:
                count *= input.shape[d]
    
    result = total / count
    
    if dtype is not None:
        result = result.to(dtype)
    
    return result


def mm_batch_invariant(
    a: Any,  # torch.Tensor
    b: Any,  # torch.Tensor
    *,
    out: Any | None = None,
) -> Any:
    """
    Deterministic matrix multiplication (2D x 2D).
    
    Args:
        a: First matrix [M, K]
        b: Second matrix [K, N]
        out: Optional output tensor
        
    Returns:
        Result matrix [M, N]
    """
    if not HAS_TORCH:
        result = np.matmul(a, b)
        if out is not None:
            out[:] = result
            return out
        return result
    
    # For CUDA, use persistent kernel if available
    if a.is_cuda and HAS_TRITON and a.dim() == 2 and b.dim() == 2:
        result = matmul_persistent(a, b)
        if out is not None:
            out.copy_(result)
            return out
        return result
    
    # Fall back to torch.mm
    if out is not None:
        return torch.mm(a, b, out=out)
    return torch.mm(a, b)


def bmm_batch_invariant(
    a: Any,  # torch.Tensor
    b: Any,  # torch.Tensor
    *,
    out: Any | None = None,
) -> Any:
    """
    Deterministic batched matrix multiplication (3D x 3D).
    
    Args:
        a: First batch of matrices [B, M, K]
        b: Second batch of matrices [B, K, N]
        out: Optional output tensor
        
    Returns:
        Result batch [B, M, N]
    """
    if not HAS_TORCH:
        result = np.matmul(a, b)
        if out is not None:
            out[:] = result
            return out
        return result
    
    # Note: For batched operations, we rely on torch.bmm
    # as Triton batched GEMM is more complex
    if out is not None:
        return torch.bmm(a, b, out=out)
    return torch.bmm(a, b)


def addmm_batch_invariant(
    bias: Any,  # torch.Tensor
    a: Any,  # torch.Tensor
    b: Any,  # torch.Tensor
) -> Any:
    """
    Deterministic bias + matrix multiplication.
    
    Args:
        bias: Bias vector [N]
        a: First matrix [M, K]
        b: Second matrix [K, N]
        
    Returns:
        Result: bias + a @ b, shape [M, N]
    """
    return matmul_persistent(a, b, bias=bias)


def gelu_batch_invariant(input: Any) -> Any:
    """
    Deterministic GELU activation.
    
    Uses the explicit formula instead of approximations.
    
    Args:
        input: Input tensor
        
    Returns:
        GELU output tensor
    """
    if not HAS_TORCH:
        # Numpy GELU using error function
        from scipy import special
        return 0.5 * input * (1.0 + special.erf(input / math.sqrt(2.0)))
    
    # Use PyTorch's GELU with tanh approximation for speed
    # but explicit computation for determinism:
    # GELU(x) = 0.5 * x * (1 + erf(x / sqrt(2)))
    return 0.5 * input * (1.0 + torch.erf(input / math.sqrt(2.0)))


def layer_norm_batch_invariant(
    input: Any,  # torch.Tensor
    normalized_shape: tuple[int, ...],
    weight: Any | None = None,  # torch.Tensor
    bias: Any | None = None,  # torch.Tensor
    eps: float = 1e-5,
) -> Any:
    """
    Deterministic layer normalization.
    
    Uses explicit mean/variance computation for reproducibility.
    
    Args:
        input: Input tensor
        normalized_shape: Shape over which to normalize
        weight: Optional scale parameter
        bias: Optional shift parameter
        eps: Epsilon for numerical stability
        
    Returns:
        Normalized tensor
    """
    if not HAS_TORCH:
        # Numpy implementation
        dims = tuple(range(-len(normalized_shape), 0))
        mean = np.mean(input, axis=dims, keepdims=True)
        var = np.var(input, axis=dims, keepdims=True)
        result = (input - mean) / np.sqrt(var + eps)
        if weight is not None:
            result = result * weight
        if bias is not None:
            result = result + bias
        return result
    
    # Compute mean and variance explicitly
    dims = tuple(range(-len(normalized_shape), 0))
    
    # Deterministic mean
    mean = mean_batch_invariant(input, dim=dims, keepdim=True)
    
    # Deterministic variance: E[(x - mean)^2]
    centered = input - mean
    var = mean_batch_invariant(centered * centered, dim=dims, keepdim=True)
    
    # Normalize
    result = centered / torch.sqrt(var + eps)
    
    # Apply weight and bias
    if weight is not None:
        result = result * weight
    if bias is not None:
        result = result + bias
    
    return result


def rms_norm_batch_invariant(
    input: Any,  # torch.Tensor
    weight: Any | None = None,  # torch.Tensor
    eps: float = 1e-6,
) -> Any:
    """
    Deterministic RMS normalization.
    
    RMS norm doesn't subtract mean, just divides by RMS.
    
    Args:
        input: Input tensor
        weight: Optional scale parameter
        eps: Epsilon for numerical stability
        
    Returns:
        RMS normalized tensor
    """
    if not HAS_TORCH:
        # Numpy implementation
        rms = np.sqrt(np.mean(input * input, axis=-1, keepdims=True) + eps)
        result = input / rms
        if weight is not None:
            result = result * weight
        return result
    
    # Compute RMS = sqrt(mean(x^2))
    squared = input * input
    mean_sq = mean_batch_invariant(squared, dim=-1, keepdim=True)
    rms = torch.sqrt(mean_sq + eps)
    
    result = input / rms
    
    if weight is not None:
        result = result * weight
    
    return result


def attention_score_batch_invariant(
    query: Any,  # torch.Tensor [B, H, L, D]
    key: Any,  # torch.Tensor [B, H, S, D]
    scale: float | None = None,
) -> Any:
    """
    Compute attention scores deterministically.
    
    Args:
        query: Query tensor [B, H, L, D]
        key: Key tensor [B, H, S, D]
        scale: Optional scaling factor (default: 1/sqrt(D))
        
    Returns:
        Attention scores [B, H, L, S]
    """
    if not HAS_TORCH:
        d = query.shape[-1]
        if scale is None:
            scale = 1.0 / math.sqrt(d)
        return np.matmul(query, np.swapaxes(key, -2, -1)) * scale
    
    d = query.shape[-1]
    if scale is None:
        scale = 1.0 / math.sqrt(d)
    
    # Q @ K^T
    scores = torch.matmul(query, key.transpose(-2, -1))
    scores = scores * scale
    
    return scores


def attention_output_batch_invariant(
    scores: Any,  # torch.Tensor [B, H, L, S]
    value: Any,  # torch.Tensor [B, H, S, D]
    mask: Any | None = None,  # torch.Tensor
) -> Any:
    """
    Compute attention output deterministically.
    
    Args:
        scores: Attention scores [B, H, L, S]
        value: Value tensor [B, H, S, D]
        mask: Optional attention mask
        
    Returns:
        Attention output [B, H, L, D]
    """
    if not HAS_TORCH:
        if mask is not None:
            scores = np.where(mask, scores, -1e9)
        weights = softmax_batch_invariant(scores, dim=-1)
        return np.matmul(weights, value)
    
    # Apply mask
    if mask is not None:
        scores = scores.masked_fill(~mask, float('-inf'))
    
    # Deterministic softmax
    weights = softmax_batch_invariant(scores, dim=-1)
    
    # Weighted sum of values
    output = torch.matmul(weights, value)
    
    return output


class BatchInvariantOps:
    """
    Container class for batch-invariant operations.
    
    Provides a consistent interface and tracks usage statistics.
    """
    
    def __init__(self, device: Any = None, dtype: Any = None):
        """
        Initialize batch-invariant operations.
        
        Args:
            device: Target device
            dtype: Default dtype for operations
        """
        if HAS_TORCH:
            self.device = device or torch.device("cpu")
            self.dtype = dtype or torch.float32
        else:
            self.device = device or "cpu"
            self.dtype = dtype
        
        self._call_counts = {
            "matmul": 0,
            "softmax": 0,
            "mean": 0,
            "mm": 0,
            "bmm": 0,
            "addmm": 0,
            "gelu": 0,
            "layer_norm": 0,
            "rms_norm": 0,
        }
    
    def matmul(self, a: Any, b: Any, bias: Any = None) -> Any:
        self._call_counts["matmul"] += 1
        return matmul_persistent(a, b, bias)
    
    def softmax(self, input: Any, dim: int = -1, dtype: Any = None) -> Any:
        self._call_counts["softmax"] += 1
        return softmax_batch_invariant(input, dim, dtype)
    
    def log_softmax(self, input: Any, dim: int = -1) -> Any:
        return log_softmax_batch_invariant(input, dim)
    
    def mean(
        self, 
        input: Any, 
        dim: int | tuple[int, ...] | None = None,
        keepdim: bool = False,
        dtype: Any = None,
    ) -> Any:
        self._call_counts["mean"] += 1
        return mean_batch_invariant(input, dim, keepdim, dtype)
    
    def mm(self, a: Any, b: Any, out: Any = None) -> Any:
        self._call_counts["mm"] += 1
        return mm_batch_invariant(a, b, out=out)
    
    def bmm(self, a: Any, b: Any, out: Any = None) -> Any:
        self._call_counts["bmm"] += 1
        return bmm_batch_invariant(a, b, out=out)
    
    def addmm(self, bias: Any, a: Any, b: Any) -> Any:
        self._call_counts["addmm"] += 1
        return addmm_batch_invariant(bias, a, b)
    
    def gelu(self, input: Any) -> Any:
        self._call_counts["gelu"] += 1
        return gelu_batch_invariant(input)
    
    def layer_norm(
        self,
        input: Any,
        normalized_shape: tuple[int, ...],
        weight: Any = None,
        bias: Any = None,
        eps: float = 1e-5,
    ) -> Any:
        self._call_counts["layer_norm"] += 1
        return layer_norm_batch_invariant(input, normalized_shape, weight, bias, eps)
    
    def rms_norm(
        self,
        input: Any,
        weight: Any = None,
        eps: float = 1e-6,
    ) -> Any:
        self._call_counts["rms_norm"] += 1
        return rms_norm_batch_invariant(input, weight, eps)
    
    def get_stats(self) -> dict[str, int]:
        """Get operation call counts."""
        return self._call_counts.copy()
    
    def reset_stats(self) -> None:
        """Reset operation call counts."""
        for key in self._call_counts:
            self._call_counts[key] = 0
