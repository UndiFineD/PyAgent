#!/usr/bin/env python3
r"""
LLM_CONTEXT_START

## Source: src-old/classes/agent/utils.description.md

# utils

**File**: `src\classes\agent\utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 11 imports  
**Lines**: 168  
**Complexity**: 4 (simple)

## Overview

Utility functions used by the Agent classes.

## Functions (4)

### `load_codeignore(root)`

Load and parse ignore patterns from .codeignore file.

Reads the .codeignore file from the repository root and extracts all
ignore patterns (lines that are not empty or comments).

Caches patterns to avoid re-parsing on subsequent calls. Cache is invalidated
if the file is modified (checked by file mtime).

Args:
    root: Path to the repository root directory.

Returns:
    Set of ignore patterns (strings) from the .codeignore file.
    Returns empty set if file doesn't exist.

Raises:
    None. Logs warnings if file cannot be read but doesn't raise.

Example:
    patterns=load_codeignore(Path('/repo'))
    # patterns might be: {'*.log', '__pycache__/', 'venv/**'}

Note:
    - Lines starting with '#' are treated as comments and ignored
    - Empty lines are skipped
    - File encoding is assumed to be UTF-8
    - Patterns are cached with mtime checking for efficiency

### `setup_logging(verbosity)`

Configure logging based on verbosity level.

Defaults to WARNING to capture only errors and failures as requested.

### `_multiprocessing_worker(agent_instance, file_path)`

Worker function for multiprocessing file processing.

This function must be at module level to be pickleable for multiprocessing.

### `_load_fix_markdown_content()`

Load the markdown fixer module dynamically.

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `collections.abc.Callable`
- `importlib.util`
- `logging`
- `pathlib.Path`
- `src.core.base.version.VERSION`
- `sys`
- `typing.Any`
- `typing.Optional`
- `typing.Set`
- `typing.cast`

---
*Auto-generated documentation*
## Source: src-old/classes/agent/utils.improvements.md

# Improvements for utils

**File**: `src\classes\agent\utils.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 168 lines (medium)  
**Complexity**: 4 score (simple)

## Suggested Improvements

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


r"""Utility functions used by the Agent classes."""
