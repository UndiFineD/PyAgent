#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/mixins/security_mixin.description.md

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
## Source: src-old/core/base/mixins/security_mixin.improvements.md

# Improvements for security_mixin

**File**: `src\core\base\mixins\security_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 52 lines (small)  
**Complexity**: 4 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `security_mixin_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module: security_mixin
Security mixin for BaseAgent, implementing API security patterns for agent communications.
"""


from typing import Any, Dict

from src.core.base.logic.security.api_security_core import (
    APISecurityCore, AgentCredentials, RateLimitConfig, SecurityEvent
)


class SecurityMixin:
    """Mixin providing API security features for agent communications."""

    def __init__(self, **kwargs: Any) -> None:
        self.api_security = APISecurityCore()
        self.agent_credentials: Dict[str, AgentCredentials] = {}

    def register_agent_credentials(self, creds: AgentCredentials) -> None:
        """Register credentials for an agent."""
        self.api_security.authenticator.register_agent(creds)
        self.agent_credentials[creds.agent_id] = creds

    def configure_rate_limiting(self, config: RateLimitConfig) -> None:
        """Configure rate limiting."""
        self.api_security.rate_limiter = self.api_security.rate_limiter.__class__(config)

    async def secure_agent_communication(self, sender_id: str, receiver_id: str,
                                       message: Dict[str, Any], token: str) -> Dict[str, Any]:
        """Secure communication between agents."""
        return await self.api_security.secure_communication(sender_id, receiver_id, message, token)

    def log_security_event(self, event: SecurityEvent) -> None:
        """Log a security event."""
        self.api_security.error_handler.log_security_event(event)
