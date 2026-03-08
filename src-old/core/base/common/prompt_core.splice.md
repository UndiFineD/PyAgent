# Class Breakdown: prompt_core

**File**: `src\core\base\common\prompt_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PromptCore`

**Line**: 33  
**Inherits**: BaseCore  
**Methods**: 4

Authoritative engine for prompt templates and A/B testing.

[TIP] **Suggested split**: Move to `promptcore.py`

---

### 2. `PromptVersion`

**Line**: 65  
**Methods**: 3

Represents a specific version of a prompt for A/B testing and tracking.

[TIP] **Suggested split**: Move to `promptversion.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
