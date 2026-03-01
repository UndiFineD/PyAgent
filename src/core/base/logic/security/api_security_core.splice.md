# Class Breakdown: api_security_core

**File**: `src\core\base\logic\security\api_security_core.py`  
**Classes**: 8

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AgentCredentials`

**Line**: 36  
**Methods**: 0

Credentials for agent authentication.

[TIP] **Suggested split**: Move to `agentcredentials.py`

---

### 2. `RateLimitConfig`

**Line**: 45  
**Methods**: 0

Configuration for rate limiting.

[TIP] **Suggested split**: Move to `ratelimitconfig.py`

---

### 3. `SecurityEvent`

**Line**: 52  
**Methods**: 0

Security event for logging.

[TIP] **Suggested split**: Move to `securityevent.py`

---

### 4. `InputValidator`

**Line**: 61  
**Methods**: 3

Input validation and sanitization for agent communications.

[TIP] **Suggested split**: Move to `inputvalidator.py`

---

### 5. `RateLimiter`

**Line**: 106  
**Methods**: 2

Rate limiting for agent communications.

[TIP] **Suggested split**: Move to `ratelimiter.py`

---

### 6. `Authenticator`

**Line**: 134  
**Methods**: 4

Authentication and authorization for agents.

[TIP] **Suggested split**: Move to `authenticator.py`

---

### 7. `ErrorHandler`

**Line**: 165  
**Methods**: 2

Error handling and masking for security.

[TIP] **Suggested split**: Move to `errorhandler.py`

---

### 8. `APISecurityCore`

**Line**: 187  
**Methods**: 1

Core class for API security patterns in agent communications.

[TIP] **Suggested split**: Move to `apisecuritycore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
