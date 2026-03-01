# crypto_core

**File**: `src\core\base\logic\processing\crypto_core.py`  
**Type**: Python Module  
**Summary**: 3 classes, 0 functions, 5 imports  
**Lines**: 192  
**Complexity**: 5 (moderate)

## Overview

Module: crypto_core
Core logic for cryptographic operations.
Implements DPAPI and AES decryption patterns from ADSyncDump-BOF.

## Classes (3)

### `DATA_BLOB`

**Inherits from**: Structure

Class DATA_BLOB implementation.

### `CREDENTIALW`

**Inherits from**: Structure

Class CREDENTIALW implementation.

### `CryptoCore`

Core class for cryptographic operations.

**Methods** (5):
- `__init__(self)`
- `decrypt_dpapi_blob(self, encrypted_data, entropy)`
- `decrypt_aes_cbc(self, key, iv, encrypted_data)`
- `base64_decode(self, encoded_data)`
- `read_windows_credential(self, target_name)`

## Dependencies

**Imports** (5):
- `__future__.annotations`
- `base64`
- `ctypes`
- `ctypes.wintypes`
- `typing.Optional`

---
*Auto-generated documentation*
