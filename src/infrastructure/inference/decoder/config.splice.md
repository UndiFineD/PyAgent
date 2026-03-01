# Class Breakdown: config

**File**: `src\infrastructure\inference\decoder\config.py`  
**Classes**: 5

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SpecMethod`

**Line**: 8  
**Inherits**: str, Enum  
**Methods**: 0

Speculative decoding method.

[TIP] **Suggested split**: Move to `specmethod.py`

---

### 2. `SpeculativeConfig`

**Line**: 18  
**Methods**: 1

Configuration for speculative decoding.

[TIP] **Suggested split**: Move to `speculativeconfig.py`

---

### 3. `DraftProposal`

**Line**: 50  
**Methods**: 2

A batch of draft tokens proposed by speculator.

[TIP] **Suggested split**: Move to `draftproposal.py`

---

### 4. `VerificationResult`

**Line**: 67  
**Methods**: 2

Result of verifying draft tokens against target model.

[TIP] **Suggested split**: Move to `verificationresult.py`

---

### 5. `SpecDecodingMetrics`

**Line**: 89  
**Methods**: 8

Metrics for speculative decoding performance.

[TIP] **Suggested split**: Move to `specdecodingmetrics.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
