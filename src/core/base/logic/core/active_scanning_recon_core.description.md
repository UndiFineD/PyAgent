# active_scanning_recon_core

**File**: `src\core\base\logic\core\active_scanning_recon_core.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 18 imports  
**Lines**: 625  
**Complexity**: 9 (moderate)

## Overview

Active Scanning and Reconnaissance Core

Inspired by active-scan-plus-plus repository patterns for comprehensive
network scanning, service enumeration, and vulnerability assessment.

## Classes (4)

### `ScanTarget`

Target for scanning operations

**Methods** (1):
- `__post_init__(self)`

### `ScanResult`

Result from scanning operation

### `VulnerabilityFinding`

Vulnerability finding

### `ActiveScanningReconCore`

Core for active scanning and reconnaissance operations.

Based on patterns from active-scan-plus-plus repository, implementing
comprehensive network scanning, service enumeration, and vulnerability assessment.

**Methods** (8):
- `__init__(self)`
- `_init_service_signatures(self)`
- `_init_vulnerability_db(self)`
- `_check_service_vulnerabilities(self, service, port)`
- `export_scan_results(self, results, format_type)`
- `_export_json(self, results)`
- `_export_csv(self, results)`
- `get_scan_statistics(self, results)`

## Dependencies

**Imports** (18):
- `aiohttp`
- `asyncio`
- `concurrent.futures.ThreadPoolExecutor`
- `dataclasses.dataclass`
- `datetime.datetime`
- `hashlib`
- `ipaddress`
- `json`
- `logging`
- `socket`
- `ssl`
- `struct`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- ... and 3 more

---
*Auto-generated documentation*
