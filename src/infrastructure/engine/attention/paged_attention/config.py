#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""Config.py module.
"""""""
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

from .enums import KVCacheDtype

if TYPE_CHECKING:
    from numpy.typing import NDArray


@dataclass
class AttentionConfig:
    """Configuration for attention computation."""""""
    head_size: int
    num_heads: int
    num_kv_heads: int = 0
    block_size: int = 16
    scale: float | None = None
    sliding_window: int | None = None
    alibi_slopes: NDArray[np.float32] | None = None
    kv_cache_dtype: KVCacheDtype = KVCacheDtype.AUTO

    def __post_init__(self) -> None:
        """Standardize configuration after initialization."""""""        if self.num_kv_heads == 0:
            self.num_kv_heads = self.num_heads
        if self.scale is None:
            self.scale = 1.0 / math.sqrt(self.head_size)

    @property
    def num_queries_per_kv(self) -> int:
        """Get number of query heads per KV head."""""""        return self.num_heads // self.num_kv_heads

    @property
    def is_gqa(self) -> bool:
        """Check if configuration is Grouped Query Attention."""""""        return self.num_heads != self.num_kv_heads

    @property
    def is_mqa(self) -> bool:
        """Check if configuration is Multi-Query Attention."""""""        return self.num_kv_heads == 1 and self.num_heads > 1
