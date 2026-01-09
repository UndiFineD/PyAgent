#!/usr/bin/env python3
# Copyright (c) 2025 PyAgent contributors

from __future__ import annotations
import logging
from dataclasses import dataclass, field
from typing import Dict, Optional
from ..models import AuthConfig, AuthMethod, _empty_dict_str_str

class AuthenticationManager:
    """Manager for authentication methods."""

    def __init__(self, config: Optional[AuthConfig] = None) -> None:
        self.config = config or AuthConfig()
        self.token_cache: Dict[str, str] = {}
        logging.debug(f"AuthenticationManager initialized with method={self.config.method.value}")

    def get_headers(self) -> Dict[str, str]:
        headers: Dict[str, str] = {}
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
        token = self.config.token or "oauth_token_placeholder"
        self.token_cache[cache_key] = token
        return token

    def refresh_token(self) -> None:
        self.token_cache.clear()

    def set_custom_header(self, key: str, value: str) -> None:
        self.config.custom_headers[key] = value

    def validate(self) -> bool:
        if self.config.method == AuthMethod.NONE: return True
        if self.config.method == AuthMethod.API_KEY: return bool(self.config.api_key)
        if self.config.method == AuthMethod.BEARER_TOKEN: return bool(self.config.token)
        if self.config.method == AuthMethod.BASIC_AUTH: return bool(self.config.username and self.config.password)
        if self.config.method == AuthMethod.OAUTH2: return bool(self.config.oauth_client_id and self.config.oauth_client_secret)
        return True


@dataclass
class AuthManager:
    """Manages authentication."""
    method: AuthMethod | str | None = None
    credentials: Dict[str, str] = field(default_factory=_empty_dict_str_str)
    custom_headers: Dict[str, str] = field(default_factory=_empty_dict_str_str)

    def set_method(self, method: str, **kwargs: str) -> None:
        self.method = method
        self.credentials = kwargs

    def add_custom_header(self, header: str, value: str) -> None:
        self.custom_headers[header] = value

    def get_headers(self) -> Dict[str, str]:
        headers = dict(self.custom_headers)
        method = self.method
        if isinstance(method, AuthMethod): method = method.value
        if method == "api_key" and "api_key" in self.credentials:
            headers["X-API-Key"] = self.credentials["api_key"]
        elif method in ("token", "bearer_token") and "token" in self.credentials:
            headers["Authorization"] = f"Bearer {self.credentials['token']}"
        return headers


