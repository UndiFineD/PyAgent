# Class Breakdown: fast_serializer

**File**: `src\infrastructure\storage\serialization\fast_serializer.py`  
**Classes**: 9

This file contains multiple classes. Consider splitting into separate modules for better maintainability.

## Classes Overview

### 1. `SerializationFormat`

**Line**: 38  
**Inherits**: Enum  
**Methods**: 0

Supported serialization formats.

[TIP] **Suggested split**: Move to `serializationformat.py`

---

### 2. `SerializerStats`

**Line**: 49  
**Methods**: 3

Statistics for serializer operations.

[TIP] **Suggested split**: Move to `serializerstats.py`

---

### 3. `Serializer`

**Line**: 87  
**Inherits**: ABC  
**Methods**: 7

Abstract base class for serializers.

[TIP] **Suggested split**: Move to `serializer.py`

---

### 4. `JSONSerializer`

**Line**: 163  
**Inherits**: Serializer  
**Methods**: 4

JSON serializer with optional compression.

[TIP] **Suggested split**: Move to `jsonserializer.py`

---

### 5. `PickleSerializer`

**Line**: 215  
**Inherits**: Serializer  
**Methods**: 4

Pickle serializer with protocol selection.

[TIP] **Suggested split**: Move to `pickleserializer.py`

---

### 6. `MsgPackSerializer`

**Line**: 259  
**Inherits**: Serializer  
**Methods**: 5

MessagePack serializer for fast, compact serialization.

Falls back to JSON if msgpack not installed.

[TIP] **Suggested split**: Move to `msgpackserializer.py`

---

### 7. `CBORSerializer`

**Line**: 326  
**Inherits**: Serializer  
**Methods**: 5

CBOR serializer for cross-language compatibility.

Falls back to JSON if cbor2 not installed.

[TIP] **Suggested split**: Move to `cborserializer.py`

---

### 8. `BinarySerializer`

**Line**: 372  
**Inherits**: Serializer  
**Methods**: 6

Custom binary serializer for primitive types.

Extremely fast for simple types (int, float, str, bytes).

[TIP] **Suggested split**: Move to `binaryserializer.py`

---

### 9. `SerializerRegistry`

**Line**: 507  
**Methods**: 8

Registry for serializers with format negotiation.

[TIP] **Suggested split**: Move to `serializerregistry.py`

---

## Refactoring Strategy

1. Create separate files for each class
2. Update imports in dependent modules
3. Create __init__.py to maintain backwards compatibility
4. Run tests to ensure functionality is preserved

---
*Auto-generated class breakdown*
