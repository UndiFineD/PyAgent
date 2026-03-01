# Class Breakdown: APKDeepLens

**File**: `src\logic\agents\security\scanners\mobile\apk_deeplens\APKDeepLens.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `util`

**Line**: 23  
**Inherits**: util  
**Methods**: 2

A static class for which contain some useful variables and methods

[TIP] **Suggested split**: Move to `util.py`

---

### 2. `AutoApkScanner`

**Line**: 117  
**Inherits**: object  
**Methods**: 5

[TIP] **Suggested split**: Move to `autoapkscanner.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
