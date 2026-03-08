# Class Breakdown: stream_manager_mixin

**File**: `src\core\base\mixins\stream_manager_mixin.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StreamState`

**Line**: 42  
**Methods**: 2

Represents the current state of a stream.

[TIP] **Suggested split**: Move to `streamstate.py`

---

### 2. `StreamInfo`

**Line**: 62  
**Methods**: 2

Information about an active stream.

[TIP] **Suggested split**: Move to `streaminfo.py`

---

### 3. `StreamManagerMixin`

**Line**: 87  
**Methods**: 1

Mixin providing Redis-backed stream management capabilities.
Adapted from Adorable's stream-manager.ts patterns for Python/asyncio.

[TIP] **Suggested split**: Move to `streammanagermixin.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
