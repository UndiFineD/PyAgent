# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Enums for multimodal caching."""

from enum import Enum, auto


class MediaType(Enum):
    """Types of media content."""
    IMAGE = auto()
    VIDEO = auto()
    AUDIO = auto()
    TEXT = auto()
    EMBEDDING = auto()
    UNKNOWN = auto()


class CacheBackend(Enum):
    """Cache storage backend types."""
    MEMORY = auto()       # In-memory dictionary
    MMAP = auto()         # Memory-mapped file
    SHARED = auto()       # Shared memory (IPC)
    DISK = auto()         # Disk-based persistence
    HYBRID = auto()       # Multi-tier caching


class HashAlgorithm(Enum):
    """Hash algorithms for content addressing."""
    BLAKE3 = auto()       # Fast cryptographic hash
    SHA256 = auto()       # Standard SHA-256
    XXHASH = auto()       # Fast non-cryptographic
    PERCEPTUAL = auto()   # Perceptual hash for images
