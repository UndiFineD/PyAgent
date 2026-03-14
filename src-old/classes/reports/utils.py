#!/usr/bin/env python3
r"""
LLM_CONTEXT_START

## Source: src-old/classes/reports/utils.description.md

# utils

**File**: `src\classes\reports\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 8 functions, 7 imports  
**Lines**: 121  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for utils.

## Functions (8)

### `_read_text(path)`

Read text file with UTF-8 and replacement errors.

### `_is_pytest_test_file(path)`

Check if file is a pytest test file.

### `_looks_like_pytest_import_problem(path)`

Check if filename has characters that cause pytest import issues.

### `_find_imports(tree)`

Find all top-level imports in an AST.

### `_detect_argparse(source)`

Check if source uses argparse.

### `_placeholder_test_note(path, source)`

Check if it's a placeholder test file.

### `_rel(path)`

Get relative path string for display.

### `_find_issues(tree, source)`

Find potential issues via lightweight static analysis.

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `ast`
- `pathlib.Path`
- `re`
- `src.core.base.version.VERSION`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/reports/utils.improvements.md

# Improvements for utils

**File**: `src\classes\reports\utils.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 121 lines (medium)  
**Complexity**: 8 score (moderate)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `utils_test.py` with pytest tests

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


# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from src.core.base.version import VERSION
import ast
import re
from pathlib import Path
from typing import List, Optional

__version__ = VERSION

# Constants used by helpers

AGENT_DIR = Path(__file__).resolve().parent.parent.parent
REPO_ROOT = AGENT_DIR.parent


def _read_text(path: Path) -> str:
    """
    """
