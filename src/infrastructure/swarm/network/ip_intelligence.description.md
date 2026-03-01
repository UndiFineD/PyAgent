# ip_intelligence

**File**: `src\infrastructure\swarm\network\ip_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 218  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for ip_intelligence.

## Classes (1)

### `IPIntelligence`

Asynchronous IP Intelligence gathering using RDAP and Cymru Whois.
Refactored from 0xSojalSec-netscan.

**Methods** (3):
- `__init__(self, max_concurrent, timeout)`
- `is_cloudflare(self, ip)`
- `clean_org_name(org_name)`

## Dependencies

**Imports** (9):
- `aiohttp`
- `asyncio`
- `functools.lru_cache`
- `ipaddress`
- `logging`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
