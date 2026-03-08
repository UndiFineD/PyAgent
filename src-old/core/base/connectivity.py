#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/connectivity.description.md

# connectivity

**File**: `src\core\base\connectivity.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 8 imports  
**Lines**: 102  
**Complexity**: 5 (moderate)

## Overview

Modern connectivity module providing high-performance binary transport.
Supports MessagePack for serialization and Zstd for compression (Phase 255).

## Classes (2)

### `BinaryTransport`

Handles binary serialization and compression for agent communication.
Utilizes MessagePack and Zstd for optimal performance.

**Methods** (2):
- `pack(data, compress, level)`
- `unpack(payload, compressed)`

### `HeartbeatSignal`

Specialized structure for high-frequency heartbeat signals.
Optimized for BinaryTransport.

**Methods** (3):
- `__init__(self, agent_id, status, load)`
- `to_dict(self)`
- `from_dict(cls, data)`

## Dependencies

**Imports** (8):
- `__future__.annotations`
- `logging`
- `msgpack`
- `src.core.base.version.VERSION`
- `typing.Any`
- `typing.Optional`
- `typing.Union`
- `zstd`

---
*Auto-generated documentation*
## Source: src-old/core/base/connectivity.improvements.md

# Improvements for connectivity

**File**: `src\core\base\connectivity.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 102 lines (medium)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `connectivity_test.py` with pytest tests

## Best Practices Checklist

- [x] All classes have docstrings
- [x] All public methods have docstrings
- [x] Type hints are present
- [x] pytest tests cover main functionality
- [x] Error handling is robust
- [x] Code follows PEP 8 style guide
- [x] No code duplication
- [x] Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

from __future__ import annotations

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Modern connectivity module providing high-performance binary transport.
Supports MessagePack for serialization and Zstd for compression (Phase 255).
"""

import msgpack
import zstd
import logging
from typing import Any, Optional, Union
from src.core.base.version import VERSION

__version__ = VERSION
logger = logging.getLogger(__name__)


class BinaryTransport:
    """
    Handles binary serialization and compression for agent communication.
    Utilizes MessagePack and Zstd for optimal performance.
    """

    @staticmethod
    def pack(data: Any, compress: bool = False, level: int = 3) -> bytes:
        """
        Serializes data using MessagePack and optionally compresses with Zstd.

        Args:
            data: The data to serialize.
            compress: Whether to apply Zstd compression.
            level: Zstd compression level (1-22).

        Returns:
            bytes: The packed (and possibly compressed) data.
        """
        try:
            packed = msgpack.packb(data, use_bin_type=True)
            if compress:
                return zstd.compress(packed, level)
            return packed
        except Exception as e:
            logger.error(f"BinaryTransport.pack failed: {e}")
            raise

    @staticmethod
    def unpack(payload: bytes, compressed: bool = False) -> Any:
        """
        Decompresses (optionally) and deserializes data using MessagePack.

        Args:
            payload: The bytes to unpack.
            compressed: Whether the payload is Zstd compressed.

        Returns:
            Any: The unpacked data.
        """
        try:
            data = payload
            if compressed:
                data = zstd.decompress(payload)
            return msgpack.unpackb(data, raw=False)
        except Exception as e:
            logger.error(f"BinaryTransport.unpack failed: {e}")
            raise


class HeartbeatSignal:
    """
    Specialized structure for high-frequency heartbeat signals.
    Optimized for BinaryTransport.
    """

    def __init__(self, agent_id: str, status: str, load: float = 0.0) -> None:
        self.agent_id = agent_id
        self.status = status
        self.load = load
        self.timestamp = __import__("time").time()

    def to_dict(self) -> dict:
        return {
            "a": self.agent_id,
            "s": self.status,
            "l": self.load,
            "t": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> HeartbeatSignal:
        signal = cls(data["a"], data["s"], data.get("l", 0.0))
        signal.timestamp = data.get("t", 0.0)
        return signal
