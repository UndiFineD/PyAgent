# Class Breakdown: base

**File**: `src\infrastructure\services\cloud\base.py`  
**Classes**: 6

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `InferenceRequest`

**Line**: 30  
**Methods**: 0

Standardized inference request across all cloud providers.

[TIP] **Suggested split**: Move to `inferencerequest.py`

---

### 2. `InferenceResponse`

**Line**: 60  
**Methods**: 0

Standardized inference response from cloud providers.

[TIP] **Suggested split**: Move to `inferenceresponse.py`

---

### 3. `CloudProviderBase`

**Line**: 95  
**Inherits**: ABC  
**Methods**: 6

Abstract base class for cloud AI provider integrations.

All cloud connectors (Gemini, Bedrock, Groq, etc.) must inherit from this
class and implement the required abstract methods.

Example:
    clas...

[TIP] **Suggested split**: Move to `cloudproviderbase.py`

---

### 4. `CloudProviderError`

**Line**: 211  
**Inherits**: Exception  
**Methods**: 1

Base exception for cloud provider errors.

[TIP] **Suggested split**: Move to `cloudprovidererror.py`

---

### 5. `RateLimitError`

**Line**: 220  
**Inherits**: CloudProviderError  
**Methods**: 1

Raised when rate limits are exceeded.

[TIP] **Suggested split**: Move to `ratelimiterror.py`

---

### 6. `AuthenticationError`

**Line**: 228  
**Inherits**: CloudProviderError  
**Methods**: 1

Raised when authentication fails.

[TIP] **Suggested split**: Move to `authenticationerror.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
