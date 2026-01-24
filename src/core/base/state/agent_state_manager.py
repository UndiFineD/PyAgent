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
State management for swarm agents.
Handles persistence of agent memory, history, and metadata.
"""

from __future__ import annotations

import collections
import json
import logging
import time
from pathlib import Path
from typing import Any

from src.core.base.common.file_system_core import FileSystemCore
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class EmergencyEventLog:
    """Phase 278: Ring buffer recording the last 10 filesystem actions for recovery."""

    def __init__(self, log_path: Path = Path("data/logs/emergency_recovery.log")) -> None:
        self.log_path = log_path
        self.buffer = collections.deque(maxlen=10)
        self._fs = FileSystemCore()

        self._load_buffer()

    def _load_buffer(self) -> None:
        if self.log_path.exists():
            try:
                content = self.log_path.read_text(encoding="utf-8")
                self.buffer.extend(content.splitlines())

            except Exception:  # pylint: disable=broad-exception-caught
                pass

    def record_action(self, action: str, details: str) -> None:
        """Record an action to the emergency log."""
        event = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {action}: {details}"

        self.buffer.append(event)
        try:
            self._fs.atomic_write(self.log_path, "\n".join(self.buffer))
        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.error(f"StructuredLogger: Failed to write emergency log: {e}")


# Global instance for easy access (Phase 278)


EMERGENCY_LOG = EmergencyEventLog()


class StateTransaction:
    """Phase 267: Transactional context manager for agent file operations."""

    def __init__(self, target_files: list[Path]) -> None:
        self.target_files = target_files

        self.backups: dict[Path, Path] = {}
        self.temp_dir = Path("temp/transactions")
        self._fs = FileSystemCore()
        self._fs.ensure_directory(self.temp_dir)
        self.id = f"tx_{int(time.time() * 1000)}"

    def __enter__(self) -> StateTransaction:
        for file in self.target_files:
            if file.exists():
                backup_path = self.temp_dir / f"{file.name}_{self.id}.bak"
                self._fs.safe_copy(file, backup_path)
                self.backups[file] = backup_path
        logging.info(f"Transaction {self.id} started. {len(self.backups)} files backed up.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()

    def commit(self) -> None:
        """Discard backups after successful transaction."""
        for backup in self.backups.values():
            if backup.exists():
                backup.unlink()
        logging.info(f"Transaction {self.id} committed successfully.")

    def rollback(self) -> None:
        """Restore files from backups after failure."""
        for original, backup in self.backups.items():
            if backup.exists():
                self._fs.safe_copy(backup, original)
                backup.unlink()
        logging.warning(f"Transaction {self.id} ROLLED BACK. Files restored.")


class AgentStateManager:
    """Manages saving and loading agent state to/from disk."""

    @staticmethod
    # pylint: disable=too-many-positional-arguments
    def save_state(
        file_path: Path,
        current_state: str,
        token_usage: int,
        state_data: dict[str, Any],
        history_len: int,
        path: Path | None = None,
    ) -> None:
        """Save agent state to disk."""
        state_path: Path = path or file_path.with_suffix(".state.json")
        state: dict[str, Any] = {
            "file_path": str(file_path),
            "state": current_state,
            "token_usage": token_usage,
            "state_data": state_data,
            "history_length": history_len,
        }
        FileSystemCore().atomic_write(state_path, json.dumps(state, indent=2))
        logging.debug(f"State saved to {state_path}")

    @staticmethod
    def load_state(file_path: Path, path: Path | None = None) -> dict[str, Any] | None:
        """Load agent state from disk."""
        state_path: Path = path or file_path.with_suffix(".state.json")
        if not state_path.exists():
            return None

        try:
            return json.loads(state_path.read_text(encoding="utf-8"))
        except Exception as e:  # pylint: disable=broad-exception-caught
            logging.warning(f"Failed to load state: {e}")
            return None
