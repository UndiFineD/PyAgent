# Class Breakdown: renderers

**File**: `src\infrastructure\prompt_renderer\renderers.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CompletionRenderer`

**Line**: 25  
**Inherits**: PromptRenderer  
**Methods**: 1

Renderer for completion-style prompts.

[TIP] **Suggested split**: Move to `completionrenderer.py`

---

### 2. `ChatRenderer`

**Line**: 81  
**Inherits**: PromptRenderer  
**Methods**: 4

Renderer for chat-style prompts.

[TIP] **Suggested split**: Move to `chatrenderer.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
