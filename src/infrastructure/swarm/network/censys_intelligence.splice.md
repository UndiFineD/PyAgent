# Class Breakdown: censys_intelligence

**File**: `src\infrastructure\swarm\network\censys_intelligence.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `CensysResult`

**Line**: 28  
**Methods**: 0

[TIP] **Suggested split**: Move to `censysresult.py`

---

### 2. `CensysIntelligence`

**Line**: 34  
**Methods**: 1

Integrates functionality from 0xSojalSec-censeye and 0xSojalSec-censys-subdomain-finder.
Provides subdomain enumeration and deep host enrichment via Censys API.

[TIP] **Suggested split**: Move to `censysintelligence.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
