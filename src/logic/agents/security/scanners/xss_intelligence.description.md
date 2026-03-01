# xss_intelligence

**File**: `src\logic\agents\security\scanners\xss_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 11 imports  
**Lines**: 116  
**Complexity**: 0 (simple)

## Overview

Python module containing implementation for xss_intelligence.

## Classes (1)

### `XssIntelligence`

Refactored XSS detection logic from various external tools (AutoRecon-XSS, etc).
Focuses on reflected XSS by verifying payload reflection in responses.

## Dependencies

**Imports** (11):
- `aiohttp`
- `asyncio`
- `re`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `urllib.parse.parse_qs`
- `urllib.parse.urlencode`
- `urllib.parse.urlparse`
- `urllib.parse.urlunparse`

---
*Auto-generated documentation*
