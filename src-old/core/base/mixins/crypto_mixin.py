#!/usr/bin/env python3
"""
LLM_CONTEXT_START

## Source: src-old/core/base/mixins/crypto_mixin.description.md

# crypto_mixin

**File**: `src\core\base\mixins\crypto_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 6 imports  
**Lines**: 53  
**Complexity**: 5 (moderate)

## Overview

Module: crypto_mixin
Cryptography mixin for BaseAgent, implementing DPAPI and AES operations.
Inspired by ADSyncDump-BOF decryption patterns.

## Classes (1)

### `CryptoMixin`

Mixin providing cryptographic operations for Windows environments.

**Methods** (5):
- `__init__(self)`
- `decrypt_dpapi_blob(self, encrypted_data, entropy)`
- `decrypt_aes_cbc(self, key, iv, encrypted_data)`
- `base64_decode(self, encoded_data)`
- `read_windows_credential(self, target_name)`

## Dependencies

**Imports** (6):
- `__future__.annotations`
- `base64`
- `platform`
- `src.core.base.logic.processing.crypto_core.CryptoCore`
- `typing.Any`
- `typing.Optional`

---
*Auto-generated documentation*
## Source: src-old/core/base/mixins/crypto_mixin.improvements.md

# Improvements for crypto_mixin

**File**: `src\core\base\mixins\crypto_mixin.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 53 lines (small)  
**Complexity**: 5 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `crypto_mixin_test.py` with pytest tests

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
Module: crypto_mixin
Cryptography mixin for BaseAgent, implementing DPAPI and AES operations.
Inspired by ADSyncDump-BOF decryption patterns.
"""


import base64
import platform
from typing import Any, Optional

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
