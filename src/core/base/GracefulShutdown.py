#!/usr/bin/env python3

"""Auto-extracted class from agent.py"""

from __future__ import annotations

from src.core.base.models import ShutdownState

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

class GracefulShutdown:
    """Handles graceful shutdown with state persistence.

    Captures SIGINT / SIGTERM and allows current operation to complete
    before stopping, saving state for resume.

    Attributes:
        state: Current shutdown state.
        state_file: Path to state persistence file.
    """

    def __init__(self, repo_root: Path, state_file: str = ".agent_shutdown.json") -> None:
        """Initialize graceful shutdown handler.

        Args:
            repo_root: Repository root directory.
            state_file: Name of state file.
        """
        self.repo_root = repo_root
        self.state_file = repo_root / state_file
        self.state = ShutdownState()
        self._original_sigint = None
        self._original_sigterm = None

    def install_handlers(self) -> None:
        """Install signal handlers for graceful shutdown."""
        self._original_sigint = signal.signal(signal.SIGINT, self._handle_signal)
        if hasattr(signal, 'SIGTERM'):
            self._original_sigterm = signal.signal(signal.SIGTERM, self._handle_signal)
        logging.debug("Installed graceful shutdown handlers")

    def restore_handlers(self) -> None:
        """Restore original signal handlers."""
        if self._original_sigint:
            signal.signal(signal.SIGINT, self._original_sigint)
        if self._original_sigterm and hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, self._original_sigterm)
        logging.debug("Restored original signal handlers")

    def _handle_signal(self, signum: int, frame: Any) -> None:
        """Handle shutdown signal."""
        signal_name = signal.Signals(signum).name
        logging.warning(f"Received {signal_name}, initiating graceful shutdown...")
        self.state.shutdown_requested = True
        self._save_state()

    def should_continue(self) -> bool:
        """Check if processing should continue.

        Returns:
            bool: True if should continue, False if shutdown requested.
        """
        return not self.state.shutdown_requested

    def set_current_file(self, file_path: Optional[Path]) -> None:
        """Set the currently processing file.

        Args:
            file_path: Path to current file, or None if not processing.
        """
        self.state.current_file = str(file_path) if file_path else None

    def mark_completed(self, file_path: Path) -> None:
        """Mark a file as completed.

        Args:
            file_path: Path to completed file.
        """
        self.state.completed_files.append(str(file_path))
        if str(file_path) in self.state.pending_files:
            self.state.pending_files.remove(str(file_path))

    def set_pending_files(self, files: List[Path]) -> None:
        """Set the list of pending files.

        Args:
            files: List of pending file paths.
        """
        self.state.pending_files = [str(f) for f in files]

    def _save_state(self) -> None:
        """Save shutdown state to disk."""
        try:
            data: dict[str, Any] = {
                'shutdown_requested': self.state.shutdown_requested,
                'current_file': self.state.current_file,
                'completed_files': self.state.completed_files,
                'pending_files': self.state.pending_files,
                'start_time': self.state.start_time
            }
            self.state_file.write_text(json.dumps(data, indent=2))
        except Exception as e:
            logging.error(f"Failed to save shutdown state: {e}")

    def load_resume_state(self) -> Optional[ShutdownState]:
        """Load state for resuming an interrupted run.

        Returns:
            ShutdownState if resume state exists, None otherwise.
        """
        if not self.state_file.exists():
            return None

        try:
            raw = json.loads(self.state_file.read_text())
            data: dict[str, Any] = cast(dict[str, Any], raw) if isinstance(raw, dict) else {}
            state = ShutdownState(
                shutdown_requested=False,  # Reset for resume
                current_file=data.get('current_file'),
                completed_files=data.get('completed_files', []),
                pending_files=data.get('pending_files', []),
                start_time=data.get('start_time', time.time())
            )
            logging.info(f"Loaded resume state: {len(state.completed_files)} completed, "
                         f"{len(state.pending_files)} pending")
            return state
        except Exception as e:
            logging.warning(f"Failed to load resume state: {e}")
            return None

    def cleanup(self) -> None:
        """Clean up state file after successful completion."""
        if self.state_file.exists():
            self.state_file.unlink()
        self.restore_handlers()
