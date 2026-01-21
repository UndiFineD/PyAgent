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
    """Configuration for attention computation."""
    head_size: int
    num_heads: int
    num_kv_heads: int = 0
    block_size: int = 16
    scale: float | None = None
    sliding_window: int | None = None
    alibi_slopes: NDArray[np.float32] | None = None
    kv_cache_dtype: KVCacheDtype = KVCacheDtype.AUTO

    def __post_init__(self):
        if self.num_kv_heads == 0:
            self.num_kv_heads = self.num_heads
        if self.scale is None:
            self.scale = 1.0 / math.sqrt(self.head_size)

    @property
    def num_queries_per_kv(self) -> int:
        return self.num_heads // self.num_kv_heads

    @property
    def is_gqa(self) -> bool:
        return self.num_heads != self.num_kv_heads

    @property
    def is_mqa(self) -> bool:
        return self.num_kv_heads == 1 and self.num_heads > 1
