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

"""
LLM_CONTEXT_START

## Source: src-old/core/base/environment/__init__.description.md

# __init__

**File**: `src\core\base\environment\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 2 imports  
**Lines**: 22  
**Complexity**: 0 (simple)

## Overview

Environment management module for PyAgent.
Provides isolated execution environments for agents.

## Dependencies

**Imports** (2):
- `environment_manager.EnvironmentManager`
- `environment_manager.get_environment_manager`

---
*Auto-generated documentation*
## Source: src-old/core/base/environment/__init__.improvements.md

# Improvements for __init__

**File**: `src\core\base\environment\__init__.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 22 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `__init___test.py` with pytest tests

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

"""
Environment management module for PyAgent.
Provides isolated execution environments for agents.
"""

from .environment_manager import EnvironmentManager, get_environment_manager

__all__ = ["EnvironmentManager", "get_environment_manager"]