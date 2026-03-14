#!/usr/bin/env python3
from __future__ import annotations
r"""LLM_CONTEXT_START

## Source: src-old/classes/context/ContextRecommender.description.md

# ContextRecommender

**File**: `src\classes\context\ContextRecommender.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 90  
**Complexity**: 4 (simple)

## Overview

Auto-extracted class from agent_context.py

## Classes (1)

### `ContextRecommender`

Recommends context improvements based on similar files.

Analyzes similar files to suggest context improvements.

Example:
    >>> recommender=ContextRecommender()
    >>> recommendations=recommender.recommend("auth.py", similar_contexts)

**Methods** (4):
- `__init__(self)`
- `add_reference(self, file_name, content)`
- `find_similar(self, query)`
- `recommend(self, content_or_target_file, similar_contexts)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `re`
- `src.core.base.version.VERSION`
- `src.logic.agents.cognitive.context.models.ContextRecommendation.ContextRecommendation`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`

---
*Auto-generated documentation*
## Source: src-old/classes/context/ContextRecommender.improvements.md

# Improvements for ContextRecommender

**File**: `src\classes\context\ContextRecommender.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 90 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `ContextRecommender_test.py` with pytest tests

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
