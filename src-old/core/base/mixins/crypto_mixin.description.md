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
