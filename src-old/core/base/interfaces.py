#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/core/base/interfaces.description.md

# interfaces

**File**: `src\\core\base\\interfaces.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 9 imports  
**Lines**: 70  
**Complexity**: 12 (moderate)

## Overview

Python module containing implementation for interfaces.

## Classes (4)

### `AgentInterface`

**Inherits from**: Protocol

Core interface for all AI-powered agents. 
Defining this as a Protocol facilitates future Rust implementation (PyO3).

**Methods** (6):
- `read_previous_content(self)`
- `improve_content(self, prompt)`
- `update_file(self)`
- `get_diff(self)`
- `calculate_metrics(self, content)`
- `scan_for_secrets(self, content)`

### `OrchestratorInterface`

**Inherits from**: Protocol

Interface for fleet orchestrators.

**Methods** (2):
- `execute_task(self, task)`
- `get_status(self)`

### `CoreInterface`

**Inherits from**: Protocol

Pure logic interface. High-performance, no-IO, candidate for Rust parity.

**Methods** (3):
- `process_data(self, data)`
- `validate(self, content)`
- `get_metadata(self)`

### `ContextRecorderInterface`

**Inherits from**: Protocol

Interface for cognitive recording and context harvesting.

**Methods** (1):
- `record_interaction(self, provider, model, prompt, result, meta)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Protocol`
- `typing.runtime_checkable`

---
*Auto-generated documentation*
## Source: src-old/core/base/interfaces.improvements.md

# Improvements for interfaces

**File**: `src\\core\base\\interfaces.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 70 lines (small)  
**Complexity**: 12 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `interfaces_test.py` with pytest tests

### Code Organization
- [TIP] **4 classes in one file** - Consider splitting into separate modules

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


from pathlib import Path
from typing import Any, Protocol, runtime_checkable

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


@runtime_checkable
class AgentInterface(Protocol):
    """
    """
