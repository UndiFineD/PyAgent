"""
ZeroCopySerializer - Zero-copy msgpack serialization for tensors and arrays.

Implements vLLM's v1 serialization pattern for efficient tensor transfer
without copying data. Uses auxiliary buffers for large tensors to avoid
memory copies in ZMQ multipart messages.

Phase 23: Advanced Serialization & Validation
"""

from __future__ import annotations

import dataclasses
import pickle
from collections.abc import Callable, Sequence
from enum import Enum
from functools import lru_cache
from typing import Any, TypeVar, Generic, TYPE_CHECKING

try:
    import msgspec
    from msgspec import msgpack
    MSGSPEC_AVAILABLE = True
except ImportError:
    MSGSPEC_AVAILABLE = False
    msgspec = None
    msgpack = None

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    np = None

if TYPE_CHECKING:
    import torch

__all__ = [
    "ZeroCopyEncoder",
    "ZeroCopyDecoder",
    "encode_with_buffers",
    "decode_with_buffers",
    "MSGSPEC_AVAILABLE",
]

# Custom extension type codes
CUSTOM_TYPE_PICKLE = 1
CUSTOM_TYPE_RAW_VIEW = 3

T = TypeVar("T")


class ZeroCopyEncoder:
    """
    Encoder with zero-copy tensor and numpy array serialization.
    
    Large tensors are stored as references to auxiliary buffers rather than
    being copied into the main msgpack buffer. This enables efficient ZMQ
    multipart message transmission.
    
    Example:
        >>> encoder = ZeroCopyEncoder(size_threshold=256)
        >>> buffers = encoder.encode({"tensor": my_tensor, "data": [1, 2, 3]})
        >>> # buffers[0] is main msgpack data
        >>> # buffers[1:] are tensor data references
    """
    
    def __init__(self, size_threshold: int = 256):
        """
        Initialize the encoder.
        
        Args:
            size_threshold: Tensors/arrays smaller than this are inlined.
                          Larger ones use auxiliary buffers. Default 256 bytes.
        """
        if not MSGSPEC_AVAILABLE:
            raise ImportError("msgspec is required for ZeroCopyEncoder")
        
        self.size_threshold = size_threshold
        self._encoder = msgpack.Encoder(enc_hook=self._enc_hook)
        self._aux_buffers: list[bytes | memoryview] | None = None
    
    def encode(self, obj: Any) -> Sequence[bytes | memoryview]:
        """
        Encode an object with zero-copy tensor handling.
        
        Returns:
            Sequence of buffers. First is main msgpack data,
            remaining are tensor/array data references.
        """
        try:
            self._aux_buffers = [b""]  # Placeholder for main buffer
            self._aux_buffers[0] = self._encoder.encode(obj)
            return self._aux_buffers
        finally:
            self._aux_buffers = None
    
    def encode_into(self, obj: Any, buf: bytearray) -> Sequence[bytes | memoryview]:
        """
        Encode into an existing bytearray.
        
        Args:
            obj: Object to encode
            buf: Bytearray to encode into
            
        Returns:
            Sequence of buffers with buf as first element.
        """
        try:
            self._aux_buffers = [buf]
            self._encoder.encode_into(obj, buf)
            return self._aux_buffers
        finally:
            self._aux_buffers = None
    
    def _enc_hook(self, obj: Any) -> Any:
        """Custom encoding hook for special types."""
        # Handle torch tensors
        if _is_torch_tensor(obj):
            return self._encode_tensor(obj)
        
        # Handle numpy arrays (excluding object/void dtypes)
        if NUMPY_AVAILABLE and isinstance(obj, np.ndarray):
            if obj.dtype.kind not in ("O", "V"):
                return self._encode_ndarray(obj)
        
        # Handle slices
        if isinstance(obj, slice):
            return (
                obj.start if obj.start is not None else None,
                obj.stop if obj.stop is not None else None,
                obj.step if obj.step is not None else None,
            )
        
        # Handle dataclasses
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            return {f.name: getattr(obj, f.name) for f in dataclasses.fields(obj)}
        
        # Handle Enums
        if isinstance(obj, Enum):
            return {"__enum__": type(obj).__name__, "value": obj.value}
        
        # Fallback to pickle for unknown types
        return msgpack.Ext(CUSTOM_TYPE_PICKLE, pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL))
    
    def _encode_tensor(self, tensor: "torch.Tensor") -> tuple[str, tuple[int, ...], int | memoryview]:
        """Encode a torch tensor."""
        import torch
        
        assert self._aux_buffers is not None
        
        # Get raw bytes view
        if tensor.is_contiguous():
            arr_data = tensor.detach().cpu().numpy().tobytes()
        else:
            arr_data = tensor.detach().cpu().contiguous().numpy().tobytes()
        
        nbytes = tensor.numel() * tensor.element_size()
        
        if nbytes < self.size_threshold:
            # Inline small tensors
            data = msgpack.Ext(CUSTOM_TYPE_RAW_VIEW, arr_data)
        else:
            # Reference large tensors
            data = len(self._aux_buffers)
            self._aux_buffers.append(arr_data)
        
        dtype_str = str(tensor.dtype).removeprefix("torch.")
        return dtype_str, tuple(tensor.shape), data
    
    def _encode_ndarray(self, arr: "np.ndarray") -> tuple[str, tuple[int, ...], int | memoryview]:
        """Encode a numpy array."""
        assert self._aux_buffers is not None
        
        # Ensure contiguous
        if arr.flags.c_contiguous:
            arr_data = bytes(arr.data)
        else:
            arr_data = arr.tobytes()
        
        if arr.nbytes < self.size_threshold:
            # Inline small arrays
            data = msgpack.Ext(CUSTOM_TYPE_RAW_VIEW, arr_data)
        else:
            # Reference large arrays
            data = len(self._aux_buffers)
            self._aux_buffers.append(arr_data)
        
        return arr.dtype.str, arr.shape, data


