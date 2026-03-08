# Class Breakdown: android_core

**File**: `src\logic\agents\multimodal\core\android_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ADBResult`

**Line**: 30  
**Inherits**: TypedDict  
**Methods**: 0

Result of an ADB command execution.

[TIP] **Suggested split**: Move to `adbresult.py`

---

### 2. `AndroidCore`

**Line**: 39  
**Methods**: 3

Core logic for ADB command formatting and parsing.

[TIP] **Suggested split**: Move to `androidcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
