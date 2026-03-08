#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/classes/base_agent/managers.description.md

# managers

**File**: `src\classes\base_agent\managers.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 23 imports  
**Lines**: 26  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for managers.

## Dependencies

**Imports** (23):
- `__future__.annotations`
- `managers.AuthManagers.AuthManager`
- `managers.AuthManagers.AuthenticationManager`
- `managers.BatchManagers.BatchRequest`
- `managers.BatchManagers.RequestBatcher`
- `managers.ConversationManagers.ConversationHistory`
- `managers.OrchestrationManagers.ABTest`
- `managers.OrchestrationManagers.AgentComposer`
- `managers.OrchestrationManagers.ModelSelector`
- `managers.OrchestrationManagers.QualityScorer`
- `managers.ProcessorManagers.MultimodalProcessor`
- `managers.ProcessorManagers.ResponsePostProcessor`
- `managers.ProcessorManagers.SerializationManager`
- `managers.PromptManagers.PromptTemplateManager`
- `managers.PromptManagers.PromptVersion`
- ... and 8 more

---
*Auto-generated documentation*
## Source: src-old/classes/base_agent/managers.improvements.md

# Improvements for managers

**File**: `src\classes\base_agent\managers.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 26 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Documentation
- [!] **Missing module docstring** - Add comprehensive module-level documentation

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `managers_test.py` with pytest tests

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

# Copyright (c) 2025 PyAgent contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Manager and utility classes for BaseAgent (Facade)."""

from .managers.PromptManagers import (
    PromptTemplateManager,
    PromptVersion,
    PromptVersionManager,
)
from .managers.ConversationManagers import ConversationHistory
from .managers.AuthManagers import AuthenticationManager, AuthManager
from .managers.BatchManagers import BatchRequest, RequestBatcher
from .managers.ProcessorManagers import (
    ResponsePostProcessor,
    MultimodalProcessor,
    SerializationManager,
)
from .managers.OrchestrationManagers import (
    AgentComposer,
    ModelSelector,
    QualityScorer,
    ABTest,
)
from .managers.SystemManagers import (
    FilePriorityManager,
    ResponseCache,
    StatePersistence,
    EventManager,
    PluginManager,
    HealthChecker,
    ProfileManager,
)
