#!/usr/bin/env python3

"""
LLM_CONTEXT_START

## Source: src-old/classes/fleet/SecretManager.description.md

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
## Source: src-old/classes/fleet/SecretManager.improvements.md

# Improvements for SecretManager

**File**: `src\classes\fleet\SecretManager.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 57 lines (small)  
**Complexity**: 6 score (moderate)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `SecretManager_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""Secret manager for production environments.
Mocks integration with Azure Key Vault or HashiCorp Vault.
"""

import os
import logging
from typing import Optional
from .SecretCore import SecretCore


class SecretManager:
    """
    Provides secure access to credentials and API keys.
    Shell for SecretCore.
    """

    def __init__(self, provider: str = "local") -> None:
        self.provider = provider
        self.core = SecretCore()
        self._cache = {}
        self.providers = {
            "local": self._fetch_local,
            "azure": self._fetch_azure,
            "vault": self._fetch_vault,
        }

    def _fetch_local(self, key: str) -> Optional[str]:
        return os.getenv(key)

    def _fetch_azure(self, key: str) -> Optional[str]:
        logging.info(f"{self.core.get_provider_prefix('azure')} Fetching {key}")
        return self._cache.get(key) or os.getenv(key)

    def _fetch_vault(self, key: str) -> Optional[str]:
        logging.info(f"{self.core.get_provider_prefix('vault')} Fetching {key}")
        return self._cache.get(key) or os.getenv(key)

    def get_secret(self, key: str) -> Optional[str]:
        """Retrieves a secret from the configured provider."""
        if key in self._cache:
            return self._cache[key]

        fetch_func = self.providers.get(self.provider, self._fetch_local)
        value = fetch_func(key)

        if value:
            masked = self.core.mask_secret(value)
            logging.info(f"Retrieved secret {key} -> {masked}")
            return value

        return None

    def set_secret(self, key: str, value: str) -> None:
        """Sets a secret (mocked)."""
        self._cache[key] = value
        logging.info(f"Secret {key} stored in {self.provider} cache.")
