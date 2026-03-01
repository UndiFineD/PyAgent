# acunetix_automation_core

**File**: `src\core\base\logic\core\acunetix_automation_core.py`  
**Type**: Python Module  
**Summary**: 6 classes, 0 functions, 14 imports  
**Lines**: 647  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for acunetix_automation_core.

## Classes (6)

### `ScanType`

**Inherits from**: Enum

Acunetix scan types

### `ScanStatus`

**Inherits from**: Enum

Scan status enumeration

### `ScanTarget`

Represents a target for scanning

### `ScanResult`

Result from a vulnerability scan

### `AcunetixConfig`

Configuration for Acunetix API

**Methods** (1):
- `base_url(self)`

### `AcunetixAutomationCore`

Acunetix Automation Core for automated web vulnerability scanning.

Provides capabilities for automated scanning, batch processing,
scan management, and integration with Acunetix vulnerability scanner.

**Methods** (2):
- `__init__(self, config)`
- `_is_valid_url(self, url)`

## Dependencies

**Imports** (14):
- `aiohttp`
- `asyncio`
- `dataclasses.dataclass`
- `dataclasses.field`
- `datetime.datetime`
- `enum.Enum`
- `json`
- `logging`
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Union`

---
*Auto-generated documentation*
