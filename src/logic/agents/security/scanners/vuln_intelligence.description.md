# vuln_intelligence

**File**: `src\logic\agents\security\scanners\vuln_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 10 imports  
**Lines**: 217  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for vuln_intelligence.

## Classes (1)

### `VulnIntelligence`

Refactored vulnerability scanners from Artemis.
Focuses on web application vulnerabilities and misconfigurations.

**Methods** (3):
- `generate_crlf_payloads()`
- `generate_content_type_bypasses(original_ct)`
- `get_vulnerable_params()`

## Dependencies

**Imports** (10):
- `aiohttp`
- `asyncio`
- `re`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `urllib.parse.parse_qs`
- `urllib.parse.urlencode`
- `urllib.parse.urlparse`
- `urllib.parse.urlunparse`

---
*Auto-generated documentation*