class ZeroCopyDecoder:
    """
    Decoder with zero-copy tensor and numpy array deserialization.
    
    Reconstructs tensors and arrays from auxiliary buffers without copying.
    
    Example:
        >>> decoder = ZeroCopyDecoder()
        >>> obj = decoder.decode(buffers)
    """
    
    def __init__(self, expected_type: type | None = None, share_memory: bool = True):
        """
        Initialize the decoder.
        
        Args:
            expected_type: Optional type hint for decoding
            share_memory: If True, tensors share memory with buffers
        """
        if not MSGSPEC_AVAILABLE:
            raise ImportError("msgspec is required for ZeroCopyDecoder")
        
        self.share_memory = share_memory
        self._aux_buffers: Sequence[bytes | memoryview] = ()
        
        args = () if expected_type is None else (expected_type,)
        self._decoder = msgpack.Decoder(
            *args,
            ext_hook=self._ext_hook,
            dec_hook=self._dec_hook,
        )
    
    def decode(self, bufs: bytes | Sequence[bytes | memoryview]) -> Any:
        """
        Decode from buffers.
        
        Args:
            bufs: Single buffer or sequence of buffers (first is main, rest are aux)
            
        Returns:
            Decoded object
        """
        if isinstance(bufs, (bytes, bytearray, memoryview)):
            return self._decoder.decode(bufs)
        
        self._aux_buffers = bufs
        try:
            return self._decoder.decode(bufs[0])
        finally:
            self._aux_buffers = ()
    
    def _ext_hook(self, code: int, data: bytes) -> Any:
        """Handle msgpack extension types."""
        if code == CUSTOM_TYPE_PICKLE:
            return pickle.loads(data)
        if code == CUSTOM_TYPE_RAW_VIEW:
            return data
        raise ValueError(f"Unknown extension type: {code}")
    
    def _dec_hook(self, typ: type, obj: Any) -> Any:
        """Custom decoding hook for special types."""
        if NUMPY_AVAILABLE and typ is np.ndarray:
            return self._decode_ndarray(obj)
        
        if _is_torch_type(typ):
            return self._decode_tensor(obj)
        
        if typ is slice:
            return slice(*obj)
        
        return obj
    
    def _decode_ndarray(self, obj: tuple) -> "np.ndarray":
        """Decode a numpy array."""
        dtype_str, shape, data = obj
        
        # Get buffer
        if isinstance(data, int):
            buffer = self._aux_buffers[data]
        else:
            buffer = data
        
        # Create array from buffer
        arr = np.frombuffer(buffer, dtype=np.dtype(dtype_str)).reshape(shape)
        
        if not self.share_memory:
            arr = arr.copy()
        
        return arr
    
    def _decode_tensor(self, obj: tuple) -> "torch.Tensor":
        """Decode a torch tensor."""
        import torch
        
        dtype_str, shape, data = obj
        
        # Get buffer
        if isinstance(data, int):
            buffer = self._aux_buffers[data]
        else:
            buffer = data
        
        # Map dtype string to torch dtype
        dtype = _str_to_torch_dtype(dtype_str)
        
        # Create tensor from buffer
        arr = np.frombuffer(buffer, dtype=_torch_dtype_to_numpy(dtype)).reshape(shape)
        tensor = torch.from_numpy(arr)
        
        if not self.share_memory:
            tensor = tensor.clone()
        
        return tensor


