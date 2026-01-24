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
Model cache for LM Studio handles.
"""

import time
from typing import Any

from .models import CachedModel


class ModelCache:
    """Simple model cache with TTL."""

    def __init__(self, ttl: float = 300.0):
        self._cache: dict[str, CachedModel] = {}
        self._ttl = ttl

    def get(self, model_id: str) -> CachedModel | None:
        """Get cached model if not expired."""
        entry = self._cache.get(model_id)
        if entry is None:
            return None
        if entry.is_expired(self._ttl):
            del self._cache[model_id]
            return None
        entry.touch()
        return entry

    def set(self, model_id: str, model_info: Any) -> CachedModel:
        """Cache a model reference."""
        entry = CachedModel(
            model_id=model_id,
            model_info=model_info,
            loaded_at=time.time(),
        )
        self._cache[model_id] = entry
        return entry

    def clear(self) -> None:
        """Clear the cache."""
        self._cache.clear()

    def prune_expired(self) -> int:
        """Remove expired entries, return count removed."""
        expired = [k for k, v in self._cache.items() if v.is_expired(self._ttl)]
        for k in expired:
            del self._cache[k]
        return len(expired)
