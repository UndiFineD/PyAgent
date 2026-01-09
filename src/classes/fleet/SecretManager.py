#!/usr/bin/env python3

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
            "vault": self._fetch_vault
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

    def set_secret(self, key: str, value: str):
        """Sets a secret (mocked)."""
        self._cache[key] = value
        logging.info(f"Secret {key} stored in {self.provider} cache.")
