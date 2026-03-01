# Class Breakdown: advanced_web_scanning_core

**File**: `src\core\base\logic\core\advanced_web_scanning_core.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ScanResult`

**Line**: 36  
**Methods**: 0

Result from a web scan operation

[TIP] **Suggested split**: Move to `scanresult.py`

---

### 2. `HostHeaderTest`

**Line**: 48  
**Methods**: 0

Host header manipulation test case

[TIP] **Suggested split**: Move to `hostheadertest.py`

---

### 3. `AdvancedWebScanningCore`

**Line**: 56  
**Methods**: 2

Core for advanced web application scanning and vulnerability detection.

This core implements scanning patterns from active-scan-plus-plus,
including host header attacks, code injection, and edge case...

[TIP] **Suggested split**: Move to `advancedwebscanningcore.py`

---

### 4. `MockResponse`

**Line**: 92  
**Methods**: 1

[TIP] **Suggested split**: Move to `mockresponse.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
