# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified file system core for atomic I/O and shared access."""

import os
import shutil
import logging
import tempfile
import fnmatch
from pathlib import Path
from typing import Any, Optional, Union, List, Set
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

    def discover_files(self, root: Path, patterns: List[str] = ["*"], ignore: Optional[List[str]] = None) -> List[Path]:
        """Discovers files matching patterns, respecting ignore list."""
        # Use Rust-accelerated directory walking if available
        if rc and hasattr(rc, "discover_files_rust"):  # pylint: disable=no-member
            try:
                # Map Python call to Rust name
                files = rc.discover_files_rust(str(root), patterns, ignore or []) # type: ignore
                return [Path(f) for f in files]
            except Exception as e: # pylint: disable=broad-exception-caught
                self.logger.warning(f"Rust directory walking failed: {e}")

        found = []
        ignore_list = ignore or list(self._ignore_patterns)
        
        for path in root.rglob("*"):
            if path.is_dir(): continue
            
            # Apply ignore patterns
            should_ignore = False
            for pat in ignore_list:
                if fnmatch.fnmatch(path.name, pat) or any(fnmatch.fnmatch(str(p), pat) for p in path.parents):
                    should_ignore = True
                    break
            if should_ignore: continue
            
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
                    self.logger.error(f"Failed to acquire lock for atomic write: {p}")
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
            
        except Exception as e: # pylint: disable=broad-exception-caught
            self.logger.error(f"Atomic write failed for {p}: {e}")
            return False
        finally:
            if lock:
                self.lock_manager.release_lock(p)

    def safe_copy(self, src: Union[str, Path], dst: Union[str, Path]) -> bool:
        """Copy a file with error handling."""
        try:
            shutil.copy2(src, dst)
            return True
        except Exception as e: # pylint: disable=broad-exception-caught
            self.logger.error(f"Failed to copy {src} to {dst}: {e}")
            return False

    def move(self, src: Union[str, Path], dst: Union[str, Path]) -> bool:
        """Move a file with error handling."""
        try:
            shutil.move(str(src), str(dst))
            return True
        except Exception as e: # pylint: disable=broad-exception-caught
            self.logger.error(f"Failed to move {src} to {dst}: {e}")
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
        except Exception as e: # pylint: disable=broad-exception-caught
            self.logger.error(f"Failed to delete {p}: {e}")
            return False

    def ensure_directory(self, path: Union[str, Path]) -> Path:
        """Ensure a directory exists and return the Path object."""
        p = Path(path)
        p.mkdir(parents=True, exist_ok=True)
        return p

    def get_file_hash(self, path: Union[str, Path]) -> Optional[str]:
        """Calculate SHA256 hash of a file."""
        import hashlib
        p = Path(path)
        if not p.exists():
            return None
        try:
            sha256_hash = hashlib.sha256()
            with open(p, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e: # pylint: disable=broad-exception-caught
            self.logger.error(f"Failed to calculate hash for {p}: {e}")
            return None
