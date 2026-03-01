# Class Breakdown: http_client

**File**: `src\infrastructure\swarm\network\http_client.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `HTTPClient`

**Line**: 32  
**Inherits**: HTTPConnection  
**Methods**: 0

Alias for HTTPConnection with sync-focused interface.

[TIP] **Suggested split**: Move to `httpclient.py`

---

### 2. `AsyncHTTPClient`

**Line**: 38  
**Inherits**: HTTPConnection  
**Methods**: 0

Alias for HTTPConnection with async-focused interface.

[TIP] **Suggested split**: Move to `asynchttpclient.py`

---

### 3. `RetryableHTTPClient`

**Line**: 44  
**Inherits**: HTTPConnection, RetryHTTPMixin  
**Methods**: 1

HTTP client with automatic retry on failures.

[TIP] **Suggested split**: Move to `retryablehttpclient.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
