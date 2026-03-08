# Class Breakdown: safety_guardrails

**File**: `src\core\base\logic\safety_guardrails.py`  
**Classes**: 11

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ValidationResult`

**Line**: 47  
**Inherits**: BaseModel  
**Methods**: 0

Result of a validation operation.

[TIP] **Suggested split**: Move to `validationresult.py`

---

### 2. `SafetyLevel`

**Line**: 55  
**Inherits**: Enum  
**Methods**: 0

Safety enforcement levels.

[TIP] **Suggested split**: Move to `safetylevel.py`

---

### 3. `ContentCategory`

**Line**: 63  
**Inherits**: Enum  
**Methods**: 0

Content categories for filtering.

[TIP] **Suggested split**: Move to `contentcategory.py`

---

### 4. `SafetyConfig`

**Line**: 74  
**Methods**: 0

Configuration for safety mechanisms.

[TIP] **Suggested split**: Move to `safetyconfig.py`

---

### 5. `InputValidator`

**Line**: 90  
**Methods**: 2

Validates and moderates input content.

[TIP] **Suggested split**: Move to `inputvalidator.py`

---

### 6. `OutputValidator`

**Line**: 191  
**Methods**: 1

Validates and filters output content.

[TIP] **Suggested split**: Move to `outputvalidator.py`

---

### 7. `RateLimiter`

**Line**: 289  
**Methods**: 1

Rate limiting for agent requests.

[TIP] **Suggested split**: Move to `ratelimiter.py`

---

### 8. `Guardrail`

**Line**: 334  
**Methods**: 2

Comprehensive guardrail system combining multiple safety mechanisms.

[TIP] **Suggested split**: Move to `guardrail.py`

---

### 9. `ResilienceDecorator`

**Line**: 428  
**Methods**: 2

Decorator for adding resilience patterns to functions.

[TIP] **Suggested split**: Move to `resiliencedecorator.py`

---

### 10. `ResearchSummary`

**Line**: 519  
**Inherits**: BaseModel  
**Methods**: 2

Schema for research summary outputs.

[TIP] **Suggested split**: Move to `researchsummary.py`

---

### 11. `CodeReviewResult`

**Line**: 540  
**Inherits**: BaseModel  
**Methods**: 0

Schema for code review outputs.

[TIP] **Suggested split**: Move to `codereviewresult.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
