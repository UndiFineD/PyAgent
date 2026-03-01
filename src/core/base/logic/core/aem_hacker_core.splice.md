# Class Breakdown: aem_hacker_core

**File**: `src\core\base\logic\core\aem_hacker_core.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AEMFinding`

**Line**: 48  
**Methods**: 0

Represents a security finding in AEM assessment.

[TIP] **Suggested split**: Move to `aemfinding.py`

---

### 2. `AEMScanConfig`

**Line**: 59  
**Methods**: 0

Configuration for AEM security scanning.

[TIP] **Suggested split**: Move to `aemscanconfig.py`

---

### 3. `AEMScanResults`

**Line**: 73  
**Methods**: 0

Results from AEM security scanning.

[TIP] **Suggested split**: Move to `aemscanresults.py`

---

### 4. `AEMHackerCore`

**Line**: 82  
**Inherits**: BaseCore  
**Methods**: 10

Advanced AEM Security Assessment Core

Implements comprehensive vulnerability scanning for Adobe Experience Manager
instances, detecting SSRF, RCE, XSS, and misconfiguration vulnerabilities.

[TIP] **Suggested split**: Move to `aemhackercore.py`

---

### 5. `AEMSSRFDetector`

**Line**: 471  
**Methods**: 1

SSRF detection server for AEM vulnerability scanning.

[TIP] **Suggested split**: Move to `aemssrfdetector.py`

---

### 6. `AEMSSRFHandler`

**Line**: 500  
**Inherits**: BaseHTTPRequestHandler  
**Methods**: 5

HTTP handler for SSRF detection.

[TIP] **Suggested split**: Move to `aemssrfhandler.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
