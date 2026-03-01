# censys_intelligence

**File**: `src\infrastructure\swarm\network\censys_intelligence.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 15 imports  
**Lines**: 155  
**Complexity**: 1 (simple)

## Overview

Python module containing implementation for censys_intelligence.

## Classes (2)

### `CensysResult`

Class CensysResult implementation.

### `CensysIntelligence`

Integrates functionality from 0xSojalSec-censeye and 0xSojalSec-censys-subdomain-finder.
Provides subdomain enumeration and deep host enrichment via Censys API.

**Methods** (1):
- `__init__(self, api_id, api_secret)`

## Dependencies

**Imports** (15):
- `asyncio`
- `censys.common.exceptions.CensysException`
- `censys.search.CensysCerts`
- `censys.search.CensysHosts`
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `os`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
