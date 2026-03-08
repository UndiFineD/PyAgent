# Class Breakdown: compliance_core

**File**: `src\logic\agents\compliance\core\compliance_core.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ComplianceIssue`

**Line**: 26  
**Methods**: 0

Represents a regulatory or policy violation found in code.

[TIP] **Suggested split**: Move to `complianceissue.py`

---

### 2. `ComplianceCore`

**Line**: 35  
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
