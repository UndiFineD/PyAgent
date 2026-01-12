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


"""Auto-extracted class from agent_coder.py"""




from src.core.base.types.MigrationRule import MigrationRule
from src.core.base.types.MigrationStatus import MigrationStatus

from src.core.base.BaseAgent import BaseAgent
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
import ast
import hashlib
import logging
import math
import re
import shutil
import subprocess
import tempfile

class MigrationManager:
    """Manages code migration from old APIs to new ones.

    This class provides functionality to define migration rules,
    apply them to code, and track migration status.

    Attributes:
        rules: List of migration rules.

    Example:
        >>> manager=MigrationManager()
        >>> manager.add_rule(MigrationRule(
        ...     name="urllib2_to_urllib",
        ...     old_pattern=r"import urllib2",
        ...     new_pattern="import urllib.request",
        ...     description="Migrate urllib2 to urllib.request"
        ... ))
        >>> code, results=manager.apply_migrations("import urllib2")
    """

    def __init__(self) -> None:
        """Initialize the migration manager."""
        self.rules: List[MigrationRule] = []

    def add_rule(self, rule: MigrationRule) -> None:
        """Add a migration rule.

        Args:
            rule: The migration rule to add.
        """
        self.rules.append(rule)

    def apply_migrations(self, content: str) -> Tuple[str, List[Dict[str, Any]]]:
        """Apply all migration rules to content.

        Args:
            content: The source code to migrate.

        Returns:
            Tuple of migrated content and list of applied migrations.
        """
        result = content
        applied: List[Dict[str, Any]] = []

        for rule in self.rules:
            if rule.status == MigrationStatus.SKIPPED:
                continue
            rule.status = MigrationStatus.IN_PROGRESS
            new_result = re.sub(rule.old_pattern, rule.new_pattern, result)
            if new_result != result:
                applied.append({
                    "rule": rule.name,
                    "description": rule.description,
                    "breaking_change": rule.breaking_change
                })
                rule.status = MigrationStatus.COMPLETED
                result = new_result
            else:
                rule.status = MigrationStatus.PENDING

        return result, applied

    def get_pending_migrations(self) -> List[MigrationRule]:
        """Get list of pending migration rules.

        Returns:
            List of rules with pending status.
        """
        return [r for r in self.rules if r.status == MigrationStatus.PENDING]
