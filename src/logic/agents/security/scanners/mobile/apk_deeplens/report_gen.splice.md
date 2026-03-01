# Class Breakdown: report_gen

**File**: `src\logic\agents\security\scanners\mobile\apk_deeplens\report_gen.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `util`

**Line**: 21  
**Methods**: 2

A static class for which contain some useful variables and methods

[TIP] **Suggested split**: Move to `util.py`

---

### 2. `ReportGen`

**Line**: 45  
**Inherits**: object  
**Methods**: 17

[TIP] **Suggested split**: Move to `reportgen.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
