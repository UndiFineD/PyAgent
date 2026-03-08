"""
LLM_CONTEXT_START

## Source: src-old/core/modules/SignalModule.description.md

# SignalModule

**File**: `src\core\modules\SignalModule.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 68  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for SignalModule.

## Classes (1)

### `SignalModule`

**Inherits from**: BaseModule

Consolidated core module for signal processing.
Migrated from SignalCore.

**Methods** (5):
- `initialize(self)`
- `execute(self, action)`
- `create_event(self, signal_name, data, sender)`
- `prune_history(self, history, limit)`
- `shutdown(self)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `datetime.datetime`
- `src.core.base.modules.BaseModule`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/core/modules/SignalModule.improvements.md

# Improvements for SignalModule

**File**: `src\core\modules\SignalModule.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 68 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SignalModule_test.py` with pytest tests

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

from datetime import datetime
from typing import Any, Dict, List
from src.core.base.modules import BaseModule


class SignalModule(BaseModule):
    """
    Consolidated core module for signal processing.
    Migrated from SignalCore.
    """

    def initialize(self) -> bool:
        """Initialize signal handlers."""
        return super().initialize()

    def execute(self, action: str, **kwargs) -> Any:
        """
        Executes signal-related logic.
        Supported actions: create_event, prune_history
        """
        if not self.initialized:
            self.initialize()

        if action == "create_event":
            return self.create_event(
                kwargs.get("signal_name", "generic"),
                kwargs.get("data"),
                kwargs.get("sender", "unknown"),
            )
        elif action == "prune_history":
            return self.prune_history(
                kwargs.get("history", []), kwargs.get("limit", 100)
            )
        return None

    def create_event(self, signal_name: str, data: Any, sender: str) -> dict[str, Any]:
        """Creates a standardized signal event object."""
        return {
            "signal": signal_name,
            "data": data,
            "sender": sender,
            "timestamp": datetime.now().isoformat(),
        }

    def prune_history(
        self, history: list[dict[str, Any]], limit: int
    ) -> list[dict[str, Any]]:
        """Returns the last N events from the signal history."""
        return history[-limit:]

    def shutdown(self) -> bool:
        """Cleanup signal module."""
        return super().shutdown()
