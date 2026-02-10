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
# limitations under the License.

"""
Batch matrix multiplication operations using available backends.
"""

from typing import Any

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
import numpy as np


def mm_batch_invariant(
    a: Any,
    b: Any,
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
    if out is not None:
        return torch.mm(a, b, out=out)
    return torch.mm(a, b)


def bmm_batch_invariant(
    a: Any,
    b: Any,
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
