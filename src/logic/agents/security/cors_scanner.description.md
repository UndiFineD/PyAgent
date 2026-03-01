# cors_scanner

**File**: `src\logic\agents\security\cors_scanner.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 8 imports  
**Lines**: 251  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for cors_scanner.

## Classes (2)

### `CORSVulnerability`

Class CORSVulnerability implementation.

### `CORSScanner`

Ported logic from 0xSojalSec-Corsy.
Scans a target URL for CORS misconfigurations.

**Methods** (3):
- `__init__(self, timeout, concurrency)`
- `_get_host(self, url)`
- `_create_vuln(self, url, key, acao, acac)`

## Dependencies

**Imports** (8):
- `aiohttp`
- `asyncio`
- `dataclasses.dataclass`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