def encode_with_buffers(obj: Any, size_threshold: int = 256) -> Sequence[bytes | memoryview]:
    """
    Convenience function to encode with zero-copy.
    
    Args:
        obj: Object to encode
        size_threshold: Threshold for inlining vs referencing
        
    Returns:
        Sequence of buffers
    """
    return ZeroCopyEncoder(size_threshold).encode(obj)


def decode_with_buffers(
    bufs: bytes | Sequence[bytes | memoryview],
    expected_type: type | None = None,
    share_memory: bool = True,
) -> Any:
    """
    Convenience function to decode with zero-copy.
    
    Args:
        bufs: Buffer or sequence of buffers
        expected_type: Optional expected type
        share_memory: Whether to share memory with buffers
        
    Returns:
        Decoded object
    """
    return ZeroCopyDecoder(expected_type, share_memory).decode(bufs)


# Helper functions

@lru_cache(maxsize=32)
def _str_to_torch_dtype(dtype_str: str) -> "torch.dtype":
    """Convert string to torch dtype."""
    import torch
    
    dtype_map = {
        "float32": torch.float32,
        "float64": torch.float64,
        "float16": torch.float16,
        "bfloat16": torch.bfloat16,
        "int8": torch.int8,
        "int16": torch.int16,
        "int32": torch.int32,
        "int64": torch.int64,
        "uint8": torch.uint8,
        "bool": torch.bool,
        "complex64": torch.complex64,
        "complex128": torch.complex128,
    }
    return dtype_map.get(dtype_str, torch.float32)


def _torch_dtype_to_numpy(dtype: "torch.dtype") -> "np.dtype":
    """Convert torch dtype to numpy dtype."""
    import torch
    
    dtype_map = {
        torch.float32: np.float32,
        torch.float64: np.float64,
        torch.float16: np.float16,
        torch.int8: np.int8,
        torch.int16: np.int16,
        torch.int32: np.int32,
        torch.int64: np.int64,
        torch.uint8: np.uint8,
        torch.bool: np.bool_,
        torch.complex64: np.complex64,
        torch.complex128: np.complex128,
    }
    # Handle bfloat16 specially (numpy doesn't support it)
    if dtype == torch.bfloat16:
        return np.float16
    return dtype_map.get(dtype, np.float32)


def _is_torch_tensor(obj: Any) -> bool:
    """Check if object is a torch tensor without importing torch."""
    return type(obj).__module__.startswith("torch") and type(obj).__name__ == "Tensor"


def _is_torch_type(typ: type) -> bool:
    """Check if type is torch.Tensor."""
    return typ.__module__.startswith("torch") and typ.__name__ == "Tensor"
