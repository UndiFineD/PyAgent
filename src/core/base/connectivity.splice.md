# Class Breakdown: connectivity

**File**: `src\core\base\connectivity.py`  
**Classes**: 2

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `BinaryTransport`

**Line**: 30  
**Methods**: 2

Handles binary serialization and compression for agent communication.
Utilizes MessagePack and Zstd for optimal performance.

[TIP] **Suggested split**: Move to `binarytransport.py`

---

### 2. `HeartbeatSignal`

**Line**: 79  
**Methods**: 3

Specialized structure for high-frequency heartbeat signals.
Optimized for BinaryTransport.

[TIP] **Suggested split**: Move to `heartbeatsignal.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
