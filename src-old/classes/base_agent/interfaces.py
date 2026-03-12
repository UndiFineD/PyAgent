#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/base_agent/interfaces.description.md

# interfaces

**File**: `src\classes\base_agent\interfaces.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 8 imports  
**Lines**: 37  
**Complexity**: 11 (moderate)

## Overview

Python module containing implementation for interfaces.

## Classes (3)

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

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `pathlib.Path`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Protocol`
- `typing.runtime_checkable`

---
*Auto-generated documentation*
## Source: src-old/classes/base_agent/interfaces.improvements.md

# Improvements for interfaces

**File**: `src\classes\base_agent\interfaces.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 37 lines (small)  
**Complexity**: 11 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `interfaces_test.py` with pytest tests

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

from typing import Protocol, runtime_checkable, Dict, Any, List, Optional
from pathlib import Path


@runtime_checkable
class AgentInterface(Protocol):
    """
    Core interface for all AI-powered agents.
    Defining this as a Protocol facilitates future Rust implementation (PyO3).
    """

    file_path: Path
    previous_content: str
    current_content: str

    def read_previous_content(self) -> str: ...
    def improve_content(self, prompt: str) -> str: ...
    def update_file(self) -> bool: ...
    def get_diff(self) -> str: ...

    # Advanced features that might be offloaded to Rust later
    def calculate_metrics(self, content: Optional[str] = None) -> Any: ...
    def scan_for_secrets(self, content: str) -> List[str]: ...


@runtime_checkable
class OrchestratorInterface(Protocol):
    """Interface for fleet orchestrators."""

    def execute_task(self, task: str) -> str: ...
    def get_status(self) -> Dict[str, Any]: ...


@runtime_checkable
class CoreInterface(Protocol):
    """Pure logic interface. High-performance, no-IO, candidate for Rust parity."""

    def process_data(self, data: Any) -> Any: ...
    def validate(self, content: str) -> bool: ...
    def get_metadata(self) -> Dict[str, Any]: ...
