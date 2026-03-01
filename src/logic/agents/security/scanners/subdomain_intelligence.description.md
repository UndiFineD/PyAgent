# subdomain_intelligence

**File**: `src\logic\agents\security\scanners\subdomain_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 142  
**Complexity**: 2 (simple)

## Overview

Python module containing implementation for subdomain_intelligence.

## Classes (1)

### `SubdomainIntelligence`

Unified engine for passive subdomain discovery using multiple OSINT sources.

**Methods** (2):
- `__init__(self, session)`
- `_clean_subdomains(self, subdomains, target_domain)`

## Dependencies

**Imports** (9):
- `aiohttp`
- `asyncio`
- `json`
- `re`
- `src.core.base.logic.logger.logger`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
