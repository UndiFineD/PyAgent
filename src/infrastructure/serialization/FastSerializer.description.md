# FastSerializer

**File**: `src\infrastructure\serialization\FastSerializer.py`  
**Type**: Python Module  
**Summary**: 9 classes, 7 functions, 25 imports  
**Lines**: 620  
**Complexity**: 49 (complex)

## Overview

Fast Serialization with msgpack and CBOR support.

Phase 19: Beyond vLLM - Performance Patterns
High-performance serialization for inter-process communication.

## Classes (9)

### `SerializationFormat`

**Inherits from**: Enum

Supported serialization formats.

### `SerializerStats`

Statistics for serializer operations.

**Methods** (3):
- `avg_serialize_time_us(self)`
- `avg_deserialize_time_us(self)`
- `to_dict(self)`

### `Serializer`

**Inherits from**: ABC

Abstract base class for serializers.

**Methods** (7):
- `__init__(self)`
- `_serialize(self, obj)`
- `_deserialize(self, data)`
- `format(self)`
- `serialize(self, obj)`
- `deserialize(self, data)`
- `stats(self)`

### `JSONSerializer`

**Inherits from**: Serializer

JSON serializer with optional compression.

**Methods** (4):
- `__init__(self, indent, ensure_ascii, compress, compress_level)`
- `format(self)`
- `_serialize(self, obj)`
- `_deserialize(self, data)`

### `PickleSerializer`

**Inherits from**: Serializer

Pickle serializer with protocol selection.

**Methods** (4):
- `__init__(self, protocol, compress, compress_level)`
- `format(self)`
- `_serialize(self, obj)`
- `_deserialize(self, data)`

### `MsgPackSerializer`

**Inherits from**: Serializer

MessagePack serializer for fast, compact serialization.

Falls back to JSON if msgpack not installed.

**Methods** (5):
- `__init__(self, use_bin_type, raw)`
- `format(self)`
- `is_available(self)`
- `_serialize(self, obj)`
- `_deserialize(self, data)`

### `CBORSerializer`

**Inherits from**: Serializer

CBOR serializer for cross-language compatibility.

Falls back to JSON if cbor2 not installed.

**Methods** (5):
- `__init__(self)`
- `format(self)`
- `is_available(self)`
- `_serialize(self, obj)`
- `_deserialize(self, data)`

### `BinarySerializer`

**Inherits from**: Serializer

Custom binary serializer for primitive types.

Extremely fast for simple types (int, float, str, bytes).

**Methods** (6):
- `__init__(self)`
- `format(self)`
- `_serialize(self, obj)`
- `_encode_value(self, obj, parts)`
- `_deserialize(self, data)`
- `_decode_value(self, data, offset)`

### `SerializerRegistry`

Registry for serializers with format negotiation.

**Methods** (8):
- `__init__(self)`
- `get(self, format)`
- `register(self, serializer)`
- `set_default(self, format)`
- `default(self)`
- `serialize(self, obj, format)`
- `deserialize(self, data, format)`
- `get_fastest_available(self)`

## Functions (7)

### `get_serializer_registry()`

Get global serializer registry.

### `fast_serialize(obj)`

Serialize using fastest available format.

### `fast_deserialize(data)`

Deserialize using fastest available format.

### `to_json(obj, compress)`

Serialize to JSON bytes.

### `from_json(data, compressed)`

Deserialize from JSON bytes.

### `to_msgpack(obj)`

Serialize to MessagePack bytes.

### `from_msgpack(data)`

Deserialize from MessagePack bytes.

## Dependencies

**Imports** (25):
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `cbor2`
- `dataclasses.dataclass`
- `dataclasses.field`
- `enum.Enum`
- `enum.auto`
- `json`
- `msgpack`
- `pickle`
- `struct`
- `threading`
- `time`
- `typing.Any`
- ... and 10 more

---
*Auto-generated documentation*
