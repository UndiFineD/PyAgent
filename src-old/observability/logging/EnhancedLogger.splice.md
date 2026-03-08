# Class Breakdown: EnhancedLogger

**File**: `src\observability\logging\EnhancedLogger.py`  
**Classes**: 3

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `LogScopeEnum`

**Line**: 23  
**Inherits**: Enum  
**Methods**: 0

Enum for log scope types.

[TIP] **Suggested split**: Move to `logscopeenum.py`

---

### 2. `EnhancedLoggerAdapter`

**Line**: 216  
**Inherits**: LoggerAdapter  
**Methods**: 7

Logger adapter providing enhanced logging methods.

Provides a clean API without patching the underlying logger.

[TIP] **Suggested split**: Move to `enhancedloggeradapter.py`

---

### 3. `EnhancedLogger`

**Line**: 340  
**Inherits**: Logger  
**Methods**: 4

Type hint class for enhanced logger.

Not for direct instantiation - use init_logger() or patch_logger().

[TIP] **Suggested split**: Move to `enhancedlogger.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
