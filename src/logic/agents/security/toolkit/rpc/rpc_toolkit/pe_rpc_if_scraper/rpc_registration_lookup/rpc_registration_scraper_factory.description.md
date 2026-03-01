# rpc_registration_scraper_factory

**File**: `src\logic\agents\security\toolkit\rpc\rpc_toolkit\pe_rpc_if_scraper\rpc_registration_lookup\rpc_registration_scraper_factory.py`  
**Type**: Python Module  
**Summary**: 1 classes, 1 functions, 3 imports  
**Lines**: 40  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for rpc_registration_scraper_factory.

## Classes (1)

### `UnsupportedDisassemblerTypeException`

**Inherits from**: Exception

Class UnsupportedDisassemblerTypeException implementation.

**Methods** (1):
- `__init__(self, dism_name)`

## Functions (1)

### `rpc_registration_scraper_factory(disassembler)`

## Dependencies

**Imports** (3):
- `rpc_registration_lookup.base_rpc_registration_scraper.BaseRpcRegistrationExtractor`
- `rpc_registration_lookup.ida_rpc_registration_scraper.IdaProRpcRegistrationExtractor`
- `rpc_registration_lookup.radare_rpc_registration_scraper.Radare2RpcRegistrationExtractor`

---
*Auto-generated documentation*
