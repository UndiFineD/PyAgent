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
"""Graceful shutdown helper used by tests.

This is a compact, robust implementation providing a clean API for
installing and restoring signal handlers and persisting a tiny
shutdown state. It intentionally keeps behavior minimal for test use.
"""

from __future__ import annotations

import json
import logging
import signal
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from src.core.base.common.models import ShutdownState


__all__ = ["GracefulShutdown"]


class GracefulShutdown:
    def __init__(self, repo_root: Path | str, state_file: str = ".agent_shutdown.json") -> None:
        self.repo_root = Path(repo_root)
        self.state_file = self.repo_root / state_file
        self.state = ShutdownState()
        self._original_sigint: Optional[Any] = None
        self._original_sigterm: Optional[Any] = None

    def install_handlers(self) -> None:
        self._original_sigint = signal.signal(signal.SIGINT, self._handle_signal)
        if hasattr(signal, "SIGTERM"):
            self._original_sigterm = signal.signal(signal.SIGTERM, self._handle_signal)
        logging.debug("Installed graceful shutdown handlers")

    def restore_handlers(self) -> None:
        if self._original_sigint:
            signal.signal(signal.SIGINT, self._original_sigint)
        if self._original_sigterm and hasattr(signal, "SIGTERM"):
            signal.signal(signal.SIGTERM, self._original_sigterm)
        logging.debug("Restored original signal handlers")

    def _handle_signal(self, signum: int, _frame: Any) -> None:
        logging.warning("Received signal %s, initiating graceful shutdown...", signum)
        self.state.shutdown_requested = True
        self._save_state()

    def should_continue(self) -> bool:
        return not self.state.shutdown_requested

    def set_current_file(self, file_path: Optional[Path]) -> None:
        self.state.current_file = str(file_path) if file_path else None

    def mark_completed(self, file_path: Path) -> None:
        self.state.completed_files.append(str(file_path))
        if str(file_path) in self.state.pending_files:
            self.state.pending_files.remove(str(file_path))

    def set_pending_files(self, files: list[Path]) -> None:
        self.state.pending_files = [str(f) for f in files]

    def _save_state(self) -> None:
        try:
            data = {
                "shutdown_requested": self.state.shutdown_requested,
                "current_file": self.state.current_file,
                "completed_files": self.state.completed_files,
                "pending_files": self.state.pending_files,
                "start_time": getattr(self.state, "start_time", time.time()),
            }
            self.state_file.write_text(json.dumps(data, indent=2))
        except Exception as e:  # pragma: no cover - best-effort
            logging.error("Failed to save shutdown state: %s", e)

    def load_resume_state(self) -> Optional[ShutdownState]:
        if not self.state_file.exists():
            return None
        try:
            raw = json.loads(self.state_file.read_text())
            data = raw if isinstance(raw, dict) else {}
            state = ShutdownState(
                shutdown_requested=False,
                current_file=data.get("current_file"),
                completed_files=data.get("completed_files", []),
                pending_files=data.get("pending_files", []),
                start_time=data.get("start_time", time.time()),
            )
            logging.info("Loaded resume state: %s completed, %s pending", len(state.completed_files), len(state.pending_files))
            return state
        except Exception as e:  # pragma: no cover - non-critical
            logging.warning("Failed to load resume state: %s", e)
            return None

    def cleanup(self) -> None:
        if self.state_file.exists():
            try:
                self.state_file.unlink()
            except Exception:
                pass
        self.restore_handlers()
        self.restore_handlers()
