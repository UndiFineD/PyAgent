# cloud_asset_discovery_core

**File**: `src\core\base\logic\core\cloud_asset_discovery_core.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 18 imports  
**Lines**: 493  
**Complexity**: 6 (moderate)

## Overview

Cloud Asset Discovery Core

Inspired by CloudRecon tool for SSL certificate-based asset discovery.
Implements certificate inspection and keyword-based cloud asset finding.

## Classes (4)

### `CertificateInfo`

SSL certificate information

### `AssetFinding`

Discovered cloud asset

### `DiscoveryResult`

Result from asset discovery scan

### `CloudAssetDiscoveryCore`

Core for discovering cloud assets through SSL certificate inspection.

Based on CloudRecon patterns for finding ephemeral and development assets
by inspecting SSL certificates in IP ranges.

**Methods** (6):
- `__init__(self, max_concurrent, timeout)`
- `_init_database(self)`
- `_check_keywords(self, cert_info, keywords)`
- `_classify_asset(self, cert_info, keywords)`
- `_calculate_confidence(self, cert_info, keywords)`
- `get_cloud_ranges(self, provider)`

## Dependencies

**Imports** (18):
- `aiohttp`
- `asyncio`
- `concurrent.futures.ThreadPoolExecutor`
- `dataclasses.dataclass`
- `datetime.datetime`
- `ipaddress`
- `logging`
- `re`
- `socket`
- `sqlite3`
- `ssl`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- ... and 3 more

---
*Auto-generated documentation*
