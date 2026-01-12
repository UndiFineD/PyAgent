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




from .ExecutionCondition import ExecutionCondition

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

class ConditionalExecutor:
    """Execute agents based on file content conditions.

    Example:
        executor=ConditionalExecutor()
        executor.add_condition("has_todos", lambda p, c: "TODO" in c)
        executor.add_condition("is_large", lambda p, c: len(c) > 10000)

        if executor.should_execute("coder", file_path, content):
            run_coder(file_path)
    """

    def __init__(self) -> None:
        """Initialize executor."""
        self._conditions: Dict[str, ExecutionCondition] = {}
        self._agent_conditions: Dict[str, Dict[str, Any]] = {}

    def add_condition(
        self,
        name: str,
        check: Callable[[Path, str], bool],
        description: str = "",
    ) -> None:
        """Add a condition.

        Args:
            name: Condition name.
            check: Function taking (path, content) returning bool.
            description: Human - readable description.
        """
        self._conditions[name] = ExecutionCondition(
            name=name,
            check=check,
            description=description,
        )

    def set_agent_conditions(
        self,
        agent_name: str,
        conditions: List[str],
        require_all: bool = False,
    ) -> None:
        """Set conditions for an agent.

        Args:
            agent_name: Name of the agent.
            conditions: List of condition names.
            require_all: If True, all conditions must pass.
        """
        self._agent_conditions[agent_name] = {
            "conditions": conditions,
            "require_all": require_all,
        }

    def should_execute(
        self,
        agent_name: str,
        file_path: Path,
        content: str,
    ) -> bool:
        """Check if agent should execute for file.

        Args:
            agent_name: Agent name.
            file_path: File path.
            content: File content.

        Returns:
            True if agent should execute.
        """
        if agent_name not in self._agent_conditions:
            return True  # No conditions, always execute

        config = self._agent_conditions[agent_name]
        condition_names: List[str] = config["conditions"]  # type: ignore
        require_all = config["require_all"]

        results: list[bool] = []
        for cond_name in condition_names:
            if cond_name not in self._conditions:
                continue
            condition = self._conditions[cond_name]
            try:
                results.append(condition.check(file_path, content))
            except Exception:
                results.append(False)

        if not results:
            return True

        if require_all:
            return all(results)
        else:
            return any(results)
