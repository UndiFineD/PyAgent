# Class Breakdown: config

**File**: `src\infrastructure\scheduling\disaggregated\config.py`  
**Classes**: 4

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `InstanceInfo`

**Line**: 11  
**Methods**: 3

Information about a vLLM instance.

Inspired by vLLM's proxy server patterns.

[TIP] **Suggested split**: Move to `instanceinfo.py`

---

### 2. `DCPConfig`

**Line**: 55  
**Methods**: 0

Configuration for disaggregated prefill-decode.

Inspired by vLLM's kv_transfer configuration.

[TIP] **Suggested split**: Move to `dcpconfig.py`

---

### 3. `KVTransferParams`

**Line**: 91  
**Methods**: 2

Parameters for KV cache transfer between instances.

Inspired by vLLM's kv_transfer_params dict structure.

[TIP] **Suggested split**: Move to `kvtransferparams.py`

---

### 4. `ScheduledRequest`

**Line**: 149  
**Methods**: 0

A request scheduled for processing.

[TIP] **Suggested split**: Move to `scheduledrequest.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
