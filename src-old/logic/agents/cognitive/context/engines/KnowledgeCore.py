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
# See the License for the specific language governing permissions and
# limitations under the License.


r"""LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/KnowledgeCore.description.md

# KnowledgeCore

**File**: `src\\logic\agents\\cognitive\\context\\engines\\KnowledgeCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 38  
**Complexity**: 1 (simple)

## Overview

KnowledgeCore logic for specialized workspace analysis.
Contains pure regex and indexing logic for fast symbol discovery.
This file is optimized for Rust migration (Phase 114).

## Classes (1)

### `KnowledgeCore`

**Inherits from**: KnowledgeSymbolMixin, KnowledgeSearchMixin, KnowledgeProcessMixin

KnowledgeCore performs pure computational analysis of workspace symbols.
No I/O or database operations are allowed here to ensure Rust portability.

**Methods** (1):
- `__init__(self, fleet)`

## Dependencies

**Imports** (5):
- `knowledge_mixins.KnowledgeProcessMixin.KnowledgeProcessMixin`
- `knowledge_mixins.KnowledgeSearchMixin.KnowledgeSearchMixin`
- `knowledge_mixins.KnowledgeSymbolMixin.KnowledgeSymbolMixin`
- `src.core.base.Version.VERSION`
- `typing.Any`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/KnowledgeCore.improvements.md

# Improvements for KnowledgeCore

**File**: `src\\logic\agents\\cognitive\\context\\engines\\KnowledgeCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 38 lines (small)  
**Complexity**: 1 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `KnowledgeCore_test.py` with pytest tests

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
KnowledgeCore logic for specialized workspace analysis.
Contains pure regex and indexing logic for fast symbol discovery.
This file is optimized for Rust migration (Phase 114).
"""
from typing import Any

from src.core.base.Version import VERSION

from .knowledge_mixins.KnowledgeProcessMixin import KnowledgeProcessMixin
from .knowledge_mixins.KnowledgeSearchMixin import KnowledgeSearchMixin
from .knowledge_mixins.KnowledgeSymbolMixin import KnowledgeSymbolMixin

__version__ = VERSION


class KnowledgeCore(KnowledgeSymbolMixin, KnowledgeSearchMixin, KnowledgeProcessMixin):
    """
    """
