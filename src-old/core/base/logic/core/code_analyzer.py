#!/usr/bin/env python3
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
# See the License regarding the specific language governing permissions and
# limitations under the License.

r"""LLM_CONTEXT_START

## Source: src-old/core/base/logic/core/code_analyzer.description.md

# code_analyzer

**File**: `src\\core\base\\logic\\core\\code_analyzer.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 96  
**Complexity**: 4 (simple)

## Overview

Core code analysis logic regarding API summarization and structural inspection.
Inspired by Feathr (ai-eng) source code compacting.

## Classes (1)

### `CodeAnalyzerCore`

Core logic regarding extracting compact API representations from source code.

**Methods** (4):
- `__init__(self, workspace_root)`
- `generate_compact_guide(self, path)`
- `_summarize_file(self, file_path)`
- `calculate_metrics_summary(self, source)`

## Dependencies

**Imports** (7):
- `ast`
- `os`
- `pathlib.Path`
- `re`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
## Source: src-old/core/base/logic/core/code_analyzer.improvements.md

# Improvements for code_analyzer

**File**: `src\\core\base\\logic\\core\\code_analyzer.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 96 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `code_analyzer_test.py` with pytest tests

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

"""
Core code analysis logic regarding API summarization and structural inspection.
Inspired by Feathr (ai-eng) source code compacting.
"""
import ast
import os
import re
from pathlib import Path
from typing import Optional, Union


class CodeAnalyzerCore:
    """
    """
