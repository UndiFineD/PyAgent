#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");

"""
LLM_CONTEXT_START

## Source: src-old/classes/coder/SqlAgent.description.md

# SqlAgent

**File**: `src\classes\coder\SqlAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 30  
**Complexity**: 2 (simple)

## Overview

Agent specializing in SQL and database scripts.

## Classes (1)

### `SqlAgent`

**Inherits from**: CoderAgent

Agent for auditing and improving SQL scripts.

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
## Source: src-old/classes/coder/SqlAgent.improvements.md

# Improvements for SqlAgent

**File**: `src\classes\coder\SqlAgent.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 30 lines (small)  
**Complexity**: 2 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SqlAgent_test.py` with pytest tests

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

"""Agent specializing in SQL and database scripts."""

from .CoderAgent import CoderAgent
from src.classes.base_agent.utilities import create_main_function
import logging


class SqlAgent(CoderAgent):
    """Agent for auditing and improving SQL scripts."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "sql"
        # SQL-specific instructions
        self._system_prompt = (
            "You are a SQL Expert and Database Administrator. "
            "Focus on query performance, indexing, security (injection prevention), "
            "and adherence to standard SQL patterns or specific dialects (PostgreSQL, MySQL, T-SQL)."
        )

    def _get_default_content(self) -> str:
        return "-- SQL Script\nSELECT 1;\n"


if __name__ == "__main__":
    main = create_main_function(SqlAgent, "SQL Agent", "Path to SQL file")
    main()
