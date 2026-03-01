# js_intelligence

**File**: `src\logic\agents\security\scanners\js_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 180  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for js_intelligence.

## Classes (1)

### `JSIntelligence`

Intelligence module for JavaScript analysis, secret discovery, and link extraction.
Ported from jsleak, LinkFinder, and jsluce.

**Methods** (3):
- `__init__(self, session)`
- `extract_links(self, content, base_url)`
- `generate_xss_payload(self, callback_url, include_screenshot)`

## Dependencies

**Imports** (9):
- `aiohttp`
- `asyncio`
- `re`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `urllib.parse.urljoin`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
