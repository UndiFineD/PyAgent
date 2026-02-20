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
# See the License for the specific language governing permissions and
# limitations under the License.


"""Module: crypto_mixin
Cryptography mixin for BaseAgent, implementing DPAPI and AES operations.
Inspired by ADSyncDump-BOF decryption patterns.
"""


from __future__ import annotations


try:
    import platform
except ImportError:
    import platform

try:
    from typing import Any, Optional
except ImportError:
    from typing import Any, Optional


try:
    from .core.base.logic.processing.crypto_core import CryptoCore
except ImportError:
    from src.core.base.logic.processing.crypto_core import CryptoCore




class CryptoMixin:
    """Mixin providing cryptographic operations for Windows environments."""
    def __init__(self, **kwargs: Any) -> None:
        if platform.system() != "Windows":
            raise RuntimeError("CryptoMixin is only supported on Windows")
        self.crypto_core = CryptoCore()

    def decrypt_dpapi_blob(self, encrypted_data: bytes, entropy: Optional[bytes] = None) -> Optional[bytes]:
        """Decrypt data using Windows DPAPI."""
        return self.crypto_core.decrypt_dpapi_blob(encrypted_data, entropy)

    def decrypt_aes_cbc(self, key: bytes, iv: bytes, encrypted_data: bytes) -> Optional[bytes]:
        """Decrypt data using AES-CBC."""
        return self.crypto_core.decrypt_aes_cbc(key, iv, encrypted_data)

    def base64_decode(self, encoded_data: str) -> Optional[bytes]:
        """Decode base64 string to bytes."""
        return self.crypto_core.base64_decode(encoded_data)

    def read_windows_credential(self, target_name: str) -> Optional[bytes]:
        """Read encrypted credential blob from Windows Credential Manager."""
        return self.crypto_core.read_windows_credential(target_name)
