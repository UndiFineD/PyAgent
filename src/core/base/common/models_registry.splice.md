# Class Breakdown: models_registry

**File**: `src\core\base\common\models_registry.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `ModelSpec`

**Line**: 22  
**Inherits**: TypedDict  
**Methods**: 0

[TIP] **Suggested split**: Move to `modelspec.py`

---

### 2. `ProviderRegistry`

**Line**: 30  
**Methods**: 2

Central repository for 65+ LLM/multimodal providers and their pricing.

[TIP] **Suggested split**: Move to `providerregistry.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
