# security_mixin

**File**: `src\core\base\mixins\security_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 52  
**Complexity**: 4 (simple)

## Overview

Module: security_mixin
Security mixin for BaseAgent, implementing API security patterns for agent communications.

## Classes (1)

### `SecurityMixin`

Mixin providing API security features for agent communications.

**Methods** (4):
- `__init__(self)`
- `register_agent_credentials(self, creds)`
- `configure_rate_limiting(self, config)`
- `log_security_event(self, event)`

## Dependencies

**Imports** (7):
- `__future__.annotations`
- `src.core.base.logic.security.api_security_core.APISecurityCore`
- `src.core.base.logic.security.api_security_core.AgentCredentials`
- `src.core.base.logic.security.api_security_core.RateLimitConfig`
- `src.core.base.logic.security.api_security_core.SecurityEvent`
- `typing.Any`
- `typing.Dict`

---
*Auto-generated documentation*
