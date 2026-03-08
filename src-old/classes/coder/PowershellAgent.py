#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/coder/PowershellAgent.description.md

# PowershellAgent

**File**: `src\classes\coder\PowershellAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 27  
**Complexity**: 2 (simple)

## Overview

Agent specializing in PowerShell scripting.

## Classes (1)

### `PowershellAgent`

**Inherits from**: CoderAgent

Agent for PowerShell scripts.

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
## Source: src-old/classes/coder/PowershellAgent.improvements.md

# Improvements for PowershellAgent

**File**: `src\classes\coder\PowershellAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 27 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `PowershellAgent_test.py` with pytest tests

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

"""Agent specializing in PowerShell scripting."""

from .CoderAgent import CoderAgent
from src.classes.base_agent.utilities import create_main_function
import logging


class PowershellAgent(CoderAgent):
    """Agent for PowerShell scripts."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "powershell"
        self._system_prompt = (
            "You are an Expert PowerShell Scripter. "
            "Focus on idiomatic PowerShell, proper naming conventions (Verb-Noun), "
            "error handling (Try/Catch), and pipeline efficiency."
        )

    def _get_default_content(self) -> str:
        return "# PowerShell Script\nWrite-Host 'Hello World'\n"


if __name__ == "__main__":
    main = create_main_function(
        PowershellAgent, "PowerShell Agent", "Path to .ps1 file"
    )
    main()
