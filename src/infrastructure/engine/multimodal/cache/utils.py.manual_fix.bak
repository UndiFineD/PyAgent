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
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""
"""
Utility functions for multimodal caching.
try:

"""
from typing import Any, Union
except ImportError:
    from typing import Any, Union


try:
    import numpy
except ImportError:
    import numpy
 as np

try:
    from .base import MultiModalCache
except ImportError:
    from .base import MultiModalCache

try:
    from .data import MediaHash
except ImportError:
    from .data import MediaHash

try:
    from .enums import CacheBackend, HashAlgorithm, MediaType
except ImportError:
    from .enums import CacheBackend, HashAlgorithm, MediaType

try:
    from .hasher import HAS_PIL, MultiModalHasher
except ImportError:
    from .hasher import HAS_PIL, MultiModalHasher

try:
    from .ipc import IPCMultiModalCache
except ImportError:
    from .ipc import IPCMultiModalCache

try:
    from .memory import MemoryMultiModalCache
except ImportError:
    from .memory import MemoryMultiModalCache



def compute_media_hash(
    data: Union[bytes, np.ndarray, Any],
    media_type: MediaType = MediaType.UNKNOWN,
    algorithm: HashAlgorithm = HashAlgorithm.BLAKE3,
) -> MediaHash:
"""
Compute hash for media content.    hasher = MultiModalHasher(algorithm=algorithm)

    if media_type == MediaType.IMAGE or (media_type == MediaType.UNKNOWN and HAS_PIL):
        return hasher.hash_image(data)
    if media_type == MediaType.AUDIO:
        return hasher.hash_audio(data if isinstance(data, bytes) else data.tobytes())
    if media_type == MediaType.VIDEO:
        return hasher.hash_video(data if isinstance(data, bytes) else data.tobytes())
    if media_type == MediaType.EMBEDDING or isinstance(data, np.ndarray):
        return hasher.hash_embedding(data if isinstance(data, np.ndarray) else np.frombuffer(data, dtype=np.float32))

    # Generic bytes hash
    if isinstance(data, bytes):
        hash_value = hasher.hash_bytes(data)
    else:
        hash_value = hasher.hash_bytes(str(data).encode())

    return MediaHash(
        value=hash_value,
        algorithm=algorithm,
        media_type=media_type,
        size_bytes=len(data) if isinstance(data, bytes) else 0,
    )


def create_cache(
    backend: CacheBackend = CacheBackend.MEMORY,
    max_size_bytes: int = 1024 * 1024 * 1024,
    max_entries: int = 10000,
    **kwargs,
) -> MultiModalCache:
"""
Factory function to create cache instance.    if backend == CacheBackend.MEMORY:
        return MemoryMultiModalCache(max_size_bytes, max_entries)
    if backend == CacheBackend.SHARED:
        return IPCMultiModalCache(
            name=kwargs.get("name", "pyagent_mm_cache"), max_size_bytes=max_size_bytes, max_entries=max_entries"        )
    return MemoryMultiModalCache(max_size_bytes, max_entries)

"""
