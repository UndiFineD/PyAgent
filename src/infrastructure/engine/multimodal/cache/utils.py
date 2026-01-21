# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Utility functions for multimodal caching."""

from typing import Any, Optional, Union
import numpy as np
from .enums import MediaType, HashAlgorithm, CacheBackend
from .data import MediaHash
from .hasher import MultiModalHasher, HAS_PIL
from .base import MultiModalCache
from .memory import MemoryMultiModalCache
from .ipc import IPCMultiModalCache


def compute_media_hash(
    data: Union[bytes, np.ndarray, Any],
    media_type: MediaType = MediaType.UNKNOWN,
    algorithm: HashAlgorithm = HashAlgorithm.BLAKE3,
) -> MediaHash:
    """Compute hash for media content."""
    hasher = MultiModalHasher(algorithm=algorithm)
    
    if media_type == MediaType.IMAGE or (media_type == MediaType.UNKNOWN and HAS_PIL):
        return hasher.hash_image(data)
    elif media_type == MediaType.AUDIO:
        return hasher.hash_audio(data if isinstance(data, bytes) else data.tobytes())
    elif media_type == MediaType.VIDEO:
        return hasher.hash_video(data if isinstance(data, bytes) else data.tobytes())
    elif media_type == MediaType.EMBEDDING or isinstance(data, np.ndarray):
        return hasher.hash_embedding(data if isinstance(data, np.ndarray) else np.frombuffer(data, dtype=np.float32))
    else:
        # Generic bytes hash
        if isinstance(data, bytes):
            hash_value = hasher.hash_bytes(data)
        else:
            hash_value = hasher.hash_bytes(str(data).encode())
        
        return MediaHash(
            value=hash_value,
            algorithm=algorithm,
            media_type=media_type,
            size_bytes=len(data) if isinstance(data, bytes) else 0
        )


def create_cache(
    backend: CacheBackend = CacheBackend.MEMORY,
    max_size_bytes: int = 1024 * 1024 * 1024,
    max_entries: int = 10000,
    **kwargs
) -> MultiModalCache:
    """Factory function to create cache instance."""
    if backend == CacheBackend.MEMORY:
        return MemoryMultiModalCache(max_size_bytes, max_entries)
    elif backend == CacheBackend.SHARED:
        return IPCMultiModalCache(
            name=kwargs.get("name", "pyagent_mm_cache"),
            max_size_bytes=max_size_bytes,
            max_entries=max_entries
        )
    else:
        return MemoryMultiModalCache(max_size_bytes, max_entries)
