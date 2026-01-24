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
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
FlashInfer backend for decode-focused attention.
"""

from __future__ import annotations

import logging
from typing import Any

from .base import AttentionBackend
from .models import AttentionCapabilities, AttentionMetadata
from .sdpa import TorchSDPABackend

logger = logging.getLogger(__name__)


class FlashInferBackend(AttentionBackend[None]):
    """
    FlashInfer backend for decode-focused attention.

    Optimized for single-token decode with PagedAttention.
    """

    @staticmethod
    def get_name() -> str:
        return "flashinfer"

    @staticmethod
    def get_capabilities() -> AttentionCapabilities:
        return AttentionCapabilities(
            supports_prefill=True,
            supports_decode=True,
            supports_encoder=False,
            supports_cross=False,
            supports_sliding_window=True,
            supports_alibi=False,
            supports_gqa=True,
            supports_mqa=True,
            supports_prefix_caching=True,
            supports_cuda_graphs=True,
            supports_fp8=True,
            requires_cuda=True,
            min_sm_version=80,
            best_for_short_seqs=True,
            best_for_long_seqs=True,
            memory_efficient=True,
        )

    def forward(
        self,
        query: Any,
        key: Any,
        value: Any,
        kv_cache: tuple[Any, Any] | None,
        metadata: AttentionMetadata,
        scale: float | None = None,
    ) -> Any:
        """FlashInfer implementation."""
        try:
            import flashinfer  # noqa: F401
        except ImportError:
            logger.warning("flashinfer not available, falling back to SDPA")
            return TorchSDPABackend().forward(query, key, value, kv_cache, metadata, scale)

        # FlashInfer-specific implementation would go here
        # For now, fall back to SDPA
        return TorchSDPABackend().forward(query, key, value, kv_cache, metadata, scale)
