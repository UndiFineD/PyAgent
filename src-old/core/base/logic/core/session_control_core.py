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

"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/session_control_core.description.md

# session_control_core

**File**: `src\\core\base\\logic\\core\\session_control_core.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 5 imports  
**Lines**: 69  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for session_control_core.

## Classes (2)

### `SessionSignal`

**Inherits from**: Enum

Signals for agent session lifecycle control.

### `SessionControlCore`

Manages session interrupt signals and shared state flags for long-running agent tasks.
Enables orchestration layers to pause or stop agents mid-loop via filesystem or shared memory flags.
Lesson harvested from .external/agentcloud pattern.

**Methods** (6):
- `__init__(self, storage_dir)`
- `_get_signal_file(self, session_id)`
- `set_signal(self, session_id, signal)`
- `get_signal(self, session_id)`
- `check_interrupt(self, session_id)`
- `check_pause(self, session_id)`

## Dependencies

**Imports** (5):
- `enum`
- `json`
- `pathlib.Path`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/session_control_core.improvements.md

# Improvements for session_control_core

**File**: `src\\core\base\\logic\\core\\session_control_core.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 69 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `session_control_core_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

import enum
import json
from pathlib import Path


class SessionSignal(enum.Enum):
    """Signals for agent session lifecycle control."""

    RUNNING = "running"
    PAUSE = "pause"
    STOP = "stop"
    RESUME = "resume"


class SessionControlCore:
    """Manages session interrupt signals and shared state flags for long-running agent tasks.
    Enables orchestration layers to pause or stop agents mid-loop via filesystem or shared memory flags.
    Lesson harvested from .external/agentcloud pattern.
    """

    def __init__(self, storage_dir: str = "data/agent_cache/sessions") -> None:
        self.storage_path = Path(storage_dir)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def _get_signal_file(self, session_id: str) -> Path:
        return self.storage_path / f"{session_id}_signal.json"

    def set_signal(self, session_id: str, signal: SessionSignal) -> None:
        """Sets a control signal for a specific session."""
        file_path = self._get_signal_file(session_id)
        data = {"signal": signal.value, "session_id": session_id}

        # In a real system, this would be an atomic write or a Redis call.
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def get_signal(self, session_id: str) -> SessionSignal:
        """Retrieves the current signal for a session."""
        file_path = self._get_signal_file(session_id)
        if not file_path.exists():
            return SessionSignal.RUNNING

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return SessionSignal(data.get("signal", "running"))
        except (json.JSONDecodeError, ValueError):
            return SessionSignal.RUNNING

    def check_interrupt(self, session_id: str) -> bool:
        """Returns True if the session should stop immediately."""
        return self.get_signal(session_id) == SessionSignal.STOP

    def check_pause(self, session_id: str) -> bool:
        """Returns True if the session should pause."""
        return self.get_signal(session_id) == SessionSignal.PAUSE
