#!/usr/bin/env python3
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


from __future__ import annotations
from src.core.base.version import VERSION
import logging
from dataclasses import dataclass, field
from src.core.base.models import AuthConfig, AuthMethod
from src.core.base.models.base_models import _empty_dict_str_str

__version__ = VERSION


class AuthenticationManager:
    """Manager for authentication methods."""

    def __init__(self, config: AuthConfig | None = None) -> None:
        self.config = config or AuthConfig()
        self.token_cache: dict[str, str] = {}
        logging.debug(
            f"AuthenticationManager initialized with method={self.config.method.value}"
        )

    def get_headers(self) -> dict[str, str]:
        headers: dict[str, str] = {}
        if self.config.method == AuthMethod.API_KEY:
            headers["X-API-Key"] = self.config.api_key
        elif self.config.method == AuthMethod.BEARER_TOKEN:
            headers["Authorization"] = f"Bearer {self.config.token}"
        elif self.config.method == AuthMethod.BASIC_AUTH:
            import base64

            credentials = f"{self.config.username}:{self.config.password}"
            encoded = base64.b64encode(credentials.encode()).decode()
            headers["Authorization"] = f"Basic {encoded}"
        elif self.config.method == AuthMethod.OAUTH2:
            token = self._get_oauth_token()
            headers["Authorization"] = f"Bearer {token}"
        headers.update(self.config.custom_headers)
        return headers

    def _get_oauth_token(self) -> str:
        cache_key = f"oauth_{self.config.oauth_client_id}"
        if cache_key in self.token_cache:
            return self.token_cache[cache_key]
        token = self.config.token
        if not token:
            logging.error(f"OAuth token missing for {cache_key}")
            return ""

        self.token_cache[cache_key] = token
        return token

    def refresh_token(self) -> None:
        self.token_cache.clear()

    def set_custom_header(self, key: str, value: str) -> None:
        self.config.custom_headers[key] = value

    def validate(self) -> bool:
        if self.config.method == AuthMethod.NONE:
            return True

        if self.config.method == AuthMethod.API_KEY:
            return bool(self.config.api_key)
        if self.config.method == AuthMethod.BEARER_TOKEN:
            return bool(self.config.token)
        if self.config.method == AuthMethod.BASIC_AUTH:
            return bool(self.config.username and self.config.password)
        if self.config.method == AuthMethod.OAUTH2:
            return bool(self.config.oauth_client_id and self.config.oauth_client_secret)
        return True


@dataclass
class AuthManager:
    """Manages authentication."""

    method: AuthMethod | str | None = None
    credentials: dict[str, str] = field(default_factory=_empty_dict_str_str)
    custom_headers: dict[str, str] = field(default_factory=_empty_dict_str_str)

    def set_method(self, method: str, **kwargs: str) -> None:
        self.method = method
        self.credentials = kwargs

    def add_custom_header(self, header: str, value: str) -> None:
        self.custom_headers[header] = value

    def get_headers(self) -> dict[str, str]:
        headers = dict(self.custom_headers)
        method = self.method
        if isinstance(method, AuthMethod):
            method = method.value
        if method == "api_key" and "api_key" in self.credentials:
            headers["X-API-Key"] = self.credentials["api_key"]
        elif method in ("token", "bearer_token") and "token" in self.credentials:
            headers["Authorization"] = f"Bearer {self.credentials['token']}"
        return headers
