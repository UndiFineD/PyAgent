#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/RustAgent.description.md

# RustAgent

**File**: `src\classes\coder\RustAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 29  
**Complexity**: 2 (simple)

## Overview

Agent specializing in Rust programming.

## Classes (1)

### `RustAgent`

**Inherits from**: CoderAgent

Agent for Rust code improvement and auditing.

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
## Source: src-old/classes/coder/RustAgent.improvements.md

# Improvements for RustAgent

**File**: `src\classes\coder\RustAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 29 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `RustAgent_test.py` with pytest tests

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

"""Agent specializing in Rust programming."""


from src.classes.base_agent.utilities import create_main_function

from .CoderAgent import CoderAgent


class RustAgent(CoderAgent):
    """Agent for Rust code improvement and auditing."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "rust"
        self._system_prompt = (
            "You are a Rust Expert. "
            "Focus on memory safety, ownership patterns, idiomatic usage of Result/Option, "
            "zero-cost abstractions, and effective use of the borrow checker. "
            "Suggest crates from crates.io where appropriate for common tasks."
        )

    def _get_default_content(self) -> str:
        return 'fn main() {\n    println!("Hello, Rust!");\n}\n'


if __name__ == "__main__":
    main = create_main_function(RustAgent, "Rust Agent", "Path to Rust file (.rs)")
    main()
