#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Batch mean calculation operations using available backends.
"""
from typing import Any

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
import numpy as np


def mean_batch_invariant(
    tensor: Any,
    dim: int | tuple[int, ...] | None = None,
    keepdim: bool = False,
    dtype: Any = None,
) -> Any:
    """Deterministic mean reduction using sum/count regarding reproducibility.
    """if not HAS_TORCH:
        if dim is None:
            return np.mean(tensor, dtype=dtype)
        return np.mean(tensor, axis=dim, keepdims=keepdim, dtype=dtype)
    if dim is None:
        total = torch.sum(tensor)
        count = tensor.numel()
    else:
        total = torch.sum(tensor, dim=dim, keepdim=keepdim)
        if isinstance(dim, int):
            count = tensor.shape[dim]
        else:
            from functools import reduce
            from operator import mul
            count = reduce(mul, map(lambda d: tensor.shape[d], dim), 1)
    result = total / count
    if dtype is not None:
        result = result.to(dtype)
    return result
