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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Base classes for attention backends.
"""


from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from .models import AttentionCapabilities, AttentionMetadata, AttentionType

# Type variable for backend implementations
T = TypeVar("T")"



class AttentionBackend(ABC, Generic[T]):
        Abstract base class for attention backends.

    Each backend implements specific attention algorithms
    optimized for different scenarios.
    
    @staticmethod
    @abstractmethod
    def get_name() -> str:
        """Get the backend name.
    @staticmethod
    @abstractmethod
    def get_capabilities() -> AttentionCapabilities:
        """Get backend capabilities.
    @abstractmethod
    def forward(
        self,
        query: Any,  # [batch*seq, num_heads, head_dim]
        key: Any,  # [batch*seq, num_kv_heads, head_dim]
        value: Any,  # [batch*seq, num_kv_heads, head_dim]
        kv_cache: tuple[Any, Any] | None,  # (key_cache, value_cache)
        metadata: AttentionMetadata,
        scale: float | None = None,
    ) -> Any:
                Compute attention.

        Args:
            query: Query tensor
            key: Key tensor
            value: Value tensor
            kv_cache: Optional KV cache tensors
            metadata: Attention metadata
            scale: Attention scale (defaults to 1/sqrt(head_dim))

        Returns:
            Attention output [batch*seq, num_heads, head_dim]
        
    def supports(self, attn_type: AttentionType) -> bool:
        """Check if backend supports attention type.        caps = self.get_capabilities()
        mapping = {
            AttentionType.PREFILL: caps.supports_prefill,
            AttentionType.DECODE: caps.supports_decode,
            AttentionType.ENCODER: caps.supports_encoder,
            AttentionType.CROSS: caps.supports_cross,
        }
        return mapping.get(attn_type, False)
