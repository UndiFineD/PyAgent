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


"""
"""
Softmax activation operations regarding batch processing.
"""

"""
from typing import Any

try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False
import numpy as np


def softmax_batch_invariant(
    tensor: Any,
    dim: int = -1,
    dtype: Any = None,
) -> Any:
"""
Numerically stable softmax that is deterministic across batch orderings.
"""
if not HAS_TORCH:
        arr = np.asarray(tensor)
        input_max = np.max(arr, axis=dim, keepdims=True)
        exp_x = np.exp(arr - input_max)
        sum_exp_x = np.sum(exp_x, axis=dim, keepdims=True)
        result = exp_x / sum_exp_x
        if dtype is not None:
            result = result.astype(dtype)
        return result

    input_max = torch.amax(tensor, dim=dim, keepdim=True)
    input_shifted = tensor - input_max
    exp_x = torch.exp(input_shifted)
    sum_exp_x = torch.sum(exp_x, dim=dim, keepdim=True)
    result = exp_x / sum_exp_x
    if dtype is not None:
        result = result.to(dtype)
    return result
