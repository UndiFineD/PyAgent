#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from .IncrementalState import IncrementalState

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from types import TracebackType
from typing import List, Set, Optional, Dict, Any, Callable, Iterable, TypeVar, cast, Final
import argparse
import asyncio
import difflib
import fnmatch
import functools
import hashlib
import importlib.util
import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time
import uuid

class IncrementalProcessor:
    """Processes only files changed since last run.

    Tracks file modification times and content hashes to enable
    incremental processing, avoiding reprocessing unchanged files.

    Attributes:
        state_file: Path to state persistence file.
        state: Current incremental processing state.
    """

    def __init__(self, repo_root: Path, state_file: str = ".agent_state.json") -> str:
        """Initialize the incremental processor.

        Args:
            repo_root: Repository root directory.
            state_file: Name of state file.
        """
        self.repo_root = repo_root
        self.state_file = repo_root / state_file
        self.state = IncrementalState()
        self._load_state()

    def _load_state(self) -> None:
        """Load state from disk."""
        if self.state_file.exists():
            try:
                raw = json.loads(self.state_file.read_text())
                if isinstance(raw, dict):
                    data: dict[str, Any] = cast(dict[str, Any], raw)
                else:
                    data = {}
                self.state = IncrementalState(
                    last_run_timestamp=data.get('last_run_timestamp', 0),
                    processed_files=data.get('processed_files', {}),
                    file_hashes=data.get('file_hashes', {}),
                    pending_files=data.get('pending_files', [])
                )
                logging.debug(f"Loaded incremental state from {self.state_file}")
            except Exception as e:
                logging.warning(f"Failed to load state: {e}")

    def _save_state(self) -> None:
        """Save state to disk."""
        try:
            data: dict[str, Any] = {
                'last_run_timestamp': self.state.last_run_timestamp,
                'processed_files': self.state.processed_files,
                'file_hashes': self.state.file_hashes,
                'pending_files': self.state.pending_files
            }
            self.state_file.write_text(json.dumps(data, indent=2))
            logging.debug(f"Saved incremental state to {self.state_file}")
        except Exception as e:
            logging.warning(f"Failed to save state: {e}")

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute MD5 hash of file content."""
        try:
            content = file_path.read_bytes()
            return hashlib.md5(content).hexdigest()
        except Exception:
            return ""

    def get_changed_files(self, files: List[Path]) -> List[Path]:
        """Get list of files changed since last run.

        Args:
            files: List of all files to consider.

        Returns:
            List of files that have changed.
        """
        changed: list[Path] = []

        for file_path in files:
            path_str = str(file_path)

            # Check if file is new
            if path_str not in self.state.processed_files:
                changed.append(file_path)
                continue

            # Check if file was modified
            try:
                mtime = file_path.stat().st_mtime
                if mtime > self.state.processed_files.get(path_str, 0):
                    # Verify with hash comparison
                    new_hash = self._compute_file_hash(file_path)
                    if new_hash != self.state.file_hashes.get(path_str, ""):
                        changed.append(file_path)
            except Exception:
                changed.append(file_path)

        logging.info(f"Incremental: {len(changed)}/{len(files)} files changed")
        return changed

    def mark_processed(self, file_path: Path) -> None:
        """Mark a file as processed.

        Args:
            file_path: Path to the processed file.
        """
        path_str = str(file_path)
        self.state.processed_files[path_str] = time.time()
        self.state.file_hashes[path_str] = self._compute_file_hash(file_path)

        # Remove from pending if present
        if path_str in self.state.pending_files:
            self.state.pending_files.remove(path_str)

    def complete_run(self) -> None:
        """Mark the run as complete and save state."""
        self.state.last_run_timestamp = time.time()
        self.state.pending_files = []
        self._save_state()

    def reset_state(self) -> None:
        """Reset incremental state (force full reprocessing)."""
        self.state = IncrementalState()
        if self.state_file.exists():
            self.state_file.unlink()
        logging.info("Incremental state reset")
