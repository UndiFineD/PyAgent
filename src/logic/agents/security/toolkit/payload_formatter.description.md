# payload_formatter

**File**: `src\logic\agents\security\toolkit\payload_formatter.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 35  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for payload_formatter.

## Classes (1)

### `PayloadFormatter`

Formats parameter lists into various HTTP request body formats. 

**Methods** (4):
- `to_json(params, value)`
- `to_form_urlencoded(params, value)`
- `to_xml(params, value)`
- `to_multipart(params, value, boundary)`

## Dependencies

**Imports** (3):
- `json`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
