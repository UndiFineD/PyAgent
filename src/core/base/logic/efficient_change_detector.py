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
Efficient Change Detection Core - USN-inspired change tracking for file systems
Based on ADSpider's replication metadata approach for efficient monitoring
"""

import asyncio
import os
import time
import hashlib
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set, Callable
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@dataclass
class ChangeRecord:
    """Record of a file system change"""
    path: str
    change_type: str  # 'created', 'modified', 'deleted'
    timestamp: float
    usn: int  # Update Sequence Number for ordering
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FileMetadata:
    """Metadata for efficient change detection"""
    path: str
    size: int
    mtime: float
    usn: int
    hash: Optional[str] = None
    last_checked: float = field(default_factory=time.time)


class EfficientChangeDetector:
    """
    USN-inspired change detection for file systems
    Uses metadata-based tracking instead of full content scanning
    """

    def __init__(self, root_path: str, enable_hashing: bool = False):
        self.root_path = Path(root_path).resolve()
        self.enable_hashing = enable_hashing
        self.current_usn = 0
        self.metadata_cache: Dict[str, FileMetadata] = {}
        self.change_history: List[ChangeRecord] = []
        self.excluded_patterns: Set[str] = {'.git', '__pycache__', '.pytest_cache', 'node_modules'}

    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded from monitoring"""
        path_str = str(path)
        for pattern in self.excluded_patterns:
            if pattern in path_str:
                return True
        return False

    def _calculate_file_hash(self, path: Path) -> Optional[str]:
        """Calculate SHA256 hash of file content"""
        if not self.enable_hashing:
            return None

        try:
            with open(path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except (OSError, IOError):
            return None

    def _get_file_metadata(self, path: Path) -> Optional[FileMetadata]:
        """Get metadata for a file"""
        try:
            stat = path.stat()
            return FileMetadata(
                path=str(path),
                size=stat.st_size,
                mtime=stat.st_mtime,
                usn=self.current_usn,
                hash=self._calculate_file_hash(path),
                last_checked=time.time()
            )
        except (OSError, FileNotFoundError):
            return None

    def _scan_directory(self, path: Path) -> Dict[str, FileMetadata]:
        """Scan directory and return metadata for all files"""
        metadata = {}

        try:
            for root, dirs, files in os.walk(path):
                root_path = Path(root)

                # Skip excluded directories
                dirs[:] = [d for d in dirs if not self._should_exclude(root_path / d)]

                for file in files:
                    file_path = root_path / file
                    if not self._should_exclude(file_path):
                        meta = self._get_file_metadata(file_path)
                        if meta:
                            metadata[str(file_path)] = meta

        except (OSError, PermissionError) as e:
            logger.warning(f"Error scanning directory {path}: {e}")

        return metadata

    def initialize_baseline(self) -> Dict[str, FileMetadata]:
        """Initialize baseline metadata for all files"""
        logger.info(f"Initializing baseline for {self.root_path}")
        self.metadata_cache = self._scan_directory(self.root_path)
        self.current_usn += 1
        logger.info(f"Baseline initialized with {len(self.metadata_cache)} files")
        return self.metadata_cache.copy()

    def detect_changes(self) -> List[ChangeRecord]:
        """
        Detect changes using USN-based approach
        Returns list of changes since last check
        """
        changes = []
        self.current_usn += 1

        # Scan current state
        current_metadata = self._scan_directory(self.root_path)

        # Find new and modified files
        for path_str, current_meta in current_metadata.items():
            if path_str not in self.metadata_cache:
                # New file
                changes.append(ChangeRecord(
                    path=path_str,
                    change_type='created',
                    timestamp=time.time(),
                    usn=self.current_usn,
                    metadata={'size': current_meta.size, 'mtime': current_meta.mtime}
                ))
            else:
                # Check for modifications
                cached_meta = self.metadata_cache[path_str]
                if (current_meta.mtime > cached_meta.mtime or
                        current_meta.size != cached_meta.size or
                        (self.enable_hashing and current_meta.hash != cached_meta.hash)):
                    changes.append(ChangeRecord(
                        path=path_str,
                        change_type='modified',
                        timestamp=time.time(),
                        usn=self.current_usn,
                        metadata={
                            'old_size': cached_meta.size,
                            'new_size': current_meta.size,
                            'old_mtime': cached_meta.mtime,
                            'new_mtime': current_meta.mtime
                        }
                    ))

        # Find deleted files
        for path_str, cached_meta in self.metadata_cache.items():
            if path_str not in current_metadata:
                changes.append(ChangeRecord(
                    path=path_str,
                    change_type='deleted',
                    timestamp=time.time(),
                    usn=self.current_usn,
                    metadata={'size': cached_meta.size, 'mtime': cached_meta.mtime}
                ))

        # Update cache
        self.metadata_cache = current_metadata

        # Add to history
        self.change_history.extend(changes)

        # Keep history bounded (last 1000 changes)
        if len(self.change_history) > 1000:
            self.change_history = self.change_history[-1000:]

        return changes

    async def monitor_changes(
        self,
        callback: Callable[[List[ChangeRecord]], None],
        interval: float = 30.0,
        max_iterations: Optional[int] = None
    ):
        """
        Monitor for changes asynchronously
        Calls callback with list of changes when detected
        """
        iteration = 0

        while max_iterations is None or iteration < max_iterations:
            changes = self.detect_changes()

            if changes:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(changes)
                    else:
                        callback(changes)
                except Exception as e:
                    logger.error(f"Error in change callback: {e}")

            iteration += 1
            await asyncio.sleep(interval)


    def get_change_statistics(self) -> Dict[str, Any]:
        """Get statistics about detected changes"""
        if not self.change_history:
            return {'total_changes': 0}

        change_types = {}
        for change in self.change_history:
            change_types[change.change_type] = change_types.get(change.change_type, 0) + 1

        return {
            'total_changes': len(self.change_history),
            'change_types': change_types,
            'time_range': {
                'oldest': min(c.timestamp for c in self.change_history),
                'newest': max(c.timestamp for c in self.change_history)
            },
            'current_usn': self.current_usn,
            'monitored_files': len(self.metadata_cache)
        }

    def filter_changes_by_type(self, changes: List[ChangeRecord], change_type: str) -> List[ChangeRecord]:
        """Filter changes by type"""
        return [c for c in changes if c.change_type == change_type]

    def filter_changes_by_path(self, changes: List[ChangeRecord], path_pattern: str) -> List[ChangeRecord]:
        """Filter changes by path pattern"""
        return [c for c in changes if path_pattern in c.path]

    def get_recent_changes(self, since_timestamp: float) -> List[ChangeRecord]:
        """Get changes since timestamp"""
        return [c for c in self.change_history if c.timestamp >= since_timestamp]
