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

"""
LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/artifact_cleanup_core.description.md

# artifact_cleanup_core

**File**: `src\core\base\logic\core\artifact_cleanup_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 106  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for artifact_cleanup_core.

## Classes (1)

### `ArtifactCleanupCore`

Background worker for disk maintenance of modality artifacts (images/test logs).
Pattern harvested from 4o-ghibli-at-home.

**Methods** (2):
- `__init__(self, base_dir, interval, ttl, patterns)`
- `force_purge(self)`

## Dependencies

**Imports** (8):
- `asyncio`
- `logging`
- `os`
- `pathlib.Path`
- `time`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/artifact_cleanup_core.improvements.md

# Improvements for artifact_cleanup_core

**File**: `src\core\base\logic\core\artifact_cleanup_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 106 lines (medium)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `artifact_cleanup_core_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import asyncio
import os
import time
import logging
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class ArtifactCleanupCore:
    """
    Background worker for disk maintenance of modality artifacts (images/test logs).
    Pattern harvested from 4o-ghibli-at-home.
    """

    def __init__(
        self,
        base_dir: str,
        interval: int = 300,
        ttl: int = 3600,
        patterns: Optional[List[str]] = None,
    ):
        self.base_dir = Path(base_dir)
        self.interval = interval  # seconds
        self.ttl = ttl  # seconds
        self.patterns = patterns or ["*.mp3", "*.mp4", "*.png", "*.log"]
        self.is_running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """Starts the background cleanup loop."""
        if self.is_running:
            return
        self.is_running = True
        self._task = asyncio.create_task(self._cleanup_loop())
        logger.info(
            f"ArtifactCleanupCore started for {self.base_dir} (TTL: {self.ttl}s)"
        )

    async def stop(self):
        """Stops the background cleanup loop."""
        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("ArtifactCleanupCore stopped.")

    async def _cleanup_loop(self):
        while self.is_running:
            try:
                await self.perform_cleanup()
            except Exception as e:
                logger.error(f"Error during artifact cleanup: {e}")
            await asyncio.sleep(self.interval)

    async def perform_cleanup(self) -> int:
        """
        Scans binary artifact directories and removes old files.
        Returns the count of deleted files.
        """
        if not self.base_dir.exists():
            return 0

        current_time = time.time()
        deleted_count = 0

        for pattern in self.patterns:
            for file_path in self.base_dir.rglob(pattern):
                try:
                    stats = file_path.stat()
                    # Use last modification time
                    if (current_time - stats.st_mtime) > self.ttl:
                        file_path.unlink()
                        deleted_count += 1
                        logger.debug(f"Deleted expired artifact: {file_path}")
                except Exception as e:
                    logger.warning(f"Could not delete artifact {file_path}: {e}")

        if deleted_count > 0:
            logger.info(f"Cleanup complete. Removed {deleted_count} expired artifacts.")

        return deleted_count

    def force_purge(self):
        """Immediately deletes all artifacts matching patterns, regardless of TTL."""
        for pattern in self.patterns:
            for file_path in self.base_dir.rglob(pattern):
                try:
                    file_path.unlink()
                except Exception:
                    pass
