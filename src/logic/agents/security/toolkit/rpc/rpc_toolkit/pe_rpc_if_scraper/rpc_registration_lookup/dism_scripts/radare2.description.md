# radare2

**File**: `src\logic\agents\security\toolkit\rpc\rpc_toolkit\pe_rpc_if_scraper\rpc_registration_lookup\dism_scripts\radare2.py`  
**Type**: Python Module  
**Summary**: 0 classes, 10 functions, 5 imports  
**Lines**: 173  
**Complexity**: 10 (moderate)

## Overview

Python module containing implementation for radare2.

## Functions (10)

### `find_rpc_server_registration_funcs()`

### `find_all_func_xrefs(func_ea)`

### `get_func_start(ins_ea)`

### `get_reg_value(arg_ea, reg_name)`

### `is_reg(reg)`

### `parse_argument(arg_ea)`

### `get_func_call_args(func_ea, arg_count)`

### `get_call_args_manually(call_ea, max_look_behind, max_args)`

### `get_rpc_server_registration_info()`

### `get_arg_count_for_function_name(func_name)`

## Dependencies

**Imports** (5):
- `json`
- `r2pipe`
- `typing.Dict`
- `typing.List`
- `typing.Tuple`

---
*Auto-generated documentation*
