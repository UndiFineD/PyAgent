#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/agent/AgentCommandHandler.description.md

# AgentCommandHandler

**File**: `src\\classes\agent\\AgentCommandHandler.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 15 imports  
**Lines**: 171  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for AgentCommandHandler.

## Classes (1)

### `AgentCommandHandler`

Handles command execution for the Agent, including sub-agent orchestration.

**Methods** (6):
- `__init__(self, repo_root, models_config, recorder)`
- `_record(self, action, result, meta)`
- `run_command(self, cmd, timeout, max_retries)`
- `_prepare_command_environment(self, cmd)`
- `_get_agent_env_vars(self, agent_name)`
- `with_agent_env(self, agent_name)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `collections.abc.Iterator`
- `contextlib`
- `logging`
- `os`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `subprocess`
- `sys`
- `threading`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/AgentCommandHandler.improvements.md

# Improvements for AgentCommandHandler

**File**: `src\\classes\agent\\AgentCommandHandler.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 171 lines (medium)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `AgentCommandHandler_test.py` with pytest tests

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
from __future__ import annotations


import contextlib
import logging
import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import Any

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
from src.core.base.version import VERSION

__version__ = VERSION


class AgentCommandHandler:
    """
    """
