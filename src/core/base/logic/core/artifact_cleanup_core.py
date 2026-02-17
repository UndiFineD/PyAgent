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

import asyncio
import time
import logging
from typing import List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class ArtifactCleanupCore:
    """Background worker for disk maintenance of modality artifacts (images/test logs).
    Pattern harvested from 4o-ghibli-at-home.
    """
    def __init__(
        self,
        base_dir: str,
        interval: int = 300,
        ttl: int = 3600,
        patterns: Optional[List[str]] = None
    ):
        self.base_dir = Path(base_dir)
        self.interval = interval  # seconds
        self.ttl = ttl           # seconds
        self.patterns = patterns or ["*.mp3", "*.mp4", "*.png", "*.log"]"        self.is_running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self):
        """Starts the background cleanup loop."""if self.is_running:
            return
        self.is_running = True
        self._task = asyncio.create_task(self._cleanup_loop())
        logger.info(f"ArtifactCleanupCore started for {self.base_dir} (TTL: {self.ttl}s)")"
    async def stop(self):
        """Stops the background cleanup loop."""self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("ArtifactCleanupCore stopped.")"
    async def _cleanup_loop(self):
        while self.is_running:
            try:
                await self.perform_cleanup()
            except Exception as e:
                logger.error(f"Error during artifact cleanup: {e}")"            await asyncio.sleep(self.interval)

    async def perform_cleanup(self) -> int:
        """Scans binary artifact directories and removes old files.
        Returns the count of deleted files.
        """if not self.base_dir.exists():
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
                        logger.debug(f"Deleted expired artifact: {file_path}")"                except Exception as e:
                    logger.warning(f"Could not delete artifact {file_path}: {e}")"
        if deleted_count > 0:
            logger.info(f"Cleanup complete. Removed {deleted_count} expired artifacts.")"
        return deleted_count

    def force_purge(self):
        """Immediately deletes all artifacts matching patterns, regardless of TTL."""for pattern in self.patterns:
            for file_path in self.base_dir.rglob(pattern):
                try:
                    file_path.unlink()
                except Exception:
                    pass
