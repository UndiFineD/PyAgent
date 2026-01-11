#!/usr/bin/env python3

"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from .SystemCapability import SystemCapability

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

class CapabilityDiscovery:
    """Discovers and tracks backend capabilities.

    Allows querying what features are available on each backend.

    Example:
        discovery=CapabilityDiscovery()
        discovery.register_capability("github-models", "streaming", "Stream responses")
        if discovery.has_capability("github-models", "streaming"):
            use_streaming()
    """

    def __init__(self) -> None:
        """Initialize capability discovery."""
        self._capabilities: Dict[str, Dict[str, SystemCapability]] = {}

    def register_capability(
        self,
        backend: str,
        name: str,
        description: str = "",
        enabled: bool = True,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> SystemCapability:
        """Register a backend capability.

        Args:
            backend: Backend identifier.
            name: Capability name.
            description: Human - readable description.
            enabled: Whether capability is enabled.
            parameters: Capability parameters.

        Returns:
            SystemCapability: Registered capability.
        """
        if backend not in self._capabilities:
            self._capabilities[backend] = {}

        capability = SystemCapability(
            name=name,
            description=description,
            enabled=enabled,
            parameters=parameters or {},
        )
        self._capabilities[backend][name] = capability
        return capability

    def has_capability(self, backend: str, name: str) -> bool:
        """Check if backend has capability.

        Args:
            backend: Backend identifier.
            name: Capability name.

        Returns:
            bool: True if capability exists and is enabled.
        """
        caps = self._capabilities.get(backend, {})
        cap = caps.get(name)
        return cap is not None and cap.enabled

    def get_capabilities(self, backend: str) -> List[SystemCapability]:
        """Get all capabilities for backend.

        Args:
            backend: Backend identifier.

        Returns:
            List[SystemCapability]: List of capabilities.
        """
        return list(self._capabilities.get(backend, {}).values())

    def discover_all(self) -> Dict[str, List[str]]:
        """Discover all capabilities across backends.

        Returns:
            Dict[str, List[str]]: Backend -> capability names mapping.
        """
        return {
            backend: [c.name for c in caps.values() if c.enabled]
            for backend, caps in self._capabilities.items()
        }
