#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/context/ConflictResolution.description.md

# ConflictResolution

**File**: `src\classes\context\ConflictResolution.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 24  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ConflictResolution`

**Inherits from**: Enum

Strategies for merge conflict resolution.

## Dependencies

**Imports** (17):
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
- `typing.Optional`
- ... and 2 more

---
*Auto-generated documentation*
## Source: src-old/classes/context/ConflictResolution.improvements.md

# Improvements for ConflictResolution

**File**: `src\classes\context\ConflictResolution.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 24 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ConflictResolution_test.py` with pytest tests

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

from __future__ import annotations

"""Auto-extracted class from agent_context.py"""


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


class ConflictResolution(Enum):
    """Strategies for merge conflict resolution."""

    OURS = "ours"
    THEIRS = "theirs"
    MANUAL = "manual"
    AUTO = "auto"
