"""
LLM_CONTEXT_START

## Source: src-old/logic/agents/cognitive/context/engines/GlobalContextCore.description.md

# GlobalContextCore

**File**: `src\logic\agents\cognitive\context\engines\GlobalContextCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 5 imports  
**Lines**: 29  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for GlobalContextCore.

## Classes (1)

### `GlobalContextCore`

**Inherits from**: CorePartitionMixin, CoreResolutionMixin, CoreSummaryMixin

Pure logic for GlobalContext.
Handles data merging, pruning, and summary formatting.
No I/O or direct disk access.

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `core_mixins.CorePartitionMixin.CorePartitionMixin`
- `core_mixins.CoreResolutionMixin.CoreResolutionMixin`
- `core_mixins.CoreSummaryMixin.CoreSummaryMixin`
- `src.core.base.Version.VERSION`

---
*Auto-generated documentation*
## Source: src-old/logic/agents/cognitive/context/engines/GlobalContextCore.improvements.md

# Improvements for GlobalContextCore

**File**: `src\logic\agents\cognitive\context\engines\GlobalContextCore.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 29 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `GlobalContextCore_test.py` with pytest tests

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


from src.core.base.Version import VERSION
from .core_mixins.CorePartitionMixin import CorePartitionMixin
from .core_mixins.CoreResolutionMixin import CoreResolutionMixin
from .core_mixins.CoreSummaryMixin import CoreSummaryMixin

__version__ = VERSION


class GlobalContextCore(CorePartitionMixin, CoreResolutionMixin, CoreSummaryMixin):
    """
    Pure logic for GlobalContext.
    Handles data merging, pruning, and summary formatting.
    No I/O or direct disk access.
    """
