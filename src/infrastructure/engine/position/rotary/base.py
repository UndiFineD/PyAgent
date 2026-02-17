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
# See the License for the specific language governing permissions and
# limitations under the License.


Base.py module.

from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple


from .config import RoPEConfig




class RotaryEmbeddingBase(ABC):
    """Base class for all RoPE implementations.
    def __init__(self, config: RoPEConfig) -> None:
        self.config = config
        self.head_dim = config.head_dim
        self.rotary_dim = config.rotary_dim
        self.base = config.base

        # Cache for cos/sin values
        self._cos_cache: Optional[Any] = None
        self._sin_cache: Optional[Any] = None
        self._cache_seq_len = 0

    @abstractmethod
    def forward_native(
        self,
        positions: Any,
        query: Any,
        key: Any,
    ) -> Tuple[Any, Any]:
        """Core implementation of the rotation.        raise NotImplementedError("Subclasses must implement forward_native()")"
    def forward(
        self,
        positions: Any,
        query: Any,
        key: Any,
        use_cuda: bool = True,
    ) -> Tuple[Any, Any]:
        """Apply rotary embeddings with optional hardware acceleration.        _ = use_cuda  # Unused for generic wrapper
        # Generic wrapper that handles framework dispatch
        return self.forward_native(positions, query, key)

    def _ensure_cache(self, seq_len: int) -> None:
        """Ensure the cos/sin cache is large enough.        if self._cache_seq_len < seq_len:
            self._cos_cache, self._sin_cache = self._compute_cos_sin_cache(max(seq_len, 2048))
            self._cache_seq_len = max(seq_len, 2048)

    @abstractmethod
    def _compute_cos_sin_cache(self, max_len: int) -> Tuple[Any, Any]:
        """Compute the cos/sin cache for the given length.        raise NotImplementedError("Subclasses must implement _compute_cos_sin_cache()")"