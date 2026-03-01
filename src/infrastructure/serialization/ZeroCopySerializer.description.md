# ZeroCopySerializer

**File**: `src\infrastructure\serialization\ZeroCopySerializer.py`  
**Type**: Python Module  
**Summary**: 2 classes, 6 functions, 19 imports  
**Lines**: 395  
**Complexity**: 18 (moderate)

## Overview

ZeroCopySerializer - Zero-copy msgpack serialization for tensors and arrays.

Implements vLLM's v1 serialization pattern for efficient tensor transfer
without copying data. Uses auxiliary buffers for large tensors to avoid
memory copies in ZMQ multipart messages.

Phase 23: Advanced Serialization & Validation

## Classes (2)

### `ZeroCopyEncoder`

Encoder with zero-copy tensor and numpy array serialization.

Large tensors are stored as references to auxiliary buffers rather than
being copied into the main msgpack buffer. This enables efficient ZMQ
multipart message transmission.

Example:
    >>> encoder = ZeroCopyEncoder(size_threshold=256)
    >>> buffers = encoder.encode({"tensor": my_tensor, "data": [1, 2, 3]})
    >>> # buffers[0] is main msgpack data
    >>> # buffers[1:] are tensor data references

**Methods** (6):
- `__init__(self, size_threshold)`
- `encode(self, obj)`
- `encode_into(self, obj, buf)`
- `_enc_hook(self, obj)`
- `_encode_tensor(self, tensor)`
- `_encode_ndarray(self, arr)`

### `ZeroCopyDecoder`

Decoder with zero-copy tensor and numpy array deserialization.

Reconstructs tensors and arrays from auxiliary buffers without copying.

Example:
    >>> decoder = ZeroCopyDecoder()
    >>> obj = decoder.decode(buffers)

**Methods** (6):
- `__init__(self, expected_type, share_memory)`
- `decode(self, bufs)`
- `_ext_hook(self, code, data)`
- `_dec_hook(self, typ, obj)`
- `_decode_ndarray(self, obj)`
- `_decode_tensor(self, obj)`

## Functions (6)

### `encode_with_buffers(obj, size_threshold)`

Convenience function to encode with zero-copy.

Args:
    obj: Object to encode
    size_threshold: Threshold for inlining vs referencing
    
Returns:
    Sequence of buffers

### `decode_with_buffers(bufs, expected_type, share_memory)`

Convenience function to decode with zero-copy.

Args:
    bufs: Buffer or sequence of buffers
    expected_type: Optional expected type
    share_memory: Whether to share memory with buffers
    
Returns:
    Decoded object

### `_str_to_torch_dtype(dtype_str)`

Convert string to torch dtype.

### `_torch_dtype_to_numpy(dtype)`

Convert torch dtype to numpy dtype.

### `_is_torch_tensor(obj)`

Check if object is a torch tensor without importing torch.

### `_is_torch_type(typ)`

Check if type is torch.Tensor.

## Dependencies

**Imports** (19):
- `__future__.annotations`
- `collections.abc.Callable`
- `collections.abc.Sequence`
- `dataclasses`
- `enum.Enum`
- `functools.lru_cache`
- `msgspec`
- `msgspec.msgpack`
- `numpy`
- `pickle`
- `torch`
- `typing.Any`
- `typing.Generic`
- `typing.TYPE_CHECKING`
- `typing.TypeVar`
- ... and 4 more

---
*Auto-generated documentation*
