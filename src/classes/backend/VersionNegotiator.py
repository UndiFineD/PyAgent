#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from .BackendVersion import BackendVersion

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from queue import PriorityQueue
from typing import Any, Callable, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import os
import re
import subprocess
import threading
import time
import uuid

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
        self._versions: Dict[str, BackendVersion] = {}
        self._client_version = "1.0"

    def register_backend(
        self,
        backend: str,
        version: str,
        capabilities: Optional[List[str]] = None,
        api_version: str = "v1",
    ) -> BackendVersion:
        """Register backend version information.

        Args:
            backend: Backend identifier.
            version: Backend version string.
            capabilities: List of supported capabilities.
            api_version: API version string.

        Returns:
            BackendVersion: Registered version info.
        """
        backend_version = BackendVersion(
            backend=backend,
            version=version,
            capabilities=capabilities or [],
            api_version=api_version,
        )
        self._versions[backend] = backend_version
        return backend_version

    def negotiate(
        self,
        backend: str,
        required: Optional[List[str]] = None,
    ) -> Optional[BackendVersion]:
        """Negotiate version with backend.

        Args:
            backend: Backend to negotiate with.
            required: Required capabilities.

        Returns:
            Optional[BackendVersion]: Negotiated version or None if incompatible.
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

    def get_all_versions(self) -> Dict[str, BackendVersion]:
        """Get all registered backend versions."""
        return dict(self._versions)
