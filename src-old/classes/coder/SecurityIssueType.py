#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/coder/SecurityIssueType.description.md

# SecurityIssueType

**File**: `src\classes\coder\SecurityIssueType.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 20 imports  
**Lines**: 31  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_coder.py

## Classes (1)

### `SecurityIssueType`

**Inherits from**: Enum

Types of security vulnerabilities.

## Dependencies

**Imports** (20):
- `__future__.annotations`
- `ast`
- `base_agent.BaseAgent`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `hashlib`
- `logging`
- `math`
- `pathlib.Path`
- `re`
- `shutil`
- `subprocess`
- `tempfile`
- `typing.Any`
- ... and 5 more

---
*Auto-generated documentation*
## Source: src-old/classes/coder/SecurityIssueType.improvements.md

# Improvements for SecurityIssueType

**File**: `src\classes\coder\SecurityIssueType.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 31 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SecurityIssueType_test.py` with pytest tests

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

"""Auto-extracted class from agent_coder.py"""


from base_agent import BaseAgent
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import ast
import hashlib
import logging
import math
import re
import shutil
import subprocess
import tempfile


class SecurityIssueType(Enum):
    """Types of security vulnerabilities."""

    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    HARDCODED_SECRET = "hardcoded_secret"
    INSECURE_DESERIALIZATION = "insecure_deserialization"
    PATH_TRAVERSAL = "path_traversal"
    COMMAND_INJECTION = "command_injection"
    INSECURE_RANDOM = "insecure_random"
    INJECTION_ATTEMPT = "injection_attempt"
    OTHER = "other"
