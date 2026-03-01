# aem_detection_core

**File**: `src\core\base\logic\core\aem_detection_core.py`  
**Type**: Python Module  
**Summary**: 4 classes, 0 functions, 23 imports  
**Lines**: 649  
**Complexity**: 5 (moderate)

## Overview

AEM Detection Core

This core implements AEM (Adobe Experience Manager) detection patterns inspired by aem-eye.
It provides fast, concurrent detection of AEM installations through signature-based analysis.

Key Features:
- Fast concurrent AEM detection using async HTTP requests
- Signature-based detection with configurable patterns
- Rate limiting and concurrency controls
- Support for large-scale host scanning
- AEM-specific path and content detection
- Version fingerprinting capabilities
- Integration with vulnerability assessment workflows

## Classes (4)

### `AEMDetectionResult`

Result of AEM detection for a single host.

### `AEMScanConfig`

Configuration for AEM detection scan.

### `AEMScanResults`

Results of a complete AEM detection scan.

### `AEMDetectionCore`

**Inherits from**: BaseCore

Core for AEM (Adobe Experience Manager) detection and analysis.

This core provides fast, concurrent detection of AEM installations using
signature-based analysis patterns inspired by the aem-eye tool.

**Methods** (5):
- `__init__(self)`
- `_detect_aem_version(self, body)`
- `_parse_config(self, config_dict)`
- `get_capabilities(self)`
- `get_supported_task_types(self)`

## Dependencies

**Imports** (23):
- `aiohttp`
- `asyncio`
- `concurrent.futures.ThreadPoolExecutor`
- `csv`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `json`
- `logging`
- `os`
- `re`
- `src.core.base.common.base_core.BaseCore`
- `src.core.base.common.models.communication_models.CascadeContext`
- `src.core.base.state.agent_state_manager.StateTransaction`
- `ssl`
- ... and 8 more

---
*Auto-generated documentation*
