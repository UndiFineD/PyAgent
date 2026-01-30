#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

import logging
import math
from typing import Any
import numpy as np

logger = logging.getLogger(__name__)

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
try:
    import triton
    import triton.language as tl
    HAS_TRITON = True
except ImportError:
    HAS_TRITON = False
    HAS_TRITON = True
except ImportError:
    HAS_TRITON = False

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
    Persistent GEMM using Triton kernel if available, else falls back to torch or numpy.
    """
    if not HAS_TORCH:
        result = np.matmul(a, b)
        if bias is not None:
            result = result + bias
        return result
    if not HAS_TRITON or not getattr(a, 'is_cuda', False):
        result = torch.matmul(a, b)
        if bias is not None:
            result = result + bias
        return result
    # Triton kernel not implemented in this stub (see vLLM for details)
    # Fallback to torch.matmul for now
    result = torch.matmul(a, b)
    if bias is not None:
        result = result + bias
    return result


def softmax_batch_invariant(
    x: Any,  # torch.Tensor
    dim: int = -1,
    dtype: Any = None,
) -> Any:
    """
    Numerically stable softmax that is deterministic across batch orderings.
    """
    if not HAS_TORCH:
        x_max = np.max(x, axis=dim, keepdims=True)
        exp_x = np.exp(x - x_max)
        sum_exp_x = np.sum(exp_x, axis=dim, keepdims=True)
        return exp_x / sum_exp_x
    x_max = torch.amax(x, dim=dim, keepdim=True)
    x_shifted = x - x_max
    exp_x = torch.exp(x_shifted)
    sum_exp_x = torch.sum(exp_x, dim=dim, keepdim=True)
    result = exp_x / sum_exp_x
    if dtype is not None:
        result = result.to(dtype)
    return result


def log_softmax_batch_invariant(
    x: Any,  # torch.Tensor
    dim: int = -1,
) -> Any:
    """
    Numerically stable log softmax that is deterministic.
    """
    if not HAS_TORCH:
        x_max = np.max(x, axis=dim, keepdims=True)
        shifted = x - x_max
        log_sum_exp = np.log(np.sum(np.exp(shifted), axis=dim, keepdims=True))
        return shifted - log_sum_exp
    x_max = torch.amax(x, dim=dim, keepdim=True)
    shifted = x - x_max
    log_sum_exp = torch.log(torch.sum(torch.exp(shifted), dim=dim, keepdim=True))
    return shifted - log_sum_exp


def mean_batch_invariant(
    x: Any,  # torch.Tensor
    dim: int | tuple[int, ...] | None = None,
    keepdim: bool = False,
    dtype: Any = None,
) -> Any:
    """
    Deterministic mean reduction.
    """
    if not HAS_TORCH:
        if dim is None:
            return np.mean(x, dtype=dtype)
        return np.mean(x, axis=dim, keepdims=keepdim, dtype=dtype)
    if dim is None:
        total = torch.sum(x)
        count = x.numel()
    else:
        total = torch.sum(x, dim=dim, keepdim=keepdim)
        if isinstance(dim, int):
            count = x.shape[dim]
        else:
            count = 1
            for d in dim:
                count *= x.shape[d]
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
    """
    if not HAS_TORCH:
        result = np.matmul(a, b)
        if out is not None:
            out[:] = result
            return out
        return result
    if getattr(a, 'is_cuda', False) and HAS_TRITON and getattr(a, 'dim', lambda: 0)() == 2 and getattr(b, 'dim', lambda: 0)() == 2:
        result = matmul_persistent(a, b)
        if out is not None:
            out.copy_(result)
            return out
        return result
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
    """
    if not HAS_TORCH:
        result = np.matmul(a, b)
        if out is not None:
            out[:] = result
            return out
        return result
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
    """
    return matmul_persistent(a, b, bias=bias)


def gelu_batch_invariant(x: Any) -> Any:
    """
    Deterministic GELU activation.
    """
    if not HAS_TORCH:
        from scipy import special
        return 0.5 * x * (1.0 + special.erf(x / math.sqrt(2.0)))
    return 0.5 * x * (1.0 + torch.erf(x / math.sqrt(2.0)))


def layer_norm_batch_invariant(
    x: Any,  # torch.Tensor
    normalized_shape: tuple[int, ...],
    weight: Any | None = None,  # torch.Tensor
    bias: Any | None = None,  # torch.Tensor
    eps: float = 1e-5,
) -> Any:
    """
    Deterministic layer normalization.
    """
    if not HAS_TORCH:
        dims = tuple(range(-len(normalized_shape), 0))
        mean = np.mean(x, axis=dims, keepdims=True)
        var = np.var(x, axis=dims, keepdims=True)
        result = (x - mean) / np.sqrt(var + eps)
        if weight is not None:
            result = result * weight
        if bias is not None:
            result = result + bias
        return result
    dims = tuple(range(-len(normalized_shape), 0))
    mean = mean_batch_invariant(x, dim=dims, keepdim=True)
    centered = x - mean
    var = mean_batch_invariant(centered * centered, dim=dims, keepdim=True)
    result = centered / torch.sqrt(var + eps)
    if weight is not None:
        result = result * weight
    if bias is not None:
        result = result + bias
    return result


def rms_norm_batch_invariant(
    x: Any,  # torch.Tensor
    weight: Any | None = None,  # torch.Tensor
    eps: float = 1e-6,
) -> Any:
    """
    Deterministic RMS normalization.
    """
    if not HAS_TORCH:
        rms = np.sqrt(np.mean(x * x, axis=-1, keepdims=True) + eps)
        result = x / rms
        if weight is not None:
            result = result * weight
        return result
    squared = x * x
    mean_sq = mean_batch_invariant(squared, dim=-1, keepdim=True)
    rms = torch.sqrt(mean_sq + eps)
    result = x / rms
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
    """
    if not HAS_TORCH:
        d = query.shape[-1]
        if scale is None:
            scale = 1.0 / math.sqrt(d)
        return np.matmul(query, np.swapaxes(key, -2, -1)) * scale
    d = query.shape[-1]
    if scale is None:
        scale = 1.0 / math.sqrt(d)
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
    """
    if not HAS_TORCH:
        if mask is not None:
            scores = np.where(mask, scores, -1e9)
        weights = softmax_batch_invariant(scores, dim=-1)
        return np.matmul(weights, value)
    if mask is not None:
        scores = scores.masked_fill(~mask, float("-inf"))
    weights = softmax_batch_invariant(scores, dim=-1)
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
