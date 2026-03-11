#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

"""LLM_CONTEXT_START

## Source: src-old/classes/base_agent/managers/__init__.description.md

# __init__

**File**: `src\\classes\base_agent\\managers\\__init__.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 22 imports  
**Lines**: 19  
**Complexity**: 0 (simple)

## Overview

Internal managers for prompt, conversation, auth, and batch processing.

## Dependencies

**Imports** (22):
- `AuthManagers.AuthManager`
- `AuthManagers.AuthenticationManager`
- `BatchManagers.BatchRequest`
- `BatchManagers.RequestBatcher`
- `ConversationManagers.ConversationHistory`
- `OrchestrationManagers.ABTest`
- `OrchestrationManagers.AgentComposer`
- `OrchestrationManagers.ModelSelector`
- `OrchestrationManagers.QualityScorer`
- `ProcessorManagers.MultimodalProcessor`
- `ProcessorManagers.ResponsePostProcessor`
- `ProcessorManagers.SerializationManager`
- `PromptManagers.PromptTemplateManager`
- `PromptManagers.PromptVersion`
- `PromptManagers.PromptVersionManager`
- ... and 7 more

---
*Auto-generated documentation*
## Source: src-old/classes/base_agent/managers/__init__.improvements.md

# Improvements for __init__

**File**: `src\\classes\base_agent\\managers\\__init__.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 19 lines (small)  
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
Internal managers for prompt, conversation, auth, and batch processing.
"""

from .AuthManagers import AuthenticationManager, AuthManager
from .BatchManagers import BatchRequest, RequestBatcher
from .ConversationManagers import ConversationHistory
from .OrchestrationManagers import ABTest, AgentComposer, ModelSelector, QualityScorer
from .ProcessorManagers import (
    MultimodalProcessor,
    ResponsePostProcessor,
    SerializationManager,
)
from .PromptManagers import PromptTemplateManager, PromptVersion, PromptVersionManager
from .SystemManagers import (
    EventManager,
    FilePriorityManager,
    HealthChecker,
    PluginManager,
    ProfileManager,
    ResponseCache,
    StatePersistence,
)
