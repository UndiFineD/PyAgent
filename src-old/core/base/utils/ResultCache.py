#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/utils/ResultCache.description.md

# ResultCache

**File**: `src\core\base\utils\ResultCache.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 123  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent.py

## Classes (1)

### `ResultCache`

Cache agent results for reuse.

Example:
    cache=ResultCache()

    # Check cache
    result=cache.get("test.py", "coder", content_hash)
    if result is None:
        result=run_coder("test.py")
        cache.set("test.py", "coder", content_hash, result)

**Methods** (6):
- `__init__(self, cache_dir)`
- `_make_key(self, file_path, agent_name, content_hash)`
- `get(self, file_path, agent_name, content_hash)`
- `set(self, file_path, agent_name, content_hash, result, ttl_seconds)`
- `invalidate(self, file_path)`
- `clear(self)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `pathlib.Path`
- `src.core.base.models.CachedResult`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/utils/ResultCache.improvements.md

# Improvements for ResultCache

**File**: `src\core\base\utils\ResultCache.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 123 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ResultCache_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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


"""Auto-extracted class from agent.py"""

from src.core.base.version import VERSION
from src.core.base.models import CachedResult
from pathlib import Path
from typing import Optional, Dict, Any
import time

__version__ = VERSION


class ResultCache:
    """Cache agent results for reuse.

    Example:
        cache=ResultCache()

        # Check cache
        result=cache.get("test.py", "coder", content_hash)
        if result is None:
            result=run_coder("test.py")
            cache.set("test.py", "coder", content_hash, result)
    """

    def __init__(self, cache_dir: Path | None = None) -> None:
        """Initialize cache.

        Args:
            cache_dir: Directory for persistent cache.
        """
        self.cache_dir = cache_dir
        self._memory_cache: dict[str, CachedResult] = {}

    def _make_key(self, file_path: str, agent_name: str, content_hash: str) -> str:
        """Create cache key."""
        return f"{file_path}:{agent_name}:{content_hash}"

    def get(
        self,
        file_path: str,
        agent_name: str,
        content_hash: str,
    ) -> Any | None:
        """Get cached result.

        Args:
            file_path: File path.
            agent_name: Agent name.
            content_hash: Hash of content.

        Returns:
            Cached result or None.
        """
        key = self._make_key(file_path, agent_name, content_hash)

        if key in self._memory_cache:
            cached = self._memory_cache[key]
            # Check TTL
            if time.time() - cached.timestamp < cached.ttl_seconds:
                return cached.result
            else:
                del self._memory_cache[key]

        return None

    def set(
        self,
        file_path: str,
        agent_name: str,
        content_hash: str,
        result: Any,
        ttl_seconds: int = 3600,
    ) -> None:
        """Cache a result.

        Args:
            file_path: File path.
            agent_name: Agent name.
            content_hash: Hash of content.
            result: Result to cache.
            ttl_seconds: Time to live.
        """
        key = self._make_key(file_path, agent_name, content_hash)
        self._memory_cache[key] = CachedResult(
            file_path=file_path,
            agent_name=agent_name,
            content_hash=content_hash,
            result=result,
            ttl_seconds=ttl_seconds,
        )

    def invalidate(self, file_path: str) -> int:
        """Invalidate all cache entries for a file.

        Args:
            file_path: File path.

        Returns:
            Number of entries invalidated.
        """
        to_remove = [k for k in self._memory_cache if k.startswith(f"{file_path}:")]
        for key in to_remove:
            del self._memory_cache[key]
        return len(to_remove)

    def clear(self) -> None:
        """Clear all cached results."""
        self._memory_cache.clear()
