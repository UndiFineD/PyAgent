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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .CleanupStrategy import CleanupStrategy
from pathlib import Path
from typing import Any
from collections.abc import Callable
import logging
import shutil

__version__ = VERSION




class TestDataCleaner:
    """Utilities for cleaning up test data.

    Manages cleanup of test artifacts with configurable strategies.

    Example:
        cleaner=TestDataCleaner()
        cleaner.register_path(temp_dir)
        cleaner.register_file(temp_file)
        cleaner.cleanup_all()
    """
    __test__ = False

    def __init__(self, strategy: CleanupStrategy = CleanupStrategy.IMMEDIATE) -> None:
        """Initialize cleaner.

        Args:
            strategy: Default cleanup strategy.
        """
        self.strategy = strategy
        self._paths: list[tuple[Path, bool]] = []
        self._files: list[Path] = []
        self._callbacks: list[Callable[[], None]] = []
        self._cleanup_done = False

    def register_path(self, path: Path, recursive: bool = True) -> None:
        """Register directory for cleanup.

        Args:
            path: Directory path.
            recursive: Whether to remove recursively.
        """
        self._paths.append((path, recursive))

    def register_file(self, path: Path) -> None:
        """Register file for cleanup.

        Args:
            path: File path.
        """
        self._files.append(path)

    def register_callback(self, callback: Callable[[], None]) -> None:
        """Register cleanup callback.

        Args:
            callback: Function to call during cleanup.
        """
        self._callbacks.append(callback)

    def cleanup_all(self, force: bool = False) -> int:
        """Clean up all registered resources.

        Args:
            force: Force cleanup regardless of strategy.

        Returns:
            Number of items cleaned.
        """
        if self._cleanup_done and not force:
            return 0

        cleaned = 0

        # Clean files
        for file_path in self._files:
            try:
                if file_path.exists():
                    file_path.unlink()
                    cleaned += 1
            except OSError as e:
                logging.warning(f"Failed to clean file {file_path}: {e}")

        # Clean directories
        for path, recursive in self._paths:
            try:
                if path.exists():
                    if recursive:
                        shutil.rmtree(path)
                    else:
                        path.rmdir()
                    cleaned += 1
            except OSError as e:
                logging.warning(f"Failed to clean path {path}: {e}")

        # Run callbacks
        for callback in self._callbacks:
            try:
                callback()
                cleaned += 1
            except Exception as e:
                logging.warning(f"Cleanup callback failed: {e}")

        self._cleanup_done = True
        return cleaned

    def __enter__(self) -> TestDataCleaner:
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit - perform cleanup."""
        if self.strategy == CleanupStrategy.IMMEDIATE:
            self.cleanup_all()
