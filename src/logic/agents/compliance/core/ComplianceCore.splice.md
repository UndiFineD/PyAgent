# Class Breakdown: ComplianceCore

**File**: `src\logic\agents\compliance\core\ComplianceCore.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ComplianceIssue`

**Line**: 8  
**Methods**: 0

[TIP] **Suggested split**: Move to `complianceissue.py`

---

### 2. `ComplianceCore`

**Line**: 14  
**Methods**: 2

Pure logic for continuous compliance auditing and regulatory scanning.
Identifies licensing conflicts, PII leaks, and dependency risks.

[TIP] **Suggested split**: Move to `compliancecore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
