# pe_utils

**File**: `src\logic\agents\security\toolkit\rpc\rpc_toolkit\pe_rpc_if_scraper\pe_utils.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 6 imports  
**Lines**: 51  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for pe_utils.

## Functions (4)

### `ptr_to_rva(ptr, pe)`

### `assert_dotnet_pe(pe)`

### `get_rdata_offset_size_rva(pe)`

### `get_rpcrt_imports(pe)`

## Dependencies

**Imports** (6):
- `pefile.PE`
- `scraper_exceptions.CantFindRDataSectionException`
- `scraper_exceptions.DotNetPeException`
- `scraper_exceptions.NoRpcImportException`
- `typing.Dict`
- `typing.Tuple`

---
*Auto-generated documentation*
