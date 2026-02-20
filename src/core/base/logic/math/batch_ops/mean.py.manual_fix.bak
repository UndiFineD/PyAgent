#!/usr/bin/env python3
"""
Parser-safe stub: batch mean operations.

Minimal, deterministic implementation preserving public API for imports.
"""
from __future__ import annotations

from typing import Any, Optional, Tuple

try:
    import numpy as np
except Exception:
    np = None


def mean_batch_invariant(
    tensor: Any,
    dim: Optional[Tuple[int, ...]] | int | None = None,
    keepdim: bool = False,
    dtype: Any = None,
) -> Any:
    if np is None:
        raise ImportError("numpy is required for mean_batch_invariant stub")
    if dim is None:
        return np.mean(tensor, dtype=dtype)
    return np.mean(tensor, axis=dim, keepdims=keepdim, dtype=dtype)


__all__ = ["mean_batch_invariant"]
