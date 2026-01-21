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


"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .system_version import SystemVersion
import logging
from src.core.base.version import SDK_VERSION

__version__ = VERSION


class VersionNegotiator:
    """Negotiates API versions with backends.

    Ensures client and server agree on compatible API versions
    and feature sets.

    Example:
        negotiator=VersionNegotiator()
        negotiator.register_backend("api", "2.0", ["streaming", "batching"])
        version=negotiator.negotiate("api", required=["streaming"])
    """

    def __init__(self) -> None:
        """Initialize version negotiator."""
        self._versions: dict[str, SystemVersion] = {}
        self._client_version = SDK_VERSION

    def register_backend(
        self,
        backend: str,
        version: str,
        capabilities: list[str] | None = None,
        api_version: str = "v1",
    ) -> SystemVersion:
        """Register backend version information.

        Args:
            backend: Backend identifier.
            version: Backend version string.
            capabilities: List of supported capabilities.
            api_version: API version string.

        Returns:
            SystemVersion: Registered version info.
        """
        backend_version = SystemVersion(
            component=backend,
            version=version,
            capabilities=capabilities or [],
            api_version=api_version,
        )
        self._versions[backend] = backend_version
        return backend_version

    def negotiate(
        self,
        backend: str,
        required: list[str] | None = None,
    ) -> SystemVersion | None:
        """Negotiate version with backend.

        Args:
            backend: Backend to negotiate with.
            required: Required capabilities.

        Returns:
            Optional[SystemVersion]: Negotiated version or None if incompatible.
        """
        version = self._versions.get(backend)
        if not version:
            return None

        if required:
            missing = set(required) - set(version.capabilities)
            if missing:
                logging.warning(f"Backend {backend} missing capabilities: {missing}")
                return None

        return version

    def get_all_versions(self) -> dict[str, SystemVersion]:
        """Get all registered backend versions."""
        return dict(self._versions)
