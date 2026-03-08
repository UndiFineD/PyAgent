# api_security_core

**File**: `src\core\base\logic\security\api_security_core.py`  
**Type**: Python Module  
**Summary**: 8 classes, 0 functions, 15 imports  
**Lines**: 255  
**Complexity**: 12 (moderate)

## Overview

Module: api_security_core
Implements API security patterns for agent communications, inspired by 31-days-of-API-Security-Tips.
Provides input validation, rate limiting, authentication, BOLA prevention, error handling, and logging.

## Classes (8)

### `AgentCredentials`

Credentials for agent authentication.

### `RateLimitConfig`

Configuration for rate limiting.

### `SecurityEvent`

Security event for logging.

### `InputValidator`

Input validation and sanitization for agent communications.

**Methods** (3):
- `sanitize_input(input_data)`
- `validate_agent_id(agent_id)`
- `validate_resource_access(agent_id, resource_id, credentials)`

### `RateLimiter`

Rate limiting for agent communications.

**Methods** (2):
- `__init__(self, config)`
- `is_allowed(self, agent_id)`

### `Authenticator`

Authentication and authorization for agents.

**Methods** (4):
- `__init__(self)`
- `register_agent(self, creds)`
- `authenticate(self, agent_id, token)`
- `authorize(self, creds, action)`

### `ErrorHandler`

Error handling and masking for security.

**Methods** (2):
- `mask_error(error)`
- `log_security_event(event)`

### `APISecurityCore`

Core class for API security patterns in agent communications.

**Methods** (1):
- `__init__(self)`

## Dependencies

**Imports** (15):
- `__future__.annotations`
- `asyncio`
- `collections.defaultdict`
- `dataclasses.dataclass`
- `dataclasses.field`
- `hashlib`
- `hmac`
- `logging`
- `re`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.Set`

---
*Auto-generated documentation*
