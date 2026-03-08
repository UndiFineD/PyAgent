# Class Breakdown: network_reconnaissance_core

**File**: `src\core\base\logic\core\network_reconnaissance_core.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `AssetDiscoveryResult`

**Line**: 39  
**Methods**: 0

Result of network asset discovery operations.

[TIP] **Suggested split**: Move to `assetdiscoveryresult.py`

---

### 2. `ReconnaissanceConfig`

**Line**: 53  
**Methods**: 0

Configuration for reconnaissance operations.

[TIP] **Suggested split**: Move to `reconnaissanceconfig.py`

---

### 3. `NetworkReconnaissanceCore`

**Line**: 68  
**Inherits**: BaseCore  
**Methods**: 4

Network Reconnaissance Core implementing comprehensive asset discovery patterns.

Inspired by OWASP Amass, this core provides:
- DNS enumeration and subdomain discovery
- Certificate transparency anal...

[TIP] **Suggested split**: Move to `networkreconnaissancecore.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
