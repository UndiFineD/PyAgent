# Class Breakdown: usage_message

**File**: `src\observability\telemetry\usage_message.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `UsageContext`

**Line**: 61  
**Inherits**: str, Enum  
**Methods**: 0

Context in which PyAgent is being used.

[TIP] **Suggested split**: Move to `usagecontext.py`

---

### 2. `UsageMessage`

**Line**: 275  
**Methods**: 5

Structured usage telemetry message.

Collects platform information and reports it asynchronously.

[TIP] **Suggested split**: Move to `usagemessage.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
