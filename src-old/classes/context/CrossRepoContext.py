#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/context/CrossRepoContext.description.md

# CrossRepoContext

**File**: `src\classes\context\CrossRepoContext.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 17 imports  
**Lines**: 34  
**Complexity**: 0 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `CrossRepoContext`

Context from cross-repository analysis.

Attributes:
    repo_name: Name of the repository.
    repo_url: URL to the repository.
    related_files: List of related file paths.
    similarity_score: Overall similarity score.
    common_patterns: Patterns shared between repos.

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
## Source: src-old/classes/context/CrossRepoContext.improvements.md

# Improvements for CrossRepoContext

**File**: `src\classes\context\CrossRepoContext.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 34 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `CrossRepoContext_test.py` with pytest tests

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


@dataclass
class CrossRepoContext:
    """Context from cross-repository analysis.

    Attributes:
        repo_name: Name of the repository.
        repo_url: URL to the repository.
        related_files: List of related file paths.
        similarity_score: Overall similarity score.
        common_patterns: Patterns shared between repos.
    """

    repo_name: str
    repo_url: str
    related_files: List[str] = field(default_factory=lambda: [])
    similarity_score: float = 0.0
    common_patterns: List[str] = field(default_factory=lambda: [])
