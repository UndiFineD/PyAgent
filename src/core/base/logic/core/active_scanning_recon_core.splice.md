# Class Breakdown: active_scanning_recon_core

**File**: `src\core\base\logic\core\active_scanning_recon_core.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ScanTarget`

**Line**: 38  
**Methods**: 1

Target for scanning operations

[TIP] **Suggested split**: Move to `scantarget.py`

---

### 2. `ScanResult`

**Line**: 57  
**Methods**: 0

Result from scanning operation

[TIP] **Suggested split**: Move to `scanresult.py`

---

### 3. `VulnerabilityFinding`

**Line**: 69  
**Methods**: 0

Vulnerability finding

[TIP] **Suggested split**: Move to `vulnerabilityfinding.py`

---

### 4. `ActiveScanningReconCore`

**Line**: 81  
**Methods**: 8

Core for active scanning and reconnaissance operations.

Based on patterns from active-scan-plus-plus repository, implementing
comprehensive network scanning, service enumeration, and vulnerability as...

[TIP] **Suggested split**: Move to `activescanningreconcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
