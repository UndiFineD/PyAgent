#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/coder/GoAgent.description.md

# GoAgent

**File**: `src\classes\coder\GoAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 29  
**Complexity**: 2 (simple)

## Overview

Agent specializing in Go (Golang) programming.

## Classes (1)

### `GoAgent`

**Inherits from**: CoderAgent

Agent for Go code improvement and auditing.

**Methods** (2):
- `__init__(self, file_path)`
- `_get_default_content(self)`

## Dependencies

**Imports** (3):
- `CoderAgent.CoderAgent`
- `logging`
- `src.classes.base_agent.utilities.create_main_function`

---
*Auto-generated documentation*
## Source: src-old/classes/coder/GoAgent.improvements.md

# Improvements for GoAgent

**File**: `src\classes\coder\GoAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 29 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `GoAgent_test.py` with pytest tests

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

"""Agent specializing in Go (Golang) programming."""

from .CoderAgent import CoderAgent
from src.classes.base_agent.utilities import create_main_function
import logging


class GoAgent(CoderAgent):
    """Agent for Go code improvement and auditing."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "go"
        self._system_prompt = (
            "You are a Go Expert. "
            "Focus on concurrency patterns (goroutines, channels), "
            "effective error handling, interface design, and idiomatic Go project structure. "
            "Follow 'Effective Go' principles."
        )

    def _get_default_content(self) -> str:
        return 'package main\n\nimport "fmt"\n\nfunc main() {\n    fmt.Println("Hello, Go!")\n}\n'


if __name__ == "__main__":
    main = create_main_function(GoAgent, "Go Agent", "Path to Go file (.go)")
    main()
