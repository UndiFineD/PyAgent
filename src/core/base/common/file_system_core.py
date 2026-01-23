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
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.
"""Unified file system core for atomic I/O and shared access."""

import os
import shutil
import logging
import tempfile
import fnmatch
import hashlib
from pathlib import Path
from typing import Optional, Union, List, Set
from .storage_core import StorageCore
from .utils.file_lock_manager import FileLockManager
from .models import LockType

try:
    import rust_core as rc
except ImportError:
    rc = None

class FileSystemCore:
    """
    Centralized handler for file system operations.
    Provides atomic writes, locking, and standardized backup logic.
    """

    def __init__(self, lock_manager: Optional[FileLockManager] = None):
        self.logger = logging.getLogger("pyagent.fs")
        self.lock_manager = lock_manager or FileLockManager()
        self.storage = StorageCore()
        self._ignore_patterns: Set[str] = set()

    def discover_files(
        self,
        root: Path,
        patterns: Optional[List[str]] = None,
        ignore: Optional[List[str]] = None
    ) -> List[Path]:
        """Discovers files matching patterns, respecting ignore list."""
        if patterns is None:
            patterns = ["*"]
        # Use Rust-accelerated directory walking if available
        if rc and hasattr(rc, "discover_files_rust"):  # pylint: disable=no-member
            try:
                # Map Python call to Rust name
                # pylint: disable=no-member
                files = rc.discover_files_rust(str(root), patterns, ignore or [])  # type: ignore
                return [Path(f) for f in files]
            except Exception as e:  # pylint: disable=broad-exception-caught
                self.logger.warning("Rust directory walking failed: %s", e)

        found = []
        ignore_list = ignore or list(self._ignore_patterns)

        for path in root.rglob("*"):
            if path.is_dir():
                continue

            # Apply ignore patterns
            should_ignore = False
            for pat in ignore_list:
                match_name = fnmatch.fnmatch(path.name, pat)
                match_parent = any(fnmatch.fnmatch(str(p), pat) for p in path.parents)
                if match_name or match_parent:
                    should_ignore = True
                    break
            if should_ignore:
                continue

            # Check match patterns
            for pat in patterns:
                if fnmatch.fnmatch(path.name, pat):
                    found.append(path)
                    break
        return found

    def atomic_write(
        self,
        path: Union[str, Path],
        content: str,
        encoding: str = "utf-8",
        use_lock: bool = True
    ) -> bool:
        """
        Write content to a file atomically by using a temporary file.
        Optional advisory locking.
        """
        p = Path(path)
        lock = None

        try:
            if use_lock:
                lock = self.lock_manager.acquire_lock(p, LockType.EXCLUSIVE)
                if not lock:
                    self.logger.error("Failed to acquire lock for atomic write: %s", p)
                    return False

            # Ensure parent directory exists
            p.parent.mkdir(parents=True, exist_ok=True)

            # Create temporary file in the same directory to ensure same filesystem (for os.rename)
            with tempfile.NamedTemporaryFile(
                mode='w',
                dir=p.parent,
                delete=False,
                encoding=encoding,
                suffix=".tmp"
            ) as tmp_file:
                tmp_file.write(content)
                tmp_path = Path(tmp_file.name)

            # Atomic rename (on POSIX)
            # On Windows, os.replace replaces existing, os.rename might not
            os.replace(tmp_path, p)
            return True

        except Exception as e:  # pylint: disable=broad-exception-caught
            self.logger.error("Atomic write failed for %s: %s", p, e)
            return False
        finally:
            if lock:
                self.lock_manager.release_lock(p)

    def safe_copy(self, src: Union[str, Path], dst: Union[str, Path]) -> bool:
        """Copy a file with error handling."""
        try:
            shutil.copy2(src, dst)
            return True
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.logger.error("Failed to copy %s to %s: %s", src, dst, e)
            return False

    def move(self, src: Union[str, Path], dst: Union[str, Path]) -> bool:
        """Move a file with error handling."""
        try:
            shutil.move(str(src), str(dst))
            return True
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.logger.error("Failed to move %s to %s: %s", src, dst, e)
            return False

    def delete(self, path: Union[str, Path]) -> bool:
        """Delete a file or directory with error handling."""
        p = Path(path)
        try:
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink(missing_ok=True)
            return True
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.logger.error("Failed to delete %s: %s", p, e)
            return False

    def ensure_directory(self, path: Union[str, Path]) -> Path:
        """Ensure a directory exists and return the Path object."""
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def exists(self, path: Union[str, Path]) -> bool:
        """Checks if a path exists."""
        return Path(path).exists()

    def read_text(self, path: Union[str, Path], encoding: str = "utf-8") -> str:
        """Reads the content of a file."""
        return Path(path).read_text(encoding=encoding)

    def get_file_hash(self, path: Union[str, Path]) -> Optional[str]:
        """Calculate SHA256 hash of a file."""
        p = Path(path)
        if not p.exists():
            return None
        try:
            sha256_hash = hashlib.sha256()
            with open(p, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.logger.error("Failed to calculate hash for %s: %s", p, e)
            return None
