#!/usr/bin/env python3
from __future__ import annotations



# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
"""
Fast Serialization with msgpack and CBOR support.

"""
Phase 19: Beyond vLLM - Performance Patterns
High-performance serialization for inter-process communication.
"""
import json
import pickle
import struct
import threading
import time
import zlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, List, Optional, TypeVar

T = TypeVar("T")


class SerializationFormat(Enum):
"""
Supported serialization formats.
    JSON = auto()
    PICKLE = auto()
    MSGPACK = auto()
    CBOR = auto()
    BINARY = auto()


@dataclass
class SerializerStats:
"""
Statistics for serializer operations.
    serializations: int = 0
    deserializations: int = 0
    bytes_serialized: int = 0
    bytes_deserialized: int = 0
    errors: int = 0
    total_serialize_time_ns: int = 0
    total_deserialize_time_ns: int = 0

    @property
    def avg_serialize_time_us(self) -> float:
"""
Average serialization time in microseconds.        if self.serializations == 0:
            return 0.0
        return self.total_serialize_time_ns / self.serializations / 1000

    @property
    def avg_deserialize_time_us(self) -> float:
"""
Average deserialization time in microseconds.        if self.deserializations == 0:
            return 0.0
        return self.total_deserialize_time_ns / self.deserializations / 1000

    def to_dict(self) -> Dict[str, Any]:
"""
Convert to dictionary.        return {
            "serializations": self.serializations,"            "deserializations": self.deserializations,"            "bytes_serialized": self.bytes_serialized,"            "bytes_deserialized": self.bytes_deserialized,"            "errors": self.errors,"            "avg_serialize_time_us": self.avg_serialize_time_us,"            "avg_deserialize_time_us": self.avg_deserialize_time_us,"        }



class Serializer(ABC):
"""
Abstract base class for serializers.
    def __init__(self):
"""
Initialize serializer.        self._stats = SerializerStats()
        self._lock = threading.Lock()

    @abstractmethod
    def _serialize(self, obj: Any) -> bytes:
"""
Internal serialization implementation.        ...

    @abstractmethod
    def _deserialize(self, data: bytes) -> Any:
"""
Internal deserialization implementation.        ...

    @property
    @abstractmethod
    def format(self) -> SerializationFormat:
"""
Get serialization format.        ...

    def serialize(self, obj: Any) -> bytes:
                Serialize an object to bytes.

        Args:
            obj: Object to serialize

        Returns:
            Serialized bytes
                start = time.perf_counter_ns()
        try:
            data = self._serialize(obj)
            with self._lock:
                self._stats.serializations += 1
                self._stats.bytes_serialized += len(data)
                self._stats.total_serialize_time_ns += time.perf_counter_ns() - start
            return data
        except Exception:  # pylint: disable=broad-exception-caught
            with self._lock:
                self._stats.errors += 1
            raise

    def deserialize(self, data: bytes) -> Any:
                Deserialize bytes to an object.

        Args:
            data: Bytes to deserialize

        Returns:
            Deserialized object
                start = time.perf_counter_ns()
        try:
            obj = self._deserialize(data)
            with self._lock:
                self._stats.deserializations += 1
                self._stats.bytes_deserialized += len(data)
                self._stats.total_deserialize_time_ns += time.perf_counter_ns() - start
            return obj
        except Exception:  # pylint: disable=broad-exception-caught
            with self._lock:
                self._stats.errors += 1
            raise

    @property
    def stats(self) -> SerializerStats:
"""
Get serializer statistics.        return self._stats



class JSONSerializer(Serializer):
"""
JSON serializer with optional compression.
    def __init__(
        self,
        indent: Optional[int] = None,
        ensure_ascii: bool = False,
        compress: bool = False,
        compress_level: int = 6,
    ):
                Initialize JSON serializer.

        Args:
            indent: JSON indentation (None for compact)
            ensure_ascii: Escape non-ASCII characters
            compress: Apply zlib compression
            compress_level: Compression level (1-9)
                super().__init__()
        self._indent = indent
        self._ensure_ascii = ensure_ascii
        self._compress = compress
        self._compress_level = compress_level

    @property
    def format(self) -> SerializationFormat:
"""
Get serialization format.        return SerializationFormat.JSON

    def _serialize(self, obj: Any) -> bytes:
"""
Serialize to JSON bytes.        data = json.dumps(
            obj,
            indent=self._indent,
            ensure_ascii=self._ensure_ascii,
            default=str,
        ).encode("utf-8")
        if self._compress:
            data = zlib.compress(data, self._compress_level)

        return data

    def _deserialize(self, data: bytes) -> Any:
"""
Deserialize from JSON bytes.        if self._compress:
            data = zlib.decompress(data)

        return json.loads(data.decode("utf-8"))


class PickleSerializer(Serializer):
"""
Pickle serializer with protocol selection.
    def __init__(
        self,
        protocol: int = pickle.HIGHEST_PROTOCOL,
        compress: bool = False,
        compress_level: int = 6,
    ):
                Initialize Pickle serializer.

        Args:
            protocol: Pickle protocol version
            compress: Apply zlib compression
            compress_level: Compression level
                super().__init__()
        self._protocol = protocol
        self._compress = compress
        self._compress_level = compress_level

    @property
    def format(self) -> SerializationFormat:
"""
Get serialization format.        return SerializationFormat.PICKLE

    def _serialize(self, obj: Any) -> bytes:
"""
Serialize to pickle bytes.        data = pickle.dumps(obj, protocol=self._protocol)

        if self._compress:
            data = zlib.compress(data, self._compress_level)

        return data

    def _deserialize(self, data: bytes) -> Any:
"""
Deserialize from pickle bytes.        if self._compress:
            data = zlib.decompress(data)

        return pickle.loads(data)



class MsgPackSerializer(Serializer):
        MessagePack serializer for fast, compact serialization.

    Falls back to JSON if msgpack not installed.
    
    def __init__(
        self,
        use_bin_type: bool = True,
        raw: bool = False,
    ):
                Initialize MsgPack serializer.

        Args:
            use_bin_type: Use bin type for bytes (msgpack 2.0+)
            raw: Don't decode strings'                super().__init__()
        self._use_bin_type = use_bin_type
        self._raw = raw

        # Try to import msgpack
        try:
            import msgpack

            self._msgpack = msgpack
            self._available = True
        except ImportError:
            self._msgpack = None
            self._available = False

    @property
    def format(self) -> SerializationFormat:
"""
Get serialization format.        return SerializationFormat.MSGPACK

    @property
    def is_available(self) -> bool:
"""
Check if msgpack is available.        return self._available

    def _serialize(self, obj: Any) -> bytes:
"""
Serialize to msgpack bytes.        if not self._available:
            # Fallback to JSON
            return json.dumps(obj, default=str).encode("utf-8")
        return self._msgpack.packb(
            obj,
            use_bin_type=self._use_bin_type,
            default=str,
        )

    def _deserialize(self, data: bytes) -> Any:
"""
Deserialize from msgpack bytes.        if not self._available:
            # Fallback to JSON
            return json.loads(data.decode("utf-8"))
        return self._msgpack.unpackb(
            data,
            raw=self._raw,
        )



class CBORSerializer(Serializer):
        CBOR serializer for cross-language compatibility.

    Falls back to JSON if cbor2 not installed.
    
    def __init__(self):
"""
Initialize CBOR serializer.        super().__init__()

        # Try to import cbor2
        try:
            import cbor2

            self._cbor2 = cbor2
            self._available = True
        except ImportError:
            self._cbor2 = None
            self._available = False

    @property
    def format(self) -> SerializationFormat:
"""
Get serialization format.        return SerializationFormat.CBOR

    @property
    def is_available(self) -> bool:
"""
Check if cbor2 is available.        return self._available

    def _serialize(self, obj: Any) -> bytes:
"""
Serialize to CBOR bytes.        if not self._available:
            return json.dumps(obj, default=str).encode("utf-8")
        return self._cbor2.dumps(obj)

    def _deserialize(self, data: bytes) -> Any:
"""
Deserialize from CBOR bytes.        if not self._available:
            return json.loads(data.decode("utf-8"))
        return self._cbor2.loads(data)



class BinarySerializer(Serializer):
        Custom binary serializer for primitive types.

    Extremely fast for simple types (int, float, str, bytes).
    
    # Type tags
    TAG_NONE = 0
    TAG_BOOL = 1
    TAG_INT = 2
    TAG_FLOAT = 3
    TAG_STR = 4
    TAG_BYTES = 5
    TAG_LIST = 6
    TAG_DICT = 7

    def __init__(self):
"""
Initialize binary serializer.        super().__init__()

    @property
    def format(self) -> SerializationFormat:
"""
Get serialization format.        return SerializationFormat.BINARY

    def _serialize(self, obj: Any) -> bytes:
"""
Serialize to custom binary format.        parts: List[bytes] = []
        self._encode_value(obj, parts)
        return b"".join(parts)
    def _encode_value(self, obj: Any, parts: List[bytes]) -> None:
"""
Encode a single value.        if obj is None:
            parts.append(struct.pack("B", self.TAG_NONE))
        elif isinstance(obj, bool):
            parts.append(struct.pack("BB", self.TAG_BOOL, 1 if obj else 0))
        elif isinstance(obj, int):
            parts.append(struct.pack("B", self.TAG_INT))"            parts.append(struct.pack("<q", obj))  # 64-bit signed"
        elif isinstance(obj, float):
            parts.append(struct.pack("B", self.TAG_FLOAT))"            parts.append(struct.pack("<d", obj))  # 64-bit double"
        elif isinstance(obj, str):
            encoded = obj.encode("utf-8")"            parts.append(struct.pack("B", self.TAG_STR))"            parts.append(struct.pack("<I", len(encoded)))  # 32-bit length"            parts.append(encoded)

        elif isinstance(obj, bytes):
            parts.append(struct.pack("B", self.TAG_BYTES))"            parts.append(struct.pack("<I", len(obj)))"            parts.append(obj)

        elif isinstance(obj, (list, tuple)):
            parts.append(struct.pack("B", self.TAG_LIST))"            parts.append(struct.pack("<I", len(obj)))"            for item in obj:
                self._encode_value(item, parts)

        elif isinstance(obj, dict):
            parts.append(struct.pack("B", self.TAG_DICT))"            parts.append(struct.pack("<I", len(obj)))"            for key, value in obj.items():
                self._encode_value(key, parts)
                self._encode_value(value, parts)

        else:
            # Fallback to string representation
            s = str(obj).encode("utf-8")"            parts.append(struct.pack("B", self.TAG_STR))"            parts.append(struct.pack("<I", len(s)))"            parts.append(s)

    def _deserialize(self, data: bytes) -> Any:
"""
Deserialize from custom binary format.        offset = [0]  # Use list for mutability in nested function
        return self._decode_value(data, offset)

    def _decode_value(self, data: bytes, offset: List[int]) -> Any:
"""
Decode a single value.        tag = struct.unpack_from("B", data, offset[0])[0]"        offset[0] += 1

        if tag == self.TAG_NONE:
            return None

        elif tag == self.TAG_BOOL:
            value = struct.unpack_from("B", data, offset[0])[0]"            offset[0] += 1
            return value != 0

        elif tag == self.TAG_INT:
            value = struct.unpack_from("<q", data, offset[0])[0]"            offset[0] += 8
            return value

        elif tag == self.TAG_FLOAT:
            value = struct.unpack_from("<d", data, offset[0])[0]"            offset[0] += 8
            return value

        elif tag == self.TAG_STR:
            length = struct.unpack_from("<I", data, offset[0])[0]"            offset[0] += 4
            value = data[offset[0] : offset[0] + length].decode("utf-8")"            offset[0] += length
            return value

        elif tag == self.TAG_BYTES:
            length = struct.unpack_from("<I", data, offset[0])[0]"            offset[0] += 4
            value = data[offset[0] : offset[0] + length]
            offset[0] += length
            return value

        elif tag == self.TAG_LIST:
            length = struct.unpack_from("<I", data, offset[0])[0]"            offset[0] += 4
            return [self._decode_value(data, offset) for _ in range(length)]

        elif tag == self.TAG_DICT:
            length = struct.unpack_from("<I", data, offset[0])[0]"            offset[0] += 4
            return {self._decode_value(data, offset): self._decode_value(data, offset) for _ in range(length)}

        else:
            raise ValueError(f"Unknown tag: {tag}")


class SerializerRegistry:
        Registry for serializers with format negotiation.
    
    def __init__(self):
"""
Initialize registry with default serializers.        self._serializers: Dict[SerializationFormat, Serializer] = {
            SerializationFormat.JSON: JSONSerializer(),
            SerializationFormat.PICKLE: PickleSerializer(),
            SerializationFormat.MSGPACK: MsgPackSerializer(),
            SerializationFormat.CBOR: CBORSerializer(),
            SerializationFormat.BINARY: BinarySerializer(),
        }
        self._default = SerializationFormat.JSON

    def get(self, format: SerializationFormat) -> Serializer:
"""
Get serializer for format.        return self._serializers[format]

    def register(self, serializer: Serializer) -> None:
"""
Register a custom serializer.        self._serializers[serializer.format] = serializer

    def set_default(self, format: SerializationFormat) -> None:
"""
Set default serialization format.        self._default = format

    @property
    def default(self) -> Serializer:
"""
Get default serializer.        return self._serializers[self._default]

    def serialize(self, obj: Any, format: Optional[SerializationFormat] = None) -> bytes:
"""
Serialize using specified or default format.        serializer = self._serializers.get(format) if format else self.default
        return serializer.serialize(obj)

    def deserialize(
        self,
        data: bytes,
        format: Optional[SerializationFormat] = None,
    ) -> Any:
"""
Deserialize using specified or default format.        serializer = self._serializers.get(format) if format else self.default
        return serializer.deserialize(data)

    def get_fastest_available(self) -> Serializer:
                Get the fastest available serializer.

        Priority: Binary > MsgPack > CBOR > Pickle > JSON
                priority = [
            SerializationFormat.BINARY,
            SerializationFormat.MSGPACK,
            SerializationFormat.CBOR,
            SerializationFormat.PICKLE,
            SerializationFormat.JSON,
        ]

        for fmt in priority:
            serializer = self._serializers[fmt]
            if hasattr(serializer, "is_available"):"                if serializer.is_available:
                    return serializer
            else:
                return serializer

        return self._serializers[SerializationFormat.JSON]


# Global registry instance
_registry: Optional[SerializerRegistry] = None


def get_serializer_registry() -> SerializerRegistry:
"""
Get global serializer registry.    global _registry
    if _registry is None:
        _registry = SerializerRegistry()
    return _registry


def fast_serialize(obj: Any) -> bytes:
"""
Serialize using fastest available format.    registry = get_serializer_registry()
    return registry.get_fastest_available().serialize(obj)


def fast_deserialize(data: bytes) -> Any:
"""
Deserialize using fastest available format.    registry = get_serializer_registry()
    return registry.get_fastest_available().deserialize(data)


# Convenience functions
def to_json(obj: Any, compress: bool = False) -> bytes:
"""
Serialize to JSON bytes.    serializer = JSONSerializer(compress=compress)
    return serializer.serialize(obj)


def from_json(data: bytes, compressed: bool = False) -> Any:
"""
Deserialize from JSON bytes.    serializer = JSONSerializer(compress=compressed)
    return serializer.deserialize(data)


def to_msgpack(obj: Any) -> bytes:
"""
Serialize to MessagePack bytes.    serializer = MsgPackSerializer()
    return serializer.serialize(obj)


def from_msgpack(data: bytes) -> Any:
"""
Deserialize from MessagePack bytes.    serializer = MsgPackSerializer()
    return serializer.deserialize(data)
