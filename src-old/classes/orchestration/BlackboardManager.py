#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/orchestration/BlackboardManager.description.md

# BlackboardManager

**File**: `src\classes\orchestration\BlackboardManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 30  
**Complexity**: 4 (simple)

## Overview

Shared central memory for opportunistic agent collaboration (Blackboard Pattern).

## Classes (1)

### `BlackboardManager`

Central repository for agents to post findings and look for data.
Shell for BlackboardCore.

**Methods** (4):
- `__init__(self)`
- `post(self, key, value, agent_name)`
- `get(self, key)`
- `list_keys(self)`

## Dependencies

**Imports** (5):
- `BlackboardCore.BlackboardCore`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
## Source: src-old/classes/orchestration/BlackboardManager.improvements.md

# Improvements for BlackboardManager

**File**: `src\classes\orchestration\BlackboardManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 30 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `BlackboardManager_test.py` with pytest tests

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

"""Shared central memory for opportunistic agent collaboration (Blackboard Pattern)."""

import logging
from typing import Dict, Any, List

from .BlackboardCore import BlackboardCore

class BlackboardManager:
    """
    Central repository for agents to post findings and look for data.
    Shell for BlackboardCore.
    """
    
    def __init__(self) -> None:
        self.core = BlackboardCore()

    def post(self, key: str, value: Any, agent_name: str) -> None:
        """Post data to the blackboard."""
        logging.info(f"Blackboard: Agent {agent_name} posted to {key}")
        self.core.process_post(key, value, agent_name)

    def get(self, key: str) -> Any:
        """Retrieve data from the blackboard."""
        return self.core.get_value(key)

    def list_keys(self) -> List[str]:
        """List all available keys on the blackboard."""
        return self.core.get_all_keys()
