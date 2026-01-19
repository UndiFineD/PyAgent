# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
AttentionBackendRegistry - Dynamic attention backend selection (Facade).

This file is now a facade for the modularized backend package.
"""

from .backend import (
    AttentionBackend,
    AttentionBackendEnum,
    AttentionBackendRegistry,
    AttentionCapabilities,
    AttentionMetadata,
    AttentionType,
    FlashAttentionBackend,
    FlashInferBackend,
    NaiveAttentionBackend,
    PackKVAttentionBackend,
    TorchSDPABackend,
    get_attention_registry,
)

__all__ = [
    "AttentionBackend",
    "AttentionBackendEnum",
    "AttentionBackendRegistry",
    "AttentionCapabilities",
    "AttentionMetadata",
    "AttentionType",
    "FlashAttentionBackend",
    "FlashInferBackend",
    "NaiveAttentionBackend",
    "PackKVAttentionBackend",
    "TorchSDPABackend",
    "get_attention_registry",
]
