#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/ContextExporter.description.md

# ContextExporter

**File**: `src\classes\context\ContextExporter.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 89  
**Complexity**: 6 (moderate)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextExporter`

Exports context to documentation systems.

Provides functionality to export context to various formats.

Example:
    >>> exporter=ContextExporter()
    >>> exported=exporter.export(content, ExportFormat.HTML)

**Methods** (6):
- `__init__(self, default_format)`
- `set_format(self, format)`
- `get_supported_formats(self)`
- `export(self, content, format)`
- `_to_html(self, content)`
- `_to_rst(self, content)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `datetime.datetime`
- `re`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.models.ExportFormat.ExportFormat`
- `src.logic.agents.cognitive.context.models.ExportedContext.ExportedContext`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/classes/context/ContextExporter.improvements.md

# Improvements for ContextExporter

**File**: `src\classes\context\ContextExporter.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 89 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextExporter_test.py` with pytest tests

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


r"""Auto-extracted class from agent_context.py"""
