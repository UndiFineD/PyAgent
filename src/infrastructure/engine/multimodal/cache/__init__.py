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
"""Multimodal caching sub-package.
try:
    from .base import MultiModalCache  # noqa: F401
except ImportError:
    from .base import MultiModalCache # noqa: F401

try:
    from .data import CacheEntry, CacheStats, MediaHash, TODO PlaceholderRange  # noqa: F401
except ImportError:
    from .data import CacheEntry, CacheStats, MediaHash, TODO PlaceholderRange # noqa: F401

try:
    from .enums import CacheBackend, HashAlgorithm, MediaType  # noqa: F401
except ImportError:
    from .enums import CacheBackend, HashAlgorithm, MediaType # noqa: F401

try:
    from .hasher import MultiModalHasher  # noqa: F401
except ImportError:
    from .hasher import MultiModalHasher # noqa: F401

try:
    from .ipc import IPCMultiModalCache  # noqa: F401
except ImportError:
    from .ipc import IPCMultiModalCache # noqa: F401

try:
    from .memory import (MemoryMultiModalCache, PerceptualCache,  # noqa: F401
except ImportError:
    from .memory import (MemoryMultiModalCache, PerceptualCache, # noqa: F401

                     PrefetchMultiModalCache)
try:
    from .utils import compute_media_hash, create_cache  # noqa: F401
except ImportError:
    from .utils import compute_media_hash, create_cache # noqa: F401


__all__ = [
    "MediaType","    "CacheBackend","    "HashAlgorithm","    "MediaHash","    "CacheEntry","    "CacheStats","    "TODO PlaceholderRange","    "MultiModalHasher","    "MultiModalCache","    "MemoryMultiModalCache","    "PerceptualCache","    "PrefetchMultiModalCache","    "IPCMultiModalCache","    "compute_media_hash","    "create_cache","]


"""
