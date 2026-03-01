# symbol_helper

**File**: `src\logic\agents\security\toolkit\rpc\rpc_toolkit\pe_rpc_if_scraper\symbol_helper.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 3 imports  
**Lines**: 184  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for symbol_helper.

## Classes (7)

### `CantInitializeDebugHelperException`

**Inherits from**: Exception

Class CantInitializeDebugHelperException implementation.

### `CantLoadDebugSymbolsException`

**Inherits from**: Exception

Class CantLoadDebugSymbolsException implementation.

### `PeAlreadyLoadedException`

**Inherits from**: Exception

Class PeAlreadyLoadedException implementation.

### `PeNotLoadedException`

**Inherits from**: Exception

Class PeNotLoadedException implementation.

### `SYMBOL_INFO`

**Inherits from**: Structure

Class SYMBOL_INFO implementation.

### `MODULE_INFO`

**Inherits from**: Structure

Class MODULE_INFO implementation.

### `PESymbolMatcher`

**Inherits from**: object

Class PESymbolMatcher implementation.

**Methods** (8):
- `__init__(self)`
- `__del__(self)`
- `__call__(self, pe_path)`
- `_define_dbghelp_funcs(self)`
- `load_pe(self, pe_path)`
- `unload_pe(self)`
- `sym_from_addr(self, addr)`
- `assert_loaded_pe(self)`

## Dependencies

**Imports** (3):
- `contextlib.contextmanager`
- `ctypes`
- `ctypes.wintypes`

---
*Auto-generated documentation*
