# advanced_web_scanning_core

**File**: `src\core\base\logic\core\advanced_web_scanning_core.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 15 imports  
**Lines**: 570  
**Complexity**: 3 (simple)

## Overview

Advanced Web Scanning Core

This core provides comprehensive web application scanning capabilities,
including host header attacks, code injection detection, and advanced vulnerability checks.

Based on patterns from active-scan-plus-plus Burp Suite extension.

## Classes (4)

### `ScanResult`

Result from a web scan operation

### `HostHeaderTest`

Host header manipulation test case

### `AdvancedWebScanningCore`

Core for advanced web application scanning and vulnerability detection.

This core implements scanning patterns from active-scan-plus-plus,
including host header attacks, code injection, and edge case detection.

**Methods** (2):
- `__init__(self)`
- `_is_internal_redirect(self, location_header, target_url)`

### `MockResponse`

Class MockResponse implementation.

**Methods** (1):
- `__init__(self, aio_response)`

## Dependencies

**Imports** (15):
- `aiohttp`
- `asyncio`
- `dataclasses.dataclass`
- `hashlib`
- `logging`
- `re`
- `requests`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `urllib.parse.urljoin`
- `urllib.parse.urlparse`
- `urllib3`

---
*Auto-generated documentation*
