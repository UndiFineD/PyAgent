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
__version__ = VERSION

# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.


"""Auto-extracted class from agent.py"""




from src.core.base.models import AgentHealthCheck, AgentPriority, HealthStatus

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from types import TracebackType
from typing import List, Set, Optional, Dict, Any, Callable, Iterable, TypeVar, cast, Final
import argparse
import asyncio
import difflib
import fnmatch
import functools
import hashlib
import importlib.util
import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time
import uuid

class AgentPluginBase(ABC):
    """Abstract base class for agent plugins.

    Provides interface for third - party agents to integrate with
    the agent orchestrator without modifying core code.

    Attributes:
        name: Plugin name.
        priority: Execution priority.
        config: Plugin configuration.
    """

    def __init__(self, name: str, priority: AgentPriority = AgentPriority.NORMAL,
                 config: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the plugin.

        Args:
            name: Unique plugin name.
            priority: Execution priority.
            config: Plugin - specific configuration.
        """
        self.name = name
        self.priority = priority
        self.config = config or {}
        self.logger = logging.getLogger(f"plugin.{name}")

    @abstractmethod
    def run(self, file_path: Path, context: Dict[str, Any]) -> bool:
        """Execute the plugin on a file.

        Args:
            file_path: Path to the file to process.
            context: Execution context with agent state.

        Returns:
            bool: True if changes were made, False otherwise.
        """
        raise NotImplementedError()

    def setup(self) -> None:
        """Called once when plugin is loaded. Override for initialization."""
        pass

    @abstractmethod
    def health_check(self) -> AgentHealthCheck:
        """Verify plugin health and dependency status.

        Returns:
            AgentHealthCheck: Health status and details.
        """
        raise NotImplementedError()

    @abstractmethod
    def shutdown(self) -> None:
        """Handle graceful shutdown, cleanup resources, and terminate processes."""
        raise NotImplementedError()
        pass

    def teardown(self) -> None:
        """Called once when plugin is unloaded. Override for cleanup."""
        pass

    def health_check(self) -> AgentHealthCheck:
        """Check plugin health status.

        Returns:
            AgentHealthCheck: Health check result.
        """
        return AgentHealthCheck(
            agent_name=self.name,
            status=HealthStatus.HEALTHY
        )
