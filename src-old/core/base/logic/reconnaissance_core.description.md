# reconnaissance_core

**File**: `src\core\base\logic\reconnaissance_core.py`  
**Type**: Python Module  
**Summary**: 7 classes, 0 functions, 15 imports  
**Lines**: 347  
**Complexity**: 11 (moderate)

## Overview

Reconnaissance Core - Intelligence gathering and asset discovery
Based on patterns from alterx (DSL-based generation) and amass (multi-source intelligence)

## Classes (7)

### `SubdomainResult`

Result of subdomain enumeration

**Methods** (1):
- `__post_init__(self)`

### `ReconConfig`

Configuration for reconnaissance operations

**Methods** (1):
- `__post_init__(self)`

### `IntelligenceSource`

**Inherits from**: ABC

Abstract base class for intelligence sources

**Methods** (1):
- `name(self)`

### `DNSSource`

**Inherits from**: IntelligenceSource

DNS-based subdomain enumeration using brute force

**Methods** (2):
- `__init__(self)`
- `name(self)`

### `CertificateTransparencySource`

**Inherits from**: IntelligenceSource

Certificate Transparency log enumeration

**Methods** (1):
- `name(self)`

### `ThreatCrowdSource`

**Inherits from**: IntelligenceSource

ThreatCrowd API enumeration

**Methods** (1):
- `name(self)`

### `ReconnaissanceCore`

Intelligence gathering and asset discovery core
Combines patterns from alterx (DSL generation) and amass (multi-source intelligence)

**Methods** (4):
- `__init__(self)`
- `_register_sources(self)`
- `generate_wordlist(self, patterns, payloads)`
- `_expand_pattern(self, pattern, payloads)`

## Dependencies

**Imports** (15):
- `abc.ABC`
- `abc.abstractmethod`
- `aiohttp`
- `asyncio`
- `dataclasses.dataclass`
- `dns.exception`
- `dns.resolver`
- `logging`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`
- `urllib.parse.urlparse`

---
*Auto-generated documentation*
