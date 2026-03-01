# pe_rpc_if_analysis

**File**: `src\logic\agents\security\toolkit\rpc\rpc_toolkit\pe_rpc_if_scraper\pe_rpc_if_analysis.py`  
**Type**: Python Module  
**Summary**: 1 classes, 1 functions, 18 imports  
**Lines**: 160  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for pe_rpc_if_analysis.

## Classes (1)

### `PeRpcInterfaceScraper`

Class PeRpcInterfaceScraper implementation.

**Methods** (7):
- `__init__(self, disassembler)`
- `__del__(self)`
- `scrape_executable(self, pe_path)`
- `_get_rpc_if_offsets(self, data)`
- `_get_interface_data(self, pe, interface_off)`
- `_check_flags_for_global_cache(flags)`
- `_get_security_callback_name(self, callback_addr)`

## Functions (1)

### `sym_help_dummy(pe_path)`

## Dependencies

**Imports** (18):
- `contextlib.contextmanager`
- `pe_utils.assert_dotnet_pe`
- `pe_utils.get_rdata_offset_size_rva`
- `pe_utils.ptr_to_rva`
- `pefile.PE`
- `platform`
- `re`
- `rpc_registration_lookup.base_rpc_registration_scraper.BaseRpcRegistrationExtractor`
- `rpc_registration_lookup.base_rpc_registration_scraper.INTERFACE_FLAGS`
- `rpc_registration_lookup.base_rpc_registration_scraper.INTERFACE_SECURITY_CALLBACK`
- `rpc_registration_lookup.base_rpc_registration_scraper.PARSING_ERROR`
- `symbol_helper.PESymbolMatcher`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 3 more

---
*Auto-generated documentation*
