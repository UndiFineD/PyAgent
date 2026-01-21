# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for Multimodal Cache.
Delegates to modularized sub-packages in src/infrastructure/multimodal/cache/.
"""

from __future__ import annotations

from .cache import (
    MediaType,
    CacheBackend,
    HashAlgorithm,
    MediaHash,
    CacheEntry,
    CacheStats,
    PlaceholderRange,
    MultiModalHasher,
    MultiModalCache,
    MemoryMultiModalCache,
    PerceptualCache,
    PrefetchMultiModalCache,
    IPCMultiModalCache,
    compute_media_hash,
    create_cache,
)

__all__ = [
    "MediaType",
    "CacheBackend",
    "HashAlgorithm",
    "MediaHash",
    "CacheEntry",
    "CacheStats",
    "PlaceholderRange",
    "MultiModalHasher",
    "MultiModalCache",
    "MemoryMultiModalCache",
    "PerceptualCache",
    "PrefetchMultiModalCache",
    "IPCMultiModalCache",
    "compute_media_hash",
    "create_cache",
]
