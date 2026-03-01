# Class Breakdown: active_directory_threat_hunting_core

**File**: `src\core\base\logic\core\active_directory_threat_hunting_core.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ThreatLevel`

**Line**: 29  
**Inherits**: Enum  
**Methods**: 0

Threat severity levels

[TIP] **Suggested split**: Move to `threatlevel.py`

---

### 2. `ADObjectType`

**Line**: 37  
**Inherits**: Enum  
**Methods**: 0

Active Directory object types

[TIP] **Suggested split**: Move to `adobjecttype.py`

---

### 3. `ADObject`

**Line**: 48  
**Methods**: 0

Represents an Active Directory object

[TIP] **Suggested split**: Move to `adobject.py`

---

### 4. `ThreatFinding`

**Line**: 63  
**Methods**: 0

Represents a threat hunting finding

[TIP] **Suggested split**: Move to `threatfinding.py`

---

### 5. `HuntingResult`

**Line**: 77  
**Methods**: 0

Results from a threat hunting operation

[TIP] **Suggested split**: Move to `huntingresult.py`

---

### 6. `ActiveDirectoryThreatHuntingCore`

**Line**: 88  
**Inherits**: BaseCore  
**Methods**: 1

Active Directory Threat Hunting Core for comprehensive AD security analysis.

Provides capabilities for Active Directory enumeration, threat detection,
permission analysis, and security monitoring bas...

[TIP] **Suggested split**: Move to `activedirectorythreathuntingcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
