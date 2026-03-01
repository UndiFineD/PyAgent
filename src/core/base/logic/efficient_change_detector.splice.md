# Class Breakdown: efficient_change_detector

**File**: `src\core\base\logic\efficient_change_detector.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ChangeRecord`

**Line**: 33  
**Methods**: 0

Record of a file system change

[TIP] **Suggested split**: Move to `changerecord.py`

---

### 2. `FileMetadata`

**Line**: 43  
**Methods**: 0

Metadata for efficient change detection

[TIP] **Suggested split**: Move to `filemetadata.py`

---

### 3. `EfficientChangeDetector`

**Line**: 53  
**Methods**: 11

USN-inspired change detection for file systems
Uses metadata-based tracking instead of full content scanning

[TIP] **Suggested split**: Move to `efficientchangedetector.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
