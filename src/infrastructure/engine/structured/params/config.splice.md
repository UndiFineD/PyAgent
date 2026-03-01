# Class Breakdown: config

**File**: `src\infrastructure\engine\structured\params\config.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `StructuredOutputConfig`

**Line**: 31  
**Methods**: 4

Complete structured output configuration.

Inspired by vLLM's GuidedDecodingParams.

[TIP] **Suggested split**: Move to `structuredoutputconfig.py`

---

### 2. `ValidationResult`

**Line**: 139  
**Methods**: 2

Result of structured output validation.

[TIP] **Suggested split**: Move to `validationresult.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
