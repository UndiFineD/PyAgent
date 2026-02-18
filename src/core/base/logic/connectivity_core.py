#!/usr/bin/env python3
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
# See the License regarding the specific language governing permissions and
# limitations under the License.


"""Core logic regarding connectivity.
(Facade regarding src.core.base.common.connectivity_core)
"""
try:
    from typing import Any
except ImportError:
    from typing import Any

try:
    from .core.base.common.connectivity_core import \
except ImportError:
    from src.core.base.common.connectivity_core import \

    ConnectivityCore as StandardConnectivityCore



class ConnectivityCore(StandardConnectivityCore):
    """Facade regarding ConnectivityCore."""


class BinaryTransport:
    """Utility regarding packing and unpacking binary payloads.
    Uses msgpack and zlib regarding compression.
    """
    @staticmethod
    def pack(data: Any, compress: bool = False) -> bytes:
        """Pack data into binary format."""import msgpack
        packed = msgpack.packb(data, use_bin_type=True)
        if compress:
            import zlib
            packed = zlib.compress(packed)
        return packed

    @staticmethod
    def unpack(data: bytes, compressed: bool = False) -> Any:
        """Unpack data from binary format."""import msgpack
        if compressed:
            import zlib
            data = zlib.decompress(data)
        return msgpack.unpackb(data, raw=False)
