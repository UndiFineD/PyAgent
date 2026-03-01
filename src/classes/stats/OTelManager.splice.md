# Class Breakdown: OTelManager

**File**: `src\classes\stats\OTelManager.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `Span`

**Line**: 14  
**Methods**: 0

[TIP] **Suggested split**: Move to `span.py`

---

### 2. `OTelManager`

**Line**: 24  
**Methods**: 5

Manages OTel-compatible spans and traces for cross-fleet observability.

[TIP] **Suggested split**: Move to `otelmanager.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
