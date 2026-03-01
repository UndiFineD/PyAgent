# Class Breakdown: symbol_helper

**File**: `src\logic\agents\security\toolkit\rpc\rpc_toolkit\pe_rpc_if_scraper\symbol_helper.py`  
**Classes**: 7

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CantInitializeDebugHelperException`

**Line**: 28  
**Inherits**: Exception  
**Methods**: 0

[TIP] **Suggested split**: Move to `cantinitializedebughelperexception.py`

---

### 2. `CantLoadDebugSymbolsException`

**Line**: 32  
**Inherits**: Exception  
**Methods**: 0

[TIP] **Suggested split**: Move to `cantloaddebugsymbolsexception.py`

---

### 3. `PeAlreadyLoadedException`

**Line**: 36  
**Inherits**: Exception  
**Methods**: 0

[TIP] **Suggested split**: Move to `pealreadyloadedexception.py`

---

### 4. `PeNotLoadedException`

**Line**: 40  
**Inherits**: Exception  
**Methods**: 0

[TIP] **Suggested split**: Move to `penotloadedexception.py`

---

### 5. `SYMBOL_INFO`

**Line**: 44  
**Inherits**: Structure  
**Methods**: 0

[TIP] **Suggested split**: Move to `symbol_info.py`

---

### 6. `MODULE_INFO`

**Line**: 63  
**Inherits**: Structure  
**Methods**: 0

[TIP] **Suggested split**: Move to `module_info.py`

---

### 7. `PESymbolMatcher`

**Line**: 78  
**Inherits**: object  
**Methods**: 8

[TIP] **Suggested split**: Move to `pesymbolmatcher.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
