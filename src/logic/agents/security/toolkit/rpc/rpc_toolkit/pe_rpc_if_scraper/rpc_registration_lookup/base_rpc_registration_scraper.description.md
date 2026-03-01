# base_rpc_registration_scraper

**File**: `src\logic\agents\security\toolkit\rpc\rpc_toolkit\pe_rpc_if_scraper\rpc_registration_lookup\base_rpc_registration_scraper.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 8 imports  
**Lines**: 101  
**Complexity**: 10 (moderate)

## Overview

Python module containing implementation for base_rpc_registration_scraper.

## Classes (3)

### `UnknownRpcServerRegistrationFunctionException`

**Inherits from**: Exception

Class UnknownRpcServerRegistrationFunctionException implementation.

**Methods** (1):
- `__init__(self, func_name)`

### `DismExtractorFailue`

**Inherits from**: Exception

Class DismExtractorFailue implementation.

**Methods** (1):
- `__init__(self, return_code)`

### `BaseRpcRegistrationExtractor`

Class BaseRpcRegistrationExtractor implementation.

**Methods** (8):
- `__init__(self, dism_path)`
- `get_rpc_registration_info(self, pe_path)`
- `_get_rpc_registration_info(self, pe_path)`
- `_get_parser_for_func_name(self, func_name)`
- `_parse_server_register_ex(self, args)`
- `_parse_server_register(self, args)`
- `_parse_server_register3(self, args)`
- `_formalize_params(rpc_if_addr, flags, security_callback, explicit_security_descriptor)`

## Dependencies

**Imports** (8):
- `abc.ABCMeta`
- `abc.abstractmethod`
- `typing.Callable`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Tuple`
- `typing.Union`

---
*Auto-generated documentation*
