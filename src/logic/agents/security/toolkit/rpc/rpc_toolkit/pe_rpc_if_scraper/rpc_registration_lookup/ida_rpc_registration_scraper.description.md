# ida_rpc_registration_scraper

**File**: `src\logic\agents\security\toolkit\rpc\rpc_toolkit\pe_rpc_if_scraper\rpc_registration_lookup\ida_rpc_registration_scraper.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 7 imports  
**Lines**: 51  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for ida_rpc_registration_scraper.

## Classes (2)

### `IdaDBOpenException`

**Inherits from**: Exception

Class IdaDBOpenException implementation.

**Methods** (1):
- `__init__(self, pe_path)`

### `IdaProRpcRegistrationExtractor`

**Inherits from**: BaseRpcRegistrationExtractor

Class IdaProRpcRegistrationExtractor implementation.

**Methods** (1):
- `_get_rpc_registration_info(self, pe_path)`

## Dependencies

**Imports** (7):
- `json`
- `os`
- `rpc_registration_lookup.base_rpc_registration_scraper.BaseRpcRegistrationExtractor`
- `rpc_registration_lookup.base_rpc_registration_scraper.DismExtractorFailue`
- `subprocess`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
