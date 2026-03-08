# security_scanner_agent

**File**: `src\core\agents\security_scanner_agent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 169  
**Complexity**: 2 (simple)

## Overview

Module: security_scanner_agent
Agent for comprehensive security scanning using patterns from aem-hacker.
Implements vulnerability scanning, payload generation, SSRF detection, and reconnaissance.

## Classes (1)

### `SecurityScannerAgent`

**Inherits from**: BaseAgent, VulnerabilityScannerMixin, PayloadGeneratorMixin, SSRFDetectorMixin, ReconnaissanceMixin

Comprehensive security scanner agent inspired by aem-hacker patterns.

Features:
- Modular vulnerability scanning with extensible checks
- Payload generation for various exploit types
- SSRF detection using callback server pattern
- Target reconnaissance and service fingerprinting

**Methods** (2):
- `__init__(self)`
- `_generate_scan_summary(self, results)`

## Dependencies

**Imports** (12):
- `__future__.annotations`
- `asyncio`
- `src.core.base.lifecycle.base_agent.BaseAgent`
- `src.core.base.mixins.payload_generator_mixin.PayloadGeneratorMixin`
- `src.core.base.mixins.reconnaissance_mixin.ReconnaissanceMixin`
- `src.core.base.mixins.ssrf_detector_mixin.SSRFDetectorMixin`
- `src.core.base.mixins.vulnerability_scanner_mixin.VulnerabilityScannerMixin`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `uuid.UUID`

---
*Auto-generated documentation*
