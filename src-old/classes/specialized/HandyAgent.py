#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/specialized/HandyAgent.description.md

# HandyAgent

**File**: `src\classes\specialized\HandyAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 48  
**Complexity**: 1 (simple)

## Overview

Agent specializing in terminal-native interactions and context-aware shell execution.
Inspired by the Handy pattern (Rust terminal agent) and GitHub Copilot CLI.

## Classes (1)

### `HandyAgent`

**Inherits from**: BaseAgent, HandyFileSystemMixin, HandyTerminalMixin, HandyCoreMixin

Provides a terminal-native interface for the agent to interact with the OS.

**Methods** (1):
- `__init__(self, file_path)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `mixins.HandyCoreMixin.HandyCoreMixin`
- `mixins.HandyFileSystemMixin.HandyFileSystemMixin`
- `mixins.HandyTerminalMixin.HandyTerminalMixin`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.Version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`

---
*Auto-generated documentation*
## Source: src-old/classes/specialized/HandyAgent.improvements.md

# Improvements for HandyAgent

**File**: `src\classes\specialized\HandyAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 48 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `HandyAgent_test.py` with pytest tests

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


"""Agent specializing in terminal-native interactions and context-aware shell execution.
Inspired by the Handy pattern (Rust terminal agent) and GitHub Copilot CLI.
"""

from src.core.base.Version import VERSION
from pathlib import Path
from .mixins.HandyFileSystemMixin import HandyFileSystemMixin
from .mixins.HandyTerminalMixin import HandyTerminalMixin
from .mixins.HandyCoreMixin import HandyCoreMixin
from src.core.base.BaseAgent import BaseAgent
from src.infrastructure.backend.LocalContextRecorder import LocalContextRecorder

__version__ = VERSION


class HandyAgent(BaseAgent, HandyFileSystemMixin, HandyTerminalMixin, HandyCoreMixin):
    """Provides a terminal-native interface for the agent to interact with the OS."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._system_prompt = (
            "You are the Handy Agent. "
            "Your role is to act as an 'Agentic Bash' – a terminal shell that understands codebase context. "
            "You provide tools for intelligent file search, system diagnosis, and command execution."
        )

        # Phase 108: Intelligence Harvesting
        work_root = getattr(self, "_workspace_root", None)
        self.recorder = LocalContextRecorder(Path(work_root)) if work_root else None

    # Methods delegated to mixins
