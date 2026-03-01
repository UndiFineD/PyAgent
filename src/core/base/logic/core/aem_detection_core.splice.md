# Class Breakdown: aem_detection_core

**File**: `src\core\base\logic\core\aem_detection_core.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AEMDetectionResult`

**Line**: 53  
**Methods**: 0

Result of AEM detection for a single host.

[TIP] **Suggested split**: Move to `aemdetectionresult.py`

---

### 2. `AEMScanConfig`

**Line**: 69  
**Methods**: 0

Configuration for AEM detection scan.

[TIP] **Suggested split**: Move to `aemscanconfig.py`

---

### 3. `AEMScanResults`

**Line**: 91  
**Methods**: 0

Results of a complete AEM detection scan.

[TIP] **Suggested split**: Move to `aemscanresults.py`

---

### 4. `AEMDetectionCore`

**Line**: 101  
**Inherits**: BaseCore  
**Methods**: 5

Core for AEM (Adobe Experience Manager) detection and analysis.

This core provides fast, concurrent detection of AEM installations using
signature-based analysis patterns inspired by the aem-eye tool...

[TIP] **Suggested split**: Move to `aemdetectioncore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
