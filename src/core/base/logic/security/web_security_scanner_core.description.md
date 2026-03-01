# web_security_scanner_core

**File**: `src\core\base\logic\security\web_security_scanner_core.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 150  
**Complexity**: 2 (simple)

## Overview

Module: web_security_scanner_core
Core logic for web security scanning, refactored from aem-eye patterns.
Implements asynchronous web application scanning with pattern matching for vulnerability detection.

## Classes (1)

### `WebSecurityScannerCore`

Core logic for web security scanning operations.

**Methods** (2):
- `__init__(self, timeout, concurrency, rate_limit)`
- `_normalize_url(self, host)`

## Dependencies

**Imports** (11):
- `__future__.annotations`
- `aiohttp`
- `asyncio`
- `re`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
