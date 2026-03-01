# GatewayCore

**File**: `src\infrastructure\api\core\GatewayCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 45  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for GatewayCore.

## Classes (1)

### `GatewayCore`

GatewayCore implements logic for SaaS service integration and load balancing.
It manages service routing and 'Interface Affinity'.

**Methods** (4):
- `__init__(self)`
- `get_service_endpoint(self, service_name)`
- `resolve_model_by_affinity(self, interface_type)`
- `format_saas_request(self, service, action, params)`

## Dependencies

**Imports** (4):
- `__future__.annotations`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

---
*Auto-generated documentation*
