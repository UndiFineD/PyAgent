#!/usr/bin/env python3

r"""LLM_CONTEXT_START

## Source: src-old/classes/coder/BashAgent.description.md

# BashAgent

**File**: `src\classes\coder\BashAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 27  
**Complexity**: 2 (simple)

## Overview

Agent specializing in Bash and shell scripting.

## Classes (1)

### `BashAgent`

**Inherits from**: CoderAgent

Agent for shell scripts.

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
## Source: src-old/classes/coder/BashAgent.improvements.md

# Improvements for BashAgent

**File**: `src\classes\coder\BashAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 27 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `BashAgent_test.py` with pytest tests

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

"""Agent specializing in Bash and shell scripting."""


from src.classes.base_agent.utilities import create_main_function

from .CoderAgent import CoderAgent


class BashAgent(CoderAgent):
    """Agent for shell scripts."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "bash"
        self._system_prompt = (
            "You are an Expert Shell Scripter. "
            "Focus on POSIX compliance, shell-check standards, error handling (set -e), "
            "and secure handling of variables."
        )

    def _get_default_content(self) -> str:
        return "#!/bin/bash\nset -euo pipefail\necho 'Hello World'\n"


if __name__ == "__main__":
    main = create_main_function(BashAgent, "Bash Agent", "Path to shell script")
    main()
