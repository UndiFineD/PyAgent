# dns_security_core

**File**: `src\core\base\logic\core\dns_security_core.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 22 imports  
**Lines**: 522  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for dns_security_core.

## Classes (7)

### `DnsRecordType`

**Inherits from**: Enum

DNS record types

### `FilterAction`

**Inherits from**: Enum

DNS filtering actions

### `QueryResult`

**Inherits from**: Enum

DNS query results

### `DnsQuery`

DNS query representation

### `FilterRule`

DNS filtering rule

### `DnsStatistics`

DNS statistics container

### `DnsSecurityCore`

DNS Security Core for network-level filtering and analysis.

Provides comprehensive DNS filtering, logging, and security analysis
based on AdGuard Home methodologies.

**Methods** (3):
- `__init__(self)`
- `_matches_pattern(self, domain, pattern)`
- `_update_statistics(self, query)`

## Dependencies

**Imports** (22):
- `asyncio`
- `collections.defaultdict`
- `collections.deque`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timedelta`
- `enum.Enum`
- `hashlib`
- `ipaddress`
- `json`
- `logging`
- `pathlib.Path`
- `re`
- `time`
- ... and 7 more

---
*Auto-generated documentation*
