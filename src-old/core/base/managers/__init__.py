#!/usr/bin/env python3
"""LLM_CONTEXT_START

## Source: src-old/core/base/managers/__init__.description.md

# __init__

**File**: `src\\core\base\\managers\\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 27 imports  
**Lines**: 64  
**Complexity**: 0 (simple)

## Overview

Internal managers for prompt, conversation, auth, and batch processing.

## Dependencies

**Imports** (27):
- `AuthManagers.AuthManager`
- `AuthManagers.AuthenticationManager`
- `BatchManagers.BatchRequest`
- `BatchManagers.RequestBatcher`
- `ConversationManagers.ConversationHistory`
- `OrchestrationManagers.ABTest`
- `OrchestrationManagers.AgentComposer`
- `OrchestrationManagers.ModelSelector`
- `OrchestrationManagers.QualityScorer`
- `PluginManager.PluginManager`
- `PluginManager.PluginMetadata`
- `ProcessorManagers.MultimodalProcessor`
- `ProcessorManagers.ResponsePostProcessor`
- `ProcessorManagers.SerializationManager`
- `PromptManagers.PromptTemplateManager`
- ... and 12 more

---
*Auto-generated documentation*
## Source: src-old/core/base/managers/__init__.improvements.md

# Improvements for __init__

**File**: `src\\core\base\\managers\\__init__.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 64 lines (small)  
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
7

from src.core.base.Version import VERSION as VERSION

try:
    from .AuthManagers import AuthenticationManager, AuthManager
    from .BatchManagers import BatchRequest, RequestBatcher
    from .ConversationManagers import ConversationHistory
    from .OrchestrationManagers import (
        ABTest,
        AgentComposer,
        ModelSelector,
        QualityScorer,
    )
    from .PluginManager import PluginManager, PluginMetadata
    from .ProcessorManagers import (
        MultimodalProcessor,
        ResponsePostProcessor,
        SerializationManager,
    )
    from .PromptManagers import (
        PromptTemplateManager,
        PromptVersion,
        PromptVersionManager,
    )
    from .ResourceQuotaManager import QuotaConfig, ResourceQuotaManager
    from .SystemManagers import (
        EventManager,
        FilePriorityManager,
        HealthChecker,
        ProfileManager,
        ResponseCache,
        StatePersistence,
    )
except Exception:
    # Best-effort: allow package import even if some manager submodules are
    # missing or named differently (legacy/pluralization differences).
    pass


"""
Internal managers for prompt, conversation, auth, and batch processing.
"""

__version__ = VERSION
