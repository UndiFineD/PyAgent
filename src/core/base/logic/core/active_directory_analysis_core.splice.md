# Class Breakdown: active_directory_analysis_core

**File**: `src\core\base\logic\core\active_directory_analysis_core.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PrivilegeLevel`

**Line**: 31  
**Inherits**: Enum  
**Methods**: 0

Active Directory privilege levels

[TIP] **Suggested split**: Move to `privilegelevel.py`

---

### 2. `ADObjectType`

**Line**: 40  
**Inherits**: Enum  
**Methods**: 0

Active Directory object types

[TIP] **Suggested split**: Move to `adobjecttype.py`

---

### 3. `ADObject`

**Line**: 51  
**Methods**: 0

Represents an Active Directory object

[TIP] **Suggested split**: Move to `adobject.py`

---

### 4. `ADEnumerationResult`

**Line**: 62  
**Methods**: 0

Results from AD enumeration

[TIP] **Suggested split**: Move to `adenumerationresult.py`

---

### 5. `ADVulnerability`

**Line**: 75  
**Methods**: 0

Represents a detected AD vulnerability

[TIP] **Suggested split**: Move to `advulnerability.py`

---

### 6. `ActiveDirectoryAnalysisCore`

**Line**: 85  
**Methods**: 2

Core for analyzing Active Directory environments and detecting security vulnerabilities.

This core implements patterns from the Active-Directory-Exploitation-Cheat-Sheet
for comprehensive AD security...

[TIP] **Suggested split**: Move to `activedirectoryanalysiscore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
