#!/usr/bin/env python3
r"""LLM_CONTEXT_START

## Source: src-old/classes/reports/ReportGenerator.description.md

# ReportGenerator

**File**: `src\\classes\reports\\ReportGenerator.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 20 imports  
**Lines**: 446  
**Complexity**: 25 (complex)

## Overview

Report generation logic for agent source files.

## Classes (1)

### `ReportGenerator`

Generates quality reports (description, errors, improvements) for agent files.

**Methods** (25):
- `__init__(self, agent_dir, output_dir, recorder)`
- `_record(self, action, result)`
- `process_all_files(self)`
- `export_jsonl_report(self, items, filename)`
- `generate_full_report(self)`
- `render_3x3_grid(self)`
- `process_file(self, py_path)`
- `iter_agent_py_files(self)`
- `render_description(self, py_path, source, tree)`
- `render_errors(self, py_path, source, compile_result)`
- ... and 15 more methods

## Dependencies

**Imports** (20):
- `CompileResult.CompileResult`
- `__future__.annotations`
- `ast`
- `collections.abc.Iterable`
- `core.DeduplicationCore.DeduplicationCore`
- `hashlib`
- `logging`
- `os`
- `pathlib.Path`
- `re`
- `src.core.base.version.VERSION`
- `subprocess`
- `sys`
- `time`
- `typing.Any`
- ... and 5 more

---
*Auto-generated documentation*
## Source: src-old/classes/reports/ReportGenerator.improvements.md

# Improvements for ReportGenerator

**File**: `src\\classes\reports\\ReportGenerator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 446 lines (medium)  
**Complexity**: 25 score (complex)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ReportGenerator_test.py` with pytest tests

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


r"""Report generation logic for agent source files."""
