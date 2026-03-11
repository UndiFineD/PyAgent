"""LLM_CONTEXT_START

## Source: src-old/core/base/state.description.md

# state

**File**: `src\\core\base\\state.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 13 imports  
**Lines**: 129  
**Complexity**: 10 (moderate)

## Overview

State management for swarm agents.
Handles persistence of agent memory, history, and metadata.

## Classes (3)

### `EmergencyEventLog`

Phase 278: Ring buffer recording the last 10 filesystem actions for recovery.

**Methods** (3):
- `__init__(self, log_path)`
- `_load_buffer(self)`
- `record_action(self, action, details)`

### `StateTransaction`

Phase 267: Transactional context manager for agent file operations.

**Methods** (5):
- `__init__(self, target_files)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`
- `commit(self)`
- `rollback(self)`

### `AgentStateManager`

Manages saving and loading agent state to/from disk.

**Methods** (2):
- `save_state(file_path, current_state, token_usage, state_data, history_len, path)`
- `load_state(file_path, path)`

## Dependencies

**Imports** (13):
- `__future__.annotations`
- `collections`
- `json`
- `logging`
- `pathlib.Path`
- `shutil`
- `src.core.base.version.VERSION`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/state.improvements.md

# Improvements for state

**File**: `src\\core\base\\state.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 129 lines (medium)  
**Complexity**: 10 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `state_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

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

import collections
import json
import logging
import shutil
import time
from pathlib import Path
from typing import Any

from src.core.base.version import VERSION

__version__ = VERSION


class EmergencyEventLog:
    """Phase 278: Ring buffer recording the last 10 filesystem actions for recovery."""

    def __init__(
        self, log_path: Path = Path("data/logs/emergency_recovery.log")
    ) -> None:
        self.log_path = log_path
        self.buffer = collections.deque(maxlen=10)
        self._load_buffer()

    def _load_buffer(self) -> None:
        if self.log_path.exists():
            try:
                content = self.log_path.read_text(encoding="utf-8")
                self.buffer.extend(content.splitlines())
            except Exception:
                pass

    def record_action(self, action: str, details: str) -> None:
        event = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {action}: {details}"
        self.buffer.append(event)
        try:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            self.log_path.write_text("\n".join(self.buffer), encoding="utf-8")
        except Exception as e:
            logging.error(f"StructuredLogger: Failed to write emergency log: {e}")


# Global instance for easy access (Phase 278)
EMERGENCY_LOG = EmergencyEventLog()


class StateTransaction:
    """Phase 267: Transactional context manager for agent file operations."""

    def __init__(self, target_files: list[Path]) -> None:
        self.target_files = target_files
        self.backups: dict[Path, Path] = {}
        self.temp_dir = Path("temp/transactions")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        self.id = f"tx_{int(time.time()*1000)}"

    def __enter__(self) -> StateTransaction:

        for file in self.target_files:
            if file.exists():
                backup_path = self.temp_dir / f"{file.name}_{self.id}.bak"
                shutil.copy2(file, backup_path)
                self.backups[file] = backup_path
        logging.info(
            f"Transaction {self.id} started. {len(self.backups)} files backed up."
        )
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
                shutil.copy2(backup, original)
                backup.unlink()
        logging.warning(f"Transaction {self.id} ROLLED BACK. Files restored.")


class AgentStateManager:
    """Manages saving and loading agent state to/from disk."""

    @staticmethod
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
        state_path.write_text(json.dumps(state, indent=2), encoding="utf-8")
        logging.debug(f"State saved to {state_path}")

    @staticmethod
    def load_state(file_path: Path, path: Path | None = None) -> dict[str, Any] | None:
        """Load agent state from disk."""
        state_path: Path = path or file_path.with_suffix(".state.json")
        if not state_path.exists():
            return None

        try:
            return json.loads(state_path.read_text(encoding="utf-8"))
        except Exception as e:
            logging.warning(f"Failed to load state: {e}")
            return None
