# Class Breakdown: ida_rpc_registration_scraper

**File**: `src\logic\agents\security\toolkit\rpc\rpc_toolkit\pe_rpc_if_scraper\rpc_registration_lookup\ida_rpc_registration_scraper.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `IdaDBOpenException`

**Line**: 29  
**Inherits**: Exception  
**Methods**: 1

[TIP] **Suggested split**: Move to `idadbopenexception.py`

---

### 2. `IdaProRpcRegistrationExtractor`

**Line**: 34  
**Inherits**: BaseRpcRegistrationExtractor  
**Methods**: 1

[TIP] **Suggested split**: Move to `idaprorpcregistrationextractor.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
