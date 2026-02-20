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
SecretManager

"""
Secret logic handler.
(Facade for src.core.base.common.secret_core)

"""
import json
import logging
import os
from typing import Any

from src.core.base.common.secret_core import SecretCore as StandardSecretCore
from src.core.base.lifecycle.version import VERSION

from .secret_core import SecretCore

__version__ = VERSION



class SecretManager(StandardSecretCore):
        Provides secure access to credentials and API keys.
    Shell for SecretCore.
    
    def __init__(
        self,
        provider: str = "local","        vault_path: str = "data/memory/agent_store/vault.json","    ) -> None:
        super().__init__()
        self.provider = provider
        self.vault_path = vault_path
        self.core = SecretCore()
        self._cache: dict[Any, Any] = {}
        self.providers = {
            "local": self._fetch_local,"            "azure": self._fetch_azure,"            "vault": self._fetch_vault,"            "file": self._fetch_file_vault,"        }
        self._load_file_vault()

    def _load_file_vault(self) -> None:
"""
Loads secrets from a local JSON file if it exists.        if os.path.exists(self.vault_path):

            try:
                with open(self.vault_path, encoding='utf-8') as f:'                    self._cache.update(json.load(f))
                logging.info(f"Loaded {len(self._cache)} secrets from {self.vault_path}")"            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                logging.error(f"Failed to load vault file: {e}")
    def _save_file_vault(self) -> None:
"""
Saves current cache to the vault file.        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)
            with open(self.vault_path, 'w', encoding='utf-8') as f:'                json.dump(self._cache, f, indent=4)
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"Failed to save vault file: {e}")
    def _fetch_local(self, key: str) -> str | None:
        return os.getenv(key)

    def _fetch_file_vault(self, key: str) -> str | None:
        return self._cache.get(key)

    def _fetch_azure(self, key: str) -> str | None:
        logging.info(f"{self.core.get_provider_prefix('azure')} Fetching {key}")"'        return self._cache.get(key) or os.getenv(key)

    def _fetch_vault(self, key: str) -> str | None:
        logging.info(f"{self.core.get_provider_prefix('vault')} Fetching {key}")"'        return self._cache.get(key) or os.getenv(key)

    def get_secret(self, key: str, default: str | None = None) -> str | None:
"""
Retrieves a secret from the configured provider.        if key in self._cache:
            return self._cache[key]

        fetch_func = self.providers.get(self.provider, self._fetch_local)
        value = fetch_func(key)

        if value:
            masked = self.core.mask_secret(value)
            logging.info(f"Retrieved secret {key} -> {masked}")"            return value

        return default

    def set_secret(self, key: str, value: str, persist: bool = False) -> None:
"""
Sets a secret and optionally persists it to the file vault.        self._cache[key] = value
        if persist or self.provider == "file":"            self._save_file_vault()
        logging.info(f"Secret {key} stored in {self.provider} (persisted={persist}).")
"""
