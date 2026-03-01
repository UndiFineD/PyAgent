# Class Breakdown: subdomain_permutation_core

**File**: `src\core\base\logic\core\subdomain_permutation_core.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `PermutationResult`

**Line**: 30  
**Methods**: 0

Result of subdomain permutation generation.

[TIP] **Suggested split**: Move to `permutationresult.py`

---

### 2. `PermutationConfig`

**Line**: 41  
**Methods**: 0

Configuration for permutation generation.

[TIP] **Suggested split**: Move to `permutationconfig.py`

---

### 3. `SubdomainPermutationCore`

**Line**: 51  
**Inherits**: BaseCore  
**Methods**: 12

Subdomain Permutation Core implementing intelligent wordlist generation.

Inspired by AlterX, this core provides:
- DSL-based pattern generation
- Automatic word enrichment from input domains
- Cluste...

[TIP] **Suggested split**: Move to `subdomainpermutationcore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
