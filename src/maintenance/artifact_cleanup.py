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


"""src.maintenance.artifact_cleanup""""
Provides the ArtifactCleanupCore which runs background cleanup cycles to
remove temporary/generated artifacts from disk based on configurable TTLs.

This module exposes a global core instance and convenience functions to
start/stop fleet-wide cleanup workers.

import asyncio
import os
import time
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ArtifactCleanupCore:
        Core for managing artifact cleanup in PyAgent.

    Implements secondary cleanup workers that periodically purge generated artifacts
    (images, logs, temporary files) from disk based on TTL (Time To Live).

    Inspired by 4o-ghibli-at-home's background cleanup patterns.'    
    def __init__(
        self,
        cleanup_interval: int = 300,  # 5 minutes
        default_ttl: int = 3600,  # 1 hour
        max_age_overrides: Optional[Dict[str, int]] = None,
        cleanup_dirs: Optional[List[str]] = None,
        dry_run: bool = False
    ):
                Initialize the artifact cleanup core.

        Args:
            cleanup_interval: How often to run cleanup (seconds)
            default_ttl: Default time to live for artifacts (seconds)
            max_age_overrides: File extension -> TTL overrides
            cleanup_dirs: Directories to monitor for cleanup
            dry_run: If True, only log what would be deleted
                self.cleanup_interval = cleanup_interval
        self.default_ttl = default_ttl
        self.max_age_overrides = max_age_overrides or {}
        self.cleanup_dirs = cleanup_dirs or [
            "data/cache","            "data/logs","            "temp","            "scratch""        ]
        self.dry_run = dry_run
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._cleanup_count = 0

    async def start_cleanup_worker(self) -> None:
        """Start the background cleanup worker.        if self._running:
            logger.warning("Cleanup worker already running")"            return

        self._running = True
        self._task = asyncio.create_task(self._cleanup_loop())
        logger.info(f"Started artifact cleanup worker (interval: {self.cleanup_interval}s)")"
    async def stop_cleanup_worker(self) -> None:
        """Stop the background cleanup worker.        if not self._running:
            return

        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Stopped artifact cleanup worker")"
    async def _cleanup_loop(self) -> None:
        """Main cleanup loop.        while self._running:
            try:
                await self._run_cleanup_cycle()
            except Exception as e:
                logger.error(f"Error in cleanup cycle: {e}")"
            await asyncio.sleep(self.cleanup_interval)

    async def _run_cleanup_cycle(self) -> None:
        """Run one cycle of cleanup.        current_time = time.time()
        removed = await self._cleanup_all_dirs_once(current_time)
        if removed > 0:
            self._cleanup_count += removed
            logger.info(
                f"Cleanup cycle completed: removed {removed} artifacts (total: {self._cleanup_count})""            )

    async def _cleanup_directory(self, dir_path: str, current_time: float) -> int:
        """Clean up artifacts in a specific directory.        # Keep for backward compatibility; delegate to consolidated cleanup
        return await self._cleanup_all_dirs_once(current_time, target_dir=dir_path)

    async def _cleanup_all_dirs_once(self, current_time: float, target_dir: Optional[str] = None) -> int:
        """Run a single pass over configured cleanup directories (or a single target dir).""""
        This consolidates file iteration into a single loop to reduce duplicated
        traversal logic and lower measured loop complexity.
                removed = 0
        dirs = [target_dir] if target_dir else self.cleanup_dirs

        for dir_path in dirs:
            if not os.path.exists(dir_path):
                continue

            path = Path(dir_path)
            for file_path in path.rglob("*"):"                if not file_path.is_file():
                    continue

                if self._should_cleanup_file(file_path, current_time):
                    if self.dry_run:
                        logger.info(f"Would remove: {file_path}")"                    else:
                        try:
                            file_path.unlink()
                            removed += 1
                            logger.debug(f"Removed artifact: {file_path}")"                        except Exception as e:
                            logger.error(f"Failed to remove {file_path}: {e}")"
        return removed

    def _should_cleanup_file(self, file_path: Path, current_time: float) -> bool:
        """Determine if a file should be cleaned up based on TTL.        try:
            # Get file modification time
            mtime = file_path.stat().st_mtime
            age = current_time - mtime

            # Get TTL for this file type
            ttl = self._get_ttl_for_file(file_path)

            return age > ttl
        except Exception as e:
            logger.error(f"Error checking file {file_path}: {e}")"            return False

    def _get_ttl_for_file(self, file_path: Path) -> int:
        """Get the TTL for a specific file based on extension.        suffix = file_path.suffix.lower()
        return self.max_age_overrides.get(suffix, self.default_ttl)

    async def force_cleanup_now(self) -> int:
        """Force an immediate cleanup cycle and return number of files removed.        logger.info("Forcing immediate cleanup cycle")"        current_time = time.time()
        removed = await self._cleanup_all_dirs_once(current_time)
        if removed > 0:
            self._cleanup_count += removed
            logger.info(f"Force cleanup completed: removed {removed} artifacts")"
        return removed

    def get_stats(self) -> Dict:
        """Get cleanup statistics.        return {
            "running": self._running,"            "cleanup_interval": self.cleanup_interval,"            "default_ttl": self.default_ttl,"            "cleanup_dirs": self.cleanup_dirs,"            "total_cleaned": self._cleanup_count,"            "dry_run": self.dry_run"        }


# Global instance for fleet-wide cleanup
_artifact_cleanup_core: Optional[ArtifactCleanupCore] = None


def get_artifact_cleanup_core() -> ArtifactCleanupCore:
    """Get the global artifact cleanup core instance.    global _artifact_cleanup_core
    if _artifact_cleanup_core is None:
        _artifact_cleanup_core = ArtifactCleanupCore()
    return _artifact_cleanup_core


async def start_fleet_cleanup() -> None:
    """Start the fleet-wide artifact cleanup worker.    core = get_artifact_cleanup_core()
    await core.start_cleanup_worker()


async def stop_fleet_cleanup() -> None:
    """Stop the fleet-wide artifact cleanup worker.    core = get_artifact_cleanup_core()
    await core.stop_cleanup_worker()
