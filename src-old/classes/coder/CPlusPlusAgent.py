#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/coder/CPlusPlusAgent.description.md

# CPlusPlusAgent

**File**: `src\classes\coder\CPlusPlusAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 29  
**Complexity**: 2 (simple)

## Overview

Agent specializing in C++ programming.

## Classes (1)

### `CPlusPlusAgent`

**Inherits from**: CoderAgent

Agent for C++ code improvement and auditing.

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
## Source: src-old/classes/coder/CPlusPlusAgent.improvements.md

# Improvements for CPlusPlusAgent

**File**: `src\classes\coder\CPlusPlusAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 29 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CPlusPlusAgent_test.py` with pytest tests

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

"""Agent specializing in C++ programming."""

from .CoderAgent import CoderAgent
from src.classes.base_agent.utilities import create_main_function
import logging


class CPlusPlusAgent(CoderAgent):
    """Agent for C++ code improvement and auditing."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "cpp"
        self._system_prompt = (
            "You are a C++ Expert. "
            "Focus on modern C++ (C++11/14/17/20/23) features, "
            "RAII, smart pointers, template metaprogramming, and performance optimization. "
            "Ensure low-latency and memory-efficient patterns are used."
        )

    def _get_default_content(self) -> str:
        return "#include <iostream>\n\nint main() {\n    std::cout << 'Hello, C++!' << std::endl;\n    return 0;\n}\n"


if __name__ == "__main__":
    main = create_main_function(
        CPlusPlusAgent, "C++ Agent", "Path to C++ file (.cpp, .hpp, .cc)"
    )
    main()
