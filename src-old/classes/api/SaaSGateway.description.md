# SaaSGateway

**File**: `src\classes\api\SaaSGateway.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 102  
**Complexity**: 5 (moderate)

## Overview

Gateway for managing multi-tenant SaaS access, API keys, and usage quotas.

## Classes (1)

### `SaaSGateway`

Provides usage control and authentication for the fleet as a service.
Integrated with GatewayCore for external SaaS orchestration.

**Methods** (5):
- `__init__(self)`
- `call_external_saas(self, api_key, service, action, params)`
- `create_api_key(self, tenant_id, daily_quota)`
- `validate_request(self, api_key, cost)`
- `get_quota_status(self, api_key)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `logging`
- `src.core.base.version.VERSION`
- `src.infrastructure.api.core.GatewayCore.GatewayCore`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `uuid`

---
*Auto-generated documentation*
