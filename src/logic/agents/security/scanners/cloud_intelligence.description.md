# cloud_intelligence

**File**: `src\logic\agents\security\scanners\cloud_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 148  
**Complexity**: 6 (moderate)

## Overview

Python module containing implementation for cloud_intelligence.

## Classes (1)

### `CloudIntelligence`

Handles discovery and auditing of cloud assets (S3, Azure Blobs, GCP Buckets).
Ported logic from s3crets_scanner and other cloud-focused tools.

**Methods** (6):
- `__init__(self)`
- `get_gcp_audit_targets()`
- `get_dangling_resource_indicators()`
- `get_cspm_misconfigurations()`
- `get_ciem_path_finding_logic()`
- `get_ai_spm_indicators()`

## Dependencies

**Imports** (8):
- `aiohttp`
- `asyncio`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `urllib.parse.urljoin`

---
*Auto-generated documentation*
