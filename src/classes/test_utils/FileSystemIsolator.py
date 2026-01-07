#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from .IsolationLevel import IsolationLevel

from pathlib import Path
from typing import Any, List, Optional
import os
import shutil
import tempfile

class FileSystemIsolator:
    """Isolates file system operations for testing.

    Example:
        with FileSystemIsolator() as fs:
            fs.write_file("test.txt", "content")
            content=fs.read_file("test.txt")
    """

    def __init__(
        self,
        isolation_level: IsolationLevel = IsolationLevel.TEMP_DIR,
    ) -> None:
        """Initialize file system isolator.

        Args:
            isolation_level: Level of isolation.
        """
        self.isolation_level = isolation_level
        self._temp_dir: Optional[Path] = None
        self._original_cwd: Optional[str] = None
        self._created_files: List[Path] = []

    def __enter__(self) -> "FileSystemIsolator":
        """Enter context and set up isolation."""
        if self.isolation_level == IsolationLevel.TEMP_DIR:
            self._temp_dir = Path(tempfile.mkdtemp())
            self._original_cwd = os.getcwd()
            os.chdir(self._temp_dir)
        return self

    def __exit__(self, *args: Any) -> None:
        """Exit context and clean up."""
        if self._original_cwd:
            os.chdir(self._original_cwd)
        if self._temp_dir and self._temp_dir.exists():
            shutil.rmtree(self._temp_dir)
        self._created_files.clear()

    def write_file(self, path: str, content: str) -> Path:
        """Write a file in isolated environment.

        Args:
            path: File path.
            content: File content.

        Returns:
            Path: Path to created file.
        """
        file_path = Path(path)
        if self._temp_dir:
            file_path = self._temp_dir / path

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        self._created_files.append(file_path)
        return file_path

    def read_file(self, path: str) -> str:
        """Read a file from isolated environment.

        Args:
            path: File path.

        Returns:
            str: File content.
        """
        file_path = Path(path)
        if self._temp_dir:
            file_path = self._temp_dir / path
        return file_path.read_text(encoding="utf-8")

    def get_temp_dir(self) -> Optional[Path]:
        """Get the temporary directory."""
        return self._temp_dir
