# Class Breakdown: scraper_exceptions

**File**: `src\logic\agents\security\toolkit\rpc\rpc_toolkit\pe_rpc_if_scraper\scraper_exceptions.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `NoRpcImportException`

**Line**: 18  
**Inherits**: Exception  
**Methods**: 0

[TIP] **Suggested split**: Move to `norpcimportexception.py`

---

### 2. `CantDetermineRpcSideException`

**Line**: 22  
**Inherits**: Exception  
**Methods**: 0

[TIP] **Suggested split**: Move to `cantdeterminerpcsideexception.py`

---

### 3. `CantFindRDataSectionException`

**Line**: 26  
**Inherits**: Exception  
**Methods**: 0

[TIP] **Suggested split**: Move to `cantfindrdatasectionexception.py`

---

### 4. `DotNetPeException`

**Line**: 30  
**Inherits**: Exception  
**Methods**: 0

[TIP] **Suggested split**: Move to `dotnetpeexception.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
