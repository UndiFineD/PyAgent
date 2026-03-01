# Class Breakdown: bloodhound_integration_core

**File**: `src\core\base\logic\core\bloodhound_integration_core.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `RiskLevel`

**Line**: 29  
**Inherits**: Enum  
**Methods**: 0

Risk severity levels

[TIP] **Suggested split**: Move to `risklevel.py`

---

### 2. `ADObjectType`

**Line**: 37  
**Inherits**: Enum  
**Methods**: 0

Active Directory object types

[TIP] **Suggested split**: Move to `adobjecttype.py`

---

### 3. `SecurityControl`

**Line**: 47  
**Inherits**: Enum  
**Methods**: 0

Security controls that can be assessed

[TIP] **Suggested split**: Move to `securitycontrol.py`

---

### 4. `ADObject`

**Line**: 68  
**Methods**: 0

Represents an Active Directory object

[TIP] **Suggested split**: Move to `adobject.py`

---

### 5. `SecurityFinding`

**Line**: 80  
**Methods**: 0

Represents a security finding

[TIP] **Suggested split**: Move to `securityfinding.py`

---

### 6. `ControlPath`

**Line**: 93  
**Methods**: 0

Represents a control path in the AD graph

[TIP] **Suggested split**: Move to `controlpath.py`

---

### 7. `AuditReport`

**Line**: 103  
**Methods**: 0

Comprehensive audit report

[TIP] **Suggested split**: Move to `auditreport.py`

---

### 8. `BloodHoundIntegrationCore`

**Line**: 116  
**Methods**: 1

BloodHound Integration Core for graph-based Active Directory security analysis.

Provides comprehensive AD security assessment using graph database patterns,
risk analysis, and security control evalua...

[TIP] **Suggested split**: Move to `bloodhoundintegrationcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
