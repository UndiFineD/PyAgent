# SecretManager

**File**: `src\classes\fleet\SecretManager.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 57  
**Complexity**: 6 (moderate)

## Overview

Secret manager for production environments.
Mocks integration with Azure Key Vault or HashiCorp Vault.

## Classes (1)

### `SecretManager`

Provides secure access to credentials and API keys.
Shell for SecretCore.

**Methods** (6):
- `__init__(self, provider)`
- `_fetch_local(self, key)`
- `_fetch_azure(self, key)`
- `_fetch_vault(self, key)`
- `get_secret(self, key)`
- `set_secret(self, key, value)`

## Dependencies

**Imports** (4):
- `SecretCore.SecretCore`
- `logging`
- `os`
- `typing.Optional`

---
*Auto-generated documentation*
