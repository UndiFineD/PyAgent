#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/context/MergeConflict.description.md

# MergeConflict

**File**: `src\classes\context\MergeConflict.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 18 imports  
**Lines**: 34  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `MergeConflict`

Merge conflict information.

Attributes:
    section: Section with conflict.
    ours: Our version of content.
    theirs: Their version of content.
    resolution: Applied resolution.

## Dependencies

**Imports** (18):
- `ConflictResolution.ConflictResolution`
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `hashlib`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `src.classes.base_agent.BaseAgent`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 3 more

---
*Auto-generated documentation*
## Source: src-old/classes/context/MergeConflict.improvements.md

# Improvements for MergeConflict

**File**: `src\classes\context\MergeConflict.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 34 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `MergeConflict_test.py` with pytest tests

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

"""Auto-extracted class from agent_context.py"""


from .ConflictResolution import ConflictResolution

from src.classes.base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import re
import zlib

@dataclass
class MergeConflict:
    """Merge conflict information.

    Attributes:
        section: Section with conflict.
        ours: Our version of content.
        theirs: Their version of content.
        resolution: Applied resolution.
    """
    section: str
    ours: str
    theirs: str
    resolution: Optional[ConflictResolution] = None
