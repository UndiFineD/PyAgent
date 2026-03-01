# Class Breakdown: ssrf_detector_mixin

**File**: `src\core\base\mixins\ssrf_detector_mixin.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SSRFDetectorMixin`

**Line**: 23  
**Methods**: 10

Mixin providing SSRF detection capabilities using callback server pattern.

Inspired by aem-hacker's detector server for SSRF vulnerability detection.

[TIP] **Suggested split**: Move to `ssrfdetectormixin.py`

---

### 2. `_DetectorHandler`

**Line**: 42  
**Inherits**: BaseHTTPRequestHandler  
**Methods**: 6

HTTP handler for SSRF detection callbacks.

[TIP] **Suggested split**: Move to `_detectorhandler.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
