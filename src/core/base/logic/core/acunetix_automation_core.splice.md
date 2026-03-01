# Class Breakdown: acunetix_automation_core

**File**: `src\core\base\logic\core\acunetix_automation_core.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ScanType`

**Line**: 29  
**Inherits**: Enum  
**Methods**: 0

Acunetix scan types

[TIP] **Suggested split**: Move to `scantype.py`

---

### 2. `ScanStatus`

**Line**: 39  
**Inherits**: Enum  
**Methods**: 0

Scan status enumeration

[TIP] **Suggested split**: Move to `scanstatus.py`

---

### 3. `ScanTarget`

**Line**: 49  
**Methods**: 0

Represents a target for scanning

[TIP] **Suggested split**: Move to `scantarget.py`

---

### 4. `ScanResult`

**Line**: 62  
**Methods**: 0

Result from a vulnerability scan

[TIP] **Suggested split**: Move to `scanresult.py`

---

### 5. `AcunetixConfig`

**Line**: 81  
**Methods**: 1

Configuration for Acunetix API

[TIP] **Suggested split**: Move to `acunetixconfig.py`

---

### 6. `AcunetixAutomationCore`

**Line**: 94  
**Methods**: 2

Acunetix Automation Core for automated web vulnerability scanning.

Provides capabilities for automated scanning, batch processing,
scan management, and integration with Acunetix vulnerability scanner...

[TIP] **Suggested split**: Move to `acunetixautomationcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
