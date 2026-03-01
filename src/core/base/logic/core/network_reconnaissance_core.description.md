# network_reconnaissance_core

**File**: `src\core\base\logic\core\network_reconnaissance_core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 25 imports  
**Lines**: 430  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for network_reconnaissance_core.

## Classes (3)

### `AssetDiscoveryResult`

Result of network asset discovery operations.

### `ReconnaissanceConfig`

Configuration for reconnaissance operations.

### `NetworkReconnaissanceCore`

**Inherits from**: BaseCore

Network Reconnaissance Core implementing comprehensive asset discovery patterns.

Inspired by OWASP Amass, this core provides:
- DNS enumeration and subdomain discovery
- Certificate transparency analysis
- Web asset discovery and crawling
- API endpoint detection
- Passive and active reconnaissance techniques

**Methods** (4):
- `__init__(self, config)`
- `_extract_links_from_html(self, html, domain)`
- `_calculate_confidence_score(self, result)`
- `get_discovery_summary(self, result)`

## Dependencies

**Imports** (25):
- `aiohttp`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `datetime.timedelta`
- `dns.resolver`
- `dns.reversename`
- `dns.zone`
- `ipaddress`
- `json`
- `re`
- `socket`
- `src.core.base.common.base_core.BaseCore`
- `ssl`
- ... and 10 more

---
*Auto-generated documentation*
